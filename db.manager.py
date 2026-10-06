import sqlite3
import os

DB_PATH = "carbon_project.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        wallet_balance REAL DEFAULT 150000.0
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_projects (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        owner TEXT NOT NULL,
        price REAL NOT NULL,
        volume INTEGER NOT NULL,
        duration INTEGER NOT NULL,
        funding_goal REAL NOT NULL,
        funded_amount REAL NOT NULL,
        status TEXT NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS social_posts (
        id TEXT PRIMARY KEY,
        author TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        time TEXT NOT NULL,
        likes INTEGER DEFAULT 0
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS green_diary (
        date_str TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        content TEXT NOT NULL
    );
    """)
    
    conn.commit()
    seed_default_data(conn)
    conn.close()

def seed_default_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO users (username, password, role, wallet_balance) VALUES (?, ?, ?, ?)
        """, [
            ("admin", "123", "Chủ rừng / Kỹ sư MRV", 150000.0),
            ("investor", "123", "Nhà đầu tư từ xa (Cổ đông)", 250000.0),
            ("buyer", "123", "Doanh nghiệp mua tín chỉ", 500000.0)
        ])
    
    cursor.execute("SELECT COUNT(*) FROM market_projects")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO market_projects (id, name, owner, price, volume, duration, funding_goal, funded_amount, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ("p1", "Dự án giảm phát thải Bắc Trung Bộ", "Bộ NN&PTNT", 10.5, 1030000, 5, 50000.0, 15000.0, "Active"))
        
    cursor.execute("SELECT COUNT(*) FROM social_posts")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO social_posts (id, author, role, content, time, likes)
        VALUES (?, ?, ?, ?, ?, ?)
        """, ("post_1", "Hệ Thống", "Admin", "Thử nghiệm công nghệ vệ tinh mới rất ấn tượng!", "04/10/2026 09:30", 12))
        
    cursor.execute("SELECT COUNT(*) FROM green_diary")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO green_diary (date_str, title, type, content) VALUES (?, ?, ?, ?)
        """, [
            ("2026-10-10", "Kỳ đánh giá sinh khối dự án", "Quan trọng", "Rà soát lại dữ liệu trên nền tảng GEE."),
            ("2026-10-15", "Phát hiện cháy rừng diện rộng", "Bất thường", "Rừng ở khu vực B bị suy giảm sinh khối nghiêm trọng.")
        ])
    conn.commit()

# --- USER FUNCTIONS ---
def load_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, role, wallet_balance FROM users")
    rows = cursor.fetchall()
    conn.close()
    return {row["username"]: {"password": row["password"], "role": row["role"], "wallet_balance": row["wallet_balance"]} for row in rows}

def register_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        return True, "Thành công"
    except sqlite3.IntegrityError:
        return False, "Tài khoản đã tồn tại."
    finally:
        conn.close()

# --- MARKET FUNCTIONS ---
def load_market_projects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM market_projects")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# --- SOCIAL FUNCTIONS ---
def load_social_posts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM social_posts ORDER BY rowid DESC")
    rows = cursor.fetchall()
    conn.close()
    result = []
    for row in rows:
        d = dict(row)
        d["comments"] = []
        result.append(d)
    return result

def add_social_post(author, role, content, post_time):
    conn = get_connection()
    cursor = conn.cursor()
    post_id = f"post_{int(os.urandom(4).hex(), 16)}"
    cursor.execute("""
    INSERT INTO social_posts (id, author, role, content, time, likes)
    VALUES (?, ?, ?, ?, ?, 0)
    """, (post_id, author, role, content, post_time))
    conn.commit()
    conn.close()

# --- DIARY FUNCTIONS ---
def load_green_diary():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM green_diary")
    rows = cursor.fetchall()
    conn.close()
    return {row["date_str"]: {"title": row["title"], "type": row["type"], "content": row["content"]} for row in rows}

def save_diary_entry(date_str, title, event_type, content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO green_diary (date_str, title, type, content)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(date_str) DO UPDATE SET
        title=excluded.title,
        type=excluded.type,
        content=excluded.content
    """, (date_str, title, event_type, content))
    conn.commit()
    conn.close()
