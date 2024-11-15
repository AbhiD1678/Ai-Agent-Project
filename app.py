import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
from gspread.exceptions import APIError
import serpapi
from groq import Groq

# Load environment variables
load_dotenv()

# Set up API keys for SerpAPI and Groq
serp_api_key = os.getenv("SERPAPI_KEY")
serp_client = serpapi.Client(api_key=serp_api_key)
groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key)

# Path to your service account credentials JSON file
creds_file = 'google_credentials.json'
st.title("Entity Search and Extraction App")
st.markdown("This app helps you search for entities and extract information from search results using SerpAPI and Groq. Made by **Abhishek Dubey**")

# Option to select CSV or Google Sheets
option = st.selectbox('Proceed with a CSV file or Google Sheet?', ['', 'CSV', 'Google Sheet'])

# Initialize DataFrame for the selected data
df = pd.DataFrame()

# Load data based on user selection
if option == "CSV":
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("CSV Data Preview:")
        st.dataframe(df)

elif option == "Google Sheet":
    # User inputs Google Sheets URL
    gsheet_url = st.text_input("Enter the Google Sheets URL:")
    
    # Proceed only if URL is provided
    if gsheet_url:
        try:
            # Authenticate and read data from Google Sheets
            creds = Credentials.from_service_account_file(creds_file, scopes=["https://www.googleapis.com/auth/spreadsheets"])
            gc = gspread.authorize(creds)
            export_to_gsheet = st.checkbox("Export extracted data back to Google Sheet")
            spreadsheet = gc.open_by_url(gsheet_url)
            worksheet = spreadsheet.sheet1
            df = pd.DataFrame(worksheet.get_all_records())
            st.write("Google Sheet Data Preview:")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error fetching data from Google Sheets: {e}")

# Only proceed if data is loaded
if not df.empty:
    primary_column = st.selectbox("Select the primary column for entity search:", df.columns)
    rows_to_search = st.number_input("Number of rows to search:", min_value=1, max_value=len(df), value=1)
    user_defined_prompt = st.text_input("Enter the information to extract (e.g., 'Extract the email address of {company}')")

    # User clicks search button to initiate process
    if st.button("Search and Extract"):
        search_results = []
        extraction_results = []

        for value in df[primary_column].head(rows_to_search):
            custom_prompt = user_defined_prompt.replace("{company}", str(value))
            st.write(f"Searching for: {value}")

            # Retrieve search results from SerpAPI
            try:
                result = serp_client.search(
                    q=custom_prompt,
                    engine='google',
                    location='India',
                    hl='en',
                    gl='in'
                )
                entity_results = {
                    "entity": value,
                    "prompt": custom_prompt,
                    "results": result.get("organic_results", [])
                }
                search_results.append(entity_results)

                # Prepare text for LLM
                results_text = "\n".join([f"Results: {r['snippet']}" for r in entity_results['results']])
                if not results_text.strip():
                    results_text = "No results found"

                # Send to Groq API for extraction
                chat_completion = groq_client.chat.completions.create(
                    messages=[{
                        "role": "user",
                        "content": f"You will be given a prompt with a dataset in it,if the required thing mentioned in prompt is available in the dataset,if there are multiple answers for it,separate them with commas,extract it and give that data in your reply only,no extra information is needed,if no data is available then reply with No data available only,{custom_prompt} from the following search results:\n{results_text} and dont repeat the prompt,give the answer"
                    }],
                    model="llama3-8b-8192",
                )

                extracted_data = chat_completion.choices[0].message.content.strip() or "No data available"
                extraction_results.append({
                    "entity": value,
                    "prompt": custom_prompt,
                    "extracted_data": extracted_data
                })

            except Exception as api_error:
                st.error(f"Error in API call for {value}: {api_error}")
                extraction_results.append({
                    "entity": value,
                    "prompt": custom_prompt,
                    "extracted_data": "API error occurred"
                })

        # Display the extracted results
        st.write("Extracted Information from Search Results:")
        extracted_df = pd.DataFrame(extraction_results)
        st.dataframe(extracted_df)

        # Provide download option for the extracted results as CSV
        csv_data = extracted_df.to_csv(index=False)
        st.download_button("Download Extracted Results as CSV", data=csv_data, file_name="extracted_results.csv", mime="text/csv")

        # Export to Google Sheet if the option was selected
        if option == "Google Sheet" and gsheet_url and export_to_gsheet:
            try:
                try:
                    worksheet = spreadsheet.worksheet("Sheet4")
                except gspread.exceptions.WorksheetNotFound:
                    worksheet = spreadsheet.add_worksheet(title="Sheet4", rows="100", cols="20")
                # Append extracted results to the Google Sheet
                worksheet.clear()  # Clear existing data if necessary
                set_with_dataframe(worksheet, extracted_df)  # Write DataFrame to Google Sheet
                st.success("Extracted results successfully exported to Google Sheet.")
            except APIError as api_error:
                st.error(f"Error exporting data to Google Sheets: {api_error}")
