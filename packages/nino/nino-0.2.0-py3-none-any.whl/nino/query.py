from __future__ import annotations

__all__ = (
    "Query",
    "QueryFields",
    "QueryOperation",
)

import typing as t


class QueryIncomplete(Exception):
    def __init__(self, element: str) -> None:
        super().__init__(f"Query missing {element!r} element")


class QueryOperation:
    def __init__(
        self, type: str, *, name: str = None, variables: t.Dict[str, str]
    ) -> None:
        self.name = name
        self.type = type
        self.variables = variables

    def build(self) -> str:
        vars = ", ".join([f"{k}: {v}" for k, v in self.variables.items()])

        if self.name:
            operation = f"{self.type} {self.name} ({vars}) "
        else:
            operation = f"{self.type} ({vars}) "

        return operation + "{"

    def __str__(self) -> str:
        return self.build()


class QueryField:
    def __init__(self, name: str, *items, **arguments) -> None:
        self.name = name
        self.arguments = arguments

        self._items = list(items)
        self.fields = []

    def add_item(self, name: str) -> QueryField:
        self._items.append(name)
        return self

    def add_field(self, name: str, *items, **arguments) -> QueryField:
        field = QueryField(name, *items, **arguments)
        self.fields.append(field)

        return field

    def build(self) -> str:
        args = ", ".join([f"{k}: {v}" for k, v in self.arguments.items()])
        fields = "\n".join([field.build() for field in self.fields])
        items = "\n".join(self._items)

        if self._items or self.arguments:
            if args:
                query = f"{self.name} ({args}) " + "{\n" + f"{fields}\n{items}" + "\n}"
            else:
                query = f"{self.name} " + "{\n" + f"{fields}\n{items}" + "\n}"

            return query

        return self.name


class QueryFields:
    def __init__(
        self, name: str, fields: t.List[QueryField] = None, **arguments
    ) -> None:
        self.name = name
        self.fields = fields or []

        self.arguments = arguments

    def add_field(self, name: str, *items, **arguments) -> QueryField:
        field = QueryField(name, *items, **arguments)
        self.fields.append(field)

        return field

    def build(self) -> str:
        if not self.fields:
            raise QueryIncomplete("fields")

        fields = "\n".join([field.build() for field in self.fields])
        args = ", ".join([f"{k}: {v}" for k, v in self.arguments.items()])

        query = f"{self.name} ({args}) " + "{\n" + fields + "\n}"
        return query

    def __str__(self) -> str:
        return self.build()


class Query:
    def __init__(self, operation: QueryOperation, fields: QueryFields) -> None:
        self._operation = operation
        self._fields: QueryFields = fields

    @property
    def operation(self) -> QueryOperation:
        return self._operation

    @operation.setter
    def operation(self, value) -> None:
        if not isinstance(value, QueryOperation):
            raise TypeError("operation value must be an instance of QueryOperation")

        self._operation = value

    @property
    def fields(self) -> QueryFields:
        return self._fields

    @fields.setter
    def fields(self, value) -> None:
        if not isinstance(value, QueryFields):
            raise TypeError("fields value must be an instance of QueryFields")

        self._fields = value

    def set_operation(
        self, type: str, *, name: str = None, variables: t.Dict[str, str]
    ) -> QueryOperation:
        operation = QueryOperation(type, name=name, variables=variables)
        self._opration = operation

        return operation

    def add_fields(
        self, name: str, fields: t.List[QueryField] = None, **arguments
    ) -> QueryFields:
        self._fields: QueryFields = QueryFields(name, fields, **arguments)

        return self._fields

    def build(self) -> str:
        if not self._operation:
            raise QueryIncomplete("operation")

        operation = self.operation.build()

        query = operation + " "
        query += self._fields.build()

        return query + "\n}"

    def __str__(self) -> str:
        return self.build()

    # <3 blanket
