document.addEventListener('DOMContentLoaded', function() {
    // تبديل القائمة الجانبية
    const sidebar = document.querySelector('.sidebar-custom');
    const toggleButton = document.getElementById('sidebarToggle');
    
    toggleButton.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        
        // حفظ الحالة في localStorage
        localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
    });
    
    // تحميل الحالة المحفوظة
    if (localStorage.getItem('sidebarCollapsed') === 'true') {
        sidebar.classList.add('collapsed');
    }
    
    // تأثيرات الروابط
    const navLinks = document.querySelectorAll('.nav-link-custom');
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(-5px)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });
    
    // تكيف مع الشاشات الصغيرة
    function handleResize() {
        if (window.innerWidth < 992) {
            document.querySelector('.sidebar-toggle-custom').classList.add('sidebar-toggle-mobile');
        } else {
            document.querySelector('.sidebar-toggle-custom').classList.remove('sidebar-toggle-mobile');
        }
    }
    
    window.addEventListener('resize', handleResize);
    handleResize(); // التشغيل الأولي
});