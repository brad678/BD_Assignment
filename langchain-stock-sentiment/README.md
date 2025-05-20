# LangChain Stock Sentiment Analysis Project

## Overview
This project leverages LangChain to create a sentiment analysis application that processes company names, retrieves stock codes, fetches related news articles, generates news summary, and analyzes sentiment using Azure OpenAI. The application is designed to provide structured sentiment profiles in JSON format, including sentiment classification and named entity extraction.

## Project Structure
```
langchain-stock-sentiment
├── src
│   ├── app.py                      # Main entry point of the application
│   ├── services
│   │   ├── news_retriever.py       # Retrieves stock code, news articles and summary related to the company
│   │   ├── sentiment_analyzer.py   # Analyzes sentiment using Azure OpenAI and extracts entities
│   │   └── tracing.py              # Implements tracing with LangFuse
│   ├── prompts
│   │   └── sentiment_prompt.txt    # Prompt template for sentiment analysis
│   └── utils
│       └── helpers.py              # Utility functions for common tasks
├── requirements.txt                # Python dependencies for the project
├── README.md                       # Documentation for the project
└── .env                            # Environment variables for sensitive information
```

## Setup Instructions
1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd langchain-stock-sentiment
   ```

2. **Create a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the root directory and add your API keys and other sensitive information.

5. **Run the application**:
   ```
   python src/app.py
   To Test locally using swagger UI: Navigate to src ->> uvicorn app:app --reload --port 8001
   ```

## Usage
- Send a request to the application with a company name to retrieve the stock code, fetch news articles, generate news summary and analyze sentiment.
- The application will return a structured JSON response containing the sentiment profile and named entities.

## Features
- **Stock Code Extraction**: Automatically retrieves or suggests stock codes.
- **News Retrieval**: Gathers the latest news articles related to the specified company.
- **Sentiment Analysis**: Utilizes Azure OpenAI to analyze sentiment and extract named entities.
- **Tracing and Monitoring**: Integrates LangFuse for tracing, prompt debugging, and performance monitoring.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
