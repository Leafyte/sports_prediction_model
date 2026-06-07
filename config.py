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
    'Kolkata Knight Riders', 'Gujarat Titans', 'Delhi Capitals',
    'Lucknow Super Giants', 'Sunrisers Hyderabad', 'Rajasthan Royals', 'Punjab Kings'
]

IPL_VENUES = [
    'MA Chidambaram Stadium (Chepauk)', 'Wankhede Stadium', 'M Chinnaswamy Stadium',
    'Eden Gardens', 'Ekana Cricket Stadium', 'Arun Jaitley Stadium',
    'Rajiv Gandhi International Stadium', 'Narendra Modi Stadium', 'Sawai Mansingh Stadium'
]

# Map teams to their primary home venues for realistic generation
IPL_HOME_VENUES = {
    'Chennai Super Kings': 'MA Chidambaram Stadium (Chepauk)',
    'Mumbai Indians': 'Wankhede Stadium',
    'Royal Challengers Bangalore': 'M Chinnaswamy Stadium',
    'Kolkata Knight Riders': 'Eden Gardens',
    'Gujarat Titans': 'Narendra Modi Stadium',
    'Delhi Capitals': 'Arun Jaitley Stadium',
    'Lucknow Super Giants': 'Ekana Cricket Stadium',
    'Sunrisers Hyderabad': 'Rajiv Gandhi International Stadium',
    'Rajasthan Royals': 'Sawai Mansingh Stadium',
    'Punjab Kings': 'Sawai Mansingh Stadium' # Can be updated if needed, but keeping simple
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
