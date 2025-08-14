# app.py — Streamlit "Pokémon Math Mystery" with multi-tab layout
import random, math
from pathlib import Path
from typing import List, Tuple, Optional

import numpy as np
import streamlit as st
from PIL import Image, ImageSequence, features
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

st.set_page_config(page_title="Math Games", page_icon="🧮", layout="wide")
ASSETS_DIR = Path("assets"); ASSETS_DIR.mkdir(exist_ok=True)

def rand_item(xs): return xs[random.randrange(len(xs))]
def clamp(x, lo, hi): return max(lo, min(hi, x))

def parse_factors(text: str) -> List[int]:
    xs=[]; 
    for part in text.split(","):
        part=part.strip()
        if not part: continue
        try:
            n=int(part)
            if 0<=n<=12: xs.append(n)
        except: pass
    return xs or [0,1,2,5,10]

def list_asset_images()->List[str]:
    return sorted([f.name for f in ASSETS_DIR.iterdir()
                   if f.suffix.lower() in {".png",".jpg",".jpeg",".gif",".webp"}]) if ASSETS_DIR.exists() else []

WEBP_ENABLED = features.check("webp")
def load_token_image(path: Path) -> Optional[Image.Image]:
    if not path.exists(): return None
    try:
        im = Image.open(path)
        if getattr(im,"is_animated",False): im = next(ImageSequence.Iterator(im))
        return im.convert("RGBA")
    except Exception as e:
        if path.suffix.lower()==".webp" and not WEBP_ENABLED:
            st.warning("WEBP not supported by this Pillow build. Try a PNG/JPG or upgrade Pillow.")
        else:
            st.warning(f"Image load error for {path.name}: {e}")
        return None

MYSTERY_PHRASES = ["TRAINER BADGE","ELECTRIC ENERGY","MYSTERY GYM","POCKET CREATURES"]
STORY_BEATS = [
    "A quiet morning in Pal Meadow. Your partner creature nudges you awake — the town's Gym is glowing with strange symbols.",
    "At the meadow gate, you find a note: 'Only those who understand equal groups may pass...'",
    "A breeze flips another card: 'Count your jumps on the number line to cross the river.'",
    "The Gym doors shimmer: 'Know a fact, and its family follows.'",
    "Inside the entry hall, a pedestal asks for a mystery phrase. Each correct step will reveal a letter...",
]

def make_problem(factors: List[int], mode: str):
    if mode=="multiply":
        a=rand_item(factors); b=rand_item(factors)
        return {"a":a,"b":b,"op":"×","prompt":f"{a} × {b} = ?","answer":a*b,
                "dividend":None,"divisor":None}
    elif mode=="divide":
        a=rand_item(factors); b=rand_item(factors)
        dividend=a*b; divisor=rand_item([a,b]) or 1
        return {"a":a,"b":b,"op":"÷","prompt":f"{dividend} ÷ {divisor} = ?",
                "answer":dividend//divisor,"dividend":dividend,"divisor":divisor}
    else:
        return make_problem(factors, "multiply" if random.random()<0.5 else "divide")

def number_line_steps(prob)->List[int]:
    if prob["op"]=="×":
        return [(i+1)*prob["a"] for i in range(prob["b"])]
    step = prob.get("divisor",1) or 1
    target = prob.get("dividend",0) or 0
    jumps = max(1, target//max(1,step))
    return [(i+1)*step for i in range(jumps)]

def show_number_line(prob):
    steps=number_line_steps(prob)
    if not steps: st.info("No steps to show."); return
    maxv=steps[-1]; ticks=max(5,min(10, math.ceil(maxv/2))); xs=np.linspace(0,maxv,ticks+1)
    fig,ax=plt.subplots(figsize=(5,1.5)); ax.hlines(0,0,maxv)
    for x in xs: ax.vlines(x,-0.05,0.05); ax.text(x,-0.15,str(int(round(x))),ha="center",va="top",fontsize=8)
    last=0
    for s in steps: ax.hlines(0,last,s,linewidth=3); ax.text(s,0.1,str(s),ha="center",va="bottom",fontsize=8); last=s
    ax.set_ylim(-0.3,0.3); ax.set_xlim(0,maxv); ax.axis("off"); st.pyplot(fig, clear_figure=True)

def show_equal_groups(prob):
    groups,in_each=(prob["a"],prob["b"]) if prob["op"]=="×" else (prob.get("divisor",1), prob["answer"])
    cols=min(5,groups); rows=math.ceil(groups/cols)
    fig,axes=plt.subplots(rows,cols,figsize=(cols*1.6,rows*1.6)); axes=np.atleast_1d(axes).flatten()
    for g in range(groups):
        ax=axes[g]; ax.set_title(f"Group {g+1}",fontsize=8)
        side=max(1, math.ceil(math.sqrt(in_each))); grid=np.zeros((side,side))
        ax.imshow(grid); ax.set_xticks([]); ax.set_yticks([]); ax.text(0.5,0.5,f"{in_each}",transform=ax.transAxes,ha="center",va="center",fontsize=10)
    for k in range(groups,len(axes)): axes[k].axis("off")
    plt.tight_layout(); st.pyplot(fig, clear_figure=True)

def fact_web(prob):
    if prob["op"]=="×":
        a,b=prob["a"],prob["b"]; p=a*b; facts=[f"{a} × {b} = {p}",f"{b} × {a} = {p}",f"{p} ÷ {a} = {b}",f"{p} ÷ {b} = {a}"]
    else:
        d,v,q=prob["dividend"],prob["divisor"],prob["answer"]; facts=[f"{q]()
