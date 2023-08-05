import datetime
import json
from collections import defaultdict
from typing import Any
from typing import cast
from typing import DefaultDict
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type

import apsw
from shillelagh.adapters.base import Adapter
from shillelagh.exceptions import ProgrammingError
from shillelagh.fields import Field
from shillelagh.fields import Integer
from shillelagh.fields import Order
from shillelagh.fields import type_map
from shillelagh.filters import Filter
from shillelagh.filters import Operator
from shillelagh.lib import deserialize
from shillelagh.types import Constraint
from shillelagh.types import Index
from shillelagh.types import RequestedOrder
from shillelagh.types import Row
from shillelagh.types import SQLiteValidType


operator_map = {
    apsw.SQLITE_INDEX_CONSTRAINT_EQ: Operator.EQ,
    apsw.SQLITE_INDEX_CONSTRAINT_GE: Operator.GE,
    apsw.SQLITE_INDEX_CONSTRAINT_GT: Operator.GT,
    apsw.SQLITE_INDEX_CONSTRAINT_LE: Operator.LE,
    apsw.SQLITE_INDEX_CONSTRAINT_LT: Operator.LT,
}


SQLiteRow = Dict[str, SQLiteValidType]


def convert_rows_to_sqlite(
    columns: Dict[str, Field],
    rows: Iterator[Row],
) -> Iterator[SQLiteRow]:
    """
    Convert values from native Python types to SQLite types.

    Native Python types like `datetime.datetime` are not supported by SQLite; instead
    we need to cast them to strings or numbers. We use the original fields to handle
    the conversion (not the adapter fields).
    """
    converters = {
        column_name: type_map[column_field.type]().format
        for column_name, column_field in columns.items()
    }
    converters["rowid"] = Integer().format
    for row in rows:
        yield {
            column_name: converters[column_name](value)
            for column_name, value in row.items()
        }


def convert_rows_from_sqlite(
    columns: Dict[str, Field],
    rows: Iterator[SQLiteRow],
) -> Iterator[Row]:
    """
    Convert values from SQLite types to native Python types.

    Native Python types like `datetime.datetime` are not supported by SQLite; instead
    we need to cast them to strings or numbers. We use the original fields to handle
    the conversion (not the adapter fields).
    """
    converters = {
        column_name: type_map[column_field.type]().parse
        for column_name, column_field in columns.items()
    }
    converters["rowid"] = Integer().parse
    for row in rows:
        yield {
            column_name: converters[column_name](value)
            for column_name, value in row.items()
        }


class VTModule:
    def __init__(self, adapter: Type[Adapter]):
        self.adapter = adapter

    def Create(
        self,
        connection: apsw.Connection,
        modulename: str,
        dbname: str,
        tablename: str,
        *args: str,
    ) -> Tuple[str, "VTTable"]:
        deserialized_args = [deserialize(arg) for arg in args]
        adapter = self.adapter(*deserialized_args)
        table = VTTable(adapter)
        create_table: str = table.get_create_table(tablename)
        return create_table, table

    Connect = Create


