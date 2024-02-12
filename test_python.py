"""Module that contains a Pandas to BigQuery schema translator."""

import datetime
import pandas as pd

from bigQuery_schema import BIGQUERY_SCHEMA
from pandas_input import PANDAS_SCHEMA

data = [
    {
        "column1": 10,
        "column2": 3.14,
        "column3": {"nested1": "A", "nested2": {"nested3": True}},
        "column4": ["X", "Y"],
        "column5": datetime.datetime(2023, 1, 1),
    },
    {
        "column1": 20,
        "column2": 2.71,
        "column3": {"nested1": "B", "nested2": {"nested3": False}},
        "column4": ["Z"],
        "column5": datetime.datetime(2023, 2, 1),
    },
    {
        "column1": 30,
        "column2": 1.23,
        "column3": {"nested1": "C", "nested2": {"nested3": True}},
        "column4": ["W", "V"],
        "column5": datetime.datetime(2023, 3, 1),
    },
]
df = pd.DataFrame(data)
print(df)

DEFAULT_FIELD = {
    "name": "",
    "type": "",
    "mode": "NULLABLE"
}

DTYPES_KIND_BIGQUERY = {
    "i": "INTEGER",
    "f": "FLOAT",
    "M": "TIMESTAMP",
    "?": "BOOLEAN"
}

PYTHON_TYPES_BIGQUERY = {
    str: "STRING",
    int: "INTEGER",
    float: "FLOAT",
    dict: "RECORD",
    datetime.datetime: "TIMESTAMP",
    bool: "BOOLEAN",
}
DTYPES_NAMES_BIGQUERY = {
    "string": "STRING",
    "int64": "INTEGER",
    "float64": "FLOAT",
    "datetime64[ns]": "TIMESTAMP",
    "datetime": "TIMESTAMP",
    "bool": "BOOLEAN",
}


def generate_schema_from_nested_field(name: str, obj: dict | list):
    if isinstance(obj, dict):
        return {
                **DEFAULT_FIELD,
                "name": name,
                "type" : "RECORD",
                "fields": [
                    generate_schema_from_nested_field(key, value)
                    for key, value in obj.items() 
                ]
            }
    elif isinstance(obj, list):
        print(obj[0])
        return {
            **DEFAULT_FIELD,
            "name": name,
            "type": PYTHON_TYPES_BIGQUERY.get(
                type(obj[0]), # real item
                DTYPES_NAMES_BIGQUERY.get(obj[0]) # pandas type name
            ),
            "mode": "REPEATED",
        }
    else:
        if name == "column4":
            print("ACTUAL", obj, type(obj))
        return {
            **DEFAULT_FIELD,
            "name": name,
            "type": PYTHON_TYPES_BIGQUERY.get(
                type(obj), # real item
                DTYPES_NAMES_BIGQUERY.get(obj) # pandas type name
            )
        }



def generate_bigquery_schema_from_pandas(df: pd.DataFrame) -> list[dict]:
    bigquery_schema = []
    for column in df.columns:
        kind = df[column].dtype.kind
        if kind == 'O':
            current_column = generate_schema_from_nested_field(column, df[column].iloc[0])
        else:
            current_column = {**DEFAULT_FIELD}
            current_column["name"] = column
            current_column["type"] = DTYPES_KIND_BIGQUERY.get(kind, "UNKNOWN")
            if  current_column["type"] == "UNKONWN":
                raise ValueError(f"unknown kind {kind}", kind)

        bigquery_schema.append(current_column)
    return bigquery_schema

for field1, field2 in zip(generate_bigquery_schema_from_pandas(df=df), BIGQUERY_SCHEMA):
    assert field1 == field2
