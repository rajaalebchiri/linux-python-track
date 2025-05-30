import argparse
import aiohttp
import json
import asyncio
import time
from dataclasses import dataclass


parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'e25e7a84-828c-4f50-8488-859c5eed8d9e',
}

@dataclass
class Coin:
    id: int
    name: str
    symbol: str
    slug: str
    price: float

    def __str__(self):
        return f"{self.name} ({self.symbol}): ${self.price}"

async def fetch_json(session, url, params=None):
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        return await response.json()


async def get_coin(coin: str, n: int = None):
    async with aiohttp.ClientSession(headers=headers) as session:
        if n is not None:
            print(f"Getting {coin} price")
            while True:
                print(f"Getting {coin} price at {time.strftime('%H:%M:%S')}")
                response = fetch_json(session, url="https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest", params={"symbol": coin})
                data = await response
                coin_data = data["data"][coin]
                c = Coin(coin, coin_data['name'], coin_data['symbol'], coin_data['slug'], coin_data['quote']['USD']['price'])
                print(c)
                await asyncio.sleep(n)
        else:
            response = fetch_json(session, url="https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest", params={"symbol": coin})
            data = await response
            coin_data = data["data"][coin]
            c = Coin(coin, coin_data['name'], coin_data['symbol'], coin_data['slug'], coin_data['quote']['USD']['price'])
            print(c)


async def convert_coin(amount: float, from_coin: str, to: str):

    async with aiohttp.ClientSession(headers=headers) as session:
        response = fetch_json(session, url="https://pro-api.coinmarketcap.com/v1/tools/price-conversion", params={"symbol": from_coin, "convert": to, "amount": amount})
        data = await response
        coin_data = data["data"]
        print(f"{amount} {from_coin} is equal to {coin_data['quote'][to]['price']} {to}")

            
    
async def get_coins(limit: int = 5):
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit={limit}'
    async with aiohttp.ClientSession(headers=headers) as session:
        response = fetch_json(session, url)
        data = await response

        for coin in data["data"]:
            c = Coin(coin['id'], coin['name'], coin['symbol'], coin['slug'], coin['quote']['USD']['price'])
            print(c)

async def top_coins(limit: int):
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&limit={limit}'
    async with aiohttp.ClientSession(headers=headers) as session:
        response = fetch_json(session, url)
        data = await response

        for coin in data["data"]:
            c = Coin(coin['id'], coin['name'], coin['symbol'], coin['slug'], coin['quote']['USD']['price'])
            print(c)

def run_get_coin(args):
    asyncio.run(get_coin(args.coin, args.number))

def run_get_coins(_):
    asyncio.run(get_coins())

def run_top_coins(args):
    if args.limit is None:
        limit = 5
    else:
        limit = args.limit
    asyncio.run(top_coins(limit))

def main():
    parser = argparse.ArgumentParser(
        description="Crypto Tracker CLI",
        prog="crypto-tracker-cli",
    )

    subparsers = parser.add_subparsers(title="commands", dest="command")

    # get current price of specific coin command
    track_coin_parser = subparsers.add_parser("track-coin", help="Track coin price")
    track_coin_parser.add_argument('-c', '--coin', help='Coin symbol', required=True)
    track_coin_parser.add_argument('-n', '--number', help='Number of seconds to wait between each update', required=False, type=int)
    track_coin_parser.set_defaults(func=run_get_coin)

    # List Top coins
    track_coin_parser = subparsers.add_parser("top-coins", help="get top coins")
    track_coin_parser.add_argument('-l', '--limit', help='Limit the number of coins to list', type=int)
    track_coin_parser.set_defaults(func=run_top_coins)

    # Convert Coin
    convert_coin_parser = subparsers.add_parser("convert-coin", help="Convert Coin")
    convert_coin_parser.add_argument('-a', '--amount', help='Amount to convert', required=True, type=float)
    convert_coin_parser.add_argument('-f', '--from-coin', help='From Coin', required=True, type=str)
    convert_coin_parser.add_argument('-t', '--to-coin', help='To Coin', required=True, type=str)
    convert_coin_parser.set_defaults(func=lambda args: asyncio.run(convert_coin(args.amount, args.from_coin, args.to_coin)))



    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        run_get_coins(None)

                
if __name__ == "__main__":
    main()
