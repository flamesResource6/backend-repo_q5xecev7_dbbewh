import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime

from database import create_document

app = FastAPI(title="EABL Kenya API", description="Content and interactions for the EABL showcase site")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Models
# -----------------------------
class SubscribeRequest(BaseModel):
    email: EmailStr
    language: Optional[str] = "en"

class Brand(BaseModel):
    name: str
    category: str
    tagline: Optional[str] = None
    image: Optional[str] = None
    color: Optional[str] = None
    featured: bool = False

class NewsPost(BaseModel):
    title: str
    summary: str
    image: Optional[str] = None
    link: Optional[str] = None
    published_at: Optional[str] = None
    tags: Optional[List[str]] = None

class InvestorMetric(BaseModel):
    revenue: float
    growth_percent: float
    share_price: float
    updated_at: Optional[str] = None
    report_url: Optional[str] = None
    nse_url: Optional[str] = None

# -----------------------------
# Health
# -----------------------------
@app.get("/")
def read_root():
    return {"message": "EABL Kenya API running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the EABL backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# -----------------------------
# Content Endpoints
# -----------------------------
@app.get("/api/brands", response_model=List[Brand])
def get_brands():
    gold = "#D4AF37"  # gold
    tusker = "#FFD100"  # tusker yellow
    deep_green = "#0A3B2E"
    black = "#111111"
    return [
        # Beer
        {"name": "Tusker Lager", "category": "Beer", "tagline": "Kenya's iconic lager since 1922", "image": None, "color": tusker, "featured": True},
        {"name": "Tusker Malt", "category": "Beer", "tagline": "Full-bodied, smooth finish", "image": None, "color": deep_green},
        {"name": "Guinness", "category": "Beer", "tagline": "Bold. Characterful. Iconic.", "image": None, "color": black},
        {"name": "Pilsner", "category": "Beer", "tagline": "Crisp and refreshing", "image": None, "color": "#F5D06C"},
        {"name": "White Cap", "category": "Beer", "tagline": "Pure mountain refreshment", "image": None, "color": "#C0D6E8"},
        {"name": "Senator Keg", "category": "Beer", "tagline": "Quality, affordable", "image": None, "color": "#B87333"},
        # Spirits
        {"name": "Johnnie Walker", "category": "Spirits", "tagline": "Keep Walking", "image": None, "color": gold, "featured": True},
        {"name": "Smirnoff", "category": "Spirits", "tagline": "Vibrant and versatile", "image": None, "color": "#E50914"},
        {"name": "Chrome Vodka", "category": "Spirits", "tagline": "Crisp, clean taste", "image": None, "color": "#B0B7C3"},
        {"name": "Gilbey’s", "category": "Spirits", "tagline": "Classic gin character", "image": None, "color": "#0A5B83"},
        {"name": "Captain Morgan", "category": "Spirits", "tagline": "Spiced adventure", "image": None, "color": "#7F1D1D"},
        {"name": "Jebel Gold", "category": "Spirits", "tagline": "Rich and smooth", "image": None, "color": gold},
        # Non-Alcoholic
        {"name": "Alvaro", "category": "Non-Alcoholic", "tagline": "Natural malt refreshment", "image": None, "color": "#8BC34A"},
        {"name": "Malta", "category": "Non-Alcoholic", "tagline": "Wholesome malt goodness", "image": None, "color": "#6B4F1D"},
        {"name": "Energy Drinks", "category": "Non-Alcoholic", "tagline": "Boost with flavor", "image": None, "color": "#00BCD4"},
    ]

@app.get("/api/news", response_model=List[NewsPost])
def get_news():
    now = datetime.utcnow().strftime("%Y-%m-%d")
    return [
        {"title": "EABL marks 100 years of brewing excellence", "summary": "A century of innovation, sustainability, and community.", "image": None, "link": "https://www.eabl.com/", "published_at": now, "tags": ["heritage", "centenary"]},
        {"title": "Tusker celebrates Kenyan sporting champions", "summary": "Proudly supporting local talent with bold new campaign.", "image": None, "link": "https://www.tusker.beer/", "published_at": now, "tags": ["campaign", "sports"]},
        {"title": "Investing in water stewardship across East Africa", "summary": "Scaling conservation and community water access.", "image": None, "link": "https://www.diageo.com/", "published_at": now, "tags": ["sustainability", "water"]}
    ]

@app.get("/api/investor-metrics", response_model=InvestorMetric)
def get_investor_metrics():
    return {
        "revenue": 116.3,  # billions KES (illustrative)
        "growth_percent": 7.8,
        "share_price": 189.5,
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d"),
        "report_url": "https://www.eabl.com/en/investors/reports",
        "nse_url": "https://www.nse.co.ke/"
    }

# -----------------------------
# Newsletter subscribe (persists to DB)
# -----------------------------
@app.post("/api/subscribe")
def subscribe(req: SubscribeRequest):
    try:
        doc_id = create_document("subscriber", req.dict())
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
