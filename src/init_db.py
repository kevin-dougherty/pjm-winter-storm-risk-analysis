from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "pjm_risk.duckdb"
SQL_DIR = ROOT / "sql"

def main():
    DB_PATH.parent.mkdir(exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    # Run every numbered SQL file in order: a minimal "migrations" pattern
    for sql_file in sorted(SQL_DIR.glob("*.sql")):
        print(f"Running {sql_file.name}")
        con.execute(sql_file.read_text())
    print(con.sql("SELECT table_schema, table_name FROM information_schema.tables"))
    con.close()

if __name__ == "__main__":
    main()
