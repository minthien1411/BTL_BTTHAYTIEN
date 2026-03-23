import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# 1. Cấu hình trang (Để lên đầu file)
st.set_page_config(page_title="Uppic - Trình chỉnh sửa ảnh", layout="wide")

# 2. Custom CSS để tái tạo giao diện y hệt ảnh
st.markdown("""
<style>
.main { background-color: white; }
.header {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px 0;
    background-color: #A3E9FF; /* Xanh cyan nhạt */
    color: #5B97FF;
    font-family: 'Segoe UI', sans-serif;
    margin-bottom: 50px;
}
.logo { font-weight: bold; font-size: 30px; }

/* CSS cho trang Editor ( image_4.png ) */
.control-panel {
    background-color: #F5F5F5; /* Xám nhạt */
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 100%;
    max-width: 350px;
    margin: auto;
}
.control-item {
    display: flex;
    align-items: center;
    gap: 20px;
}
.control-icon {
    width: 35px;
    height: 35px;
}
.image-label {
    color: black;
    font-size: 20px;
    font-weight: 500;
    width: 70px;
    text-align: right;
    margin-right: 20px;
}
.image-wrapper {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 30px;
}

/* Tái cấu trúc CSS cho nút Xuất ảnh */
div.stDownloadButton > button {
    background-color: #6EB4FF !important;
    color: black !important;
    border: none !important;
    padding: 10px 40px !important;
    font-weight: bold !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
}

/* CSS cho uploader trang chủ */
.stFileUploader section {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# 3. Header
st.markdown('<div class="header"><div class="logo">💠 Uppic</div></div>', unsafe_allow_html=True)

# 4. Quản lý trạng thái: Kiểm tra đã có ảnh chưa
if 'image_ready' not in st.session_state:
    st.session_state.image_ready = False

# 5. --- Bắt đầu phân chia giao diện ---

uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if not st.session_state.image_ready:
    # --- Trang chủ: Tải ảnh ( Giao diện y hệt image_3.png nhưng không nét đứt ) ---
    
    col_home_1, col_home_2 = st.columns([1, 1])
    with col_home_1:
        st.markdown("""
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%;">
                <div style="background-color: #6EB4FF; width: 150px; height: 150px; border-radius: 50%; display: flex; justify-content: center; align-items: center; box-shadow: 0 15px 35px rgba(110, 180, 255, 0.3); margin-bottom: 30px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/3342/3342137.png" width="70" style="filter: brightness(0) invert(1);">
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_home_2:
        st.markdown("""
            <div style="padding-top: 100px;">
                <div style="color: #5B97FF; font-size: 50px; font-weight: 900; line-height: 1.1; margin-bottom: 20px;">Trang chỉnh sửa ảnh Đa phương tiện<br>đơn giản hơn bao giờ hết</div>
                <div style="color: #888; font-size: 20px; max-width: 600px; margin-bottom: 40px;">
                    Chào mừng bạn đến với <b>Uppic</b> - Sản phẩm Bài tập lớn nhóm 10.<br>
                    Tải một bức ảnh lên để bắt đầu trải nghiệm sức mạnh của xử lý ảnh số thời gian thực.
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.info("💡 Bấm vào cái nút ở trên đầu hoặc kéo ảnh vào để bắt đầu nhé!")

    # Nếu có file mới, đọc ảnh và chuyển trạng thái
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.session_state.img_array = np.array(image) # Lưu ảnh vào session
        st.session_state.image_ready = True
        st.rerun() # Nạp lại trang để chuyển giao diện

else:
    # --- Trang chỉnh sửa: Editor ( Giao diện image_4.png ) ---
    
    # Bố cục 2 cột (Tỷ lệ 1:2)
    col_ctrl, col_img = st.columns([1, 2])
    
    # 1. Bảng điều khiển (Cột 1)
    with col_ctrl:
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        
        # Thanh 1: Bộ lọc (Icon phễu)
        st.markdown('<div class="control-item">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/107/107831.png", width=30) # Icon phễu
        f_style = st.select_slider("", options=["Gốc", "Vintage", "Cyberpunk"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        # Thanh 2: Độ tương phản (α)
        st.markdown('<div class="control-item">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/32/32381.png", width=30) # Vòng tròn chia đôi
        alpha = st.slider("", 1.0, 3.0, 1.0, step=0.1, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        # Thanh 3: Độ sáng (β)
        st.markdown('<div class="control-item">', unsafe_allow_html=True)
        st.image("https://vn.freepik.com/bieu-tuong/sun_18764257#fromView=search&page=1&position=7&uuid=960c94c5-84ef-445e-b45d-3fd24bece604", width=30) # Mặt trời
        beta = st.slider("", -100, 100, 0, step=1, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        # Thanh 4: Nhiễu
        st.markdown('<div class="control-item">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/117/117150.png", width=30) # Dấu chấm
        noise_level = st.slider("", 0.0, 0.2, 0.0, step=0.01, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # 2. Hiển thị ảnh (Cột 2)
    with col_img:
        img_array = st.session_state.img_array
        
        # --- THUẬT TOÁN XỬ LÝ (SÁNG/TỐI + FILTER + NHIỄU) ---
        # A. Chỉnh sáng/tương phản
        processed = cv2.convertScaleAbs(img_array, alpha=alpha, beta=beta)
        
        # B. Áp dụng bộ lọc
        if f_style == "Vintage":
            processed[:,:,0] = cv2.addWeighted(processed[:,:,0], 1.2, 0, 0, 15)
            processed = cv2.GaussianBlur(processed, (3,3), 0)
        elif f_style == "Cyberpunk":
            processed[:,:,1] = cv2.multiply(processed[:,:,1], 0.7) # Giảm xanh lá
            processed[:,:,2] = cv2.addWeighted(processed[:,:,2], 1.4, 0, 0, 25) # Tăng xanh dương
            
        # C. Thêm nhiễu muối tiêu
        if noise_level > 0.0:
            output = np.copy(processed)
            num_salt = np.ceil(noise_level * processed.size * 0.5)
            coords = [np.random.randint(0, i - 1, int(num_salt)) for i in processed.shape]
            output[tuple(coords)] = 255
            num_pepper = np.ceil(noise_level * processed.size * 0.5)
            coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in processed.shape]
            output[tuple(coords)] = 0
            processed = output

        # Hiển thị ảnh "Trước"
        st.markdown('<div class="image-wrapper"><div class="image-label">Trước</div>', unsafe_allow_html=True)
        st.image(img_array, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Hiển thị ảnh "Sau"
        st.markdown('<div class="image-wrapper"><div class="image-label">Sau</div>', unsafe_allow_html=True)
        st.image(processed, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 3. Nút xuất ảnh (Dưới cùng ở giữa)
        # Chuyển ảnh kết quả sang định dạng có thể tải về
        from io import BytesIO
        result_pil = Image.fromarray(processed)
        buf = BytesIO()
        result_pil.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.markdown('<p style="text-align: center; margin-top: 30px;">', unsafe_allow_html=True)
        st.download_button(
            label="Xuất ảnh",
            data=byte_im,
            file_name="result_uppic.png",
            mime="image/png"
        )
        st.markdown('</p>', unsafe_allow_html=True)

    # Thêm Histogram vào thanh bên để thầy Tiến chấm
    if st.sidebar.checkbox("Bật Histogram phân tích", value=False):
        st.sidebar.markdown("### 📊 Lược đồ mức xám")
        gray = cv2.cvtColor(processed, cv2.COLOR_RGB2GRAY)
        fig, ax = plt.subplots()
        ax.hist(gray.ravel(), bins=256, range=[0, 256], color='#5B97FF', alpha=0.8)
        ax.axis('off') # Tắt trục cho đẹp
        st.sidebar.pyplot(fig)
        st.sidebar.info("Biểu đồ phân bố các mức sáng trong ảnh.")
