import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# --- 1. TIÊU ĐỀ ---
st.title("HỆ THỐNG XỬ LÝ ẢNH NHÓM 10 - PTIT")

uploaded_file = st.file_uploader("Chọn ảnh để bắt đầu", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    # Lấy kích thước ảnh gốc để giới hạn thanh trượt cắt ảnh
    chieu_cao, chieu_rong = img_array.shape[:2]

    # --- 2. THANH ĐIỀU CHỈNH (SIDEBAR) ---
    st.sidebar.header("CÔNG CỤ XỬ LÝ")
    
    # Chức năng cắt ảnh (MỚI THÊM)
    st.sidebar.subheader("1. Cắt ảnh (Crop)")
    left = st.sidebar.slider("Cắt từ bên trái", 0, chieu_rong - 1, 0)
    right = st.sidebar.slider("Cắt từ bên phải", 0, chieu_rong, chieu_rong)
    top = st.sidebar.slider("Cắt từ phía trên", 0, chieu_cao - 1, 0)
    bottom = st.sidebar.slider("Cắt từ phía dưới", 0, chieu_cao, chieu_cao)

    # Chức năng chỉnh sáng & tương phản (Giữ nguyên)
    st.sidebar.subheader("2. Chỉnh điểm ảnh")
    alpha = st.sidebar.slider("Hệ số Tương phản (α)", 1.0, 3.0, 1.0, 0.1)
    beta = st.sidebar.slider("Độ sáng cộng thêm (β)", -100, 100, 0)

    # --- 3. THUẬT TOÁN XỬ LÝ ---
    
    # Bước A: Cắt ảnh bằng kỹ thuật Slicing ma trận Numpy
    # Cú pháp: mang_anh[y_dau : y_cuoi, x_dau : x_cuoi]
    img_cropped = img_array[top:bottom, left:right]

    # Bước B: Chỉnh sáng/tương phản trên phần ảnh đã cắt
    img_processed = cv2.convertScaleAbs(img_cropped, alpha=alpha, beta=beta)

    # --- 4. HIỂN THỊ SO SÁNH ---
    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        st.write("🖼 **Ảnh gốc ban đầu**")
        st.image(img_array, use_container_width=True)
    with c2:
        st.write("✨ **Kết quả (Đã cắt + Chỉnh sửa)**")
        st.image(img_processed, use_container_width=True)

    # --- 5. TẢI ẢNH VỀ ---
    st.write("---")
    result_pil = Image.fromarray(img_processed)
    buffer = io.BytesIO()
    result_pil.save(buffer, format="PNG")
    st.download_button(
        label="📥 Tải ảnh kết quả về máy",
        data=buffer.getvalue(),
        file_name="uppic_result.png",
        mime="image/png"
    )

    # Hiện công thức toán học
    st.latex(r"P_{out} = \alpha \cdot P_{in}[y_1:y_2, x_1:x_2] + \beta")
