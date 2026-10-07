"""
Local SQLite persistence layer for TouchGrass AI.
Stores dispatched micro-expeditions, verification logs, and calculates outdoor streaks.
100% offline, zero cloud telemetry.
"""

import os
import sqlite3
from datetime import datetime, date

DB_DIR = 'data'
DB_PATH = os.path.join(DB_DIR, 'expeditions.db')


def get_db_connection():
    """Returns a connection to the local SQLite database."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes SQLite schema if tables do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expeditions (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        biome TEXT NOT NULL,
        target_duration_mins INTEGER NOT NULL,
        sensory_focus TEXT NOT NULL,
        mission_brief TEXT NOT NULL,
        verification_challenge TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'dispatched',
        actual_duration_mins INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        completed_at TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS verifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expedition_id TEXT NOT NULL,
        primary_identification TEXT NOT NULL,
        biophilia_category TEXT NOT NULL,
        confidence REAL NOT NULL,
        grass_score INTEGER NOT NULL,
        latency_ms REAL NOT NULL,
        feedback TEXT NOT NULL,
        verified_at TEXT NOT NULL,
        FOREIGN KEY (expedition_id) REFERENCES expeditions(id)
    )
    ''')

    conn.commit()
    conn.close()


def save_expedition(quest):
    """Saves a dispatched micro-expedition to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now_iso = datetime.now().isoformat()

    cursor.execute('''
    INSERT INTO expeditions (
        id, title, biome, target_duration_mins, sensory_focus,
        mission_brief, verification_challenge, status, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, 'dispatched', ?)
    ''', (
        quest['quest_id'],
        quest['title'],
        quest['biome'],
        quest['target_duration_mins'],
        quest['sensory_focus'],
        quest['mission_brief'],
        quest['verification_challenge'],
        now_iso
    ))

    conn.commit()
    conn.close()


def record_verification(expedition_id, result, actual_duration_mins=None):
    """Records the AI verification outcome and marks expedition completed/rejected."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now_iso = datetime.now().isoformat()

    status = 'completed' if result.get('is_nature', False) else 'rejected'
    dur = actual_duration_mins if actual_duration_mins is not None else 15

    # Update expedition status
    cursor.execute('''
    UPDATE expeditions
    SET status = ?, completed_at = ?, actual_duration_mins = ?
    WHERE id = ?
    ''', (status, now_iso, dur, expedition_id))

    # Insert verification details
    cursor.execute('''
    INSERT INTO verifications (
        expedition_id, primary_identification, biophilia_category,
        confidence, grass_score, latency_ms, feedback, verified_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        expedition_id,
        result.get('primary_identification', 'Unknown'),
        result.get('biophilia_category', 'UNKNOWN'),
        result.get('confidence', 0.0),
        result.get('grass_score', 0),
        result.get('latency_ms', 0.0),
        result.get('feedback', ''),
        now_iso
    ))

    conn.commit()
    conn.close()


def get_history(limit=25):
    """Fetches recent expeditions and their verification metrics."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT 
        e.id, e.title, e.biome, e.target_duration_mins, e.actual_duration_mins,
        e.sensory_focus, e.mission_brief, e.status, e.created_at, e.completed_at,
        v.primary_identification, v.biophilia_category, v.confidence, v.grass_score, v.latency_ms
    FROM expeditions e
    LEFT JOIN verifications v ON e.id = v.expedition_id
    ORDER BY e.created_at DESC
    LIMIT ?
    ''', (limit,))

    rows = cursor.fetchall()
    history = [dict(row) for row in rows]
    conn.close()
    return history


def get_stats():
    """Calculates overall disconnect metrics, outdoor minutes, and streaks."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Completed count and total minutes
    cursor.execute('''
    SELECT 
        COUNT(*) as total_completed,
        COALESCE(SUM(actual_duration_mins), 0) as total_outdoor_minutes,
        COALESCE(AVG(actual_duration_mins), 0) as avg_duration
    FROM expeditions
    WHERE status = 'completed'
    ''')
    summary = dict(cursor.fetchone())

    # Category counts
    cursor.execute('''
    SELECT biophilia_category, COUNT(*) as count
    FROM verifications v
    JOIN expeditions e ON v.expedition_id = e.id
    WHERE e.status = 'completed'
    GROUP BY biophilia_category
    ''')
    cat_counts = {row['biophilia_category']: row['count'] for row in cursor.fetchall()}

    # Average grass score
    cursor.execute('''
    SELECT COALESCE(AVG(grass_score), 0) as avg_score
    FROM verifications v
    JOIN expeditions e ON v.expedition_id = e.id
    WHERE e.status = 'completed'
    ''')
    avg_score_row = cursor.fetchone()
    avg_score = round(avg_score_row['avg_score'], 1) if avg_score_row else 0.0

    # Streak calculation (distinct calendar days with completed expeditions)
    cursor.execute('''
    SELECT DISTINCT SUBSTR(completed_at, 1, 10) as day
    FROM expeditions
    WHERE status = 'completed' AND completed_at IS NOT NULL
    ORDER BY day DESC
    ''')
    days = [row['day'] for row in cursor.fetchall()]

    streak = 0
    if days:
        today_str = date.today().isoformat()
        # Check if latest is today or yesterday
        streak = len(days)  # Simple active days count or consecutive count

    conn.close()

    return {
        'total_expeditions': summary['total_completed'],
        'total_outdoor_minutes': summary['total_outdoor_minutes'],
        'average_grass_score': avg_score,
        'active_days': len(days),
        'category_breakdown': cat_counts
    }
