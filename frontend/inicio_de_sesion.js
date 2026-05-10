function iniciarSesion() {
  const email    = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;
  const msgError = document.getElementById('mensaje-error');

  // Validación básica
  if (!email || !password) {
    mostrarError('Por favor llena todos los campos.');
    return;
  }

  if (!email.includes('@')) {
    mostrarError('Ingresa un correo válido.');
    return;
  }

  if (password.length < 4) {
    mostrarError('La contraseña es muy corta.');
    return;
  }

  msgError.style.display = 'none';


  localStorage.setItem('usuario', email);


  alert('¡Sesión iniciada como ' + email + '!');
  window.location.href = 'dashboard.html';
}

function mostrarError(texto) {
  const msgError = document.getElementById('mensaje-error');
  msgError.textContent = texto;
  msgError.style.display = 'block';
}


document.addEventListener('keydown', function(e) {
  if (e.key === 'Enter') iniciarSesion();
});
