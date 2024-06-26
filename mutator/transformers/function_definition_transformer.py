from typing import Union, Literal, no_type_check

import libcst

from type_definitions.function_path import FunctionPath
from transformers.abstract_transformer import AbstractTransformer
from visitors.abstract_visitor import AbstractVisitor


class FunctionDefinitionTransformer(AbstractTransformer):
    def __init__(
        self,
        result: AbstractVisitor.Result,
        mode: Union[Literal["insert"], Literal["remove"]] = "remove",
    ) -> None:
        self.result = result
        self.mode = mode

        self.current_function_path: FunctionPath = []

    def visit_ClassDef(self, node: libcst.ClassDef) -> Literal[True]:
        self.current_function_path.append(node.name.value)

        return True

    @no_type_check
    def leave_ClassDef(
        self, original_node: libcst.ClassDef, updated_node: libcst.ClassDef
    ) -> libcst.CSTNode:
        self.current_function_path.pop()

        return updated_node

    @no_type_check
    def visit_FunctionDef(self, node: libcst.FunctionDef) -> Literal[True]:
        return self.visit_ClassDef(node)

    @no_type_check
    def leave_FunctionDef(
        self, original_node: libcst.FunctionDef, updated_node: libcst.FunctionDef
    ) -> libcst.CSTNode:
        return self.leave_ClassDef(original_node, updated_node)

    @no_type_check
    def leave_Param(
        self,
        original_node: libcst.Param,
        updated_node: libcst.Param,
    ) -> Union[libcst.Param, libcst.RemovalSentinel]:
        path = self.__current_path()

        if path in self.result.data and original_node not in self.result.data[path]:
            return libcst.RemovalSentinel.REMOVE
        else:
            return updated_node

    def leave_Parameters(
        self,
        original_node: libcst.Parameters,
        updated_node: libcst.Parameters,
    ) -> libcst.Parameters:
        if self.mode == "remove" and (not original_node.deep_equals(updated_node)):
            if len(updated_node.params) == 1:
                return updated_node.with_deep_changes(
                    updated_node.params[0], comma=libcst.MaybeSentinel.DEFAULT
                )
        elif self.mode == "insert" and updated_node.params != (
            self.result.data[self.__current_path()]
        ):
            return updated_node.with_changes(
                params=self.result.data[self.__current_path()]
            )

        return updated_node

    def __current_path(self) -> str:
        return ".".join(self.current_function_path)
