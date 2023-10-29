import psycopg2
import threading
import time

# List of Database server IPs
db_ips = ["127.0.0.1","127.0.0.1"]  # Use "localhost" for local database


def reader_thread(ip):
    conn = psycopg2.connect(
        host=ip,
        database="test",  # Your database name
        user="dist_user",  # Your database user
        password='dist_pass_123'  # Your database user's password
    )
    cursor = conn.cursor()

    while True:
        # cursor = conn.cursor()
        # print('2\n')
        # Check for available messages with (RECEIVED_TIME IS NULL and SENDER_NAME != yours)

        sql = """
            SELECT RECORD_ID, SENDER_NAME, MESSAGE, SENT_TIME
            FROM ASYNC_MESSAGES
            WHERE RECEIVED_TIME IS NULL AND SENDER_NAME != %s
            
            FOR UPDATE SKIP LOCKED
        """
        cursor.execute(sql, ("Your Name",))
        rows = cursor.fetchall()

        for row in rows:
            if row:
                record_id, sender_name, message, sent_time = row
                received_time = time.strftime('%Y-%m-%d %H:%M:%S')

                # Mark the message as received
                update_sql = """
                    UPDATE ASYNC_MESSAGES
                    SET RECEIVED_TIME = %s
                    WHERE RECORD_ID = %s
                """
                cursor.execute(update_sql, (received_time, record_id))
                conn.commit()
                # cursor.execute(sql, ("Your Name",))

                print(f"Sender {sender_name} sent '{message}' at time {sent_time}.")
            else:
                time.sleep(1)  # Wait for messages if none are available
                # cursor.close()

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
