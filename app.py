import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import math
import io

st.set_page_config(layout="wide")

# =========================
# PREMIUM UI (UNCHANGED)
# =========================
st.markdown("""
<style>

/* =========================
   PREMIUM OTT SIDEBAR (UPGRADED)
========================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #020617 0%,
        #020617 20%,
        #020b2a 55%,
        #0b0f3a 100%
    );
    
    backdrop-filter: blur(24px);
    border-right: 1px solid rgba(99,102,241,0.15);

    /* subtle glow edge */
    box-shadow: 
        4px 0 25px rgba(59,130,246,0.08),
        inset -1px 0 0 rgba(255,255,255,0.04);
}

/* =========================
   SIDEBAR SECTION TITLE
========================= */
section[data-testid="stSidebar"] h3 {
    color: #c7d2fe;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* =========================
   RADIO BUTTON CONTAINER
========================= */
div[role="radiogroup"] {
    margin-top: 8px;
}

/* =========================
   COMPACT CHANNEL BUTTONS
========================= */
section[data-testid="stSidebar"] div[role="radiogroup"] > label {
    background: rgba(255,255,255,0.03);
    
    padding: 6px 8px;        /* ↓ reduced */
    margin-bottom: 5px;      /* ↓ reduced */
    
    border-radius: 8px;
    font-size: 12.5px;       /* ↓ smaller text */
    line-height: 1.2;        /* ↓ tighter */
    
    border: 1px solid rgba(255,255,255,0.05);
    transition: all 0.2s ease;
}

/* Hover */
section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background: rgba(59,130,246,0.15);
    transform: translateX(2px);
}

/* Selected */
section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-baseweb="radio"][aria-checked="true"] {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white !important;
    box-shadow: 0 0 10px rgba(99,102,241,0.4);
}
/* =========================
   FILE UPLOADER (CLEAN)
========================= */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04);
    border-radius: 10px;
    padding: 10px;
    border: 1px solid rgba(255,255,255,0.06);
}

/* =========================
   SELECTBOX (CATEGORY)
========================= */
div[data-baseweb="select"] {
    background: rgba(255,255,255,0.04);
    border-radius: 10px;
}

/* dropdown */
ul[role="listbox"] {
    background: #020617;
    border: 1px solid rgba(255,255,255,0.1);
}

/* =========================
   CURSOR FIX
========================= */
section[data-testid="stSidebar"] * {
    cursor: pointer !important;
    user-select: none !important;
    caret-color: transparent;
}

/* =========================
   HIDE STREAMLIT TOP-RIGHT CONTROLS
   (Keep Deploy button visible)
========================= */

/* Hide "File change", "Rerun", "Always rerun" */
header [data-testid="stStatusWidget"],
header [data-testid="stRerunButton"],
header [data-testid="stToolbar"] button[title="Rerun"],
header [data-testid="stToolbar"] button[title="Always rerun"] {
    display: none !important;
}

/* Hide the 3-dot menu */
header [data-testid="stToolbar"] button[aria-label="More options"] {
    display: none !important;
}

/* Keep Deploy visible and aligned */
header [data-testid="stToolbar"] {
    justify-content: flex-end;
}
</style>
""", unsafe_allow_html=True)

st.title("Sponsor Tool")

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
    if len(coords[0])==0: return None
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

# =========================
# TEXT
# =========================
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

# =========================
# WARNING
# ========================= 
def draw_warning(bg, text):
    draw = ImageDraw.Draw(bg)

    # Font (slightly bigger for clarity)
    font = ImageFont.truetype("assets/fonts/Magenos-Regular.otf", 34)

    text = text.upper()

    # Measure text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2]
    text_h = bbox[3]

    # Layout settings
    icon_size = 26
    gap = 14
    padding_x = 28
    padding_y = 14

    total_w = icon_size + gap + text_w

    # PERFECT CENTER ALIGNMENT
    x = (bg.width - total_w) // 2
    y = bg.height - (text_h + padding_y * 2 + 40)

    # -------------------------
    # BACKGROUND STRIP (clean centered)
    # -------------------------
    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    rect_x1 = x - padding_x
    rect_y1 = y - padding_y
    rect_x2 = x + total_w + padding_x
    rect_y2 = y + text_h + padding_y

    overlay_draw.rounded_rectangle(
        [rect_x1, rect_y1, rect_x2, rect_y2],
        radius=6,
        fill=(0, 0, 0, 200)
    )

    bg.paste(overlay, (0, 0), overlay)

    # -------------------------
    # WARNING ICON (centered vertically)
    # -------------------------
    icon_x = x
    icon_y = y + (text_h - icon_size) // 2

    triangle = [
        (icon_x, icon_y + icon_size),
        (icon_x + icon_size // 2, icon_y),
        (icon_x + icon_size, icon_y + icon_size)
    ]

    draw.polygon(triangle, fill="#FFD60A")

    # Exclamation mark
    ex_x = icon_x + icon_size // 2
    draw.line(
        [(ex_x, icon_y + 6), (ex_x, icon_y + 16)],
        fill="black",
        width=2
    )
    draw.ellipse(
        (ex_x - 1, icon_y + 19, ex_x + 1, icon_y + 21),
        fill="black"
    )

    # -------------------------
    # TEXT (aligned properly)
    # -------------------------
    text_x = icon_x + icon_size + gap
    draw.text((text_x, y), text, fill="#FFD60A", font=font)

# =========================
# MAIN
# =========================
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
        draw_warning(bg, "Logo resolution below broadcast standard")

    st.subheader("Final Output")
    st.image(bg)

    name = os.path.splitext(logo_file.name)[0]
    filename = f"{channel.replace(' ','')}_{name}_{category.replace(' ','')}.jpg"

    buf = io.BytesIO()
    bg.save(buf, "JPEG", quality=95, subsampling=0)
    buf.seek(0)

    st.download_button(
        "Download Output",
        buf,
        file_name=filename,
        key=f"download_{channel}_{name}"
    )