import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import math
import io

# =========================
# PAGE HEADER
# =========================
st.set_page_config(
    page_title="Sponsor Tool",
    page_icon="🎬",   # or use image path like "assets/logo.png"
    layout="wide"
)


# =========================
# THEME BASED TEXT FIXES (UNCHANGED)
# =========================
theme = st.get_option("theme.base")

if theme == "dark":
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {
        color: #e5e7eb !important;
    }

    button[kind="secondary"] {
        color: white !important;
    }

    [data-testid="stFileUploader"] small {
        color: #9ca3af !important;
    }
    </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {
        color: white !important;
    }

    button[kind="secondary"] {
        color: black !important;
    }

    [data-testid="stFileUploader"] small {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)


# =========================
# CHANNEL BUTTON UI (FIXED)
# =========================
st.markdown("""
<style>

/* =========================
   SIDEBAR (PREMIUM DARK GLASS)
========================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #020617 0%,
        #020617 25%,
        #020b2a 60%,
        #0b0f3a 100%
    );

    backdrop-filter: blur(20px);

    border-right: 1px solid rgba(99,102,241,0.15);

    box-shadow:
        4px 0 30px rgba(59,130,246,0.08),
        inset -1px 0 0 rgba(255,255,255,0.05);
}


/* =========================
   CHANNEL BUTTON BASE
========================= */
section[data-testid="stSidebar"] div[role="radiogroup"] > label {

    display: flex;
    align-items: center;

    padding: 8px 10px;
    margin-bottom: 8px;

    border-radius: 10px;
    font-size: 13px;

    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);

    transition: all 0.25s ease;
}

/* Hover */
section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background: rgba(59,130,246,0.18);
    transform: translateX(3px);
}


/* =========================
   SELECTED BUTTON
========================= */
section[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"] {
    background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
    color: white !important;
    border: none;

    box-shadow: 
        0 0 14px rgba(99,102,241,0.7),
        inset 0 0 8px rgba(255,255,255,0.15);
}


/* =========================
   RADIO DOT
========================= */
section[data-testid="stSidebar"] input[type="radio"] {
    accent-color: #ef4444;
}


/* =========================
   HERO SECTION (NEW PREMIUM GRADIENT)
========================= */

/* Container spacing fix */
.block-container {
    padding-top: 2rem;
}

/* Hero Wrapper */
.hero-container {
    border-radius: 18px;
    padding: 18px;
    position: relative;
    overflow: hidden;

    background: linear-gradient(
        135deg,
        #fbbf24 0%,
        #f59e0b 25%,
        #f97316 55%,
        #ea580c 80%,
        #dc2626 100%
    );

    box-shadow: 
        0 15px 40px rgba(0,0,0,0.35),
        inset 0 0 40px rgba(255,255,255,0.06);
}


/* Gloss light effect */
.hero-container::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 18px;

    background: linear-gradient(
        120deg,
        rgba(255,255,255,0.18) 0%,
        rgba(255,255,255,0.05) 30%,
        transparent 60%
    );

    pointer-events: none;
}


/* Image inside hero */
.hero-container img {
    border-radius: 12px;
}


/* =========================
   FILE UPLOADER BUTTON (CLEAR GREY)
========================= */
[data-testid="stFileUploader"] button {
    background-color: #374151 !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 8px;
}

[data-testid="stFileUploader"] button:hover {
    background-color: #4b5563 !important;
}


/* =========================
   REMOVE TEXT CURSOR (CLEAN UI)
========================= */
body, div, section {
    caret-color: transparent !important;
}

input, textarea {
    caret-color: auto !important;
}
            
/* DOWNLOAD BUTTON */
div.stDownloadButton > button {
    background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 18px !important;
    font-weight: 500;
    box-shadow: 0 0 10px rgba(99,102,241,0.5);
}

/* Hover */
div.stDownloadButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 0 16px rgba(99,102,241,0.8);
}

/* Hide top right toolbar (Deploy + menu) */
header[data-testid="stHeader"] {
    display: none;
}

/* Remove top spacing created by header */
.block-container {
    padding-top: 1rem !important;
}
            
/* Category dropdown → show hand cursor */
div[data-baseweb="select"] * {
    cursor: pointer !important;
}

/* Dropdown options list → hand cursor */
ul[role="listbox"] li {
    cursor: pointer !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# CONFIG
# =========================
CHANNEL_MAP = {
    "Star Gold": "StarGold.jpg",
    "Star Gold 2": "StarGold2.jpg",
    "Star Gold Thrills": "StarGoldThrills.jpg",
    "Star Gold Romance": "StarGoldRomance.jpg",
    "Star Gold Select": "StarGoldSelect.jpg",
    "Star Utsav Movies": "StarUtsavMovies.jpg"
}

DEFAULT_PATCH = {"x": 385, "y": 195, "width": 1150, "height": 715}
UTSAV_PATCH = {"x": 550, "y": 312, "width": 820, "height": 550}


def get_patch(channel):
    return UTSAV_PATCH if channel == "Star Utsav Movies" else DEFAULT_PATCH


# =========================
# SIDEBAR
# =========================
channel = st.sidebar.radio("Channel", list(CHANNEL_MAP.keys()))
logo_file = st.sidebar.file_uploader("Upload Logo", type=["png","jpg","jpeg"])

category = st.sidebar.selectbox("Category", [
    "Presented by","Co-Presented by","Associate Partner",
    "Powered by","Co-Powered by","Special Partner","Others"
])

custom_text = st.sidebar.text_input("Custom Text") if category=="Others" else ""


# =========================
# FUNCTIONS
# =========================
def get_scale(category):
    return 0.20 if category in ["Presented by","Co-Presented by"] else 0.15


def get_bbox(img):
    if img.mode!="RGBA":
        img=img.convert("RGBA")

    arr=np.array(img)
    alpha=arr[:,:,3]
    coords=np.where(alpha>0)

    if len(coords[0])==0:
        return None

    return coords[1].min(),coords[0].min(),coords[1].max(),coords[0].max()


def crop(img):
    bbox=get_bbox(img)
    return img.crop(bbox) if bbox else img


def scale_logo(logo,patch,scale):
    w,h=logo.size
    factor=math.sqrt((patch["width"]*patch["height"])/(w*h))*scale
    return logo.resize((int(w*factor),int(h*factor)),Image.LANCZOS)


def paste(bg,logo,patch):
    x=patch["x"]+(patch["width"]-logo.width)//2
    y=patch["y"]+(patch["height"]-logo.height)//2
    bg.paste(logo,(x,y),logo if logo.mode=="RGBA" else None)
    return y


def draw_text(bg,text,logo_top,patch,logo_width):
    draw=ImageDraw.Draw(bg)
    font_size=int(logo_width*0.12)
    font=ImageFont.truetype("assets/fonts/Magenos-Regular.otf",font_size)

    text=text.upper()
    bbox=draw.textbbox((0,0),text,font=font)
    text_w=bbox[2]

    x=patch["x"]+(patch["width"]-text_w)//2
    y=logo_top-int(font_size*2.5)

    draw.text((x,y),text,fill="black",font=font)


def draw_warning(bg, text):
    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype("assets/fonts/Magenos-Regular.otf", 34)

    text = text.upper()

    # TEXT SIZE
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2]
    text_h = bbox[3]

    # ICON CONFIG
    icon_size = 26
    gap = 12

    total_w = icon_size + gap + text_w

    # CENTER WHOLE BLOCK (ICON + TEXT)
    x = (bg.width - total_w) // 2
    y = bg.height - (text_h + 60)

    # =========================
    # BACKGROUND STRIP
    # =========================
    padding_x = 24
    padding_y = 10

    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    overlay_draw.rounded_rectangle(
        [
            x - padding_x,
            y - padding_y,
            x + total_w + padding_x,
            y + text_h + padding_y
        ],
        radius=10,
        fill=(0, 0, 0, 210)
    )

    bg.paste(overlay, (0, 0), overlay)

    # =========================
    # ICON (perfect alignment)
    # =========================
    icon_x = x
    icon_y = y + (text_h - icon_size) // 2

    triangle = [
        (icon_x, icon_y + icon_size),
        (icon_x + icon_size // 2, icon_y),
        (icon_x + icon_size, icon_y + icon_size)
    ]

    draw.polygon(triangle, fill="#FFD60A")

    # exclamation
    ex_x = icon_x + icon_size // 2
    draw.line([(ex_x, icon_y + 6), (ex_x, icon_y + 16)], fill="black", width=2)
    draw.ellipse((ex_x - 2, icon_y + 18, ex_x + 2, icon_y + 22), fill="black")

    # =========================
    # TEXT (aligned to icon)
    # =========================
    draw.text((icon_x + icon_size + gap, y), text, fill="#FFD60A", font=font)


# =========================
# MAIN
# =========================
# =========================
# HERO / PREVIEW SECTION
# =========================

st.markdown("## ")

# Load default slate preview
preview_bg = Image.open(
    os.path.join("assets/slates", CHANNEL_MAP[channel])
).convert("RGB")

# Show preview if no logo uploaded
if not logo_file:
    st.markdown(
        "<h3 style='text-align:center; color:#9ca3af;'>Upload a logo to generate sponsor slate</h3>",
        unsafe_allow_html=True
    )

    st.image(preview_bg)

if logo_file:
    bg = Image.open(os.path.join("assets/slates", CHANNEL_MAP[channel])).convert("RGB")
    logo = Image.open(logo_file)

    is_low_res = max(logo.size) < 800

    cropped = crop(logo)
    patch = get_patch(channel)

    resized = scale_logo(cropped, patch, get_scale(category))
    y = paste(bg, resized, patch)

    text = custom_text if category == "Others" else category
    draw_text(bg, text, y, patch, resized.width)

    if is_low_res:
        draw_warning(bg, "LOW RESOLUTION LOGO — MAY APPEAR BLURRY")

    st.subheader("Final Output")
    st.image(bg)

    name = os.path.splitext(logo_file.name)[0]
    filename = f"{channel.replace(' ','')}_{name}_{category.replace(' ','')}.jpg"

    buf = io.BytesIO()
    bg.save(buf, "JPEG", quality=95, subsampling=0)
    buf.seek(0)

    st.download_button("Download Output", buf, file_name=filename)
