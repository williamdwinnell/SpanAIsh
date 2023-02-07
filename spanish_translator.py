import openai

import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import ttk
from tkinter import filedialog

gptMODEL = "text-curie-001"#"text-davinci-002" #text-curie-001
gptMODEL = "text-davinci-003"

def get_translation(inputLabel, explanation=False):
    if explanation==True:
        prompt = "\n\nTranslate the sentence to Spanish (labelled Translation: ), then do a break down explanation (label it Break Down: ) teaching the translation. Lastly, identify the tense of the translation, as one of the following (Present, Past, Future, Imperfect, Pluperfect, Conditional, Present Perfect, Past Perfect, Future Perfect, Conditional Perfect, Subjunctive, Present Subjunctive, Imperfect Subjunctive, Future Subjunctive, Present Perfect Subjunctive, Preterite Perfect or Past Anterior)."
    else:
        prompt = "\n\nTranslate the sentence to Spanish."
    
    response = openai.Completion.create(
    engine=gptMODEL,
    prompt= "Input:\n" + inputLabel + prompt,
    temperature=0.45,
    max_tokens=225,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    response = response['choices'][0]['text']
    return response

#activate api_key
openai.api_key = "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"

def on_submit():

    disp_string = get_translation(input_entry.get(), explanation=True)

    answer_text.config(state='normal') # Enable edition of the text area
    answer_text.delete(1.0, tk.END)
    answer_text.insert(tk.INSERT, disp_string)
    answer_text.config(state='disabled') # Disable edition of the text area

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", root.quit)
root.geometry("960x600") # set window size
root.title("Question Answering")

root.columnconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

inputLabel = ttk.Label(root, text="English: ")
inputLabel.grid(row=0, column=0, padx=5, pady=5,sticky='W')

input_entry = ttk.Entry(root,width=85)
input_entry.grid(row=0, column=1, padx=5, pady=5,ipadx=0,sticky='NSEW')


submit_button = ttk.Button(root, text="Submit", command=on_submit)
submit_button.grid(row=0, column=2, padx=15, pady=5, sticky='W')

answer_text = tkst.ScrolledText(root, wrap='word', state='disable', width=110, height=29) # use ScrolledText widget to have a scrollable text
answer_text.grid(row=2, column=0, columnspan=3, padx=5, pady=5,sticky='NSEW')

root.mainloop()