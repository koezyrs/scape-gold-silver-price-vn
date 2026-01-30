# Gold & Silver Price Scraper API

A FastAPI web service that scrapes gold and silver prices from Phú Quý Group:
- Gold: [giavang.phuquygroup.vn](https://giavang.phuquygroup.vn/)
- Silver: [giabac.phuquygroup.vn](https://giabac.phuquygroup.vn/)

## Project Structure

```
scape-gold-silver-price-vn/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   └── scraper.py       # Scraping logic
├── requirements.txt
├── gold-price-api.service
└── README.md
```

## Local Development

### Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

| Endpoint             | Description                  |
| -------------------- | ---------------------------- |
| `GET /`              | Health check                 |
| `GET /prices`        | Get all gold & silver prices |
| `GET /prices/gold`   | Get gold prices only         |
| `GET /prices/silver` | Get silver prices only       |

### Example Response

```json
{
  "timestamp": "2026-01-31T10:30:00",
  "sources": {
    "gold": "https://giavang.phuquygroup.vn",
    "silver": "https://giabac.phuquygroup.vn"
  },
  "gold": [
    {
      "category": "VÀNG THƯƠNG HIỆU PHÚ QUÝ",
      "product": "VÀNG MIẾNG PHÚ QUÝ 999.9 1 LƯỢNG",
      "unit": "Vnđ/Lượng",
      "buy_price": 92500000,
      "sell_price": 94500000
    }
  ],
  "silver": [
    {
      "category": "BẠC THƯƠNG HIỆU PHÚ QUÝ",
      "product": "BẠC MIẾNG PHÚ QUÝ 999 1 LƯỢNG",
      "unit": "Vnđ/Lượng",
      "buy_price": 3848000,
      "sell_price": 3967000
    }
  ]
}
```

## Deployment on Ubuntu

### 1. Copy Files to Server

```bash
sudo mkdir -p /opt/gold-price-api
sudo cp -r . /opt/gold-price-api/
sudo chown -R www-data:www-data /opt/gold-price-api
```

### 2. Create Virtual Environment

```bash
cd /opt/gold-price-api
sudo -u www-data python3 -m venv venv
sudo -u www-data ./venv/bin/pip install -r requirements.txt
```

### 3. Install systemd Service

```bash
sudo cp gold-price-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gold-price-api
sudo systemctl start gold-price-api
```

### 4. Check Service Status

```bash
sudo systemctl status gold-price-api
```

### 5. View Logs

```bash
sudo journalctl -u gold-price-api -f
```

## API Usage Examples

```bash
# Health check
curl http://localhost:8001/

# Get all prices
curl http://localhost:8001/prices

# Get gold prices only
curl http://localhost:8001/prices/gold

# Get silver prices only
curl http://localhost:8001/prices/silver
```

## License

MIT
