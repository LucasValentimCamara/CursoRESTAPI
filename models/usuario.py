from sql_alchemy import banco

class UserModel(banco.Model):
	__tablename__='usuarios' #nome da tabela para o SQLAlchemy

#mapeamento para o SQLAlchemy de como sontruir a tabela
	user_id = banco.Column(banco.Integer, primary_key=True) #coluna do tipo string como chave primária
	login = banco.Column(banco.String(40))
	senha = banco.Column(banco.String(40))

	def __init__(self, login, senha): #se não passar o id, como ele é primary key, ele é gerado automaticamnte
		self.login=login
		self.senha=senha

	def json(self):
		return {
			'user_id': self.user_id,
			'login': self.login
		}

	@classmethod
	def find_user(cls, user_id): #cls class 
		user=cls.query.filter_by(user_id=user_id).first() #query consulta o banco filtrando pelo id
			# SELECT * FROM hoteis WHERE hotel_id=hotel+id
		if user: #se existir
				return user
		return None

	@classmethod
	def find_by_login(cls, login): #cls class 
		user=cls.query.filter_by(login=login).first() #query consulta o banco filtrando pelo id
			# SELECT * FROM hoteis WHERE hotel_id=hotel+id
		if user: #se existir
				return user #retorna hotel
		return None

	def save_user(self):
		banco.session.add(self)
		banco.session.commit()

	def delete_user(self):
		banco.session.delete(self)
		banco.session.commit()
