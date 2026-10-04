import sqlite3
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def seed_database():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = OFF")

    print("Emptying database")
    con.execute("DELETE FROM users")
    con.execute("DELETE FROM threads")
    con.execute("DELETE FROM messages")
    con.execute("DELETE FROM participants")

    print("Creating 1 000 users")
    pw_hash = generate_password_hash("testi123")
    users = [(f"user_{i}", pw_hash) for i in range(1, 1001)]
    con.executemany("INSERT INTO users (username, password_hash) VALUES (?, ?)", users)

    print("Creating 100 000 notices and messages")
    locations = ["Kimpisen massatenniskentät", "Huhtiniemen sisähalli"]
    levels = ["Aloittelija", "Keskitaso", "Kilpa"]

    threads = []
    messages = []
    base_time = datetime.now()

    for i in range(1, 100001):
        user_id = random.randint(1, 1000)
        location = random.choice(locations)
        level = random.choice(levels)
        p_count = random.randint(1, 4)
        duration = random.randint(1, 4)

        days_ahead = random.randint(1, 365)
        hour = random.randint(8, 21)
        play_time = (base_time + timedelta(days=days_ahead)).replace(hour=hour, minute=0).strftime("%d.%m.%Y klo %H:%M")

        threads.append((i, play_time, location, level, p_count, duration, user_id, 1))

        sent_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        messages.append((f"Automaattisesti generoitu lisätieto vuorolle {i}.", sent_at, user_id, i, 1))

    con.executemany("INSERT INTO threads (id, play_time, location, skill_level, player_count, duration, user_id, visible) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", threads)
    con.executemany("INSERT INTO messages (content, sent_at, user_id, thread_id, status) VALUES (?, ?, ?, ?, ?)", messages)

    con.commit()
    con.close()
    print("Ready")

if __name__ == "__main__":
    seed_database()
