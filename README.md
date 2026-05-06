# Image Classifier with FastAPI

This project serves a trained image classification model via an API using the FastAPI web framework. The system analyzes images uploaded via the POST method and returns classification results.

## Installation and Setup

### 1. Installing Dependencies
Run the following command to install the required libraries:
`pip install -r requirements.txt`

### 2. Preparing Model Files
Copy the [pre-trained models available here](https://drive.google.com/drive/folders/1cnbq-2SmnofCMNLb7uC5zOd1Ob344hSR?usp=sharing) into the `src/prediction/models` directory of the project.

### 3. Launching the Application
To start the server, execute the following command in the root directory:
`python main.py`, or to run via Docker, use `docker compose up`.

## API Endpoints

| Endpoint | Description |
| :--- | :--- |
| `http://localhost:7001/` | Used to check the system status (Health Check). |
| `http://localhost:7001/UI` | A simple user interface for uploading files via the browser. |
| `http://localhost:7001/predict` | The main prediction endpoint where the image classification process is performed. |