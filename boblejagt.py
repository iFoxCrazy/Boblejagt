import json
from tkinter import *
from math import sqrt
from random import randint
from time import sleep, time

# Spilparametre
HEIGHT = 500
WIDTH = 800
UBAAD_R = 15
UBAAD_FART = 10
GAB = 100
MIN_BOB_R = 10
MAX_BOB_R = 30
MAX_BOB_FART = 10
BOB_CHANCE = 10
TIDSFRIST = 30
BONUS_SCORE = 1000
HIGH_SCORE_FILE = "high_scores.json"

# Start på Tkinter vindue
window = Tk()
window.title('Boblejagt')
l = Canvas(window, width=WIDTH, height=HEIGHT, bg='darkblue')
l.pack()

# Oprettelse af ubåd
ubaad_id = l.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
ubaad_id2 = l.create_polygon(0, 0, 30, 30, outline='red')
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
l.move(ubaad_id, MID_X, MID_Y)
l.move(ubaad_id2, MID_X, MID_Y)

# Bevægelse af ubåd
def flyt_ubaad(event):
    if event.keysym == 'Up':
        l.move(ubaad_id, 0, -UBAAD_FART)
        l.move(ubaad_id2, 0, -UBAAD_FART)
    elif event.keysym == 'Down':
        l.move(ubaad_id, 0, UBAAD_FART)
        l.move(ubaad_id2, 0, UBAAD_FART)
    elif event.keysym == 'Left':
        l.move(ubaad_id, -UBAAD_FART, 0)
        l.move(ubaad_id2, -UBAAD_FART, 0)
    elif event.keysym == 'Right':
        l.move(ubaad_id, UBAAD_FART, 0)
        l.move(ubaad_id2, UBAAD_FART, 0)

l.bind_all('<Key>', flyt_ubaad)

# Spiltilstande
score = 0
bonus = 0
slut = time() + TIDSFRIST

# Liste til bobler
bob_id = list()
bob_r = list()
bob_fart = list()

# Funktioner til bobler
def lav_boble():
    x = WIDTH + GAB
    y = randint(0, HEIGHT)
    r = randint(MIN_BOB_R, MAX_BOB_R)
    id1 = l.create_oval(x - r, y - r, x + r, y + r, outline='white')
    bob_id.append(id1)
    bob_r.append(r)
    bob_fart.append(randint(1, MAX_BOB_FART))

def flyt_bobler():
    for i in range(len(bob_id)):
        l.move(bob_id[i], -bob_fart[i], 0)

def ryd_bob_op():
    for i in range(len(bob_id)-1, -1, -1):
        x, y = faa_koord(bob_id[i])
        if x < -GAB:
            slet_boble(i)

def faa_koord(id_tal):
    hvor = l.coords(id_tal)
    x = (hvor[0] + hvor[2]) / 2
    y = (hvor[1] + hvor[3]) / 2
    return x, y

def slet_boble(i):
    del bob_r[i]
    del bob_fart[i]
    l.delete(bob_id[i])
    del bob_id[i]

def afstand(id1, id2):
    x1, y1 = faa_koord(id1)
    x2, y2 = faa_koord(id2)
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def kollision():
    point = 0
    for bob in range(len(bob_id)-1, -1, -1):
        if afstand(ubaad_id2, bob_id[bob]) < (UBAAD_R + bob_r[bob]):
            point += (bob_r[bob] + bob_fart[bob])
            slet_boble(bob)
    return point

# Funktioner til visning af score og tid
def vis_score(score):
    l.itemconfig(score_tekst, text=str(score))

def vis_tid(tid_rest):
    l.itemconfig(tid_tekst, text=str(tid_rest))

# Oprettelse af tekstområder til tid og score
l.create_text(50, 30, text='TID', fill='white')
l.create_text(150, 30, text='SCORE', fill='white')
tid_tekst = l.create_text(50, 50, fill='white')
score_tekst = l.create_text(150, 50, fill='white')

# Funktioner til vindertable
def get_high_scores():
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            high_scores = json.load(f)
    except FileNotFoundError:
        high_scores = []
    return high_scores

def update_high_scores(name, score):
    high_scores = get_high_scores()
    high_scores.append({"name": name, "score": score})
    high_scores = sorted(high_scores, key=lambda x: x['score'], reverse=True)[:5]
    with open(HIGH_SCORE_FILE, 'w') as f:
        json.dump(high_scores, f, indent=4)

def show_high_scores():
    high_scores = get_high_scores()
    y_offset = 100
    for i, entry in enumerate(high_scores):
        l.create_text(MID_X, y_offset, text=f"{i+1}. {entry['name']} - {entry['score']}", fill='white')
        y_offset += 30

# Spilsløjfe med opdatering
def spil():
    global score, bonus, slut
    if time() > slut:
        # Slut på spillet
        name = "Spiller"  # Du kan ændre dette til at få spillerens navn via et inputfelt
        update_high_scores(name, score)
        l.create_text(MID_X, MID_Y, text='GAME OVER', fill='white', font=('Helvetica', 30))
        l.create_text(MID_X, MID_Y + 30, text='Score: ' + str(score), fill='white')
        l.create_text(MID_X, MID_Y + 45, text='Bonustid: ' + str(bonus * TIDSFRIST), fill='white')
        show_high_scores()
        return

    if randint(1, BOB_CHANCE) == 1:
        lav_boble()
    flyt_bobler()
    ryd_bob_op()

    score += kollision()

    if (int(score / BONUS_SCORE)) > bonus:
        bonus += 1
        slut += TIDSFRIST

    vis_score(score)
    vis_tid(int(slut - time()))

    window.after(10, spil)  # Kald spil() igen efter 10ms

# Start spillet
spil()

# Start Tkinter GUI-løkke
window.mainloop()