"""
This module abstracts the Database layer with a Repository pattern.
"""

import abc
from typing import Generic, TypeVar

T = TypeVar("T")


class AbstractRepository(abc.ABC, Generic[T]):
    """
    Abstract base class for repository implementations.
    """

    def __init__(self, kind: T):
        self.kind = kind

    @abc.abstractmethod
    def save(self, entity: T) -> None:
        """
        Saves an entity to the repository.

        Args:
            entity (T): The entity to save.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, entity_id: int) -> T | None:
        """
        Finds an entity by its ID.

        Args:
            entity_id (int): The unique identifier of an entity.

        Returns:
            T : An entity if exists, otherwise None.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def find_by(self, **kwargs) -> T | None:
        """
        Finds an entity by its attributes.

        Args:
            **kwargs: The attributes of an entity.

        Returns:
            T : An entity if exists, otherwise None.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def find_all(
        self,
    ) -> list[T]:
        """
        Find all entities.

        Returns:
            list[T]: A list of all entities in the database.
        """
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository, Generic[T]):
    """
    SQLAlchemy repository implementation.
    """

    def __init__(self, session, kind: T):
        self.session = session
        super().__init__(kind)

    def save(self, entity):
        self.session.add(entity)

    def find_by_id(self, entity_id) -> T:
        return self.session.query(self.kind).filter_by(id=entity_id).one()

    def find_by(self, **kwargs) -> T:
        return self.session.query(self.kind).filter_by(**kwargs).one()

    def find_all(self) -> list[T]:
        return self.session.query(self.kind).all()
