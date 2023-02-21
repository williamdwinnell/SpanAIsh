###Code written by Liam & Capryiana 
### add lesson recommendations using a special classifier 
### 
import openai
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import ttk
from win32 import win32clipboard
import os 


gptMODEL = "text-curie-001"#"text-davinci-002" #text-curie-001
gptMODEL = "text-davinci-003"

# Load the API-key
ext_key = ""

# Get the directory of the current Python file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the text file and read the first line
with open(os.path.join(current_dir, "key.txt"), "r") as file:
    ext_key = file.readline()


def emoji_img(size, text):
    font = ImageFont.truetype("seguiemj.ttf", size=int(round(size*72/96, 0))) 
    # pixels = points * 96 / 72 : 96 is windowsDPI
    im = Image.new("RGBA", (int(size), int(size)), (255, 255, 255, 0))
    draw = ImageDraw.Draw(im)
    draw.text((int(size/2), int(size/2)), text, embedded_color=True, font=font, anchor="mm")
    return ImageTk.PhotoImage(im)

def get_translation(inputLabel, explanation=False):
    if explanation==True:
        #prompt = "\n\nTranslate the sentence to Spanish (labelled Translation: ), then do a break down explanation (label it Break Down: ) teaching the translation. Lastly, identify the tense of the translation, as one of the following (Present, Past, Future, Imperfect, Pluperfect, Conditional, Present Perfect, Past Perfect, Future Perfect, Conditional Perfect, Subjunctive, Present Subjunctive, Imperfect Subjunctive, Future Subjunctive, Present Perfect Subjunctive, Preterite Perfect or Past Anterior)."
        prompt = "\n\nTranslate the sentence to Spanish (labelled Translation: ), then do a break down explanation in a list format (label it Break Down: ) with the goal of teaching the concepts of the translation. Then, identify the tense of the translation (Tense:) Make sure the tense is written in english."
        if emoji_var.get() == 1:
            prompt = "\n\nTranslate the sentence to Spanish and include an educational emojis for every word in the translation (labelled Translation: ), then do a break down explanation in a list format (label it Break Down: ) with the goal of teaching the concepts of the translation. Then, identify the tense of the translation (Tense:) Make sure the tense is written in english."
        
    response = openai.Completion.create(
    engine=gptMODEL,
    prompt= "Input:\n" + inputLabel + prompt,
    temperature=0.65,
    max_tokens=300,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    response = response['choices'][0]['text']

    return response

#activate api_key
openai.api_key = ext_key

def on_submit():

    disp_string = get_translation(input_entry.get(), explanation=True)
    
    translation_entry.config(state='normal') # Enable edition of the text area
    translation_entry.delete(1.0, tk.END)
    translation_entry.insert(tk.INSERT, disp_string.split("Translation:")[1].split("Break Down:")[0])
    translation_entry.config(state='disabled') # Disable edition of the text area

    breakdown_entry.config(state='normal') # Enable edition of the text area
    breakdown_entry.delete(1.0, tk.END)
    breakdown_entry.insert(tk.INSERT, disp_string.split("Break Down:")[1].split("Tense:")[0])
    breakdown_entry.config(state='disabled') # Disable edition of the text area

    tense_entry.config(state='normal') # Enable edition of the text area
    tense_entry.delete(1.0, tk.END)
    tense_entry.insert(tk.INSERT, disp_string.split("Break Down:")[1].split("Tense:")[1])
    tense_entry.config(state='disabled') # Disable edition of the text area

def on_explain():
    return 0

def on_example():
    return 0
'''
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", root.quit)
root.geometry("960x600") # set window size
root.title("SpanAI")

root.columnconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

inputLabel = ttk.Label(root, text="English: ")
inputLabel.grid(row=0, column=0, padx=5, pady=5,sticky='W')

input_entry = ttk.Entry(root,width=85)
input_entry.grid(row=0, column=1, padx=5, pady=5,ipadx=0,sticky='NSEW')


submit_button = ttk.Button(root, text="Submit", command=on_submit)
submit_button.grid(row=0, column=2, padx=15, pady=5, sticky='W')

answer_text = tkst.ScrolledText(root, wrap='word', state='disable', width=110, height=29) # use ScrolledText widget to have a scrollable text
answer_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5,sticky='NSEW')
'''

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", root.quit)
root.geometry("960x580") # set window size
root.title("SpanAI")

#root.columnconfigure(1, weight=1)
#root.rowconfigure(2, weight=1)

root.columnconfigure(0, weight=1)
#root.columnconfigure(1, weight=1)

inputLabel = ttk.Label(root, text="English: ")
inputLabel.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')

input_entry = ttk.Entry(root, width=100)
input_entry.grid(row=1, column=0, padx=5, pady=5, ipadx=0, sticky='EW')

submit_button = ttk.Button(root, text="Submit", command=on_submit)
submit_button.grid(row=2, column=0, padx=5, pady=5, sticky='NSEW')

translation_label = ttk.Label(root, text="Translation:")
translation_label.grid(row=3, column=0, padx=5, pady=5, sticky='NSEW')
translation_entry = tkst.ScrolledText(root, wrap='word', state='disable', width=105, height=3)
translation_entry.grid(row=4, column=0, padx=5, pady=5, sticky='EW')

breakdown_label = ttk.Label(root, text="Break Down:")
breakdown_label.grid(row=5, column=0, padx=5, pady=5, sticky='NSEW')
breakdown_entry = tkst.ScrolledText(root, wrap='word', state='disable', width=105, height=12)
breakdown_entry.grid(row=6, column=0, padx=5, pady=5, sticky='EW')

tense_label = ttk.Label(root, text="Tense:")
tense_label.grid(row=7, column=0, padx=5, pady=5, sticky='NSEW')
tense_entry = tkst.ScrolledText(root, wrap='word', state='disable', width=40, height=1)
tense_entry.grid(row=8, column=0, padx=5, pady=5, sticky='EW')

# create the "emoji translation" checkbox
emoji_var = tk.IntVar()
emoji_checkbox = ttk.Checkbutton(root, text="Emoji Translation", variable=emoji_var)
emoji_checkbox.grid(row=9, column=0, padx=5, pady=5, sticky='W')

# create the "simplify" checkbox
simplify_var = tk.IntVar()
simplify_checkbox = ttk.Checkbutton(root, text="Simplify", variable=simplify_var)
simplify_checkbox.grid(row=9, column=0, padx=135, pady=5, sticky='W')


root.mainloop()