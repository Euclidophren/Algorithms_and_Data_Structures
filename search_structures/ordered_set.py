import itertools as it
from typing import (
    Any,
    Iterable,
    Iterator,
    List,
    MutableSet,
    Optional,
    Sequence,
    Set,
    TypeVar,
    Union,
    overload,
)

SLICE_ALL = slice(None)


T = TypeVar("T")


def _is_atomic(obj: Any) -> bool:
    return isinstance(obj, str) or isinstance(obj, tuple)


class OrderedSet(MutableSet[T], Sequence[T]):
    def __init__(self, iterable: Optional[Iterable[T]] = None):
        self.items = []
        self.map = {}
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.items)

    @overload
    def __getitem__(self, index: Sequence[int]) -> List[T]:
        ...

    @overload
    def __getitem__(self, index: slice) -> "OrderedSet[T]":
        ...

    def __getitem__(self, index: int) -> T:
        if isinstance(index, slice) and index == SLICE_ALL:
            return self.copy()
        elif isinstance(index, Iterable):
            return [self.items[i] for i in index]
        elif isinstance(index, slice) or hasattr(index, "__index__"):
            result = self.items[index]
            if isinstance(result, list):
                return self.__class__(result)
            else:
                return result
        else:
            raise TypeError("Don't know how to index an OrderedSet by %r" % index)

    def copy(self) -> "OrderedSet[T]":
        return self.__class__(self)

    def __getstate__(self):
        if len(self) == 0:
            return (None,)
        else:
            return list(self)

    def __setstate__(self, state):
        if state == (None,):
            self.__init__([])
        else:
            self.__init__(state)

    def __contains__(self, key: Any) -> bool:

        return key in self.map

    def add(self, key: T) -> int:
        if key not in self.map:
            self.map[key] = len(self.items)
            self.items.append(key)
        return self.map[key]

    append = add

    def update(self, sequence: Union[Sequence[T], Set[T]]) -> int:
        item_index = 0
        try:
            for item in sequence:
                item_index = self.add(item)
        except TypeError:
            raise ValueError(
                "Argument needs to be an iterable, got %s" % type(sequence)
            )
        return item_index

    @overload
    def index(self, key: T) -> int:
        ...

    def index(self, key: Sequence[T]) -> List[int]:
        if isinstance(key, Iterable) and not _is_atomic(key):
            return [self.index(subkey) for subkey in key]
        return self.map[key]

    get_loc = index
    get_indexer = index

    def pop(self) -> T:
        if not self.items:
            raise KeyError("Set is empty")

        elem = self.items[-1]
        del self.items[-1]
        del self.map[elem]
        return elem

    def discard(self, key: T) -> None:
        if key in self:
            i = self.map[key]
            del self.items[i]
            del self.map[key]
            for k, v in self.map.items():
                if v >= i:
                    self.map[k] = v - 1

    def clear(self) -> None:
        del self.items[:]
        self.map.clear()

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def __reversed__(self) -> Iterator[T]:
        return reversed(self.items)

    def __repr__(self) -> str:
        if not self:
            return "%s()" % (self.__class__.__name__,)
        return "%s(%r)" % (self.__class__.__name__, list(self))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Sequence):
            return list(self) == list(other)
        try:
            other_as_set = set(other)
        except TypeError:
            return False
        else:
            return set(self) == other_as_set

    def union(self, *sets: Union[Sequence[T], Set[T]]) -> "OrderedSet[T]":
        cls = self.__class__ if isinstance(self, OrderedSet) else OrderedSet
        containers = map(list, it.chain([self], sets))
        items = it.chain.from_iterable(containers)
        return cls(items)

    def __and__(self, other: Union[Sequence[T], Set[T]]) -> "OrderedSet[T]":
        # the parent implementation of this is backwards
        return self.intersection(other)

    def intersection(self, *sets: Union[Sequence[T], Set[T]]) -> "OrderedSet[T]":
        cls = self.__class__ if isinstance(self, OrderedSet) else OrderedSet
        if sets:
            common = set.intersection(*map(set, sets))
            items = (item for item in self if item in common)
        else:
            items = self
        return cls(items)

    def difference(self, *sets: Union[Sequence[T], Set[T]]) -> "OrderedSet[T]":
        cls = self.__class__
        if sets:
            other = set.union(*map(set, sets))
            items = (item for item in self if item not in other)
        else:
            items = self
        return cls(items)

    def issubset(self, other: Union[Sequence[T], Set[T]]) -> bool:
        if len(self) > len(other):  # Fast check for obvious cases
            return False
        return all(item in other for item in self)

    def issuperset(self, other: Union[Sequence[T], Set[T]]) -> bool:
        if len(self) < len(other):  # Fast check for obvious cases
            return False
        return all(item in self for item in other)

    def symmetric_difference(self, other: Union[Sequence[T], Set[T]]) -> "OrderedSet[T]":
        cls = self.__class__ if isinstance(self, OrderedSet) else OrderedSet
        diff1 = cls(self).difference(other)
        diff2 = cls(other).difference(self)
        return diff1.union(diff2)

    def _update_items(self, items: list) -> None:
        self.items = items
        self.map = {item: idx for (idx, item) in enumerate(items)}

    def difference_update(self, *sets: Union[Sequence[T], Set[T]]) -> None:
        items_to_remove = set()  # type: Set[T]
        for other in sets:
            items_as_set = set(other)  # type: Set[T]
            items_to_remove |= items_as_set
        self._update_items([item for item in self.items if item not in items_to_remove])

    def intersection_update(self, other: Union[Sequence[T], Set[T]]) -> None:
        other = set(other)
        self._update_items([item for item in self.items if item in other])

    def symmetric_difference_update(self, other: Union[Sequence[T], Set[T]]) -> None:
        items_to_add = [item for item in other if item not in self]
        items_to_remove = set(other)
        self._update_items(
            [item for item in self.items if item not in items_to_remove] + items_to_add
        )