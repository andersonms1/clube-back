from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

logger = logging.getLogger(__name__)


class MongoDB:
    """
    Classe de conexão com o MongoDB.
    Implementa o padrão Singleton para garantir apenas uma instância de conexão.
    """

    _instances = {}
    _client = None
    _db = None
    _config = None

    def __new__(cls, config=None):
        # Use config as key for the instance to support different environments
        config_key = id(config) if config else "default"

        if config_key not in cls._instances:
            cls._instances[config_key] = super(MongoDB, cls).__new__(cls)
            cls._instances[config_key]._config = config
            cls._instances[config_key]._connect()
        return cls._instances[config_key]

    def _connect(self):
        """Estabelece a conexão com o MongoDB"""
        try:
            if not self._config:
                from app.config import BaseConfig

                self._config = BaseConfig

            self._client = MongoClient(
                self._config.MONGODB_URI, serverSelectionTimeoutMS=5000
            )
            # Verifica se a conexão foi estabelecida
            self._client.admin.command("ismaster")
            self._db = self._client[self._config.MONGODB_DATABASE]
            logger.info(
                f"Conexão com MongoDB estabelecida com sucesso: {self._config.MONGODB_URI}"
            )
            # for collection in ['tasks', 'users']:
            #     if collection not in self._db.list_collection_names():
            #         self._db.create_collection(collection)
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
