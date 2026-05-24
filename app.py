import os
import pandas as pd
from flask import Flask, render_template, jsonify, request

from config import (
    IPL_FILE, FOOTBALL_FILE, NBA_FILE,
    IPL_TEAMS, IPL_VENUES, IPL_HOME_VENUES,
    FOOTBALL_TEAMS, NBA_TEAMS
)
from models import models_db, init_all_models

app = Flask(__name__)

# Initialize datasets and models
init_all_models()


# ==========================================
# FLASK HTTP ROUTING & ENDPOINTS
# ==========================================

@app.route('/')
def home():
    """Renders the landing page."""
    return render_template('index.html')


@app.route('/predict')
def predict_page():
    """Renders the prediction dashboard page."""
    # Pre-select sport from query parameter if provided, default to ipl
    selected_sport = request.args.get('sport', 'ipl')
    if selected_sport not in ['ipl', 'football', 'nba']:
        selected_sport = 'ipl'
        
    return render_template(
        'predict.html',
        selected_sport=selected_sport,
        ipl_teams=sorted(IPL_TEAMS),
        venues=sorted(IPL_VENUES),
        football_teams=sorted(FOOTBALL_TEAMS),
        nba_teams=sorted(NBA_TEAMS)
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        ipl_metrics=models_db.get('ipl', {}),
        football_metrics=models_db.get('football', {}),
        nba_metrics=models_db.get('nba', {})
    )


# ==========================================
# API ENDPOINTS FOR DYNAMIC INTERACTION
# ==========================================

