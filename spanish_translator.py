###Code written by Liam & Capriana 
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
import pickle
import random
import torch
import torch.nn as nn
from torch.nn import functional as F

# Get the directory of the current Python file
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = current_dir + r'\models\BigramLanguageModel_s2.387702_it10000.pkl'

# model meta data for loading
block_size = 48 # what is the maximum context length for predictions?
device = 'cuda' if torch.cuda.is_available() else 'cpu'
chars = ['\r', ' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ª', '²', '³', 'µ', 'º', '¼', '½', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Ç', 'È', 'É', 'Ê', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', 'Ø', 'Ù', 'Ú', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'Ā', 'ā', 'ă', 'ą', 'ć', 'Č', 'č', 'ď', 'Đ', 'đ', 'ē', 'ė', 'ę', 'ě', 'ğ', 'ġ', 'Ħ', 'ħ', 'Ī', 'ī', 'ĭ', 'ı', 'ľ', 'Ł', 'ł', 'ń', 'ņ', 'ň', 'Ō', 'ō', 'ő', 'œ', 'ŕ', 'ř', 'Ś', 'ś', 'ŝ', 'Ş', 'ş', 'Š', 'š', 'ū', 'ů', 'ų', 'ź', 'Ż', 'ż', 'Ž', 'ž', 'ǎ', 'ǔ', 'ș', 'ə', 'ʾ', 'ː', 'Έ', 'Ό', 'Α', 'Β', 'Δ', 'Ε', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ο', 'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'ά', 'έ', 'ή', 'ί', 'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'ς', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω', 'ϊ', 'ό', 'ύ', 'ώ', 'А', 'Б', 'В', 'Г', 'Д', 'Ж', 'З', 'И', 'К', 'М', 'Н', 'О', 'П', 'Р', 'С', 'У', 'Ф', 'Х', 'Ч', 'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'я', 'ё', 'і', 'ј', 'ћ', 'Қ', 'қ', 'ң', 'ү', 'א', 'ה', 'י', 'ל', 'ם', 'ئ', 'ا', 'ب', 'ة', 'ت', 'ج', 'ح', 'د', 'ر', 'ز', 'س', 'ش', 'ص', 'ط', 'ع', 'ف', 'ق', 'ل', 'م', 'ن', 'ه', 'و', 'ى', 'ي', 'ڭ', 'ۇ', 'ۋ', 'ی', 'ې', 'क', 'ठ', 'न', 'फ', 'र', 'श', 'स', 'ক', 'ঠ', 'ন', 'র', 'শ', 'క', 'డ', 'న', 'พ', 'ศ', 'ᑦ', 'ᓂ', 'ᓄ', 'ᓇ', 'ᓴ', 'ᕗ', 'ᙱ', 'ḫ', 'Ṭ', 'ế', 'ồ', 'ἀ', 'Ἀ', 'Ἄ', 'ぁ', 'い', 'う', 'く', 'こ', 'た', 'つ', 'と', 'な', 'の', 'ふ', 'ゅ', 'り', 'る', 'を', 'イ', 'ウ', 'ォ', 'オ', 'キ', 'ゴ', 'サ', 'ザ', 'ジ', 'ス', 'ダ', 'ツ', 'ナ', 'ネ', 'ノ', 'ハ', 'パ', 'ビ', 'フ', 'ブ', 'ボ', 'マ', 'ム', 'ャ', 'ラ', 'リ', 'ル', 'レ', 'ロ', 'ン', 'ー', '一', '三', '丽', '仁', '会', '使', '全', '公', '六', '内', '初', '判', '医', '半', '华', '卜', '原', '古', '台', '和', '喜', '囲', '在', '地', '坤', '士', '多', '大', '天', '太', '奥', '妃', '妹', '字', '存', '学', '安', '完', '家', '密', '小', '峡', '島', '崎', '川', '巡', '工', '年', '彦', '彩', '彼', '徽', '心', '忠', '我', '戦', '戸', '抄', '报', '拳', '持', '政', '教', '数', '新', '旗', '早', '書', '望', '木', '村', '条', '東', '极', '楊', '歌', '氏', '洋', '流', '淀', '湾', '瀬', '炮', '爱', '独', '玉', '王', '現', '町', '界', '疆', '発', '目', '碁', '礼', '科', '秘', '竹', '紙', '統', '義', '色', '草', '荪', '薬', '藤', '袋', '論', '谷', '道', '郎', '鉄', '録', '長', '陽', '隊', '韓', '馬', '魔', '그', '년', '단', '도', '리', '맘', '반', '방', '소', '앵', '일', '탄', '통', '한', 'ﬁ']
vocab_size = len(chars)

# create a mapping from characters to integers
stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i,ch in enumerate(chars) }
encode = lambda s: [stoi[c] for c in s] # encoder: take a string, output a list of integers
decode = lambda l: ''.join([itos[i] for i in l]) # decoder: take a list of integers, output a string

