from services import tracing 
from fastapi import FastAPI
from services.news_retriever import StockNewsLangChain
from services.sentiment_analyzer import StockNewsSentimentAnalyzer
import os

app = FastAPI()

@app.get("/analyze/{company_name}")
def analyze(company_name: str):
    retriever = StockNewsLangChain(company_name)
    news_output = retriever.run_chain()

    analyzer = StockNewsSentimentAnalyzer(
        news_output['summary'],
        news_output['company_name'],
        news_output['stock_code'],
        news_output['news_headlines']
    )

    sentiment_output = analyzer.analyze_sentiment_and_entities()
    return {
        # "summary_output": news_output,
        "sentiment_output": sentiment_output
    }