class VTTable:
    def __init__(self, adapter: Adapter):
        self.adapter = adapter

    def get_create_table(self, tablename: str) -> str:
        columns = self.adapter.get_columns()
        if not columns:
            raise ProgrammingError(f"Virtual table {tablename} has no columns")
        formatted_columns = ", ".join(f'"{k}" {v.type}' for (k, v) in columns.items())
        return f'CREATE TABLE "{tablename}" ({formatted_columns})'

    def BestIndex(
        self,
        constraints: List[Tuple[int, int]],
        orderbys: List[Tuple[int, bool]],
    ) -> Tuple[List[Constraint], int, str, bool, int]:
        column_types = list(self.adapter.get_columns().values())

        index_number = 42
        estimated_cost = 666

        indexes: List[Index] = []
        constraints_used: List[Constraint] = []
        filter_index = 0
        for column_index, sqlite_index_constraint in constraints:
            operator = operator_map.get(sqlite_index_constraint)
            column_type = column_types[column_index]
            for class_ in column_type.filters:
                if operator in class_.operators:
                    constraints_used.append((filter_index, column_type.exact))
                    filter_index += 1
                    indexes.append((column_index, sqlite_index_constraint))
                    break
            else:
                # no indexes supported in this column
                constraints_used.append(None)

        # is the data being returned in the requested order? if not, SQLite will have
        # to sort it
        orderby_consumed = True
        orderbys_to_process: List[Tuple[int, bool]] = []
        for column_index, descending in orderbys:
            requested_order = Order.DESCENDING if descending else Order.ASCENDING
            column_type = column_types[column_index]
            if column_type.order == Order.ANY:
                orderbys_to_process.append((column_index, descending))
            elif column_type.order != requested_order:
                orderby_consumed = False
                break

        # serialize the indexes to str so it can be used later when filtering the data
        index_name = json.dumps([indexes, orderbys_to_process])

        return (
            constraints_used,
            index_number,
            index_name,
            orderby_consumed,
            estimated_cost,
        )

    def Open(self) -> "VTCursor":
        return VTCursor(self.adapter)

    def Disconnect(self) -> None:
        self.adapter.close()

    Destroy = Disconnect

    def UpdateInsertRow(self, rowid: Optional[int], fields: Tuple[Any, ...]) -> int:
        columns = self.adapter.get_columns()

        row = {column_name: field for field, column_name in zip(fields, columns.keys())}
        row["rowid"] = rowid
        row = next(convert_rows_from_sqlite(columns, iter([row])))

        return cast(int, self.adapter.insert_row(row))

    def UpdateDeleteRow(self, rowid: int) -> None:
        self.adapter.delete_row(rowid)

    def UpdateChangeRow(
        self,
        rowid: int,
        newrowid: int,
        fields: Tuple[Any, ...],
    ) -> None:
        columns = self.adapter.get_columns()

        row = {column_name: field for field, column_name in zip(fields, columns.keys())}
        row["rowid"] = newrowid
        row = next(convert_rows_from_sqlite(columns, iter([row])))

        self.adapter.update_row(rowid, row)


class VTCursor:
    def __init__(self, adapter: Adapter):
        self.adapter = adapter

    def Filter(
        self,
        indexnumber: int,
        indexname: str,
        constraintargs: List[Any],
    ) -> None:
        columns: Dict[str, Field] = self.adapter.get_columns()
        column_names: List[str] = list(columns.keys())
        index = json.loads(indexname)
        indexes: List[Index] = index[0]
        orderbys: List[Tuple[int, bool]] = index[1]

        all_bounds: DefaultDict[str, Set[Tuple[Operator, Any]]] = defaultdict(set)
        for (column_index, sqlite_index_constraint), constraint in zip(
            indexes,
            constraintargs,
        ):
            if sqlite_index_constraint not in operator_map:
                raise Exception(f"Invalid constraint passed: {sqlite_index_constraint}")
            operator = operator_map[sqlite_index_constraint]
            column_name = column_names[column_index]
            column_type = columns[column_name]

            # convert constraint to native Python type, then to DB specific type
            constraint = type_map[column_type.type]().parse(constraint)
            value = column_type.format(constraint)

            all_bounds[column_name].add((operator, value))

        # find the filter that works with all the operations and build it
        bounds: Dict[str, Filter] = {}
        for column_name, operations in all_bounds.items():
            column_type = columns[column_name]
            operators = {operation[0] for operation in operations}
            for class_ in column_type.filters:
                if all(operator in class_.operators for operator in operators):
                    break
            else:
                raise Exception("No valid filter found")
            bounds[column_name] = class_.build(operations)

        order: List[Tuple[str, RequestedOrder]] = [
            (
                column_names[column_index],
                Order.DESCENDING if descending else Order.ASCENDING,
            )
            for column_index, descending in orderbys
        ]

        rows = self.adapter.get_rows(bounds, order)
        rows = convert_rows_to_sqlite(columns, rows)
        self.data = (
            tuple(row[name] for name in ["rowid", *column_names]) for row in rows
        )
        self.Next()

    def Eof(self) -> bool:
        return self.eof

    def Rowid(self) -> int:
        return cast(int, self.current_row[0])

    def Column(self, col) -> Any:
        return self.current_row[1 + col]

    def Next(self) -> None:
        try:
            self.current_row = next(self.data)
            self.eof = False
        except StopIteration:
            self.eof = True

    def Close(self) -> None:
        pass
