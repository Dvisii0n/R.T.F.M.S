import componentes from "./componentes.js";

function establecerDatosDeteccion(eventData) {
	document.querySelector(".detecciones").textContent =
		eventData.num_detecciones;

	const riesgoDiv = document.querySelector(".nivel-riesgo");

	riesgoDiv.textContent = eventData.nivel_riesgo;
	riesgoDiv.setAttribute("nivel", eventData.nivel_riesgo.toUpperCase());
}

function mostrarAlertas(nivel_riesgo) {
	const alertas_lista = document.querySelector(".alertas-lista");
	const LIMITE_ALERTAS = 100;
	if (alertas_lista.childNodes.length < LIMITE_ALERTAS) {
		const alerta = componentes.createAlertaItem({
			titulo: `Incendio nivel ${nivel_riesgo}`,
			hora: new Date().toLocaleString(),
		});
		alerta.setAttribute("nivel", nivel_riesgo);
		alertas_lista.prepend(alerta);
	} else {
		alertas_lista.removeChild(alertas_lista.childNodes[LIMITE_ALERTAS - 1]);
	}
}

export { establecerDatosDeteccion, mostrarAlertas };
