from app.lib.database.mongodb import MongoDB


def init_mongodb(config):
    """
    Initialize MongoDB connection with the specified configuration

    Args:
        config: Configuration object with MongoDB settings

    Returns:
        MongoDB instance
    """
    mongodb = MongoDB(config)
    return mongodb
