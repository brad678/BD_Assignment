import json
from langchain.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from .tracing import langfuse_handler
import os


class StockNewsSentimentAnalyzer:
    def __init__(self, news_summary, company_name, stock_code, news_desc):
        self.news_summary = news_summary
        self.company_name = company_name
        self.stock_code = stock_code
        self.news_desc = news_desc

        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            api_version="2024-12-01-preview"
        )

    def analyze_sentiment_and_entities(self):
        with open("prompts/sentiment_prompt.txt", "r") as f:
            prompt_template = f.read()

        prompt = PromptTemplate.from_template(prompt_template)

        chain = prompt | self.llm | StrOutputParser()
        output_str = chain.invoke({"news_summary": self.news_summary}, config={"callbacks": [langfuse_handler]})

        if output_str.startswith("```json"):
            output_str = output_str.lstrip("```json").rstrip("```")

        try:
            return json.loads(output_str.strip())
        except json.JSONDecodeError as e:
            print(f"JSON error: {e}")
            return None
