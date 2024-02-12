with trades as (
    select *
    from trades
    ORDER BY executed_at 
),
indexes as (
    select *
    from indexes
    ORDER BY updated_at
),
result as (
    select t.transaction_id, ind.updated_at, ind.exchange, ind.exchange_type from trades t
    LEFT JOIN LATERAL (
        SELECT * from indexes i
        ORDER BY ABS(EXTRACT(EPOCH FROM t.executed_at - i.updated_at))
        LIMIT 1
    ) ind ON  t.currency_1 = ind.currency_1 
    AND  t.currency_2 = ind.currency_2
    AND t.exchange_type = ind.exchange_type
    AND t.exchange = ind.exchange 
)
select *
From result;
