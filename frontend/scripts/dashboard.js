import { API_URL } from "./globales.js";
// ===== TOGGLE PANELS =====
function togglePanel(btn) {
	const panel = btn.closest(".panel");
	const body = panel.querySelector(".panel-body");
	const collapsed = panel.classList.toggle("collapsed");
	btn.textContent = collapsed ? "＋" : "－";
	body.style.display = collapsed ? "none" : "";
}

// ===== MAPA =====
const LAT = 23.2494;
const LNG = -106.4111;

// CartoDB tiles — no requieren referrer, funcionan desde file://
const TILE_URL =
	"https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png";
const TILE_ATTR =
	'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/">CARTO</a>';

const iconoRojo = L.divIcon({
	className: "",
	html: `<div style="
    width:22px; height:22px;
    background:#d62828;
    border-radius:50% 50% 50% 0;
    transform:rotate(-45deg);
    border:2px solid white;
    box-shadow:0 0 8px rgba(214,40,40,0.8)
  "></div>`,
	iconSize: [22, 22],
	iconAnchor: [11, 22],
});

const mapaMini = L.map("mapa-mini", {
	zoomControl: false,
	attributionControl: false,
	dragging: false,
	scrollWheelZoom: false,
	touchZoom: false,
	keyboard: false,
}).setView([LAT, LNG], 14);

L.tileLayer(TILE_URL, { attribution: TILE_ATTR }).addTo(mapaMini);
L.marker([LAT, LNG], { icon: iconoRojo }).addTo(mapaMini);

let mapaGrande = null;

function abrirMapa() {
	document.getElementById("modal-mapa").classList.add("activo");
	if (!mapaGrande) {
		mapaGrande = L.map("mapa-grande").setView([LAT, LNG], 16);
		L.tileLayer(TILE_URL, { attribution: TILE_ATTR }).addTo(mapaGrande);
		L.marker([LAT, LNG], { icon: iconoRojo }).addTo(mapaGrande).openPopup();
	} else {
		setTimeout(() => mapaGrande.invalidateSize(), 100);
	}
}

function cerrarMapa() {
	document.getElementById("modal-mapa").classList.remove("activo");
}

document.getElementById("modal-mapa").addEventListener("click", function (e) {
	if (e.target === this) cerrarMapa();
});

document.querySelector(".camara-feed").setAttribute("src", `${API_URL}/stream`);
