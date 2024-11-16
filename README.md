# AI Agent

## Project Description

This project is a powerful Streamlit-based application that bridges the gap between data sources, web scraping, and AI-driven analysis. It allows users to connect to either a CSV file or Google Sheets, select an entity to iterate over, and perform automated internet scraping using the SERP API for a specific type of information.

The scraped results are processed by Groq AI (LLM) to extract meaningful insights related to the specified query. The output is displayed as a dataframe in Streamlit and can be downloaded as a CSV file. Additionally, users working with Google Sheets can append the results directly to their sheet.

### Key Features:
- **Flexible Input:** Connect to a CSV file or Google Sheets.
- **Custom Entity Selection:** Choose the entity to process via a user prompt.
- **Web Scraping:** Scrape specific information from the web using the SERP API.
- **AI-Driven Analysis:** Extract meaningful, query-specific information using Groq AI (LLM).
- **Intuitive Output:** View results in Streamlit and download them in CSV format.
- **Google Sheets Integration:** Update Google Sheets with the processed data.

## Setup Instructions

Follow these steps to set up and run the application:

### Prerequisites
- Python 3.8 or higher
- An IDE or text editor of your choice
- Required API keys for [SerpAPI](https://serpapi.com/) and [Groq AI](https://groq.com/)
- A Google Cloud project with access to Google Sheets and service account credentials (JSON file)

### Step 1: Clone the Repository
Clone this repository to your local machine using:
```bash
[git clone <repository-url>](https://github.com/AbhiD1678/Ai-Agent-Project.git)
cd Ai-Agent-Project
```

### Step 2: Install Dependencies
Install the required Python packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables
Create a `.env` file in the project root and add the following keys:
```
SERPAPI_KEY=your_serpapi_key
GROQ_API_KEY=your_groq_api_key
```

### Step 4: Add Google Service Account Credentials
Place your Google service account credentials JSON file in the project root and name it `google_credentials.json`. This is required for accessing Google Sheets.

### Step 5: Run the Application
Start the Streamlit app with the following command:
```bash
streamlit run app.py
```

### Step 6: Open the Application
Once the app is running, it will open in your default browser at `http://localhost:8501`. You can follow the on-screen instructions to upload a CSV file or connect a Google Sheet.

## Usage Guide

This section explains how to use the application, including connecting to data sources, running queries, and downloading results.

### Step 1: Launch the Application
1. Open your terminal and navigate to the project folder.
2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. The app will open in your default web browser at `http://localhost:8501`.

### Step 2: Choose Your Data Source
1. **CSV File**:
   - Select **CSV** in the dropdown.
   - Upload a CSV file using the file uploader.
   - Preview the uploaded data on the app interface.
   
2. **Google Sheets**:
   - Select **Google Sheet** in the dropdown.
   - Enter the URL of your Google Sheet.
   - Ensure the service account has access to the sheet.
   - Preview the loaded Google Sheet data in the app.

### Step 3: Define the Search Parameters
1. **Select the Primary Column**:
   - Choose the column that contains the entities you want to search for.
2. **Number of Rows to Search**:
   - Enter the number of rows (starting from the top) to process.
3. **Define the Search Query**:
   - Enter a user-defined prompt to specify the type of information you want to extract.
   - Use placeholders like `{company}` in your prompt, which will be dynamically replaced by the entity values from the selected column. Example:
     ```
     Extract the email address of {company}.
     ```

### Step 4: Start the Search and Extraction
1. Click **Search and Extract** to start:
   - The app will scrape the web for the defined search query using SerpAPI.
   - Extract meaningful information from the results using Groq AI.

### Step 5: Review the Results
1. The extracted data will be displayed as a table on the app.
2. Options to:
   - **Download as CSV**: Save the extracted results locally.
   - **Export to Google Sheets** (if using Google Sheets): Append the results to the same Google Sheet.

### Notes:
- Ensure the service account JSON file has the correct permissions for Google Sheets.
- The app processes one specific type of information per search query.

## API Keys and Environment Variables

To run this application, you need to configure API keys and environment variables. Follow these steps:

### Step 1: Create a `.env` File
1. In the root directory of your project, create a `.env` file.
2. Add the following environment variables:
   ```
   SERPAPI_KEY=your_serpapi_api_key
   GROQ_API_KEY=your_groq_ai_api_key
   ```

### Step 2: Obtain Your API Keys
1. **SerpAPI Key**:
   - Visit [SerpAPI](https://serpapi.com/) and sign up for an account.
   - Create an API key in your SerpAPI dashboard.
   - Copy and paste the key into the `SERPAPI_KEY` variable in your `.env` file.

2. **Groq AI Key**:
   - Visit [Groq AI](https://groq.com/) and create an account.
   - Generate an API key from your Groq AI dashboard.
   - Copy and paste the key into the `GROQ_API_KEY` variable in your `.env` file.

### Step 3: Google Sheets Service Account
1. Create a service account in your [Google Cloud](https://console.cloud.google.com/) project.
2. Enable the **Google Sheets API** for the project.
3. Download the service account JSON file and name it `google_credentials.json`.
4. Place the JSON file in the root directory of your project.

### Important Notes:
- Ensure that the `.env` file and `google_credentials.json` file are not exposed in public repositories. Add these files to your `.gitignore` to keep them secure.
- The environment variables are loaded automatically by the application using the `dotenv` package.

## Optional Features

This application includes additional features to enhance usability and flexibility:

1. **Export Results to Google Sheets**:
   - If you are working with a Google Sheet, you can append the extracted results back to the same sheet.
   - The app automatically creates a new worksheet (if it doesn’t already exist) for exporting the results.

2. **Customizable Search Prompts**:
   - Users can define dynamic prompts using placeholders like `{company}` to personalize search queries for different entities.
   - This flexibility allows for precise control over the type of information extracted.

3. **Dynamic Entity Selection**:
   - Users can specify which column and how many rows of data to process, making it easy to tailor searches to specific use cases.

4. **Download Extracted Results**:
   - Extracted data can be downloaded locally as a CSV file, enabling further offline analysis.

5. **Error Handling**:
   - The app provides clear error messages for common issues like API failures, invalid Google Sheets URLs, or missing environment variables.
   - Logs errors to help users troubleshoot effectively.

### Future Enhancements (Planned or Suggested):
- Integration with additional APIs for broader data scraping capabilities.
- Support for advanced filtering and processing of extracted data.
- Enhanced UI/UX with real-time progress indicators during scraping and analysis.


