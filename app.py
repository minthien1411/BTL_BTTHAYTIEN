import cv2
import numpy as np
import streamlit as st
from PIL import Image
import io

#Tiêu đề web
st.title("Web Xử Lý Ảnh Nhóm 16")

file_upload = st.file_uploader("Chọn file ảnh (jpg, png)", type=["jpg", "jpeg", "png"])


if file_upload:
    # Mở ảnh bằng thư viện PIL rồi chuyển sang mảng numpy để cv2 đọc được
    img_goc = Image.open(file_upload)
    img = np.array(img_goc)
    
    # Lấy chiều cao, rộng của ảnh để làm giới hạn cho thanh trượt
    h, w = img.shape[:2] 

    st.write("### Công cụ chỉnh sửa")

    # 1. chỉnh sáng/tương phản
    st.write("**1. Chỉnh độ tương phản & độ sáng**")
    c1, c2 = st.columns(2)
    with c1:
        do_tuong_phan = st.slider("Tương phản ", 1.0, 3.0, 1.0, step=0.1)
    with c2:
        do_sang = st.slider("Độ sáng ", -100, 100, 0)

    # 2. Xoay ảnh
    st.write("**2. Xoay ảnh**")
    goc = st.slider("Góc xoay", -180, 180, 0)

    # 3. Cắt ảnh  
    st.write("**3. Cắt ảnh (Kéo 2 đầu thanh trượt để chọn vùng)**")
    trai, phai = st.slider("Cắt theo chiều NGANG (Trái ↔ Phải)", 0, w, (0, w))
    tren, duoi = st.slider("Cắt theo chiều DỌC (Trên ↕ Dưới)", 0, h, (0, h))

    # 4. Làm mịn ảnh 
    st.write("**4. Làm mịn ảnh**")

    do_min = st.slider("Mức độ làm mịn", 1, 101, 1, step=2)

    st.write("---")
    # 5. Chuyển đổi hệ màu
    st.write("**5. Chuyển đổi không gian màu**")
    he_mau = st.selectbox("Chọn hệ màu muốn hiển thị", ["Gốc (RGB)", "Ảnh Xám (Grayscale)", "Hệ màu HSV"])

    #THUẬT TOÁN XỬ LÝ
    
   
    
    # Bước 1: Cắt ảnh 
    img_cut = img[tren:duoi, trai:phai]

    # Bước 2: Chỉnh độ sáng và tương phản
    img_color = cv2.convertScaleAbs(img_cut, alpha=do_tuong_phan, beta=do_sang)

    # Bước 3: Làm mịn ảnh 
    # Nếu thanh trượt > 1 thì áp dụng làm mịn
    if do_min > 1:
        img_color = cv2.GaussianBlur(img_color, (do_min, do_min), 0)

    # Bước 4: Xoay ảnh
    if goc != 0:
        h_moi, w_moi = img_color.shape[:2]
        tam = (w_moi // 2, h_moi // 2) # Lấy tâm bức ảnh
        
        # Tạo ma trận xoay
        matrix = cv2.getRotationMatrix2D(tam, goc, 1.0)
        img_final = cv2.warpAffine(img_color, matrix, (w_moi, h_moi))
    else:
        # Nếu góc = 0 thì không cần xoay
        img_final = img_color
    # Bước 5: Chuyển hệ màu 
    if he_mau == "Ảnh Xám (Grayscale)":
        img_final = cv2.cvtColor(img_final, cv2.COLOR_RGB2GRAY)
    elif he_mau == "Hệ màu HSV":
        img_final = cv2.cvtColor(img_final, cv2.COLOR_RGB2HSV)

    # HIỂN THỊ LÊN WEB VÀ TẢI VỀ
    
    cot_trai, cot_phai = st.columns(2)
    with cot_trai:
        st.write("Ảnh ban đầu")
        st.image(img, use_container_width=True)
    with cot_phai:
        st.write("Ảnh đã sửa")
        st.image(img_final, use_container_width=True)

    # chuyển ảnh thành dạng Bytes để cho tải về
    buf = io.BytesIO()
    Image.fromarray(img_final).save(buf, format="PNG")
    
    st.download_button(
        label="Tải ảnh về", 
        data=buf.getvalue(), 
        file_name="anh_da_sua.png", 
        mime="image/png"
    )
