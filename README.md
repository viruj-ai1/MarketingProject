# Synthesis Route Finder 🧪

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Render](https://img.shields.io/badge/Render-Backend-black.svg)](https://render.com/)
[![Vercel](https://img.shields.io/badge/Vercel-Frontend-black.svg)](https://vercel.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered web application designed for pharmaceutical intelligence. The platform automates API (Active Pharmaceutical Ingredient) synthesis route analysis, discovering verified manufacturers strictly from regulatory sources, and identifying potential API buyers. 

This project is architected for a decoupled deployment: **Backend API on Render** and **Frontend on Vercel**.

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

### **Backend (Render API)**
- **Framework:** Flask 3.0.3 API with Gunicorn WSGI server.
- **Database:** PostgreSQL (via Supabase) with SQLAlchemy ORM.
- **AI & Data Intelligence:** Groq (`llama-3.3-70b-versatile`), `crawl4ai`, Pandas, RDKit, Scikit-learn.

### **Frontend (Vercel)**
- **UI:** Web templates communicating with the Flask backend REST API.

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
   Create a `.env` file in the root directory and add the following keys:
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
   *The backend will be accessible locally, typically at `http://127.0.0.1:5000`.*

---

## ☁️ Deployment Guide

### 1. Backend Deployment on Render

The backend handles the AI-heavy lifting, web scraping, and database communication.

1. Create an account on [Render](https://render.com/).
2. Click **New +** and select **Web Service**.
3. Connect your GitHub repository.
4. **Configuration:**
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt` (or custom build steps if required by RDKit).
   - **Start Command:** `gunicorn app:app` (or `gunicorn --config gunicorn.conf.py app:app` for memory optimization).
5. Add your **Environment Variables** (`GROQ_API_KEY`, `DATABASE_URL`, etc.) under the "Environment" tab.
6. Deploy the service and note your new backend URL (e.g., `https://your-backend-api.onrender.com`).

### 2. Frontend Deployment on Vercel

The frontend application connects to the Render API to display data to users.

1. Update your frontend environment variables or API base URL configurations to point to your new **Render Backend URL**.
2. Create an account on [Vercel](https://vercel.com/).
3. Click **Add New Project** and import the frontend portion of your repository.
4. **Configuration:**
   - Define the Framework Preset (if using a specific framework, otherwise default).
   - Add any necessary frontend Environment Variables (e.g., `NEXT_PUBLIC_API_URL=https://your-backend-api.onrender.com`).
5. Click **Deploy**. Vercel will automatically build and host your frontend.

---

## 🔒 Security

- Sensitive keys (API keys, DB credentials) have been completely stripped from the codebase and rely entirely on environment variables.
- Implements lazy loading and worker isolation on Render to prevent out-of-memory errors.
- Cross-Origin Resource Sharing (CORS) should be configured on the Flask backend to only accept requests from your Vercel frontend URL.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Ensure to update tests as appropriate.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
