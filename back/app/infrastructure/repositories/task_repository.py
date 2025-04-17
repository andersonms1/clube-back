import logging
from datetime import datetime
from app.infrastructure.database.mongodb import MongoDB
from app.domain.models.task import Task
import json
logger = logging.getLogger(__name__)

class TaskRepository:
    """
    Classe responsável por gerenciar operações de banco de dados relacionadas a tarefas.
    """
    
    def __init__(self):
        """Inicializa o repositório com a coleção de tarefas do MongoDB"""
        self.db = MongoDB()
        self.collection = self.db.get_collection('tasks')
        
        
    def find_all(self):
        """
        Busca uma tarefa pelo ID
        
        Args:
            task_id (str): ID da tarefa
            
        Returns:
            Task: Objeto de tarefa ou None se não encontrado
        """
        try:
            task_data = self.collection.find_one({})
            if task_data:
                return json.dumps( [Task.from_dict(task) for task in task_data])
                
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar tarefa por ID: {str(e)}")
            return None
            
 