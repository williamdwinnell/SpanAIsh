import tkinter as tk
from tkinter import messagebox as mb
import os
import pickle
import random
import torch
import torch.nn as nn
from torch.nn import functional as F

# Get the directory of the current Python file
current_dir = str(os.path.dirname(os.path.abspath(__file__)))
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
        # stores the message history
        #self.messages = []
        self.mLoader = model_loader()

    # when the send button is pressed this function is run
    def send_message(self):
        # get the suggestions
        suggestions = self.get_autocomplete(5)

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
        self.user_entry.insert(tk.END, current_text + suggestion)

    # Generates the next word for the user entry
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

autoGUI = AutocompleteGUI()
autoGUI.create_window()