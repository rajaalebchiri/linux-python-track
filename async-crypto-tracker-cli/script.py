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
  'X-CMC_PRO_API_KEY': 'api-key',
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


async def get_coin(coin: str, n: int = None):

    async with aiohttp.ClientSession(headers=headers) as session:
        if n is not None:
            print(f"Getting {coin} price")
            while True:
                print(f"Getting {coin} price at {time.strftime('%H:%M:%S')}")
                async with session.get(f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest", params={"symbol": coin}) as response:
                    data = await response.text()
                    data = json.loads(data)
                    coin_data = data["data"][coin]
                    c = Coin(coin, coin_data['name'], coin_data['symbol'], coin_data['slug'], coin_data['quote']['USD']['price'])
                    print(c)
                await asyncio.sleep(n)

        else:
            async with session.get(f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest", params={"symbol": coin}) as response:
                data = await response.text()
                data = json.loads(data)
                coin_data = data["data"][coin]
                c = Coin(coin, coin_data['name'], coin_data['symbol'], coin_data['slug'], coin_data['quote']['USD']['price'])
                print(c)


async def convert_coin(amount: float, from_coin: str, to: str):

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"https://pro-api.coinmarketcap.com/v1/tools/price-conversion", 
            params={"symbol": from_coin, "convert": to, "amount": amount}) as response:
            data = await response.text()
            data = json.loads(data)
            coin_data = data["data"]
            print(f"{amount} {from_coin} is equal to {coin_data['quote'][to]['price']} {to}")

            
    

async def get_coins(limit: int = 5):
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit={limit}'
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:

            data = await response.text()
            data = json.loads(data)

            for coin in data["data"]:
                c = Coin(coin['id'], coin['name'], coin['symbol'], coin['slug'], coin['quote']['USD']['price'])
                print(c)

async def top_coins(limit: int = 5):
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&limit={limit}'
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:

            data = await response.text()
            data = json.loads(data)

            for coin in data["data"]:
                c = Coin(coin['id'], coin['name'], coin['symbol'], coin['slug'], coin['quote']['USD']['price'])
                print(c)



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--track", help="Get current price of specific coin", action="store_true")

    parser.add_argument("-c", "--coin", help="Coin to track")

    parser.add_argument("-n", "--number", help="Number of seconds to wait between each update", type=int)

    parser.add_argument("--top", help="List Top coins", action="store_true")

    parser.add_argument("-l", "--limit", help="Limit the number of coins to list", type=int)

    parser.add_argument("--convert", help="Convert Coin", action="store_true")

    parser.add_argument("-a", "--amount", help="The amount you want to convert", type=int)

    parser.add_argument("-f", "--from-coin", help="From Coin", type=str)

    parser.add_argument("-t", "--to-coin", help="To Coin", type=str)

    args = parser.parse_args()


    if args.track:
        if not args.coin:
            print("you need to specify the coin symbol")
        else:
            asyncio.run(get_coin(args.coin, args.number))
    if args.top:
        if args.limit:
            asyncio.run(top_coins(args.limit))
        else:
            asyncio.run(top_coins())

    if args.convert:
        if args.amount and args.from_coin and args.to_coin:
            print(f"Converting {args.amount} {args.from_coin} to {args.to_coin}")
            asyncio.run(convert_coin(float(args.amount), args.from_coin, args.to_coin))
        else:
            print("you need to specify the amount, from coin, and to coin")
        
    else:
        asyncio.run(get_coins())

if __name__ == "__main__":
    main()
