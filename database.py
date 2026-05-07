import sqlite3

def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS keywords (id INTEGER PRIMARY KEY, keyword TEXT, domain TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, keyword TEXT, domain TEXT, rank INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def add_keywords_and_domains(keywords, domains):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    for keyword in keywords:
        for domain in domains:
            cursor.execute("INSERT INTO keywords (keyword, domain) VALUES (?, ?)", (keyword, domain))
    conn.commit()
    conn.close()

def get_keywords():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT keyword, domain FROM keywords")
    data = cursor.fetchall()
    conn.close()

    keywords = {}
    for keyword, domain in data:
        if keyword not in keywords:
            keywords[keyword] = []
        keywords[keyword].append(domain)
    return keywords

def save_result(keyword, domain, rank):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO results (keyword, domain, rank) VALUES (?, ?, ?)", (keyword, domain, rank))
    conn.commit()
    conn.close()
