from abc import ABC

from core.config import settings
from database.db import Database


class ServiceBase(ABC):

    _db = Database(settings.db_conn_link)
