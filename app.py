import streamlit as st
import cv2
import numpy as np
from PIL import Image

# --- 1. GIAO DIỆN CƠ BẢN ---
st.title("HỆ THỐNG XỬ LÝ ẢNH ĐA PHƯƠNG TIỆN - NHÓM 10")

uploaded_file = st.file_uploader("Tải ảnh lên (JPG, PNG, JPEG)", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    # --- 2. BẢNG ĐIỀU KHIỂN BÊN TRÁI (SIDEBAR) ---
    st.sidebar.header("THANH ĐIỀU CHỈNH THÔNG SỐ")
    
    # Chỉnh điểm ảnh (Chương 2)
    st.sidebar.subheader("1. Độ sáng & Tương phản")
    alpha = st.sidebar.slider("Hệ số Tương phản (α)", 0.5, 3.0, 1.0, 0.1)
    beta = st.sidebar.slider("Độ sáng cộng thêm (β)", -100, 100, 0)

    # Chỉnh bộ lọc lân cận (Chương 3)
    st.sidebar.subheader("2. Độ nhòe (Blur)")
    filter_type = st.sidebar.selectbox("Chọn bộ lọc:", ["Gốc", "Median Filter", "Gaussian Blur"])
    # Thanh trượt chỉnh kích thước cửa sổ lọc (phải là số lẻ: 1, 3, 5, 7...)
    ksize = st.sidebar.slider("Kích thước bộ lọc (Kernel)", 1, 15, 5, step=2)
    
    # Chỉnh hiệu ứng màu
    st.sidebar.subheader("3. Cường độ hiệu ứng")
    color_effect = st.sidebar.radio("Chọn hiệu ứng:", ["Không", "Vintage", "Cyberpunk"])
    # Thanh trượt chỉnh mức độ áp dụng màu sắc
    intensity = st.sidebar.slider("Mức độ áp dụng hiệu ứng (%)", 0, 100, 50) / 100.0

    # --- 3. THUẬT TOÁN XỬ LÝ ---
    
    # A. Biến đổi điểm ảnh
    processed_img = cv2.convertScaleAbs(img_array, alpha=alpha, beta=beta)

    # B. Áp dụng bộ lọc (Sử dụng ksize từ thanh trượt)
    if filter_type == "Median Filter":
        processed_img = cv2.medianBlur(processed_img, ksize)
    elif filter_type == "Gaussian Blur":
        processed_img = cv2.GaussianBlur(processed_img, (ksize, ksize), 0)

    # C. Áp dụng hiệu ứng màu (Sử dụng intensity từ thanh trượt)
    if color_effect == "Vintage":
        # Tăng đỏ dựa theo thanh trượt intensity
        red_boost = int(30 * intensity)
        processed_img[:, :, 0] = cv2.addWeighted(processed_img[:, :, 0], 1.0 + intensity, 0, 0, red_boost)
    elif color_effect == "Cyberpunk":
        # Tăng xanh dương dựa theo thanh trượt intensity
        blue_boost = int(50 * intensity)
        processed_img[:, :, 2] = cv2.addWeighted(processed_img[:, :, 2], 1.0 + intensity, 0, 0, blue_boost)
        processed_img[:, :, 1] = cv2.multiply(processed_img[:, :, 1], 1.0 - (0.5 * intensity))

    # --- 4. HIỂN THỊ KẾT QUẢ ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Ảnh gốc")
        st.image(img_array, use_container_width=True)
    with col2:
        st.subheader("Ảnh đã xử lý")
        st.image(processed_img, use_container_width=True)

    # Hiện công thức cho thầy Tiến xem
    st.write("---")
    st.latex(r"P_{out} = \alpha \cdot P_{in} + \beta")
