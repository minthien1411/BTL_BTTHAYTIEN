import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io  # Thư viện để xử lý luồng dữ liệu (vào/ra)

# --- 1. TIÊU ĐỀ ---
st.title("HỆ THỐNG XỬ LÝ ẢNH NHÓM 10 - PTIT")

uploaded_file = st.file_uploader("Chọn ảnh để bắt đầu", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    # --- 2. THANH ĐIỀU CHỈNH ---
    st.write("---")
    col_a, col_b = st.columns(2)
    with col_a:
        alpha = st.slider("Hệ số Tương phản (α)", 1.0, 3.0, 1.0, 0.1)
    with col_b:
        beta = st.slider("Độ sáng cộng thêm (β)", -100, 100, 0)

    # --- 3. THUẬT TOÁN XỬ LÝ ---
    img_processed = cv2.convertScaleAbs(img_array, alpha=alpha, beta=beta)

    # --- 4. HIỂN THỊ SO SÁNH ---
    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        st.write("Ảnh gốc")
        st.image(img_array, use_container_width=True)
    with c2:
        st.write("Ảnh sau xử lý")
        st.image(img_processed, use_container_width=True)

    # --- 5. CHỨC NĂNG TẢI ẢNH VỀ ---
    st.write("---")
    
    # Bước A: Chuyển mảng Numpy về lại định dạng PIL Image
    result_pil = Image.fromarray(img_processed)
    
    # Bước B: Lưu ảnh vào một "Bộ nhớ đệm" (Buffer) dưới dạng byte
    buffer = io.BytesIO()
    result_pil.save(buffer, format="PNG") # Lưu định dạng PNG để giữ chất lượng
    byte_im = buffer.getvalue() # Lấy giá trị byte của ảnh

    # Bước C: Tạo nút tải về
    st.download_button(
        label="Tải ảnh",
        data=byte_im,
        file_name="ket_qua_xu_ly.png",
        mime="image/png"
    )



