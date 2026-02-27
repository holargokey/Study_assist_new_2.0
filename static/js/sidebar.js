const sidebar = document.querySelector('.sa-sidebar');
const backdrop = document.querySelector('.sa-backdrop');
const body = document.body;
const openBtn = document.querySelector('.sa-showsidebar');
const closeBtn = document.querySelector('.close-sidebar');

// Open sidebar
openBtn.addEventListener('click', () => {
    sidebar.classList.add('active');
    backdrop.classList.add('active');
    body.style.overflow = 'hidden';
});

// Close sidebar
function closeSidebar() {
    sidebar.classList.remove('active');
    backdrop.classList.remove('active');
    body.style.overflow = '';
}

// Close via X button
closeBtn.addEventListener('click', closeSidebar);

// Close by clicking outside
backdrop.addEventListener('click', closeSidebar);

// Close with ESC key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeSidebar();
});

