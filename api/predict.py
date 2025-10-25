import json
import os
import sys
import pandas as pd
import numpy as np
import joblib

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.recommendations import get_risk_level

# Load model
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'model', 'heart_failure_model.pkl')
model = joblib.load(model_path)

def handler(event, context):
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Validate required fields
        required_fields = ['age', 'sex', 'chest_pain', 'resting_bp', 'cholesterol', 
                          'fasting_bs', 'resting_ecg', 'max_hr', 'exercise_angina', 
                          'oldpeak', 'st_slope']
        
        for field in required_fields:
            if field not in body:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps({"error": f"Missing required field: {field}"})
                }
        
        # Convert to model input format
        patient_data = [
            int(body['age']),
            body['sex'],
            body['chest_pain'],
            int(body['resting_bp']),
            int(body['cholesterol']),
            int(body['fasting_bs']),
            body['resting_ecg'],
            int(body['max_hr']),
            body['exercise_angina'],
            float(body['oldpeak']),
            body['st_slope']
        ]
        
        # Create DataFrame
        feature_columns = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 
                          'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 
                          'Oldpeak', 'ST_Slope']
        patient_df = pd.DataFrame([patient_data], columns=feature_columns)
        
        # Make prediction
        prediction = model.predict(patient_df)[0]
        probability = model.predict_proba(patient_df)[0][1]
        
        # Get risk level
        risk_level = get_risk_level(probability)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "prediction": int(prediction),
                "risk_level": risk_level,
                "probability": float(probability),
                "message": "Heart Failure Detected" if prediction == 1 else "Normal"
            })
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }