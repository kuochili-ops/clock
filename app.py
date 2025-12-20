import streamlit as st
from flip_clock_lib import st_flip_clock

st.set_page_config(page_title="全球城市翻板鐘", layout="centered")
st.title("🌏 全球城市翻板鐘")
st_flip_clock()
