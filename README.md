# Code Scraper
## Overview
This project is designed to scrape data from various sources, process it through a queuing system, and store it in a MySQL database. The pipeline consists of data detectors, a RabbitMQ-based queuing system, and a Python-based converter to store data in MySQL.

## Architecture
1. **Detectors**: Custom scripts or tools responsible for scraping and collecting raw data from specified sources.
2. **RabbitMQ**: A message broker that queues the scraped data, ensuring reliable and scalable data processing.
3. **Converter**: A Python script that processes the queued data and stores it in a MySQL database.

## Prerequisites
- Python 3.8+
- RabbitMQ server (installed and running)
- MySQL server
- Required Python libraries (listed in `requirements.txt`)

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure RabbitMQ**:
   - Ensure RabbitMQ is installed and running.
   - Update the RabbitMQ connection settings in `config.py` (e.g., host, port, credentials).

4. **Configure MySQL**:
   - Set up a MySQL database and user.
   - Update the MySQL connection settings in `config.py` (e.g., host, database, user, password).

5. **Run Detectors**:
   - Execute the detector scripts to start scraping data:
     ```bash
     python detectors/<detector_script>.py
     ```

6. **Run Converter**:
   - Start the converter to process queued data and store it in MySQL:
     ```bash
     python converter.py
     ```

## Project Structure
```
├── detectors/              # Scripts for scraping data
├── converter.py            # Python script to process and store data in MySQL
├── config.py              # Configuration file for RabbitMQ and MySQL settings
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Usage
1. Start the RabbitMQ server.
2. Run the detector scripts to scrape data and send it to the RabbitMQ queue.
3. Run the `converter.py` script to consume data from the queue and store it in the MySQL database.

Example:
```bash
python detectors/scraper.py
python converter.py
```

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
