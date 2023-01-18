"""
This module contains the schemas used for request/response validation in the allocation service.
"""
from datetime import date
from re import sub

from pydantic import BaseConfig, BaseModel, Field


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

    order_id: str = Field(title="Order ID", description="The order unique identifier")
    sku: str = Field(title="SKU", description="The stock keeping unit")
    qty: int = Field(title="Quantity", description="The quantity of the item", gt=0)


class BatchIn(CamelCaseModel):
    """
    Represents a batch of items.
    """

    ref: str = Field(title="Reference", description="A batch reference.")
    sku: str = Field(title="SKU", description="A Stock Keeping Unit.")
    qty: int = Field(title="Quantity", description="The quantity of items in the batch.", gt=0)
    eta: date | None = Field(title="ETA", description="The estimated time of arrival.")
