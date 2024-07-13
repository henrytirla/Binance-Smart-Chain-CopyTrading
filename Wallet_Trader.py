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


monitored_wallets_hex = [format_hex(address) for address in addresses]
seen_hashes = set()
print(monitored_wallets_hex)


async def process_buy_transaction(txHash, amount_bought):
    try:

        receipt = web3.eth.get_transaction_receipt(txHash)
        transfer_details = web3.eth.get_transaction(txHash)
        from_address = transfer_details['from']
        txn_hash = web3.to_hex(transfer_details['hash'])
        block_num = transfer_details['blockNumber']
        if receipt['status'] == 1:

            eth_value = None

            for logs in receipt['logs']:
                if logs['address'] == WETH and web3.to_hex(logs['topics'][0]) == "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef":
                    hex_value = web3.to_hex(logs['data'])
                    integer_value = int(hex_value, 16)
                    eth_value = web3.from_wei(integer_value, 'ether')
                    eth_value = '{:.4f}'.format(eth_value)

            if eth_value is not None:
                first_log = receipt['logs'][0]
                second_log = receipt['logs'][1]
                third_log = receipt['logs'][2]

                print(f"{getTimestamp()} {style.RED}{block_num}{style.RESET} {style.GREEN} TOKEN BOUGHT: {second_log['address']}  Amount Bought: {amount_bought}{style.RESET} {style.MAGENTA} WALLET_ADDRESS: {from_address}{style.RESET} For {eth_value} BNB",style.RESET)

                print(f"TxnHash:  https://bscscan.com/tx/{txn_hash} ")
                print(style.MAGENTA + "====BUYING TRADE SALE SIMULATION=====", style.RESET)
                
                if second_log['address'] == "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c":
                    await Trading.buy(third_log['address'], snipeAmount)
                else:
                    await Trading.buy(second_log['address'], snipeAmount)
                # await asyncio.sleep(2)
              





        else:
            pass
    except Exception as e:
        print("An error occurred while processing a buy transaction:", e)


async def process_sell_transaction(txHash, amount_bought):
    try:
        receipt = web3.eth.get_transaction_receipt(txHash)
        transfer_details = web3.eth.get_transaction(txHash)
        from_address = transfer_details['from']
        txn_hash = web3.to_hex(transfer_details['hash'])
        block_num = transfer_details['blockNumber']
        bnb_value = None
        if receipt['status'] == 1:
            eth_value = None
            for logs in receipt['logs']:
                if logs['address'] == WETH and web3.to_hex(logs['topics'][0]) == "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef":
                    hex_value = web3.to_hex(logs['data'])
                    integer_value = int(hex_value, 16)
                    eth_value = web3.from_wei(integer_value, 'ether')
                    eth_value = '{:.4f}'.format(eth_value)
                    bnb_value = eth_value

        if bnb_value is not None:
            first_log = receipt['logs'][0]
            second_log = receipt['logs'][1]
            print(web3.to_hex(first_log['topics'][1]))
            print(
                f" {getTimestamp()} {style.RED}{block_num}{style.RESET} {style.YELLOW}TOKEN SOLD: {second_log['address']}  Amount Sold {amount_bought} {style.RESET}  {style.MAGENTA} WALLET_ADDRESS: {from_address}{style.RESET} For {eth_value} BNB",
                style.RESET)
            print(f"TxnHash:  https://bscscan.com/tx/{txn_hash} ")
            print(style.MAGENTA + "====SELLING TRADE SALE SIMULATION=====", style.RESET)

            if second_log['address'] != "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c":
                    await Trading.sell(second_log['address'])
            else:
                    await Trading.sell(first_log['address'])
            
            await Trading.sell(second_log['address'])




    except Exception as e:
        print("An error occurred while processing a sell transaction:", e)


async def get_event():
    async with websockets.connect(infura_ws_url) as websocket:
        subscription_data = {"jsonrpc": "2.0", "method": "eth_subscribe",
                             "params": ["logs", {"fromBlock": "latest", "topics": [
                                 "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
                             ]}], "id": 1}
        print(subscription_data)
        await websocket.send(json.dumps(subscription_data))

        while True:
            try:
                response = await websocket.recv()
                response_data = json.loads(response)
                txHash = response_data['params']['result']['transactionHash']
                topics = response_data["params"]["result"]['topics']
                log_address = response_data["params"]["result"]['address']
                if topics[
                    1] in monitored_wallets_hex and log_address != "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c" and txHash not in seen_hashes:  #
                    print(log_address)
                    print(type(log_address))
                    print(txHash, "adding to seen_hashes")
                    seen_hashes.add(txHash)
                    print('SELLING')
                    data = response_data["params"]["result"]['data']
                    second_number = data[66:]
                    value = Web3.to_int(hexstr=data)
                    tokenBought = value * 10 ** -18
                    await process_sell_transaction(txHash, tokenBought)
                if topics[
                    1] in monitored_wallets_hex and log_address == "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c" and txHash not in seen_hashes:  #
                    seen_hashes.add(txHash)

                    print('BUYING')
                    data = response_data["params"]["result"]['data']
                    second_number = data[66:]
                    value = Web3.to_int(hexstr=data)
                    tokenBought = value * 10 ** -18
                    await process_buy_transaction(txHash, tokenBought)

                if topics[
                    -1] in monitored_wallets_hex and txHash not in seen_hashes:  # and txHash not in seen_hashes                     seen_hashes.add(txHash)
                    seen_hashes.add(txHash)
                    print('BUYING')
                    data = response_data["params"]["result"]['data']
                    second_number = data[66:]
                    value = Web3.to_int(hexstr=data)
                    tokenBought = value * 10 ** -18
                    await process_buy_transaction(txHash, tokenBought)

            except Exception as e:
                # print("An error occurred while processing a transaction:", e)
                pass


if __name__ == "__main__":
    asyncio.run(get_event())
