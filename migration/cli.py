import sys
from migration.schema import MigrationRunner
from migration.registry import setup_default_migrations

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "up"
    runner = MigrationRunner("app.db")
    setup_default_migrations(runner)
    
    if action == "up":
        n = runner.migrate_up()
        print(f"Applied {n} migration(s). Current versions: {runner.get_applied_versions()}")
    elif action == "down":
        n = runner.migrate_down(1)
        print(f"Rolled back {n} migration(s). Current versions: {runner.get_applied_versions()}")

if __name__ == "__main__":
    main()
