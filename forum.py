import db

def thread_count():
    sql = "SELECT COUNT(*) FROM threads WHERE visible = 1"
    result = db.query(sql)
    return result[0][0] if result else 0

def get_threads(page, page_size):
    sql = """SELECT t.id, t.play_time, t.location, t.skill_level, t.player_count, t.duration, COUNT(m.id) total, MAX(m.sent_at) last
             FROM threads t, messages m
             WHERE t.id = m.thread_id AND m.status = 1 AND t.visible = 1
             GROUP BY t.id
             ORDER BY t.id DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def add_thread(play_time, location, skill_level, player_count, duration, content, user_id):
    sql = """INSERT INTO threads (play_time, location, skill_level, player_count, duration, user_id)
             VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [play_time, location, skill_level, player_count, duration, user_id])
    thread_id = db.last_insert_id()
    add_message(content, user_id, thread_id)
    return thread_id

def add_message(content, user_id, thread_id):
    sql = """INSERT INTO messages (content, sent_at, user_id, thread_id, status)
             VALUES (?, datetime('now'), ?, ?, 1)"""
    db.execute(sql, [content, user_id, thread_id])

def get_thread(thread_id):
    sql = """SELECT t.id, t.play_time, t.location, t.skill_level, t.player_count, t.duration, t.user_id, u.username as creator
             FROM threads t, users u
             WHERE t.user_id = u.id AND t.id = ? AND t.visible = 1"""
    result = db.query(sql, [thread_id])
    return result[0] if result else None

def get_messages(thread_id):
    sql = """SELECT m.id, m.content, m.sent_at, m.user_id, u.username
             FROM messages m, users u
             WHERE m.user_id = u.id AND m.thread_id = ? AND m.status = 1
             ORDER BY m.id"""
    return db.query(sql, [thread_id])

def get_message(message_id):
    sql = "SELECT id, content, thread_id, user_id FROM messages WHERE id = ?"
    result = db.query(sql, [message_id])
    return result[0] if result else None

def update_message(message_id, content):
    sql = "UPDATE messages SET content = ? WHERE id = ?"
    db.execute(sql, [content, message_id])

def update_thread(thread_id, play_time, location, skill_level, player_count, duration):
    sql = """UPDATE threads
             SET play_time = ?, location = ?, skill_level = ?, player_count = ?, duration = ?
             WHERE id = ?"""
    db.execute(sql, [play_time, location, skill_level, player_count, duration, thread_id])


def remove_message(message_id):
    sql = "UPDATE messages SET status = 0 WHERE id = ?"
    db.execute(sql, [message_id])

def remove_thread(thread_id):
    sql = "UPDATE threads SET visible = 0 WHERE id = ?"
    db.execute(sql, [thread_id])

def search_thread_count(play_time, location, player_count):
    sql = """SELECT COUNT(*)
             FROM threads t, users u
             WHERE t.user_id = u.id AND t.visible = 1"""
    params = []

    if play_time:
        sql += " AND t.play_time LIKE ?"
        params.append("%" + play_time + "%")
    if location:
        sql += " AND t.location = ?"
        params.append(location)
    if player_count:
        sql += " AND t.player_count = ?"
        params.append(player_count)

    result = db.query(sql, params)
    return result[0][0] if result else 0

def search_threads(play_time, location, player_count, page, page_size):
    sql = """SELECT t.id as thread_id,
                    t.location || ' (' || t.play_time || ')' as thread_title,
                    u.username, t.skill_level, t.player_count, t.duration
             FROM threads t, users u
             WHERE t.user_id = u.id AND t.visible = 1"""
    params = []

    if play_time:
        sql += " AND t.play_time LIKE ?"
        params.append("%" + play_time + "%")
    if location:
        sql += " AND t.location = ?"
        params.append(location)
    if player_count:
        sql += " AND t.player_count = ?"
        params.append(player_count)

    sql += " ORDER BY t.id DESC LIMIT ? OFFSET ?"

    limit = page_size
    offset = page_size * (page - 1)
    params.extend([limit, offset])

    return db.query(sql, params)

def get_participants(thread_id):
    sql = """SELECT u.id, u.username
             FROM users u, participants p
             WHERE u.id = p.user_id AND p.thread_id = ?"""
    return db.query(sql, [thread_id])

def add_participant(user_id, thread_id):
    sql = "INSERT INTO participants (user_id, thread_id) VALUES (?, ?)"
    db.execute(sql, [user_id, thread_id])

def remove_participant(user_id, thread_id):
    sql = "DELETE FROM participants WHERE user_id = ? AND thread_id = ?"
    db.execute(sql, [user_id, thread_id])
