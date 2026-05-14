from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

search_tool = TavilySearchResults(max_results = 5)

llm = ChatMistralAI(model="mistral-small-latest")

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful assistant.

Summarize the following news into clear bullet points:

{news}
"""
)

chain = prompt | llm | StrOutputParser()

news_result = search_tool.run("Latest AI news of 2026")

result = chain.invoke({"news" : news_result})
print(result)