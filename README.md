# TravelPlanner AI Agent

An intelligent travel planning agent powered by **IBM Granite** (`ibm/granite-4-h-small`) via IBM watsonx.ai.

## Features
- **Plan Trip** — AI-generated day-by-day itinerary, accommodation, food, budget breakdown
- **TravelBot Chat** — Conversational AI travel assistant
- **Discover** — AI-suggested destinations based on your preferences and budget

## Tech Stack
| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript (no frameworks) |
| Backend | Python 3, Flask, Flask-CORS |
| AI Model | IBM Granite 4 (`ibm/granite-4-h-small`) |
| AI Platform | IBM watsonx.ai (us-south) |

## Project Structure
```
TravelPlanner_agent/
├── frontend/
│   └── index.html        # Single-page UI (3 tabs: Plan, Chat, Discover)
├── backend/
│   ├── app.py            # Flask REST API + IBM Granite integration
│   └── requirements.txt  # Python dependencies
├── .gitignore
└── README.md
```

## Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/TravelPlanner_agent.git
cd TravelPlanner_agent
```

### 2. Set up the backend
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Add your IBM credentials
Edit `backend/app.py` and replace the placeholder values:
```python
API_KEY    = "your-ibm-cloud-api-key"
PROJECT_ID = "your-watsonx-project-id"
```

> **Never commit real API keys to GitHub.** Use environment variables in production.

### 4. Start the backend
```bash
python app.py
# Server running on http://localhost:5000
```

### 5. Open the frontend
Open `frontend/index.html` directly in your browser (no extra server needed).

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/plan` | Generate full trip itinerary |
| POST | `/api/chat` | TravelBot conversational reply |
| POST | `/api/suggest` | AI destination suggestions |
| GET | `/health` | Health check |

## License
MIT
