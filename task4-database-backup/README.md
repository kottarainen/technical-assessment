# Task 4: Database backups
This script provides automates PostgreSQL database backups. It meets the requirements of the scenaio by creating timestamped backup files, storing them in a designated directory, and enforcing a retention policy of the 10 most recent backups.

## Scenario

The script should automatically back up a PostgreSQL database, create a backup file with a timestamp in the filename, store it in a designated backup directory and keep the 10 most recent backups.

## Features

- **Full database dump** using `pg_dump`
- **Timestamped backup filenames** for traceability
- **Backups stored** in the local `backups/` directory
- **Retention policy**: Only the latest 10 backups are kept
- **Environment configuration** isolated in `config.py`
- **Docker-based testing environment** provided

## Workflow

1. A timestamped `.sql` file is created using `pg_dump`
2. The file is saved in the `backups/` directory
3. The script checks how many backups exist
4. If more than 10, the oldest files are automatically deleted

## Testing with Docker

To test the script without a live production database, a local PostgreSQL instance was created using Docker.

### Start a test PostgreSQL container:

```bash
docker run --name test-postgres \
  -e POSTGRES_PASSWORD=testpass \
  -e POSTGRES_DB=testdb \
  -p 5432:5432 \
  -d postgres:13.4
```

##  Structure

```bash
task4-database-backup/
├── backup.py       # the script for running backups
├── config.py       # database connection config
├── backups/        # directory for .sql files
└── .gitignore  
