"""Unit of Work

The Unit of Work (UoW) pattern is our abstraction over the idea of atomic operations. It will allow
us to finally and fully decouple our service layer from the data layer.

"""
import abc

from sqlalchemy.orm import Session

from allocation.adapters.database import get_session_factory
from allocation.adapters.repository import AbstractRepository, SqlAlchemyRepository
from allocation.domain.models import Batch


class AbstractUnitOfWork(abc.ABC):
    """Abstract Unit of Work"""

    batches: AbstractRepository

    def __exit__(self, *args):
        self.rollback()

    def __enter__(self):
        return self

    @abc.abstractmethod
    def commit(self):
        """Commits the changes to the database."""
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        """Rolls back the changes to the database."""
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """SQLAlchemy Unit of Work Implementation"""

    def __init__(self, session_factory=get_session_factory):
        self.session_factory = session_factory
        self.session: Session | None = None

    def __enter__(self):
        self.session = self.session_factory()
        self.batches = SqlAlchemyRepository(session=self.session, kind=Batch)
        return self

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()