class Head(nn.Module):
    """ one head of self-attention """

    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        B,T,C = x.shape
        k = self.key(x)   # (B,T,C)
        q = self.query(x) # (B,T,C)
        # compute attention scores ("affinities")
        wei = q @ k.transpose(-2,-1) * C**-0.5 # (B, T, C) @ (B, C, T) -> (B, T, T)
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf')) # (B, T, T)
        wei = F.softmax(wei, dim=-1) # (B, T, T)
        wei = self.dropout(wei)
        # perform the weighted aggregation of the values
        v = self.value(x) # (B,T,C)
        out = wei @ v # (B, T, T) @ (B, T, C) -> (B, T, C)
        return out

class MultiHeadAttention(nn.Module):
    """ multiple heads of self-attention in parallel """

    def __init__(self, num_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
        self.proj = nn.Linear(n_embd, n_embd)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.dropout(self.proj(out))
        return out

class FeedFoward(nn.Module):
    """ a simple linear layer followed by a non-linearity """

    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),
            nn.ReLU(),
            nn.Linear(4 * n_embd, n_embd),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        return self.net(x)

class Block(nn.Module):
    """ Transformer block: communication followed by computation """

    def __init__(self, n_embd, n_head):
        # n_embd: embedding dimension, n_head: the number of heads we'd like
        super().__init__()
        head_size = n_embd // n_head
        self.sa = MultiHeadAttention(n_head, head_size)
        self.ffwd = FeedFoward(n_embd)
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)

    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x

class BigramLanguageModel(nn.Module):

    def __init__(self):
        super().__init__()
        # each token directly reads off the logits for the next token from a lookup table
        self.token_embedding_table = nn.Embedding(vocab_size, n_embd)
        self.position_embedding_table = nn.Embedding(block_size, n_embd)
        self.blocks = nn.Sequential(*[Block(n_embd, n_head=n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd) # final layer norm
        self.lm_head = nn.Linear(n_embd, vocab_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape

        # idx and targets are both (B,T) tensor of integers
        tok_emb = self.token_embedding_table(idx) # (B,T,C)
        pos_emb = self.position_embedding_table(torch.arange(T, device=device)) # (T,C)
        x = tok_emb + pos_emb # (B,T,C)
        x = self.blocks(x) # (B,T,C)
        x = self.ln_f(x) # (B,T,C)
        logits = self.lm_head(x) # (B,T,vocab_size)

        if targets is None:
            loss = None
        else:
            B, T, C = logits.shape
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits, targets)

        return logits, loss

    def generate(self, idx, max_new_tokens):
        # idx is (B, T) array of indices in the current context
        for _ in range(max_new_tokens):
            # crop idx to the last block_size tokens
            idx_cond = idx[:, -block_size:]
            # get the predictions
            logits, loss = self(idx_cond)
            # focus only on the last time step
            logits = logits[:, -1, :] # becomes (B, C)
            # apply softmax to get probabilities
            probs = F.softmax(logits, dim=-1) # (B, C)
            # sample from the distribution
            idx_next = torch.multinomial(probs, num_samples=1) # (B, 1)
            # append sampled index to the running sequence
            idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)
        return idx

class model_loader():
    def __init__(self):
        with open(model_path, "rb") as file:
            model = pickle.load(file)

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.m = model.to(self.device)

    def generate_sample(self, prompt):
        # generate from the model
        context = torch.tensor([encode(prompt)], dtype=torch.long)
        return decode(self.m.generate(context, max_new_tokens=100)[0].tolist())

    def get_next_seg(self, prompt):
        # generate from the model
        context = torch.tensor([encode(prompt)], dtype=torch.long)
        seq = decode(self.m.generate(context, max_new_tokens=10)[0].tolist())
        print(seq)
        seq = seq[len(prompt):]
        lib = seq.split(" ")
        for tik in lib:
            if len(tik)<1:
                lib.remove(tik)
        return lib[0]

class AutocompleteGUI:

    def __init__(self):
        self.mLoader = model_loader()

    # Generates suggestions for the autocomplete GUI
    def send_message(self):
        # get the suggestions
        suggestions = self.get_autocomplete(6)

        # clear the suggestion buttons
        for btn in self.suggestion_buttons:
            btn.destroy()

        # create new suggestion buttons
        for suggestion in suggestions:
            btn = tk.Button(self.suggestions_frame, text=suggestion, command=lambda s=suggestion: self.append_suggestion(s), bg="#A1C6EA", relief="solid")
            btn.pack(side="left", padx=5)
            self.suggestion_buttons.append(btn)

    # Appends the clicked suggestion to the user entry
    def append_suggestion(self, suggestion):
        current_text = self.user_entry.get()
        self.user_entry.delete(0, tk.END)
        self.user_entry.insert(tk.END, current_text + " " + suggestion)

    # Inference the model and return the first word segment n times
    def get_autocomplete(self, n_completions):
        completions = []

        for i in range(n_completions):
            completion = self.mLoader.get_next_seg(self.user_entry.get())
            completions.append(completion)

        return completions

    # the tkinter instantiation code goes here
    def create_window(self):
        root = tk.Tk()
        root.title("Autocomplete: Spanish Helper")

        root.resizable(width=False, height=False)

        main_frame = tk.Frame(root, bg="#F5F5F5")
        main_frame.pack(fill="both", expand=True)

        self.suggestions_frame = tk.Frame(main_frame, bg="#F5F5F5")
        self.suggestions_frame.pack(side="top", fill="x", pady=10)
        self.suggestion_buttons = []

        input_frame = tk.Frame(main_frame, bg="#F5F5F5")
        input_frame.pack(side="bottom", fill="x", pady=10)

        self.user_entry = tk.Entry(input_frame, width=50, relief="solid")
        self.user_entry.pack(side="left", padx=10)
        send_button = tk.Button(input_frame,text="Get\nSuggestions", command=self.send_message, bg="#A1C6EA", relief="solid")
        send_button.pack(side="right", padx=10)

        root.mainloop()

gptMODEL = "gpt-3.5-turbo"

# Load the API-key
ext_key = ""

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

def auto_launch():
    autoBox = AutocompleteGUI()
    autoBox.create_window()

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
root.title("SpanAIsh")

w =1120  # window width 
h = 850  # window height

# get screen width and height
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for centering the window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (int(ws/3*2), int(hs/3*2), x, y))

