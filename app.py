import streamlit as st
from google import genai

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Hệ Thống AI Chấm Bài Ngữ Văn",
    page_icon="📝",
    layout="centered"
)

st.title("📝 HỆ THỐNG AI CHẤM BÀI NGỮ VĂN")
st.write(
    "Hệ thống trợ giảng AI hỗ trợ học sinh tự chấm "
    "và nhận xét bài làm Ngữ văn."
)

# ==============================
# NHẬP DỮ LIỆU
# ==============================
de_bai = st.text_area(
    "Nhập đề bài Ngữ văn:",
    placeholder="Ví dụ: Nghị luận xã hội về lòng biết ơn..."
)

bai_lam = st.text_area(
    "Nhập bài làm của học sinh:",
    placeholder="Dán toàn bộ bài văn của học sinh vào đây..."
)

# ==============================
# CHẤM BÀI
# ==============================
if st.button("🚀 Bắt đầu chấm bài", type="primary"):

    if not de_bai.strip() or not bai_lam.strip():
        st.warning("⚠️ Vui lòng nhập đầy đủ cả đề bài và bài làm của học sinh.")

    else:
        try:
            with st.spinner("🤖 AI đang đọc bài và chấm điểm..."):

                # Lấy API Key từ Streamlit Secrets
                api_key = st.secrets["GEMINI_API_KEY"]

                # Kết nối Gemini
                client = genai.Client(api_key=api_key)

                # Prompt chấm bài
                prompt = f"""
Bạn là một giáo viên Ngữ văn Việt Nam tận tâm và công bằng.

Hãy chấm bài viết của học sinh dựa trên đề bài và bài làm dưới đây.

ĐỀ BÀI:
{de_bai}

BÀI LÀM CỦA HỌC SINH:
{bai_lam}

Hãy trả lời bằng tiếng Việt và trình bày rõ ràng theo cấu trúc:

1. ĐIỂM SỐ:
- Cho điểm theo thang 10.
- Nêu ngắn gọn lý do cho số điểm.

2. ƯU ĐIỂM:
- Nội dung
- Lập luận
- Dẫn chứng
- Diễn đạt
- Sáng tạo

3. NHƯỢC ĐIỂM:
- Chỉ ra những lỗi hoặc điểm chưa tốt trong bài.
- Nếu có lỗi diễn đạt, chính tả hoặc lập luận thì chỉ rõ.

4. GỢI Ý CẢI THIỆN:
- Đưa ra cách sửa cụ thể để bài viết tốt hơn.

5. NHẬN XÉT CHUNG:
- Nhận xét ngắn gọn, tích cực và phù hợp với học sinh.

Không được bịa dẫn chứng hoặc thông tin không có trong bài.
Hãy chấm công bằng, không quá dễ cũng không quá khắt khe.
"""

                # Gọi Gemini
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                # Hiển thị kết quả
                st.success("✅ Đã chấm bài thành công!")

                st.subheader("📋 Kết quả từ Giáo viên AI")
                st.markdown(response.text)

        except KeyError:
            st.error(
"❌ Chưa tìm thấy GEMINI_API_KEY trong Streamlit Secrets."
            )

        except Exception as e:
            st.error("❌ Hệ thống AI gặp lỗi khi chấm bài.")
            st.code(str(e))
