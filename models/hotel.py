from sql_alchemy import banco

class HotelModel(banco.Model):
	__tablename__='hoteis' #nome da tabela para o SQLAlchemy

#mapeamento para o SQLAlchemy de como sontruir a tabela
	hotel_id = banco.Column(banco.String, primary_key=True) #coluna do tipo string como chave primária
	nome = banco.Column(banco.String(80))
	estrelas = banco.Column(banco.Float(1)) #uma casa depois da vírgula
	diaria = banco.Column(banco.Float(2))
	cidade = banco.Column(banco.String(40))
	site_id = banco.Column(banco.Integer, banco.ForeignKey('sites.site_id')) #coluna do tipo inteiro como chave estrangeira, está linkando esse bd ao outro bd que armazenará URLs

	def __init__(self, hotel_id, nome, estrelas, diaria, cidade, site_id):
		self.hotel_id=hotel_id
		self.nome=nome
		self.estrelas=estrelas
		self.diaria=diaria
		self.cidade=cidade
		self.site_id=site_id

	def json(self):
		return {
			'hotel_id': self.hotel_id,
			'nome': self.nome,
			'estrelas': self.estrelas,
			'diaria': self.diaria,
			'cidade': self.cidade,
			'site_id': self.site_id
		}

	@classmethod
	def find_hotel(cls, hotel_id): #cls class 
		hotel=cls.query.filter_by(hotel_id=hotel_id).first() #query consulta o banco filtrando pelo id
			# SELECT * FROM hoteis WHERE hotel_id=hotel+id
		if hotel: #se existir
				return hotel #retorna hotel
		return None

	def save_hotel(self):
		banco.session.add(self)
		banco.session.commit()

	def update_hotel(self, nome, estrelas, diaria, cidade): #substitui os dados com base na variável colocada, self.var pega a variavel escria e coloca na var que está no dicionário
		self.nome=nome
		self.estrelas=estrelas
		self.diaria=diaria
		self.cidade=cidade

	def delete_hotel(self):
		banco.session.delete(self)
		banco.session.commit()