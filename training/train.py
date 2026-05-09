from ultralytics import YOLO
import os
import sys
import matplotlib
matplotlib.use('Agg')
print("SCRIPT INICIADO", flush=True)
sys.stdout.flush()
# ============================================================
#                    CONFIGURACION
# ============================================================
RUTA_YAML   = "dataset/data.yaml" 
MODELO_BASE = "yolov8n.pt"         
EPOCHS      = 50                  
IMGSZ       = 320                  
BATCH       = 4                    # imagenes por batch (se tiene que bajar por si eres pobre y tienes poca ram)
NOMBRE_RUN  = "fuego_v1"           # nombre para identificar este entrenamiento
# ============================================================

def entrenar():
    print(" Iniciando entrenamiento YOLOv8...")
    print(f"   Modelo base : {MODELO_BASE}")
    print(f"   Epochs      : {EPOCHS}")
    print(f"   Imagen size : {IMGSZ}")
    print(f"   Batch size  : {BATCH}")
    print()

    # Cargar modelo base preentrenado
    model = YOLO(MODELO_BASE)

    # Entrenar
    results = model.train(
        data=RUTA_YAML,
        epochs=EPOCHS,
        imgsz=IMGSZ,
        batch=BATCH,
        name=NOMBRE_RUN,
        augment=True,       # rotaciones, brillo, zoom automatico
        patience=10,        # se me para si no mejora en 10 epochs seguidas
        save=True,          # guardamos sus checkpoint
        plots=False,         # me generara graficas
        amp=False,          #quito esto para que me use la gpu como es debido
        device='cpu',
        workers=0,          #esta onda me evita que se vuelva a re-ejecutar el script y me cause problemas
        optimizer="SGD",    #FORZAMOS EL OPTIMIZADOR DIRECTAMENTE
        cache=True,
    )

    print()
    print(" El entrenamiento completado!")
    print(f" Resultados guardados en: runs/detect/{NOMBRE_RUN}/")
    print(f" Mejor modelo en        : runs/detect/{NOMBRE_RUN}/weights/best.pt")

if __name__ == "__main__":
    entrenar()
