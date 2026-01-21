🚀 PROYECTO: SIMULADOR DE CINEMÁTICA Y TRAYECTORIAS VECTORIALES

📖 Descripción General

Este software es una plataforma integral para el estudio del movimiento de proyectiles en el vacío. Combina el rigor de la física clásica con herramientas modernas de desarrollo como la gestión de datos en JSON, el uso de Type Hints para la robustez del código y una interfaz gráfica interactiva con telemetría en tiempo real.

🎯 Objetivos y Tareas del Sistema
El programa resuelve cinco retos específicos de ingeniería y física:

Cálculo de Alcance (Tarea 1): Determina la distancia horizontal máxima.

Identificación de Cénit (Tarea 2): Rastrea el punto más alto alcanzado.

Filtro de Persistencia (Tarea 3): Clasifica proyectiles con tiempo de vuelo >5 segundos.

Muestreo de Datos (Tarea 4): Exporta coordenadas (x,y) cada 0.5 s en formato JSON.

Análisis Vectorial (Tarea 5): Representación visual de los vectores de velocidad.

📐 Fundamentos del Motor Físico
El simulador aplica las leyes del movimiento parabólico, descomponiendo el vector de velocidad inicial (v 
0
​
 ) en sus componentes rectangulares:

Ecuaciones Paramétricas
La posición del proyectil se calcula instante a instante mediante:

x(t)=v 
0
​
 cos(θ)t
y(t)=v 
0
​
 sin(θ)t− 
2
1
​
 gt 
2
 
Dinámica de Velocidad (Vectores)
Al interactuar con la interfaz, se resuelven las velocidades instantáneas:

Velocidad Horizontal (v 
x
​
 ): Constante, ya que a 
x
​
 =0.

Velocidad Vertical (v 
y
​
 ): Variable, definida por v 
y
​
 =v 
0
​
 sin(θ)−gt.

💻 Arquitectura y Patrones de Desarrollo
Para asegurar un código de alta calidad, se han implementado:

Contratos de Integridad: Uso de assert para evitar lanzamientos con ángulos >90 
∘
  o velocidades negativas.

Type Hinting: Definición de tipos de datos para prevenir errores de lógica durante el desarrollo.

Lógica de Coronación: Un sistema de búsqueda que otorga dinámicamente el título de 🏆 VERDADERO RÉCORD basándose en el alcance calculado, ignorando las etiquetas del archivo de entrada.

Auto-Escalado: Algoritmo de mapeo que ajusta la vista sin importar si el alcance es de 10 m o 1000 m.

📂 Estructura del Software
generar_datos.py: El administrador del archivo JSON de entrada.

ejercicio.py: El motor de cálculo analítico y generador de reportes.

interfaz_pro.py: El visualizador animado con panel de telemetría y slider de tiempo.

🛠️ Instalación y Requisitos
Asegúrate de tener instaladas las dependencias necesarias:

Bash

# Clonar el repositorio o descargar archivos
# Instalar librerías requeridas
pip install numpy matplotlib
Guía de Inicio Rápido
Ejecuta generar_datos.py para crear la base de datos datos.json.

Ejecuta ejercicio.py para obtener el análisis técnico y el archivo de muestreo.

Ejecuta interfaz_pro.py para iniciar la simulación visual.

⚠️ Resolución de Problemas (Troubleshooting)
"La bola va muy lento": Usa el slider "Sim Speed" en la interfaz para acelerar el tiempo (recomendado 10x para velocidades >100 m/s).

"Error: FileNotFoundError": Asegúrate de ejecutar el generador de datos antes que el analizador.

"La ventana se ve pequeña": El sistema usa auto-escalado; si redimensionas la ventana, pulsa "Lanzar" de nuevo para recalcular la proporción.

Nota Científica: Este simulador asume condiciones de vacío. La resistencia del aire (rozamiento) no está incluida en los cálculos actuales.