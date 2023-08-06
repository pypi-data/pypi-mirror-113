from __future__ import annotations

from typing import TYPE_CHECKING, Collection, Mapping, Optional

from atoti.type import DataType

from .._path_utils import PathLike, to_absolute_path
from .._type_utils import ScenarioName
from . import DataSource

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..table import Table


class ParquetDataSource(DataSource):
    """Parquet data source."""

    def __init__(self, java_api: JavaApi):
        """Init."""
        super().__init__(java_api, "PARQUET")

    def create_table_from_parquet(
        self,
        *,
        path: PathLike,
        table_name: str,
        keys: Optional[Collection[str]],
        partitioning: Optional[str],
        pattern: Optional[str],
        hierarchized_columns: Optional[Collection[str]],
        is_parameter_table: Optional[bool],
        _parquet_column_name_to_table_column_name: Optional[Mapping[str, str]],
        _types: Optional[Mapping[str, DataType]],
    ):
        """Create a table from a Parquet file."""
        self.create_table_from_source(
            table_name,
            keys=keys,
            partitioning=partitioning,
            types=_types,
            source_params={
                "path": to_absolute_path(path),
                "globPattern": pattern,
                "parquetColumnNamesToStoreFieldNamesMapping": _parquet_column_name_to_table_column_name,
            },
            hierarchized_columns=hierarchized_columns,
            is_parameter_table=is_parameter_table,
        )

    def load_parquet_into_table(
        self,
        *,
        path: PathLike,
        table: Table,
        scenario_name: ScenarioName,
        pattern: Optional[str] = None,
        _parquet_column_name_to_table_column_name: Optional[Mapping[str, str]] = None,
    ):
        """Load a Parquet into an existing table."""
        self.load_data_into_table(
            table.name,
            scenario_name=scenario_name,
            source_params={
                "path": to_absolute_path(path),
                "globPattern": pattern,
                "parquetColumnNamesToStoreFieldNamesMapping": _parquet_column_name_to_table_column_name,
            },
        )
