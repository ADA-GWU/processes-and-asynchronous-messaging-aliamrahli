import threading
import psycopg2
import time

# List of Database server IPs
db_ips = ["localhost"]  # Use "localhost" for local database


def reader_thread(ip):
    conn = psycopg2.connect(
        host=ip,
        database="test",  # Your database name
        user="dist_user",  # Your database user
        password="dist_pass_123"  # Your database user's password
    )
    cursor = conn.cursor()

    while True:
        try:
            # Select an available message and lock the record
            cursor.execute("""
                SELECT RECORD_ID, SENDER_NAME, MESSAGE, SENT_TIME
                FROM ASYNC_MESSAGES
                WHERE RECEIVED_TIME IS NULL AND SENDER_NAME != 'Your Name'
                ORDER BY RECORD_ID
                FOR UPDATE SKIP LOCKED
                LIMIT 1
            """)
            row = cursor.fetchone()

            if row:
                record_id, sender_name, message, sent_time = row
                print(f"Sender {sender_name} sent '{message}' at time {sent_time}.")

                # Update RECEIVED_TIME to mark the message as received
                cursor.execute("""
                    UPDATE ASYNC_MESSAGES
                    SET RECEIVED_TIME = %s
                    WHERE RECORD_ID = %s
                """, (time.strftime('%Y-%m-%d %H:%M:%S'), record_id))
                conn.commit()

            time.sleep(1)  # Pause for a short interval before checking for the next message
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()  # Roll back the transaction in case of an error

    cursor.close()
    conn.close()


# Create reader threads
reader_threads = []
for ip in db_ips:
    thread = threading.Thread(target=reader_thread, args=(ip,))
    reader_threads.append(thread)
    thread.start()

# Wait for all reader threads to finish
for thread in reader_threads:
    thread.join()

print("All reader threads have exited.")
