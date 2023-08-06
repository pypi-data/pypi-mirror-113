from __future__ import annotations

from dataclasses import dataclass, field
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Mapping

from typeguard import typechecked, typeguard_ignore

from ._base._base_hierarchy import BaseHierarchy
from .level import Level

if TYPE_CHECKING:
    from ._java_api import JavaApi
    from ._local_cube import LocalCube
    from .hierarchies import Hierarchies
    from .levels import Levels
    from .measures import Measures


def _refresh_decorator(func: Callable[..., Any]) -> Callable:
    @wraps(func)
    def func_wrapper(self: Hierarchy, *args: Any, **kwargs: Any) -> Any:
        func(self, *args, **kwargs)
        self._java_api.refresh()

    return func_wrapper


@typeguard_ignore
@dataclass(eq=False)
class Hierarchy(BaseHierarchy[Mapping[str, Level]]):
    """Hierarchy of a :class:`~atoti.cube.Cube`.

    A hierarchy is a sub category of a :attr:`~dimension` and represents a precise type of data.

    For example, :guilabel:`Quarter` or :guilabel:`Week` could be hierarchies in the :guilabel:`Time` dimension.
    """

    _name: str
    _levels: Mapping[str, Level]
    _dimension: str
    _slicing: bool
    _cube: LocalCube[Hierarchies, Levels, Measures] = field(repr=False)
    _java_api: JavaApi = field(repr=False)
    _visible: bool

    @property
    def levels(self) -> Mapping[str, Level]:
        return self._levels

    @property
    def dimension(self) -> str:
        return self._dimension

    @property
    def slicing(self) -> bool:
        return self._slicing

    @property
    def name(self) -> str:
        return self._name

    @property
    def visible(self) -> bool:
        """Whether the hierarchy is visible or not."""
        return self._visible

    @levels.setter
    @_refresh_decorator
    @typechecked
    def levels(self, value: Mapping[str, Level]):
        """Levels setter."""
        self._levels = value
        self._java_api.create_or_update_hierarchy(
            self._name,
            cube=self._cube,
            dimension=self._dimension,
            levels=self._levels,
        )

    @dimension.setter
    @_refresh_decorator
    @typechecked
    def dimension(self, value: str):
        """Dimension setter."""
        self._java_api.update_hierarchy_coordinate(
            cube=self._cube, hierarchy=self, new_dim=value, new_hier=self._name
        )
        self._dimension = value

    @slicing.setter
    @_refresh_decorator
    @typechecked
    def slicing(self, value: bool):
        """Slicing setter."""
        self._java_api.update_hierarchy_slicing(self, value)
        self._slicing = value

    @visible.setter
    @_refresh_decorator
    @typechecked
    def visible(self, value: bool):
        """Visibility setter."""
        self._java_api.set_hierarchy_visibility(
            cube=self._cube, dimension=self._dimension, name=self._name, visible=value
        )
        self._visible = value
