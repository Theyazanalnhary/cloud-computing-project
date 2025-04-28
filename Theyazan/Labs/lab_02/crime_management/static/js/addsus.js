// script.js

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const inputs = form.querySelectorAll('input, select, textarea');

    // إضافة تأثيرات لحظية عند التركيز
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.style.borderColor = 'var(--primary-color)';
            input.style.boxShadow = '0 0 10px rgba(0, 123, 255, 0.2)';
        });

        input.addEventListener('blur', () => {
            input.style.borderColor = '#ddd';
            input.style.boxShadow = 'none';
        });
    });

    // التحقق من صحة النموذج قبل الإرسال
    form.addEventListener('submit', function (event) {
        let isValid = true;

        inputs.forEach(input => {
            const errorMessage = input.nextElementSibling;

            if (!input.value.trim()) {
                isValid = false;
                input.style.borderColor = 'var(--danger-color)';

                if (errorMessage && errorMessage.classList.contains('error-message')) {
                    errorMessage.textContent = 'هذا الحقل مطلوب';
                    errorMessage.style.display = 'block';
                }

                // تأثير الهزة عند الخطأ
                input.parentElement.classList.add('shake');
                setTimeout(() => {
                    input.parentElement.classList.remove('shake');
                }, 500);
            } else {
                input.style.borderColor = '#ddd';

                if (errorMessage && errorMessage.classList.contains('error-message')) {
                    errorMessage.style.display = 'none';
                }
            }
        });

        if (!isValid) {
            event.preventDefault(); // منع الإرسال إذا كانت هناك أخطاء
        }
    });
});