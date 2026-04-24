# 🏢 Agency 360 Portal

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![License](https://img.shields.io/badge/License-MIT-green)
![Last Commit](https://img.shields.io/github/last-commit/Edwing0634/agency-360-portal)

> Full-stack internal web portal for managing a 130+ agent sales force — deployable as a **desktop app** (PyWebView + PyInstaller) or a standard web application.

---

## 🏭 Background

Designed to replace spreadsheet-based tracking for a **130+ agent sales force at a multinational insurance company in Colombia**. The 4-role hierarchy (Admin → Senior → GA → GU), Elite Club rankings, and KPI dashboard were built around the actual reporting structure of the commercial team — where agency managers need to track their units independently while senior leadership sees the full picture.

Packaging as a `.exe` was a hard requirement: the target users are field managers without IT support, running Windows machines that can't expose internal DB ports to the web.

---

## ✨ Features

- **Role-Based Access Control** — Admin, Senior, GA (Agency Manager), GU (Unit Manager) with domain-restricted login
- **KPI Dashboard** — real-time production, achievement %, collections rate, new clients
- **Elite Club Rankings** — top performer leaderboard with medal badges
- **Consultants Directory** — searchable/filterable agent cards with unit filter
- **AI Copilot** — chat interface wired to a backend LLM (mock included, plug Azure OpenAI)
- **Desktop Mode** — ships as a single `.exe` via PyWebView + PyInstaller
- **Demo Mode** — runs fully offline with sample data (no DB required)

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, Flask 3.0 |
| Desktop wrapper | PyWebView 5.1 |
| Database | SQL Server (pyodbc) |
| Frontend | Bootstrap 5.3, Chart.js 4, Bootstrap Icons |
| Packaging | PyInstaller 6 |
| Config | python-dotenv |

---

## ⚡ Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Edwing0634/agency-360-portal.git
cd agency-360-portal

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment (optional — app works in demo mode without it)
cp .env.example .env
# Edit .env with your DB credentials

# 5. Run as desktop app
python app.py

# 6. Or run as web server
python app.py --web
```

**Demo login:** `admin@agency360.com` / any password

---

## 📁 Project Structure

```
agency-360-portal/
├── app.py              # Flask app + PyWebView launcher
├── config.py           # Environment-based configuration
├── build.py            # PyInstaller build script
├── models/
│   └── database.py     # pyodbc connection + demo data fallback
├── routes/
│   ├── auth.py         # Login / logout / decorators
│   ├── dashboard.py    # Main views
│   └── api.py          # JSON API endpoints
├── templates/          # Jinja2 HTML templates
├── static/             # CSS, JS, images
└── docs/
    └── architecture.md
```

---

## 🏗 Architecture

```
PyWebView (desktop shell)
        │
        ▼
Flask App (localhost:5000)
├── /login          → auth.py
├── /dashboard      → dashboard.py
├── /rankings       → dashboard.py
├── /consultants    → dashboard.py
├── /copilot        → dashboard.py
└── /api/*          → api.py (JSON)
        │
        ▼
Database Layer (pyodbc → SQL Server)
[falls back to demo data if no DB configured]
```

---

## ⚙️ Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask session secret | `dev-secret` |
| `DB_SERVER` | SQL Server hostname | `localhost` |
| `DB_NAME` | Database name | `agency360_db` |
| `DB_USER` | SQL login (leave empty for Windows Auth) | — |
| `DB_PASSWORD` | SQL password | — |
| `COMPANY_DOMAIN` | Email domain for login validation | `agency360.com` |
| `WINDOW_WIDTH` | Desktop window width | `1280` |
| `WINDOW_HEIGHT` | Desktop window height | `800` |

---

## 📦 Build Desktop App

```bash
python build.py
# Output: dist/Agency360Portal.exe
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

MIT © [Edwin González](https://github.com/Edwing0634)

---

## 👤 Author

**Edwin González** — Customer Intelligence Specialist & Full-Stack Developer

[![GitHub](https://img.shields.io/badge/GitHub-Edwing0634-black?logo=github)](https://github.com/Edwing0634)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/Edwin gonzalez)
