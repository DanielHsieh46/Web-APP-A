#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import google.generativeai as genai
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from uvicorn import Config, Server

# Configure Google Generative AI
GOOGLE_API_KEY = "AIzaSyCsHusSOv-FsyAA-otiNwfTDhfF-p_cdRg"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize FastAPI app
app = FastAPI()

# Configure templates directory
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Render the upload form page.
    """
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/", response_class=HTMLResponse)
async def generate_caption(request: Request, file: UploadFile = File(...)):
    """
    Upload an image and generate an IG caption using Gemini AI.
    """
    # Save the uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file.file.read())

    # Upload the image to Gemini AI
    sample_file = genai.upload_file(path=temp_file_path, display_name=file.filename)

    # Use Gemini model to generate content
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content(
        [sample_file, "請幫我想一個ig 限動的文案，只要生成一個就好，不大於十個字，並且視情況加入emoji"]
    )

    # Clean up temporary file
    os.remove(temp_file_path)

    # Render the result on the webpage
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": response.text},
    )


# Run the FastAPI app using Config and Server
if __name__ == "__main__":
    config = Config(app=app, host="127.0.0.1", port=8000, log_level="info")
    server = Server(config=config)
    server.run()

