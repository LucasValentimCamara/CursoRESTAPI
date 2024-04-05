from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt #biblioteca JWT-Extended -> biblioteca para fazer login e logout
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

atributos = reqparse.RequestParser() #consegue pegar tudoi que for passado pelo usuario
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")

class User(Resource):
	#/usuario/{user_id}		
	def get (self, user_id):
		user = UserModel.find_user(user_id)
		if user:
			return user.json() #hotel objeto
		return {'message': 'User not found.'}, 404 #not found

	@jwt_required()
	def delete (self, user_id):
		#linhas que deixaram de existir pela criação do BD e Models
		#global hoteis #se referenciando a variável lista de hoteis que já existe
			#Sem chamar global: UnboundLocalError: local variable 'hoteis' referenced before assigment
		#hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
			#pegando todos hoteis que não tem o id igual o id passado, criando uma nova lista e substituindo a original
		user = UserModel.find_user(user_id)
		if user:
			try:
				user.delete_user()
			except:
				return {'message': 'An error ocurred trying to delete user'}, 500 #internal server error
			return {'message': 'User deleted'}
		return {'message': 'User not found.'}, 404 #not found

class UserRegister(Resource):
	#/cadastro
	def post(self):
		
		dados = atributos.parse_args() #salvar os atributos na variavel dados

		if UserModel.find_by_login(dados['login']): #encontrar pelo login se ele existe no BD
			return {"message": "The login '{}' already exists.".format(dados['login'])}

		user = UserModel(**dados) #desembrulha o login e senha
		user.save_user()
		#retorno deve ser sempre na estrutura de chave e valor, por esse motivo não aceita uma lista, set, etc
		return {"message": "User created successfully!"}, 201 #created

		#faixa 100 - antes de alcançar o servidor
		#faixa 200 - alcançou o servidor e foi "aceito"
		#faixa 300 - erro do endereçamento
		#faixa 400 - erro de solicitação, dados incorretos, não autorizado
		#faixa 500 - Erro do servidor (delisgado, endpoint quebrado (bad gateway), timeout)

class UserLogin(Resource):

	@classmethod
	def post(cls):
		dados = atributos.parse_args()

		user = UserModel.find_by_login(dados['login'])

		if user and safe_str_cmp(user.senha, dados['senha']): #biblioteca werkzeug.security que compara dados independente dos seus tipos
			token_de_acesso = create_access_token(identity=user.user_id) #cria um token de acesso pelo id do usuário
			return {'access_token': token_de_acesso}, 200
		return {'message': 'The username or password is incorrect.'}, 401 #Unauthorized

class UserLogout(Resource):

	@jwt_required()
	def post(self):
		jwt_id = get_jwt()['jti'] #pega o ID do JWT - JWT Token Identifier
		BLACKLIST.add(jwt_id)
		return {'message': 'Logged out successfully.'}, 200