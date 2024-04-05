#quando se importa a biblioteca inteira ela estará inteira em memória, para um código grande pode fazer diferença
#o ultimo nome que vai ser chamado diretamente evita ter que usar datetime.datetime

from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from resources.site import Site, Sites
from flask_jwt_extended import JWTManager
from flask_jwt_extended.config import config
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db' #cria na raiz uma banco sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #rastrio de modificações pelo flask alchemy que dá avisos 
api = Api(app)
app.config["JWT_SECRET_KEY"] = "secret_key" 
#app.config["JWT_ALGORITHM"]="HS256"
jwt = JWTManager(app)
app.config['JWT_BLACKLIST_ENABLED'] = True


@app.before_first_request #verifica antes da primeira requisição se há um banco
def cria_banco(): #se não houver ele é criado
	banco.create_all() #cria automaticamente todos os bancos e tabela

@jwt.token_in_blocklist_loader #verificar se um token está ou não na blacklist
def verifica_blacklist(self,token):
	return token['jti'] in BLACKLIST

@jwt.revoked_token_loader #acesso invalidado
def token_de_acesso_invalidado(jwt_header,jwt_payload):
	return jsonify({'message': 'You have been logged out'}), 401 #a função permite converter um dicionáio para json

#endpoints
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')

if __name__ == '__main__':
	from sql_alchemy import banco
	banco.init_app(app) #importação dentro do if para ele ser executado somente se for chamado desse arquivo
	app.run(debug=True)

# .\ambvir\Scripts\activate.bat
#(ambvir) C:\Users\Extra\Desktop\Kogui\Caderno\Curso - REST API and Flask>python app.py
# * Serving Flask app 'app' (lazy loading)
# * Environment: production
#   WARNING: This is a development server. Do not use it in a production deployment.
#   Use a production WSGI server instead.
# * Debug mode: on
# * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
# * Restarting with stat
# * Debugger is active!
# * Debugger PIN: 553-395-616