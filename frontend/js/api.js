// Địa chỉ Backend
const API_URL = "https://homestay-project-5svy.onrender.com/api";
//Hàm tiện ích
//Lấy token từ localStorage
function getToken(){
    return localStorage.getItem("token");
}

//Tạo header có kèm token
function authHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${getToken()}`
    };
}

//AUTH API
async function apiRegister(fullName, email, password) {
    const res = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            full_name: fullName,
            email: email,
            password: password
        })
    });
    return res.json();
}

async function apiLogin(email, password) {
    const res = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });
    return res.json();
}

async function apiGetMe() {
    const res = await fetch(`${API_URL}/auth/me`, {
        headers: authHeaders()
    });
    return res.json();
}

// =====================
// ROOMS API
// =====================

async function apiGetRooms() {
    const res = await fetch(`${API_URL}/rooms/`);
    return res.json();
}

async function apiGetRoom(roomId) {
    const res = await fetch(`${API_URL}/rooms/${roomId}`);
    return res.json();
}

async function apiCreateRoom(roomData) {
    const res = await fetch(`${API_URL}/rooms/`, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify(roomData)
    });
    return res.json();
}

async function apiUpdateRoom(roomId, roomData) {
    const res = await fetch(`${API_URL}/rooms/${roomId}`, {
        method: "PUT",
        headers: authHeaders(),
        body: JSON.stringify(roomData)
    });
    return res.json();
}

async function apiDeleteRoom(roomId) {
    const res = await fetch(`${API_URL}/rooms/${roomId}`, {
        method: "DELETE",
        headers: authHeaders()
    });
    return res.json();
}

// =====================
// BOOKINGS API
// =====================

async function apiCreateBooking(bookingData) {
    const res = await fetch(`${API_URL}/bookings/`, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify(bookingData)
    });
    return res.json();
}

async function apiGetMyBookings() {
    const res = await fetch(`${API_URL}/bookings/my-bookings`, {
        headers: authHeaders()
    });
    return res.json();
}

async function apiGetAllBookings() {
    const res = await fetch(`${API_URL}/bookings/`, {
        headers: authHeaders()
    });
    return res.json();
}

async function apiUpdateBooking(bookingId, status) {
    const res = await fetch(`${API_URL}/bookings/${bookingId}`, {
        method: "PUT",
        headers: authHeaders(),
        body: JSON.stringify({ status })
    });
    return res.json();
}

async function apiCancelBooking(bookingId) {
    const res = await fetch(`${API_URL}/bookings/${bookingId}`, {
        method: "DELETE",
        headers: authHeaders()
    });
    return res.json();
}

// =====================
// CHAT API
// =====================

async function apiChat(message, history = []) {
    const res = await fetch(`${API_URL}/chat/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, history })
    });
    return res.json();
}