// =====================
// HIỂN THỊ THÔNG BÁO
// =====================

function showAlert(elementId, message, type = "error") {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.textContent = message;
    el.className = `alert alert-${type}`;
    el.style.display = "block";

    // Tự động ẩn sau 5 giây
    setTimeout(() => {
        el.style.display = "none";
    }, 5000);
}

function hideAlert(elementId) {
    const el = document.getElementById(elementId);
    if (el) el.style.display = "none";
}

// =====================
// FORMAT DỮ LIỆU
// =====================

// Format tiền Việt Nam
function formatPrice(price) {
    return price.toLocaleString("vi-VN") + "đ";
}

// Format ngày tháng
function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString("vi-VN", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric"
    });
}

// Format trạng thái booking
function formatStatus(status) {
    const map = {
        "pending":   { text: "Chờ xác nhận", color: "#f59e0b", bg: "#fef3c7" },
        "confirmed": { text: "Đã xác nhận",  color: "#10b981", bg: "#d1fae5" },
        "cancelled": { text: "Đã hủy",       color: "#ef4444", bg: "#fee2e2" },
        "checked_out":  { text: "Đã trả phòng", color: "#6366f1", bg: "#ede9fe" }
    };
    const s = map[status] || { text: status, color: "#64748b", bg: "#f1f5f9" };
    return `<span style="
        background:${s.bg}; 
        color:${s.color}; 
        padding:4px 12px; 
        border-radius:20px; 
        font-size:0.8rem;
        font-weight:600;
    ">${s.text}</span>`;
}

// =====================
// KIỂM TRA FORM
// =====================

function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validatePhone(phone) {
    return /^[0-9]{10,11}$/.test(phone);
}

function validateDate(dateStr) {
    const date = new Date(dateStr);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return date >= today;
}

function validateDateRange(checkIn, checkOut) {
    return new Date(checkOut) > new Date(checkIn);
}

// =====================
// TÍNH SỐ ĐÊM VÀ TIỀN
// =====================

function calculateNights(checkIn, checkOut) {
    const diff = new Date(checkOut) - new Date(checkIn);
    return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

function calculateTotal(checkIn, checkOut, pricePerNight) {
    const nights = calculateNights(checkIn, checkOut);
    return nights * pricePerNight;
}

// =====================
// LOADING STATE
// =====================

function setLoading(buttonId, isLoading, originalText) {
    const btn = document.getElementById(buttonId);
    if (!btn) return;
    btn.disabled = isLoading;
    btn.textContent = isLoading ? "Đang xử lý..." : originalText;
}

// =====================
// LẤY THAM SỐ TRÊN URL
// =====================

function getUrlParam(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
}

// =====================
// HIỂN THỊ MODAL XÁC NHẬN
// =====================

function confirmAction(message, onConfirm) {
    if (window.confirm(message)) {
        onConfirm();
    }
}

// =====================
// TOAST NOTIFICATION
// =====================
function showToast(message, type = "success") {
    // Tạo container nếu chưa có
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        container.style.cssText = `
            position: fixed;
            top: 24px;
            right: 24px;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 12px;
        `;
        document.body.appendChild(container);
    }

    const colors = {
        success: { bg: "#10b981", icon: "✓" },
        error: { bg: "#ef4444", icon: "✕" },
        info: { bg: "#6366f1", icon: "ℹ" }
    };
    const c = colors[type] || colors.success;

    const toast = document.createElement("div");
    toast.style.cssText = `
        background: white;
        border-left: 5px solid ${c.bg};
        border-radius: 10px;
        padding: 16px 20px;
        min-width: 280px;
        max-width: 360px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 12px;
        animation: slideInToast 0.3s ease;
        font-weight: 600;
        color: #1e293b;
    `;
    toast.innerHTML = `
        <div style="
            width: 28px; height: 28px;
            background: ${c.bg};
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            flex-shrink: 0;
        ">${c.icon}</div>
        <div style="flex:1; font-size:0.95rem;">${message}</div>
    `;

    container.appendChild(toast);

    // Tự động ẩn sau 3 giây
    setTimeout(() => {
        toast.style.animation = "slideOutToast 0.3s ease forwards";
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Thêm animation CSS
const toastStyle = document.createElement("style");
toastStyle.textContent = `
@keyframes slideInToast {
    from { transform: translateX(120%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
@keyframes slideOutToast {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(120%); opacity: 0; }
}
`;
document.head.appendChild(toastStyle);