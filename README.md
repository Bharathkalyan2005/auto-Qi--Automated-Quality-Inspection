# AutoQI — Automated Quality Inspection System

AI-powered defect detection for Industry 4.0 manufacturing using camera feeds and deep learning.

## Tech Stack

- **Language:** Python 3.10+
- **Vision:** OpenCV, Pillow
- **ML:** PyTorch, YOLOv8
- **API:** FastAPI
- **Dashboard:** Streamlit
- **Database:** PostgreSQL + Redis
- **IoT:** MQTT (Mosquitto)
- **Deployment:** Docker

## Quick Setup

```bash
git clone https://github.com/yourname/autoqi
cd autoqi
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

cp .env.example .env
# Edit .env: ANTHROPIC_API_KEY, DB_URL, MQTT_BROKER, CAMERA_INDEX

# Run backend
uvicorn src.api.main:app --reload

# Run dashboard (new terminal)
streamlit run dashboard/app.py

# Docker (full stack)
docker-compose up --build
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/inspect` | Submit image, get defect result |
| GET | `/results` | Paginated inspection history |
| GET | `/stats` | Defect rates, accuracy metrics |
| POST | `/retrain` | Trigger model retraining |

## Project Structure

```
autoqi/
├── data/raw, labeled, augmented
├── models/train.py, evaluate.py, saved/
├── src/capture, preprocessing, inference, integration, api
├── dashboard/
├── tests/
└── docker/
```

## License

MIT
