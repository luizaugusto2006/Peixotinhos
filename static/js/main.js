document.addEventListener('DOMContentLoaded', function () {

    // Auto-dismiss flash messages
    document.querySelectorAll('.flash').forEach(function (el) {
        setTimeout(function () {
            el.style.opacity = '0';
            el.style.transform = 'translateY(-10px)';
            setTimeout(function () { el.remove(); }, 300);
        }, 5000);
    });

    // File input label update
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

    // Confirm delete actions
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            if (!confirm(this.dataset.confirm || 'Tem certeza?')) {
                e.preventDefault();
            }
        });
    });

    // Scroll to #eventos
    if (window.location.hash === '#eventos') {
        var target = document.getElementById('eventos');
        if (target) {
            setTimeout(function () {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 300);
        }
    }
});
