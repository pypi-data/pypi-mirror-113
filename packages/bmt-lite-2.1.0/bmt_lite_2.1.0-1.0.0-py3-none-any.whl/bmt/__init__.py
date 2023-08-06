"""BMT basics."""
from functools import wraps
from typing import Callable, List, Optional, TypeVar, Union

from .data import (
    all_classes, all_elements, all_slots,
    all_types, ancestors, descendants, children, parent, element,
)
from .util import pascal_to_snake, snake_to_pascal


def normalize(s: str) -> str:
    """Normalize string input."""
    if s.startswith("biolink:"):
        s = s[8:]
    if "_" in s:
        # it's snake case
        return s.replace("_", " ")
    if " " in s:
        return s
    return pascal_to_snake(s, " ")


T = TypeVar("T")


def listify(func: Callable) -> Callable:
    """Expand function to take list of arguments."""
    @wraps(func)
    def wrapper(arg: Union[T, List[T]], **kwargs) -> Union[T, List[T]]:
        """Apply function to each element in list."""
        if isinstance(arg, list):
            return [
                func(el, **kwargs)
                for el in arg
            ]
        else:
            return func(arg, **kwargs)
    return wrapper


@listify
def format(s: str, case: Optional[str] = None, **kwargs) -> str:
    """Format space-case string as biolink CURIE."""
    if isinstance(case, str) and case.lower() == "pascal":
            return "biolink:" + snake_to_pascal(s, " ")
    elif isinstance(case, str) and case.lower() == "snake":
            return "biolink:" + s.replace(" ", "_")
    else:
        return "biolink:" + s


def robustify():
    """Add format conversions to method."""
    def decorator(func: Callable) -> Callable:
        """Generate decorator."""
        @wraps(func)
        def wrapper(self: "Toolkit", s: str, *args, formatted=False, **kwargs):
            """Wrap in format conversions."""
            normalized = normalize(s)
            output: Union[str, List[str]] = func(self, normalized, *args, **kwargs)
            if formatted:
                if normalized in all_classes:
                    output = format(output, case="pascal")
                elif normalized in all_slots:
                    output = format(output, case="snake")
                else:
                    output = format(output)
            return output
        return wrapper
    return decorator


class Toolkit():
    """Biolink model toolkit - lite!"""

    def __init__(self, schema=None):
        """Initialize."""
        if schema is not None:
            raise ValueError("bmt-lite does not support the `schema` argument. The biolink model version is dictated by the library flavor you installed.")

    def get_all_classes(self):
        """Get all classes."""
        return all_classes

    def get_all_slots(self):
        """Get all slots."""
        return all_slots

    def get_all_types(self):
        """Get all types."""
        return all_types

    def get_all_elements(self):
        """Get all elements."""
        return all_elements

    @robustify()
    def get_ancestors(
        self,
        name: str,
        reflexive: bool = True,
    ):
        """Get ancestors."""
        if name not in ancestors:
            return []
        if reflexive:
            return ancestors[name] + [name]
        else:
            return ancestors[name]

    @robustify()
    def get_descendants(
        self,
        name: str,
        reflexive: bool = True,
    ):
        """Get descendants."""
        if name not in descendants:
            return []
        if reflexive:
            return descendants[name] + [name]
        else:
            return descendants[name]

    @robustify()
    def get_children(
        self,
        name: str,
    ):
        """Get children."""
        return children.get(name, [])

    @robustify()
    def get_parent(
        self,
        name: str,
    ):
        """Get parent."""
        return parent.get(name, None)

    @robustify()
    def get_element(
        self,
        name: str,
    ):
        """Get element."""
        if name in all_classes:
            return ClassDefinition(name, **element.get(name, dict()))
        elif name in all_slots:
            return SlotDefinition(name, **element.get(name, dict()))
        return None
        # raise ValueError(f"Unrecognized element: {name}")


class Element():
    """Biolink model element."""

    def __init__(self, name: str):
        """Initialize."""
        self.name: str = name


class SlotDefinition(Element):
    """Slot definition."""

    def __init__(
        self,
        name: str,
        symmetric: bool = False,
        inverse: Optional[str] = None,
    ):
        """Initialize."""
        super().__init__(name)
        self.symmetric: bool = symmetric
        self.inverse: Optional[str] = inverse


class ClassDefinition(Element):
    """Class definition."""

    def __init__(
        self,
        name: str,
        id_prefixes: List[str],
    ):
        """Initialize."""
        super().__init__(name)
        self.id_prefixes: List[str] = id_prefixes
