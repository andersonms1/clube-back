from app.lib.database.mongodb import MongoDB
import logging
from app.config import config_by_name

logger = logging.getLogger(__name__)


def init_mongodb(app):
    """
    Inicializa a conexão com o MongoDB

    Args:
        app: Instância da aplicação Flask
    """
    try:
        logger.info("Inicializando conexão com MongoDB...")
        # Get the current configuration
        config_name = app.config.get("ENV", "development")
        configuration = config_by_name.get(config_name)

        # Initialize MongoDB with the correct configuration
        mongodb = MongoDB(configuration)

        # Testa a conexão com o banco de dados
        db = mongodb.get_database()
        app.mongodb = mongodb

        logger.info(f"MongoDB inicializado com sucesso. Banco de dados: {db.name}")
        return mongodb
    except Exception as e:
        logger.error(f"Erro ao inicializar MongoDB: {str(e)}")
        # Em produção, pode ser desejável tratar isso como um erro fatal
        if app.config.get("FLASK_ENV") == "production":
            raise
