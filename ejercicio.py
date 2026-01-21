import json
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Optional

def analizar_proyectiles() -> None:
    """
    FUNCIÓN PRINCIPAL: Lee datos, valida física, calcula trayectorias y 
    genera una interfaz visual interactiva.
    """
    # --- 1. CONFIGURACIÓN DE PARÁMETROS ---
    G: float = 9.81              # Constante de gravedad terrestre
    ARCHIVO_IN: str = 'datos.json'
    ARCHIVO_OUT: str = 'analisis_trayectorias.json'
    INTERVALO: float = 0.5       # Cada cuánto tiempo tomamos una muestra (Tarea 4)
    LIMITE_T: float = 5.0        # Filtro para lanzamientos de larga duración (Tarea 3)

    # --- 2. LÓGICA DE CARGA Y CONTRATOS ---
    try:
        with open(ARCHIVO_IN, 'r', encoding='utf-8') as f:
            datos: List[Dict[str, Any]] = json.load(f)
        
        # CONTRATO: Verificamos que el archivo contenga al menos un proyectil
        assert len(datos) > 0, "No hay datos suficientes para realizar el análisis."
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return

    # Contenedores para almacenar resultados y estadísticas
    resultados_fisicos: List[Dict[str, Any]] = []
    max_alcance: float = 0.0
    ganador_idx: int = -1
    vuelos_largos: List[str] = []

    # --- 3. BUCLE DE CÁLCULO CINEMÁTICO ---
    for i, p in enumerate(datos):
        # Hint de tipos y validación de entrada
        v0: float = float(p['velocidad'])
        deg: float = float(p['angulo'])
        
        # CONTRATO FÍSICO: Validamos que los valores tengan sentido en el mundo real
        assert v0 >= 0, "La velocidad no puede ser negativa."
        assert 0 <= deg <= 90, "El ángulo debe estar entre 0 y 90 grados."

        rad: float = np.radians(deg) # La librería NumPy requiere radianes

        # FORMULACIÓN MATEMÁTICA:
        # Alcance: R = (v0² * sin(2θ)) / g
        alcance: float = (v0**2 * np.sin(2 * rad)) / G
        # Altura Máxima: H = (v0² * sin²θ) / (2g)
        altura: float = (v0**2 * (np.sin(rad)**2)) / (2 * G)
        # Tiempo total: T = (2 * v0 * sinθ) / g
        t_vuelo: float = (2 * v0 * np.sin(rad)) / G

        # TAREA 3: Identificar vuelos de larga duración
        if t_vuelo > LIMITE_T:
            vuelos_largos.append(f"{p['id']} ({t_vuelo:.2f}s)")
        
        # LOGICA DE CORONACIÓN: Buscamos el índice del que llega más lejos
        if alcance > max_alcance:
            max_alcance, ganador_idx = alcance, i

        # TAREA 4: MUESTREO TEMPORAL (HISTORIAL DE POSICIONES)
        # Creamos una lista de tiempos (0, 0.5, 1.0...) y añadimos el impacto final
        tiempos: np.ndarray = np.append(np.arange(0, t_vuelo, INTERVALO), t_vuelo)
        muestreo: List[Dict[str, float]] = []
        
        for t in tiempos:
            # Ecuaciones paramétricas de posición:
            # x = v0 * cos(θ) * t
            # y = v0 * sin(θ) * t - 0.5 * g * t²
            muestreo.append({
                "t": round(float(t), 2),
                "x": round(float(v0 * np.cos(rad) * t), 2),
                "y": round(float(v0 * np.sin(rad) * t - 0.5 * G * t**2), 2)
            })

        # Guardamos el objeto procesado con todos sus datos físicos
        resultados_fisicos.append({
            "id": p['id'], "v0": v0, "deg": deg, "rad": rad,
            "alcance": alcance, "altura": altura, "t_vuelo": t_vuelo, "puntos": muestreo
        })

    # --- 4. EXPORTACIÓN Y REPORTES ---
    json_final: List[Dict[str, Any]] = []
    print(f"\n{'ID PROYECTIL':<30} | {'ALCANCE':<12} | {'ALTURA'}")
    print("-" * 65)

    for i, res in enumerate(resultados_fisicos):
        # Si es el ganador, le añadimos el trofeo al nombre
        nombre_final: str = res['id']
        if i == ganador_idx:
            nombre_final = f"🏆 VERDADERO RÉCORD ({res['id']})"
        
        print(f"{nombre_final:<30} | {res['alcance']:>10.2f}m | {res['altura']:>8.2f}m")
        
        json_final.append({
            "id": nombre_final,
            "metricas": {"alcance": round(res['alcance'], 2), "altura": round(res['altura'], 2)},
            "puntos_trayectoria": res['puntos']
        })

    # Escribimos el archivo de salida para la Tarea 4
    with open(ARCHIVO_OUT, 'w', encoding='utf-8') as f:
        json.dump(json_final, f, indent=4, ensure_ascii=False)

    print(f"\n✓ Tarea 3: Vuelos > 5s: {vuelos_largos}")

    # --- 5. INTERFAZ GRÁFICA INTERACTIVA (TAREA VECTORES) ---
    fig, ax = plt.subplots(figsize=(12, 7))
    curvas_grafica: List[Any] = []

    for i, res in enumerate(resultados_fisicos):
        # Generamos una línea suave para la gráfica (200 puntos)
        t_visual = np.linspace(0, res['t_vuelo'], 200)
        x_v = res['v0'] * np.cos(res['rad']) * t_visual
        y_v = res['v0'] * np.sin(res['rad']) * t_visual - 0.5 * G * t_visual**2
        
        etiqueta = f"🏆 {res['id']}" if i == ganador_idx else res['id']
        linea, = ax.plot(x_v, y_v, label=etiqueta, picker=5) # picker habilita el clic
        curvas_grafica.append(linea)

    # Objeto para almacenar la flecha del vector actual
    flecha_vector: List[Optional[Any]] = [None]

    

    def al_clickar(event):
        """
        LÓGICA VECTORIAL: Al hacer clic, calculamos el vector velocidad instantánea.
        v_vector = (Vx)i + (Vy)j
        """
        if event.artist in curvas_grafica:
            idx = curvas_grafica.index(event.artist)
            p = resultados_fisicos[idx]
            
            # Localizamos la posición del clic en el eje X/Y
            mouse_x = event.mouseevent.xdata
            
            # Buscamos en nuestro muestreo el punto X más cercano
            pxs = np.array([pt['x'] for pt in p['puntos']])
            indice_cercano = np.argmin(np.abs(pxs - mouse_x))
            
            punto = p['puntos'][indice_cercano]
            t_actual = punto['t']

            # CÁLCULO DE COMPONENTES DEL VECTOR VELOCIDAD:
            # Vx = V0 * cos(θ) --> Constante
            # Vy = V0 * sin(θ) - g * t --> Cambia con la gravedad
            vx = p['v0'] * np.cos(p['rad'])
            vy = p['v0'] * np.sin(p['rad']) - G * t_actual
            
            # Eliminamos el vector anterior para dibujar el nuevo
            if flecha_vector[0]: flecha_vector[0].remove()
            
            # 'ax.quiver' dibuja la flecha del vector trayectoria en rojo
            flecha_vector[0] = ax.quiver(punto['x'], punto['y'], vx, vy, 
                                        color='red', scale=15, scale_units='xy')
            
            ax.set_title(f"Vector Trayectoria: {p['id']} | v_total: {np.sqrt(vx**2+vy**2):.2f} m/s", color='red')
            fig.canvas.draw_idle()

    # Conectamos el evento de clic con nuestra función lógica
    fig.canvas.mpl_connect('pick_event', al_clickar)
    
    # Estética de la gráfica
    ax.set_xlabel("Distancia Horizontal (m)")
    ax.set_ylabel("Altura Vertical (m)")
    ax.legend(ncol=2, fontsize='8')
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color='black', lw=1.5)
    
    print("\nINSTRUCCIÓN: Haz clic en cualquier trayectoria de la gráfica para ver su vector.")
    plt.show()

if __name__ == "__main__":
    analizar_proyectiles()