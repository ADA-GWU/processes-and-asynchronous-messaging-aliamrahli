import psycopg2
import threading
import time

# List of Database server IPs
db_ips = ["localhost"]  # Use "localhost" for local database


def sender_thread(ip):
    conn = psycopg2.connect(
        host=ip,
        database="test",  # Your database name
        user="dist_user",  # Your database user
        password='dist_pass_123'  # Your database user's password
    )
    cursor = conn.cursor()

    while True:
        message = input("Enter your message (or 'exit' to quit): ")
        if message.lower() == "exit":
            break

        sender_name = "Your Name"
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        sql = """
            INSERT INTO ASYNC_MESSAGES (SENDER_NAME, MESSAGE, SENT_TIME)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (sender_name, message, current_time))
        conn.commit()

    cursor.close()
    conn.close()


# Create sender threads
sender_threads = []
for ip in db_ips:
    thread = threading.Thread(target=sender_thread, args=(ip,))
    sender_threads.append(thread)
    thread.start()

# Wait for all sender threads to finish
for thread in sender_threads:
    thread.join()

print("All sender threads have exited.")


