from sql_alchemy import banco

class SiteModel(banco.Model):
	__tablename__='sites' #nome da tabela para o SQLAlchemy

#mapeamento para o SQLAlchemy de como construir a tabela
	site_id = banco.Column(banco.Integer, primary_key=True) #coluna do tipo string como chave primária
	url = banco.Column(banco.String(80))

	#relacionamento entre os BDs
	hoteis = banco.relationship('HotelModel') #a classe SiteModel tem relação com a classe HotelModel, ao verificar a chave Estrangeira, ele automaticamente sabera que a relação é de um site para muitos hoteis
		#-> lista de objetos hoteis
	def __init__(self, url):
		self.url=url
		
	def json(self):
		return {
			'site_id': self.site_id,
			'url': self.url,
			'hoteis': [hotel.json() for hotel in self.hoteis], #list comprehension
			}

#list comprehension: maneira de contruir listas no python 

	@classmethod
	def find_site(cls, url): #cls class 
		site=cls.query.filter_by(url=url).first() #query consulta o banco filtrando pelo id
			# SELECT * FROM hoteis WHERE hotel_id=hotel+id
		if site: #se existir
				return site #retorna hotel
		return None

	@classmethod
	def find_by_id(cls, site_id): #cls class 
		site=cls.query.filter_by(site_id=site_id).first() #query consulta o banco filtrando pelo id
			# SELECT * FROM hoteis WHERE hotel_id=hotel+id
		if site: #se existir
				return site #retorna hotel
		return None


	def save_site(self):
		banco.session.add(self)
		banco.session.commit()


	def delete_site(self):
		#deletenado todos hoteis associados ao site
		[hotel.delete_hotel() for hotel in self.hoteis] 

		#deletendo o site
		banco.session.delete(self)
		banco.session.commit()