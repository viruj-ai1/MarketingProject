# Synthesis Route Finder - Complete Project Overview

## 🎯 Project Goal
Build a Flask-based web application for pharmaceutical API (Active Pharmaceutical Ingredient) synthesis route analysis, manufacturer discovery, and buyer finding, deployed on Railway.

---

## 📋 Journey Summary

### **Phase 1: Initial Problem - Import Error**
**Problem:** `Import "phi.tools.crawl4ai_tools" could not be resolved`

**Solution:**
- Removed dependency on the problematic `phi` package
- Reimplemented `Crawl4aiTools` locally using `crawl4ai` directly
- Created `synthesis_engine/tools/crawl4ai_toolkit.py` with custom implementation

**Key Files:**
- `synthesis_route_finder/synthesis_engine/tools/crawl4ai_toolkit.py` - Local Crawl4AI implementation
- `synthesis_route_finder/synthesis_engine/tools/__init__.py` - Tool exports

---

### **Phase 2: Data Source Enforcement**
**Problem:** System was discovering manufacturers from general web searches (DuckDuckGo) instead of regulatory bodies only

**Solution:**
- Removed `DuckDuckGoTools` completely
- Updated agent instructions to only crawl regulatory websites (FDA, EMA, etc.)
- Modified `extract_manufacturers` to parse and validate `source` column
- Added `source_name` tracking in database

**Key Changes:**
- `api_manufacturer_discovery.py` - Removed web agent, enforced regulator-only discovery
- `api_manufacturer_service.py` - Added `delete_by_source` method for cleanup
- Database now tracks `source_name` to distinguish regulator vs. web discovery

---

### **Phase 3: Database Cleanup**
**Problem:** Existing "web_discovery" entries needed removal

**Solution:**
- Added `delete_by_source` method to `ApiManufacturerService`
- Allows SQL-based deletion of records by source name
- Supports both exact match and LIKE pattern matching

**Usage:**
```sql
-- Example: Delete all web_discovery entries for a specific API
DELETE FROM api_manufacturers 
WHERE LOWER(source_name) LIKE '%web%' 
AND LOWER(api_name) = 'roxadustat';
```

---

### **Phase 4: Service Architecture Refactoring**
**Problem:** Code organization needed improvement for better maintainability

**Solution:**
- Created `ApiManufacturerDiscoveryService` class to wrap discovery workflow
- Separated concerns: discovery logic vs. database operations
- Improved error handling and result normalization

**Key Files:**
- `api_manufacturer_discovery.py` - Contains `ApiManufacturerDiscoveryService` class
- `app.py` - Uses service class instead of direct function calls

---

### **Phase 5: Railway Deployment Preparation**

#### **5.1: Python Version Pinning**
**Problem:** Railway was using Python 3.13, causing build failures with older packages

**Solution:**
- Created `runtime.txt` with `python-3.12.0`
- Ensures consistent Python version across deployments

**File:** `runtime.txt`

---

#### **5.2: Dependency Conflicts**
**Problem 1:** `Pillow==10.1.0` conflicted with `crawl4ai==0.7.4` (requires `pillow>=10.4`)

**Solution:**
- Updated `Pillow==10.4.0` in both `requirements.txt` files

**Problem 2:** `openai==1.51.0` conflicted with `litellm>=1.53.1` (requires `openai>=1.54.0`)

**Solution:**
- Changed to `openai>=1.54.0` to allow pip to resolve compatible version

**Files:**
- `requirements.txt`
- `synthesis_route_finder/requirements.txt`

---

#### **5.3: Build Configuration**
**Problem:** Railway's default Railpack builder wasn't handling dependencies correctly

**Solution:**
- Created `nixpacks.toml` with custom build steps
- Explicitly upgrades pip, setuptools, wheel before installing
- Uses `--no-build-isolation` flag for problematic packages
- Installs system dependencies (libpq, X libraries for RDKit)

**File:** `nixpacks.toml`

