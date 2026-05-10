

function registrar() {
  const nombre   = document.getElementById('nombre').value.trim();
  const email    = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;
  const password2 = document.getElementById('password2').value;

  // Validaciones básicas
  if (!nombre || !email || !password || !password2) {
    mostrarError('Por favor llena todos los campos obligatorios.');
    return;
  }

  if (!email.includes('@')) {
    mostrarError('Ingresa un correo válido.');
    return;
  }

  if (password.length < 6) {
    mostrarError('La contraseña debe tener al menos 6 caracteres.');
    return;
  }

  if (password !== password2) {
    mostrarError('Las contraseñas no coinciden.');
    return;
  }

  document.getElementById('mensaje-error').style.display = 'none';


  localStorage.setItem('usuario', email);
  localStorage.setItem('nombre', nombre);

  alert('¡Cuenta creada exitosamente! Bienvenido, ' + nombre + '.');
  window.location.href = 'dashboard.html';
}

function mostrarError(texto) {
  const msg = document.getElementById('mensaje-error');
  msg.textContent = texto;
  msg.style.display = 'block';
}
