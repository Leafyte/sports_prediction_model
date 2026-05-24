import os
import random
import numpy as np
import pandas as pd
from config import (
    IPL_FILE, FOOTBALL_FILE, NBA_FILE,
    IPL_TEAMS, IPL_VENUES, IPL_HOME_VENUES,
    FOOTBALL_TEAMS, NBA_TEAMS
)

def generate_ipl_dataset():
    """Generates synthetic, realistic IPL match dataset."""
    random.seed(42)
    np.random.seed(42)
    
    data = []
    # Strength factor (for realistic bias in winning)
    team_strength = {
        'Chennai Super Kings': 1.2,
        'Mumbai Indians': 1.15,
        'Royal Challengers Bangalore': 1.05,
        'Kolkata Knight Riders': 1.02,
        'Rajasthan Royals': 1.0,
        'Delhi Capitals': 0.95,
        'Punjab Kings': 0.85,
        'Sunrisers Hyderabad': 0.9
    }
    
    for _ in range(800):
        t1, t2 = random.sample(IPL_TEAMS, 2)
        venue = random.choice(IPL_VENUES)
        
        # Toss winner is either team1 or team2
        toss_winner = t1 if random.random() < 0.5 else t2
        toss_decision = 'field' if random.random() < 0.6 else 'bat'
        
        # Calculate winning probability with biases
        # Home advantage bias
        p_t1 = 0.5
        if IPL_HOME_VENUES.get(t1) == venue:
            p_t1 += 0.12
        if IPL_HOME_VENUES.get(t2) == venue:
            p_t1 -= 0.12
            
        # Strength bias
        p_t1 += (team_strength[t1] - team_strength[t2]) * 0.25
        
        # Toss bias (fielding first has slight advantage)
        if toss_winner == t1 and toss_decision == 'field':
            p_t1 += 0.05
        elif toss_winner == t2 and toss_decision == 'field':
            p_t1 -= 0.05
            
        # Clamp probability
        p_t1 = max(0.1, min(0.9, p_t1))
        
        winner = t1 if random.random() < p_t1 else t2
        
        # Runs score logic
        # High scoring venue vs low scoring
        base_runs = 160
        if venue in ['M Chinnaswamy Stadium', 'Wankhede Stadium']:
            base_runs = 180
        elif venue in ['MA Chidambaram Stadium (Chepauk)']:
            base_runs = 150
            
        t1_runs = int(np.random.normal(base_runs + (team_strength[t1] - 1)*20, 20))
        t2_runs = int(np.random.normal(base_runs + (team_strength[t2] - 1)*20, 20))
        
        # Ensure winner has more runs (or chased successfully)
        if winner == t1 and t1_runs <= t2_runs:
            t1_runs = t2_runs + random.randint(1, 10)
        elif winner == t2 and t2_runs <= t1_runs:
            t2_runs = t1_runs + random.randint(1, 10)
            
        data.append({
            'team1': t1,
            'team2': t2,
            'toss_winner': toss_winner,
            'toss_decision': toss_decision,
            'venue': venue,
            'winner': winner,
            'team1_runs': max(80, t1_runs),
            'team2_runs': max(80, t2_runs)
        })
        
    df = pd.DataFrame(data)
    df.to_csv(IPL_FILE, index=False)
    print(f"Generated IPL Match Dataset: {IPL_FILE}")


