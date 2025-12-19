CREATE TABLE IF NOT EXISTS wow_stats (
    id SERIAL PRIMARY_KEY,
    timestamp TIMESTAMPZ DEFAULT NOW(),
    player_name VARCHAR(50) NOT NULL,
    action VARCHAR(50),
    points INTEGER NOT NULL,
    lvl INTEGER CHECK (lvl BETWEEN 1 AND 70),
    zone VARCHAR(50)
);