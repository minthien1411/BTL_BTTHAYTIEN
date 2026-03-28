import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# --- 1. GIAO DIỆN CƠ BẢN ---
st.title("HỆ THỐNG XỬ LÝ ẢNH ĐA PHƯƠNG TIỆN - NHÓM 10")

# Thành phần chính: Tải ảnh
uploaded_file = st.file_uploader("Tải ảnh lên (JPG, PNG, JPEG)", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Chuyển đổi file tải lên sang định dạng mảng Numpy để OpenCV xử lý
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    # --- 2. BẢNG ĐIỀU KHIỂN BÊN TRÁI (SIDEBAR) ---
    st.sidebar.header("CHỨC NĂNG XỬ LÝ")
    
    # Chức năng 1: Biến đổi điểm ảnh (Chương 2)
    st.sidebar.subheader("1. Chỉnh Brightness & Contrast")
    alpha = st.sidebar.slider("Hệ số Tương phản (α)", 1.0, 3.0, 1.0, step=0.1)
    beta = st.sidebar.slider("Độ sáng cộng thêm (β)", -100, 100, 0)

    # Chức năng 2: Bộ lọc không gian (Chương 3)
    st.sidebar.subheader("2. Bộ lọc làm mịn")
    filter_type = st.sidebar.selectbox("Chọn bộ lọc:", ["Gốc", "Median Filter (Lọc trung vị)", "Gaussian Blur (Lọc Gauss)"])
    
    # Chức năng 3: Chỉnh màu (Color Grading)
    st.sidebar.subheader("3. Hiệu ứng màu sắc")
    color_effect = st.sidebar.radio("Chọn hiệu ứng:", ["Không", "Vintage (Hoài cổ)", "Cyberpunk (Neon)"])

    # --- 3. THUẬT TOÁN XỬ LÝ (PHẦN QUAN TRỌNG ĐỂ GIẢI THÍCH) ---
    
    # Bước A: Áp dụng công thức P_out = alpha * P_in + beta
    # cv2.convertScaleAbs giúp xử lý tràn số (0-255)
    processed_img = cv2.convertScaleAbs(img_array, alpha=alpha, beta=beta)

    # Bước B: Áp dụng bộ lọc lân cận (Lọc nhiễu)
    if filter_type == "Median Filter (Lọc trung vị)":
        processed_img = cv2.medianBlur(processed_img, 5) # Kích thước cửa sổ 5x5
    elif filter_type == "Gaussian Blur (Lọc Gauss)":
        processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)

    # Bước C: Biến đổi kênh màu đơn lẻ
    if color_effect == "Vintage (Hoài cổ)":
        processed_img[:, :, 0] = cv2.addWeighted(processed_img[:, :, 0], 1.2, 0, 0, 15) # Tăng Đỏ
        processed_img[:, :, 2] = cv2.addWeighted(processed_img[:, :, 2], 0.8, 0, 0, -10) # Giảm Xanh dương
    elif color_effect == "Cyberpunk (Neon)":
        processed_img[:, :, 1] = cv2.multiply(processed_img[:, :, 1], 0.7) # Giảm Xanh lá
        processed_img[:, :, 2] = cv2.addWeighted(processed_img[:, :, 2], 1.4, 0, 0, 25) # Tăng Xanh dương

    # --- 4. HIỂN THỊ KẾT QUẢ SO SÁNH ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Ảnh gốc")
        st.image(img_array, use_container_width=True)
    with col2:
        st.subheader("Ảnh đã xử lý")
        st.image(processed_img, use_container_width=True)

    # Hiện công thức toán học (Thầy Tiến cực thích cái này)
    st.write("---")
    st.markdown("### Cơ sở toán học:")
    st.latex(r"P_{out}(x,y) = \alpha \cdot P_{in}(x,y) + \beta")

    # Phân tích đặc trưng Histogram (Chương 2)
    if st.checkbox("Hiển thị Biểu đồ Histogram"):
        st.write("#### Phân tích mật độ mức xám")
        gray_img = cv2.cvtColor(processed_img, cv2.COLOR_RGB2GRAY)
        fig, ax = plt.subplots()
        ax.hist(gray_img.ravel(), bins=256, range=[0, 256], color='blue', alpha=0.7)
        st.pyplot(fig)
