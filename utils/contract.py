
from web3 import Web3
from solcx import compile_source

# Solidity source code
compiled_sol = compile_source(
     '''
     pragma solidity >0.5.0;

     contract Greeter {
         string public greeting;

         constructor() public {
             greeting = 'Hello';
         }

         function setGreeting(string memory _greeting) public {
             greeting = _greeting;
         }

         function greet() view public returns (string memory) {
             return greeting;
         }
     }
     ''',
     output_values=['abi', 'bin']
 )

# retrieve the contract interface
contract_id, contract_interface = compiled_sol.popitem()

# get bytecode / bin
bytecode = contract_interface['bin']

# get abi
abi = contract_interface['abi']

ganache_url = 'HTTP://127.0.0.1:7545'
web3 = Web3(Web3.HTTPProvider(ganache_url))
print(web3.isConnected())
web3.eth.defaultAccount=web3.eth.accounts[0]

# web3.py instance
#w3 = Web3(Web3.EthereumTesterProvider())

# set pre-funded account as sender
#w3.eth.default_account = w3.eth.accounts[0]

Greeter = web3.eth.contract(abi=abi, bytecode=bytecode)

# Submit the transaction that deploys the contract
tx_hash = Greeter.constructor().transact()
print(web3.toHex(tx_hash))

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

greeter = web3.eth.contract(
     address=tx_receipt.contractAddress,
     abi=abi
 )

print(greeter.functions.greet().call())
 
tx_hash = greeter.functions.setGreeting('Nihao').transact()
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(greeter.functions.greet().call())
