import cv2
import numpy as np
import streamlit as st
from PIL import Image

st.title("Web Xử Lý Ảnh Siêu Tốc ")

uploaded_file = st.file_uploader("Tải một bức ảnh lên đây đi m", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    st.write("📸 Ảnh gốc nè:")
    st.image(img_array)
    st.write("---") 

    alpha = st.slider("Chỉnh độ tương phản", 1.0, 3.0, 1.0)
    beta = st.slider("Chỉnh độ sáng", -100, 100, 0)

    img_adjusted = cv2.convertScaleAbs(img_array, alpha=alpha, beta=beta)

    st.write("✨ Ảnh sau khi chỉnh sửa:")
    st.image(img_adjusted)