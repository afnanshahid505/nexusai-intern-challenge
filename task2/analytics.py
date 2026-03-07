import asyncpg
from typing import List, Dict


async def get_lowest_resolution_intents(pool: asyncpg.Pool) -> List[Dict]:
    """
    Returns top 5 intents with lowest resolution rate in last 7 days
    along with their average CSAT score.
    """

    query = """
    SELECT
        intent,
        COUNT(*) AS total_calls,
        SUM(
            CASE WHEN outcome = 'resolved' THEN 1 ELSE 0 END
        ) AS resolved_calls,
        SUM(
            CASE WHEN outcome = 'resolved' THEN 1 ELSE 0 END
        )::float / COUNT(*) AS resolution_rate,
        AVG(csat_score) AS avg_csat
    FROM call_records
    WHERE timestamp >= NOW() - INTERVAL '7 days'
    GROUP BY intent
    ORDER BY resolution_rate ASC
    LIMIT 5;
    """

    async with pool.acquire() as conn:
        rows = await conn.fetch(query)

    return [dict(row) for row in rows]