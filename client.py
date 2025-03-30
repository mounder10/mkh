import socket
import threading

HOST = '192.168.185.16'  # ضع هنا IP السيرفر
PORT = 2021

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# دالة لاستقبال الرسائل من السيرفر
def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"\n {data} ")  # طباعة الرسالة المستلمة
        except:
            print("Connection closed.")
            break

# تشغيل استقبال الرسائل في Thread منفصل
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

while True:
    message = input("Enter message (or 'exit' to quit): ")
    if message.lower() == 'exit':
        break
    client_socket.send(message.encode())

client_socket.close()
