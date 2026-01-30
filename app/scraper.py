"""
Scraper module for fetching gold and silver prices from Phú Quý Group
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional
from datetime import datetime

GOLD_URL = "http://giavang.phuquygroup.vn"
SILVER_URL = "http://giabac.phuquygroup.vn"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def fetch_page(url: str) -> Optional[str]:
    """
    Fetch HTML content from URL.

    Args:
        url: The full URL to fetch

    Returns:
        HTML content as string, or None if request fails
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def format_price(price_str: str) -> Optional[int]:
    """
    Convert price string to integer (in VND).

    Args:
        price_str: Price string like "3,848,000"

    Returns:
        Integer price value, or None if parsing fails
    """
    if not price_str:
        return None
    try:
        cleaned = price_str.strip().replace(",", "")
        if not cleaned or not cleaned.isdigit():
            return None
        return int(cleaned)
    except (ValueError, AttributeError):
        return None


def parse_gold_prices(html: str) -> list[dict]:
    """
    Extract gold price data from giavang.phuquygroup.vn HTML.

    Args:
        html: HTML content from gold price page

    Returns:
        List of gold price dictionaries
    """
    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")
    prices = []

    rows = soup.select("table tbody tr")

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 3:
            continue

        product_name = cells[0].get_text(strip=True)
        buy_cell = row.select_one("td.buy-price")
        sell_cell = row.select_one("td.sell-price")

        buy_price = format_price(buy_cell.get_text(strip=True)) if buy_cell else None
        sell_price = format_price(sell_cell.get_text(strip=True)) if sell_cell else None

        if product_name and (buy_price is not None or sell_price is not None):
            prices.append({
                "product": product_name,
                "unit": "VNĐ/Chỉ",
                "buy_price": buy_price,
                "sell_price": sell_price,
            })

    return prices


def parse_silver_prices(html: str) -> list[dict]:
    """
    Extract silver price data from giabac.phuquygroup.vn HTML.

    Args:
        html: HTML content from silver price page

    Returns:
        List of silver price dictionaries
    """
    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")
    prices = []
    current_category = ""

    rows = soup.select("table tbody tr")

    for row in rows:
        # Check if this is a category header row
        header = row.select_one("td[colspan] .branch_title")
        if header:
            current_category = header.get_text(strip=True)
            continue

        # Get product cells
        product_cell = row.select_one("td.col-product")
        unit_cell = row.select_one("td.col-unit-value")
        buy_cells = row.select("td.col-buy-cell")

        if not product_cell or len(buy_cells) < 2:
            continue

        product_name = product_cell.get_text(strip=True)
        unit = unit_cell.get_text(strip=True) if unit_cell else ""
        buy_price = format_price(buy_cells[0].get_text(strip=True))
        sell_price = format_price(buy_cells[1].get_text(strip=True))

        if product_name and (buy_price is not None or sell_price is not None):
            prices.append({
                "category": current_category,
                "product": product_name,
                "unit": unit,
                "buy_price": buy_price,
                "sell_price": sell_price,
            })

    return prices


def get_gold_prices() -> list[dict]:
    """
    Fetch and parse gold prices from giavang.phuquygroup.vn.

    Returns:
        List of gold price dictionaries
    """
    html = fetch_page(GOLD_URL)
    return parse_gold_prices(html)


def get_silver_prices() -> list[dict]:
    """
    Fetch and parse silver prices from giabac.phuquygroup.vn.

    Returns:
        List of silver price dictionaries
    """
    html = fetch_page(SILVER_URL)
    return parse_silver_prices(html)


def get_all_prices() -> dict:
    """
    Fetch all gold and silver prices.

    Returns:
        Dictionary containing timestamp, sources, gold prices, and silver prices
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "sources": {
            "gold": GOLD_URL,
            "silver": SILVER_URL
        },
        "gold": get_gold_prices(),
        "silver": get_silver_prices()
    }
