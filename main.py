from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import nest_asyncio
#from pyngrok import ngrok
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import pickle 
import os


# Initialize FastAPI app
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run the server
# nest_asyncio.apply()

# Get absolute file paths for model & scaler
model_path = os.path.abspath("./src/prediction_models/car_purchase_decision_model.pkl")
scaler_path = os.path.abspath("./src/prediction_models/car_purchase_decision_scaler.pkl")

# Load the saved model and scaler
# car_model = pickle.load(open('./src/prediction_models/car_purchase_decision_model.pkl', 'rb'))
# car_scaler = pickle.load(open('./src/prediction_models/car_purchase_decision_scaler.pkl', 'rb'))
# Load the saved model and scaler
try:
    with open(model_path, "rb") as model_file:
        car_model = pickle.load(model_file)

    with open(scaler_path, "rb") as scaler_file:
        car_scaler = pickle.load(scaler_file)

    print("✅ Model and Scaler Loaded Successfully!")
except Exception as e:
    print(f"❌ Error Loading Model: {e}")


# Define input schema
class CarPurchase(BaseModel):
  features: list

# Welcome Endpoint
@app.get("/")
def read_root():
  return {"message": "Welcome to the Model Prediction API! ✔"}

# Define prediction endpoint
@app.post("/predict/car_purchase")
def predict_car_purchase(input_data: CarPurchase):
  # Convert input list to NumPy array
  input_array = np.array(input_data.features).reshape(1, -1)

  # scale the input features
  scaled_data = car_scaler.transform(input_array)

  # Make prediction
  prediction = car_model.predict(scaled_data)
  result = "Most likely to purchase a car" if prediction[0] == 1 else "Bad Wine"

  return {"prediction": result}

#uvicorn.run(app, host="0.0.0.0", port=8000)


