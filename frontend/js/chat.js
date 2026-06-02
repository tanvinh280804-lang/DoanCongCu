// Lưu lịch sử hội thoại
let chatHistory = [];

// =====================
// MỞ / ĐÓNG CHATBOT
// =====================

function toggleChat() {
    const chatBox = document.getElementById("chat-box");
    chatBox.classList.toggle("open");

    // Khi mở chat thì focus vào ô nhập
    if (chatBox.classList.contains("open")) {
        document.getElementById("chat-input").focus();
        scrollChatToBottom();
    }
}

// =====================
// GỬI TIN NHẮN
// =====================

async function sendChat() {
    const input = document.getElementById("chat-input");
    const message = input.value.trim();

    if (!message) return;

    // Xóa ô input
    input.value = "";

    // Hiển thị tin nhắn của user
    appendMessage("user", message);

    // Hiển thị trạng thái đang gõ
    const typingId = showTyping();

    try {
        // Gọi API chatbot
        const data = await apiChat(message, chatHistory);

        // Xóa trạng thái đang gõ
        removeTyping(typingId);

        if (data.reply) {
            // Hiển thị tin nhắn của bot
            appendMessage("bot", data.reply);

            // Lưu vào lịch sử
            chatHistory.push({ role: "user", content: message });
            chatHistory.push({ role: "assistant", content: data.reply });

            // Giới hạn lịch sử 10 tin nhắn gần nhất
            if (chatHistory.length > 20) {
                chatHistory = chatHistory.slice(-20);
            }
        } else {
            appendMessage("bot", "Xin lỗi, tôi không thể trả lời lúc này. Vui lòng thử lại!");
        }
    } catch (err) {
        removeTyping(typingId);
        appendMessage("bot", "Lỗi kết nối. Vui lòng kiểm tra lại!");
    }
}

// =====================
// HIỂN THỊ TIN NHẮN
// =====================

function appendMessage(role, content) {
    const messages = document.getElementById("chat-messages");

    const div = document.createElement("div");
    div.className = `chat-msg ${role}`;
    div.textContent = content;

    messages.appendChild(div);
    scrollChatToBottom();
}

// =====================
// HIỆU ỨNG ĐANG GÕ
// =====================

function showTyping() {
    const messages = document.getElementById("chat-messages");
    const id = "typing-" + Date.now();

    const div = document.createElement("div");
    div.className = "chat-msg bot";
    div.id = id;
    div.innerHTML = `
        <span style="display:inline-flex; gap:4px; align-items:center;">
            <span style="animation: bounce 0.6s infinite">●</span>
            <span style="animation: bounce 0.6s infinite 0.2s">●</span>
            <span style="animation: bounce 0.6s infinite 0.4s">●</span>
        </span>
    `;

    // Thêm animation bounce
    const style = document.createElement("style");
    style.textContent = `
        @keyframes bounce {
            0%, 100% { transform: translateY(0); opacity: 0.4; }
            50% { transform: translateY(-4px); opacity: 1; }
        }
    `;
    document.head.appendChild(style);

    messages.appendChild(div);
    scrollChatToBottom();
    return id;
}

function removeTyping(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// =====================
// CUỘN XUỐNG CUỐI
// =====================

function scrollChatToBottom() {
    const messages = document.getElementById("chat-messages");
    setTimeout(() => {
        messages.scrollTop = messages.scrollHeight;
    }, 50);
}