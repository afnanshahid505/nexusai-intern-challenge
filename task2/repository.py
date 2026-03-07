import asyncpg
from typing import List, Dict


class CallRecordRepository:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool = None
    async def connect(self):
        """Create connection pool."""
        self.pool = await asyncpg.create_pool(self.db_url)
    async def save(self, call_data: Dict):
        """
        Save a customer interaction record into the database.
        Uses parameterized queries to prevent SQL injection.
        """
        query = """
        INSERT INTO call_records (
            customer_phone,
            channel,
            transcript,
            ai_response,
            intent,
            outcome,
            confidence_score,
            csat_score,
            duration
        )
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
        """
        async with self.pool.acquire() as conn:
            await conn.execute(
                query,
                call_data["customer_phone"],
                call_data["channel"],
                call_data["transcript"],
                call_data["ai_response"],
                call_data["intent"],
                call_data["outcome"],
                call_data["confidence_score"],
                call_data.get("csat_score"),
                call_data.get("duration")
            )
    async def get_recent(self, phone: str, limit: int = 5) -> List[Dict]:
        """
        Retrieve recent call records for a specific customer.
        """
        query = """
        SELECT *
        FROM call_records
        WHERE customer_phone = $1
        ORDER BY timestamp DESC
        LIMIT $2
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, phone, limit)

        return [dict(row) for row in rows]