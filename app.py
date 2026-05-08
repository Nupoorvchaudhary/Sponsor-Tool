import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import math
import io

st.set_page_config(
    page_title="Sponsor Tool",
    page_icon="🎬",
    layout="wide"
)
# =========================
# THEME DETECTION
# =========================
theme = st.get_option("theme.base") or "dark"
is_dark = str(theme).lower() == "dark"

# =========================
# PREMIUM UI (FINAL FIXED)
# =========================
st.markdown(f"""
<style>

/* =========================
   GLOBAL BACKGROUND FIX
========================= */

html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {{

    background-color: {'#030712' if is_dark else '#f3f4f6'} !important;
}}

/* =========================
   MAIN CONTAINER
========================= */

.main .block-container {{

    padding-top: 1.5rem !important;

    background-color: {'#030712' if is_dark else '#f3f4f6'} !important;

    color: {'#f9fafb' if is_dark else '#111827'} !important;

    min-height: 100vh;
}}

/* =========================
   PREMIUM SIDEBAR
========================= */

section[data-testid="stSidebar"] > div:first-child {{

    background:
        {"linear-gradient(180deg, #020617 0%, #020617 20%, #020b2a 55%, #0b0f3a 100%)"
        if is_dark
        else "linear-gradient(180deg, #ffffff 0%, #f8fafc 45%, #eef2ff 100%)"};

    border-right:
        {"1px solid rgba(99,102,241,0.15)"
        if is_dark
        else "1px solid rgba(99,102,241,0.10)"};

    box-shadow:
        {"4px 0 25px rgba(59,130,246,0.08)"
        if is_dark
        else "4px 0 25px rgba(0,0,0,0.04)"};
}}

/* =========================
   SIDEBAR LABELS
========================= */

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div {{
    color: {"#e5e7eb" if is_dark else "#111827"} !important;
}}

/* =========================
   CHANNEL BUTTONS
========================= */

section[data-testid="stSidebar"] div[role="radiogroup"] > label {{

    background:
        {"rgba(255,255,255,0.03)"
        if is_dark
        else "rgba(255,255,255,0.92)"};

    padding: 6px 8px;
    margin-bottom: 6px;

    border-radius: 10px;
    font-size: 13px;

    border:
        {"1px solid rgba(255,255,255,0.06)"
        if is_dark
        else "1px solid rgba(0,0,0,0.06)"};

    transition: all 0.2s ease;

    cursor: pointer !important;
}}

/* Hover */

section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{

    background:
        {"rgba(59,130,246,0.15)"
        if is_dark
        else "rgba(59,130,246,0.10)"};

    transform: translateX(2px);
}}

/* Selected */

section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-baseweb="radio"][aria-checked="true"] {{
    background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
    color: white !important;
    box-shadow: 0 0 12px rgba(99,102,241,0.45);
}}

/* =========================
   FILE UPLOADER
========================= */

[data-testid="stFileUploader"] {{

    background:
        {"rgba(255,255,255,0.04)"
        if is_dark
        else "rgba(255,255,255,0.92)"} !important;

    border-radius: 12px;
    padding: 12px;

    border:
        {"1px solid rgba(255,255,255,0.06)"
        if is_dark
        else "1px solid rgba(0,0,0,0.06)"} !important;
}}

/* Remove white inner upload area */

[data-testid="stFileUploaderDropzone"] {{

    background:
        {"rgba(255,255,255,0.02)"
        if is_dark
        else "#ffffff"} !important;

    border:
        {"1px dashed rgba(255,255,255,0.08)"
        if is_dark
        else "1px dashed rgba(0,0,0,0.10)"} !important;

    border-radius: 10px !important;
}}

/* Remove extra white section */

[data-testid="stFileUploader"] section {{
    background: transparent !important;
}}

/* Upload Button */

[data-testid="stFileUploader"] button {{

    background:
        {"#374151"
        if is_dark
        else "#e5e7eb"} !important;

    color:
        {"white"
        if is_dark
        else "#111827"} !important;

    border: none !important;
    border-radius: 8px !important;
}}

/* Upload text */

[data-testid="stFileUploader"] small {{
    color:
        {"#9ca3af"
        if is_dark
        else "#374151"} !important;

    opacity: 1 !important;
}}

/* Filename text */

[data-testid="stFileUploader"] span {{
    color:
        {"#f9fafb"
        if is_dark
        else "#111827"} !important;
}}

/* =========================
   SELECTBOX
========================= */

div[data-baseweb="select"] {{
    cursor: pointer !important;
}}

div[data-baseweb="select"] * {{
    cursor: pointer !important;
}}

div[data-baseweb="select"] > div {{

    background:
        {"rgba(255,255,255,0.04)"
        if is_dark
        else "#ffffff"} !important;

    color:
        {"#f9fafb"
        if is_dark
        else "#111827"} !important;

    border-radius: 10px !important;

    border:
        {"1px solid rgba(255,255,255,0.08)"
        if is_dark
        else "1px solid rgba(0,0,0,0.08)"} !important;
}}

/* Selected text */

div[data-baseweb="select"] span {{
    color:
        {"#f9fafb"
        if is_dark
        else "#111827"} !important;
}}

/* Dropdown arrow */

div[data-baseweb="select"] svg {{
    fill:
        {"#f9fafb"
        if is_dark
        else "#111827"} !important;
}}

/* Dropdown menu */

ul[role="listbox"] {{

    background:
        {"#020617"
        if is_dark
        else "#ffffff"} !important;

    border:
        {"1px solid rgba(255,255,255,0.10)"
        if is_dark
        else "1px solid rgba(0,0,0,0.08)"} !important;
}}

/* Dropdown options */

ul[role="listbox"] li {{
    color:
        {"#f9fafb"
        if is_dark
        else "#111827"} !important;
}}

/* =========================
   DOWNLOAD BUTTON
========================= */

.stDownloadButton button {{
    background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.3rem !important;
    font-weight: 600 !important;
}}

.stDownloadButton button:hover {{
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(99,102,241,0.35);
}}

/* =========================
   MAIN TEXT
========================= */

h1, h2, h3, h4, h5, h6, p {{
    color: {"#f9fafb" if is_dark else "#111827"} !important;
}}

/* =========================
   REMOVE CURSOR
========================= */

* {{
    caret-color: transparent !important;
}}

/* =========================
   HIDE STREAMLIT MENU
========================= */

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

header {{
    background: transparent !important;
}}

/* Remove Deploy Button */

.stDeployButton {{
    display: none !important;
}}
/* =========================
   REMOVE DEPLOY BUTTON
========================= */

[data-testid="stToolbar"] {{
    display: none !important;
}}

.stDeployButton {{
    display: none !important;
}}

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

# Always show selected slate
bg = Image.open(
    os.path.join("assets/slates", CHANNEL_MAP[channel])
).convert("RGB")

# Remove blinking cursor space
st.markdown("""
<style>
textarea, input {
    caret-color: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# Show plain slate before upload
if not logo_file:
    st.image(bg)
else:
    logo = Image.open(logo_file)

    is_low_res = max(logo.size) < 800

    cropped = crop(logo)
    patch = get_patch(channel)

    # =========================
    # FIX FOR THUMBS UP LOGO
    # =========================
    logo_name = logo_file.name.lower()

    scale = get_scale(category)

    if "thumb" in logo_name or "thums" in logo_name:
        scale += 0.06

    resized = scale_logo(cropped, patch, scale)

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
