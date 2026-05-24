import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

from config import IPL_FILE, FOOTBALL_FILE, NBA_FILE
from data_generation import check_and_generate_datasets

# Global dictionary to store trained pipelines and their evaluation metrics
models_db = {}

def train_ipl_models():
    """Trains classification and regression pipelines for IPL."""
    df = pd.read_csv(IPL_FILE)
    
    # 1. Classification Model (Winner)
    # Define Target: 1 if team1 wins, 0 if team2 wins (team1_won)
    df['team1_won'] = (df['winner'] == df['team1']).astype(int)
    
    X_cls = df[['team1', 'team2', 'toss_winner', 'toss_decision', 'venue']]
    y_cls = df['team1_won']
    
    # Categorical features for One-Hot Encoding
    categorical_features = ['team1', 'team2', 'toss_winner', 'toss_decision', 'venue']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )
    
    clf_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, max_depth=8))
    ])
    
    # Train-test split
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_cls, y_cls, test_size=0.2, random_state=42)
    clf_pipeline.fit(X_train_c, y_train_c)
    cls_acc = clf_pipeline.score(X_test_c, y_test_c)
    
    # 2. Regression Model (Expected Runs)
    # Train a multi-output regressor to predict [team1_runs, team2_runs]
    X_reg = df[['team1', 'team2', 'venue']]
    y_reg = df[['team1_runs', 'team2_runs']]
    
    reg_preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['team1', 'team2', 'venue'])
        ]
    )
    
    reg_pipeline = Pipeline(steps=[
        ('preprocessor', reg_preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, max_depth=6))
    ])
    
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
    reg_pipeline.fit(X_train_r, y_train_r)
    
    # Save in global model storage
    models_db['ipl'] = {
        'classifier': clf_pipeline,
        'regressor': reg_pipeline,
        'accuracy': round(cls_acc * 100, 2),
        'dataset_size': len(df)
    }


def train_football_models():
    """Trains classification and regression pipelines for Football."""
    df = pd.read_csv(FOOTBALL_FILE)
    
    # 1. Classification Model (Winner: 'Home', 'Away', 'Draw')
    X_cls = df[['home_team', 'away_team', 'possession', 'shots_on_target']]
    y_cls = df['winner']
    
    categorical_features = ['home_team', 'away_team']
    numeric_features = ['possession', 'shots_on_target']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('num', StandardScaler(), numeric_features)
        ]
    )
    
    clf_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, max_depth=8))
    ])
    
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_cls, y_cls, test_size=0.2, random_state=42)
    clf_pipeline.fit(X_train_c, y_train_c)
    cls_acc = clf_pipeline.score(X_test_c, y_test_c)
    
    # 2. Regression Model (Expected Goals)
    y_reg = df[['home_goals', 'away_goals']]
    
    reg_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, max_depth=6))
    ])
    
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_cls, y_reg, test_size=0.2, random_state=42)
    reg_pipeline.fit(X_train_r, y_train_r)
    
    models_db['football'] = {
        'classifier': clf_pipeline,
        'regressor': reg_pipeline,
        'accuracy': round(cls_acc * 100, 2),
        'dataset_size': len(df)
    }


def train_nba_models():
    """Trains classification and regression pipelines for NBA."""
    df = pd.read_csv(NBA_FILE)
    
    # 1. Classification Model (Winner: 'Home' vs 'Away' represented as binary home_team_won 1/0)
    df['home_won'] = (df['winner'] == 'Home').astype(int)
    
    X_cls = df[['home_team', 'away_team', 'rebounds', 'assists', 'shooting_percentage']]
    y_cls = df['home_won']
    
    categorical_features = ['home_team', 'away_team']
    numeric_features = ['rebounds', 'assists', 'shooting_percentage']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('num', StandardScaler(), numeric_features)
        ]
    )
    
    clf_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, max_depth=8))
    ])
    
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_cls, y_cls, test_size=0.2, random_state=42)
    clf_pipeline.fit(X_train_c, y_train_c)
    cls_acc = clf_pipeline.score(X_test_c, y_test_c)
    
    # 2. Regression Model (Expected Score)
    y_reg = df[['home_score', 'away_score']]
    
    reg_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, max_depth=6))
    ])
    
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_cls, y_reg, test_size=0.2, random_state=42)
    reg_pipeline.fit(X_train_r, y_train_r)
    
    models_db['nba'] = {
        'classifier': clf_pipeline,
        'regressor': reg_pipeline,
        'accuracy': round(cls_acc * 100, 2),
        'dataset_size': len(df)
    }


def init_all_models():
    """Generates datasets and trains all ML models on startup."""
    check_and_generate_datasets()
    print("Training IPL models...")
    train_ipl_models()
    print("Training Football models...")
    train_football_models()
    print("Training NBA models...")
    train_nba_models()
    print("All models trained and ready!")
