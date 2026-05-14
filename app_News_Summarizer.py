import streamlit as st
from dotenv import load_dotenv

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="AI News Summarizer",
    page_icon="📰",
    layout="centered"
)

# Title
st.title("📰 AI News Summarizer")
st.write("Enter any topic and get summarized news in bullet points.")

# User Input
user_query = st.text_input(
    "Enter your topic",
    placeholder="Example: Latest AI news of 2026"
)

# Button
if st.button("Generate Summary"):

    if user_query.strip() == "":
        st.warning("Please enter a topic.")
    
    else:
        with st.spinner("Fetching and summarizing news..."):

            try:
                # Tavily Search Tool
                search_tool = TavilySearchResults(max_results=5)

                # Mistral LLM
                llm = ChatMistralAI(
                    model="mistral-small-latest"
                )

                # Prompt
                prompt = ChatPromptTemplate.from_template(
                    """
                    You are a helpful assistant.

                    Summarize the following news into clear bullet points:

                    {news}
                    """
                )

                # Chain
                chain = prompt | llm | StrOutputParser()

                # Fetch News
                news_result = search_tool.run(user_query)

                # Generate Summary
                result = chain.invoke({
                    "news": news_result
                })

                # Display Output
                st.subheader("📌 Summary")
                st.write(result)

            except Exception as e:
                st.error(f"Error: {e}")