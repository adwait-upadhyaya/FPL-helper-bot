import streamlit as st
import os
from dotenv import load_dotenv
from fpl_advisor import FPLAdvisor
from database import Database

# Load environment variables
load_dotenv()

# Initialize FPL Advisor
api_key = os.getenv('OPENAI_API_KEY')
bot = FPLAdvisor(api_key)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Page configuration
st.set_page_config(page_title="FPL Helper", page_icon="⚽")

# Main app
def main():
    st.title("FPL Assistant 🏆")

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask your FPL question"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process the question
        with st.chat_message("assistant"):
            with st.spinner("Generating advice..."):
                try:
                    # Generate SQL query
                    query = bot.generate_sql_query(prompt)
                    
                    # Execute query
                    db = Database()
                    data = db.execute_query(query)
                    
                    # Display query results
                    if not data.empty:
                        st.dataframe(data)
                    
                    # Generate and display advice
                    advice = bot.generate_advice(prompt, data)
                    st.write(advice)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": advice
                    })
                
                except Exception as e:
                    error_msg = f"An error occurred: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })

if __name__ == "__main__":
    main()