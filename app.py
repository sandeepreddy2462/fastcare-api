from fastapi import FastAPI, HTTPException, status, Request, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
import uvicorn
import json
import requests
import torch
import numpy as np
import cv2
import io
from PIL import Image
import base64
from sam_utils import get_max_contour, get_wound_RYB_composition, predictor

# Initialize FastAPI app
app = FastAPI(
    title="FastCare API",
    description="A FastAPI server with public endpoints for healthcare management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/upload_img_and_roi", status_code=status.HTTP_200_OK)
async def result(
    image: UploadFile = File(...),
    roi_points: str = Form(...)
):
    try:
       
        # Read the image file
        image_data = await image.read()
        img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Parse the JSON array (roi_points)
        roi_array = json.loads(roi_points)
        
        # Print received data for debugging
        print(f"Received image: {image.filename}")
        print(f"Received ROI points: {roi_points}")

        image_height, image_width = image_rgb.shape[:2]
        predictor.set_image(image_rgb)

        max_contour = get_max_contour(image_width, image_height, roi_array).reshape(-1,2)
        RYB_composition = get_wound_RYB_composition(image_rgb, max_contour)
       
        return {
            "max_contour": max_contour.tolist(),
            "RYB_values" : RYB_composition
            }
        
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON in roi_points: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

