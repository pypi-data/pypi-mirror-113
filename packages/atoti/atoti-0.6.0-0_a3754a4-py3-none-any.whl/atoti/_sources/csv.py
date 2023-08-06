from __future__ import annotations

from typing import TYPE_CHECKING, Any, Collection, Dict, Mapping, Optional

from .._path_utils import PathLike, to_absolute_path
from .._type_utils import ScenarioName
from . import DataSource

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..table import Table
    from ..type import DataType


def create_csv_params(
    *,
    path: PathLike,
    separator: Optional[str],
    encoding: str,
    process_quotes: Optional[bool],
    array_separator: Optional[str],
    pattern: Optional[str],
    date_patterns: Optional[Mapping[str, str]],
) -> Dict[str, Any]:
    """Create the CSV specific parameters."""
    return {
        "path": to_absolute_path(path),
        "separator": separator,
        "encoding": encoding,
        "processQuotes": process_quotes,
        "arraySeparator": array_separator,
        "globPattern": pattern,
        "datePatterns": date_patterns,
    }


class CsvDataSource(DataSource):
    """CSV data source."""

    def __init__(self, java_api: JavaApi):
        """Init."""
        super().__init__(java_api, "CSV")

    def create_table_from_csv(
        self,
        path: PathLike,
        table_name: str,
        *,
        keys: Optional[Collection[str]],
        separator: Optional[str],
        encoding: str,
        process_quotes: Optional[bool],
        partitioning: Optional[str],
        types: Optional[Mapping[str, DataType]],
        array_separator: Optional[str],
        pattern: Optional[str],
        hierarchized_columns: Optional[Collection[str]],
        date_patterns: Optional[Mapping[str, str]],
        is_parameter_table: Optional[bool],
    ):
        """Create a Java table from a CSV file or directory."""
        source_params = create_csv_params(
            path=path,
            separator=separator,
            encoding=encoding,
            process_quotes=process_quotes,
            array_separator=array_separator,
            pattern=pattern,
            date_patterns=date_patterns,
        )
        self.create_table_from_source(
            table_name,
            keys=keys,
            partitioning=partitioning,
            types=types,
            source_params=source_params,
            hierarchized_columns=hierarchized_columns,
            is_parameter_table=is_parameter_table,
        )

    def load_csv_into_table(
        self,
        path: PathLike,
        table: Table,
        *,
        scenario_name: ScenarioName,
        separator: Optional[str],
        encoding: str,
        process_quotes: bool,
        array_separator: Optional[str],
        pattern: Optional[str],
        date_patterns: Optional[Mapping[str, str]],
    ):
        """Load a csv into an existing table."""
        source_params = create_csv_params(
            path=path,
            separator=separator,
            encoding=encoding,
            process_quotes=process_quotes,
            array_separator=array_separator,
            pattern=pattern,
            date_patterns=date_patterns,
        )
        self.load_data_into_table(
            table.name,
            scenario_name=scenario_name,
            source_params=source_params,
        )
