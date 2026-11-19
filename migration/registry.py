from migration.schema import MigrationRunner

def setup_default_migrations(runner: MigrationRunner):
    runner.register(
        version=1,
        name="create_users_table",
        up_sql="CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, email TEXT NOT NULL);",
        down_sql="DROP TABLE IF EXISTS users;"
    )
    runner.register(
        version=2,
        name="add_user_roles",
        up_sql="ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'USER';",
        down_sql="CREATE TABLE users_temp (id INTEGER PRIMARY KEY, username TEXT NOT NULL, email TEXT NOT NULL); INSERT INTO users_temp SELECT id, username, email FROM users; DROP TABLE users; ALTER TABLE users_temp RENAME TO users;"
    )
    runner.register(
        version=3,
        name="create_audit_logs",
        up_sql="CREATE TABLE audit_logs (id INTEGER PRIMARY KEY, action TEXT NOT NULL, user_id INTEGER);",
        down_sql="DROP TABLE IF EXISTS audit_logs;"
    )
