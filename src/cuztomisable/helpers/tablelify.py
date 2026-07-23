from typing import Optional, Sequence, Union

from sqlalchemy.orm import Query, Session

from cuztomisable.schemas.tablelify import TablelifyParams, TablelifyResponse
from cuztomisable.settings import settings


class Tablelify:
    @staticmethod
    def run(
        db: Session,
        query: Query,
        params: TablelifyParams,
        search_columns: Optional[list[str]] = None,
    ) -> TablelifyResponse:
        pass

    @staticmethod
    def create(
        query: Query,
        params: TablelifyParams,
        search_columns: Optional[list[str]] = None,
        allowed_filters: Optional[list[str]] = None,
    ) -> tuple[int, int, Query]:
        pass

    @staticmethod
    def sort(
        query: Query,
        columns,
        direction: Optional[str] = None,
        allowed_columns: Optional[list[str]] = None,
        default_columns: Optional[dict] = None,
    ) -> Query:
        pass

    @staticmethod
    def execute(
        query: Query,
        size: Union[int, str],
        page: int,
    ) -> tuple[Sequence, Optional[int], int]:
        pass

    @staticmethod
    def response(
        data: Sequence,
        size: Union[int, str],
        page: int,
        search: Optional[str],
        total: int,
        filtered_total: int = 0,
    ) -> TablelifyResponse:
        pass

    @staticmethod
    def clean_parameters(params: TablelifyParams) -> TablelifyParams:
        params = TablelifyParams(**params.model_dump())
        max_size = settings("tablelify.max_size", 100)
        size = params.size
        if isinstance(size, str) and size != "all":
            try:
                size = int(size)
            except ValueError:
                size = settings("tablelify.default.size", 10)
        # Prevents the size from being to large or small
        if size == "all" or size > max_size:
            size = max_size
        elif size < 5:
            size = 5
        params.size = size
        # Prevents the page from being used with a value less than 1
        if not params.page or params.page < 1:
            params.page = 1
        # Normalizes the asc/desc direction
        direction = params.direction.lower() if params.direction else None
        params.direction = direction if direction in ("asc", "desc") else "asc"
        # Cleans the search for LIKE query
        search = params.search.strip() if params.search else None
        search = search.strip("%") if search else None
        search = "%" + search + "%" if search else None
        params.search = search
        return params

    @staticmethod
    def clean_request(data: dict) -> dict:
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = Tablelify.clean_request(value)
            elif isinstance(value, list):
                data[key] = [Tablelify.clean_request(item) if isinstance(item, dict) else item for item in value]
            else:
                if isinstance(value, str):
                    value = value.strip()
                is_null_string = isinstance(value, str) and value.lower() in ("null", "none")
                if not value or is_null_string:
                    # Normalizes the null values to None for easier handling in the backend
                    value = None
                elif key != "search":
                    # Cleans the booleans to prevent issues with 1/0, true/false, True/False, etc.
                    if value in ("true", "True", "1", 1, True):
                        value = True
                    elif value in ("false", "False", "0", 0, False):
                        value = False
                data[key] = value
        return data