**Key Configuration:**
```toml
[phases.install]
cmds = [
  "python -m venv --copies /app/.venv",
  ". /app/.venv/bin/activate && pip install --upgrade pip setuptools wheel",
  ". /app/.venv/bin/activate && pip install --no-build-isolation -r requirements.txt"
]

[start]
cmd = "cd synthesis_route_finder && gunicorn --config gunicorn.conf.py app:app"
```

---

### **Phase 6: Memory Optimization (SIGKILL Fix)**
**Problem:** Application was being killed with SIGKILL due to out-of-memory errors on Railway's free tier

**Solution:**

#### **6.1: Gunicorn Configuration**
Created `gunicorn.conf.py` with memory-optimized settings:
- **1 worker only** (reduces memory footprint)
- **max_requests = 1000** (prevents memory leaks by restarting workers)
- **preload_app = False** (avoids loading app before forking)
- **timeout = 300** (allows longer-running operations)

**File:** `synthesis_route_finder/gunicorn.conf.py`

#### **6.2: Lazy Loading**
**Problem:** Heavy services were being initialized at startup, consuming memory immediately

**Solution:**
- Created `initialize_services()` function for lazy initialization
- Services (`SynthesisAnalyzer`, `ApiBuyerFinder`, etc.) are only loaded when first needed
- Significantly reduces startup memory footprint

**Key Changes in `app.py`:**
- Removed initialization from `app.app_context()` block
- Added `initialize_services()` calls at the start of each endpoint
- Services are initialized once and reused

---

## 🏗️ Architecture Overview

### **Application Structure**
```
DOM_1/
├── synthesis_route_finder/
│   ├── app.py                          # Main Flask application
│   ├── gunicorn.conf.py                # Gunicorn memory optimization config
│   ├── requirements.txt                # Python dependencies
│   ├── synthesis_engine/
│   │   ├── analysis.py                 # Main synthesis analysis logic
│   │   ├── api_manufacturer_discovery.py  # Manufacturer discovery service
│   │   ├── api_manufacturer_service.py    # Database operations
│   │   ├── api_buyer_finder.py         # API buyer discovery
│   │   └── tools/
│   │       ├── __init__.py
│   │       └── crawl4ai_toolkit.py     # Local Crawl4AI implementation
│   └── templates/                      # HTML templates
├── requirements.txt                    # Root-level dependencies
├── runtime.txt                         # Python version pinning
└── nixpacks.toml                       # Railway build configuration
```

### **Key Services**

1. **SynthesisAnalyzer**
   - Analyzes API synthesis routes
   - Predicts optimal synthesis paths
   - Generates reaction visualizations

2. **ApiManufacturerDiscoveryService**
   - Discovers manufacturers from regulatory websites
   - Uses Crawl4AI to scrape FDA, EMA, etc.
   - Validates and normalizes manufacturer data

3. **ApiManufacturerService**
   - Manages manufacturer database operations
   - Query, insert, delete operations
   - Source tracking and filtering

4. **ApiBuyerFinder**
   - Finds potential API buyers
   - Searches pharmaceutical databases
   - Tracks buyer information

---

## 🔧 Technology Stack

### **Backend**
- **Flask 3.0.3** - Web framework
- **Gunicorn 21.2.0** - WSGI HTTP server
- **SQLAlchemy 2.0.23** - Database ORM
- **psycopg2-binary 2.9.9** - PostgreSQL adapter

### **AI/ML**
- **agno 1.1.12** - Agent framework
- **groq 0.19.0** - LLM provider (using llama-3.3-70b-versatile)
- **crawl4ai 0.7.4** - Web crawling
- **openai>=1.54.0** - LLM client (via litellm)

### **Data Processing**
- **pandas 2.1.3** - Data manipulation
- **rdkit 2023.09.1** - Chemical informatics
- **scikit-learn 1.3.2** - Machine learning

### **Database**
- **PostgreSQL** (via Supabase) - Primary database
- **SQLite** - Local caching/storage

---

## 🚀 Deployment Configuration

### **Railway Setup**
1. **Build System:** Nixpacks (custom configuration)
2. **Python Version:** 3.12.0 (pinned in `runtime.txt`)
3. **Start Command:** `cd synthesis_route_finder && gunicorn --config gunicorn.conf.py app:app`
4. **Memory:** Optimized for free tier (1 worker, lazy loading)

