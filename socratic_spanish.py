'''
# System rules
Do not answer your own questions. 
Only teach using the Socratic method, giving help when needed. 
When the user is uncertain, present the answer as a multiple choice question to help them learn. Otherwise, never give the user the answer, and only teach socratically.
Teach Spanish.
Do not provide any translations when phrasing your questions, only provide translations when the user is uncertain.
'''

import tkinter as tk
from tkinter import messagebox as mb
import openai
import os
gptMODEL = "gpt-3.5-turbo"
# Load the API-key
ext_key = ""

# Get the directory of the current Python file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the text file and read the first line
with open(os.path.join(current_dir, "key.txt"), "r") as file:
    ext_key = file.readline()

class SocraticChatBox:

    def __init__(self):
        self.messages = []

    def send_message(self):
        user_message = self.user_entry.get()
        self.messages.append(user_message)
        self.user_entry.delete(0, tk.END)

        user_message_frame = tk.Frame(self.messages_inner_frame, bg="#F5F5F5")
        user_message_frame.pack(anchor="w", pady=5)

        user_message_label = tk.Label(user_message_frame, text=user_message, bg="#A1C6EA", wraplength=400, justify="left", relief="solid")
        user_message_label.pack(anchor="w", padx=10)

        response_message_frame = tk.Frame(self.messages_inner_frame, bg="#F5F5F5")
        response_message_frame.pack(anchor="w", pady=5)

        response_message = self.get_response_turbo()
        self.messages.append(response_message)
        response_message_label = tk.Label(response_message_frame, text=response_message, bg="#EAEAEA", wraplength=400, justify="left", relief="solid")
        response_message_label.pack(anchor="w", padx=10)

        self.messages_frame.update_idletasks()
        self.messages_frame.configure(scrollregion=self.messages_frame.bbox("all"))
        self.messages_frame.yview_moveto(1)

    def get_response_turbo(self):
        system = """Do not answer your own questions. 
        Only teach using the Socratic method, giving help when needed. 
        When the user is uncertain, present the answer as a multiple choice question to help them learn. 
        Otherwise, never give the user the answer, and only teach socratically. 
        Speak in English when teaching spanish. 
        Do not provide any translations when phrasing your questions, only provide translations when the user is uncertain."""
        mod_msg = [{"role": "system", "content": system}]
        for i in range(len(self.messages)):
            if i % 2 == 0 or i == 0:
                mod_msg.append({"role": "user", "content": self.messages[i]})
            else:
                mod_msg.append({"role": "assistant", "content": self.messages[i]})
        print(mod_msg)
        response = openai.ChatCompletion.create(model="gpt-4", 
                                                messages=mod_msg) 
        response = response.choices[0].message.content
        return response

    def create_window(self):
        root = tk.Tk()
        root.title("Socratic Tutor.")

        root.resizable(width=False, height=False)

        main_frame = tk.Frame(root, bg="#F5F5F5")
        main_frame.pack(expand=True, fill="both")

        self.messages_frame = tk.Canvas(main_frame, bg="#F5F5F5")
        self.messages_frame.pack(expand=True, fill="both")

        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=self.messages_frame.yview)
        scrollbar.pack(side="right", fill="y")

        self.messages_frame.configure(yscrollcommand=scrollbar.set)

        self.messages_inner_frame = tk.Frame(self.messages_frame, bg="#F5F5F5")
        self.messages_frame.create_window((0, 0), window=self.messages_inner_frame, anchor="ne")

        input_frame = tk.Frame(main_frame, bg="#F5F5F5")
        input_frame.pack(side="bottom", fill="x", pady=10)

        self.user_entry = tk.Entry(input_frame, width=50, relief="solid")
        self.user_entry.pack(side="left", padx=10)
        self.user_entry.insert(0, "Ex: Teach me how to order tacos at a mexican restaurant.")

        send_button = tk.Button(input_frame,text="Send", command=self.send_message, bg="#A1C6EA", relief="solid")
        send_button.pack(side="right", padx=10)

        root.mainloop()

        

#chatBox = SocraticChatBox()
#chatBox.create_window()