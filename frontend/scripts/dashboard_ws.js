import { establecerDatosDeteccion, mostrarAlertas } from "./dashboard_utils.js";

const socket = new WebSocket("ws://localhost:8080");

socket.onopen = () => {
	const estado = document.querySelector(".estado");
	estado.textContent = "WS: Activo";
	estado.setAttribute("estado", "ACTIVO");
	console.log("Conectado al servidor de WebSocket");
};

socket.onmessage = (event) => {
	const eventData = JSON.parse(event.data);
	console.log(eventData);
	switch (eventData.type) {
		case "DETECCION":
			establecerDatosDeteccion(eventData);
			if (eventData.nivel_riesgo !== "SEGURO") {
				mostrarAlertas(eventData.nivel_riesgo);
			}
			break;

		default:
			break;
	}
};

socket.onclose = () => {
	const estado = document.querySelector(".estado");
	estado.textContent = "WS: Inactivo";
	estado.setAttribute("estado", "INACTIVO");
	console.log("Conexión cerrada");
};
