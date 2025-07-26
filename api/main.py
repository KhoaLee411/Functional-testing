import joblib  # or any method to load your model
import pandas as pd
import requests
from fastapi import FastAPI, HTTPException
from loguru import logger

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import constants, preprocess
from api.pydantic_models import HouseData

# Define constants
MODEL_PATH = "models"
EXTERNAL_API = "http://localhost:8081/retrieve-data"

# Load your model
label_encoders = joblib.load(f"{MODEL_PATH}/label_encoders.joblib")
model = joblib.load(f"{MODEL_PATH}/model_xgb.joblib")

# Initialize FastAPI
app = FastAPI()


@app.post("/retrieve-data")
def retrieve_data(id: int):
    logger.info(f"Retrieving data for ID {id}")
    return constants.SAMPLE_DATA


@app.post("/predict-by-id")
def predict_by_id(id: int):
    # Make an external call to get the
    # corresponding data for the given ID
    response = requests.post(
        url=EXTERNAL_API,
        params={"id": id},
        headers={
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
        },
    )

    # Make a df from the response
    test_df = pd.DataFrame.from_dict([response.json()])

    # Drop some columns
    test_df = preprocess.drop_unnecessary_columns(test_df, constants.COLS_TO_DROP)

    # Convert categorical columns to string type
    test_df = preprocess.cast_to_string(test_df, constants.COLS_TO_CAST)

    # Encode categorical features
    test_df = preprocess.encode_cat_cols(test_df, label_encoders, constants.CAT_COLS)

    # Make predictions
    try:
        y_pred = model.predict(test_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"predictions": y_pred.tolist()}


@app.post("/predict")
def predict(house_data: HouseData):
    # Convert input data to DataFrame
    test_df = pd.DataFrame.from_dict([house_data.dict()])

    # Drop some columns
    test_df = preprocess.drop_unnecessary_columns(test_df, constants.COLS_TO_DROP)

    # Convert categorical columns to string type
    test_df = preprocess.cast_to_string(test_df, constants.COLS_TO_CAST)

    # Encode categorical features
    test_df = preprocess.encode_cat_cols(test_df, label_encoders, constants.CAT_COLS)

    # Make predictions
    try:
        y_pred = model.predict(test_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"predictions": y_pred.tolist()}
