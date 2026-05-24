import os

# Ensure datasets directory exists
DATASETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datasets')
os.makedirs(DATASETS_DIR, exist_ok=True)

# Define file paths for the generated datasets
IPL_FILE = os.path.join(DATASETS_DIR, 'ipl_matches.csv')
FOOTBALL_FILE = os.path.join(DATASETS_DIR, 'football_matches.csv')
NBA_FILE = os.path.join(DATASETS_DIR, 'nba_matches.csv')

# Teams and Venues definitions
IPL_TEAMS = [
    'Chennai Super Kings', 'Mumbai Indians', 'Royal Challengers Bangalore',
    'Kolkata Knight Riders', 'Rajasthan Royals', 'Delhi Capitals',
    'Punjab Kings', 'Sunrisers Hyderabad'
]

IPL_VENUES = [
    'MA Chidambaram Stadium (Chepauk)', 'Wankhede Stadium', 'M Chinnaswamy Stadium',
    'Eden Gardens', 'Sawai Mansingh Stadium', 'Arun Jaitley Stadium',
    'Rajiv Gandhi International Stadium', 'Narendra Modi Stadium'
]

# Map teams to their primary home venues for realistic generation
IPL_HOME_VENUES = {
    'Chennai Super Kings': 'MA Chidambaram Stadium (Chepauk)',
    'Mumbai Indians': 'Wankhede Stadium',
    'Royal Challengers Bangalore': 'M Chinnaswamy Stadium',
    'Kolkata Knight Riders': 'Eden Gardens',
    'Rajasthan Royals': 'Sawai Mansingh Stadium',
    'Delhi Capitals': 'Arun Jaitley Stadium',
    'Sunrisers Hyderabad': 'Rajiv Gandhi International Stadium'
}

FOOTBALL_TEAMS = [
    'Manchester United', 'Manchester City', 'Liverpool', 'Chelsea',
    'Arsenal', 'Tottenham Hotspur', 'Real Madrid', 'Barcelona'
]

NBA_TEAMS = [
    'Los Angeles Lakers', 'Golden State Warriors', 'Boston Celtics',
    'Brooklyn Nets', 'Milwaukee Bucks', 'Miami Heat', 'Chicago Bulls',
    'Phoenix Suns'
]
