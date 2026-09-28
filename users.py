import db

def get_user(user_id):
    sql = """SELECT id, username, image IS NOT NULL as has_image
             FROM users
             WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def message_count(user_id):
    sql = "SELECT COUNT(*) FROM messages WHERE user_id = ? AND status = 1"
    result = db.query(sql, [user_id])
    return result[0][0] if result else 0

def get_messages(user_id, page, page_size):
    sql = """SELECT m.id, m.thread_id, 
                    t.pelipaikka || ' (' || t.peliaika || ')' as thread_title, 
                    m.sent_at
             FROM threads t, messages m
             WHERE t.id = m.thread_id AND m.user_id = ? AND m.status = 1
             ORDER BY m.sent_at DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [user_id, limit, offset])

def update_image(user_id, image):
    sql = "UPDATE users SET image = ? WHERE id = ?"
    db.execute(sql, [image, user_id])

def get_image(user_id):
    sql = "SELECT image FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0]["image"] if result and result[0]["image"] else None