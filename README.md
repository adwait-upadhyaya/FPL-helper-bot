# FPL Assistant 🏆

## Overview

FPL Assistant is an intelligent Fantasy Premier League (FPL) advisor that helps managers make data-driven decisions using AI and player statistics.

## Features

- AI-powered player recommendations
- SQL-based data querying
- Interactive Streamlit UI
- Real-time FPL data analysis

## Prerequisites

- Python 3.8+
- OpenAI API Key

## Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/fpl-assistant.git
cd fpl-assistant
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Set up environment variables

- Create a `.env` file
- Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

## Usage

### Data Collection

```bash
python fpl_data_collector.py
```

### Running the App

```bash
streamlit run app.py
```

## Project Structure

- `fpl_data_collector.py`: Fetches data from FPL API
- `database.py`: Manages SQLite database
- `fpl_advisor.py`: AI-powered advice generation
- `app.py`: Streamlit user interface

## Technologies

- Python
- Streamlit
- OpenAI GPT
- Langchain
- SQLite
