


          
# Cryptocurrency Tracker CLI

A command-line tool for tracking cryptocurrency prices and performing conversions using the CoinMarketCap API.

## Features

- Track specific cryptocurrency prices in real-time
- List top cryptocurrencies by market cap
- Convert between different cryptocurrencies
- Customizable update intervals for price tracking

## Usage

### Track a Specific Coin

```bash
# Get current price of a specific coin
python script.py --track -c BTC

# Track with automatic updates every N seconds
python script.py --track -c BTC -n 60  # Updates every 60 seconds
```

### List Top Cryptocurrencies

```bash
# List top 5 cryptocurrencies (default)
python script.py --top

# List specific number of top cryptocurrencies
python script.py --top -l 10  # Lists top 10
```

### Convert Between Cryptocurrencies

```bash
# Convert between cryptocurrencies
python script.py --convert -a 1 -f BTC -t USD  # Convert 1 BTC to USD
```

### Default Behavior

```bash
# List top 5 cryptocurrencies
python script.py
```

## Arguments

- `--track`: Track a specific cryptocurrency
- `-c, --coin`: Specify the coin symbol (e.g., BTC, ETH)
- `-n, --number`: Update interval in seconds
- `--top`: List top cryptocurrencies
- `-l, --limit`: Number of cryptocurrencies to list
- `--convert`: Convert between cryptocurrencies
- `-a, --amount`: Amount to convert
- `-f, --from-coin`: Source cryptocurrency
- `-t, --to-coin`: Target cryptocurrency

        