import unittest
from migration.schema import MigrationRunner
from migration.registry import setup_default_migrations

class TestMigrationPipeline(unittest.TestCase):
    def setUp(self):
        self.runner = MigrationRunner(":memory:")
        setup_default_migrations(self.runner)

    def test_full_migration_cycle(self):
        # 1. Forward migrate all
        applied_count = self.runner.migrate_up()
        self.assertEqual(applied_count, 3)
        self.assertEqual(self.runner.get_applied_versions(), [1, 2, 3])

        # 2. Idempotent check
        re_apply = self.runner.migrate_up()
        self.assertEqual(re_apply, 0)

        # 3. Rollback one step
        rolled_back = self.runner.migrate_down(1)
        self.assertEqual(rolled_back, 1)
        self.assertEqual(self.runner.get_applied_versions(), [1, 2])

        # 4. Rollback remaining steps
        rolled_back_all = self.runner.migrate_down(2)
        self.assertEqual(rolled_back_all, 2)
        self.assertEqual(self.runner.get_applied_versions(), [])

if __name__ == "__main__":
    unittest.main()
