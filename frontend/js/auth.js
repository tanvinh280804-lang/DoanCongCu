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

function showToast(message) {
    const toast = document.createElement("div");
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #4CAF50;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        z-index: 9999;
        font-size: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// =====================
// ĐĂNG NHẬP
// =====================

async function handleLogin(email, password, redirect = true) {
    try {
        const data = await apiLogin(email, password);

        if (data.access_token) {
            saveToken(data.access_token);

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

            // Chỉ redirect khi gọi từ trang login
            if (redirect) {
                showToast("Đăng nhập thành công! Chào mừng bạn trở lại 🎉");
                setTimeout(() => {
                    if (user.is_admin) {
                        window.location.replace("dashboard.html");
                    } else {
                        window.location.replace("index.html");
                    }
                }, 1500);
            }

            return null;
        } else {
            return data.detail || "Email hoặc mật khẩu không đúng";
        }
    } catch (err) {
        console.log("Login error:", err);
        return "Lỗi kết nối server, vui lòng thử lại";
    }
}

// =====================
// ĐĂNG KÝ
// =====================

async function handleRegister(fullName, email, password) {
    try {
        const data = await apiRegister(fullName, email, password);

        if (data.id) {
            // Đăng nhập nhưng không redirect, để register.html tự redirect
            await handleLogin(email, password, false);
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
    localStorage.clear();
    window.location.href = "index.html";
}

// =====================
// BẢO VỆ TRANG
// =====================

function requireLogin() {
    if (!isLoggedIn()) {
        window.location.href = "login.html";
    }
}

function requireAdmin() {
    if (!isLoggedIn()) {
        window.location.href = "login.html";
        return;
    }
    if (!isAdmin()) {
        window.location.href = "index.html";
    }
}

function updateNavbar() {
    const user = getUser();
    const navAuth = document.getElementById("nav-auth");
    if (!navAuth) return;

    if (user) {
        navAuth.innerHTML = `
            ${!user.is_admin ? '<a href="my-bookings.html" class="nav-link">Booking của tôi</a>' : ''}
            <span class="nav-user">Xin chào, ${user.full_name}</span>
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