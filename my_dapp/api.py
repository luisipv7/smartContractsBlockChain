from flask import Flask
from flask_graphql import GraphQLView
import graphene
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

# Carregar o ABI e o endereço do contrato
with open('build/contracts/SimpleStorage.json') as f:
    contract_data = json.load(f)

abi = contract_data['abi']
contract_address = '0xDF28a2D057770178d7927E09Fc0A8dce77445673' #contract_data['networks']['1715813714482']['address']  # Usar o endereço correto do contrato

# Criar uma instância do contrato
contract = web3.eth.contract(address=contract_address, abi=abi)

# Definir a chave privada (garanta que ela está em formato hexadecimal)
PRIVATE_KEY = '0x11e7172cbfd145ae3565bebbfb16a64e96ac179a7c807aba9bad4c6de429412f'  # Atualize isso com sua chave privada do Ganache

# Definir o Schema do GraphQL
class Query(graphene.ObjectType):
    get_data = graphene.Int()

    def resolve_get_data(self, info):
        return contract.functions.getData().call()

class SetData(graphene.Mutation):
    class Arguments:
        data = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, data):
        # Construir a transação
        txn = contract.functions.setData(data).build_transaction({
            'from': account,
            'nonce': web3.eth.get_transaction_count(account),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })

        # Assinar a transação
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        web3.eth.wait_for_transaction_receipt(tx_hash)
        return SetData(success=True)

class Mutation(graphene.ObjectType):
    set_data = SetData.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

# Configurar o Flask
app = Flask(__name__)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(debug=True)
