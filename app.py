import json
import urllib.request
import streamlit as st

st.set_page_config(
    page_title="AI Chấm Bài Ngữ Văn", page_icon="📝", layout="centered"
)

st.title("📝 HỆ THỐNG AI CHẤM BÀI NGỮ VĂN")
st.write(
    "Hệ thống trợ giảng AI hỗ trợ học sinh tự chấm và nhận xét bài làm văn trực"
    " tuyến."
)

# Khung nhập liệu
de_bai = st.text_area(
    "Nhập đề bài Ngữ văn:",
    placeholder="Ví dụ: Nghị luận xã hội về tình yêu thương...",
)
bai_lam = st.text_area(
    "Nhập bài làm của học sinh:",
    placeholder="Dán toàn bộ bài văn của em vào đây...",
    height=200,
)

if st.button("🚀 Bắt đầu chấm bài", type="primary"):
  if not de_bai or not bai_lam:
    st.warning("Vui lòng nhập đầy đủ cả đề bài và bài làm của học sinh!")
  else:
    with st.spinner(
        "AI đang đọc bài, phân tích và chấm điểm, vui lòng đợi..."
    ):
      try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "qwen2.5",
            "prompt": (
                f"Hãy là giáo viên Ngữ văn giỏi, chấm bài sau theo thang điểm"
                f" 10. Đề bài: {de_bai}. Bài làm học sinh: {bai_lam}. Cho biết"
                " điểm số và nhận xét chi tiết từng tiêu chí."
            ),
            "stream": False,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req) as response:
          res_data = json.loads(response.read().decode("utf-8"))
          st.success("Đã chấm bài thành công!")
          st.subheader("Kết quả từ Giáo viên AI:")
          st.markdown(res_data["response"])

      except Exception as e:
        st.error(
            "Không thể kết nối với AI. Hãy đảm bảo ứng dụng **Gemini API** đang được"
            " mở trên máy tính của bạn!"
        )
