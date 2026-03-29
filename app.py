import cv2
import numpy as np
import streamlit as st
from PIL import Image
import io # Thư viện để hỗ trợ tải ảnh về

st.title("Web Xử Lý Ảnh Siêu Tốc 🚀")

uploaded_file = st.file_uploader("Tải ảnh vào đây m", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    # Lấy kích thước ảnh để đặt giới hạn cho thanh trượt cắt ảnh
    h, w = img_array.shape[:2]

    st.write("### 🛠 CÔNG CỤ ĐIỀU CHỈNH")

    # --- PHẦN 1: CHỈNH SÁNG & TƯƠNG PHẢN ---
    col_a, col_b = st.columns(2)
    with col_a:
        alpha = st.slider("Chỉnh độ tương phản (α)", 1.0, 3.0, 1.0, step=0.1)
    with col_b:
        beta = st.slider("Chỉnh độ sáng (β)", -100, 100, 0)

    st.write("---")

    # --- PHẦN 2: CẮT ẢNH TÙY Ý (4 THANH TRƯỢT) ---
    st.write("📏 **Cắt ảnh (Kéo để chọn vùng muốn lấy):**")
    c1, c2 = st.columns(2)
    with c1:
        trai = st.slider("Cắt từ bên TRÁI sang", 0, w-1, 0)
        tren = st.slider("Cắt từ phía TRÊN xuống", 0, h-1, 0)
    with c2:
        phai = st.slider("Cắt từ bên PHẢI vào", 1, w, w)
        duoi = st.slider("Cắt từ phía DƯỚI lên", 1, h, h)

    # --- PHẦN 3: THUẬT TOÁN (Slicing ma trận) ---
    # Cắt ảnh trước: lấy vùng từ [trên đến dưới, trái đến phải]
    # Lưu ý: Nếu lỡ kéo nhầm trái > phải thì code vẫn không lỗi nhờ if này
    if trai >= phai: phai = trai + 1
    if tren >= duoi: duoi = tren + 1
    
    img_cropped = img_array[tren:duoi, trai:phai]

    # Sau đó mới chỉnh sáng/tương phản trên phần ảnh đã cắt
    img_final = cv2.convertScaleAbs(img_cropped, alpha=alpha, beta=beta)

    # --- PHẦN 4: HIỂN THỊ VÀ TẢI VỀ ---
    st.write("---")
    st_col1, st_col2 = st.columns(2)
    with st_col1:
        st.write("🖼 **Ảnh gốc:**")
        st.image(img_array, use_container_width=True)
    with st_col2:
        st.write("✨ **Kết quả:**")
        st.image(img_final, use_container_width=True)

    # Chức năng tải về
    result_pil = Image.fromarray(img_final)
    buffer = io.BytesIO()
    result_pil.save(buffer, format="PNG")
    st.download_button(label="📥 Tải ảnh này về máy", data=buffer.getvalue(), file_name="ket_qua.png", mime="image/png")

    # Hiện công thức cho thầy Tiến cộng điểm
    st.latex(r"P_{out} = \alpha \cdot P_{in}[y_1:y_2, x_1:x_2] + \beta")
