import os
import subprocess
from datetime import datetime
from config import DB_CONFIG, BACKUP_DIR

def ensure_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def generate_backup_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"backup_{timestamp}.sql"
    return os.path.join(BACKUP_DIR, filename)

def run_pg_dump(output_path):
    cmd = [
        "docker", "exec", "-i", "test-postgres",
        "pg_dump",
        "-U", DB_CONFIG["user"],
        DB_CONFIG["database"]
    ]
    env = os.environ.copy()
    env["PGPASSWORD"] = DB_CONFIG["password"]
    
    try:
        with open(output_path, "w", encoding="utf-8") as outfile:
            subprocess.run(cmd, env=env, check=True, stdout=outfile)
        print(f"Backup created: {output_path}")
    except subprocess.CalledProcessError as e:
        print("Backup failed:", e)

def cleanup_old_backups(keep=10):
    files = sorted(
        [f for f in os.listdir(BACKUP_DIR) if f.endswith(".sql")],
        key=lambda f: os.path.getmtime(os.path.join(BACKUP_DIR, f))
    )

    if len(files) > keep:
        old_files = files[:-keep]
        for f in old_files:
            path = os.path.join(BACKUP_DIR, f)
            os.remove(path)
            print(f"Removed old backup: {f}")

if __name__ == "__main__":
    ensure_backup_dir()
    output_file = generate_backup_filename()
    run_pg_dump(output_file)
    cleanup_old_backups()
