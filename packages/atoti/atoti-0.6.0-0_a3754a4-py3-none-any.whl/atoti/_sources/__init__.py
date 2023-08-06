from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, Collection, Mapping, Optional

from .._type_utils import ScenarioName

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..type import DataType


class DataSource(ABC):
    """Abstract data source."""

    def __init__(self, java_api: JavaApi, source_key: str):
        """Initialise the source.

        Args:
            java_api: The Java API of the session.
            source_key: The key of the source.
        """
        self._java_api = java_api
        self.source_key = source_key

    def create_table_from_source(
        self,
        table_name: str,
        *,
        keys: Optional[Collection[str]],
        partitioning: Optional[str],
        types: Optional[Mapping[str, DataType]],
        source_params: Mapping[str, Any],
        hierarchized_columns: Optional[Collection[str]],
        is_parameter_table: Optional[bool] = False,
    ):
        """Create a table with the given source.

        Args:
            table_name: The name to give to the table.
            keys:  The key columns for the table.
            partitioning: The partitioning description.
            types: Manually specified types.
            source_params: The parameters specific to the source.
            hierarchized_columns: The columns to convert into hierarchies
        """
        self._java_api.create_table_from_source(
            table_name,
            source_key=self.source_key,
            keys=keys,
            partitioning=partitioning,
            types=types,
            source_params=source_params,
            hierarchized_columns=hierarchized_columns,
            is_parameter_table=is_parameter_table,
        )

    def load_data_into_table(
        self,
        table_name: str,
        *,
        scenario_name: Optional[ScenarioName],
        source_params: Mapping[str, Any],
    ):
        """Load the data into an existing table with a given source.

        Args:
            table_name: The name of the table to feed.
            scenario_name: The name of the scenario to feed.
            source_params: The parameters specific to the source.
        """
        self._java_api.load_data_into_table(
            table_name=table_name,
            source_key=self.source_key,
            scenario_name=scenario_name,
            source_params=source_params,
        )
