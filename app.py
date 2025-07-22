from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("ds_salaries.csv")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Simple prediction using dataset mean (replace with model later)
    prediction = df['salary_in_usd'].mean()
    return jsonify({'predicted_salary': round(prediction, 2)})

@app.route('/')
def home():
    return "✅ Flask backend is running"

if __name__ == '__main__':
    app.run(debug=True)
