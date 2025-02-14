from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import nest_asyncio
#from pyngrok import ngrok
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import pickle 


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

# Load the saved model and scaler
car_model = pickle.load(open('./src/prediction_models/car_purchase_decision_model.pkl', 'rb'))
car_scaler = pickle.load(open('./src/prediction_models/car_purchase_decision_scaler.pkl', 'rb'))


# Define input schema
class CarPurchase(BaseModel):
  features: list

# Welcome Endpoint
@app.get("/")
def read_root():
  return {"message": "Welcome to the Model Prediction API! ✔"}

# Define prediction endpoint
@app.post("/predict/car_purchase")
async def predict_car_purchase(input_data: CarPurchase):
  # Convert input list to NumPy array
  input_array = await np.array(input_data.features).reshape(1, -1)

  # scale the input features
  scaled_data = await car_scaler.transform(input_array)

  # Make prediction
  prediction = await car_model.predict(scaled_data)
  result = "Most likely to purchase a car" if prediction[0] == 1 else "Bad Wine"

  return {"prediction": result}

#uvicorn.run(app, host="0.0.0.0", port=8000)


