# Crypto Dashboard Experiment

This project provides a basic example of a backend that polls a few crypto exchanges and stores prices to CSV files along with a simple frontend that can display the latest data.

## Backend

The backend is implemented in **Python** using the [`ccxt`](https://github.com/ccxt/ccxt) library for exchange APIs.

### Requirements

- Python 3.8+
- Packages listed in `backend/requirements.txt`

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

### Running the poller

The poller fetches the latest BTC price from a few exchanges and appends the data to `data/prices.csv`.

```bash
python backend/poll.py
```

You can schedule this script with `cron` or any job scheduler to run periodically (e.g. every minute or hour).

## Frontend

The frontend is a single-page application located in `frontend/index.html`. Open this file in a web browser to see the latest prices from the CSV file. For local testing you may need to serve the file via a small HTTP server due to browser security restrictions:

```bash
cd frontend
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

## Data

CSV files produced by the poller are stored in the `data/` directory.

## License

This project is licensed under the terms of the GPL-3.0 license. See the [LICENSE](LICENSE) file for details.
