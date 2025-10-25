def get_risk_level(probability):
    if probability < 0.2:
        return "Low Risk"
    elif probability < 0.6:
        return "Moderate Risk"
    else:
        return "High Risk"

def generate_recommendations(patient_data, prediction, probability):
    age, sex, chest_pain, resting_bp, cholesterol, fasting_bs, resting_ecg, \
    max_hr, exercise_angina, oldpeak, st_slope = patient_data
    
    recommendations = {
        'lifestyle': [],
        'medications': [],
        'monitoring': [],
        'referrals': [],
        'urgent_actions': []
    }
    
    # Risk-based recommendations
    if prediction == 1:
        if probability > 0.7:
            recommendations['urgent_actions'].extend([
                "Immediate cardiology consultation (within 48 hours)",
                "Daily symptom journal",
                "Fluid restriction (<2L/day)",
                "Daily weight monitoring"
            ])
            recommendations['medications'].extend([
                "Start ACE inhibitor/ARB",
                "Start beta-blocker",
                "Consider diuretic"
            ])
        elif probability > 0.4:
            recommendations['referrals'].append("Cardiology consultation within 2 weeks")
            recommendations['medications'].extend([
                "Consider statin therapy",
                "Antihypertensive if BP > 130/80"
            ])
            recommendations['monitoring'].extend([
                "Bi-weekly BP checks",
                "Monthly lipid panel"
            ])
        
        recommendations['lifestyle'].extend([
            "Sodium restriction (<2g/day)",
            "Cardiac rehabilitation program",
            "Alcohol moderation"
        ])
        recommendations['monitoring'].append("BNP/NT-proBNP testing")
    else:
        recommendations['lifestyle'].extend([
            "Heart-healthy diet (Mediterranean or DASH)",
            "150 minutes moderate exercise weekly",
            "Annual cardiac check-up",
            "Smoking cessation if applicable"
        ])
    
    # Feature-specific recommendations
    if resting_bp >= 140:
        recommendations['medications'].append("Antihypertensive medication")
        recommendations['lifestyle'].append("DASH diet specifically")
    
    if cholesterol >= 240:
        recommendations['medications'].append("High-intensity statin")
        recommendations['monitoring'].append("Lipid panel in 4 weeks")
    
    if fasting_bs == 1:
        recommendations['medications'].append("SGLT2 inhibitor")
        recommendations['monitoring'].append("HbA1c every 3 months")
    
    if exercise_angina == 'Y':
        recommendations['lifestyle'].extend([
            "Avoid strenuous exercise",
            "Cardiac-supervised exercise only"
        ])
        recommendations['referrals'].append("Exercise stress test")
    
    if resting_ecg in ['LVH', 'ST']:
        recommendations['referrals'].append("Echocardiogram")
        recommendations['monitoring'].append("ECG every 6 months")
    
    if age >= 65:
        recommendations['medications'].append("Renal function monitoring")
        recommendations['monitoring'].append("Metabolic panel monthly")
    
    if sex == 'F':
        recommendations['monitoring'].append("Anemia screening")
    else:
        recommendations['monitoring'].append("PSA testing if >50")
    
    if oldpeak > 2.0:
        recommendations['urgent_actions'].append("Urgent coronary angiography")
    
    if st_slope == 'Down':
        recommendations['medications'].append("Antiplatelet therapy")
        recommendations['referrals'].append("Nuclear stress test")
    
    return recommendations