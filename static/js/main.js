(function () {
    'use strict'
    var forms = document.querySelectorAll('form')
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
        })
})()


const likeBtn = document.getElementById("likeBtn");
const likeCount = document.getElementById("likeCount");
let liked = false;
likeBtn.addEventListener("click", () => {
    liked = !liked;
    likeBtn.classList.toggle("liked");
    const count = parseInt(likeCount.textContent);
    likeCount.textContent = liked ? count + 1 : count - 1;
});

$("#commentForm").on("submit", function (e) {
    e.preventDefault();
    let name = $("#name");
    let email = $("#email");
    let message = $("#message");

    let valid = true;
    const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;

    if (name.val().trim().length < 3) {
        name.addClass("is-invalid"); valid = false;
    } else { name.removeClass("is-invalid").addClass("is-valid"); }

    if (!emailRegex.test(email.val().trim())) {
        email.addClass("is-invalid"); valid = false;
    } else { email.removeClass("is-invalid").addClass("is-valid"); }

    if (message.val().trim().length === 0) {
        message.addClass("is-invalid"); valid = false;
    } else { message.removeClass("is-invalid").addClass("is-valid"); }

    if (!valid) return;
    alert("دیدگاه شما با موفقیت ارسال شد ✅");
    this.reset();
    $(".form-control").removeClass("is-valid");
});