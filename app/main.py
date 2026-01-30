"""
FastAPI application for Gold & Silver Price Scraper API
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime

from .scraper import get_all_prices, get_gold_prices, get_silver_prices, GOLD_URL, SILVER_URL

app = FastAPI(
    title="Gold & Silver Price Scraper API",
    description="API for scraping gold and silver prices from btmc.vn",
    version="1.0.0"
)


@app.get("/")
async def health_check():
    """
    Health check endpoint.

    Returns:
        Status message and current timestamp
    """
    return {
        "status": "ok",
        "message": "Gold & Silver Price Scraper API is running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/prices")
async def get_prices():
    """
    Get all gold and silver prices.

    Returns:
        JSON containing timestamp, source, gold prices, and silver prices
    """
    try:
        data = get_all_prices()
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching prices: {str(e)}")


@app.get("/prices/gold")
async def get_gold():
    """
    Get gold prices only.

    Returns:
        JSON containing timestamp, source, and gold prices
    """
    try:
        gold_prices = get_gold_prices()
        return JSONResponse(content={
            "timestamp": datetime.now().isoformat(),
            "source": GOLD_URL,
            "gold": gold_prices
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching gold prices: {str(e)}")


@app.get("/prices/silver")
async def get_silver():
    """
    Get silver prices only.

    Returns:
        JSON containing timestamp, source, and silver prices
    """
    try:
        silver_prices = get_silver_prices()
        return JSONResponse(content={
            "timestamp": datetime.now().isoformat(),
            "source": SILVER_URL,
            "silver": silver_prices
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching silver prices: {str(e)}")
