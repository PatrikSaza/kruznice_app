import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import tempfile
from fpdf import FPDF

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
if st.button("Export do PDF"):
    # uložíme graf do dočasného obrázku
    tmp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    fig.savefig(tmp_img.name)

    # vytvoření PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Bodový graf", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(200, 10, f"Autor: Patrik Sázavský", ln=True)
    pdf.cell(200, 10, f"Email: 278339@vutbr.cz", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, f"Střed: ({x0}, {y0})", ln=True)
    pdf.cell(200, 10, f"Poloměr: {r} m", ln=True)
    pdf.cell(200, 10, f"Počet bodů: {n}", ln=True)
    pdf.cell(200, 10, f"Barva bodů: {barva}", ln=True)
    pdf.ln(10)

    pdf.image(tmp_img.name, x=10, y=None, w=180)

    # uložíme PDF do dočasného souboru
    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp_pdf.name)

    # nabídneme ke stažení
    with open(tmp_pdf.name, "rb") as f:
        st.download_button("Stáhnout PDF", f, file_name="bodovy_graf.pdf")

    # úklid
    os.unlink(tmp_img.name)
    os.unlink(tmp_pdf.name)
