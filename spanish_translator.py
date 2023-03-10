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
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

gptMODEL = "gpt-3.5-turbo"
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

def get_translation_turbo(inputLabel):
    #prompt = "Translate the user's sentence to Spanish (Translation:), then do a break down explanation in a list format (Break Down:) with the goal of teaching the concepts of the translation. Lastly, identify the tense of the translation (Tense:) Make sure the tense is written in English."
    #prompt = "Translate the user's sentence to Spanish (Translation:), then do a break down explanation in a list format (Break Down:) where you teach the concepts behind the translation to Spanish, like a teacher would. Lastly, identify the tense of the translation (Tense:) Make sure the tense is written in English."
    prompt = "Translate the user's sentence to Spanish (Translation:). Next, write a spanish lesson teaching the translation in depth, as if you were a spanish teacher. The lesson should be formatted as an ordered list that is 5 points long or less. (Lesson:). Lastly, identify the tense of the translation (Tense:) Make sure the tense is written in English."

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                              messages=[{"role": "system", "content": prompt},
                                                        {"role": "user", "content": "Input:\n" + inputLabel}]) 
    response = response.choices[0].message.content
    return response

#activate api_key
openai.api_key = ext_key

def on_submit():

    #parsers = ["Translation:", "Break Down:", "Tense:"]
    parsers = ["Translation:", "Lesson:", "Tense:"]
    entry = input_entry.get("1.0", "end-1c")
    if len(entry) > 150:
        mb.showerror(title = "Your input is too long.", message = "Please try a shorter translation.")
    else:
        disp_string = get_translation_turbo(input_entry.get("1.0", "end-1c"))
        
        translation_entry.config(state='normal') # Enable edition of the text area
        translation_entry.delete(1.0, tk.END)
        translation_entry.insert(tk.INSERT, disp_string.split(parsers[0])[1].split(parsers[1])[0])
        translation_entry.config(state='disabled') # Disable edition of the text area

        breakdown_entry.config(state='normal') # Enable edition of the text area
        breakdown_entry.delete(1.0, tk.END)
        breakdown_entry.insert(tk.INSERT, disp_string.split(parsers[1])[1].split(parsers[2])[0])
        breakdown_entry.config(state='disabled') # Disable edition of the text area

        tense_entry.config(state='normal') # Enable edition of the text area
        tense_entry.delete(1.0, tk.END)
        tense_entry.insert(tk.INSERT, disp_string.split(parsers[1])[1].split(parsers[2])[1])
        tense_entry.config(state='disabled') # Disable edition of the text area

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", root.quit)
root.title("SpanAI")

w = 960 # width for the Tk root
h = 580 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.columnconfigure(0, weight=1)

inputLabel = ttk.Label(root, text="English: ")
inputLabel.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')

input_entry = tk.Text(root, height=2, width=100)
input_entry.grid(row=1, column=0, padx=5, pady=5, ipadx=0, sticky='EW')

submit_button = ttk.Button(root, text="Translate", command=on_submit, width=.5)
submit_button.grid(row=2, column=0, padx=0, pady=0, sticky='NSEW')

translation_label = ttk.Label(root, text="Translation")
translation_label.grid(row=3, column=0, padx=5, pady=5, sticky='NSEW')
translation_entry = tkst.ScrolledText(root, wrap='word', state='disable', width=105, height=3)
translation_entry.grid(row=4, column=0, padx=5, pady=5, sticky='EW')

breakdown_label = ttk.Label(root, text="Lesson")
breakdown_label.grid(row=5, column=0, padx=5, pady=5, sticky='NSEW')
breakdown_entry = tkst.ScrolledText(root, wrap='word', state='disable', width=105, height=12)
breakdown_entry.grid(row=6, column=0, padx=5, pady=5, sticky='EW')

tense_label = ttk.Label(root, text="Tense")
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