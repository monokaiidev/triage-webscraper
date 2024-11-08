# Triage Webscraper

A webscraper made to get the website https://tria.ge and malware submissions! If a submission is over a 6 and it is part of a malware family, then it will automatically decompile it.

## Features

- **Decompiling**: Automatically extract the malware config (Discord Webhook, Discord Bot Token) (THANKS TO lululepu!!)
- **Nice Design**: Beautiful design overall
- **Auto-ignoring certain malware families**: If any of these malware families are detected, they will skip. 'asyncrat', 'atomsilo', 'blackmatter', 'cerber', 'urelas', 'xmrig', 'metasploit', 'xworm', 'cryptbot', 'cyrat', 'acobaltstrike', 'umbral', 'blacknet', 'berbew', 'blackmoon', 'emotet', 'mydoom', 'neshta', 'doomrat', 'shadowrat'

## Getting Started

### Prerequisites

- **Python** (v3.10.0 or later recommended)
- **Triage API Key** (only for decompiling! Not for webscraping.)
- **INFO** Please put your API Key in "api_key.txt". First line the API Key, nothing else! Just your API Key.
### Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/monokaiidev/triage-webscraper.git
    cd triage-webscraper
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Usage
1. **Run the Scraper**:
    ```bash
    python webscraper.py
    ```
