import tkinter as tk
from tkinter import scrolledtext
import openai
import os


# Get the directory of the current Python file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the API-key
ext_key = ""

# Load the text file and read the first line
with open(os.path.join(current_dir, "key.txt"), "r") as file:
    ext_key = file.readline()

#activate api_key
openai.api_key = ext_key

def get_lesson_turbo(inputLabel):
    prompt = "The user is going to try to translate the english input. Write a list of hints to help them translate the input into Spanish. Also include the translations of the less known vocabulary from the input sentence and label it `Less Know Vocabulary:`."
    response = openai.ChatCompletion.create(model="gpt-4", 
                                              messages=[{"role": "system", "content": prompt},
                                                        {"role": "user", "content": "Input:\n" + inputLabel}]) 
    response = response.choices[0].message.content
    return response

def get_feedback(inputLabel, englishText):
    system = "Are there any mistakes in the user translation of the english text into spanish? If not, say good job. If so, choose one mistake that the user made and write a lesson that teaches about that mistake without specifically fixing it for them. The goal is to get them to learn so that they can then try to fix it themself. (Keep in mind if there is english in their spanish response, they probably do not know the Spanish and you need to teach a lesson to help them know.)"
    user = "English Text: " + englishText + "\n" + "User's Spanish Translation Attempt: " + inputLabel

    response = openai.ChatCompletion.create(model="gpt-4", 
                                              messages=[{"role": "system", "content": system},
                                                        {"role": "user", "content": user}]) 
    response = response.choices[0].message.content
    return response

class SpanishTranslatorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Educational Spanish Translator")
        self.geometry("700x700")

        self.create_widgets()

    def create_widgets(self):
        width = 160
        self.input_label = tk.Label(self, text="Enter your sentence\nTo learn in Spanish")
        self.input_label.grid(row=0, column=0, padx=10, pady=10)

        self.input_text = tk.Text(self, width=width, height=2)
        self.input_text.grid(row=0, column=1, padx=10, pady=10)

        self.translate_button = tk.Button(self, text="Get Lesson", command=self.translate)
        self.translate_button.grid(row=1, column=1, padx=10, pady=10)

        self.lesson_label = tk.Label(self, text="Lesson")
        self.lesson_label.grid(row=2, column=0, padx=10, pady=10)

        self.lesson_text = scrolledtext.ScrolledText(self, wrap='word', state='disable', width=width, height=10)
        self.lesson_text.grid(row=2, column=1, padx=10, pady=10)

        self.output_label = tk.Label(self, text="Your Translation\nAttempt")
        self.output_label.grid(row=3, column=0, padx=10, pady=10)

        self.output_text = tk.Text(self, width=width, height=2)
        self.output_text.grid(row=3, column=1, padx=10, pady=10)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=4, column=1, padx=10, pady=10)

        self.feedback_label = tk.Label(self, text="Feedback")
        self.feedback_label.grid(row=5, column=0, padx=10, pady=10)

        self.feedback_text = scrolledtext.ScrolledText(self, wrap='word', state='disable', width=width, height=10)
        self.feedback_text.grid(row=5, column=1, padx=10, pady=10)

        self.columnconfigure(1, weight=1)
        for i in range(5):
            self.rowconfigure(i, weight=1)

    def translate(self):
        lesson = get_lesson_turbo(self.input_text.get("1.0", "end-1c"))
        print(lesson)
        self.lesson_text.config(state='normal') 
        self.lesson_text.delete(1.0, tk.END)
        self.lesson_text.insert(tk.INSERT, lesson)
        self.lesson_text.config(state='disabled')

    def submit(self):
        englishText = self.input_text.get("1.0", "end-1c")
        spanishTranslation = self.output_text.get("1.0", "end-1c")
        feedback=get_feedback(spanishTranslation, englishText)
        print(feedback)
        self.feedback_text.config(state='normal') 
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.INSERT, feedback)
        self.feedback_text.config(state='disabled')

if __name__ == "__main__":
    app = SpanishTranslatorApp()
    app.mainloop()