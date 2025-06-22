import psycopg2
from prettytable import PrettyTable
from config import DB_CONFIG

def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Connected to the database.")
        return conn
    except Exception as e:
        print("Could not connect to the database:")
        print(e)
        return None

def get_system_resources(conn):
    cursor = conn.cursor()
    print("\nSystem Resources (from pg_stat_activity):")

    query = """
    SELECT 
        round(sum(shared_blks_hit) / NULLIF(sum(shared_blks_hit + shared_blks_read), 0)::numeric, 2) as cache_hit_ratio
    FROM pg_stat_database;
    """
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        print(f"Cache Hit Ratio: {result[0] * 100 if result[0] is not None else 'N/A'}%")
    except Exception as e:
        print("Error fetching system resource stats:", e)

    cursor.close()

def get_connection_stats(conn):
    cursor = conn.cursor()
    print("\nConnection Management:")

    try:
        # active connections
        cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE state = 'active';")
        active_connections = cursor.fetchone()[0]

        # active transactions
        cursor.execute("""
            SELECT count(*) 
            FROM pg_stat_activity 
            WHERE state = 'active' AND xact_start IS NOT NULL;
        """)
        active_transactions = cursor.fetchone()[0]

        print(f"Active Connections: {active_connections}")
        print(f"Active Transactions: {active_transactions}")
    except Exception as e:
        print("Error fetching connection stats:", e)

    cursor.close()

def get_slow_queries(conn):
    cursor = conn.cursor()
    print("\nSlow Query Analysis:")

    try:
        # count of queries with avg_time > 200ms
        cursor.execute("""
            SELECT count(*) 
            FROM pg_stat_statements 
            WHERE total_time / calls > 200;
        """)
        slow_query_count = cursor.fetchone()[0]
        print(f"Number of queries with avg execution time > 200ms: {slow_query_count}")

        # top 10 slowest queries (by avg time)
        cursor.execute("""
            SELECT query, round(total_time / calls, 2) AS avg_time_ms
            FROM pg_stat_statements 
            WHERE calls > 0
            ORDER BY avg_time_ms DESC
            LIMIT 10;
        """)
        top_slow = cursor.fetchall()

        if top_slow:
            print("\nTop 10 slowest queries:")
            table = PrettyTable(["Avg Time (ms)", "Query"])
            for row in top_slow:
                table.add_row([row[1], row[0][:80] + ("..." if len(row[0]) > 80 else "")])
            print(table)
        else:
            print("No slow queries found.")
    except Exception as e:
        print("Error analyzing slow queries:", e)

    cursor.close()

def get_storage_stats(conn):
    cursor = conn.cursor()
    print("\nStorage usage:")

    try:
        # total size of the current database
        cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()));")
        db_size = cursor.fetchone()[0]
        print(f"Database size: {db_size}")

        # Top 5 largest tables
        cursor.execute("""
            SELECT
              relname AS table_name,
              pg_size_pretty(pg_total_relation_size(relid)) AS total_size
            FROM pg_catalog.pg_statio_user_tables
            ORDER BY pg_total_relation_size(relid) DESC
            LIMIT 5;
        """)
        top_tables = cursor.fetchall()

        print("\nTop 5 largest tables:")
        table = PrettyTable(["Table", "Size"])
        for row in top_tables:
            table.add_row(row)
        print(table)

    except Exception as e:
        print("Error retrieving storage info:", e)

    cursor.close()

if __name__ == "__main__":
    conn = connect_to_db()
    if conn:
        get_system_resources(conn)
        get_connection_stats(conn)
        get_slow_queries(conn)
        get_storage_stats(conn)
        conn.close()