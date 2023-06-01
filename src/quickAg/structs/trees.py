from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, TypeVar, Generic, Iterable, Literal
from collections import deque

from .exceptions import EmptyTreeError

_T = TypeVar("_T")


@dataclass(slots=True)
class BinaryTreeNode(Generic[_T]):
    value: _T
    children: tuple[BinaryTreeNode | None, BinaryTreeNode | None] = (None, None)

    def __str__(self) -> str:
        return (
            (f"({self.value}) -> [")
            + (f"({self.left.value})" if self.left is not None else "-")
            + (f"({self.right.value})" if self.right is not None else "-")
            + "]"
        )

    # left :BinaryTreeNode[_T] = None
    # right :BinaryTreeNode[_T] = None
    # def __setattr__(self, __name: Literal["left","right"], __value: Any) -> None:
    #     if __name == "left":
    #         self.children = BinaryTreeNode(__value, self.left.children),self.right
    #     elif __name == "right":
    #         self.children = self.left, BinaryTreeNode(__value, self.right.children)
    #     else:
    #         raise ValueError

    # def __getattr__(self, __name: Literal["left","right"]) -> BinaryTreeNode[_T]:
    #     if __name == "left":
    #         if self.children[0] is not None:
    #             return self.children[0]
    #         raise EmptyTreeError
    #     if __name == "right":
    #         if self.children[1] is not None:
    #             return self.children[1]
    #         raise EmptyTreeError
    #     raise ValueError

    @property
    def left(self) -> BinaryTreeNode[_T]:
        if self.children[0] is None:
            raise EmptyTreeError
        return self.children[0]

    @left.setter
    def left(self, val: _T):
        if self.left is None:
            self.children = BinaryTreeNode(val), self.right
        else:
            self.left.value = val

    @property
    def right(self):
        if self.children[1] is None:
            raise EmptyTreeError
        return self.children[1]

    @right.setter
    def right(self, val: _T):
        if self.right is None:
            self.children = self.left, BinaryTreeNode(val)
        else:
            self.right.value = val


class BinaryTree(Generic[_T]):
    def __init__(self):
        self.__root: BinaryTreeNode[_T] | None = None

    def is_empty(self):
        return self.__root is None

    @property
    def root(self):
        if self.__root is None:
            raise EmptyTreeError
        return self.__root

    def insert(self, value: _T) -> None:
        if self.__root is None:
            self.__root = BinaryTreeNode(value)
            return
        queue = deque[BinaryTreeNode[_T]]()

        queue.append(self.__root)
        while len(queue):
            node = queue.popleft()
            try:
                queue.append(node.left)
            except EmptyTreeError:
                node.left = value
                return
            try:
                queue.append(node.right)
            except EmptyTreeError:
                node.right = value
                return

    def _traversewidth(self) -> Iterable[BinaryTreeNode[_T]]:
        if self.__root is None:
            raise StopIteration
        queue = deque[BinaryTreeNode[_T]]()

        queue.append(self.__root)
        while len(queue):
            node = queue.popleft()
            yield node
            try:
                queue.append(node.left)
            except EmptyTreeError:
                ...
            try:
                queue.append(node.right)
            except EmptyTreeError:
                ...

    def _traverseheight(self) -> Iterable[BinaryTreeNode[_T]]:
        if self.__root is None:
            raise StopIteration
        stack = deque[BinaryTreeNode[_T]]()

        stack.append(self.__root)
        while len(stack):
            node = stack.popleft()
            yield node
            try:
                stack.append(node.right)
            except EmptyTreeError:
                ...
            try:
                stack.append(node.left)
            except EmptyTreeError:
                ...
            node = stack.pop()

    def _getlastnode(self) -> BinaryTreeNode[_T]:
        if self.__root is None:
            raise EmptyTreeError
        for elm in self._traversewidth():
            pass
        return elm  # type: ignore

    def print(self):
        print(*self._traversewidth())
