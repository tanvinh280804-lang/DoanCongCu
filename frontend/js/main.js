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
        "cancelled": { text: "Đã hủy",       color: "#ef4444", bg: "#fee2e2" }
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