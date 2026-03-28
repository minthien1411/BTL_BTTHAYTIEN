import cv2
import numpy as np
import streamlit as st
from PIL import Image

st.title("Web Xử Lý Ảnh Siêu Tốc 🚀")

uploaded_file = st.file_uploader("Tải ảnh vào đây m", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    # --- THANH ĐIỀU KHIỂN ---
    st.sidebar.header("Cài đặt thông số")
    alpha = st.sidebar.slider("Chỉnh độ tương phản", 1.0, 3.0, 1.0)
    beta = st.sidebar.slider("Chỉnh độ sáng", -100, 100, 0)

    st.write("### Chọn bộ lọc bằng cách lướt thanh trượt bên dưới:")
    # Thanh trượt lướt qua các filter
    filter_choice = st.select_slider(
        "Lướt để thay đổi phong cách:",
        options=["Gốc", "Vintage", "Cyberpunk", "Mùa Hạ", "Mùa Đông", "Mùa Thu", "Nắng Ấm"]
    )

    # --- THUẬT TOÁN XỬ LÝ ---
    # 1. Chỉnh sáng và tương phản cơ bản trước
    img_processed = cv2.convertScaleAbs(img_array, alpha=alpha, beta=beta)

    # 2. Áp dụng các Filter màu (Dùng phép toán ma trận kênh màu)
    if filter_choice == "Vintage":
        # Tăng Đỏ, giảm Xanh dương, tạo độ ấm hoài cổ
        img_processed[:, :, 0] = cv2.addWeighted(img_processed[:, :, 0], 1.1, 0, 0, 20)
        img_processed[:, :, 2] = cv2.addWeighted(img_processed[:, :, 2], 0.9, 0, 0, -10)
        
    elif filter_choice == "Cyberpunk":
        # Đẩy mạnh Hồng (Red) và Xanh neon (Blue), giảm Xanh lá
        img_processed[:, :, 1] = cv2.multiply(img_processed[:, :, 1], 0.7)
        img_processed[:, :, 2] = cv2.addWeighted(img_processed[:, :, 2], 1.3, 0, 0, 30)
        img_processed[:, :, 0] = cv2.addWeighted(img_processed[:, :, 0], 1.2, 0, 0, 10)

    elif filter_choice == "Mùa Hạ":
        # Tăng độ bão hòa, đẩy tông vàng rực rỡ
        img_processed[:, :, 0] = cv2.addWeighted(img_processed[:, :, 0], 1.2, 0, 0, 10)
        img_processed[:, :, 1] = cv2.addWeighted(img_processed[:, :, 1], 1.1, 0, 0, 5)

    elif filter_choice == "Mùa Đông":
        # Đẩy tông Xanh dương (lạnh), giảm Đỏ
        img_processed[:, :, 0] = cv2.multiply(img_processed[:, :, 0], 0.8)
        img_processed[:, :, 2] = cv2.addWeighted(img_processed[:, :, 2], 1.2, 0, 0, 20)

    elif filter_choice == "Mùa Thu":
        # Tạo sắc cam/nâu bằng cách tăng Đỏ và Xanh lá (Red + Green = Yellow/Orange)
        img_processed[:, :, 0] = cv2.addWeighted(img_processed[:, :, 0], 1.2, 0, 0, 15)
        img_processed[:, :, 1] = cv2.addWeighted(img_processed[:, :, 1], 1.05, 0, 0, 0)
        img_processed[:, :, 2] = cv2.multiply(img_processed[:, :, 2], 0.7)

    elif filter_choice == "Nắng Ấm":
        # Tông vàng nhẹ nhàng của nắng chiều
        img_processed[:, :, 0] = cv2.addWeighted(img_processed[:, :, 0], 1.1, 0, 0, 10)
        img_processed[:, :, 1] = cv2.addWeighted(img_processed[:, :, 1], 1.1, 0, 0, 10)

    # --- HIỂN THỊ ---
    col1, col2 = st.columns(2)
    with col1:
        st.write("Ảnh gốc:")
        st.image(img_array, use_container_width=True)
    with col2:
        st.write(f"Đang áp dụng: **{filter_choice}**")
        st.image(img_processed, use_container_width=True)
