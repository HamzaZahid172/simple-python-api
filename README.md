# Simple Python API

A beginner-friendly Python API project using Flask.

## Features

- Run a small web server
- Create API endpoints
- Return JSON responses
- Ready to push to GitHub

## Project Structure

```text
simple-python-api/
├── app.py
├── requirements.txt
└── README.md
```

## Setup

### 1. Create virtual environment

```bash
python -m venv venv
```

### 2. Activate virtual environment

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\\Scripts\\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
python app.py
```

The API will run at:

```text
http://localhost:5000
```

## API Endpoints

### Home

```http
GET /
```

### Health Check

```http
GET /health
```

### Get All Items

```http
GET /items
```

### Get Single Item

```http
GET /items/1
```

### Add Item

```http
POST /add-item
```

Body:

```json
{
  "name": "Flask API",
  "category": "project"
}
```

## Test with curl

```bash
curl http://localhost:5000/health
curl http://localhost:5000/items
curl -X POST http://localhost:5000/add-item \
  -H "Content-Type: application/json" \
  -d '{"name":"Flask API","category":"project"}'
```

## Push to GitHub

```bash
git init
git add .
git commit -m "Initial simple Python API project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/simple-python-api.git
git push -u origin main
```
