from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from resources.filtros import normalize_path_params, consulta_sem_cidade, consulta_com_cidade
from flask_jwt_extended import jwt_required
import sqlite3



#path /hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400 
path_params = reqparse.RequestParser() #instanciando um objeto da classe parse
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset_max', type=float)

class Hoteis(Resource): #todo recurso tem GET,POST,PUT,DELETE
	#hotel é um recurso da API
	def get (self):
		connection = sqlite3.connect('banco.db')
		cursor = connection.cursor()
		#(valor,) para delcarar valor unico em um tupla

		dados = path_params.parse_args()
		dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
		parametros = normalize_path_params(**dados_validos) #sem parametros, retornara com os filtros "abertos"
		
		if parametros.get('cidade'): #no if não tem problema se o ir der None. Mas para evitar problemas é possível usar parametros.get('cidade')
			tupla = tuple([parametros[chave] for chave in parametros])
			#dicionário que para cada chave recebe um valor para formar uma tupla na ordem que foi passada
			resultado = cursor.execute(consulta_sem_cidade, tupla) #não precisa colocar parenteses pq é uma variável que contem um tupla dentro
		else:
			tupla = tuple([parametros[chave] for chave in parametros])
			resultado = cursor.execute(consulta_com_cidade, tupla)

		hoteis = []
		for linha in resultado:
			hoteis.append({
				'hotel_id': linha[0],
				'nome': linha[1],
				'estrelas': linha[2],
				'diaria': linha[3],
				'cidade': linha[4],
				'site_id': linha[5]
				})

		return {'hoteis': hoteis}

		#tranforma objeto em json cada hotel dentro do query.all que retorna todo elementos dentro
		#=SELECT * FROM HOTEIS
		#return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} #dicionário, porem na requisição é convertido para JSON pela biblioteca

class Hotel(Resource):
	#referenciados na classe para não ser necessários colocar em cada def
	argumentos = reqparse.RequestParser() #Os arugumentos serão uma instancia de requestparser
	argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
	argumentos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank")
	argumentos.add_argument('diaria')
	argumentos.add_argument('cidade')
	argumentos.add_argument('site_id', type=int, required=True, help="Every hotel needs to be link with a site")
		
	def get (self, hotel_id):
		hotel = HotelModel.find_hotel(hotel_id)
		if hotel:
			return hotel.json() #hotel objeto
		return {'message': 'Hotel not found.'}, 404 #not found

	@jwt_required() #decorador para solicitar login com token de acesso
	def post (self, hotel_id):
		if HotelModel.find_hotel(hotel_id):
			return {"message": "Hotel id '{}' already exists". format(hotel_id)}, 400 #bad request

		dados=Hotel.argumentos.parse_args()
		hotel=HotelModel(hotel_id, **dados) #objeto

		#novo_hotel=hotel_objeto.json() #-> não é possível adicionar um objeto na lista de dicionarios, por isso json é usado para converter e adicionar na lista
		#hoteis.append(novo_hotel)
		#return novo_hotel, 201
			#-> Código que foi sobrescrito após adição do banco de dados em SQLAlchemy
		if not SiteModel.find_by_id(dados.get('site_id')):
			return {'message': 'Hotel must be associated to a valid site id'}, 400

		try:
			hotel.save_hotel()
			print("salvo")
		except:
			return {'message': 'An internal error ocurred trying to save hotel'}, 500 #internal server error
		return hotel.json()

	@jwt_required()
	def put (self, hotel_id): #se passar um id que existe ele altera todo o corpo, se não existir ele cria um novo	
		dados=Hotel.argumentos.parse_args() #colhe os dados
		hotel_encontrado = HotelModel.find_hotel(hotel_id)
		if hotel_encontrado: #se o hotel existe
			hotel_encontrado.update_hotel(**dados) #atualiza os dados
			hotel_encontrado.save_hotel() #salva ele no banco
			return hotel_encontrado.json(), 200 #OK retorna os dados

		hotel=HotelModel(hotel_id, **dados) #kwargs desempacota todos os dados, sendo que os dados estão definidos em chave e valor para cada dado inserido. Assim, caso seja dado um novo argumento ele entendera (restrito aos argumentos definidos na classe)	
		try:
			hotel.save_hotel()
		except:
			return {'message': 'An internal error ocurred trying to save hotel'}, 500 #internal server error
		return hotel.json(), 201 #CREATED

	@jwt_required()
	def delete (self, hotel_id):
		#linhas que deixaram de existir pela criação do BD e Models
		#global hoteis #se referenciando a variável lista de hoteis que já existe
			#Sem chamar global: UnboundLocalError: local variable 'hoteis' referenced before assigment
		#hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
			#pegando todos hoteis que não tem o id igual o id passado, criando uma nova lista e substituindo a original
		hotel=HotelModel.find_hotel(hotel_id)
		if hotel:
			try:
				hotel.delete_hotel()
			except:
				return {'message': 'An error ocurred trying to delete hotel'}, 500 #internal server error
			return {'message': 'Hotel deleted'}
		return {'message': 'Hotel not found.'}, 404 #not found