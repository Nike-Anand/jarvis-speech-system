"""
Machine Learning Service - Predictions and analysis using scikit-learn
"""
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from typing import Dict, List
import pickle
import os

class MLService:
    def __init__(self):
        """Initialize ML service"""
        self.models = {}
        self.scalers = {}
        self.models_dir = "ml_models"
        os.makedirs(self.models_dir, exist_ok=True)
        print("[MLService] Initialized")
    
    def train_classifier(self, X: List[List[float]], y: List[int], model_name: str = "classifier") -> Dict:
        """Train a classification model"""
        try:
            X = np.array(X)
            y = np.array(y)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train_scaled, y_train)
            
            # Evaluate
            train_score = model.score(X_train_scaled, y_train)
            test_score = model.score(X_test_scaled, y_test)
            
            # Save model
            self.models[model_name] = model
            self.scalers[model_name] = scaler
            
            return {
                "success": True,
                "model_name": model_name,
                "train_accuracy": float(train_score),
                "test_accuracy": float(test_score),
                "samples_trained": len(X_train)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def train_regressor(self, X: List[List[float]], y: List[float], model_name: str = "regressor") -> Dict:
        """Train a regression model"""
        try:
            X = np.array(X)
            y = np.array(y)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train_scaled, y_train)
            
            # Evaluate
            train_score = model.score(X_train_scaled, y_train)
            test_score = model.score(X_test_scaled, y_test)
            
            # Save model
            self.models[model_name] = model
            self.scalers[model_name] = scaler
            
            return {
                "success": True,
                "model_name": model_name,
                "train_r2": float(train_score),
                "test_r2": float(test_score),
                "samples_trained": len(X_train)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def predict(self, X: List[List[float]], model_name: str) -> Dict:
        """Make predictions using trained model"""
        try:
            if model_name not in self.models:
                return {"success": False, "error": f"Model '{model_name}' not found"}
            
            X = np.array(X)
            
            # Scale features
            scaler = self.scalers[model_name]
            X_scaled = scaler.transform(X)
            
            # Predict
            model = self.models[model_name]
            predictions = model.predict(X_scaled)
            
            return {
                "success": True,
                "predictions": predictions.tolist(),
                "count": len(predictions)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_data(self, data: List[float]) -> Dict:
        """Perform statistical analysis on data"""
        try:
            data = np.array(data)
            
            return {
                "success": True,
                "mean": float(np.mean(data)),
                "median": float(np.median(data)),
                "std": float(np.std(data)),
                "min": float(np.min(data)),
                "max": float(np.max(data)),
                "count": len(data)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