def generate_football_dataset():
    """Generates synthetic, realistic Football matches dataset."""
    random.seed(42)
    np.random.seed(42)
    
    data = []
    # Strength factor
    team_strength = {
        'Manchester City': 1.3,
        'Liverpool': 1.25,
        'Real Madrid': 1.25,
        'Barcelona': 1.15,
        'Arsenal': 1.1,
        'Chelsea': 1.0,
        'Manchester United': 0.95,
        'Tottenham Hotspur': 0.9
    }
    
    for _ in range(800):
        ht, at = random.sample(FOOTBALL_TEAMS, 2)
        
        # Possession is skewed based on team strengths
        st_diff = team_strength[ht] - team_strength[at]
        avg_possession = 50 + (st_diff * 15)
        possession = int(np.random.normal(avg_possession, 5))
        possession = max(20, min(80, possession))
        
        # Shots on target depends on strength and possession
        ht_shots = int(np.random.poisson(4 + (team_strength[ht] * 1.5) + (possession - 50)*0.1))
        at_shots = int(np.random.poisson(4 + (team_strength[at] * 1.5) - (possession - 50)*0.1))
        ht_shots = max(0, ht_shots)
        at_shots = max(0, at_shots)
        
        # Goals depend on shots on target and a bit of randomness
        # Conversion rate roughly 10-25%
        ht_goals = int(np.random.poisson(ht_shots * 0.22 + 0.3))
        at_goals = int(np.random.poisson(at_shots * 0.18 + 0.1))
        
        # Determine winner
        if ht_goals > at_goals:
            winner = 'Home'
        elif at_goals > ht_goals:
            winner = 'Away'
        else:
            winner = 'Draw'
            
        data.append({
            'home_team': ht,
            'away_team': at,
            'possession': possession,
            'shots_on_target': ht_shots,
            'home_goals': ht_goals,
            'away_goals': at_goals,
            'winner': winner
        })
        
    df = pd.DataFrame(data)
    df.to_csv(FOOTBALL_FILE, index=False)
    print(f"Generated Football Match Dataset: {FOOTBALL_FILE}")


def generate_nba_dataset():
    """Generates synthetic, realistic NBA matches dataset."""
    random.seed(42)
    np.random.seed(42)
    
    data = []
    # Strength factor
    team_strength = {
        'Boston Celtics': 1.25,
        'Milwaukee Bucks': 1.2,
        'Golden State Warriors': 1.15,
        'Phoenix Suns': 1.1,
        'Los Angeles Lakers': 1.05,
        'Miami Heat': 1.0,
        'Brooklyn Nets': 0.9,
        'Chicago Bulls': 0.85
    }
    
    for _ in range(800):
        ht, at = random.sample(NBA_TEAMS, 2)
        
        # NBA statistics generators
        # Rebounds average 40-50 per game
        ht_rebounds = int(np.random.normal(44 + (team_strength[ht]-1.0)*5, 4))
        # Assists average 22-28
        ht_assists = int(np.random.normal(25 + (team_strength[ht]-1.0)*6, 3))
        # Shooting % averages 44-50%
        ht_shooting_percentage = round(np.random.normal(46.5 + (team_strength[ht]-1.0)*8, 2.5), 1)
        
        # Scores are typically 100-120
        # Home team scoring depends on assets, rebounds, shooting %
        ht_score = int(np.random.normal(108 + (ht_shooting_percentage - 46.5)*2.5 + (team_strength[ht] - 1.0)*10, 8))
        at_score = int(np.random.normal(105 + (team_strength[at] - 1.0)*10, 8))
        
        # Cannot have a tie in NBA (overtime resolves it)
        if ht_score == at_score:
            if random.random() < 0.55: # slight home advantage in OT
                ht_score += random.choice([2, 3, 5, 7])
            else:
                at_score += random.choice([2, 3, 5, 7])
                
        winner = 'Home' if ht_score > at_score else 'Away'
        
        data.append({
            'home_team': ht,
            'away_team': at,
            'rebounds': max(20, ht_rebounds),
            'assists': max(10, ht_assists),
            'shooting_percentage': max(30.0, min(70.0, ht_shooting_percentage)),
            'home_score': ht_score,
            'away_score': at_score,
            'winner': winner
        })
        
    df = pd.DataFrame(data)
    df.to_csv(NBA_FILE, index=False)
    print(f"Generated NBA Match Dataset: {NBA_FILE}")


def check_and_generate_datasets():
    """Initial check to generate CSV files if they don't exist."""
    if not os.path.exists(IPL_FILE):
        generate_ipl_dataset()
    if not os.path.exists(FOOTBALL_FILE):
        generate_football_dataset()
    if not os.path.exists(NBA_FILE):
        generate_nba_dataset()
