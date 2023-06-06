import tkinter as tk
from PIL import Image
import tkinter
import socket
import threading
import customtkinter
import requests
import shutil


def showimg(img_url):
    response = requests.get(img_url, stream=True)
    with open('img.png', 'wb') as file:
        shutil.copyfileobj(response.raw, file)
    del response

    img = Image.open('img.png')
    img.show()


def is_url_image(string):
    filetypes = ["jpg", "png", "jpeg", "gif"]
    for filetype in filetypes:
        print(filetype)
        if filetype in string:
            return True
    return False


def send_message():
    username = entry_username.get()
    message = entry_message.get()
    if message:
        send_data = f"{username} : {message}"
        client_socket.sendall(send_data.encode())
        entry_message.delete(0, tk.END)


def receive_message():
    while True:
        data = client_socket.recv(1024).decode("utf-8")
        string = data.split(" : ")
        if len(string) > 1:
            if is_url_image(string[1]):
                showimg(string[1])
        text_messages.insert(tk.END, data + "\n")


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

window = customtkinter.CTk()
window.iconbitmap('app/assets/icon.ico')
window.title("Chat 4T v0.0.1")
window.geometry('1280x720')

label_username = customtkinter.CTkLabel(master=window, text="Pseudo :", text_color='#FFFFFF')
label_username.place(relx=0.2, rely=0.1, anchor=tkinter.CENTER)

entry_username = customtkinter.CTkEntry(master=window)
entry_username.place(relx=0.2, rely=0.1, anchor=tkinter.CENTER)

label_messages = customtkinter.CTkLabel(master=window, text="Messages :")
label_messages.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

text_messages = customtkinter.CTkTextbox(master=window, width=500, height=400)
text_messages.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

label_message = customtkinter.CTkLabel(master=window, text="Message :")
label_message.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

entry_message = customtkinter.CTkEntry(master=window)
entry_message.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
entry_message.bind("<Return>", lambda event: send_message())

button_send = customtkinter.CTkButton(master=window, command=send_message, text='envoyer')
button_send.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("146.59.227.84", 8086))

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()
window.mainloop()
