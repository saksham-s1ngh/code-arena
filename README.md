# CodeArena – Real-Time Coding Battle Platform

## Migrating this project to Javascript (realised a better implementation could be done with JS)

A multiplayer, real-time platform for users to join rooms, solve coding challenges collaboratively or competitively, and level up through head-to-head matches.

## 🌐 Project Goals

- Real-time coding rooms with code editors
- Live collaboration and competitive scoring
- Secure, sandboxed code execution (Python initially)
- Backend built with FastAPI and templated with Jinja2
- Deployed using Docker and a modern cloud provider

---

## ✅ MVP Feature Checklist

### 🔧 Setup & Infrastructure
- [x] Project scaffold with FastAPI + Jinja2
- [x] Serve static files and templates
- [x] Basic routing with working pages
- [x] Git repo + `.gitignore` + `requirements.txt`

### 👤 User Authentication
- [x] Signup page (`/signup`)
- [x] Login page (`/login`)
- [x] POST-based form handling
- [x] Password hashing with `passlib`
- [x] Session-based login state
- [x] Auth-protected `/dashboard`

### 🏟 Room Management
- [ ] Create/join room routes
- [ ] Assign static problem to room
- [ ] Display problem in room
- [ ] In-browser code editor integration

### 🧪 Code Execution
- [ ] Backend API to receive and run code
- [ ] Docker sandbox execution (Python)
- [ ] Output + error display on frontend
- [ ] Submission saving (match history)

### ⚡ Real-Time Sync
- [ ] WebSocket server setup
- [ ] Code sync between users
- [ ] Typing indicators
- [ ] Room timer

### 🧩 Game Mechanics
- [ ] Track submissions + time
- [ ] Scoreboard display
- [ ] Declare winner
- [ ] Room freeze on win

### 🚀 Deployment & Polish
- [ ] Dockerize app
- [ ] Deploy to Render/Fly.io/Railway
- [ ] Enable HTTPS
- [ ] Add favicon, SEO, and responsive design

---

## 📦 Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy
- **Frontend**: Jinja2 templates, HTML/CSS, Monaco Editor
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Real-Time**: FastAPI WebSockets
- **Execution**: Docker-based sandbox
- **Deployment**: Railway / Render / Fly.io

---

## 📌 Setup

```bash
# Set up venv
python -m venv virtual-env
source virtual-env/bin/activate


# Install dependencies
pip install -r requirements.txt

# 🚀 Running the App (Development)
## 1. Navigate to the project root:
## 2. Start the FastAPI server with Uvicorn
PYTHONPATH=. uvicorn backend.main:app --reload
```

---

### 🧱 One-Time Database Setup

To create the initial database tables, run the `init_db.py` script:
(Python doesn’t automatically treat the root of your project as an importable module path. 
Setting `PYTHONPATH=.` tells Python to look in the current directory (i.e., project root) 
when resolving imports like `from backend.models import User`.)

```bash
# From the project root
PYTHONPATH=. python backend/init_db.py
```