# container for main GUI
main_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
main_frame.grid(row=0, column=0, sticky='NSEW')

# Create a Canvas widget
canvas = tk.Canvas(main_frame)
canvas.grid(row=0, column=0, sticky='NSEW')

# Create a Scrollbar widget
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky='ns')

# Configure the canvas to work with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Create a nested frame inside main_frame
nested_frame = ttk.Frame(canvas)

# Attach the nested frame to the canvas
canvas.create_window((0, 0), window=nested_frame, anchor='nw')

# Configure main_frame
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)
canvas.columnconfigure(0, weight=1)
canvas.rowconfigure(0, weight=1)

# Configure nested_frame
for i in range(11):
    nested_frame.rowconfigure(i, weight=1)  # Add weight to each row
nested_frame.columnconfigure(0, weight=1)  # Add weight only to the first column

# Attach the nested frame to the canvas
canvas.create_window((0, 0), window=nested_frame, anchor='nw', tags='nested_frame')  # Add tags attribute

def on_configure(event):
    canvas.itemconfigure('nested_frame', width=canvas.winfo_width())  # Set the width of the nested_frame to the canvas width

canvas.bind('<Configure>', on_configure)

# Your English Input
inputLabel = ttk.Label(nested_frame, text="Your English Input", font=("Helvetica", 11, "bold"), underline=0)
inputLabel.grid(row=0, column=0, padx=10, pady=5, sticky='W')

# User Input Object
input_entry = tk.Text(nested_frame, width=100, wrap='word', height=2) #2
input_entry.grid(row=1, column=0, padx=5, pady=0, ipadx=0, sticky='EW')

# Run the submit function * contains api call
submit_button = ttk.Button(nested_frame, text="Translate", command=on_submit, width=.5)
submit_button.grid(row=2, column=0, padx=0, pady=5, sticky='NSEW')

# where translations go
translation_label = ttk.Label(nested_frame, text="Translation", font=("Helvetica", 11, "bold"), underline=0)
translation_label.grid(row=3, column=0, padx=5, pady=5, sticky='W')
translation_entry = tkst.ScrolledText(nested_frame, wrap='word', state='disable', width=105, height=3) #3
translation_entry.grid(row=4, column=0, padx=5, pady=5, sticky='EW')

# where lessons go
breakdown_label = ttk.Label(nested_frame, text="Lesson", font=("Helvetica", 11, "bold"), underline=0)
breakdown_label.grid(row=5, column=0, padx=5, pady=5, sticky='W')
breakdown_entry = tkst.ScrolledText(nested_frame, wrap='word', state='disable', width=105, height=8) #8
breakdown_entry.grid(row=6, column=0, padx=5, pady=5, sticky='EW')

# where tense info goes
tense_label = ttk.Label(nested_frame, text="Tense", font=("Helvetica", 11, "bold"), underline=0)
tense_label.grid(row=7, column=0, padx=5, pady=5, sticky='W')
tense_entry = tkst.ScrolledText(nested_frame, wrap='word', state='disable', width=105, height=10) #12
tense_entry.grid(row=8, column=0, padx=5, pady=5, sticky='EW')

# open tutor chat box
tutor_button = tk.Button(nested_frame, text="Need Help? AI Tutor.", command=tutor_launch)
tutor_button.grid(row=9, column=0, padx=5, pady=5, sticky='EW')

# open tutor chat box
auto_button = tk.Button(nested_frame, text="Writing Assistant.", command=auto_launch)
auto_button.grid(row=10, column=0, padx=5, pady=5, sticky='EW')

# Update the scrollregion after the nested_frame is configured
nested_frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))


root.mainloop()