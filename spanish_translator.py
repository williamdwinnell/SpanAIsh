###Code written by Liam & Capryiana 
### 

# api imports
import openai

# gui imports
import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import ttk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

# local imports 
import tenses_data
import socratic_spanish

# other imports
import os 

gptMODEL = "gpt-3.5-turbo"

# Load the API-key
ext_key = ""

# Get the directory of the current Python file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the text file and read the first line
with open(os.path.join(current_dir, "key.txt"), "r") as file:
    ext_key = file.readline()

def get_translation_turbo(inputLabel):
    prompt = "Translate the user's sentence to Spanish (Translation:). Next, write a spanish lesson (in English) teaching the key concepts from the translation, as if you were a spanish teacher. The lesson should be formatted as an ordered list that is 5 points long or less. (Lesson:). Lastly, identify the tense of the translation (Tense:) Make sure the tense is written in English and to label preterite vs imperfect correctly when needed, do not just say past tense."
    
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                              messages=[{"role": "system", "content": prompt},
                                                        {"role": "user", "content": "Input:\n" + inputLabel}]) 
    response = response.choices[0].message.content
    return response

#activate api_key
openai.api_key = ext_key
def tutor_launch():
    chatBox = socratic_spanish.SocraticChatBox()
    chatBox.create_window()

def on_submit():

    # The possible sections in the model output
    parsers = ["Translation:", "Lesson:", "Tense:"]
    entry = input_entry.get("1.0", "end-1c")

    # Limit the input length to a couple of sentences, as a security measure
    if len(entry) > 150:
        mb.showerror(title = "Your input is too long.", message = "Please try a shorter translation.")
    else:
        # Gets the translation from the user's input.
        disp_string = get_translation_turbo(input_entry.get("1.0", "end-1c"))
        
        # Get the translation from the output
        translation_entry.config(state='normal')
        translation_entry.delete(1.0, tk.END)
        disp_translation = disp_string.split(parsers[0])[1].split(parsers[1])[0]
        translation_entry.insert(tk.INSERT, disp_translation)
        translation_entry.config(state='disabled')

        # Get the lesson/breakdown from the output
        breakdown_entry.config(state='normal') 
        breakdown_entry.delete(1.0, tk.END)
        disp_lesson = disp_string.split(parsers[1])[1].split(parsers[2])[0]
        breakdown_entry.insert(tk.INSERT, disp_lesson)
        breakdown_entry.config(state='disabled')

        # Get the tense from the output and display it
        tense_entry.config(state='normal')
        tense_entry.delete(1.0, tk.END)
        disp_tense = disp_string.split(parsers[1])[1].split(parsers[2])[1]

        # Search for any tenses from the dict of tenses 
        index = -1
        for key in tenses_data.lowercase_keys:
            if key in disp_tense.lower():
                index = tenses_data.lowercase_keys.index(key)
        if index != -1:
            disp_tense += "\n\n"
            disp_tense += tenses_data.tenses[tenses_data.keys[index]]

        # Display the tense with or without the dict
        tense_entry.insert(tk.INSERT, disp_tense)
        tense_entry.config(state='disabled')

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", root.quit)
root.title("SpanAI")

w =1120  # window width 
h = 800  # window height

# get screen width and height
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for centering the window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.columnconfigure(0, weight=1)

# container for main GUI
main_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
main_frame.grid(row=0, column=0, sticky='NSEW')

# Your English Input
inputLabel = ttk.Label(main_frame, text="Your English Input", font=("Helvetica", 11, "bold"), underline=0)
inputLabel.grid(row=0, column=0, padx=10, pady=5, sticky='W')

# User Input Object
input_entry = tk.Text(main_frame, height=2, width=100, wrap='word')
input_entry.grid(row=1, column=0, padx=5, pady=0, ipadx=0, sticky='EW')

# Run the submit function * contains api call
submit_button = ttk.Button(main_frame, text="Translate", command=on_submit, width=.5)
submit_button.grid(row=2, column=0, padx=0, pady=5, sticky='NSEW')

# where translations go
translation_label = ttk.Label(main_frame, text="Translation", font=("Helvetica", 11, "bold"), underline=0)
translation_label.grid(row=3, column=0, padx=5, pady=5, sticky='W')
translation_entry = tkst.ScrolledText(main_frame, wrap='word', state='disable', width=105, height=3)
translation_entry.grid(row=4, column=0, padx=5, pady=5, sticky='EW')

# where lessons go
breakdown_label = ttk.Label(main_frame, text="Lesson", font=("Helvetica", 11, "bold"), underline=0)
breakdown_label.grid(row=5, column=0, padx=5, pady=5, sticky='W')
breakdown_entry = tkst.ScrolledText(main_frame, wrap='word', state='disable', width=105, height=8)
breakdown_entry.grid(row=6, column=0, padx=5, pady=5, sticky='EW')

# where tense info goes
tense_label = ttk.Label(main_frame, text="Tense", font=("Helvetica", 11, "bold"), underline=0)
tense_label.grid(row=7, column=0, padx=5, pady=5, sticky='W')
tense_entry = tkst.ScrolledText(main_frame, wrap='word', state='disable', width=105, height=12)
tense_entry.grid(row=8, column=0, padx=5, pady=5, sticky='EW')

# open tutor chat box
tutor_button = tk.Button(main_frame, text="Need Help? AI Tutor.", command=tutor_launch)
tutor_button.grid(row=9, column=0, padx=5, pady=5, sticky='EW')

root.mainloop()