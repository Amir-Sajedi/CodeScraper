# CodeScraper

A modular real estate data collection, processing, and API serving platform.

This project scrapes real estate listings from MelkRadar.com, processes and stores them in a MySQL database, and provides a REST API (using FastAPI) to access and analyze the listings. The data pipeline uses RabbitMQ for asynchronous task handling and messaging.

---

## Features

- **Data Scraping:** Collects real estate apartment and office data from MelkRadar.com via HTTP POST requests.
- **Queue-Based Processing:** Uses RabbitMQ to publish and consume scraped data, enabling scalable and decoupled processing.
- **Database Integration:** Stores listing data in a MySQL database with robust error handling.
- **REST API:** Exposes endpoints via FastAPI to fetch and analyze stored listings.
- **Containerized:** Easily deployable using Docker.

---

## Project Structure

```
.
├── Melkradar/
│   └── detector_scrapper/
│       └── new_scrapper.py        # Scrapes and publishes new listings to RabbitMQ
├── Server-side/
│   └── main.py                    # FastAPI backend serving listing data
├── sql_script.py                  # Consumes queue and inserts data into MySQL
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Container build file
└── README.md                      # You are here!
```

---

## Prerequisites

- **Docker** (recommended)  
  or
- Python 3.11+
- MySQL database (with the `listings` table)
- RabbitMQ server running locally or accessible from the container
- Python dependencies from `requirements.txt`

---

## Setup & Usage

### 1. Clone the repository

```bash
git clone https://github.com/SLFatemi/CodeScraper.git
cd CodeScraper
```

### 2. Build and Run with Docker (Recommended)

```bash
docker build -t codescraper .
docker run -p 8000:8000 codescraper
```

*This will:*
- Scrape new data from MelkRadar and publish to RabbitMQ (`new_scrapper.py`)
- Consume data from RabbitMQ and store in MySQL (`sql_script.py`)
- Start FastAPI backend (port 8000)

### 3. Manual Run (Advanced / Development)

Start dependencies (RabbitMQ, MySQL), then in three terminals:

- **Data Scraper:**  
  `python Melkradar/detector_scrapper/new_scrapper.py`
- **Consumer:**  
  `python sql_script.py`
- **API Server:**  
  `uvicorn Server-side.main:app --reload`

---

## Environment Variables & Configuration

Update database and RabbitMQ connection parameters as needed in:
- `sql_script.py` (MySQL and RabbitMQ)
- `Server-side/main.py` (MySQL)

---

## API Usage

After starting the server, access the FastAPI docs at:  
`http://localhost:8000/docs`

### Example endpoint

- `POST /link`  
  **Body:**  
  ```json
  { "link": "URL of the listing" }
  ```
  **Returns:**  
  Top 10 similar listings (dummy implementation for now).

---

## Database Schema

Create the following table in MySQL:

```sql
CREATE TABLE listings (
    id VARCHAR(255) PRIMARY KEY,
    url TEXT,
    name TEXT,
    address TEXT,
    price TEXT,
    area INT,
    room_count INT,
    year INT,
    feats JSON,
    images JSON
);
```

---

## Contributing

Contributions are welcome! Please open issues or pull requests for bug fixes, new features, or improvements.

---

## License

MIT License

---

## Acknowledgments

- [MelkRadar.com](https://melkradar.com) for data source
- [Maskan-file.ir](https://maskan-file.ir) for data source
- [FastAPI](https://fastapi.tiangolo.com/)
- [RabbitMQ](https://www.rabbitmq.com/)
- [PyMySQL](https://pymysql.readthedocs.io/)

---

## Security Notice

**Do not commit production credentials or secrets.**  
Current database and RabbitMQ connection details are for development only.
