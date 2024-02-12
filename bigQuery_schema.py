BIGQUERY_SCHEMA = [
    {
        "name": "column1",
        "type": "INTEGER",
        "mode": "NULLABLE"
    },
    {
        "name": "column2",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "column3",
        "type": "RECORD",
        "mode": "NULLABLE",
        "fields": [
            {
                "name": "nested1",
                "type": "STRING",
                "mode": "NULLABLE"
            },
            {
                "name": "nested2",
                "type": "RECORD",
                "mode": "NULLABLE",
                "fields": [
                    {
                        "name": "nested3",
                        "type": "BOOLEAN",
                        "mode": "NULLABLE"
                    }
                ]
            }
        ]
    },
    {
        "name": "column4",
        "type": "STRING",
        "mode": "REPEATED"
    },
    {
        "name": "column5",
        "type": "TIMESTAMP",
        "mode": "NULLABLE"
    }
]
