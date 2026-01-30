"""
Scraper module for fetching gold and silver prices from btmc.vn
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional
from datetime import datetime

BASE_URL = "https://btmc.vn"
GOLD_ENDPOINT = "/Home/BGiaVang"
SILVER_ENDPOINT = "/Home/BGiaBac"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://btmc.vn/",
}


def fetch_page(endpoint: str) -> Optional[str]:
    """
    Fetch HTML content from btmc.vn endpoint.

    Args:
        endpoint: The API endpoint to fetch (e.g., /Home/BGiaVang)

    Returns:
        HTML content as string, or None if request fails
    """
    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {endpoint}: {e}")
        return None


def format_price(price_str: str) -> Optional[float]:
    """
    Convert price string to float (in thousands VND).

    Args:
        price_str: Price string like "17,800" or "17800" or "51306.539"

    Returns:
        Float price value, or None if parsing fails
    """
    if not price_str:
        return None
    try:
        cleaned = price_str.strip().replace(",", "")
        # Handle non-numeric values like "Liên hệ"
        if not cleaned or not cleaned.replace(".", "").isdigit():
            return None
        return float(cleaned)
    except (ValueError, AttributeError):
        return None


def parse_gold_prices(html: str) -> list[dict]:
    """
    Extract gold price data from HTML.

    Args:
        html: HTML content from gold price endpoint

    Returns:
        List of gold price dictionaries
    """
    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")
    prices = []

    rows = soup.select("table tr")

    for row in rows:
        cells = row.find_all("td")
        num_cells = len(cells)

        # Skip header rows or rows with insufficient cells
        if num_cells < 4:
            continue

        # Determine cell positions based on row structure
        # 5 cells: [image], name, purity, buy, sell
        # 4 cells: name, purity, buy, sell
        if num_cells >= 5:
            name_idx, purity_idx, buy_idx, sell_idx = 1, 2, 3, 4
        else:
            name_idx, purity_idx, buy_idx, sell_idx = 0, 1, 2, 3

        product_name = cells[name_idx].get_text(strip=True)
        purity = cells[purity_idx].get_text(strip=True)
        buy_price = format_price(cells[buy_idx].get_text(strip=True))
        sell_price = format_price(cells[sell_idx].get_text(strip=True))

        if product_name and (buy_price is not None or sell_price is not None):
            prices.append({
                "product": product_name,
                "purity": purity,
                "buy_price": buy_price,
                "sell_price": sell_price,
                "unit": "nghìn VNĐ/lượng"
            })

    return prices


def parse_silver_prices(html: str) -> list[dict]:
    """
    Extract silver price data from HTML.

    Args:
        html: HTML content from silver price endpoint

    Returns:
        List of silver price dictionaries
    """
    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")
    prices = []

    rows = soup.select("table tr")

    for row in rows:
        cells = row.find_all("td")
        num_cells = len(cells)

        # Skip header rows or rows with insufficient cells
        if num_cells < 3:
            continue

        # Determine cell positions based on row structure
        # 4 cells: [image], product, buy, sell
        # 3 cells: product, buy, sell
        if num_cells >= 4:
            product_idx, buy_idx, sell_idx = 1, 2, 3
        else:
            product_idx, buy_idx, sell_idx = 0, 1, 2

        product_name = cells[product_idx].get_text(strip=True)
        buy_price = format_price(cells[buy_idx].get_text(strip=True))
        sell_price = format_price(cells[sell_idx].get_text(strip=True))

        if product_name and (buy_price is not None or sell_price is not None):
            prices.append({
                "product": product_name,
                "buy_price": buy_price,
                "sell_price": sell_price,
                "unit": "nghìn VNĐ"
            })

    return prices


def get_gold_prices() -> list[dict]:
    """
    Fetch and parse gold prices from btmc.vn.

    Returns:
        List of gold price dictionaries
    """
    html = fetch_page(GOLD_ENDPOINT)
    return parse_gold_prices(html)


def get_silver_prices() -> list[dict]:
    """
    Fetch and parse silver prices from btmc.vn.

    Returns:
        List of silver price dictionaries
    """
    html = fetch_page(SILVER_ENDPOINT)
    return parse_silver_prices(html)


def get_all_prices() -> dict:
    """
    Fetch all gold and silver prices.

    Returns:
        Dictionary containing timestamp, source, gold prices, and silver prices
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "source": BASE_URL + "/",
        "gold": get_gold_prices(),
        "silver": get_silver_prices()
    }
