document.addEventListener("DOMContentLoaded", function () {
    // 1. Эффект плавного появления страницы (Fade-in)
    document.body.classList.add("fade-in");

    // 2. Подсветка активной страницы в меню
    const currentUrl = window.location.pathname;
    const navLinks = document.querySelectorAll("nav a");
    
    navLinks.forEach(link => {
        const linkUrl = link.getAttribute("href");
        if (currentUrl === linkUrl) {
            link.classList.add("active");
        }
    });

    // 3. Интерактивная кнопка "Режим тишины"
    const silenceBtn = document.getElementById("silence-btn");
    if (silenceBtn) {
        // Проверяем сохраненное состояние
        if (localStorage.getItem("silenceMode") === "active") {
            enableSilenceMode();
        }

        silenceBtn.addEventListener("click", function () {
            if (localStorage.getItem("silenceMode") === "active") {
                disableSilenceMode();
            } else {
                enableSilenceMode();
            }
        });
    }

    function enableSilenceMode() {
        localStorage.setItem("silenceMode", "active");
        silenceBtn.classList.add("silence-active");
        silenceBtn.innerText = "РЕЖИМ ТИШИНЫ: ВКЛ";
        
        // Включаем «тишину» глобально для всего документа
        document.body.classList.add("silence-mode-active");
    }

    function disableSilenceMode() {
        localStorage.removeItem("silenceMode");
        silenceBtn.classList.remove("silence-active");
        silenceBtn.innerText = "РЕЖИМ ТИШИНЫ: ВЫКЛ";
        
        // Возвращаем привычные цвета и градиенты
        document.body.classList.remove("silence-mode-active");
    }
});