from initializer import appinitializer
initial = appinitializer()
import shutil
from tkinter import filedialog, messagebox
from tkinter.ttk import Notebook
from gtts import gTTS
import os
import random
from tkinter import *
from pygame import mixer  # Load the popular external library


import setting
import importlib



mixer.init()

times = 0
score = 0

def open_all():
    importlib.reload(setting)
    global sentences
    file = open(setting.file_location)
    sentences = list(file.readlines())

def get_random_sentence():
    open_all()
    num = random.randint(0, len(sentences))
    try:
        rnd = sentences[num]
    except IndexError:
        messagebox.askretrycancel("Cannot load sentences", message="Cannot load sentences, reload?")
    return rnd, num

def generate_sound():
    mytext, num= get_random_sentence()
    language = "en"
    myobj = gTTS(text=mytext, lang=language, slow=False)
    try:
        myobj.save(os.getcwd()+"\\sound\\"+ str(num)+".mp3")
    except:
        pass
    return mytext, num

class autoE(Entry):
    """please don't make fontcolor same to placecolor"""
    def __init__(self, parent, placeholder=None, placecolor='gray', fontcolor='black', only=['None', 'Num', 'Text'], limit=int, space=True, quote=True, **arg):
        Entry.__init__(self, parent, fg=placecolor, **arg)
        self.bind("<Button-1>", self.click)
        self.bind("<FocusOut>", self.out)
        self.bind("<KeyRelease>", self.check, add="+")
        self.ph = placeholder
        self.fontc = fontcolor
        self.only = only
        self.limit = limit
        
        self.num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.text = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.quote = """[ ! @ # $ % ^ & * ( ) , . / < > ? ; ' \ : ` ~ - = _ +"""
        if space:
            self.num.append(' ')
            self.text.append(' ')
        if quote:
            self.num.extend(self.quote.split(' '))
            self.text.extend(self.quote.split(' ')) 
        self.placecolor = placecolor
        self.insert(END, self.ph)

    def click(self, e):
        if self.get() == self.ph and self['fg'] == self.placecolor:
            self.delete(0, END)
            self['fg'] = self.fontc
    
    def out(self, e):
        if not self.get():
            self['fg'] = self.placecolor
            self.insert(END, self.ph)
    
    def check(self, e):
        s = ''
        if self.only == 'Num':
            
            for w in self.get():
                if w in self.num:
                    s += w
            try:
                s = s[:self.limit]
            except TypeError:
                pass
            self.delete(0, END)
            self.insert(END, s)
        elif self.only == 'Text':
            for w in self.get():
                if w in self.text:
                    s += w
            try:
                s = s[:self.limit]
            except TypeError:
                pass
            self.delete(0, END)
            self.insert(END, s)
            return

root= Tk()
# all_file = []
# root.geometry("630x200")


def lis(e=False):
    global soundfile
    mixer.music.load(soundfile)
    mixer.music.play()
    # mixer.music.stop()

def firstrun(e=True):
    global soundfile, textline, answer, submit
        # except FileNotFoundError:
        #     pass
    try:
        submit["state"] = "normal"
    except NameError:
        pass
    if not e:
        if answer["foreground"] == "red" or answer["foreground"] == "green" or answer["foreground"] == "black":
            answer.delete(0, END)
        answer.grid(row=1, column=0, padx=10, pady=20, ipadx=5, ipady=5, columnspan=13)
        correcttext['text'] = ""
        root.focus()
    text, num = generate_sound()
    soundfile = os.getcwd()+"\\sound\\"+ str(num)+".mp3"
    # all_file.append(soundfile)
    textline = text.strip()

open_all()
firstrun()

def check(e=None):
    global soundfile, textline, times, score, submit, correcttext
    ans = answer.get()
    times += 1
    if str(ans).strip() == textline:
        answer["foreground"] = "green"
        score += 1
        scores["text"] = "You got " + str(score) + " out of " + str(times) + " correct!"
    else:
        correcttext["text"] = textline
        answer["foreground"] = "red"
        scores["text"] = "You got " + str(score) + " out of " + str(times) + " correct!"
    
    submit["state"] = "disabled"

def select_file(e):

    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        filetypes=filetypes)

    if filename == "" or not filename:
        filename = setting.file_location

    messagebox.showinfo(
        title='Selected File',
        message=filename
    )
    newset = open(os.getcwd()+"\\setting.py", "w")
    newset.write(f"""file_location=\"{filename}\"""")
    location["text"] = filename

def on_closing():
    root.destroy()
    try:
        shutil.rmtree(os.getcwd()+"\\sound")
    except:
        pass

def clear_sound_folder():
    root.protocol("WM_DELETE_WINDOW", on_closing)

def open_setting():
    importlib.reload(setting)
    global location
    set_win = Toplevel()
    set_win.geometry("300x200")
    tabs = Notebook(set_win)
    info_page = Frame(tabs)
    set_page = Frame(tabs)
    tabs.add(info_page, text="     Info     ")
    tabs.add(set_page, text="     Setting     ")
    tabs.pack(fill=BOTH, expand=True)
    
    infos = "\nHello user!\n\nYou can change the sentence database by \nchanging the file location in the setting menu.\n\nHowever, the file must be a .txt file\n\nAlso, you can clear the sound folder by\nclicking on the button to reduce some size."
    inform = Label(info_page, text=infos, font=["arial", "10"])
    inform.pack()

    sett = Label(set_page, text="File:")
    location = Label(set_page, text=setting.file_location)
    clear_sound = Button(set_page, text="Clear sound files", command=lambda: clear_sound_folder())

    sett.grid(row=0, column=0, padx=10, pady=10)
    location.grid(row=0, column=1, padx=10, pady=10)
    clear_sound.grid(row=1, columnspan=2)

    location.bind("<Button-1>", select_file)
    pass

menubar = Menu(root, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')
file = Menu(menubar, tearoff=0, foreground='black')  
file.add_command(label="settings", command=open_setting)  

menubar.add_cascade(label="File", menu=file)  

photo = PhotoImage(file = "voice.png").subsample(32) 
photo_2 = PhotoImage(file = "submit.png").subsample(7)
photo_3 = PhotoImage(file = "next.png").subsample(7)
# Add image to button




listen_b = Button(root, image=photo, command=lambda: lis(), highlightthickness = 0, bd = 0)
answer = autoE(root, "What did you hear?", width=100, font=["arial", "12"])
submit = Button(root, image=photo_2, command=lambda: check(), highlightthickness = 0, bd = 0)
next_b = Button(root, image=photo_3, command=lambda: firstrun(False), highlightthickness = 0, bd = 0)
answerframe = Frame(root)
correcttext = Label(answerframe, text="")
scores = Label(answerframe, text="")

listen_b.grid(row=0, column=0, padx=10, pady=10, columnspan=13)
answer.grid(row=1, column=0, padx=10, pady=20, ipadx=5, ipady=5, columnspan=13)
submit.grid(row=2, column=11, padx=10, pady=10)
next_b.grid(row=2, column=12, padx=10, pady=10)
answerframe.grid(row=3, column=0, columnspan=13, padx=10, pady=10)
correcttext.pack(padx=10, pady=10)
scores.pack(padx=10, pady=10)

# root.protocol("WM_DELETE_WINDOW", on_closing)
root.config(menu=menubar)
root.mainloop()
