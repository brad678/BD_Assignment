import feedparser
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda
from langchain_openai import AzureChatOpenAI
from .tracing import langfuse_handler
import os

# print("Model openai endpoint from ENV:", os.getenv("AZURE_OPENAI_ENDPOINT"))
# print("Model openai key from ENV:", os.getenv("AZURE_OPENAI_API_KEY"))
# print("Model openai deployment from ENV:", os.getenv("AZURE_OPENAI_DEPLOYMENT"))


class StockNewsLangChain:
    def __init__(self, company_name):
        self.company_name = company_name
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            api_version="2024-12-01-preview"
        )

    def fetch_news(self, stock_code):
        url = f"https://news.google.com/rss/search?q={stock_code}+stock"
        feed = feedparser.parse(url)
        return [entry.title for entry in feed.entries]

    def run_chain(self):
        prompt_stock_code = PromptTemplate.from_template(
            "Provide only the four-character stock ticker symbol for {company_name}."
        )
        chain_stock_code = prompt_stock_code | self.llm | StrOutputParser()

        prompt_stock_news = PromptTemplate.from_template(
            "Summarize these financial news headlines:\n{headlines}"
        )
        chain_summarization = prompt_stock_news | self.llm | StrOutputParser()

        stock_code = chain_stock_code.invoke({"company_name": self.company_name}, config={"callbacks": [langfuse_handler]})
        news_headlines = self.fetch_news(stock_code)
        news_summary = chain_summarization.invoke({"headlines": news_headlines}, config={"callbacks": [langfuse_handler]})

        return {
            "company_name": self.company_name,
            "stock_code": stock_code,
            "news_headlines": news_headlines,
            "summary": news_summary
        }
