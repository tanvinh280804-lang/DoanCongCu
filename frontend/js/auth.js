// =====================
// LƯU VÀ XÓA TOKEN
// =====================

function saveToken(token) {
    localStorage.setItem("token", token);
}

function removeToken() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
}

function saveUser(user) {
    localStorage.setItem("user", JSON.stringify(user));
}

function getUser() {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
}

function isLoggedIn() {
    return !!getToken();
}

function isAdmin() {
    const user = getUser();
    return user && user.is_admin === true;
}

// =====================
// ĐĂNG NHẬP
// =====================

async function handleLogin(email, password) {
    try {
        const data = await apiLogin(email, password);

        if (data.access_token) {
            saveToken(data.access_token);

            // Tạo user tạm từ email nếu getMe lỗi
            // Tạo user tạm từ email nếu getMe lỗi
        let user = { email: email, full_name: email.split('@')[0], is_admin: false };

        try {
        const me = await apiGetMe();
        if (me && me.id) {
            user = me;
        }
           } catch(e) {
              console.log("GetMe error:", e);
        }

            saveUser(user);

            // Chuyển hướng
            if (user.is_admin) {
                window.location.href = "dashboard.html";
            } else {
                window.location.href = "index.html";
            }
            return null;
        } else {
            return data.detail || "Email hoặc mật khẩu không đúng";
        }
    } catch (err) {
        console.log("Login error:", err);
        return "Lỗi kết nối server, vui lòng thử lại";
    }

    // Thông báo đăng nhập thành công
        showToast("Đăng nhập thành công! Chào mừng bạn trở lại 🎉", "success");
}

// =====================
// ĐĂNG KÝ
// =====================

async function handleRegister(fullName, email, password) {
    try {
        const data = await apiRegister(fullName, email, password);

        if (data.id) {
            // Đăng ký xong tự động đăng nhập và vào trang chủ
            await handleLogin(email, password);
            return null;
        } else {
            return data.detail || "Đăng ký thất bại";
        }
    } catch (err) {
        return "Lỗi kết nối server, vui lòng thử lại";
    }
}

// =====================
// ĐĂNG XUẤT
// =====================

function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    // Xóa hết localStorage cho chắc
    localStorage.clear();
    window.location.href = "index.html";
}

// =====================
// BẢO VỆ TRANG
// =====================

// Dùng cho trang cần đăng nhập
function requireLogin() {
    if (!isLoggedIn()) {
        window.location.href = "login.html";
    }
}

// Dùng cho trang chỉ admin mới vào được
function requireAdmin() {
    if (!isLoggedIn()) {
        window.location.href = "login.html";
        return;
    }
    if (!isAdmin()) {
        window.location.href = "index.html";
    }
}

// Cập nhật navbar theo trạng thái đăng nhập
function updateNavbar() {
    const user = getUser();
    const navAuth = document.getElementById("nav-auth");
    if (!navAuth) return;

    if (user) {
        navAuth.innerHTML = `
            ${!user.is_admin ? '<a href="my-bookings.html" class="nav-link">Booking của tôi</a>' : ''}
            <span class="nav-user">Xin chào, ${user.full_name}</span>
            ${user.is_admin ? '<a href="dashboard.html" class="nav-link">Dashboard</a>' : ''}
            <a href="javascript:void(0)" onclick="handleLogout()" class="nav-link btn-logout">Đăng xuất</a>
        `;
    } else {
        navAuth.innerHTML = `
            <a href="login.html" class="nav-link">Đăng nhập</a>
            <a href="register.html" class="nav-link btn-register">Đăng ký</a>
        `;
    }
}

async function checkTokenValid() {
    if (!isLoggedIn()) return;
    
    try {
        const user = await apiGetMe();
        if (!user || user.detail) {
            // Token hết hạn hoặc không hợp lệ
            localStorage.clear();
            window.location.reload();
        } else {
            saveUser(user);
        }
    } catch(e) {
        localStorage.clear();
        window.location.reload();
    }
}