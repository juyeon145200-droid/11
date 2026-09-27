import streamlit as st
from PIL import Image
from openai import OpenAI

st.set_page_config(page_title="하늘 사진 구름 분류기", page_icon="☁️")
st.title("☁️ 하늘 사진으로 구름 종류 맞히기")
st.caption("하늘 사진을 업로드하면 AI가 구름의 종류와 기상 특성을 판별해 드립니다.")

# OpenAI 클라이언트 설정
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

uploaded_file = st.file_uploader("하늘 사진을 선택하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 사진", use_container_wid
