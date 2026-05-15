function createAlertaItem({ titulo, hora }) {
	const item = document.createElement("div");
	item.className = "alerta-item";

	const dot = document.createElement("div");
	dot.className = "alerta-dot";

	const texto = document.createElement("div");
	texto.className = "alerta-texto";

	const strong = document.createElement("strong");
	strong.textContent = titulo;

	const span = document.createElement("span");
	span.className = "alerta-hora";
	span.textContent = hora;

	texto.appendChild(strong);
	texto.appendChild(span);
	item.appendChild(dot);
	item.appendChild(texto);

	return item;
}

export default { createAlertaItem };
