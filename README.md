# 🤖 AutoQI — Automated Quality Inspection System

AI-powered defect detection for Industry 4.0 manufacturing using camera feeds, deep learning, and real-time analytics.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-purple)

---

## 🚀 Quick Start (Dashboard Only)

**The fastest way to see AutoQI in action:**

```powershell
# 1. Navigate to the project directory
cd c:\Users\bhara\Downloads\automation\autoqi

# 2. Start the local web server
.\start_server.ps1

# 3. Open your browser and go to:
# http://localhost:3000/autoqi_dashboard.html
```

That's it! The dashboard is a **self-contained HTML file** with no dependencies required.

---

## 📋 Full Setup (Backend + ML Pipeline)

### Prerequisites
- Python 3.10+
- Node.js (optional, for advanced features)
- Docker (optional, for containerized deployment)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourname/autoqi
cd autoqi

# 2. Create virtual environment
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your settings:
# - ANTHROPIC_API_KEY (for AI features)
# - DB_URL (PostgreSQL connection)
# - MQTT_BROKER (IoT integration)
# - CAMERA_INDEX (for live capture)
```

---

## 🎯 Running the Application

### Option 1: Dashboard Only (Static HTML)
```powershell
.\start_server.ps1
```
Access at: **http://localhost:3000/autoqi_dashboard.html**

### Option 2: Full Backend API
```bash
# Terminal 1: Start FastAPI backend
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start Streamlit dashboard (optional)
streamlit run dashboard/app.py
```

### Option 3: Docker (Complete Stack)
```bash
docker-compose up --build
```

Services will be available at:
- **Dashboard**: http://localhost:3000/autoqi_dashboard.html
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Streamlit**: http://localhost:8501

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.10+ |
| **Computer Vision** | OpenCV, Pillow |
| **Deep Learning** | PyTorch, YOLOv8, Ultralytics |
| **API** | FastAPI, Uvicorn |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) |
| **Dashboard** | Streamlit (optional) |
| **Database** | PostgreSQL, Redis |
| **IoT/Messaging** | MQTT (Mosquitto) |
| **AI** | Anthropic Claude API |
| **Deployment** | Docker, Docker Compose |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/inspect` | Submit image for defect detection |
| `GET` | `/results` | Retrieve inspection history (paginated) |
| `GET` | `/stats` | Get defect rates and accuracy metrics |
| `POST` | `/retrain` | Trigger model retraining workflow |
| `GET` | `/health` | System health check |

**API Documentation**: Visit `http://localhost:8000/docs` when the backend is running.

---

## 📁 Project Structure

```
autoqi/
├── autoqi_dashboard.html      # Main dashboard (standalone HTML)
├── index.html                 # Redirect to dashboard
├── start_server.ps1           # Quick server launcher
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Docker orchestration
├── pytest.ini                 # Test configuration
├── conftest.py                # Pytest fixtures
│
├── src/                       # Source code
│   ├── api/                   # FastAPI backend
│   │   ├── main.py           # API entry point
│   │   └── anthropic_ai.py   # Claude AI integration
│   ├── capture/              # Camera/image capture
│   │   └── camera.py
│   ├── preprocessing/         # Image preprocessing pipeline
│   │   └── pipeline.py
│   ├── inference/            # ML inference engine
│   │   └── engine.py
│   └── integration/          # MQTT & retraining logic
│       ├── mqtt_client.py
│       ├── decider.py
│       └── retrain.py
│
├── models/                    # ML models
│   ├── train.py              # Training script
│   ├── evaluate.py           # Evaluation script
│   └── saved/                # Saved model checkpoints
│
├── data/                      # Dataset storage
│   ├── raw/                  # Raw images
│   ├── labeled/              # Annotated data
│   └── augmented/            # Augmented training data
│
├── logs/                      # Inspection logs
│   └── inspections/          # JSON inspection records
│
├── tests/                     # Unit & integration tests
│   ├── test_api.py
│   ├── test_capture.py
│   └── test_preprocessing.py
│
├── dashboard/                 # Streamlit dashboard (optional)
│   └── app.py
│
└── docker/                    # Docker configuration
    ├── Dockerfile
    └── mosquitto.conf        # MQTT config
```

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_api.py

# Verbose mode
pytest -v
```

---

## 🎨 Dashboard Features

The **autoqi_dashboard.html** includes:

✅ **150+ Working Functions**  
✅ **Real-time Inspection Monitoring**  
✅ **Interactive Charts** (Chart.js)  
✅ **Data Upload & Export** (CSV, JSON, Excel, PDF)  
✅ **Compliance Reporting** (ISO 9001, Six Sigma)  
✅ **Dark Mode UI** with Glassmorphism  
✅ **Responsive Design** (Mobile & Desktop)  
✅ **Live Statistics** & Performance Metrics  

---

## 🔧 Configuration

Edit `.env` file:

```bash
# API Keys
ANTHROPIC_API_KEY=your_api_key_here

# Database
DB_URL=postgresql://user:pass@localhost:5432/autoqi
REDIS_URL=redis://localhost:6379/0

# MQTT
MQTT_BROKER=localhost
MQTT_PORT=1883

# Camera
CAMERA_INDEX=0  # 0 = default webcam

# Model
MODEL_PATH=models/saved/best.pt
CONFIDENCE_THRESHOLD=0.75
```

---

## 🐳 Docker Deployment

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

---

## 🌐 Cloud Deployment

### Vercel (Dashboard Only)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

See `VERCEL_DEPLOYMENT_GUIDE.md` for details.

---

## 📊 Model Training

```bash
# Train new model
python models/train.py --data data/labeled --epochs 100

# Evaluate model
python models/evaluate.py --model models/saved/best.pt --test data/test
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## 🆘 Troubleshooting

**Port 3000 already in use?**
```powershell
# Kill process on port 3000
$conn = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
if ($conn) { Stop-Process -Id $conn.OwningProcess -Force }
```

**Python dependencies failing?**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

**Docker issues?**
```bash
# Clean rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

---

## 📞 Support

For issues, questions, or contributions:
- **Issues**: [GitHub Issues](https://github.com/yourname/autoqi/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourname/autoqi/discussions)

---

**Made with ❤️ for Industry 4.0**
