# LCBO Scraper

A web scraper for the LCBO (Liquor Control Board of Ontario) website that extracts product information including names, volumes, and prices.

## Features

- Scrapes product data from LCBO website
- Supports multiple categories (Wine, Spirits, Beer & Cider, Coolers)
- Saves data in JSON format
- Headless browser operation

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd lcbo_Scraper
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Chrome WebDriver**
   - Download ChromeDriver from: https://chromedriver.chromium.org/
   - Make sure it's in your system PATH or in the same directory as the script

## Usage

Run the scraper:
```bash
python main.py
```

This will:
- Scrape all configured categories
- Save results to JSON files in the current directory
- Files will be named: `Wine.json`, `Spirits.json`, `Beer & Cider.json`, `Coolers.json`

## Configuration

Edit `main.py` to modify the categories to scrape:

```python
CATEGORIES = [
    "Wine",
    "Spirits", 
    "Beer%20%26%20Cider",
    "Coolers",
    # Add more categories as needed
]
```

## Dependencies

- `selenium` - Web browser automation
- `beautifulsoup4` - HTML parsing
- Chrome browser and ChromeDriver

## Output

The scraper generates JSON files containing product information:
- Product name
- Volume/size
- Price

## Notes

- The scraper runs in headless mode
- Includes rate limiting and proper user agent headers
- Handles dynamic content loading with "Load More" buttons 