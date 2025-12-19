import os
import time
import random
import psycopg2
from datetime import datetime

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "wow_stats")
DB_USER = os.getenv("DB_USER", "wow_user")
DB_PASS = os.getenv("DB_PASS", "wow_pass")
INTERVAL = int(os.getenv("GENERATION_INTERVAL", "1"))

PLAYERS = ["Restik", "Arthas", "Thrall", "Jaina", "Sylvanas", "Garrosh", "Anduin", "Valeera"]
ACTIONS = ["kill", "quest_complete", "loot", "arena_win", "dungeon_clear", "raid_kill"]
ZONES = [
    "Orgrimmar", "Stormwind", "Dalaran", "Blackrock Mountain",
    "Netherstorm", "Icecrown", "Zuldazar", "Boralus"
]

def connect_db():
    """Устанавливает соединение с PostgreSQL."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def ensure_table_exists(cursor):
    """Создаёт таблицу, если она ещё не существует."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_events (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            player_name VARCHAR(50) NOT NULL,
            action VARCHAR(50) NOT NULL,
            points INTEGER NOT NULL,
            player_level INTEGER CHECK (player_level BETWEEN 1 AND 70),
            zone VARCHAR(50)
        );
    """)

def generate_event():
    """Генерирует одно случайное игровое событие."""
    return (
        random.choice(PLAYERS),
        random.choice(ACTIONS),
        random.randint(10, 500),
        random.randint(1, 70),
        random.choice(ZONES)
    )

def main():
    print("Generator запущен. Ожидание готовности БД...")
    conn = None
    cursor = None

    while conn is None:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            ensure_table_exists(cursor)
            conn.commit()
            print("Таблица game_events готова. Начинаем генерацию событий...")
        except psycopg2.OperationalError as e:
            print(f"PostgreSQL недоступен, повтор через 3 сек... ({e})")
            time.sleep(3)

    try:
        while True:
            event = generate_event()
            cursor.execute(
                """
                INSERT INTO game_events (player_name, action, points, player_level, zone)
                VALUES (%s, %s, %s, %s, %s)
                """,
                event
            )
            conn.commit()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ➕ {event}")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nОстановка генератора...")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    main()