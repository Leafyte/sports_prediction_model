# Sports Match Prediction Web Application

A complete web application that predicts match outcomes, win probabilities, and expected scores for **IPL Cricket**, **Football (Soccer)**, and **NBA Basketball** using Machine Learning. 

This project uses **Python (Flask)** for the backend, **Scikit-Learn** for machine learning models, and a **premium monochromatic dark-themed HTML/CSS/JS frontend** for user interaction. It is fully self-contained, self-generating historical datasets, and includes a technical FAQ regarding the model architecture.

---

## 🚀 Key Features

* **Three Sports Integrated**: Support for IPL Cricket, Football, and NBA Basketball.
* **Dual ML Predictions**:
  * **Winning Team & Win Probability (%)**: Trained using a `RandomForestClassifier` and extracted via `predict_proba()`.
  * **Expected Match Score (Runs / Goals / Points)**: Trained using `RandomForestRegressor` predicting both team scores.
* **Preloaded Historical Averages**: When selecting teams, an API queries their historical average metrics (e.g. possession, assists, rebounds) to automatically pre-populate the input fields.
* **Interactive What-If Analysis**: Users can tweak the sliders (like possession or shooting percentage) to see how statistics influence prediction outcomes.
* **Dynamic Validation**: Ensures logical inputs (e.g., preventing selecting the same team, limiting IPL toss options to the playing teams, and predicting venues based on home grounds).
* **Recent Head-to-Head History**: Renders a table of past outcomes between the selected teams.
* **Modern Premium Dark UI**: Formulated with an Apple-style glassmorphic design, smooth micro-animations, loading states, and responsive styling.
* **Technical Reference**: Contains an educational About page detailing the ML flow and technical FAQs.

---

## 📂 Project Structure

```
python_predict/
├── datasets/                   # Generated on startup
│   ├── ipl_matches.csv
│   ├── football_matches.csv
│   └── nba_matches.csv
├── static/
│   ├── css/
│   │   └── style.css           # Premium monochromatic dark stylesheet
│   └── js/
│       └── main.js            # Frontend tab/AJAX/render controller
├── templates/
│   ├── layout.html            # Base structural template
│   ├── index.html             # Homepage / hero section
│   ├── predict.html           # Prediction dashboard form & results
│   └── about.html             # ML workflow & technical FAQs
├── app.py                     # Main Flask server & routing entry point
├── config.py                  # App configuration, teams, venues, & file paths
├── data_generation.py         # Synthetic dataset simulation utilities
├── models.py                  # Scikit-Learn training pipelines & model storage
├── requirements.txt           # Package dependencies
└── README.md                  # Project documentation (this file)
```

---

## 🛠️ Installation & Execution Steps

Follow these steps to run the application on your local machine:

### 1. Prerequisite: Python
Make sure you have Python 3.8 or higher installed. Check your version:
```bash
python3 --version
```

### 2. Set Up a Virtual Environment (Recommended)
Navigate to the project root directory and create a virtual environment:
```bash
# Create virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Activate it (Windows PowerShell)
# venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
Install all required libraries using pip:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Start the Flask development server:
```bash
python app.py
```

Upon starting, `app.py` will:
1. Trigger `init_all_models()` from `models.py`.
2. Check if the `datasets/` folder has matches CSV files via `data_generation.py`. If not, it will **auto-generate 800+ realistic matches** for all three sports.
3. Read the generated CSVs, construct pre-processing pipelines, and train the Random Forest Classifiers and Regressors.
4. Launch the local development server on `http://127.0.0.1:5080` to handle user predictions.

### 5. View in Web Browser
Open your browser and navigate to:
```
http://127.0.0.1:5080
```

---

## 🧠 Machine Learning Flow

The application follows standard data science phases:
1. **Data Loading**: Pandas reads historical CSV matches.
2. **Data Cleaning**: Handled missing records (imputed or dropped).
3. **Categorical Encoding**: Used Scikit-learn's `OneHotEncoder` inside a `ColumnTransformer` to encode string labels (team names, venues) into binary representation.
4. **Data Scaling**: Used `StandardScaler` to scale continuous features (e.g. possession, assists).
5. **Train-Test Split**: Separated data into 80% training set (to fit the models) and 20% test set (to evaluate model performance).
6. **Model Training**:
   * **Classifier**: Random Forest Classifier trains on categorical features and historical outcomes to predict winners and probability distributions.
   * **Regressor**: Random Forest Regressor trains on team strengths and stats to predict scores.
7. **Live Prediction**: Web forms capture parameters -> send to `/api/predict` -> run inference via the trained pipeline -> output visual results.

---

## 🧠 Machine Learning FAQ & Reference

Here are some common technical questions regarding the machine learning pipeline and implementation:

1. **Q: Why did you choose Random Forest over simple Logistic/Linear Regression?**
   * *A:* Random Forest is an ensemble learning method based on decision trees. Unlike linear models, it handles complex, non-linear relationships and high-dimensional categorical features (like team vs team on specific venues) without assuming a linear boundary, resulting in higher predictive accuracy and robustness to outliers.

2. **Q: What is the purpose of a Scikit-Learn `Pipeline`?**
   * *A:* A pipeline bundles the preprocessing steps (like `OneHotEncoder` and `StandardScaler`) together with the model estimator. This ensures that the exact same operations are applied to train data, test data, and real-time inputs, preventing data leakage and keeping backend code clean.

3. **Q: Why does the system predict "Home Team Won" (1/0) instead of the team name directly?**
   * *A:* Direct multi-class prediction of team names can result in predicting a team that isn't even playing in the selected match. By defining the target as a binary outcome (`1` if Team 1 wins, `0` if Team 2 wins), the model is mathematically forced to select one of the two actively competing teams.
