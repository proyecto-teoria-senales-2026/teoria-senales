"""Navegación de la aplicación de Teoría de Señales."""

from __future__ import annotations

import streamlit as st


navigation = st.navigation(
    [
        st.Page("pages/01_C1_1.py", title="C-1-1"),
        st.Page("pages/02_C1_2.py", title="C-1-2"),
        st.Page("pages/03_C1_3.py", title="C-1-3"),
        st.Page("pages/04_C1_4.py", title="C-1-4"),
        st.Page("pages/05_C3_3.py", title="C-3-3"),
    ],
    position="sidebar",
)

navigation.run()
