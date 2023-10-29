import psycopg2
import threading
import time

# List of Database server IPs

db_ips = ["localhost"]


def reader_thread(ip):
    conn = psycopg2.connect(
        host=ip,
        database="test",
        user="dist_user",
        password='dist_pass_123'
    )
    cursor = conn.cursor()

    while True:

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

                update_sql = """
                    UPDATE ASYNC_MESSAGES
                    SET RECEIVED_TIME = %s
                    WHERE RECORD_ID = %s
                """
                cursor.execute(update_sql, (received_time, record_id))
                conn.commit()

                print(f"Sender {sender_name} sent '{message}' at time {sent_time}.")
            else:
                time.sleep(1)

    cursor.close()
    conn.close()


# list for storing threads to keep track of them
reader_threads = []
for ip in db_ips:
    thread = threading.Thread(target=reader_thread, args=(ip,))
    reader_threads.append(thread)
    thread.start()

# wait for all threads to finish
for thread in reader_threads:
    thread.join()

print("All reader threads have exited.")
