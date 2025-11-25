document.addEventListener("DOMContentLoaded", function () {
    let likeBtn = document.querySelector(".action-btn-like");
    if (!likeBtn) return;

    likeBtn.addEventListener("click", function (e) {
        e.preventDefault();

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const csrftoken = getCookie('csrftoken');

        fetch(`/post/${likeBtn.dataset.postSlug}/toggle_like/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest"
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    likeBtn.classList.add("liked");
                } else {
                    likeBtn.classList.remove("liked");
                }
                likeBtn.querySelector("span").innerText = data.likes_count;
            })
            .catch(error => console.error("Error:", error));
    });
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // بررسی تطابق نام کوکی
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// روی همه دکمه‌های ذخیره گوش بده
document.addEventListener('DOMContentLoaded', function () {
    const saveButtons = document.querySelectorAll('.action-btn-save');

    saveButtons.forEach(button => {
        button.addEventListener('click', function () {
            const slug = this.dataset.postSlug;

            fetch(`/post/${slug}/toggle_save/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('خطا در پاسخ سرور!');
                    }
                    return response.json();
                })
                .then(data => {
                    const icon = this.querySelector('i');

                    if (data.saved) {
                        this.classList.add('saved');
                        if (icon) icon.classList.replace('bi-bookmark', 'bi-bookmark-fill');
                    } else {
                        this.classList.remove('saved');
                        if (icon) icon.classList.replace('bi-bookmark-fill', 'bi-bookmark');
                    }
                })
                .catch(error => {
                    console.error('مشکل رخ داده:', error);
                });
        });
    });
});