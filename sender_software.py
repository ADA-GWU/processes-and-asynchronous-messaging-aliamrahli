import psycopg2
import threading
import time
import queue

# List of Database server IPs
db_ips = ["127.0.0.1"]  # Use "localhost" for local database
thread_queue = queue.Queue()


def sender_thread(ip):
    conn = psycopg2.connect(
        host=ip,
        database="test",  # Your database name
        user="dist_user",  # Your database user
        password='dist_pass_123'  # Your database user's password
    )
    cursor = conn.cursor()

    while True:
        message = thread_queue.get()
        if message.lower() == "exit":
            break
        sender_name = "Ali"
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        sql = """
            INSERT INTO ASYNC_MESSAGES (SENDER_NAME, MESSAGE, SENT_TIME)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (sender_name, message, current_time))
        conn.commit()

    cursor.close()
    conn.close()

print('1')
# Create sender threads
sender_threads = []
for ip in db_ips:
    thread = threading.Thread(target=sender_thread, args=(ip,))
    sender_threads.append(thread)
    thread_queue.put("Start")
    thread.start()

while True:
    user_input = input("Enter your message (or 'exit' to quit): ")
    if user_input.lower() == "exit":
        # Add exit signal to the queue and wait for threads to finish
        for _ in range(thread_queue.qsize()):
            thread_queue.put("exit")
        break

    # Add user input to the queue to be processed by one of the sender threads
    thread_queue.put(user_input)

print('5')
thread_queue.join()
for thread in sender_threads:
    thread.join()


print("All sender threads have exited.")
