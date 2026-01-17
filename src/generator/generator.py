import os
import time
import random
import psycopg2
from datetime import datetime

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("POSTGRESQL_DATABASE", "main_db")
DB_USER = os.getenv("POSTGRESQL_USERNAME", "wow_user")
DB_PASS = os.getenv("POSTGRESQL_PASSWORD", "wow_pass")
INTERVAL = int(os.getenv("GENERATION_INTERVAL", "1"))

PLAYERS = ["Stan", "Kyle", "Cartman", "Kenny", "Butters", "Randy", "Mr. Garrison", "Chef"]
GUILDS = ["Silver Hand", "Warsong Clan", "Kirin Tor", "The Horde", "Alliance Vanguard", "Shadow Council"]
RACES = ["Human", "Orc", "Night Elf", "Undead", "Dwarf", "Tauren", "Gnome", "Troll"]
CLASSES = ["Warrior", "Mage", "Rogue", "Priest", "Hunter", "Shaman", "Paladin", "Warlock"]

MOBS_BY_ZONE = {
    "Orgrimmar": ["Grunt", "Peon", "Witch Doctor"],
    "Stormwind": ["Guard", "Mage", "Knight"],
    "Blackrock Mountain": ["Dragon", "Orc Warlord", "Fire Elemental"],
    "Icecrown": ["Frost Wyrm", "Death Knight", "Lich"],
    "Zuldazar": ["Zandalari Warrior", "Loa Spirit", "Dinosaur"],
}

ITEMS = {
    "Common": ["Rusty Sword", "Leather Boots", "Health Potion"],
    "Rare": ["Enchanted Dagger", "Silk Robe", "Mana Crystal"],
    "Epic": ["Thunderfury", "Shadowmourne", "Ashbringer"],
}

ZONES = list(MOBS_BY_ZONE.keys())
ACTIONS = ["kill", "quest_complete", "loot", "arena_win", "dungeon_clear", "raid_kill", "craft", "trade"]

def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def init_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL,
            race VARCHAR(20) NOT NULL,
            class VARCHAR(20) NOT NULL,
            guild VARCHAR(50),
            pvp_rating INTEGER DEFAULT 1000,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS game_events (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
            action VARCHAR(50) NOT NULL,
            points INTEGER NOT NULL,
            player_level INTEGER CHECK (player_level BETWEEN 1 AND 70),
            zone VARCHAR(50),
            mob_name VARCHAR(50),
            item_rarity VARCHAR(20),
            item_name VARCHAR(100)
        );
    """)

def ensure_players(cursor):
    for name in PLAYERS:
        cursor.execute("""
            INSERT INTO players (name, race, class, guild, pvp_rating)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (name) DO NOTHING
        """, (
            name,
            random.choice(RACES),
            random.choice(CLASSES),
            random.choice(GUILDS),
            random.randint(800, 2500)
        ))

def get_player_id(cursor, name):
    cursor.execute("SELECT id FROM players WHERE name = %s", (name,))
    return cursor.fetchone()[0]

def generate_event(cursor):
    player_name = random.choice(PLAYERS)
    player_id = get_player_id(cursor, player_name)
    
    action = random.choice(ACTIONS)
    level = random.randint(1, 70)
    zone = random.choice(ZONES)
    
    mob_name = None
    if action in ("kill", "dungeon_clear", "raid_kill"):
        mob_name = random.choice(MOBS_BY_ZONE[zone])
    
    item_rarity = None
    item_name = None
    if action in ("loot", "quest_complete", "raid_kill"):
        if level > 60 and action == "raid_kill":
            item_rarity = "Epic"
        elif level > 40:
            item_rarity = "Rare"
        else:
            item_rarity = "Common"
        item_name = random.choice(ITEMS[item_rarity])
    
    base_points = {
        "kill": 20,
        "quest_complete": 50,
        "loot": 10,
        "arena_win": 120,
        "dungeon_clear": 100,
        "raid_kill": 500,
        "craft": 30,
        "trade": 15
    }.get(action, 10)
    
    points = base_points + level * 2
    if item_rarity == "Rare":
        points += 50
    elif item_rarity == "Epic":
        points += 200

    return (
        player_id, action, points, level, zone,
        mob_name, item_rarity, item_name
    )

def main():
    print("Generator started. Waiting for DB...")
    conn = None
    while not conn:
        try:
            conn = connect_db()
            cur = conn.cursor()
            init_tables(cur)
            ensure_players(cur)
            conn.commit()
            print("Tables ready. Generating events...")
        except Exception as e:
            print(f"DB not ready ({e}), retrying in 3s...")
            time.sleep(3)

    try:
        while True:
            event = generate_event(cur)
            cur.execute("""
                INSERT INTO game_events (
                    player_id, action, points, player_level, zone,
                    mob_name, item_rarity, item_name
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, event)
            conn.commit()

            ts = datetime.now().strftime('%H:%M:%S')
            print(f"[{ts}] {event[1]:<15} | lvl {event[3]:<2} | {event[4]:<20} | +{event[2]} pts")

            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nStopping generator...")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()