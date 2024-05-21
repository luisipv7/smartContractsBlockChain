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
with open('build/contracts/BirthCertificate.json') as f:
    contract_data = json.load(f)

abi = contract_data['abi']
contract_address = '0xBb8C6E9490176d6ACAF9fa75d1Ada5201F2e8975'  # Atualize isso com o endereço do contrato implantado

# Criar uma instância do contrato
contract = web3.eth.contract(address=contract_address, abi=abi)

# Definir a chave privada (garanta que ela está em formato hexadecimal)
PRIVATE_KEY = '0xYourPrivateKeyHere'  # Atualize isso com sua chave privada

# Definir o Schema do GraphQL
class Query(graphene.ObjectType):
    get_certificate = graphene.Field(
        graphene.JSONString,
        id=graphene.Int(required=True)
    )

    def resolve_get_certificate(self, info, id):
        cert = contract.functions.getCertificate(id).call()
        return {
            'name': cert[0],
            'dateOfBirth': cert[1],
            'placeOfBirth': cert[2],
            'parents': cert[3]
        }

class CreateCertificate(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        date_of_birth = graphene.String(required=True)
        place_of_birth = graphene.String(required=True)
        parents = graphene.String(required=True)

    success = graphene.Boolean()
    transaction_hash = graphene.String()

    def mutate(self, info, name, date_of_birth, place_of_birth, parents):
        txn = contract.functions.createCertificate(
            name, date_of_birth, place_of_birth, parents).build_transaction({
            'from': account,
            'nonce': web3.eth.get_transaction_count(account),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        web3.eth.wait_for_transaction_receipt(tx_hash)
        return CreateCertificate(success=True, transaction_hash=tx_hash.hex())

class Mutation(graphene.ObjectType):
    create_certificate = CreateCertificate.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

# Configurar o Flask
app = Flask(__name__)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(debug=True)
