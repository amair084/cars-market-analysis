# 🚗 Cars.com Market Analysis

A desktop application for scraping, cleaning, and analyzing used car listings from Cars.com. Search any make and model, collect listing data, and visualize price trends — all from a clean GUI.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-8136B2?style=flat-square)
![Selenium](https://img.shields.io/badge/Scraper-Selenium-43B02A?style=flat-square&logo=selenium)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## Features

- **Scrape listings** from Cars.com by brand, model, and number of pages
- **Headless scraping** — Chrome runs silently in the background
- **Auto data cleaning** — normalizes price, mileage, year, and model fields
- **Interactive charts** — price vs mileage and price vs age scatter plots with dark mode
- **Built-in data viewer** — sortable, searchable CSV viewer with click-to-copy
- **Packagable as a standalone `.exe`** via PyInstaller

---

## Project Structure

```
cars-market-analysis/
│
├── app.py                  # Main application entry point
│
├── requirements.txt         # Holds the required dependencies to be installed for the system to function 
│
├── readme.md                
│ 
├── scrapers/
│   ├── __init__.py
│   └── scraper.py          # Selenium scraper for Cars.com
│
├── cleaner/
│   ├── __init__.py
│   └── data_clean.py       # Pandas data cleaning pipeline
│
├── analysis/
│   ├── __init__.py
│   ├── plot.py             # Matplotlib chart generation
│   └── viewer.py           # CSV data viewer window
│
├── chromedriver/
│   └── chromedriver.exe    # ChromeDriver binary (included)
│
├── resources/
│   ├── icon.ico
│   ├── logo.png
│   └── gitlgoo.png
│
└── data/                   # Auto-created on first run, stores scraped CSVs
```

---

## Requirements

- Python 3.10+
- Google Chrome installed

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/amair084/cars-market-analysis.git
   cd cars-market-analysis
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python app.py
   ```

---

## Usage

1. Enter a **Make** (e.g. `toyota`) and **Model** (e.g. `camry`)
2. Select the number of **pages to scrape** from the dropdown
3. Click **Analyse Listings** — Chrome will scrape in the background
4. Once complete, use the plot buttons to visualize the data:
   - **Price vs Model** — mileage vs price scatter plot
   - **Price vs Age** — age vs price scatter plot
5. Click **View Data** to open the CSV viewer and inspect raw listings

---

## Data Viewer

The built-in viewer supports:

- **Sorting** by any column — click a header to cycle ascending ↑ / descending ↓ / original
- **Smart numeric sorting** — price and mileage sort by value, not alphabetically
- **Search** — filters across all columns instantly as you type
- **Click to copy** — click any cell to copy its value to clipboard

---

## Building as an Executable

To package the app into a standalone `.exe`:

```bash
python -m PyInstaller --onefile --windowed --icon=resources/icon.ico --add-data "resources;resources" app.py
```

The output will be in `dist/`. Place `chromedriver/` next to the `.exe` before distributing. The `data/` folder is created automatically next to the `.exe` on first run.

---

## Notes

- The scraper targets **used and certified pre-owned** listings by default. This is controlled by the `stock_type=used` parameter in the Cars.com URL and can be changed to `new` or `all` in `scraper.py`.
- Occasionally Cars.com may block requests via Cloudflare. The scraper includes a 3-attempt refresh retry per page, but some runs may return fewer listings than expected.
- ChromeDriver is included in the `chromedriver/` folder. As long as you have Google Chrome installed, no additional setup is needed. If Chrome auto-updates and the scraper stops working, grab a matching ChromeDriver from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads) and replace the one in the folder.

---

## Author

**amair084** — [GitHub](https://github.com/amair084)
