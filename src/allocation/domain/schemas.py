"""
This module contains the schemas used for request/response validation in the allocation service.
"""
from datetime import date
from re import sub

from pydantic import BaseConfig, BaseModel, Field, validator


def to_camel(s: str) -> str:
    """
    Translates a string to camel case.

    Args:
        s (str): The string to translate.
    """
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


class CamelCaseModel(BaseModel):
    """
    A base which attributes can be translated to camel case.
    """

    class Config(BaseConfig):
        alias_generator = to_camel
        allow_population_by_field_name = True


class OrderLine(CamelCaseModel):
    """
    Represents an item in an order.
    """

    order_id: str
    sku: str
    qty: int

    @validator("qty")
    def qty_greater_than_zero(cls, v):
        """
        Validates that the quantity is greater than zero.

        Args:
            v: The quantity to validate.

        Returns:
            bool: True if the quantity is greater than zero.
        """
        if v <= 0:
            raise ValueError("Quantity must be greater than zero.")

        return v


class BatchIn(CamelCaseModel):
    """
    Represents a batch of items.
    """

    ref: str = Field(title="Reference", description="A batch reference.")
    sku: str = Field(title="SKU", description="A Stock Keeping Unit.")
    qty: int = Field(title="Quantity", description="The quantity of items in the batch.")
    eta: date | None = Field(title="ETA", description="The estimated time of arrival.")

    @validator("qty")
    def qty_greater_than_zero(cls, v):
        """
        Validates that the quantity is greater than zero.

        Args:
            v: The quantity to validate.

        Returns:
            bool: True if the quantity is greater than zero.
        """
        if v <= 0:
            raise ValueError("Quantity must be greater than zero.")

        return v
