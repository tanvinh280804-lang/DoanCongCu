from groq import Groq
from app.config import settings

client = Groq(api_key=settings.groq_api_key)


def get_chat_response(message: str, chat_history: list = [], room_info: str = "") -> str:
    try:
        system_prompt = f"""Bạn là trợ lý AI của homestay. Nhiệm vụ của bạn là:
- Tư vấn thông tin phòng, giá cả, tiện nghi
- Hỗ trợ khách đặt phòng
- Trả lời các câu hỏi về chính sách check-in, check-out
- Giới thiệu các địa điểm du lịch gần homestay
Hãy trả lời thân thiện, ngắn gọn và bằng tiếng Việt.

QUAN TRỌNG:
- Khi liệt kê phòng theo giá, phải liệt kê ĐÚNG và ĐẦY ĐỦ, không được bỏ sót hoặc nhầm lẫn.
- Phòng dưới 1 triệu: giá < 1,000,000đ (ví dụ: 450,000đ, 650,000đ, 850,000đ đều là dưới 1 triệu)
- Phòng trên 1 triệu: giá > 1,000,000đ (ví dụ: 1,200,000đ, 20,000,000đ là trên 1 triệu)
- 850,000đ < 1,000,000đ nên thuộc nhóm DƯỚI 1 triệu, KHÔNG thuộc nhóm trên 1 triệu.
- Hãy so sánh số học chính xác trước khi trả lời.

DANH SÁCH PHÒNG HIỆN CÓ:
{room_info}

Chỉ tư vấn dựa trên danh sách phòng trên, không bịa thêm phòng khác."""

        messages = [{"role": "system", "content": system_prompt}]

        for chat in chat_history:
            messages.append({
                "role": chat["role"],
                "content": chat["content"]
            })

        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            max_tokens=2000,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Xin lỗi, tôi đang gặp sự cố. Lỗi: {str(e)}"