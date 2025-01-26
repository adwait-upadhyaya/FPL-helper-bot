import sqlite3
from typing import List
import pandas as pd
from datetime import datetime
from dataclasses import dataclass

@dataclass
class PlayerStats:
    """Data class to store player statistics."""
    id: int
    name: str
    team: str
    position: str
    price: float
    total_points: int
    form: float
    selected_by_percent: float
    minutes: int
    goals_scored: int
    assists: int
    clean_sheets: int
    goals_conceded: int
    yellow_cards: int
    red_cards: int

class Database:
    """Handles database operations."""
    def __init__(self, db_path: str = "fpl_data.db"):
        """
        Initialize the Database object.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database with a `players` table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    team TEXT,
                    position TEXT,
                    price REAL,
                    total_points INTEGER,
                    form REAL,
                    selected_by_percent REAL,
                    minutes INTEGER,
                    goals_scored INTEGER,
                    assists INTEGER,
                    clean_sheets INTEGER,
                    goals_conceded INTEGER,
                    yellow_cards INTEGER,
                    red_cards INTEGER,
                    last_updated TIMESTAMP
                )
            ''')

    def update_players(self, players: List[PlayerStats]):
        """
        Update player data in the database.

        Args:
            players (List[PlayerStats]): List of player statistics to update.
        """
        with sqlite3.connect(self.db_path) as conn:
            current_time = datetime.now().isoformat()
            for player in players:
                conn.execute('''
                    INSERT OR REPLACE INTO players 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    player.id, player.name, player.team, player.position,
                    player.price, player.total_points, player.form,
                    player.selected_by_percent, player.minutes,
                    player.goals_scored, player.assists, player.clean_sheets,
                    player.goals_conceded, player.yellow_cards, player.red_cards,
                    current_time
                ))

    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query and return the results as a DataFrame.

        Args:
            query (str): SQL query to execute.

        Returns:
            pd.DataFrame: Query results as a DataFrame.

        Raises:
            ValueError: If the query fails to execute.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                return pd.read_sql_query(query, conn)
        except Exception as e:
            raise ValueError(f"Error executing query: {str(e)}")
