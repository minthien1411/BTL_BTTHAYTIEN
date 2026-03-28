import cv2
import numpy as np
import streamlit as st
from PIL import Image

st.title("Web Xử Lý Ảnh Siêu Tốc")

uploaded_file = st.file_uploader("Tải ảnh here", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    # --- HIỂN THỊ ẢNH GỐC ---
    st.write("Ảnh gốc:")
    st.image(img_array, use_container_width=True)
    st.write("---") 

    # --- PHẦN ĐIỀU CHỈNH 1: CƠ BẢN (TRÊN MÀN HÌNH CHÍNH) ---
    st.write("1. Chỉnh sửa cơ bản")
    col_a, col_b = st.columns(2)
    with col_a:
        alpha = st.slider("Độ tương phản (α)", 1.0, 3.0, 1.0, step=0.1)
    with col_b:
        beta = st.slider("Độ sáng (β)", -100, 100, 0)

    # --- PHẦN ĐIỀU CHỈNH 2: BỘ LỌC (THANH TRƯỢT LƯỚT) ---
    st.write("2. Lướt để chọn bộ lọc")
    filter_choice = st.select_slider(
        "Kéo thanh này để đổi phong cách:",
        options=["Gốc", "Vintage", "Cyberpunk", "Mùa Hạ", "Mùa Đông", "Mùa Thu", "Nắng Ấm"]
    )

    # --- THUẬT TOÁN XỬ LÝ ---
    # 1. Chỉnh sáng và tương phản (P_out = alpha * P_in + beta)
    img_processed = cv2.convertScaleAbs(img_array, alpha=alpha, beta=beta)

    # 2. Áp dụng logic các Filter màu
    if filter_choice == "Vintage":
        img_processed[:, :, 0] = cv2.addWeighted(img_processed[:, :, 0], 1.1, 0, 0, 20)
        img_processed[:, :, 2] = cv2.addWeighted(img_processed[:, :, 2], 0.9, 0, 0, -10)
        
    elif filter_choice == "Cyberpunk":
        img_processed[:, :, 1] = cv2.multiply(img_processed[:, :, 1], 0.7)
        img_processed[:, :, 2] = cv2.addWeighted(img_processed[:, :, 2], 1.3, 0, 0, 30)

    elif filter_choice == "Mùa Hạ":
        img_processed[:, :, 0] = cv2.addWeighted(img_processed[:, :, 0], 1.2, 0, 0, 10)
        img_processed[:, :, 1] = cv2.addWeighted(img_processed[:, :, 1], 1.1, 0, 0, 5)

    elif filter_choice == "Mùa Đông":
        img_processed[:, :, 0] = cv2.multiply(img_processed[:, :, 0], 0.8)
        img_processed[:, :, 2] = cv2.addWeighted(img_processed[:, :, 2], 1.2, 0, 0, 20)

    elif filter_choice == "Mùa Thu":
        img_processed[:, :, 0] = cv2.addWeighted(img_processed[:, :, 0], 1.2, 0, 0, 15)
        img_processed[:, :, 2] = cv2.multiply(img_processed[:, :, 2], 0.7)

    elif filter_choice == "Nắng Ấm":
        img_processed[:, :, 0] = cv2.addWeighted(img_processed[:, :, 0], 1.1, 0, 0, 10)
        img_processed[:, :, 1] = cv2.addWeighted(img_processed[:, :, 1], 1.1, 0, 0, 10)

    # --- HIỂN THỊ KẾT QUẢ ---
    st.write("---")
    st.write(f" **Kết quả sau khi chỉnh sửa ({filter_choice}):**")
    st.image(img_processed, use_container_width=True)

    # Công thức toán học (Dành cho thầy Tiến)
    st.latex(r"P_{out} = \alpha \cdot P_{in} + \beta")
