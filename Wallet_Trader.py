import json
import websockets
from web3 import Web3
import datetime
import asyncio
from Trading import BinanceTrading
import os
from dotenv import load_dotenv

load_dotenv()
snipeAmount = os.getenv('BNB_AMOUNT')
Trading = BinanceTrading()


class style():  # Class of different text colours - default is white
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


def getTimestamp():
    while True:
        timeStampData = datetime.datetime.now()
        currentTimeStamp = "[" + timeStampData.strftime("%H:%M:%S.%f")[:-3] + "]"
        return currentTimeStamp


def format_hex(original_hex):
    hex_without_prefix = original_hex[2:]
    desired_length = 64
    padded_hex = hex_without_prefix.zfill(desired_length)
    final_hex = "0x" + padded_hex
    return final_hex.lower()


infura_ws_url = "wss://bsc-mainnet.core.chainstack.com/your_api_key"
infura_http_url = 'https://bsc-mainnet.core.chainstack.com/your_api_key'
web3 = Web3(Web3.HTTPProvider(infura_http_url))
WETH = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"

#Addresses I want to copy
addresses = [
    "0x05C6e72A7b7A21E9858749fcd051C9d99C2fb8Ea",
    "0x1210Fde723E1d0eBc8BEF4f36100D04E8BAea436",
    "0x4C9ab021E705e1921fB342127B6378B29310Da99",
    "0xb30fd217006dec410beb90e17ae9c598ccd3aba6",
    "0x3b85e303a4171f2a751035adfee56e2a4a8d5aa8",
    "0x000461A73d3985eef4923655782aA5d0De75C111"
]
