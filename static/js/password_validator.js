class PasswordValidator {
    constructor(config) {
        // پیکربندی دلخواه (آیدی فیلدها و دکمه و ...)
        this.password     = document.querySelector(config.password);
        this.password2    = document.querySelector(config.password2);
        this.form         = document.querySelector(config.form);
        this.button       = document.querySelector(config.button);
        this.feedback     = document.querySelector(config.feedback);
        this.feedback2    = document.querySelector(config.feedback2);
        this.rules        = config.rules || [
            {id:'length',    check:pwd=>pwd.length>=8,           message:'حداقل ۸ کاراکتر'},
            {id:'uppercase', check:pwd=>/[A-Z]/.test(pwd),    message:'حرف بزرگ (A-Z)'},
            {id:'number',    check:pwd=>/\d/.test(pwd),          message:'عدد (0-9)'},
            {id:'special',   check:pwd=>/[!@#$%^&*()_\-+=\[\]\{\};:'",.<>/?\\|`~]/.test(pwd), message:'کاراکتر ویژه (!,@,...)'},
        ];
        this.statusList = config.statusList || null;    // ul لیست وضعیت رمز اگر هست
        this.init();
    }
    init() {
        if (this.password) {
            this.password.addEventListener('input', () => {
                this.updatePasswordStatus();
                this.updateRepeatStatus();
            });
        }
        if (this.password2) {
            this.password2.addEventListener('input', this.updateRepeatStatus.bind(this));
        }
        if (this.form) {
            this.form.addEventListener('submit', e => {
                this.updatePasswordStatus();
                this.updateRepeatStatus();
                if (this.button && this.button.disabled) e.preventDefault();
            });
        }
        document.addEventListener('DOMContentLoaded', () => {
            if(this.button) this.button.disabled = true;
            if(this.feedback)  this.feedback.style.display = 'none';
            if(this.feedback2) this.feedback2.style.display = 'none';
        });
    }
    updatePasswordStatus() {
        const pwd = this.password.value;
        let allValid = true;
        for(let rule of this.rules) {
            const li = document.getElementById(rule.id);
            const valid = rule.check(pwd);
            if (li) li.className = valid ? 'text-success' : 'text-danger';
            if (!valid) allValid = false;
        }
        if (allValid) {
            this.password.classList.remove('is-invalid');
            this.password.classList.add('is-valid');
            if(this.feedback) this.feedback.style.display = 'none';
        } else {
            this.password.classList.remove('is-valid');
            this.password.classList.add('is-invalid');
            if(this.feedback) this.feedback.style.display = 'block';
        }
        this.updateRegisterBtn();
    }
    updateRepeatStatus = () => {
        if (!this.password2.value) {
            this.password2.classList.remove('is-valid', 'is-invalid');
            if(this.feedback2) this.feedback2.style.display = 'none';
            return;
        }
        if (this.password2.value === this.password.value) {
            this.password2.classList.remove('is-invalid');
            this.password2.classList.add('is-valid');
            if(this.feedback2) this.feedback2.style.display = 'none';
        } else {
            this.password2.classList.remove('is-valid');
            this.password2.classList.add('is-invalid');
            if(this.feedback2) this.feedback2.style.display = 'block';
        }
        this.updateRegisterBtn();
    }
    updateRegisterBtn() {
        let allValid = this.rules.every(rule=>rule.check(this.password.value));
        let repeatValid = this.password2.value === this.password.value && this.password2.value.length>0;
        if(this.button) this.button.disabled = !(allValid && repeatValid);
    }
}
