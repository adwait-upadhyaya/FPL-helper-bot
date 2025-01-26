import os
from dotenv import load_dotenv
from fpl_advisor import FPLAdvisor
import pandas as pd
from database import Database

# Set pandas display options for better output
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', 20)

def print_separator():
    print("\n" + "=" * 80 + "\n")

def process_question(bot, question, question_number):
    """
    Process a single question to generate SQL query, retrieve data, and generate advice.
    Args:
        bot (FPLAdvisor): Instance of the FPLAdvisor class.
        question (str): The FPL question to process.
        question_number (int): The number of the question for display purposes.
    """
    print(f"Test Question {question_number}: {question}")
    try:
        # Generate SQL query
        query = bot.generate_sql_query(question)
        print("\nGenerated SQL Query:")
        print(query)

        db = Database()
        data = db.execute_query(query)  

        print("\nRetrieved Data:")
        if not data.empty:
            print(data)
        else:
            print("No data retrieved for this query")

        # Generate advice
        advice = bot.generate_advice(question, data)
        print("\nFPL Expert Advice:")
        print(advice)

    except Exception as e:
        print(f"Error processing question {question_number}: {str(e)}")

    print_separator()

def test_fpl_helper():
    """
    Main function to test the FPL Advisor functionality with sample questions.
    """
    # Load environment variables
    load_dotenv()

    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("No OpenAI API key found. Make sure you have set it in your .env file.")

    # Initialize FPL Advisor
    print("Initializing FPL Advisor...")
    bot = FPLAdvisor(api_key)

    # Test questions
    test_questions = [
        "Who are the top 3 budget forwards under 7M with good form?",
        "Which defenders have the best points per million ratio?",
        # "Who are the most in-form midfielders for captaincy?",
        # "Find me some good differential picks under 10% ownership with good form",
        # "I currently have Cole Palmer in my team, is it a good idea to replace him?"
    ]

    # Process each question
    for i, question in enumerate(test_questions, 1):
        process_question(bot, question, i)

if __name__ == "__main__":
    test_fpl_helper()
