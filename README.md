# 🔄 orm-data-migration-pipeline

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](migration/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)](migration/)
[![CI](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)](ci/)

Lightweight Database Migration Engine with forward/rollback state management, DDL generation, and transaction safety.

## Features
- **Atomic Migrations:** Each migration step is executed inside an isolated SQLite transaction.
- **Rollback Guarantee:** Full symmetric `down` script definitions for backward schema safety.
- **Audit Tracking:** Stores applied versions, migration names, and timestamps in `schema_migrations`.

## Usage
```bash
python -m migration.cli up    # Run all pending migrations
python -m migration.cli down  # Roll back latest migration
```
