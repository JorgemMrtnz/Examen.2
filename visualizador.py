import tkinter as tk
from tkinter import ttk, messagebox
import json
import math
from typing import List, Dict, Any, Optional, Tuple

class SimuladorProyectilesGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Simulador de Física - Auto-Escalado Inteligente")
        
        # Tamaño de ventana adaptable pero seguro para la mayoría de pantallas
        self.root.geometry("1000x600")
        self.root.configure(bg="#1e1e1e")

        # --- CONSTANTES ---
        self.G: float = 9.81
        self.id_animacion: Optional[str] = None
        
        # Márgenes para que el tiro no toque los bordes (en píxeles)
        self.MARGEN_X = 60
        self.MARGEN_Y = 60
        
        # Cargar datos
        self._cargar_datos()
        self._configurar_gui()

    def _cargar_datos(self):
        try:
            with open('datos.json', 'r', encoding='utf-8') as f:
                self.proyectiles = json.load(f)
        except:
            self.proyectiles = []

    def _configurar_gui(self):
        # Panel superior de controles (horizontal para ahorrar espacio vertical)
        self.top_panel = tk.Frame(self.root, bg="#2d2d2d", height=80)
        self.top_panel.pack(side=tk.TOP, fill=tk.X)

        tk.Label(self.top_panel, text="Proyectil:", bg="#2d2d2d", fg="white").pack(side=tk.LEFT, padx=10)
        self.combo = ttk.Combobox(self.top_panel, values=[p['id'] for p in self.proyectiles], state="readonly", width=20)
        self.combo.pack(side=tk.LEFT, padx=5)
        self.combo.bind("<<ComboboxSelected>>", self._auto_fill)

        tk.Label(self.top_panel, text="V (m/s):", bg="#2d2d2d", fg="white").pack(side=tk.LEFT, padx=10)
        self.ent_v = tk.Entry(self.top_panel, width=8)
        self.ent_v.pack(side=tk.LEFT, padx=5)

        tk.Label(self.top_panel, text="Ang (°):", bg="#2d2d2d", fg="white").pack(side=tk.LEFT, padx=10)
        self.ent_a = tk.Entry(self.top_panel, width=8)
        self.ent_a.pack(side=tk.LEFT, padx=5)

        self.btn_lanzar = tk.Button(self.top_panel, text="🚀 LANZAR", command=self.lanzar, bg="#007acc", fg="white", font=("Arial", 9, "bold"))
        self.btn_lanzar.pack(side=tk.LEFT, padx=20)

        # Canvas principal
        self.canvas = tk.Canvas(self.root, bg="#121212", highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Dashboard inferior de telemetría
        self.telemetria = tk.Frame(self.root, bg="#252526", height=40)
        self.telemetria.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.lbl_stats = tk.Label(self.telemetria, text="Listo para el lanzamiento", bg="#252526", fg="#00ff00", font=("Consolas", 10))
        self.lbl_stats.pack(pady=5)

    def _auto_fill(self, event):
        p = self.proyectiles[self.combo.current()]
        self.ent_v.delete(0, tk.END); self.ent_v.insert(0, str(p['velocidad']))
        self.ent_a.delete(0, tk.END); self.ent_a.insert(0, str(p['angulo']))

    def lanzar(self):
        try:
            v0 = float(self.ent_v.get())
            ang = float(self.ent_a.get())
            assert v0 > 0 and 0 <= ang <= 90
        except:
            messagebox.showerror("Error", "Velocidad > 0 y Ángulo entre 0 y 90.")
            return

        # Cancelar animaciones previas y limpiar
        if self.id_animacion: self.root.after_cancel(self.id_animacion)
        self.canvas.delete("all")
        
        # 1. CÁLCULO DE LÍMITES FÍSICOS (Para el escalado)
        rad = math.radians(ang)
        alcance_f = (v0**2 * math.sin(2 * rad)) / self.G
        altura_f = (v0**2 * (math.sin(rad)**2)) / (2 * self.G)
        t_total = (2 * v0 * math.sin(rad)) / self.G

        # 2. LÓGICA DE ESCALADO DINÁMICO
        # Obtenemos el tamaño actual del canvas
        ancho_c = self.canvas.winfo_width()
        alto_c = self.canvas.winfo_height()

        # Calculamos cuántos píxeles equivalen a 1 metro para que todo quepa
        # Restamos los márgenes para no tocar los bordes
        escala_x = (ancho_c - 2 * self.MARGEN_X) / (alcance_f if alcance_f > 1 else 1)
        escala_y = (alto_c - 2 * self.MARGEN_Y) / (altura_f if altura_f > 1 else 1)
        
        # Usamos la escala más pequeña para mantener la proporción
        self.escala = min(escala_x, escala_y)

        # Dibujar suelo
        self.canvas.create_line(0, alto_c - self.MARGEN_Y, ancho_c, alto_c - self.MARGEN_Y, fill="#444", width=1)

        self._animar(0, v0, rad, t_total, alto_c, None)

    def _animar(self, t: float, v0: float, rad: float, t_total: float, alto_c: int, last_pos: Optional[Tuple[float, float]]):
        # Ecuaciones
        x = v0 * math.cos(rad) * t
        y = v0 * math.sin(rad) * t - 0.5 * self.G * (t**2)
        
        vx = v0 * math.cos(rad)
        vy = v0 * math.sin(rad) - self.G * t
        v_res = math.sqrt(vx**2 + vy**2)

        # Mapeo a píxeles con la nueva escala dinámica
        px = self.MARGEN_X + (x * self.escala)
        py = (alto_c - self.MARGEN_Y) - (y * self.escala)

        if last_pos:
            self.canvas.create_line(last_pos[0], last_pos[1], px, py, fill="#007acc", width=2, tags="trace")
        
        self.canvas.delete("bola")
        self.canvas.create_oval(px-4, py-4, px+4, py+4, fill="white", tags="bola")

        # Actualizar telemetría
        self.lbl_stats.config(text=f"Distancia: {x:.2f}m | Altura: {y:.2f}m | V_total: {v_res:.2f}m/s | Tiempo: {t:.2f}s")

        if t < t_total:
            self.id_animacion = self.root.after(20, self._animar, t + 0.05, v0, rad, t_total, alto_c, (px, py))
        else:
            self.lbl_stats.config(text=f"TIRO COMPLETADO: Alcance final {x:.2f}m", fg="yellow")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorProyectilesGUI(root)
    root.mainloop()