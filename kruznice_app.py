import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import tempfile
from fpdf import FPDF
import base64
from io import BytesIO

# -----------------------------
# Base64 kód fontu DejaVuSans.ttf
# Z důvodu velikosti sem dej svůj base64 kód
# font_base64 = "TU1U...."
font_base64 = "TU1U..."  # nahraď úplným base64 kódem fontu
font_data = base64.b64decode(font_base64)
font_file = BytesIO(font_data)
# -----------------------------

# ---- Nadpis aplikace ----
st.title("Moje školní aplikace: body na kružnici")

# ---- Vstupy od uživatele ----
x0 = st.number_input("Souřadnice středu X:", value=0.0)
y0 = st.number_input("Souřadnice středu Y:", value=0.0)
r = st.number_input("Poloměr kružnice (m):", value=5.0, min_value=0.1)
n = st.number_input("Počet bodů:", value=8, min_value=1, step=1)
barva = st.color_picker("Vyber barvu bodů:", "#ff0000")

# ---- Výpočet souřadnic bodů ----
angles = np.linspace(0, 2*np.pi, int(n), endpoint=False)
x_points = x0 + r * np.cos(angles)
y_points = y0 + r * np.sin(angles)

# ---- Vykreslení ----
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.grid(True)

# osa x a y
ax.axhline(0, color="black", linewidth=1)
ax.axvline(0, color="black", linewidth=1)

# vykreslení kružnice a bodů
circle = plt.Circle((x0, y0), r, fill=False, linestyle="--", color="gray")
ax.add_artist(circle)
ax.scatter(x_points, y_points, color=barva, label="Body")

# popis os
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")

# zobrazíme graf ve Streamlit
st.pyplot(fig)

# ---- Informace o autorovi ----
st.sidebar.title("Bodový graf")
st.sidebar.write("Autor: Patrik Sázavský")   # změň na své jméno
st.sidebar.write("Kontakt: 278339@vutbr.cz")
st.sidebar.write("Použité technologie: Python, Streamlit, Matplotlib")

# ---- Export do PDF ----
from fpdf import FPDF
import tempfile

st.sidebar.title("Export")
if st.sidebar.button("Uložit do PDF"):
    pdf = FPDF()
    pdf.add_page()

    # font podporující UTF-8
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    # obsah PDF
    pdf.cell(0, 10, "Bodový graf", ln=True)
    pdf.cell(0, 10, f"Autor: Patrik Sázavský", ln=True)
    pdf.cell(0, 10, f"Email: 278339@vutbr.cz", ln=True)
    pdf.cell(0, 10, f"Střed: ({x0}, {y0})", ln=True)
    pdf.cell(0, 10, f"Poloměr: {r} m", ln=True)
    pdf.cell(0, 10, f"Počet bodů: {n}", ln=True)
    pdf.cell(0, 10, f"Barva: {barva}", ln=True)

    # uložení do dočasného souboru
    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp_pdf.name)

    # nabídka ke stažení
    with open(tmp_pdf.name, "rb") as f:
        st.download_button("Stáhnout PDF", f, file_name="bodovy_graf.pdf")
