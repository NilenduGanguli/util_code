import oracledb

# Example connection details (replace with your actual details)
dsn = "user/password@host:port/service_name"

try:
    # Establish a database connection
    with oracledb.connect(dsn) as connection:
        with connection.cursor() as cursor:
            try:
                # Execute a query
                cursor.execute("SELECT * FROM some_table")
                
                # Fetch results
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

            except oracledb.DatabaseError as e:
                error, = e.args
                print("Database error occurred:", error)
                # Additional error handling (e.g., logging, rollback, etc.)

            except oracledb.IntegrityError as e:
                error, = e.args
                print("Integrity error occurred:", error)
                # Additional error handling (e.g., handling unique constraint violation)

            except Exception as e:
                print("An unexpected error occurred:", e)
                # Handle other types of exceptions

except oracledb.Error as e:
    print("Connection failed:", e)
    # Handle connection-related errors

except Exception as e:
    print("An unexpected error occurred during connection:", e)
    # Handle other types of exceptions
