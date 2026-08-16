import streamlit as st
import google.generativeai as genai

# Cấu hình trang
st.set_page_config(
    page_title="Hệ Thống AI Chấm Bài Ngữ Văn", 
    page_icon="📝", 
    layout="centered"
)

st.title("📝 HỆ THỐNG AI CHẤM BÀI NGỮ VĂN")
st.write("Hệ thống trợ giảng AI hỗ trợ học sinh tự chấm và nhận xét bài làm văn trực tuyến.")

# Khung nhập liệu
de_bai = st.text_area("Nhập đề bài Ngữ văn:", placeholder="Ví dụ: Nghị luận xã hội về lòng nhân ái...")
bai_lam = st.text_area("Nhập bài làm của học sinh:", placeholder="Dán toàn bộ bài văn của em vào đây...", height=200)

# Xử lý khi nhấn nút
if st.button("🚀 Bắt đầu chấm bài", type="primary"):
    if not de_bai or not bai_lam:
        st.warning("Vui lòng nhập đầy đủ cả đề bài và bài làm của học sinh!")
    else:
        try:
            with st.spinner("AI đang đọc bài và chấm điểm..."):
                # Gọi API Key từ Streamlit Secrets
                api_key = st.secrets["GEMINI_API_KEY"]
                genai.configure(api_key=api_key)
                
                # Sử dụng model gemini-1.5-flash
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                prompt = (
                    f"Hãy đóng vai một giáo viên Ngữ văn tận tâm, chấm bài theo thang điểm 10. "
                    f"Đề bài: {de_bai}. "
                    f"Bài làm của học sinh: {bai_lam}. "
                    "Hãy cho biết điểm số và đưa ra nhận xét chi tiết, chỉ ra ưu điểm và khuyết điểm."
                )
                
                response = model.generate_content(prompt)
                
                st.success("Đã chấm bài thành công!")
                st.subheader("Kết quả từ Giáo viên AI:")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")
            st.info("Hãy kiểm tra lại xem bạn đã nhập đúng 'GEMINI_API_KEY' trong phần Secrets của Streamlit Cloud chưa nhé.")

