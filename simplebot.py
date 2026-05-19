import tkinter.scrolledtext as tks  
from datetime import datetime
from tkinter import Tk, Frame, Label, Button, Text, END, WORD, NORMAL, DISABLED
from openai import OpenAI
import threading

client = OpenAI()

def get_bot_response(user_input):
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": "You are a helpful assistant chatbot."},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content.strip()

def create_and_insert_user_frame(user_input):
    userFrame = Frame(chatWindow, bg="#d0ffff")
    Label(
        userFrame,
        text=user_input,
        font=("Arial", 11),
        bg="#d0ffff"
    ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

    Label(
        userFrame,
        text=datetime.now().strftime("%H:%M"),
        font=("Arial", 7),
        bg="#d0ffff"
    ).grid(row=1, column=0, sticky="w")

    chatWindow.insert("end", "\n ", "tag-right")
    chatWindow.window_create("end", window=userFrame)


def create_and_insert_bot_frame(bot_response):
    botFrame = Frame(chatWindow, bg="#ffffd0")
    Label(
        botFrame,
        text=bot_response,
        font=("Arial", 11),
        bg="#ffffd0",
        wraplength=400,
        justify="left"
    ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

    Label(
        botFrame,
        text=datetime.now().strftime("%H:%M"),
        font=("Arial", 7),
        bg="#ffffd0"
    ).grid(row=1, column=0, sticky="w")

    chatWindow.insert("end", "\n ", "tag-left")
    chatWindow.window_create("end", window=botFrame)
    chatWindow.insert(END, "\n\n")

def send(event=None):
    chatWindow.config(state=NORMAL)

    user_input = userEntryBox.get("1.0", "end-2c").strip()
    if not user_input:
        chatWindow.config(state=DISABLED)
        return

    create_and_insert_user_frame(user_input)

    userEntryBox.delete("1.0", "end")
    chatWindow.see("end")

    typing_start = chatWindow.index("end-1c")
    create_and_insert_bot_frame("Bot is typing...")
    typing_end = chatWindow.index("end-1c")

    chatWindow.config(state=DISABLED)

    def worker():
        try:
            bot_response = get_bot_response(user_input)
        except Exception:
            bot_response = "Something went wrong while generating a response."

        def update_ui():
            chatWindow.config(state=NORMAL)

            chatWindow.delete(typing_start, typing_end)

            create_and_insert_bot_frame(bot_response)

            chatWindow.config(state=DISABLED)
            chatWindow.see("end")

        baseWindow.after(0, update_ui)

    threading.Thread(target=worker, daemon=True).start()


baseWindow = Tk()
baseWindow.title("The Simple Bot")
baseWindow.geometry("500x250")

chatWindow = tks.ScrolledText(baseWindow, font="Arial", wrap=WORD)

chatWindow.tag_configure("tag-left", justify="left")   
chatWindow.tag_configure("tag-right", justify="right") 

chatWindow.config(state=DISABLED)

userEntryBox = Text(baseWindow, bd=1, bg="white", width=38, font="Arial")

sendButton = Button(
    baseWindow,
    font=("Verdana", 12, "bold"),
    text="Send",
    bg="#fd94b4",
    activebackground="#ff467e",
    fg="#ffffff",
    command=send
)

baseWindow.bind("<Return>", send)

chatWindow.place(x=1, y=1, height=200, width=500)
userEntryBox.place(x=3, y=212, height=27)
sendButton.place(x=410, y=210)

baseWindow.mainloop()