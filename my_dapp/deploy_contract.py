from web3 import Web3
import json

# Conectar ao Ganache
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Verificar a conexão
if not web3.is_connected():
    raise Exception("Não foi possível conectar ao Ganache")

# Conta do Ganache
account = web3.eth.accounts[0]

# Carregar o ABI e o Bytecode do contrato
with open('build/contracts/SimpleStorage.json') as f:
    contract_data = json.load(f)

abi = contract_data['abi']
bytecode = contract_data['bytecode']

# Construir e assinar a transação para implantar o contrato
SimpleStorage = web3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = SimpleStorage.constructor().transact({
    'from': account,
    'gas': 2000000,
    'gasPrice': web3.to_wei('20', 'gwei')
})
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# Obter o endereço do contrato
contract_address = tx_receipt.contractAddress
print(f'Contrato implantado em: {contract_address}')
