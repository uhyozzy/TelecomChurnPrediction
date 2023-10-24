from django.apps import AppConfig
import joblib

class TelcoDefenceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Telco_defence'
    mlmodels = joblib.load("./Predict_model/SGD_model.pkl")  # Mechine Learning Model Pre-load
