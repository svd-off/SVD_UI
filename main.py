
import tkinter as tk
from tkinter import messagebox
import requests
import os
import sys
import threading
import time
import pygame

# === Настройки автообновления ===
VERSION = "1.0"
VERSION_URL = "https://raw.githubusercontent.com/openai-sandbox/svd-updater/main/version.txt"
UPDATE_URL = "https://raw.githubusercontent.com/openai-sandbox/svd-updater/main/SVD_UI.exe"

# === Telegram Bot Token и Chat ID ===
BOT_TOKEN = "8184833461:AAGmTXbKMeh3-oBC7MomZfBGD0zj0XCIXWk"
CHAT_ID = "6107814655"

# === Проверка и загрузка обновления ===
def check_for_update():
    try:
        r = requests.get(VERSION_URL, timeout=5)
        if r.status_code == 200 and r.text.strip() != VERSION:
            download_update()
    except:
        pass

def download_update():
    try:
        r = requests.get(UPDATE_URL, stream=True)
        with open("SVD_NEW.exe", "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        os.startfile("SVD_NEW.exe")
        sys.exit()
    except:
        messagebox.showerror("Ошибка", "Не удалось загрузить обновление.")

# === Отправка сообщения в Telegram ===
def send_to_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": text
        }
        requests.post(url, data=data)
    except:
        pass

# === Отправка при нажатии ===
def on_send():
    text = entry.get()
    if not text.strip():
        messagebox.showwarning("Пустое сообщение", "Введите текст перед отправкой.")
        return
    send_to_telegram(text)
    entry.delete(0, tk.END)
    messagebox.showinfo("Отправлено", "Сообщение отправлено!")

# === Музыка ===
def play_music():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.play(-1)
    except:
        pass

# === Интерфейс ===
def launch_app():
    threading.Thread(target=check_for_update, daemon=True).start()
    threading.Thread(target=play_music, daemon=True).start()

    window = tk.Tk()
    window.title("SVD_Cyberpunk_UI")
    window.geometry("400x300")
    window.configure(bg="#0f0f0f")

    label = tk.Label(window, text="Введите обращение:", fg="#39ff14", bg="#0f0f0f", font=("Consolas", 14))
    label.pack(pady=10)

    global entry
    entry = tk.Entry(window, font=("Consolas", 14), fg="#39ff14", bg="#1a1a1a", insertbackground="#39ff14", width=30)
    entry.pack(pady=10)

    send_button = tk.Button(window, text="Отправить", command=on_send,
                            font=("Consolas", 14), bg="#000000", fg="#39ff14", activebackground="#39ff14", activeforeground="#000000")
    send_button.pack(pady=10)

    window.mainloop()

launch_app()
