import cv2
import numpy as np
import streamlit as st
from PIL import Image
import io

# Setup tiêu đề web
st.title("Web Xử Lý Ảnh Nhóm 10")

file_upload = st.file_uploader("Chọn file ảnh (jpg, png)", type=["jpg", "jpeg", "png"])

# Kịch bản khi người dùng đã tải ảnh lên
if file_upload:
    # Mở ảnh bằng thư viện PIL rồi chuyển sang mảng numpy để cv2 đọc được
    img_goc = Image.open(file_upload)
    img = np.array(img_goc)
    
    # Lấy chiều cao, rộng của ảnh để lát làm giới hạn cho thanh trượt
    h, w = img.shape[:2] 

    st.write("### Công cụ chỉnh sửa")

    # 1. Phần thanh trượt chỉnh sáng/tương phản
    st.write("**1. Chỉnh màu cơ bản**")
    c1, c2 = st.columns(2)
    with c1:
        do_tuong_phan = st.slider("Tương phản (alpha)", 1.0, 3.0, 1.0, step=0.1)
    with c2:
        do_sang = st.slider("Độ sáng (beta)", -100, 100, 0)

    # 2. Xoay ảnh
    st.write("**2. Xoay ảnh**")
    goc = st.slider("Góc xoay", -180, 180, 0)

    # 3. Cắt ảnh bằng 4 thanh trượt
    st.write("3. Cắt ảnh (Kéo 2 đầu thanh trượt để chọn vùng)")
    trai, phai = st.slider("Cắt theo chiều NGANG (Trái ↔ Phải)", 0, w, (0, w))
    tren, duoi = st.slider("Cắt theo chiều DỌC (Trên ↕ Dưới)", 0, h, (0, h))

    st.write("---")

    # ==========================================
    # BẮT ĐẦU CHẠY THUẬT TOÁN XỬ LÝ
    # ==========================================
    
  
    
    # Bước 1: Cắt ảnh (Dùng Array Slicing)
    img_cut = img[tren:duoi, trai:phai]

    # Bước 2: Chỉnh độ sáng và tương phản
    img_color = cv2.convertScaleAbs(img_cut, alpha=do_tuong_phan, beta=do_sang)

    # Bước 3: Xoay ảnh (Nếu có kéo thanh trượt góc xoay)
    if goc != 0:
        h_moi, w_moi = img_color.shape[:2]
        tam = (w_moi // 2, h_moi // 2) # Lấy tâm bức ảnh
        
        # Tạo ma trận xoay
        matrix = cv2.getRotationMatrix2D(tam, goc, 1.0)
        img_final = cv2.warpAffine(img_color, matrix, (w_moi, h_moi))
    else:
        # Nếu góc = 0 thì không cần xoay
        img_final = img_color

    # ==========================================
    # HIỂN THỊ LÊN WEB VÀ TẢI VỀ
    # ==========================================
    
    cot_trai, cot_phai = st.columns(2)
    with cot_trai:
        st.write("Ảnh ban đầu")
        st.image(img, use_container_width=True)
    with cot_phai:
        st.write("Ảnh đã sửa")
        st.image(img_final, use_container_width=True)

    # Đóng gói ảnh thành dạng Bytes để cho tải về
    buf = io.BytesIO()
    Image.fromarray(img_final).save(buf, format="PNG")
    
    st.download_button(
        label="Tải ảnh về", 
        data=buf.getvalue(), 
        file_name="anh_da_sua.png", 
        mime="image/png"
    )
