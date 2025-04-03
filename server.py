import socket
import threading
import subprocess

HOST = '0.0.0.0'  # استماع على جميع الواجهات
PORT = 2021
ALLOWED_IPS = set() # array of ips
print("Enter allowed IPs (press Enter to finish):")
while True:
    ip = input("Allowed IP: ").strip()
    if not ip:
        break
    ALLOWED_IPS.add(ip)

print(f"Allowed IPs: {ALLOWED_IPS}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

clients = []  # قائمة العملاء المتصلين

print(f"Server listening on port {PORT}...")

# دالة لإرسال رسالة لجميع العملاء
def broadcast_message(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:  # لا ترسل للمرسل نفسه (إلا إذا أردت ذلك)
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.remove(client)  # إزالة العميل في حالة خطأ

# دالة لمعالجة الأوامر المرسلة إلى السيرفر
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr  # إرسال الإخراج أو الخطأ
    except Exception as e:
        return str(e)

# دالة للتعامل مع كل عميل في Thread مستقل
def handle_client(client_socket, addr):
    clients.append(client_socket)  # إضافة العميل إلى القائمة
    print(f"Connection from {addr}")

    client_socket.send(b"Welcome! Type your message.\n")

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break  # إنهاء الاتصال في حالة عدم وجود بيانات

            if data.startswith("cmd:") or data.startswith("cmd :") :  # إذا كانت رسالة تنفيذ أمر
                parts = data.split(":", 1)  # تقسيم النص إلى جزئين فقط
                response = ""
                if len(parts) > 1:
                    command = parts[1].strip()
                    output = execute_command(command)  # تنفيذ الأمر في CMD
                    response = f"CMD Output:\n{output}" if output else "Command executed, no output."

                client_socket.send((f"Me\n{response}").encode() ) # إرسال النتيجة للجميع

            else:  # إذا كانت رسالة عادية
                message = f"From {addr[0]} Message :  {data}"
                print(message)
                broadcast_message(message, client_socket)  # إرسالها لجميع العملاء

        except Exception as e:
            print(f"Error with {addr}: {e}")
            break  # إنهاء الاتصال في حالة حدوث خطأ

    clients.remove(client_socket)  # إزالة العميل عند قطع الاتصال
    client_socket.close()
    print(f"Connection with {addr} closed.")

# استقبال الاتصالات وإنشاء Thread لكل عميل جديد
while True:
    client_socket, addr = server_socket.accept()

    # السماح فقط بالاتصالات من العناوين المحددة
    if addr[0] in ALLOWED_IPS:
        print(f"Accepted connection from {addr[0]}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()
    else:
        print(f"Rejected connection from {addr[0]}")
        client_socket.send((f"\n Rejected connection not allowed ").encode() )
        client_socket.close()