### **Environment Variables Required**
- `GROQ_API_KEY` - For LLM queries
- `SUPABASE_URL` - Database connection
- `SUPABASE_KEY` - Database authentication
- `GOOGLE_API_KEY` - For Google Custom Search (optional)
- `GOOGLE_CSE_ID` - Google Custom Search Engine ID (optional)
- `PORT` - Server port (Railway sets automatically)

---

## 📊 Key Features

### **1. Synthesis Route Analysis**
- Analyzes API synthesis routes
- Predicts optimal synthesis paths
- Generates reaction visualizations
- Provides yield and viability metrics

### **2. Manufacturer Discovery**
- **Regulator-Only Discovery:** Only sources from FDA, EMA, and other regulatory bodies
- **Automatic Persistence:** New manufacturers saved to Supabase
- **Source Tracking:** Every record tagged with source name
- **Duplicate Prevention:** Skips existing manufacturers

### **3. Buyer Finding**
- Searches pharmaceutical databases
- Finds potential API buyers
- Tracks company information and product details

### **4. Data Export**
- Download manufacturers as CSV/Excel
- Download buyers as CSV/Excel
- Includes all database records

---

## 🔒 Security & Best Practices

### **Implemented**
- ✅ Environment variables for sensitive keys
- ✅ SQL injection prevention (parameterized queries)
- ✅ Input validation on all endpoints
- ✅ Error handling with proper HTTP status codes
- ✅ Lazy loading to reduce memory footprint
- ✅ Worker restart to prevent memory leaks

### **Removed**
- ❌ Hardcoded API keys
- ❌ OpenAI API key references (using Groq only)
- ❌ Web discovery (DuckDuckGo) - regulator-only now

---

## 📈 Performance Optimizations

1. **Memory Management**
   - Single Gunicorn worker
   - Lazy service initialization
   - Worker restart after 1000 requests
   - No app preloading

2. **Database**
   - Efficient queries with proper indexing
   - Batch operations where possible
   - Connection pooling via SQLAlchemy

3. **Caching**
   - Session-based caching for analysis results
   - Database query result caching

---

## 🐛 Issues Resolved

1. ✅ Import error for `phi.tools.crawl4ai_tools`
2. ✅ Web discovery contamination (removed DuckDuckGo)
3. ✅ Database cleanup (web_discovery entries)
4. ✅ Python version conflicts (pinned to 3.12.0)
5. ✅ Pillow version conflict (updated to 10.4.0)
6. ✅ OpenAI version conflict (updated to >=1.54.0)
7. ✅ Build failures on Railway (custom nixpacks.toml)
8. ✅ SIGKILL memory errors (Gunicorn config + lazy loading)

---

## 📝 Development Workflow

### **Local Development**
```bash
cd synthesis_route_finder
pip install -r requirements.txt
python app.py
```

### **Deployment**
1. Push to GitHub
2. Railway auto-deploys from master branch
3. Build uses `nixpacks.toml` configuration
4. App starts with optimized Gunicorn config

---

## 🎓 Lessons Learned

1. **Dependency Management:** Always pin versions and test compatibility
2. **Memory Optimization:** Critical for free-tier deployments
3. **Lazy Loading:** Reduces startup memory significantly
4. **Build Configuration:** Custom build configs solve many deployment issues
5. **Data Source Validation:** Always validate and track data sources

---

## 🔮 Future Improvements

1. **Caching Layer:** Redis for session and query caching
2. **Background Jobs:** Celery for long-running tasks
3. **API Rate Limiting:** Prevent abuse
4. **Monitoring:** Add logging and metrics
5. **Database Indexing:** Optimize query performance
6. **Error Recovery:** Better retry mechanisms

---

## 📞 Support

For issues or questions:
- Check logs in Railway dashboard
- Review `gunicorn.conf.py` for memory settings
- Verify environment variables are set correctly
- Check database connection in Supabase

---

**Last Updated:** November 2025
**Status:** ✅ Production Ready (Optimized for Railway Free Tier)

