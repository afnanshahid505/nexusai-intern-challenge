CREATE TABLE call_records (
    id SERIAL PRIMARY KEY,
    customer_phone VARCHAR(15) NOT NULL,
    channel VARCHAR(10) NOT NULL CHECK (
        channel IN ('voice', 'whatsapp', 'chat')
    ),
    transcript TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    intent VARCHAR(100) NOT NULL,
    outcome VARCHAR(20) NOT NULL CHECK (
        outcome IN ('resolved', 'escalated', 'failed')
    ),
    confidence_score FLOAT NOT NULL CHECK (
        confidence_score >= 0 AND confidence_score <= 1
    ),
    csat_score INTEGER CHECK (
        csat_score BETWEEN 1 AND 5
    ),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    duration INTEGER
);
-- Index to quickly find all interactions for a specific customer phone
CREATE INDEX idx_call_records_phone
ON call_records(customer_phone);

-- Index to speed up time-based queries (recent interactions, analytics)
CREATE INDEX idx_call_records_timestamp
ON call_records(timestamp);

-- Index to analyze performance of outcomes (resolved/escalated/failed)
CREATE INDEX idx_call_records_outcome
ON call_records(outcome);