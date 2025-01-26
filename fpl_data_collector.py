import requests
from typing import List
from dataclasses import dataclass
from database import PlayerStats

class FPLDataCollector:
    """Handles data collection from the FPL API."""
    BASE_URL = "https://fantasy.premierleague.com/api"

    def get_player_data(self) -> List[PlayerStats]:
        """
        Fetch all player data from the FPL API.

        Returns:
            List[PlayerStats]: List of player statistics.
        """
        response = requests.get(f"{self.BASE_URL}/bootstrap-static/")
        if response.status_code != 200:
            raise ConnectionError("Failed to fetch data from FPL API")

        data = response.json()
        players = []

        for element in data['elements']:
            player = PlayerStats(
                id=element['id'],
                name=f"{element['first_name']} {element['second_name']}",
                team=data['teams'][element['team'] - 1]['name'],
                position=data['element_types'][element['element_type'] - 1]['singular_name'],
                price=element['now_cost'] / 10,
                total_points=element['total_points'],
                form=float(element['form']),
                selected_by_percent=float(element['selected_by_percent']),
                minutes=element['minutes'],
                goals_scored=element['goals_scored'],
                assists=element['assists'],
                clean_sheets=element['clean_sheets'],
                goals_conceded=element['goals_conceded'],
                yellow_cards=element['yellow_cards'],
                red_cards=element['red_cards']
            )
            players.append(player)

        return players