@app.route('/api/team_stats')
def api_team_stats():
    """Returns historical averages for dynamic stats preloading on the frontend."""
    sport = request.args.get('sport')
    t1 = request.args.get('team1')
    t2 = request.args.get('team2')
    
    if not sport or not t1 or not t2:
        return jsonify({'error': 'Missing parameters'}), 400
        
    try:
        if sport == 'football':
            df = pd.read_csv(FOOTBALL_FILE)
            
            # Find stats for home team overall
            t1_home = df[df['home_team'] == t1]
            
            # Calculate average home team statistics
            avg_pos = int(t1_home['possession'].mean()) if len(t1_home) > 0 else 50
            avg_shots = round(t1_home['shots_on_target'].mean(), 1) if len(t1_home) > 0 else 5.0
            
            # Default fallback if NaN
            if pd.isna(avg_pos): avg_pos = 50
            if pd.isna(avg_shots): avg_shots = 5.0
            
            return jsonify({
                'possession': avg_pos,
                'shots_on_target': avg_shots
            })
            
        elif sport == 'nba':
            df = pd.read_csv(NBA_FILE)
            
            # Filter matches for the home team
            t1_home = df[df['home_team'] == t1]
            
            # Average rebounds, assists, shooting percentage for home team
            avg_reb = int(t1_home['rebounds'].mean()) if len(t1_home) > 0 else 44
            avg_ast = int(t1_home['assists'].mean()) if len(t1_home) > 0 else 24
            avg_pct = round(t1_home['shooting_percentage'].mean(), 1) if len(t1_home) > 0 else 46.0
            
            if pd.isna(avg_reb): avg_reb = 44
            if pd.isna(avg_ast): avg_ast = 24
            if pd.isna(avg_pct): avg_pct = 46.0
            
            return jsonify({
                'rebounds': avg_reb,
                'assists': avg_ast,
                'shooting_percentage': avg_pct
            })
            
        elif sport == 'ipl':
            # For IPL, let's suggest venue based on Team 1's home ground
            suggested_venue = IPL_HOME_VENUES.get(t1, IPL_VENUES[0])
            return jsonify({
                'suggested_venue': suggested_venue
            })
            
        return jsonify({'error': 'Invalid sport'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """Performs ML inference and returns prediction result card data."""
    data = request.json
    if not data or 'sport' not in data:
        return jsonify({'error': 'Invalid input data'}), 400
        
    sport = data['sport']
    
    try:
        # Load datasets to fetch recent history
        if sport == 'ipl':
            t1 = data.get('team1')
            t2 = data.get('team2')
            toss_winner = data.get('toss_winner')
            toss_decision = data.get('toss_decision', 'field')
            venue = data.get('venue')
            
            if t1 == t2:
                return jsonify({'error': 'Teams must be different'}), 400
                
            # Run inference
            clf = models_db['ipl']['classifier']
            reg = models_db['ipl']['regressor']
            
            input_df = pd.DataFrame([{
                'team1': t1,
                'team2': t2,
                'toss_winner': toss_winner,
                'toss_decision': toss_decision,
                'venue': venue
            }])
            
            # Predict win probability (for Team 1)
            prob_team1 = clf.predict_proba(input_df)[0][1] # Probability of 1 (Team 1 wins)
            prob_team2 = 1.0 - prob_team1
            
            if prob_team1 >= prob_team2:
                pred_winner = t1
                win_prob = round(prob_team1 * 100, 1)
            else:
                pred_winner = t2
                win_prob = round(prob_team2 * 100, 1)
                
            # Predict scores
            # Input for regressor is team1, team2, venue
            reg_input = pd.DataFrame([{
                'team1': t1,
                'team2': t2,
                'venue': venue
            }])
            scores = reg.predict(reg_input)[0]
            pred_t1_runs = int(round(scores[0]))
            pred_t2_runs = int(round(scores[1]))
            
            # Load recent history
            df_hist = pd.read_csv(IPL_FILE)
            history = df_hist[
                ((df_hist['team1'] == t1) & (df_hist['team2'] == t2)) |
                ((df_hist['team1'] == t2) & (df_hist['team2'] == t1))
            ].head(5).to_dict(orient='records')
            
            return jsonify({
                'success': True,
                'predicted_winner': pred_winner,
                'win_probability': win_prob,
                'team1': t1,
                'team2': t2,
                'expected_score': f"{t1}: {pred_t1_runs} runs, {t2}: {pred_t2_runs} runs",
                'expected_details': {
                    'team1_val': pred_t1_runs,
                    'team2_val': pred_t2_runs,
                    'label': 'Expected Runs'
                },
                'model_accuracy': models_db['ipl']['accuracy'],
                'model_name': 'Random Forest Classifier & Regressor',
                'history': history
            })
            
        elif sport == 'football':
            ht = data.get('home_team')
            at = data.get('away_team')
            possession = int(data.get('possession', 50))
            shots = int(data.get('shots_on_target', 5))
            
            if ht == at:
                return jsonify({'error': 'Teams must be different'}), 400
                
            clf = models_db['football']['classifier']
            reg = models_db['football']['regressor']
            
            input_df = pd.DataFrame([{
                'home_team': ht,
                'away_team': at,
                'possession': possession,
                'shots_on_target': shots
            }])
            
            # Predict probabilities for Home, Away, Draw
            # Classes are: ['Away', 'Draw', 'Home'] or similar. Let's inspect clf.classes_
            classes = list(clf.classes_)
            prob_arr = clf.predict_proba(input_df)[0]
            probs = dict(zip(classes, prob_arr))
            
            # Predict expected winner based on highest probability
            pred_winner_val = clf.predict(input_df)[0]
            if pred_winner_val == 'Home':
                pred_winner = ht
                win_prob = round(probs['Home'] * 100, 1)
            elif pred_winner_val == 'Away':
                pred_winner = at
                win_prob = round(probs['Away'] * 100, 1)
            else:
                pred_winner = "Draw"
                win_prob = round(probs['Draw'] * 100, 1)
                
            # Predict score
            goals = reg.predict(input_df)[0]
            pred_ht_goals = max(0, int(round(goals[0])))
            pred_at_goals = max(0, int(round(goals[1])))
            
            # Load recent history
            df_hist = pd.read_csv(FOOTBALL_FILE)
            history = df_hist[
                ((df_hist['home_team'] == ht) & (df_hist['away_team'] == at)) |
                ((df_hist['home_team'] == at) & (df_hist['away_team'] == ht))
            ].head(5).to_dict(orient='records')
            
            # Format history to make it look clean
            formatted_history = []
            for h in history:
                formatted_history.append({
                    'team1': h['home_team'],
                    'team2': h['away_team'],
                    'winner': h['home_team'] if h['winner'] == 'Home' else (h['away_team'] if h['winner'] == 'Away' else 'Draw'),
                    'score': f"{h['home_goals']} - {h['away_goals']}"
                })
                
            return jsonify({
                'success': True,
                'predicted_winner': pred_winner,
                'win_probability': win_prob,
                'team1': ht,
                'team2': at,
                'expected_score': f"{ht} {pred_ht_goals} - {pred_at_goals} {at}",
                'expected_details': {
                    'team1_val': pred_ht_goals,
                    'team2_val': pred_at_goals,
                    'label': 'Expected Goals'
                },
                'model_accuracy': models_db['football']['accuracy'],
                'model_name': 'Random Forest Classifier & Regressor',
                'history': formatted_history
            })
            
        elif sport == 'nba':
            ht = data.get('home_team')
            at = data.get('away_team')
            rebounds = int(data.get('rebounds', 44))
            assists = int(data.get('assists', 25))
            shooting_percentage = float(data.get('shooting_percentage', 46.0))
            
            if ht == at:
                return jsonify({'error': 'Teams must be different'}), 400
                
            clf = models_db['nba']['classifier']
            reg = models_db['nba']['regressor']
            
            input_df = pd.DataFrame([{
                'home_team': ht,
                'away_team': at,
                'rebounds': rebounds,
                'assists': assists,
                'shooting_percentage': shooting_percentage
            }])
            
            # Predict win probability (for Home team)
            prob_home = clf.predict_proba(input_df)[0][1] # Probability of 1 (Home wins)
            prob_away = 1.0 - prob_home
            
            if prob_home >= prob_away:
                pred_winner = ht
                win_prob = round(prob_home * 100, 1)
            else:
                pred_winner = at
                win_prob = round(prob_away * 100, 1)
                
            # Predict score
            scores = reg.predict(input_df)[0]
            pred_ht_score = int(round(scores[0]))
            pred_at_score = int(round(scores[1]))
            
            # Load recent history
            df_hist = pd.read_csv(NBA_FILE)
            history = df_hist[
                ((df_hist['home_team'] == ht) & (df_hist['away_team'] == at)) |
                ((df_hist['home_team'] == at) & (df_hist['away_team'] == ht))
            ].head(5).to_dict(orient='records')
            
            # Format history
            formatted_history = []
            for h in history:
                formatted_history.append({
                    'team1': h['home_team'],
                    'team2': h['away_team'],
                    'winner': h['home_team'] if h['winner'] == 'Home' else h['away_team'],
                    'score': f"{h['home_score']} - {h['away_score']}"
                })
                
            return jsonify({
                'success': True,
                'predicted_winner': pred_winner,
                'win_probability': win_prob,
                'team1': ht,
                'team2': at,
                'expected_score': f"{ht} {pred_ht_score} - {pred_at_score} {at}",
                'expected_details': {
                    'team1_val': pred_ht_score,
                    'team2_val': pred_at_score,
                    'label': 'Expected Points'
                },
                'model_accuracy': models_db['nba']['accuracy'],
                'model_name': 'Random Forest Classifier & Regressor',
                'history': formatted_history
            })
            
        return jsonify({'error': 'Invalid sport'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Running Flask app on local dev server
    app.run(debug=True, host='0.0.0.0', port=5080)
