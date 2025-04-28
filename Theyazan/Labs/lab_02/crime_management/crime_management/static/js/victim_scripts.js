// تنفيذ الكود بعد تحميل الصفحة
document.addEventListener('DOMContentLoaded', function () {
    // تأثيرات GSAP للعناصر
    gsap.from('.text-center', { duration: 1, y: -50, opacity: 0, ease: 'back.out(1.7)' });
    gsap.from('.g-3', { duration: 0.8, y: 30, opacity: 0, stagger: 0.1, delay: 0.3, ease: 'power2.out' });

    // التحقق من صحة الحقول أثناء الكتابة
    const form = document.getElementById('victim-form');
    if (!form) return;

    // تحديد الحقول النصية التي يجب ألا تحتوي على أرقام
    const textFields = form.querySelectorAll('input[type="text"][name="full_name"], input[type="text"][name="nickname"]');

    // تحديد الحقول الرقمية
    const numericFields = form.querySelectorAll('input[name="phone"], input[name="age"]');

    // إضافة مستمعات الأحداث للحقول النصية
    textFields.forEach(field => {
        field.addEventListener('input', function () {
            if (/\d/.test(this.value)) {
                showFieldError(this, 'لا يُسمح بإدخال أرقام في هذا الحقل');
                addErrorStyle(this);
            } else {
                removeErrorStyle(this);
            }
        });
    });

    // إضافة مستمعات الأحداث للحقول الرقمية
    numericFields.forEach(field => {
        field.addEventListener('input', function () {
            if (isNaN(this.value) || this.value.trim() === '') {
                showFieldError(this, 'يجب إدخال أرقام فقط في هذا الحقل');
                addErrorStyle(this);
            } else {
                removeErrorStyle(this);
            }
        });
    });

    // التحقق النهائي قبل الإرسال
    form.addEventListener('submit', function (e) {
        let isValid = true;

        // التحقق من الحقول النصية
        textFields.forEach(field => {
            if (/\d/.test(field.value)) {
                showFieldError(field, 'لا يُسمح بإدخال أرقام في هذا الحقل');
                addErrorStyle(field);
                isValid = false;
            }
        });

        // التحقق من الحقول الرقمية
        numericFields.forEach(field => {
            if (isNaN(field.value) || field.value.trim() === '') {
                showFieldError(field, 'يجب إدخال أرقام فقط في هذا الحقل');
                addErrorStyle(field);
                isValid = false;
            }
        });

        if (!isValid) {
            e.preventDefault();
            Swal.fire({
                icon: 'error',
                title: 'خطأ في الإدخال',
                text: 'يوجد أخطاء في بعض الحقول، يرجى تصحيحها',
                customClass: {
                    popup: 'swal2-popup-arabic'
                }
            });
        }
    });

    // وظائف المساعدة
    function showFieldError(field, message) {
        const errorElement = field.nextElementSibling;
        if (errorElement && errorElement.classList.contains('text-danger')) {
            errorElement.textContent = message;
        } else {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'text-danger mt-2';
            errorDiv.textContent = message;
            field.parentNode.insertBefore(errorDiv, field.nextSibling);
        }
    }

    function addErrorStyle(field) {
        field.style.borderColor = 'var(--danger-color)';
        field.style.boxShadow = '0 0 0 3px rgba(220, 53, 69, 0.25)';
        gsap.to(field, { duration: 0.6, x: [-5, 5, -3, 3, 0], ease: 'power1.out' });
    }

    function removeErrorStyle(field) {
        field.style.borderColor = '';
        field.style.boxShadow = '';
        const errorElement = field.nextElementSibling;
        if (errorElement && errorElement.classList.contains('text-danger')) {
            errorElement.remove();
        }
    }
});