from datetime import datetime
from datetime import timezone
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple

from shillelagh.adapters.api.weatherapi import NativeDateTime
from shillelagh.adapters.base import Adapter
from shillelagh.backends.apsw.db import connect
from shillelagh.fields import DateTime
from shillelagh.fields import Float
from shillelagh.fields import Integer
from shillelagh.fields import Order
from shillelagh.fields import String
from shillelagh.filters import Equal
from shillelagh.filters import Filter
from shillelagh.filters import Range
from shillelagh.types import Row

from ..fakes import FakeAdapter
from ..fakes import FakeEntryPoint


class FakeAdapterWithDateTime(FakeAdapter):

    birthday = NativeDateTime(filters=[Range], order=Order.ANY, exact=True)

    data: List[Row] = []

    def __init__(self):
        pass


def test_adapter_get_columns():
    adapter = FakeAdapter()
    assert adapter.get_columns() == {
        "age": FakeAdapter.age,
        "name": FakeAdapter.name,
        "pets": FakeAdapter.pets,
    }
    adapter.close()


def test_adapter_get_metadata():
    adapter = FakeAdapter()
    assert adapter.get_metadata() == {}


def test_adapter_get_data():
    adapter = FakeAdapter()

    data = adapter.get_data({}, [])
    assert list(data) == [
        {"rowid": 0, "name": "Alice", "age": 20, "pets": 0},
        {"rowid": 1, "name": "Bob", "age": 23, "pets": 3},
    ]

    data = adapter.get_data({"name": Equal("Alice")}, [])
    assert list(data) == [
        {"rowid": 0, "name": "Alice", "age": 20, "pets": 0},
    ]

    data = adapter.get_data({"age": Range(20, None, False, False)}, [])
    assert list(data) == [
        {"rowid": 1, "name": "Bob", "age": 23, "pets": 3},
    ]

    data = adapter.get_data({}, [("age", Order.DESCENDING)])
    assert list(data) == [
        {"rowid": 1, "name": "Bob", "age": 23, "pets": 3},
        {"rowid": 0, "name": "Alice", "age": 20, "pets": 0},
    ]


def test_adapter_get_rows():
    adapter = FakeAdapter()

    adapter.insert_row({"rowid": None, "name": "Charlie", "age": 6, "pets": "1"})

    data = adapter.get_data({}, [])
    assert list(data) == [
        {"rowid": 0, "name": "Alice", "age": 20, "pets": 0},
        {"rowid": 1, "name": "Bob", "age": 23, "pets": 3},
        {"rowid": 2, "name": "Charlie", "age": 6.0, "pets": 1},
    ]

    data = adapter.get_rows({}, [])
    assert list(data) == [
        {"rowid": 0, "name": "Alice", "age": 20.0, "pets": 0},
        {"rowid": 1, "name": "Bob", "age": 23.0, "pets": 3},
        {"rowid": 2, "name": "Charlie", "age": 6.0, "pets": 1},
    ]


def test_adapter_manipulate_rows():
    adapter = FakeAdapter()

    adapter.insert_row({"rowid": None, "name": "Charlie", "age": 6, "pets": 1})
    data = adapter.get_data({}, [])
    assert list(data) == [
        {"rowid": 0, "name": "Alice", "age": 20, "pets": 0},
        {"rowid": 1, "name": "Bob", "age": 23, "pets": 3},
        {"rowid": 2, "name": "Charlie", "age": 6, "pets": 1},
    ]
    adapter.insert_row({"rowid": 4, "name": "Dani", "age": 40, "pets": 2})
    data = adapter.get_data({}, [])
    assert list(data) == [
        {"rowid": 0, "name": "Alice", "age": 20, "pets": 0},
        {"rowid": 1, "name": "Bob", "age": 23, "pets": 3},
        {"rowid": 2, "name": "Charlie", "age": 6, "pets": 1},
        {"rowid": 4, "name": "Dani", "age": 40, "pets": 2},
    ]

    adapter.delete_row(0)
    data = adapter.get_data({}, [])
    assert list(data) == [
        {"rowid": 1, "name": "Bob", "age": 23, "pets": 3},
        {"rowid": 2, "name": "Charlie", "age": 6, "pets": 1},
        {"rowid": 4, "name": "Dani", "age": 40, "pets": 2},
    ]

    adapter.update_row(1, {"rowid": 1, "name": "Bob", "age": 24, "pets": 4})
    data = adapter.get_data({}, [])
    assert list(data) == [
        {"rowid": 2, "name": "Charlie", "age": 6, "pets": 1},
        {"rowid": 4, "name": "Dani", "age": 40, "pets": 2},
        {"rowid": 1, "name": "Bob", "age": 24, "pets": 4},
    ]


def test_type_conversion(mocker):

    entry_points = [FakeEntryPoint("dummy", FakeAdapterWithDateTime)]
    mocker.patch(
        "shillelagh.backends.apsw.db.iter_entry_points",
        return_value=entry_points,
    )

    connection = connect(":memory:", ["dummy"], isolation_level="IMMEDIATE")
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM "dummy://"')
    assert cursor.fetchall() == []

    cursor.execute(
        'INSERT INTO "dummy://" (birthday) VALUES (?)',
        (datetime(2021, 1, 1, 0, 0),),
    )
    cursor.execute('SELECT * FROM "dummy://"')
    assert cursor.fetchall() == [
        (
            None,
            datetime(2021, 1, 1, 0, 0, tzinfo=timezone.utc),
            None,
            None,
        ),
    ]

    # make sure datetime is stored as a datetime
    assert FakeAdapterWithDateTime.data == [
        {
            "age": None,
            "birthday": datetime(2021, 1, 1, 0, 0, tzinfo=timezone.utc),
            "name": None,
            "pets": None,
            "rowid": 1,
        },
    ]
    assert isinstance(FakeAdapterWithDateTime.data[0]["birthday"], datetime)

    cursor.execute(
        'SELECT * FROM "dummy://" WHERE birthday > ?',
        (datetime(2020, 12, 31, 0, 0),),
    )
    assert cursor.fetchall() == [
        (None, datetime(2021, 1, 1, 0, 0, tzinfo=timezone.utc), None, None),
    ]
