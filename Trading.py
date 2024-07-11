import asyncio
import sys
from web3 import Web3
import time
import os
from dotenv import load_dotenv

load_dotenv()
private_key = os.getenv("PRIVATE_KEY")



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


# -------------------------------- INITIALISE ------------------------------------------

class BinanceTrading:
  pass
