document.addEventListener('DOMContentLoaded', function () {

    // ── Navbar scroll effect (glass → solid) ──────────────
    var navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // ── Back to top button ────────────────────────────────
    var backToTop = document.getElementById('backToTop');
    if (backToTop) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 400) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });

        backToTop.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ── Auto-dismiss flash messages ───────────────────────
    document.querySelectorAll('.flash').forEach(function (el) {
        setTimeout(function () {
            el.style.opacity = '0';
            el.style.transform = 'translateY(-10px)';
            setTimeout(function () { el.remove(); }, 300);
        }, 5000);
    });

    // ── File input label update ───────────────────────────
    document.querySelectorAll('input[type="file"]').forEach(function (input) {
        input.addEventListener('change', function () {
            var count = this.files.length;
            if (count > 0) {
                var label = count + ' arquivo(s) selecionado(s)';
                var display = this.parentElement.querySelector('.file-count');
                if (!display) {
                    display = document.createElement('small');
                    display.className = 'file-count';
                    display.style.color = '#0066cc';
                    display.style.fontWeight = '600';
                    this.parentElement.appendChild(display);
                }
                display.textContent = label;
            }
        });
    });

    // ── Skeleton loading for images ───────────────────────
    document.querySelectorAll('.event-cover img, .gallery-item img').forEach(function (img) {
        var parent = img.parentElement;
        if (img.complete) {
            img.style.opacity = '1';
        } else {
            img.style.opacity = '0';
            img.addEventListener('load', function () {
                this.style.opacity = '1';
            });
        }
    });

    // ── Smooth scroll for anchor links ────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
        link.addEventListener('click', function (e) {
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ── Confirm delete actions ────────────────────────────
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            if (!confirm(this.dataset.confirm || 'Tem certeza?')) {
                e.preventDefault();
            }
        });
    });

    // ── Scroll to #eventos ────────────────────────────────
    if (window.location.hash === '#eventos') {
        var target = document.getElementById('eventos');
        if (target) {
            setTimeout(function () {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 300);
        }
    }
});
