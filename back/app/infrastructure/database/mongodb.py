from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
from app.config import BaseConfig as Config

logger = logging.getLogger(__name__)

class MongoDB:
    """
    Classe de conexão com o MongoDB.
    Implementa o padrão Singleton para garantir apenas uma instância de conexão.
    """
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        """Estabelece a conexão com o MongoDB"""
        try:
            self._client = MongoClient(Config.MONGODB_URI, serverSelectionTimeoutMS=5000)
            # Verifica se a conexão foi estabelecida
            self._client.admin.command('ismaster')
            self._db = self._client[Config.MONGODB_DATABASE]
            logger.info(f"Conexão com MongoDB estabelecida com sucesso: {Config.MONGODB_URI}")
        except ConnectionFailure as e:
            logger.error(f"Falha ao conectar ao MongoDB: {str(e)}")
            raise

    def get_database(self):
        """Retorna a instância do banco de dados"""
        if self._db is None:
            self._connect()
        return self._db

    def get_collection(self, collection_name):
        """Retorna uma coleção específica do banco de dados"""
        return self.get_database()[collection_name]

    def close_connection(self):
        """Fecha a conexão com o MongoDB"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("Conexão com MongoDB encerrada")

    def __del__(self):
        """Garante que a conexão seja fechada quando o objeto for destruído"""
        self.close_connection()