from web3 import Web3


infura_url = "https://celo-mainnet.infura.io/v3/72d31b15181d45fd90a61e08a3256b25"
web3 = Web3(Web3.HTTPProvider(infura_url))
print(web3.isConnected())

account_balance = web3.eth.get_balance("0x088a4CCeFBbdBe750cc34C3131Bd17077d145b34")
print(account_balance)