from typing import Any, Optional, Union

from pydantic import BaseModel


class TablelifyFilter(BaseModel):
    key: str
    value: Any = None


class TablelifyParams(BaseModel):
    page: int = 1
    size: Union[int, str] = 10
    column: Optional[Union[str, list]] = None
    direction: Optional[str] = None
    search: Optional[str] = None
    filters: list[TablelifyFilter] = []
    allowed_filters: Optional[list[str]] = None
    search_columns: Optional[list[str]] = None
    additional: Optional[dict] = None


class TablelifyResponse(BaseModel):
    page: int
    total_pages: int
    size: Union[int, str]
    total: int
    data: list
    next_page: Optional[int] = None
    previous_page: Optional[int] = None
    filtered: Optional[bool] = None
    filtered_total: Optional[int] = None
