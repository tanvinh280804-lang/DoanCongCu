// Hiển thị sao (dùng để show rating, không tương tác)
function renderStars(rating) {
    let html = "";
    for (let i = 1; i <= 5; i++) {
        html += i <= rating ? "★" : "☆";
    }
    return `<span style="color:#f59e0b; letter-spacing:2px;">${html}</span>`;
}

// Tải và hiển thị danh sách đánh giá của 1 phòng vào 1 container
async function loadRoomReviews(roomId, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const reviews = await apiGetRoomReviews(roomId);

    if (!Array.isArray(reviews) || reviews.length === 0) {
        container.innerHTML = `<p style="color:#94a3b8; text-align:center; padding:16px;">Chưa có đánh giá nào cho phòng này</p>`;
        return;
    }

    const avg = (reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length).toFixed(1);

    container.innerHTML = `
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:16px;">
            <span style="font-size:1.5rem; font-weight:700;">${avg}</span>
            ${renderStars(Math.round(avg))}
            <span style="color:#64748b;">(${reviews.length} đánh giá)</span>
        </div>
        ${reviews.map(r => `
            <div style="border-top:1px solid #e2e8f0; padding:12px 0;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    ${renderStars(r.rating)}
                    <span style="color:#94a3b8; font-size:0.85rem;">${formatDate(r.created_at)}</span>
                </div>
                <p style="color:#334155;">${r.comment || ""}</p>
            </div>
        `).join("")}
    `;
}

// Gắn 1 form đánh giá (sao bấm được + textarea) vào container, dùng cho booking đã checked_out
function renderReviewForm(bookingId, containerId, onSuccess) {
    const container = document.getElementById(containerId);
    if (!container) return;

    let selectedRating = 5;

    container.innerHTML = `
        <div style="background:#f8fafc; border-radius:8px; padding:16px;">
            <label style="display:block; margin-bottom:8px; font-weight:600;">Đánh giá của bạn</label>
            <div id="star-picker-${bookingId}" style="font-size:1.8rem; cursor:pointer; margin-bottom:12px;">
                ${[1,2,3,4,5].map(i => `<span data-val="${i}" style="color:#f59e0b;">★</span>`).join("")}
            </div>
            <textarea id="review-comment-${bookingId}" placeholder="Chia sẻ trải nghiệm của bạn..."
                style="width:100%; padding:10px; border:1px solid #cbd5e1; border-radius:6px; min-height:80px;"></textarea>
            <button class="btn btn-primary" style="margin-top:12px;"
                onclick="submitReview(${bookingId}, '${containerId}')">Gửi đánh giá</button>
        </div>
    `;

    const stars = container.querySelectorAll(`#star-picker-${bookingId} span`);
    function paintStars(val) {
        stars.forEach(s => s.style.opacity = s.dataset.val <= val ? "1" : "0.3");
    }
    paintStars(selectedRating);
    stars.forEach(s => {
        s.addEventListener("click", () => {
            selectedRating = parseInt(s.dataset.val);
            paintStars(selectedRating);
        });
    });

    window[`__reviewSuccess_${bookingId}`] = onSuccess;
}

async function submitReview(bookingId, containerId) {
    const comment = document.getElementById(`review-comment-${bookingId}`).value.trim();
    const stars = document.querySelectorAll(`#star-picker-${bookingId} span`);
    let rating = 5;
    stars.forEach(s => { if (s.style.opacity === "1") rating = parseInt(s.dataset.val); });

    const data = await apiCreateReview(bookingId, rating, comment);

    if (data.id) {
        const container = document.getElementById(containerId);
        container.innerHTML = `<p style="color:#065f46; text-align:center; padding:12px;">✅ Cảm ơn bạn đã đánh giá!</p>`;
        showToast("Gửi đánh giá thành công! ⭐", "success");
        const cb = window[`__reviewSuccess_${bookingId}`];
        if (typeof cb === "function") cb();
    } else {
        showToast(data.detail || "Không thể gửi đánh giá", "error");
    }
}