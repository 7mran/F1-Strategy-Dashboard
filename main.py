import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import fastf1
import numpy as np

# =============================================================================
# APPLICATION INITIALIZATION & SETUP
# =============================================================================

print("=== F1 2024 CHAMPIONSHIP Season Explorer - COMPLETE IMPLEMENTATION ===")
print("🏎️ Interactive Race Chapter Selection with Real Data Analysis!")

# Enable FastF1 caching for improved performance
fastf1.Cache.enable_cache('src/data/data/cache')


# =============================================================================
# F1 DATA ANALYSIS ENGINE
# =============================================================================

class F1ChampionshipStoryEngine:
    """
    F1 data analysis engine - handles all FastF1 operations and chart generation.

    This class is responsible for:
    - Loading race data from FastF1
    - Processing lap times, positions, and results
    - Creating various visualization charts
    - Managing driver and constructor championship data
    """

    def __init__(self):
        """Initialize the F1 data analysis engine with empty state."""
        # Core FastF1 session data
        self.session = None
        self.results = None
        self.laps = None
        self.current_race_info = None

        # Race tracking
        self.current_race_number = None

        # Initialize driver information and championship data
        self._setup_driver_info()
        self._setup_championship_data()

    def _setup_driver_info(self):
        """
        Setup comprehensive driver information for consistent styling and identification.

        Each driver entry contains:
        - name: Full driver name
        - color: Team color for charts
        - marker: Chart marker style
        - team: Team name
        """
        self.driver_info = {
            # Red Bull Racing
            'VER': {'name': 'Max Verstappen', 'color': '#0600EF', 'marker': 'o', 'team': 'Red Bull'},
            'PER': {'name': 'Sergio Perez', 'color': '#0600EF', 'marker': 's', 'team': 'Red Bull'},

            # McLaren
            'NOR': {'name': 'Lando Norris', 'color': '#FF8000', 'marker': 's', 'team': 'McLaren'},
            'PIA': {'name': 'Oscar Piastri', 'color': '#FF8000', 'marker': 'o', 'team': 'McLaren'},

            # Ferrari
            'LEC': {'name': 'Charles Leclerc', 'color': '#DC143C', 'marker': 'o', 'team': 'Ferrari'},
            'SAI': {'name': 'Carlos Sainz', 'color': '#DC143C', 'marker': 's', 'team': 'Ferrari'},

            # Mercedes
            'RUS': {'name': 'George Russell', 'color': '#00D2BE', 'marker': 's', 'team': 'Mercedes'},
            'HAM': {'name': 'Lewis Hamilton', 'color': '#00D2BE', 'marker': 'o', 'team': 'Mercedes'},

            # Aston Martin
            'ALO': {'name': 'Fernando Alonso', 'color': '#006F62', 'marker': 'o', 'team': 'Aston Martin'},
            'STR': {'name': 'Lance Stroll', 'color': '#006F62', 'marker': 's', 'team': 'Aston Martin'},

            # Racing Bulls (AlphaTauri)
            'TSU': {'name': 'Yuki Tsunoda', 'color': '#2B4562', 'marker': 's', 'team': 'Racing Bulls'},
            'RIC': {'name': 'Daniel Ricciardo', 'color': '#2B4562', 'marker': 'o', 'team': 'Racing Bulls'},

            # Alpine
            'GAS': {'name': 'Pierre Gasly', 'color': '#0090FF', 'marker': 'o', 'team': 'Alpine'},
            'OCO': {'name': 'Esteban Ocon', 'color': '#0090FF', 'marker': 's', 'team': 'Alpine'},

            # Haas F1 Team
            'HUL': {'name': 'Nico Hulkenberg', 'color': '#900000', 'marker': 's', 'team': 'Haas F1 Team'},
            'MAG': {'name': 'Kevin Magnussen', 'color': '#900000', 'marker': 'o', 'team': 'Haas F1 Team'},

            # Kick Sauber (Alfa Romeo)
            'BOT': {'name': 'Valtteri Bottas', 'color': '#29CF1B', 'marker': 'o', 'team': 'Kick Sauber'},
            'ZHO': {'name': 'Zhou Guanyu', 'color': '#29CF1B', 'marker': 's', 'team': 'Kick Sauber'},

            # Williams
            'ALB': {'name': 'Alexander Albon', 'color': '#005AFF', 'marker': 's', 'team': 'Williams'},
            'SAR': {'name': 'Logan Sargeant', 'color': '#005AFF', 'marker': 'o', 'team': 'Williams'},

            # Reserve/Replacement drivers
            'LAW': {'name': 'Liam Lawson', 'color': '#2B4562', 'marker': 'x', 'team': 'Racing Bulls'},
            'COL': {'name': 'Franco Colapinto', 'color': '#005AFF', 'marker': 'x', 'team': 'Williams'},
            'BEA': {'name': 'Oliver Bearman', 'color': '#DC143C', 'marker': 'x', 'team': 'Ferrari'},
        }

    def _setup_championship_data(self):
        """
        Setup progressive championship standings data for both constructors and drivers.

        This data represents cumulative points after each race of the 2024 season,
        allowing for historical championship progression visualization.
        """
        # Progressive constructor standings after each race (cumulative points)
        self.progressive_constructor_standings = {
            1: {"Red Bull Racing": 44, "Ferrari": 27, "Mercedes": 16, "McLaren": 12, "Aston Martin": 3,
                "Kick Sauber": 0, "Haas F1 Team": 0, "RB": 0, "Williams": 0, "Alpine": 0},

            2: {"Red Bull Racing": 87, "Ferrari": 49, "Mercedes": 26, "McLaren": 28, "Aston Martin": 13,
                "Kick Sauber": 0, "Haas F1 Team": 1, "RB": 0, "Williams": 0, "Alpine": 0},

            3: {"Red Bull Racing": 97, "Ferrari": 93, "Mercedes": 26, "McLaren": 55, "Aston Martin": 25,
                "Kick Sauber": 0, "Haas F1 Team": 4, "RB": 6, "Williams": 0, "Alpine": 0},

            4: {"Red Bull Racing": 141, "Ferrari": 120, "Mercedes": 34, "McLaren": 69, "Aston Martin": 33,
                "Kick Sauber": 0, "Haas F1 Team": 4, "RB": 7, "Williams": 0, "Alpine": 0},

            5: {"Red Bull Racing": 181, "Ferrari": 142, "Mercedes": 44, "McLaren": 91, "Aston Martin": 40,
                "Kick Sauber": 0, "Haas F1 Team": 5, "RB": 7, "Williams": 0, "Alpine": 0},

            6: {"Red Bull Racing": 211, "Ferrari": 167, "Mercedes": 56, "McLaren": 116, "Aston Martin": 42,
                "Kick Sauber": 0, "Haas F1 Team": 5, "RB": 13, "Williams": 0, "Alpine": 1},

            7: {"Red Bull Racing": 240, "Ferrari": 192, "Mercedes": 71, "McLaren": 146, "Aston Martin": 44,
                "Kick Sauber": 0, "Haas F1 Team": 5, "RB": 14, "Williams": 0, "Alpine": 1},

            8: {"Red Bull Racing": 248, "Ferrari": 232, "Mercedes": 88, "McLaren": 176, "Aston Martin": 44,
                "Kick Sauber": 0, "Haas F1 Team": 5, "RB": 18, "Williams": 2, "Alpine": 2},

            9: {"Red Bull Racing": 273, "Ferrari": 232, "Mercedes": 116, "McLaren": 204, "Aston Martin": 58,
                "Kick Sauber": 0, "Haas F1 Team": 5, "RB": 22, "Williams": 2, "Alpine": 5},

            10: {"Red Bull Racing": 302, "Ferrari": 250, "Mercedes": 143, "McLaren": 229, "Aston Martin": 58,
                 "Kick Sauber": 0, "Haas F1 Team": 5, "RB": 22, "Williams": 2, "Alpine": 8},

            11: {"Red Bull Racing": 318, "Ferrari": 265, "Mercedes": 180, "McLaren": 247, "Aston Martin": 58,
                 "Kick Sauber": 0, "Haas F1 Team": 17, "RB": 24, "Williams": 2, "Alpine": 9},

            12: {"Red Bull Racing": 336, "Ferrari": 276, "Mercedes": 205, "McLaren": 274, "Aston Martin": 68,
                 "Kick Sauber": 0, "Haas F1 Team": 25, "RB": 25, "Williams": 4, "Alpine": 9},

            13: {"Red Bull Racing": 352, "Ferrari": 296, "Mercedes": 225, "McLaren": 317, "Aston Martin": 69,
                 "Kick Sauber": 0, "Haas F1 Team": 25, "RB": 27, "Williams": 4, "Alpine": 9},

            14: {"Red Bull Racing": 371, "Ferrari": 319, "Mercedes": 250, "McLaren": 345, "Aston Martin": 73,
                 "Kick Sauber": 0, "Haas F1 Team": 25, "RB": 28, "Williams": 4, "Alpine": 11},

            15: {"Red Bull Racing": 397, "Ferrari": 344, "Mercedes": 260, "McLaren": 383, "Aston Martin": 74,
                 "Kick Sauber": 0, "Haas F1 Team": 25, "RB": 28, "Williams": 4, "Alpine": 13},

            16: {"Red Bull Racing": 409, "Ferrari": 381, "Mercedes": 276, "McLaren": 417, "Aston Martin": 74,
                 "Kick Sauber": 0, "Haas F1 Team": 26, "RB": 28, "Williams": 6, "Alpine": 13},

            17: {"Red Bull Racing": 419, "Ferrari": 399, "Mercedes": 293, "McLaren": 455, "Aston Martin": 82,
                 "Kick Sauber": 0, "Haas F1 Team": 27, "RB": 28, "Williams": 16, "Alpine": 13},

            18: {"Red Bull Racing": 438, "Ferrari": 415, "Mercedes": 313, "McLaren": 495, "Aston Martin": 86,
                 "Kick Sauber": 0, "Haas F1 Team": 29, "RB": 28, "Williams": 16, "Alpine": 13},

            19: {"Red Bull Racing": 459, "Ferrari": 458, "Mercedes": 321, "McLaren": 517, "Aston Martin": 86,
                 "Kick Sauber": 0, "Haas F1 Team": 33, "RB": 30, "Williams": 17, "Alpine": 13},

            20: {"Red Bull Racing": 467, "Ferrari": 499, "Mercedes": 343, "McLaren": 539, "Aston Martin": 86,
                 "Kick Sauber": 0, "Haas F1 Team": 41, "RB": 30, "Williams": 17, "Alpine": 14},

            21: {"Red Bull Racing": 493, "Ferrari": 509, "Mercedes": 356, "McLaren": 551, "Aston Martin": 86,
                 "Kick Sauber": 0, "Haas F1 Team": 41, "RB": 38, "Williams": 17, "Alpine": 47},

            22: {"Red Bull Racing": 504, "Ferrari": 536, "Mercedes": 399, "McLaren": 566, "Aston Martin": 86,
                 "Kick Sauber": 0, "Haas F1 Team": 45, "RB": 40, "Williams": 17, "Alpine": 47},

            23: {"Red Bull Racing": 529, "Ferrari": 562, "Mercedes": 411, "McLaren": 583, "Aston Martin": 92,
                 "Kick Sauber": 4, "Haas F1 Team": 47, "RB": 40, "Williams": 17, "Alpine": 57},

            24: {"Red Bull Racing": 537, "Ferrari": 595, "Mercedes": 433, "McLaren": 609, "Aston Martin": 94,
                 "Kick Sauber": 4, "Haas F1 Team": 51, "RB": 40, "Williams": 17, "Alpine": 63}
        }

        # Progressive driver championship standings after each race (cumulative points)
        self.progressive_driver_standings = {
            1: {"VER": 26, "PER": 18, "SAI": 15, "LEC": 12, "RUS": 10, "NOR": 8, "HAM": 6, "PIA": 4, "ALO": 2, "STR": 1,
                "ZHO": 0, "MAG": 0, "RIC": 0, "TSU": 0, "ALB": 0, "HUL": 0, "OCO": 0, "GAS": 0, "BOT": 0, "SAR": 0},
            2: {"VER": 51, "PER": 36, "SAI": 15, "LEC": 28, "RUS": 18, "NOR": 12, "HAM": 8, "PIA": 16, "ALO": 12,
                "STR": 1, "ZHO": 0, "MAG": 0, "RIC": 0, "TSU": 0, "ALB": 0, "HUL": 1, "OCO": 0, "GAS": 0, "BOT": 0,
                "SAR": 0, "BEA": 6},
            3: {"VER": 51, "PER": 46, "SAI": 40, "LEC": 47, "RUS": 18, "NOR": 27, "HAM": 8, "PIA": 28, "ALO": 16,
                "STR": 9, "ZHO": 0, "MAG": 1, "RIC": 0, "TSU": 6, "ALB": 0, "HUL": 3, "OCO": 0, "GAS": 0, "BOT": 0,
                "SAR": 0, "BEA": 6},
            4: {"VER": 77, "PER": 64, "SAI": 55, "LEC": 59, "RUS": 24, "NOR": 37, "HAM": 10, "PIA": 32, "ALO": 24,
                "STR": 9, "ZHO": 0, "MAG": 1, "RIC": 0, "TSU": 7, "ALB": 0, "HUL": 3, "OCO": 0, "GAS": 0, "BOT": 0,
                "SAR": 0, "BEA": 6},
            5: {"VER": 102, "PER": 79, "SAI": 65, "LEC": 71, "RUS": 32, "NOR": 55, "HAM": 12, "PIA": 36, "ALO": 31,
                "STR": 9, "ZHO": 0, "MAG": 1, "RIC": 0, "TSU": 7, "ALB": 0, "HUL": 4, "OCO": 0, "GAS": 0, "BOT": 0,
                "SAR": 0, "BEA": 6},
            6: {"VER": 120, "PER": 91, "SAI": 75, "LEC": 86, "RUS": 36, "NOR": 80, "HAM": 20, "PIA": 36, "ALO": 33,
                "STR": 9, "ZHO": 0, "MAG": 1, "RIC": 0, "TSU": 13, "ALB": 0, "HUL": 4, "OCO": 1, "GAS": 0, "BOT": 0,
                "SAR": 0, "BEA": 6},
            7: {"VER": 145, "PER": 95, "SAI": 85, "LEC": 101, "RUS": 43, "NOR": 98, "HAM": 28, "PIA": 48, "ALO": 33,
                "STR": 11, "ZHO": 0, "MAG": 1, "RIC": 0, "TSU": 14, "ALB": 0, "HUL": 4, "OCO": 1, "GAS": 0, "BOT": 0,
                "SAR": 0, "BEA": 6},
            8: {"VER": 153, "PER": 95, "SAI": 100, "LEC": 126, "RUS": 53, "NOR": 110, "HAM": 35, "PIA": 66, "ALO": 33,
                "STR": 11, "ZHO": 0, "MAG": 1, "RIC": 0, "TSU": 18, "ALB": 2, "HUL": 4, "OCO": 1, "GAS": 1, "BOT": 0,
                "SAR": 0, "BEA": 6},
            9: {"VER": 178, "PER": 95, "SAI": 100, "LEC": 126, "RUS": 68, "NOR": 128, "HAM": 48, "PIA": 76, "ALO": 41,
                "STR": 17, "ZHO": 0, "MAG": 1, "RIC": 4, "TSU": 18, "ALB": 2, "HUL": 4, "OCO": 2, "GAS": 3, "BOT": 0,
                "SAR": 0, "BEA": 6},
            10: {"VER": 203, "PER": 99, "SAI": 108, "LEC": 136, "RUS": 80, "NOR": 147, "HAM": 63, "PIA": 82, "ALO": 41,
                 "STR": 17, "ZHO": 0, "MAG": 1, "RIC": 4, "TSU": 18, "ALB": 2, "HUL": 4, "OCO": 3, "GAS": 5, "BOT": 0,
                 "SAR": 0, "BEA": 6},
            11: {"VER": 213, "PER": 105, "SAI": 123, "LEC": 136, "RUS": 105, "NOR": 147, "HAM": 75, "PIA": 100,
                 "ALO": 41, "STR": 17, "ZHO": 0, "MAG": 5, "RIC": 6, "TSU": 18, "ALB": 2, "HUL": 12, "OCO": 3, "GAS": 6,
                 "BOT": 0, "SAR": 0, "BEA": 6},
            12: {"VER": 231, "PER": 105, "SAI": 134, "LEC": 136, "RUS": 105, "NOR": 162, "HAM": 100, "PIA": 112,
                 "ALO": 45, "STR": 23, "ZHO": 0, "MAG": 5, "RIC": 6, "TSU": 19, "ALB": 4, "HUL": 20, "OCO": 3, "GAS": 6,
                 "BOT": 0, "SAR": 0, "BEA": 6},
            13: {"VER": 241, "PER": 111, "SAI": 142, "LEC": 148, "RUS": 110, "NOR": 180, "HAM": 115, "PIA": 137,
                 "ALO": 45, "STR": 24, "ZHO": 0, "MAG": 5, "RIC": 6, "TSU": 21, "ALB": 4, "HUL": 20, "OCO": 3, "GAS": 6,
                 "BOT": 0, "SAR": 0, "BEA": 6},
            14: {"VER": 253, "PER": 118, "SAI": 150, "LEC": 163, "RUS": 110, "NOR": 190, "HAM": 140, "PIA": 155,
                 "ALO": 49, "STR": 24, "ZHO": 0, "MAG": 5, "RIC": 7, "TSU": 21, "ALB": 4, "HUL": 20, "OCO": 5, "GAS": 6,
                 "BOT": 0, "SAR": 0, "BEA": 6},
            15: {"VER": 271, "PER": 126, "SAI": 160, "LEC": 178, "RUS": 116, "NOR": 216, "HAM": 144, "PIA": 167,
                 "ALO": 50, "STR": 24, "ZHO": 0, "MAG": 5, "RIC": 7, "TSU": 21, "ALB": 4, "HUL": 20, "OCO": 5, "GAS": 8,
                 "BOT": 0, "SAR": 0, "BEA": 6},
            16: {"VER": 279, "PER": 130, "SAI": 172, "LEC": 203, "RUS": 122, "NOR": 232, "HAM": 154, "PIA": 185,
                 "ALO": 50, "STR": 24, "ZHO": 0, "MAG": 6, "RIC": 7, "TSU": 21, "ALB": 6, "HUL": 20, "OCO": 5, "GAS": 8,
                 "BOT": 0, "SAR": 0, "BEA": 6, "COL": 0},
            17: {"VER": 289, "PER": 130, "SAI": 172, "LEC": 221, "RUS": 137, "NOR": 245, "HAM": 156, "PIA": 210,
                 "ALO": 58, "STR": 24, "ZHO": 0, "MAG": 6, "RIC": 7, "TSU": 21, "ALB": 12, "HUL": 20, "OCO": 5,
                 "GAS": 8, "BOT": 0, "SAR": 0, "BEA": 7, "COL": 4},
            18: {"VER": 307, "PER": 131, "SAI": 178, "LEC": 231, "RUS": 149, "NOR": 270, "HAM": 164, "PIA": 225,
                 "ALO": 62, "STR": 24, "ZHO": 0, "MAG": 6, "RIC": 7, "TSU": 21, "ALB": 12, "HUL": 22, "OCO": 5,
                 "GAS": 8, "BOT": 0, "SAR": 0, "BEA": 7, "COL": 4},
            19: {"VER": 322, "PER": 137, "SAI": 196, "LEC": 256, "RUS": 157, "NOR": 282, "HAM": 164, "PIA": 235,
                 "ALO": 62, "STR": 24, "ZHO": 0, "MAG": 6, "RIC": 7, "TSU": 21, "ALB": 12, "HUL": 26, "OCO": 5,
                 "GAS": 8, "BOT": 0, "SAR": 0, "BEA": 7, "COL": 5, "LAW": 2},
            20: {"VER": 330, "PER": 137, "SAI": 221, "LEC": 272, "RUS": 167, "NOR": 300, "HAM": 176, "PIA": 239,
                 "ALO": 62, "STR": 24, "ZHO": 0, "MAG": 12, "RIC": 7, "TSU": 21, "ALB": 12, "HUL": 28, "OCO": 5,
                 "GAS": 9, "BOT": 0, "SAR": 0, "BEA": 7, "COL": 5, "LAW": 2},
            21: {"VER": 356, "PER": 137, "SAI": 221, "LEC": 282, "RUS": 179, "NOR": 308, "HAM": 177, "PIA": 243,
                 "ALO": 62, "STR": 24, "ZHO": 0, "MAG": 12, "RIC": 7, "TSU": 27, "ALB": 12, "HUL": 28, "OCO": 23,
                 "GAS": 24, "BOT": 0, "SAR": 0, "BEA": 7, "COL": 5, "LAW": 4},
            22: {"VER": 366, "PER": 138, "SAI": 236, "LEC": 294, "RUS": 204, "NOR": 317, "HAM": 195, "PIA": 249,
                 "ALO": 62, "STR": 24, "ZHO": 0, "MAG": 12, "RIC": 7, "TSU": 29, "ALB": 12, "HUL": 32, "OCO": 23,
                 "GAS": 24, "BOT": 0, "SAR": 0, "BEA": 7, "COL": 5, "LAW": 4},
            23: {"VER": 391, "PER": 138, "SAI": 244, "LEC": 312, "RUS": 216, "NOR": 319, "HAM": 195, "PIA": 264,
                 "ALO": 68, "STR": 24, "ZHO": 4, "MAG": 14, "RIC": 7, "TSU": 29, "ALB": 12, "HUL": 32, "OCO": 23,
                 "GAS": 34, "BOT": 0, "SAR": 0, "BEA": 7, "COL": 5, "LAW": 4},
            24: {"VER": 399, "PER": 138, "SAI": 262, "LEC": 327, "RUS": 226, "NOR": 344, "HAM": 207, "PIA": 265,
                 "ALO": 70, "STR": 24, "ZHO": 4, "MAG": 14, "RIC": 7, "TSU": 29, "ALB": 12, "HUL": 36, "OCO": 23,
                 "GAS": 40, "BOT": 0, "SAR": 0, "BEA": 7, "COL": 5, "LAW": 4}
        }

        # Current race for progressive standings
        self.current_race_number = None

    def load_race_data(self, race_identifier):
        """
        Load FastF1 data for a specific race.

        Args:
            race_identifier: Either race number (int) or race name (str)

        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        try:
            print(f"🔄 Loading data for {race_identifier}...")

            # Map race numbers to race names for FastF1
            race_map = {
                1: 'Bahrain', 2: 'Saudi Arabia', 3: 'Australia', 4: 'Japan',
                5: 'China', 6: 'Miami', 7: 'Emilia Romagna', 8: 'Monaco',
                9: 'Canada', 10: 'Spain', 11: 'Austria', 12: 'Great Britain',
                13: 'Hungary', 14: 'Belgium', 15: 'Netherlands', 16: 'Italy',
                17: 'Azerbaijan', 18: 'Singapore', 19: 'United States',
                20: 'Mexico', 21: 'Brazil', 22: 'Las Vegas', 23: 'Qatar',
                24: 'Abu Dhabi'
            }

            # Convert race number to race name if needed
            if isinstance(race_identifier, int):
                race_name = race_map.get(race_identifier, 'Brazil')
                self.current_race_number = race_identifier
            else:
                race_name = race_identifier
                # Find race number from name
                self.current_race_number = next(
                    (k for k, v in race_map.items() if v == race_name), 21
                )

            # Load session data from FastF1
            self.session = fastf1.get_session(2024, race_name, 'R')
            self.session.load()

            # Extract results and lap data
            self.results = self.session.results
            self.laps = self.session.laps

            # Store race information for later use
            self.current_race_info = {
                'name': race_name,
                'total_laps': len(self.laps['LapNumber'].unique()) if len(self.laps) > 0 else 0,
                'drivers': list(self.results['Abbreviation'].values)
            }

            print(f"✅ Successfully loaded {race_name} data (Race #{self.current_race_number})")
            return True

        except Exception as e:
            print(f"❌ Error loading race data: {str(e)}")
            return False

    def get_progressive_constructor_standings(self, race_number):
        """
        Get constructor standings after the specified race.

        Args:
            race_number (int): Race number (1-24)

        Returns:
            dict: Constructor standings with team names as keys and points as values
        """
        return self.progressive_constructor_standings.get(
            race_number,
            self.progressive_constructor_standings[24]
        )

    def get_progressive_driver_standings(self, race_number, selected_drivers):
        """
        Get driver standings after the specified race for selected drivers.

        Args:
            race_number (int): Race number (1-24)
            selected_drivers (list): List of driver abbreviations

        Returns:
            dict: Driver standings for selected drivers
        """
        all_standings = self.progressive_driver_standings.get(
            race_number,
            self.progressive_driver_standings[24]
        )

        return {
            driver: all_standings.get(driver, 0)
            for driver in selected_drivers
            if driver in all_standings
        }

    def get_position_data(self, driver_abbreviation):
        """
        Extract lap numbers and positions for a specific driver.

        Args:
            driver_abbreviation (str): Driver's 3-letter abbreviation

        Returns:
            tuple: (lap_numbers, positions) - lists of lap numbers and corresponding positions
        """
        if self.laps is None:
            return [], []

        # Filter laps for the specific driver
        driver_laps = self.laps[self.laps['Driver'] == driver_abbreviation].copy()
        driver_laps = driver_laps.sort_values('LapNumber')

        lap_numbers, positions = [], []

        # Extract valid lap and position data
        for _, lap in driver_laps.iterrows():
            if pd.notna(lap['Position']) and pd.notna(lap['LapNumber']):
                lap_numbers.append(int(lap['LapNumber']))
                positions.append(int(lap['Position']))

        return lap_numbers, positions

    # =============================================================================
    # CHART GENERATION METHODS
    # =============================================================================

    def create_position_progression_chart(self, selected_drivers, show_annotations=True):
        """
        Create interactive position progression chart showing how drivers' positions changed throughout the race.

        Args:
            selected_drivers (list): List of driver abbreviations to include
            show_annotations (bool): Whether to show annotations on the chart

        Returns:
            matplotlib.figure.Figure: The generated chart figure
        """
        fig, ax = plt.subplots(figsize=(12, 8))

        # Plot each selected driver's position progression
        for driver_code in selected_drivers:
            if driver_code in self.driver_info:
                laps_data, pos_data = self.get_position_data(driver_code)

                # Add starting grid position if available
                if self.session and self.session.results is not None:
                    driver_results = self.session.results[
                        self.session.results['Abbreviation'] == driver_code
                        ]

                    if not driver_results.empty and pd.notna(driver_results.iloc[0]['GridPosition']):
                        starting_pos = int(driver_results.iloc[0]['GridPosition'])
                        laps_data.insert(0, 0)  # Insert Lap 0
                        pos_data.insert(0, starting_pos)  # Insert starting position

                # Plot the line if we have data
                if len(laps_data) > 0:
                    info = self.driver_info[driver_code]
                    ax.plot(laps_data, pos_data,
                            marker=info['marker'],
                            color=info['color'],
                            linewidth=3, markersize=8,
                            label=f"{info['name']} ({info['team']})",
                            alpha=0.9)

        # Add championship zones for visual context
        ax.axhspan(1, 3, alpha=0.1, color='gold', label='Podium Zone')
        ax.axhspan(1, 10, alpha=0.05, color='green', label='Points Zone')

        # Configure chart appearance
        ax.set_title(
            f"{self.current_race_info['name']} GP 2024 - Position Progression",
            fontsize=16, fontweight='bold'
        )
        ax.set_xlabel('Lap Number')
        ax.set_ylabel('Position')
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.invert_yaxis()  # Lower positions at top
        ax.grid(True, alpha=0.3)
        ax.legend()

        plt.tight_layout()
        return fig

    def create_championship_impact_chart(self, selected_drivers):
        """
        Create championship points impact visualization showing points earned and position changes.

        Args:
            selected_drivers (list): List of driver abbreviations to analyze

        Returns:
            matplotlib.figure.Figure: The generated chart figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # Chart 1: Points earned this race
        points_data, driver_names, colors = [], [], []

        for driver_code in selected_drivers:
            if driver_code in self.results['Abbreviation'].values:
                driver_result = self.results[self.results['Abbreviation'] == driver_code]

                if len(driver_result) > 0:
                    points = int(driver_result.iloc[0]['Points'])
                    points_data.append(points)
                    driver_names.append(self.driver_info[driver_code]['name'])
                    colors.append(self.driver_info[driver_code]['color'])

        # Create points bar chart
        bars1 = ax1.bar(driver_names, points_data, color=colors, alpha=0.8)
        ax1.set_title('Points Earned This Race', fontweight='bold')
        ax1.set_ylabel('Points')
        ax1.set_xticklabels(driver_names, rotation=45)

        # Add point labels on bars
        for bar, points in zip(bars1, points_data):
            if points > 0:
                ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                         str(points), ha='center', fontweight='bold')

        # Chart 2: Grid vs Final positions comparison
        grid_positions, final_positions = [], []
        comparison_names = []

        for driver_code in selected_drivers:
            if driver_code in self.results['Abbreviation'].values:
                driver_result = self.results[self.results['Abbreviation'] == driver_code]

                if (len(driver_result) > 0 and
                        pd.notna(driver_result.iloc[0]['GridPosition'])):
                    grid_positions.append(int(driver_result.iloc[0]['GridPosition']))
                    final_positions.append(int(driver_result.iloc[0]['Position']))
                    comparison_names.append(self.driver_info[driver_code]['name'])

        # Create comparison bar chart
        if comparison_names:
            x = np.arange(len(comparison_names))
            width = 0.35

            ax2.bar(x - width / 2, grid_positions, width, label='Grid Position',
                    color='lightcoral', alpha=0.7)
            ax2.bar(x + width / 2, final_positions, width, label='Final Position',
                    color='lightblue', alpha=0.7)

            ax2.set_title('Grid vs Final Positions', fontweight='bold')
            ax2.set_ylabel('Position')
            ax2.set_xticks(x)
            ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax2.set_xticklabels(comparison_names, rotation=45)
            ax2.legend()
            ax2.invert_yaxis()

        plt.tight_layout()
        return fig

    def create_performance_dashboard(self, selected_drivers):
        """
        Create comprehensive performance dashboard with multiple charts and championship context.

        This method generates a 2x2 grid of charts:
        1. Position progression throughout the race
        2. Constructor championship standings
        3. Position changes (gained/lost)
        4. Driver championship standings for selected drivers

        Args:
            selected_drivers (list): List of driver abbreviations to analyze

        Returns:
            matplotlib.figure.Figure: The generated dashboard figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        # Get current race number for championship standings
        race_number = self.current_race_number if self.current_race_number else 24

        # =============================================================================
        # Chart 1: Position Progression (Top Left)
        # =============================================================================
        ax1 = axes[0, 0]

        for driver_code in selected_drivers:
            if driver_code in self.driver_info:
                laps_data, pos_data = self.get_position_data(driver_code)

                # Add starting grid position
                if self.session and self.session.results is not None:
                    driver_results = self.session.results[
                        self.session.results['Abbreviation'] == driver_code
                        ]

                    if not driver_results.empty and pd.notna(driver_results.iloc[0]['GridPosition']):
                        starting_pos = int(driver_results.iloc[0]['GridPosition'])
                        laps_data.insert(0, 0)
                        pos_data.insert(0, starting_pos)

                # Plot the progression line
                if len(laps_data) > 0:
                    info = self.driver_info[driver_code]
                    ax1.plot(laps_data, pos_data,
                             marker=info['marker'],
                             color=info['color'], linewidth=2, markersize=4,
                             label=info['name'], alpha=0.8)

        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax1.set_title('Position Progression', fontweight='bold')
        ax1.set_xlabel('Lap Number')
        ax1.set_ylabel('Position')
        ax1.invert_yaxis()
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # =============================================================================
        # Chart 2: Constructor Championship Standings (Bottom Right)
        # =============================================================================
        ax2 = axes[1, 1]
        constructor_standings = self.get_progressive_constructor_standings(race_number)
        constructor_names = list(constructor_standings.keys())
        constructor_points = list(constructor_standings.values())

        # Team colors for constructor chart
        constructor_colors = [
            '#0600EF', '#DC143C', '#00D2BE', '#FF8000', '#006F62',
            '#01C00E', '#900000', '#2B4562', '#005AFF', '#0090FF'
        ]

        bars2 = ax2.bar(constructor_names, constructor_points,
                        color=constructor_colors, alpha=0.8)
        ax2.set_title(f'Constructor Championship After Race {race_number}', fontweight='bold')
        ax2.set_ylabel('Points')
        ax2.set_xticklabels(constructor_names, rotation=45)

        # Add point labels on bars
        for bar, points in zip(bars2, constructor_points):
            ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10,
                     str(points), ha='center', fontweight='bold')

        # =============================================================================
        # Chart 3: Position Changes (Top Right)
        # =============================================================================
        ax3 = axes[0, 1]
        changes, change_names = [], []

        for driver_code in selected_drivers:
            if driver_code in self.results['Abbreviation'].values:
                driver_result = self.results[self.results['Abbreviation'] == driver_code]

                if (len(driver_result) > 0 and
                        pd.notna(driver_result.iloc[0]['GridPosition'])):
                    grid = int(driver_result.iloc[0]['GridPosition'])
                    final = int(driver_result.iloc[0]['Position'])
                    change = grid - final  # Positive = positions gained, negative = lost
                    changes.append(change)
                    change_names.append(self.driver_info[driver_code]['name'])

        # Create position change chart if we have data
        if changes:
            colors_change = [
                'green' if c > 0 else 'red' if c < 0 else 'gray'
                for c in changes
            ]
            bars = ax3.bar(change_names, changes, color=colors_change, alpha=0.8)
            ax3.set_title('Positions Gained/Lost', fontweight='bold')
            ax3.set_ylabel('Position Change')
            ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        else:
            # Show message if no data available
            ax3.text(0.5, 0.5, 'No position change data\navailable',
                     ha='center', va='center', transform=ax3.transAxes,
                     fontsize=12, fontweight='bold')
            ax3.set_title('Positions Gained/Lost', fontweight='bold')

        ax3.yaxis.set_major_locator(MaxNLocator(integer=True))

        # =============================================================================
        # Chart 4: Driver Championship Standings (Bottom Left)
        # =============================================================================
        ax4 = axes[1, 0]
        driver_standings = self.get_progressive_driver_standings(race_number, selected_drivers)

        if driver_standings:
            # Sort by points for better visualization
            sorted_drivers = sorted(driver_standings.items(), key=lambda x: x[1], reverse=True)
            driver_names = [
                self.driver_info[driver]['name']
                for driver, _ in sorted_drivers
                if driver in self.driver_info
            ]
            driver_points = [points for _, points in sorted_drivers]
            driver_colors = [
                self.driver_info[driver]['color']
                for driver, _ in sorted_drivers
                if driver in self.driver_info
            ]

            bars4 = ax4.barh(driver_names, driver_points, color=driver_colors, alpha=0.8)
            ax4.set_title(
                f'Driver Championship After Race {race_number} (Selected Drivers)',
                fontweight='bold'
            )
            ax4.set_xlabel('Championship Points')

            # Add point labels on bars
            for bar, points in zip(bars4, driver_points):
                ax4.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 10,
                         str(points), va='center', fontweight='bold')
        else:
            # Show message if no championship data
            ax4.text(0.5, 0.5, 'No championship data\nfor selected drivers',
                     ha='center', va='center', transform=ax4.transAxes,
                     fontsize=12, fontweight='bold')
            ax4.set_title(
                f'Driver Championship\nAfter Race {race_number}\n(Selected Drivers)',
                fontweight='bold'
            )

        plt.tight_layout(rect=[0, 0.03, 1, 0.95], h_pad=5)
        return fig

    def create_race_results_table(self):
        """
        Create comprehensive race results table with all drivers and performance metrics.

        This method generates a detailed table showing:
        - Final positions and drivers
        - Team information
        - Gap to race leader
        - Best lap times and sector times
        - Average speeds
        - Race status and points earned

        Returns:
            matplotlib.figure.Figure: The generated table figure
        """
        if self.session is None or self.results is None or self.laps.empty:
            print("Error: Session, results, or laps data is missing.")
            return None

        # Get winner's data for gap calculations
        winner_result = self.results.iloc[0]
        winner_time = winner_result['Time'] if 'Time' in self.results.columns else None
        winner_laps_completed = (
            winner_result['Laps']
            if 'Laps' in self.results.columns and pd.notna(winner_result.get('Laps'))
            else 0
        )

        table_data = []

        # Process each driver in finishing order
        for _, driver in self.results.iterrows():
            driver_abbrev = driver['Abbreviation']
            driver_laps = self.laps[self.laps['Driver'] == driver_abbrev].copy()

            # Calculate Gap to Leader
            gap_to_leader = "Winner"

            if driver['Position'] > 1:
                driver_laps_completed = int(driver['Laps']) if pd.notna(driver.get('Laps')) else 0

                if driver['Status'] == 'Finished':
                    if driver_laps_completed == winner_laps_completed:
                        # Same lap count - calculate time gap
                        try:
                            drv_finish_time = (
                                    driver_laps['LapStartTime'].max() +
                                    driver_laps['LapTime'].iloc[-1]
                            )
                            win_finish_time = (
                                    self.laps[self.laps['Driver'] == winner_result['Abbreviation']][
                                        'LapStartTime'].max() +
                                    self.laps[self.laps['Driver'] == winner_result['Abbreviation']]['LapTime'].iloc[
                                        -1]
                            )

                            gap_seconds = (drv_finish_time - win_finish_time).total_seconds()

                            if gap_seconds < 60:
                                gap_to_leader = f"+{gap_seconds:.3f}s"
                            else:
                                minutes = int(gap_seconds // 60)
                                seconds = gap_seconds % 60
                                gap_to_leader = f"+{minutes}:{seconds:06.3f}"
                        except:
                            gap_to_leader = "N/A"
                    else:
                        # Driver finished laps down
                        laps_behind = winner_laps_completed - driver_laps_completed
                        gap_to_leader = f"+{laps_behind} Lap(s)"
                else:
                    # Driver retired, DNF, etc.
                    gap_to_leader = driver['Status']

            # Calculate Performance Metrics
            best_lap = "N/A"
            avg_speed = "N/A"
            best_s1 = "N/A"
            best_s2 = "N/A"
            best_s3 = "N/A"

            if not driver_laps.empty:
                # Filter for valid laps (reasonable lap times)
                clean_laps = driver_laps[
                    (pd.notna(driver_laps['LapTime'])) &
                    (driver_laps['LapTime'].dt.total_seconds() > 60) &
                    (driver_laps['LapTime'].dt.total_seconds() < 200)
                    ]

                if not clean_laps.empty:
                    # Best Lap Time
                    best_lap_sec = clean_laps['LapTime'].min().total_seconds()
                    best_min = int(best_lap_sec // 60)
                    best_sec = best_lap_sec % 60
                    best_lap = f"{best_min}:{best_sec:06.3f}"

                    # Average Speed (rough calculation)
                    avg_lap_sec = clean_laps['LapTime'].dt.total_seconds().mean()
                    avg_speed = f"{(5000 / avg_lap_sec) * 3.6:.1f} km/h"

                # Best Sector Times
                sector_columns = ['Sector1Time', 'Sector2Time', 'Sector3Time']
                sector_vars = [best_s1, best_s2, best_s3]

                for i, col in enumerate(sector_columns):
                    if col in driver_laps.columns and pd.notna(driver_laps[col].min()):
                        sector_sec = driver_laps[col].min().total_seconds()
                        if i == 0:
                            best_s1 = f"{sector_sec:.3f}s"
                        elif i == 1:
                            best_s2 = f"{sector_sec:.3f}s"
                        else:
                            best_s3 = f"{sector_sec:.3f}s"

            # Add driver data to table
            table_data.append({
                'Pos': int(driver['Position']),
                'Driver': driver['Abbreviation'],
                'Team': driver['TeamName'],
                'Gap': gap_to_leader,
                'Best_Lap': best_lap,
                'Best_S1': best_s1,
                'Best_S2': best_s2,
                'Best_S3': best_s3,
                'Avg_Speed': avg_speed,
                'Status': driver['Status'],
                'Points': int(driver['Points'])
            })

        # =============================================================================
        # Create Matplotlib Table
        # =============================================================================
        fig, ax = plt.subplots(figsize=(16, 12))
        ax.axis('tight')
        ax.axis('off')

        # Table headers
        table_headers = [
            'Pos', 'Driver', 'Team', 'Gap to Leader', 'Best Lap',
            'Best S1', 'Best S2', 'Best S3', 'Avg Speed', 'Status', 'Points'
        ]

        # Prepare table rows
        table_rows = []
        for row in table_data:
            table_rows.append([
                f"P{row['Pos']}",
                row['Driver'],
                row['Team'],
                row['Gap'],
                row['Best_Lap'],
                row['Best_S1'],
                row['Best_S2'],
                row['Best_S3'],
                row['Avg_Speed'],
                row['Status'][:8],  # Truncate status
                f"{row['Points']} pts"
            ])

        # Create the table
        table = ax.table(
            cellText=table_rows,
            colLabels=table_headers,
            cellLoc='center',
            loc='center',
            colWidths=[0.06, 0.08, 0.12, 0.12, 0.10, 0.07, 0.07, 0.07, 0.10, 0.08, 0.08]
        )

        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)

        # Color code rows based on finishing position
        for i, row in enumerate(table_data):
            row_idx = i + 1

            # Determine row color based on position
            if row['Pos'] == 1:
                color = '#FFD700'  # Gold for winner
            elif row['Pos'] == 2:
                color = '#C0C0C0'  # Silver for 2nd
            elif row['Pos'] == 3:
                color = '#CD7F32'  # Bronze for 3rd
            elif row['Pos'] <= 10:
                color = '#90EE90'  # Light green for points
            else:
                color = '#FFFFFF'  # White for non-points

            # Apply color to all cells in the row
            for col_idx in range(len(table_headers)):
                table[(row_idx, col_idx)].set_facecolor(color)

        # Style header row
        for col_idx in range(len(table_headers)):
            table[(0, col_idx)].set_facecolor('#4472C4')
            table[(0, col_idx)].set_text_props(weight='bold', color='white')

        # Add title
        plt.suptitle(
            f"{self.current_race_info['name']} GP 2024 - Complete Race Results\n"
            f"Race Performance Analysis",
            fontsize=16, fontweight='bold', y=0.95
        )

        plt.subplots_adjust(top=0.9)
        plt.tight_layout()
        return fig

    # =============================================================================
    # MAIN GUI APPLICATION CLASS
    # =============================================================================

    def create_race_results_table(self):
        """Create comprehensive race results table with all drivers and performance metrics"""
        if self.session is None or self.results is None or self.laps.empty:
            print("Error: Session, results, or laps data is missing. Ensure session.load(laps=True) was called.")
            return None

        # Get winner's time and total laps for gap calculations
        winner_result = self.results.iloc[0]
        winner_time = winner_result['Time'] if 'Time' in self.results.columns and pd.notna(
            winner_result.get('Time')) else None
        winner_laps_completed = winner_result['Laps'] if 'Laps' in self.results.columns and pd.notna(
            winner_result.get('Laps')) else 0

        table_data = []

        # Process each driver in finishing order
        for _, driver in self.results.iterrows():
            driver_abbrev = driver['Abbreviation']
            driver_laps = self.laps[self.laps['Driver'] == driver_abbrev].copy()

            # --- REVISED GAP TO LEADER CALCULATION ---
            gap_to_leader = "Winner"

            if driver['Position'] > 1:
                driver_laps_completed = int(driver['Laps']) if pd.notna(driver.get('Laps')) else 0

                if driver['Status'] == 'Finished':
                    if driver_laps_completed == winner_laps_completed:
                        # Same lap → gap = difference between total race times
                        # Use last lap end time from laps data instead of results['Time']
                        drv_finish_time = driver_laps['LapStartTime'].max() + driver_laps['LapTime'].iloc[-1]
                        win_finish_time = self.laps[self.laps['Driver'] == winner_result['Abbreviation']][
                                              'LapStartTime'].max() \
                                          + self.laps[self.laps['Driver'] == winner_result['Abbreviation']][
                                              'LapTime'].iloc[-1]

                        gap_seconds = (drv_finish_time - win_finish_time).total_seconds()
                        if gap_seconds < 60:
                            gap_to_leader = f"+{gap_seconds:.3f}s"
                        else:
                            minutes = int(gap_seconds // 60)
                            seconds = gap_seconds % 60
                            gap_to_leader = f"+{minutes}:{seconds:06.3f}"
                    else:
                        # Laps down
                        laps_behind = winner_laps_completed - driver_laps_completed
                        gap_to_leader = f"+{laps_behind} Lap(s)"
                else:
                    # Retired, DNF, etc.
                    gap_to_leader = driver['Status']

            # --- BEST LAP AND SECTOR TIMES ---
            best_lap = "N/A"
            avg_speed = "N/A"
            best_s1 = "N/A"
            best_s2 = "N/A"
            best_s3 = "N/A"

            if not driver_laps.empty:
                # Filter for valid laps to calculate best lap and average speed
                clean_laps = driver_laps[(pd.notna(driver_laps['LapTime'])) &
                                         (driver_laps['LapTime'].dt.total_seconds() > 60) &
                                         (driver_laps['LapTime'].dt.total_seconds() < 200)]

                if not clean_laps.empty:
                    # Best Lap
                    best_lap_sec = clean_laps['LapTime'].min().total_seconds()
                    best_min = int(best_lap_sec // 60)
                    best_sec = best_lap_sec % 60
                    best_lap = f"{best_min}:{best_sec:06.3f}"

                    # Average Speed
                    avg_lap_sec = clean_laps['LapTime'].dt.total_seconds().mean()
                    avg_speed = f"{(5000 / avg_lap_sec) * 3.6:.1f} km/h"

                # Best Sector Times
                if 'Sector1Time' in driver_laps.columns and pd.notna(driver_laps['Sector1Time'].min()):
                    s1_sec = driver_laps['Sector1Time'].min().total_seconds()
                    best_s1 = f"{s1_sec:.3f}s"
                if 'Sector2Time' in driver_laps.columns and pd.notna(driver_laps['Sector2Time'].min()):
                    s2_sec = driver_laps['Sector2Time'].min().total_seconds()
                    best_s2 = f"{s2_sec:.3f}s"
                if 'Sector3Time' in driver_laps.columns and pd.notna(driver_laps['Sector3Time'].min()):
                    s3_sec = driver_laps['Sector3Time'].min().total_seconds()
                    best_s3 = f"{s3_sec:.3f}s"

            table_data.append({
                'Pos': int(driver['Position']),
                'Driver': driver['Abbreviation'],
                'Team': driver['TeamName'],
                'Gap': gap_to_leader,
                'Best_Lap': best_lap,
                'Best_S1': best_s1,
                'Best_S2': best_s2,
                'Best_S3': best_s3,
                'Avg_Speed': avg_speed,
                'Status': driver['Status'],
                'Points': int(driver['Points'])
            })

        # --- MATPLOTLIB TABLE CREATION ---
        fig, ax = plt.subplots(figsize=(16, 12))
        ax.axis('tight')
        ax.axis('off')

        # Updated headers to include the new sector columns
        table_headers = ['Pos', 'Driver', 'Team', 'Gap to Leader', 'Best Lap', 'Best S1', 'Best S2', 'Best S3', 'Avg Speed', 'Status',
                         'Points']
        table_rows = []
        for row in table_data:
            table_rows.append([
                f"P{row['Pos']}",
                row['Driver'],
                row['Team'],
                row['Gap'],
                row['Best_Lap'],
                row['Best_S1'],
                row['Best_S2'],
                row['Best_S3'],
                row['Avg_Speed'],
                row['Status'][:8],
                f"{row['Points']} pts"
            ])

        table = ax.table(cellText=table_rows, colLabels=table_headers, cellLoc='center', loc='center',
                         colWidths=[0.06, 0.08, 0.12, 0.12, 0.10, 0.07, 0.07, 0.07, 0.10, 0.08, 0.08])

        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)

        for i, row in enumerate(table_data):
            row_idx = i + 1
            if row['Pos'] == 1:
                color = '#FFD700'
            elif row['Pos'] == 2:
                color = '#C0C0C0'
            elif row['Pos'] == 3:
                color = '#CD7F32'
            elif row['Pos'] <= 10:
                color = '#90EE90'
            else:
                color = '#FFFFFF'
            for col_idx in range(len(table_headers)):
                table[(row_idx, col_idx)].set_facecolor(color)

        for col_idx in range(len(table_headers)):
            table[(0, col_idx)].set_facecolor('#4472C4')
            table[(0, col_idx)].set_text_props(weight='bold', color='white')

        plt.suptitle(f"{self.current_race_info['name']} GP 2024 - Complete Race Results\n"
                     f"Race Performance Analysis", fontsize=16, fontweight='bold', y=0.95)

        plt.subplots_adjust(top=0.9)
        plt.tight_layout()
        return fig


# =============================================================================
# MAIN GUI APPLICATION CLASS
# =============================================================================

class F1RaceChapterNavigator:
    """
    F1 Championship Season Explorer - Main Navigation Interface with Real Data Analysis.

    This class provides the main GUI interface for exploring the 2024 F1 season.
    It handles:
    - Race selection interface
    - Driver selection
    - Chart generation and display
    - Data loading and status updates
    """

    def __init__(self):
        """Initialize the main application window and components."""
        # =============================================================================
        # Main Window Setup
        # =============================================================================
        self.root = tk.Tk()
        self.root.title("F1 2024 Championship Season Explorer - Race Navigator")
        self.root.geometry("1600x1000")
        self.root.configure(bg="#1a1a2e")

        # Handle window closing properly
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # =============================================================================
        # Initialize Core Components
        # =============================================================================
        # F1 analysis engine
        self.analyzer = F1ChampionshipStoryEngine()

        # Application state
        self.current_race = None
        self.selected_drivers = ['VER', 'NOR']  # Default championship contenders
        self.current_chart_frame = None
        self.status_indicator_label = None

        # Driver selection variables (for checkboxes)
        self.driver_vars = {}

        # =============================================================================
        # F1 2024 Race Calendar Data
        # =============================================================================
        self.race_calendar = {
            1: {"event": "Bahrain", "story": "Season Opener - Setting the Stage",
                "date": "Mar 2", "circuit": "Bahrain International Circuit", "emoji": "🏁"},
            2: {"event": "Saudi Arabia", "story": "Desert Duel - Early Patterns",
                "date": "Mar 9", "circuit": "Jeddah Corniche Circuit", "emoji": "🏜️"},
            3: {"event": "Australia", "story": "Down Under Drama",
                "date": "Mar 24", "circuit": "Melbourne Grand Prix Circuit", "emoji": "🇦🇺"},
            4: {"event": "Japan", "story": "Suzuka Spectacle",
                "date": "Apr 7", "circuit": "Suzuka International Racing Course", "emoji": "🇯🇵"},
            5: {"event": "China", "story": "Shanghai Sprint Weekend",
                "date": "Apr 21", "circuit": "Shanghai International Circuit", "emoji": "🇨🇳"},
            6: {"event": "Miami", "story": "Lando's First Victory - Title Fight Ignites",
                "date": "May 5", "circuit": "Miami International Autodrome", "emoji": "🌴"},
            7: {"event": "Emilia Romagna", "story": "Imola Intensity",
                "date": "May 19", "circuit": "Imola Circuit", "emoji": "🇮🇹"},
            8: {"event": "Monaco", "story": "Monte Carlo Magic",
                "date": "May 26", "circuit": "Circuit de Monaco", "emoji": "🏰"},
            9: {"event": "Canada", "story": "Montreal Madness",
                "date": "Jun 9", "circuit": "Circuit Gilles Villeneuve", "emoji": "🇨🇦"},
            10: {"event": "Spain", "story": "Barcelona Battle",
                 "date": "Jun 23", "circuit": "Circuit de Barcelona-Catalunya", "emoji": "🇪🇸"},
            11: {"event": "Austria", "story": "Red Bull Ring Rivalry",
                 "date": "Jun 30", "circuit": "Red Bull Ring", "emoji": "🏔️"},
            12: {"event": "Great Britain", "story": "Silverstone Showdown",
                 "date": "Jul 7", "circuit": "Silverstone Circuit", "emoji": "🇬🇧"},
            13: {"event": "Hungary", "story": "Budapest Brilliance",
                 "date": "Jul 21", "circuit": "Hungaroring", "emoji": "🇭🇺"},
            14: {"event": "Belgium", "story": "Spa-Francorchamps Spectacular",
                 "date": "Jul 28", "circuit": "Circuit de Spa-Francorchamps", "emoji": "🌧️"},
            15: {"event": "Netherlands", "story": "Max's Home Victory",
                 "date": "Aug 25", "circuit": "Circuit Zandvoort", "emoji": "🇳🇱"},
            16: {"event": "Italy", "story": "Monza Temple of Speed",
                 "date": "Sep 1", "circuit": "Autodromo Nazionale di Monza", "emoji": "🏎️"},
            17: {"event": "Azerbaijan", "story": "Baku Street Fight",
                 "date": "Sep 15", "circuit": "Baku City Circuit", "emoji": "🏙️"},
            18: {"event": "Singapore", "story": "Marina Bay Night Race",
                 "date": "Sep 22", "circuit": "Marina Bay Street Circuit", "emoji": "🌃"},
            19: {"event": "United States", "story": "Austin Action",
                 "date": "Oct 20", "circuit": "Circuit of the Americas", "emoji": "🇺🇸"},
            20: {"event": "Mexico", "story": "Mexico City Altitude",
                 "date": "Oct 27", "circuit": "Autodromo Hermanos Rodriguez", "emoji": "🇲🇽"},
            21: {"event": "Brazil", "story": "Max's P17→P1 Championship Masterpiece",
                 "date": "Nov 3", "circuit": "Interlagos Circuit", "emoji": "🏆"},
            22: {"event": "Las Vegas", "story": "Sin City Speed",
                 "date": "Nov 23", "circuit": "Las Vegas Strip Circuit", "emoji": "🎰"},
            23: {"event": "Qatar", "story": "Lusail Final Push",
                 "date": "Dec 1", "circuit": "Lusail International Circuit", "emoji": "🏜️"},
            24: {"event": "Abu Dhabi", "story": "Season Finale Under the Lights",
                 "date": "Dec 8", "circuit": "Yas Marina Circuit", "emoji": "✨"}
        }

        # Key championship races to highlight
        self.key_races = [1, 6, 21, 24]

        self.create_main_interface()

    def on_closing(self):
        """Handle application window closing properly to prevent hanging processes."""
        try:
            # Close any open matplotlib figures
            plt.close('all')

            # Properly quit the application
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print(f"Error during closing: {e}")
        finally:
            # Force exit if needed
            import sys
            sys.exit()

        # =============================================================================
        # GUI CREATION METHODS
        # =============================================================================

    def create_main_interface(self):
        """Create the main F1 Championship Season Explorer interface layout."""

        # =============================================================================
        # Header Section
        # =============================================================================
        header_frame = tk.Frame(self.root, bg="#0f3460", height=100)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        header_frame.pack_propagate(False)

        # Main application title
        title_label = tk.Label(
            header_frame,
            text="🏁 F1 2024 CHAMPIONSHIP SEASON EXPLORER",
            font=("Arial", 24, "bold"),
            bg="#0f3460", fg="white"
        )
        title_label.pack(pady=15)

        # Application subtitle with features description
        subtitle_label = tk.Label(
            header_frame,
            text="📚 Navigate through all 24 race chapters • Real F1 data analysis and interactive charts",
            font=("Arial", 12),
            bg="#0f3460", fg="#00d4ff"
        )
        subtitle_label.pack()

        # =============================================================================
        # Main Content Area Layout
        # =============================================================================
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # LEFT SIDEBAR - Race Selection
        self.create_race_selection_sidebar(main_frame)

        # RIGHT PANEL - Race Details & Analysis
        self.create_race_details_panel(main_frame)

        # Show welcome screen initially
        self.show_welcome_screen()

    def create_race_selection_sidebar(self, parent):
        """
        Create the race selection sidebar with scrollable race list and highlights.

        Args:
            parent: Parent tkinter widget to attach the sidebar to
        """
        # =============================================================================
        # Sidebar Container Setup
        # =============================================================================
        sidebar_frame = tk.Frame(parent, bg="#16213e", width=400)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        sidebar_frame.pack_propagate(False)

        # Sidebar header
        sidebar_header = tk.Label(sidebar_frame,
                                  text="🏎️ SELECT RACE CHAPTER",
                                  font=("Arial", 16, "bold"),
                                  bg="#16213e", fg="white")
        sidebar_header.pack(pady=15)

        # Create a frame to hold both scrollable races and highlights
        content_frame = tk.Frame(sidebar_frame, bg="#16213e")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        # =============================================================================
        # SCROLLABLE RACE LIST SECTION
        # =============================================================================

        # Main frame for the scrollable race list
        races_frame = tk.Frame(content_frame, bg="#16213e")
        races_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas and scrollbar setup for vertical scrolling
        canvas = tk.Canvas(races_frame, bg="#16213e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(races_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#16213e")

        # Configure canvas scrolling region when content changes
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Create window inside canvas for scrollable content
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Generate race buttons for all 24 races in the calendar
        for race_num, race_info in self.race_calendar.items():
            self.create_race_button(scrollable_frame, race_num, race_info)

        # Pack canvas and scrollbar side by side
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add highlighted key races section at the bottom
        self.create_championship_highlights(content_frame)

        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<Button-4>", _on_mousewheel)

    def create_race_button(self, parent, race_num, race_info):
        """Create individual race selection button"""

        # Different styling for key championship races
        if race_num in self.key_races:
            button_bg = "#ff6b35"
            button_fg = "#1a1a2e"
        else:
            button_bg = "#00d4ff"
            button_fg = "#1a1a2e"

        # Main race button frame
        race_frame = tk.Frame(parent, bg=button_bg, relief=tk.RAISED, bd=2)
        race_frame.pack(fill=tk.X, pady=3, padx=65)

        # Race button
        race_btn = tk.Button(race_frame,
                             text=f"{race_info['emoji']} Chapter {race_num}: {race_info['event']}",
                             font=("Arial", 11, "bold"),
                             bg=button_bg, fg=button_fg,
                             relief=tk.FLAT,
                             cursor="hand2",
                             command=lambda: self.select_race_chapter(race_num))
        race_btn.pack(fill=tk.X, pady=2, padx=26)

        # Race details
        details_text = f"📅 {race_info['date']} • {race_info['story']}"
        if len(details_text) > 45:
            details_text = details_text[:42] + "..."

        details = tk.Label(race_frame,
                           text=details_text,
                           font=("Arial", 9),
                           bg=button_bg, fg=button_fg,
                           wraplength=350)
        details.pack(fill=tk.X, padx=5, pady=(0, 5))

    def create_championship_highlights(self, parent):
        """Create championship highlights section"""

        highlights_frame = tk.Frame(parent, bg="#2d4059", relief=tk.RAISED, bd=2, height=220)
        highlights_frame.pack(fill=tk.X, pady=(10, 0))
        highlights_frame.pack_propagate(False)

        highlight_title = tk.Label(highlights_frame,
                                   text="🏆 CHAMPIONSHIP HIGHLIGHTS",
                                   font=("Arial", 12, "bold"),
                                   bg="#2d4059", fg="gold")
        highlight_title.pack(pady=10)

        buttons_frame = tk.Frame(highlights_frame, bg="#2d4059")
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        key_races_info = [
            (1, "🏁 Season Opener"),
            (6, "🌟 Lando's Breakthrough"),
            (21, "👑 Max's Masterpiece"),
            (24, "🏁 Grand Finale")
        ]

        for race_num, description in key_races_info:
            highlight_btn = tk.Button(buttons_frame,
                                      text=f"Chapter {race_num}: {description}",
                                      font=("Arial", 10, "bold"),
                                      bg="gold", fg="black",
                                      relief=tk.RAISED, bd=2,
                                      cursor="hand2",
                                      command=lambda r=race_num: self.select_race_chapter(r))
            highlight_btn.pack(fill=tk.X, pady=4)

    def create_race_details_panel(self, parent):
        """Create the race details and analysis panel"""

        self.details_frame = tk.Frame(parent, bg="white", relief=tk.SUNKEN, bd=2)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

    def show_welcome_screen(self):
        """Show welcome screen when no race is selected"""

        # Clear existing content
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        welcome_frame = tk.Frame(self.details_frame, bg="white")
        welcome_frame.pack(expand=True, fill=tk.BOTH)

        # Welcome message
        welcome_title = tk.Label(welcome_frame,
                                 text="🏁 Welcome to the F1 2024 Championship Season Explorer",
                                 font=("Arial", 20, "bold"),
                                 bg="white", fg="#0f3460",
                                 justify=tk.CENTER)
        welcome_title.pack(pady=50)

        welcome_text = tk.Label(welcome_frame,
                                text="""📚 Select any of the 24 race chapters to explore:

