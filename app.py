import cv2
import numpy as np
import streamlit as st
from PIL import Image
import io

st.title("Web Xử Lý Ảnh")

uploaded_file = st.file_uploader("Tải ảnh vào đây m", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    h, w = img_array.shape[:2]

    st.write("CÔNG CỤ ĐIỀU CHỈNH")

    # --- PHẦN 1: CHỈNH ĐIỂM ẢNH (SÁNG/TƯƠNG PHẢN) ---
    st.write("1. Chỉnh điểm ảnh cơ bản")
    col_a, col_b = st.columns(2)
    with col_a:
        alpha = st.slider("Chỉnh độ tương phản (α)", 1.0, 3.0, value=1.0, step=0.1)
    with col_b:
        beta = st.slider("Chỉnh độ sáng (β)", -100, 100, value=0)

    # --- PHẦN 2: BIẾN ĐỔI HÌNH HỌC (PHÓNG TO & XOAY) - ĐÃ CẬP NHẬT ---
    st.write("2. phóng to và Cắt ảnh")
    col_zoom, col_rot = st.columns(2)
    with col_zoom:
        zoom_factor = st.slider("Tỷ lệ phóng (x lần)", 1.0, 5.0, value=1.0, step=0.1)
    with col_rot:
        # Thanh trượt xoay từ -180 độ đến 180 độ
        goc_xoay = st.slider("Góc xoay (Độ)", -180, 180, value=0, step=1)

    st.write("---")

    # --- PHẦN 3: CẮT ẢNH (Giữ nguyên) ---
    st.write("3. Cắt ảnh (Kéo để chọn vùng)")
    c1, c2 = st.columns(2)
    with c1:
        trai = st.slider("Cắt từ bên TRÁI sang", 0, w-1, value=0)
        tren = st.slider("Cắt từ phía TRÊN xuống", 0, h-1, value=0)
    with c2:
        phai = st.slider("Cắt từ bên PHẢI vào", 1, w, value=w)
        duoi = st.slider("Cắt từ phía DƯỚI lên", 1, h, value=h)

    # --- THUẬT TOÁN XỬ LÝ ---
    if trai >= phai: phai = trai + 1
    if tren >= duoi: duoi = tren + 1
    
    # Bước 1: Cắt ảnh (Array Slicing)
    img_cropped = img_array[tren:duoi, trai:phai]

    # Bước 2: Chỉnh điểm ảnh (Sáng/Tương phản)
    img_adjusted = cv2.convertScaleAbs(img_cropped, alpha=alpha, beta=beta)

    # Bước 3: Xoay ảnh (MỚI THÊM)
    if goc_xoay != 0:
        h_rot, w_rot = img_adjusted.shape[:2]
        tam_xoay = (w_rot // 2, h_rot // 2) # Lấy tọa độ tâm bức ảnh
        
        # Lập ma trận xoay (Rotation Matrix)
        ma_tran_xoay = cv2.getRotationMatrix2D(tam_xoay, goc_xoay, 1.0)
        
        # Thực hiện phép biến đổi Affine để xoay ảnh
        img_adjusted = cv2.warpAffine(img_adjusted, ma_tran_xoay, (w_rot, h_rot))

    # Bước 4: Phóng to (Resize)
    curr_h, curr_w = img_adjusted.shape[:2]
    new_w = int(curr_w * zoom_factor)
    new_h = int(curr_h * zoom_factor)
    img_final = cv2.resize(img_adjusted, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    # --- HIỂN THỊ VÀ TẢI VỀ ---
    st.write("---")
    st_col1, st_col2 = st.columns(2)
    with st_col1:
        st.write("Ảnh gốc:")
        st.image(img_array, use_container_width=True)
    with st_col2:
        st.write("Kết quả:")
        st.image(img_final, use_container_width=True)

    # Nút Tải về
    result_pil = Image.fromarray(img_final)
    buffer = io.BytesIO()
    result_pil.save(buffer, format="PNG")
    st.download_button(
        label="Tải ảnh", 
        data=buffer.getvalue(), 
        file_name="uppic_result.png", 
        mime="image/png"
    )


  
