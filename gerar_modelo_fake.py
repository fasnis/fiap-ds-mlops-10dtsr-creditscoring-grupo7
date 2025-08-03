import joblib
from sklearn.linear_model import LinearRegression
import numpy as np
import os
import json

os.makedirs("models", exist_ok=True)

# Exemplo com 4 features
X = np.array([
    [1.0, 2.0, 3.0, 4.0],
    [2.0, 3.0, 4.0, 5.0],
    [3.0, 4.0, 5.0, 6.0]
])
y = np.array([10, 20, 30])

modelo = LinearRegression().fit(X, y)
joblib.dump(modelo, "models/model.pkl")

metadata = {
    "model_name": "modelo-fake",
    "model_version": "1.0",
    "framework": "scikit-learn",
    "downloaded_at": "2025-08-03T12:00:00"
}
with open("models/model_metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)

print("✅ Modelo fake com 4 features criado.")