🏎️ Real FastF1 data analysis and visualization
📊 Interactive position progression charts  
⚡ Championship impact analysis
🏆 Constructor and driver championship standings
🚀 Multi-chart performance dashboards

Click any race chapter on the left to begin your journey through the 2024 season!

⚠️ Note: First data load may take a few moments as we fetch real F1 telemetry data.""",
                                font=("Arial", 14),
                                bg="white", fg="gray",
                                justify=tk.CENTER)
        welcome_text.pack(pady=20)

        # Featured races preview
        featured_frame = tk.Frame(welcome_frame, bg="#f0f0f0", relief=tk.RAISED, bd=2)
        featured_frame.pack(pady=30, padx=50, fill=tk.X)

        featured_title = tk.Label(featured_frame,
                                  text="⭐ FEATURED CHAMPIONSHIP CHAPTERS",
                                  font=("Arial", 16, "bold"),
                                  bg="#f0f0f0", fg="#0f3460")
        featured_title.pack(pady=5)

        featured_races = [
            (1, "🏁 Season Opener - Setting the Stage"),
            (6, "🌟 Miami: Lando's First Win - The Championship Fight Begins"),
            (21, "👑 Brazil: Max's P17→P1 Masterpiece - Championship Decider"),
            (24, "🏁 Abu Dhabi: Season Finale Under the Lights")
        ]

        for race_num, description in featured_races:
            featured_btn = tk.Button(featured_frame,
                                     text=description,
                                     font=("Arial", 12, "bold"),
                                     bg="#00d4ff", fg="black",
                                     relief=tk.RAISED, bd=2,
                                     cursor="hand2",
                                     command=lambda r=race_num: self.select_race_chapter(r))
            featured_btn.pack(pady=5, padx=20, fill=tk.X)

    def select_race_chapter(self, race_number):
        """Select and display a specific race chapter"""

        # Clear existing content
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        self.current_race = race_number
        race_info = self.race_calendar[race_number]

        print(f"📖 Loading Chapter {race_number}: {race_info['event']}")

        # Race header
        header_frame = tk.Frame(self.details_frame, bg="#0f3460", height=120)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        header_frame.pack_propagate(False)

        # Race title
        race_title = tk.Label(header_frame,
                              text=f"{race_info['emoji']} Chapter {race_number}: {race_info['event']}",
                              font=("Arial", 18, "bold"),
                              bg="#0f3460", fg="white")
        race_title.pack(pady=10)

        # Race story
        race_story = tk.Label(header_frame,
                              text=race_info['story'],
                              font=("Arial", 14, "italic"),
                              bg="#0f3460", fg="#00d4ff")
        race_story.pack()

        # Race details
        race_details = tk.Label(header_frame,
                                text=f"📅 {race_info['date']} 2024 • 🏁 {race_info['circuit']}",
                                font=("Arial", 11),
                                bg="#0f3460", fg="white")
        race_details.pack(pady=5)

        # Analysis options
        self.create_race_analysis_options(race_number)

    def create_race_analysis_options(self, race_number):
        """Create analysis options for the selected race"""

        options_frame = tk.Frame(self.details_frame, bg="white")
        options_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        # Analysis title
        analysis_title = tk.Label(options_frame,
                                  text="📊 Race Chapter Analysis Options",
                                  font=("Arial", 16, "bold"),
                                  bg="white", fg="#0f3460")
        analysis_title.pack(pady=6)

        # Driver selection section
        self.create_driver_selection(options_frame)

        # Analysis buttons
        buttons_container = tk.Frame(options_frame, bg="white")
        buttons_container.pack(pady=5, padx=50, fill=tk.X)

        analysis_buttons = [
            ("📈 Lap-by-Lap Position Tracking", "Follow each driver's position changes throughout the entire race", "position"),
            ("🏆 Points & Performance Impact", "Analyze points earned and grid vs final position comparisons", "championship"),
            ("📊 Complete Race Analytics", "Comprehensive 4-chart dashboard with championship context", "dashboard"),
            ("🏁 Full Race Results & Times", "Detailed results table with gaps, lap times, and sector analysis", "results_table"),
            ("🔄 Load Race Data", f"Fetch real F1 telemetry and timing data for this race", "load")
        ]

        for btn_text, btn_desc, analysis_type in analysis_buttons:
            btn_frame = tk.Frame(buttons_container, bg="white")
            btn_frame.pack(pady=4, fill=tk.X)

            btn = tk.Button(btn_frame,
                            text=btn_text,
                            font=("Arial", 12, "bold"),
                            bg="light gray", fg="black",
                            relief=tk.RAISED, bd=3,
                            cursor="hand2",
                            height=2,
                            command=lambda race=race_number, analysis=analysis_type: self.run_race_analysis(race,
                                                                                                            analysis))
            btn.pack(fill=tk.X, pady=2)

            desc = tk.Label(btn_frame,
                            text=btn_desc,
                            font=("Arial", 10),
                            bg="white", fg="black")
            desc.pack()

        # Current chapter indicator with status updates
        indicator_frame = tk.Frame(options_frame, bg="#f0f0f0", relief=tk.RAISED, bd=2)
        indicator_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20, padx=50)

        # Store reference to status label for updates
        self.status_indicator_label = tk.Label(indicator_frame,
                                               text=f"📍 Currently viewing: Chapter {race_number} - {self.race_calendar[race_number]['event']}",
                                               font=("Arial", 12, "bold"),
                                               bg="#f0f0f0", fg="#0f3460")
        self.status_indicator_label.pack(pady=10)

    def update_status_indicator(self, message, color="#0f3460"):
        """Update the status indicator with loading/success messages"""
        if self.status_indicator_label:
            self.status_indicator_label.config(text=message, fg=color)
            self.root.update_idletasks()  # Force GUI update

    def create_driver_selection(self, parent):
        """Create driver selection interface"""

        selection_frame = tk.Frame(parent, bg="light gray", relief=tk.RAISED, bd=2)
        selection_frame.pack(fill=tk.X, pady=10, padx=50)

        # Title
        selection_title = tk.Label(selection_frame,
                                   text="🏎️ Select Drivers to Analyze",
                                   font=("Arial", 14, "bold"),
                                   bg="light gray", fg="#0f3460")
        selection_title.pack(pady=10)

        # Driver checkboxes
        drivers_frame = tk.Frame(selection_frame, bg="light gray")
        drivers_frame.pack(pady=10)

        # Create variables for checkboxes
        self.driver_vars = {}

        # All 2024 F1 drivers organized by team
        all_drivers_by_team = [
            # Row 1 - Top teams
            [('VER', 'Max Verstappen', '#0600EF'), ('PER', 'Sergio Perez', '#0600EF'),
             ('LEC', 'Charles Leclerc', '#DC143C'), ('SAI', 'Carlos Sainz', '#DC143C'),
             ('NOR', 'Lando Norris', '#FF8000'), ('PIA', 'Oscar Piastri', '#FF8000')],

            # Row 2 - Mercedes + Aston Martin
            [('HAM', 'Lewis Hamilton', '#00D2BE'), ('RUS', 'George Russell', '#00D2BE'),
             ('ALO', 'Fernando Alonso', '#006F62'), ('STR', 'Lance Stroll', '#006F62'),
             ('GAS', 'Pierre Gasly', '#0090FF'), ('OCO', 'Esteban Ocon', '#0090FF')],

            # Row 3 - Other teams
            [('TSU', 'Yuki Tsunoda', '#2B4562'), ('RIC', 'Daniel Ricciardo', '#2B4562'),
             ('HUL', 'Nico Hulkenberg', '#900000'), ('MAG', 'Kevin Magnussen', '#900000'),
             ('BOT', 'Valtteri Bottas', '#29CF1B'), ('ZHO', 'Zhou Guanyu', '#29CF1B')],

            # Row 4 - Williams + Reserve/replacement drivers
            [('ALB', 'Alexander Albon', '#005AFF'), ('SAR', 'Logan Sargeant', '#005AFF'),
             ('COL', 'Franco Colapinto', '#005AFF'), ('BEA', 'Oliver Bearman', '#DC143C'),
             ('LAW', 'Liam Lawson', '#2B4562')]
        ]

        # Create checkboxes in organized rows
        for row_idx, driver_row in enumerate(all_drivers_by_team):
            for col_idx, (code, name, color) in enumerate(driver_row):
                var = tk.BooleanVar()
                # Default selections - main championship contenders
                if code in ['VER', 'NOR']:
                    var.set(True)

                self.driver_vars[code] = var

                # Create frame for each checkbox
                cb_frame = tk.Frame(drivers_frame, bg="light gray")
                cb_frame.grid(row=row_idx, column=col_idx, padx=5, pady=3, sticky='w')

                cb = tk.Checkbutton(cb_frame,
                                    text=name,  # Truncate long names
                                    variable=var,
                                    bg="light gray",
                                    fg=color,
                                    font=("Arial", 9, "bold"),
                                    command=self.update_driver_selection)
                cb.pack(side=tk.LEFT)

    def update_driver_selection(self):
        """Update the selected drivers based on checkboxes"""
        self.selected_drivers = [code for code, var in self.driver_vars.items() if var.get()]

        if len(self.selected_drivers) == 0:
            # Default to VER if nothing selected
            self.selected_drivers = ['VER']
            self.driver_vars['VER'].set(True)

        print(f"🎯 Selected drivers: {self.selected_drivers}")

    # =============================================================================
    # ANALYSIS EXECUTION AND DATA LOADING
    # =============================================================================
    def run_race_analysis(self, race_number, analysis_type):
        """Run the selected analysis for the race"""

        race_info = self.race_calendar[race_number]
        print(f"🔄 Running {analysis_type} analysis for Chapter {race_number}: {race_info['event']}")

        if analysis_type == "load":
            self.load_race_data_sync(race_number)
        elif self.analyzer.session is None:
            messagebox.showwarning("Data Required",
                                   "Please load race data first by clicking 'Load Race Data' button.")
        else:
            self.display_chart(analysis_type)

    def load_race_data_sync(self, race_number):
        """Load race data synchronously with status updates"""

        race_info = self.race_calendar[race_number]

        # Update status to loading
        self.update_status_indicator(f"🔄 Loading real F1 data for Chapter {race_number} - {race_info['event']}...",
                                     "#ff6b35")

        try:
            # Load the data
            success = self.analyzer.load_race_data(race_number)

            if success:
                # Update status to success
                self.update_status_indicator(
                    f"✅ Data loaded: Chapter {race_number} - {race_info['event']} • {len(self.analyzer.current_race_info['drivers'])} drivers • {self.analyzer.current_race_info['total_laps']} laps",
                    "#2ecc71"
                )

                print(f"✅ Data loaded for {race_info['event']}")
            else:
                # Update status to error
                self.update_status_indicator(
                    f"❌ Failed to load data for Chapter {race_number} - {race_info['event']}",
                    "#dc3545"
                )

        except Exception as e:
            print(f"Error loading data: {str(e)}")
            # Update status to error
            self.update_status_indicator(
                f"❌ Error loading Chapter {race_number} - {race_info['event']}: {str(e)[:50]}...",
                "#dc3545"
            )

            messagebox.showerror("Data Loading Error",
                                 f"❌ An error occurred while loading data:\n\n{str(e)}")

    def display_chart(self, analysis_type):
        """Display the requested chart in a new window"""

        # Create new window for chart
        chart_window = tk.Toplevel(self.root)
        chart_window.title(f"F1 Analysis - {self.race_calendar[self.current_race]['event']} GP 2024")
        chart_window.geometry("1400x800")
        chart_window.configure(bg="white")

        # Fix chart window closing
        chart_window.protocol("WM_DELETE_WINDOW", lambda: self.close_chart_window(chart_window))

        try:
            # Generate the appropriate chart
            if analysis_type == "position":
                fig = self.analyzer.create_position_progression_chart(
                    self.selected_drivers, show_annotations=True)
                chart_title = "📈 Lap-by-Lap Position Tracking"

            elif analysis_type == "championship":
                fig = self.analyzer.create_championship_impact_chart(self.selected_drivers)
                chart_title = "🏆 Points & Performance Impact"

            elif analysis_type == "dashboard":
                fig = self.analyzer.create_performance_dashboard(self.selected_drivers)
                chart_title = "📊 Complete Race Analytics"

            elif analysis_type == "results_table":
                fig = self.analyzer.create_race_results_table()
                chart_title = "🏁 Full Race Results & Times"

            # Chart header
            header_frame = tk.Frame(chart_window, bg="#0f3460", height=80)
            header_frame.pack(fill=tk.X, padx=10, pady=5)
            header_frame.pack_propagate(False)

            title_label = tk.Label(header_frame,
                                   text=chart_title,
                                   font=("Arial", 18, "bold"),
                                   bg="#0f3460", fg="white")
            title_label.pack(pady=10)

            drivers_text = " vs ".join([self.analyzer.driver_info[d]['name'] for d in self.selected_drivers
                                        if d in self.analyzer.driver_info])
            subtitle_label = tk.Label(header_frame,
                                      text=f"{self.race_calendar[self.current_race]['event']} GP 2024 • {drivers_text}",
                                      font=("Arial", 12),
                                      bg="#0f3460", fg="#00d4ff")
            subtitle_label.pack()

            # Embed matplotlib chart
            canvas_frame = tk.Frame(chart_window, bg="white")
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            canvas = FigureCanvasTkAgg(fig, canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            print(f"✅ Displayed {analysis_type} chart for {self.selected_drivers}")

        except Exception as e:
            print(f"❌ Error creating chart: {str(e)}")
            messagebox.showerror("Chart Error",
                                 f"Failed to create chart:\n{str(e)}\n\nPlease ensure race data is loaded properly.")
            chart_window.destroy()

    def close_chart_window(self, window):
        """Properly close chart window and clean up matplotlib figures"""
        try:
            plt.close('all')
            window.destroy()
        except Exception as e:
            print(f"Error closing chart window: {e}")

    def run(self):
        """Start the F1 Championship Season Explorer Navigator"""

        print("🚀 Starting F1 2024 Championship Season Explorer!")
        print("📚 Navigate through all 24 race chapters")
        print("🏎️ Click any race to explore with real F1 data")
        print("⚠️ First data load may take time - we're fetching real telemetry!")

        self.root.mainloop()

# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

# LAUNCH THE F1 CHAMPIONSHIP Season Explorer NAVIGATOR
if __name__ == "__main__":
    print("🏁 F1 2024 CHAMPIONSHIP Season Explorer - COMPLETE IMPLEMENTATION")
    print("=" * 80)
    print("🚀 Features:")
    print("   ✅ Real FastF1 data integration")
    print("   ✅ Interactive driver selection")
    print("   ✅ Multiple chart types (Position, Championship, Dashboard)")
    print("   ✅ Constructor and Driver championship standings")
    print("   ✅ Synchronous data loading with status updates")
    print("   ✅ Professional GUI with embedded matplotlib")
    print("   ✅ All 24 races of 2024 season")
    print("   ✅ Fixed threading and layout issues")
    print("=" * 80)

    try:
        navigator = F1RaceChapterNavigator()
        navigator.run()
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("💡 Please install: pip install fastf1 matplotlib pandas tkinter")
    except Exception as e:
        print(f"❌ Error starting application: {e}")