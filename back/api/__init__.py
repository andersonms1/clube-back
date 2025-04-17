# from flask import Flask
# from flask_restful import Api
# from api.tasks import views as tasks_routes
# from pymongo.collection import Collection, ReturnDocument

# import os
# from dotenv import load_dotenv

# load_dotenv() 

# import logging
# logger = logging.getLogger(__name__)

# def create_app(config_name="development"):
#     app = Flask(__name__)
#     api = Api(app)
#     tasks_routes.init_routes(api)


#     return app


# def _init_mongodb(app):
#     """
#     Inicializa a conexão com o MongoDB
    
#     Args:
#         app: Instância da aplicação Flask
#     """
#     try:
#         logger.info("Inicializando conexão com MongoDB...")
#         # mongodb = MongoDB()
#         mongodb = "MongoDB()"
        
#         # Testa a conexão com o banco de dados
#         db = mongodb.get_database()
#         app.mongodb = mongodb
        
#         logger.info(f"MongoDB inicializado com sucesso. Banco de dados: {db.name}")
#     except Exception as e:
#         logger.error(f"Erro ao inicializar MongoDB: {str(e)}")
#         # Em produção, pode ser desejável tratar isso como um erro fatal
#         if app.config.get('FLASK_ENV') == 'production':
#             raise