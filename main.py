from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import requests
import random
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from functools import lru_cache  # Simple in-memory cache

load_dotenv()

app = FastAPI(title="Fish Facts API", version="1.1.0")

# Rate Limiter
limiter = Limiter(key_func=get_remote_address)  # Limits by IP
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware
if os.getenv("ENVIRONMENT") == "production":
    origins = ["https://fishey.neocities.org"]
else:
    origins = ["*"]   # Allow everything in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_NINJAS_KEY = os.getenv("API_NINJAS_KEY")
if not API_NINJAS_KEY:
    raise RuntimeError("API_NINJAS_KEY is not set in environment variables!")

# Caching
# In-memory cache: 100 items, TTL not built-in but good for demo
@lru_cache(maxsize=100)
def fetch_fish_data(query: str = "fish"):
    """Cached wrapper for external API call"""
    response = requests.get(
        "https://api.api-ninjas.com/v1/animals",
        headers={"X-Api-Key": API_NINJAS_KEY},
        params={"name": query},
        timeout=10
    )
    response.raise_for_status()
    return response.json()

@app.get("/fact")
@limiter.limit("30/minute")
async def get_random_fish_fact(request: Request):
    try:
        animals = fetch_fish_data("fish")
        
        if not animals:
            raise HTTPException(404, "No fish data found")
            
        animal = random.choice(animals)
        name = animal.get('name', 'Unknown Fish')
        char = animal.get('characteristics', {})
        tax = animal.get('taxonomy', {})
        
        # Rich fact building
        main_fact = (
            char.get('fact') or 
            char.get('description') or 
            f"The {name.lower()} is a fascinating marine creature."
        )
        
        return {
            "animal_name": name,
            "scientific_name": tax.get('scientific_name'),
            "details": {
                "habitat": char.get('habitat'),
                "diet": char.get('diet'),
                "lifespan": char.get('lifespan'),
                "weight": char.get('weight'),
                "length": char.get('length'),
                "color": char.get('color'),
                "predators": char.get('predators')
            },
            "cached": True
        }
        
    except Exception as e:
        raise HTTPException(500, "Failed to fetch fish fact")
        
    except Exception as e:
        raise HTTPException(500, "Failed to fetch fish fact")
        
        return {
            "fact": fact,
            "animal_name": animal.get('name'),
            "source": "API-Ninjas (cached)",
            "cached": True
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(503, "External API unavailable")
    except Exception as e:
        raise HTTPException(500, "Internal error")

@app.get("/search")
@limiter.limit("20/minute")
async def search_fish(request: Request, q: str):
    try:
        animals = fetch_fish_data(q.lower().strip())
        return {"query": q, "results": animals[:10]}  # Limit results
    except Exception:
        raise HTTPException(500, "Search failed")