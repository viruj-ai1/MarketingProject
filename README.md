# Synthesis Route Finder 🧪

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Railway Ready](https://img.shields.io/badge/Railway-Ready-purple.svg)](https://railway.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered Flask web application designed for pharmaceutical intelligence. The platform automates API (Active Pharmaceutical Ingredient) synthesis route analysis, discovering verified manufacturers strictly from regulatory sources, and identifying potential API buyers.

---

## 🌟 Key Features

1. **Synthesis Route Analysis**
   - AI-driven prediction of optimal synthesis paths for APIs.
   - Generates visual reaction pathways.
   - Provides yield and viability metrics using advanced ML models.

2. **Verified Manufacturer Discovery**
   - **Regulator-Only Crawling:** Automatically scrapes and extracts manufacturer data exclusively from trusted regulatory bodies (FDA, EMA, etc.) using `Crawl4AI`.
   - **Automated Database Persistence:** Stores newly discovered manufacturers securely in a PostgreSQL (Supabase) database, ensuring no duplicate entries.
   - **Source Tracking:** Maintains a clear audit trail of data sources.

3. **Strategic Buyer Identification**
   - Automated searches through pharmaceutical databases to identify potential FDF (Finished Dosage Form) manufacturers and buyers.
   - Tracks comprehensive company information and product details.

4. **Data Management & Export**
   - Download complete manufacturer and buyer lists in CSV or Excel formats directly from the dashboard.

---

## 🏗️ Architecture & Tech Stack

### **Backend**
- **Framework:** Flask 3.0.3 with Gunicorn WSGI server.
- **Database:** PostgreSQL (via Supabase) with SQLAlchemy ORM.
- **Python Version:** Pinned to `3.12.0`.

### **AI & Data Intelligence**
- **LLM Engine:** Groq (`llama-3.3-70b-versatile`) integrated via Agno and LiteLLM.
- **Web Crawling:** `crawl4ai` (Custom local implementation for regulator site parsing).
- **Informatics:** Pandas, RDKit, Scikit-learn.

---

## 🚀 Getting Started (Local Development)

### Prerequisites
- Python `3.12.0`
- PostgreSQL Database (e.g., Supabase)
- API Keys for Groq and optionally Tavily/Google Custom Search

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/viruj-ai1/MarketingProject.git
   cd MarketingProject/synthesis_route_finder
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the `synthesis_route_finder` directory and add the following keys:
   ```env
   GROQ_API_KEY=your_groq_api_key
   DATABASE_URL=your_supabase_postgresql_url
   # Optional:
   TAVILY_API_KEY=your_tavily_key
   ```

5. **Run the Application:**
   ```bash
   python app.py
   ```
   *The app will be accessible at `http://127.0.0.1:5000`*

---

## ☁️ Deployment (Railway)

This project is fully optimized for deployment on the **Railway Free Tier**. 

- Uses a custom `nixpacks.toml` to manage complex C-library dependencies (RDKit) and isolate builds.
- Gunicorn is configured in `gunicorn.conf.py` to prevent memory leaks (1 worker, max requests limit, lazy loading of heavy ML models).

Simply link this repository to your Railway project, set up the Environment Variables in the Railway dashboard, and it will deploy automatically.

---

## 🔒 Security

- Sensitive keys (API keys, DB credentials) have been completely stripped from the codebase and rely entirely on environment variables.
- Implements lazy loading and single-worker execution to prevent SIGKILL out-of-memory errors on limited-resource cloud deployments.
- Includes SQL injection prevention mechanisms via SQLAlchemy parameterization.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Ensure to update tests as appropriate.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
