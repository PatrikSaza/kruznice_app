import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

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
