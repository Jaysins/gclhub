const sidebarToggler = document.querySelector('.menu-toggler .toggler');

sidebarToggler.addEventListener('click', function() {
	document.querySelector('.sidebar').classList.toggle('open');
});
