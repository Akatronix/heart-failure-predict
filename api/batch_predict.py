import json
import os
import sys
import pandas as pd
import numpy as np
import joblib

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.recommendations import get_risk_level, generate_recommendations

# Load model
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'model', 'heart_failure_model.pkl')
model = joblib.load(model_path)

def handler(event, context):
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        if not isinstance(body, list):
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Expected a list of patient data"})
            }
        
        results = []
        
        for patient in body:
            try:
                # Validate required fields
                required_fields = ['age', 'sex', 'chest_pain', 'resting_bp', 'cholesterol', 
                                  'fasting_bs', 'resting_ecg', 'max_hr', 'exercise_angina', 
                                  'oldpeak', 'st_slope']
                
                for field in required_fields:
                    if field not in patient:
                        results.append({"error": f"Missing required field: {field}"})
                        continue
                
                # Convert to model input format
                patient_data = [
                    int(patient['age']),
                    patient['sex'],
                    patient['chest_pain'],
                    int(patient['resting_bp']),
                    int(patient['cholesterol']),
                    int(patient['fasting_bs']),
                    patient['resting_ecg'],
                    int(patient['max_hr']),
                    patient['exercise_angina'],
                    float(patient['oldpeak']),
                    patient['st_slope']
                ]
                
                # Create DataFrame
                feature_columns = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 
                                  'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 
                                  'Oldpeak', 'ST_Slope']
                patient_df = pd.DataFrame([patient_data], columns=feature_columns)
                
                # Make prediction
                prediction = model.predict(patient_df)[0]
                probability = model.predict_proba(patient_df)[0][1]
                
                # Get risk level and recommendations
                risk_level = get_risk_level(probability)
                recommendations = generate_recommendations(patient_data, prediction, probability)
                
                results.append({
                    "prediction": int(prediction),
                    "risk_level": risk_level,
                    "probability": float(probability),
                    "recommendations": recommendations
                })
                
            except Exception as e:
                results.append({"error": str(e)})
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"results": results})
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