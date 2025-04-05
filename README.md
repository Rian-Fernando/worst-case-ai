# Worst Case AI 🚨

This AI predicts worst-case system scenarios using failure data and returns predictions via a FastAPI interface.

## Features
- Reads synthetic and real failure datasets
- Trains logistic regression model
- Exposes  endpoint via FastAPI
- Accepts JSON input and returns failure predictions

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Train the model:
   ```bash
   python3 train.py
   ```
3. Run API:
   ```bash
   uvicorn main:app --reload
   ```

## Example Request
POST 
```json
{
  "feature1": 85.0,
  "feature2": 70.5,
  "feature3": 3
}
```

## Output
```json
{
  "prediction": "Running"
}
```


## API Endpoint

POST `/predict`

### Request
```json
{
  "feature1": 85.0,
  "feature2": 70.5,
  "feature3": 3
}
```

### Response
```json
{
  "prediction": "Running"
}
```

