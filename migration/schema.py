from dataclasses import dataclass
from typing import Callable, Any
import sqlite3

@dataclass
class MigrationStep:
    version: int
    name: str
    up_sql: str
    down_sql: str

class MigrationRunner:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._init_schema_table()
        self.migrations = []

    def _init_schema_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def register(self, version: int, name: str, up_sql: str, down_sql: str):
        self.migrations.append(MigrationStep(version, name, up_sql, down_sql))
        self.migrations.sort(key=lambda m: m.version)

    def get_applied_versions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT version FROM schema_migrations ORDER BY version ASC")
        return [row[0] for row in cursor.fetchall()]

    def migrate_up(self) -> int:
        applied = set(self.get_applied_versions())
        count = 0
        for m in self.migrations:
            if m.version not in applied:
                with self.conn:
                    self.conn.executescript(m.up_sql)
                    self.conn.execute("INSERT INTO schema_migrations (version, name) VALUES (?, ?)", (m.version, m.name))
                count += 1
        return count

    def migrate_down(self, steps: int = 1) -> int:
        applied = self.get_applied_versions()
        if not applied:
            return 0
        count = 0
        migration_dict = {m.version: m for m in self.migrations}
        for v in reversed(applied[-steps:]):
            if v in migration_dict:
                m = migration_dict[v]
                with self.conn:
                    self.conn.executescript(m.down_sql)
                    self.conn.execute("DELETE FROM schema_migrations WHERE version = ?", (v,))
                count += 1
        return count
