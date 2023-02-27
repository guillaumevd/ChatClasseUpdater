import tkinter as tk
import tkinter
import socket
import threading
import customtkinter


def send_message():
    username = entry_username.get()
    message = entry_message.get()
    if message:
        send_data = f"{username} : {message}"
        client_socket.sendall(send_data.encode())
        entry_message.delete(0, tk.END)


def receive_message():
    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break
            text_messages.insert(tk.END, data + "\n")
        except:
            text_messages.insert(tk.END, "Le serveur a été déconnecté.\n")
            break


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

window = customtkinter.CTk()
window.iconbitmap('app/assets/icon.ico')
window.title("Chat 4T")
window.geometry("640x540")

label_username = customtkinter.CTkLabel(master=window, text="Pseudo :")
label_username.place(relx=0.2, rely=0.1, anchor=tkinter.CENTER)

entry_username = customtkinter.CTkEntry(master=window)
entry_username.place(relx=0.2, rely=0.1, anchor=tkinter.CENTER)

label_messages = customtkinter.CTkLabel(master=window, text="Messages :")
label_messages.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

text_messages = customtkinter.CTkTextbox(master=window)
text_messages.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

label_message = customtkinter.CTkLabel(master=window, text="Message :")
label_message.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

entry_message = customtkinter.CTkEntry(master=window)
entry_message.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

button_send = customtkinter.CTkButton(master=window, command=send_message)
button_send.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("146.59.227.84", 8086))

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()
window.mainloop()
