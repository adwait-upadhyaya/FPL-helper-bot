import os
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class FPLAdvisor:
    """Handles FPL advice generation using ChatGPT."""

    def __init__(self, openai_api_key: str):
        """
        Initialize the FPLAdvisor with OpenAI API key.

        Args:
            openai_api_key (str): OpenAI API key for accessing GPT models.
        """
        self.llm = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-4o-mini"
        )
        self.output_parser = StrOutputParser()

    def _clean_sql_query(self, query: str) -> str:
        """
        Remove markdown formatting and clean the SQL query.

        Args:
            query (str): Raw SQL query with possible markdown formatting.

        Returns:
            str: Cleaned SQL query.
        """
        query = query.replace('```sql', '').replace('```', '').strip()
        return query

    def generate_sql_query(self, question: str) -> str:
        """
        Generate an SQL query based on a natural language question.

        Args:
            question (str): User question in natural language.

        Returns:
            str: Generated SQL query.
        """
        sql_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an SQL expert for Fantasy Premier League (FPL) data. Generate a SQL query to answer the user's question.
            The database has a 'players' table with the following columns:
            - id (INTEGER)
            - name (TEXT)
            - team (TEXT)
            - position (TEXT)
            - price (REAL)
            - total_points (INTEGER)
            - form (REAL)
            - selected_by_percent (REAL)
            - minutes (INTEGER)
            - goals_scored (INTEGER)
            - assists (INTEGER)
            - clean_sheets (INTEGER)
            - goals_conceded (INTEGER)
            - yellow_cards (INTEGER)
            - red_cards (INTEGER)
            - last_updated (TIMESTAMP)

            Important: Return only the raw SQL query without any markdown formatting or code blocks."""),
            ("user", "{question}")
        ])

        chain = sql_prompt | self.llm | self.output_parser
        query = chain.invoke({"question": question})
        return self._clean_sql_query(query)

    def generate_advice(self, question: str, data: pd.DataFrame) -> str:
        """
        Generate FPL advice based on query results.

        Args:
            question (str): User question in natural language.
            data (pd.DataFrame): DataFrame containing relevant player statistics.

        Returns:
            str: Generated advice based on the data.
        """
        advice_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an FPL (Fantasy Premier League) expert advisor. Using the following player statistics,
            provide detailed and strategic advice in response to the user's question."""),
            ("user", """Available Player Data:
            {data}

            Question: {question}"""),
            ("system", """Provide a thorough analysis and specific recommendations based on the data shown above.
            Consider factors like form, value for money, upcoming fixtures, and recent performance.""")
        ])

        chain = advice_prompt | self.llm | self.output_parser
        return chain.invoke({
            "data": data.to_string(),
            "question": question
        })
