// Файл для интерактивных функций сайта

document.addEventListener('DOMContentLoaded', function() {
    // Обработчик для мобильного меню
    const menuToggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });
    }
    
    // Обработчик для карточек to-do list
    const todoItems = document.querySelectorAll('.todo-item');
    
    todoItems.forEach(item => {
        item.addEventListener('click', function() {
            this.classList.toggle('expanded');
            
            // Находим детальное описание внутри карточки
            const details = this.querySelector('.todo-details');
            
            if (details) {
                if (this.classList.contains('expanded')) {
                    details.style.maxHeight = details.scrollHeight + 'px';
                } else {
                    details.style.maxHeight = '0';
                }
            }
        });
    });
    
    // Обработчик для вкладок в разделе рекомендаций
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Удаляем активный класс у всех кнопок
            tabButtons.forEach(btn => btn.classList.remove('active'));
            
            // Добавляем активный класс нажатой кнопке
            this.classList.add('active');
            
            // Скрываем все контенты вкладок
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Показываем нужный контент
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Плавная прокрутка для якорных ссылок
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Учитываем высоту хедера
                    behavior: 'smooth'
                });
                
                // Закрываем мобильное меню при переходе
                if (mobileMenu && mobileMenu.classList.contains('active')) {
                    mobileMenu.classList.remove('active');
                    menuToggle.classList.remove('active');
                }
            }
        });
    });
});
