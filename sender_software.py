import psycopg2
import threading
import time
import queue

# List of Database server IPs
db_ips = ["127.0.0.1"]
thread_queue = queue.Queue()
exit_event = threading.Event()

def sender_thread(ip):
    conn = psycopg2.connect(
        host=ip,
        database="test",
        user="dist_user",
        password='dist_pass_123'
    )
    cursor = conn.cursor()

    while not exit_event.is_set():
        message = thread_queue.get()
        if message.lower() == "exit":
            break
        sender_name = "Ali Amrahli"
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        sql = """
            INSERT INTO ASYNC_MESSAGES (SENDER_NAME, MESSAGE, SENT_TIME)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (sender_name, message, current_time))
        conn.commit()

    cursor.close()
    conn.close()


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
        exit_event.set()
        for _ in range(len(db_ips)):
            thread_queue.put("exit")
        break

    # Add user input to the queue to be processed by one of the sender threads
    thread_queue.put(user_input)


for thread in sender_threads:
    thread.join()


print("All sender threads have exited.")
