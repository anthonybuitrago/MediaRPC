import customtkinter as ctk
import config_manager
import utils
import os
import ctypes

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ConfigWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        try:
            myappid = "anthony.stremio.rpc.v5"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass

        self.current_config = config_manager.cargar_config()

        self.title("Configuración - Stremio RPC")
        self.geometry("400x500")
        self.resizable(False, False)

        if os.path.exists(config_manager.PATH_ICON):
            try:
                self.iconbitmap(config_manager.PATH_ICON)
                self.after(200, lambda: self.iconbitmap(config_manager.PATH_ICON))
            except:
                pass

        self.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        self.attributes("-topmost", True)
        self.lift()
        self.focus_force()
        self.after(500, lambda: self.attributes("-topmost", False))

        # --- UI PRINCIPAL (TABS) ---
        self.tabview = ctk.CTkTabview(self, width=380, height=450)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)

        self.tab_config = self.tabview.add("Configuración")
        self.tab_logs = self.tabview.add("Logs")

        # ==========================================
        #           PESTAÑA CONFIGURACIÓN
        # ==========================================
        
        self.label_title = ctk.CTkLabel(
            self.tab_config, text="Ajustes de Stremio RPC", font=("Roboto", 22, "bold")
        )
        self.label_title.pack(pady=10)

        # ID
        self.lbl_id = ctk.CTkLabel(self.tab_config, text="Discord Client ID:")
        self.lbl_id.pack(anchor="w", padx=20)
        self.entry_id = ctk.CTkEntry(self.tab_config, placeholder_text="Ingresa tu ID", width=320)
        self.entry_id.insert(0, self.current_config.get("client_id", ""))
        self.entry_id.pack(pady=(0, 10))

        # Intervalo
        self.lbl_interval = ctk.CTkLabel(
            self.tab_config,
            text=f"Velocidad de Actualización: {self.current_config.get('update_interval')} seg",
        )
        self.lbl_interval.pack(anchor="w", padx=20)
        self.slider_interval = ctk.CTkSlider(
            self.tab_config, from_=2, to=30, number_of_steps=28, command=self.update_slider
        )
        self.slider_interval.set(self.current_config.get("update_interval", 5))
        self.slider_interval.pack(fill="x", padx=20, pady=(0, 15))

        # MODO DE TIEMPO
        self.lbl_time = ctk.CTkLabel(
            self.tab_config, text="Estilo de Tiempo:", font=("Roboto", 14, "bold")
        )
        self.lbl_time.pack(anchor="w", padx=20)

        self.time_mode_var = ctk.StringVar(value="Auto")
        current_fixed = self.current_config.get("fixed_duration_minutes", 0)
        if current_fixed == 24:
            self.time_mode_var.set("Anime")
        elif current_fixed == 0:
            self.time_mode_var.set("Auto")

        self.radio_auto = ctk.CTkRadioButton(
            self.tab_config,
            text="Automático (API / Real)",
            variable=self.time_mode_var,
            value="Auto",
        )
        self.radio_auto.pack(anchor="w", padx=20, pady=5)

        self.radio_anime = ctk.CTkRadioButton(
            self.tab_config,
            text="Forzar Anime (24 min)",
            variable=self.time_mode_var,
            value="Anime",
        )
        self.radio_anime.pack(anchor="w", padx=20, pady=5)

        # OPCIONES SISTEMA
        self.lbl_sys = ctk.CTkLabel(
            self.tab_config, text="Opciones de Sistema:", font=("Roboto", 14, "bold")
        )
        self.lbl_sys.pack(anchor="w", padx=20, pady=(15, 5))

        # Switch: Botón
        self.switch_btn = ctk.CTkSwitch(self.tab_config, text="Mostrar Botón 'Buscar Anime'")
        if self.current_config.get("show_search_button", True):
            self.switch_btn.select()
        self.switch_btn.pack(anchor="w", padx=20, pady=5)

        # Switch: Auto-Start (Lee el estado real de Windows)
        self.switch_autostart = ctk.CTkSwitch(self.tab_config, text="Iniciar con Windows")
        if utils.check_autostart():
            self.switch_autostart.select()
        self.switch_autostart.pack(anchor="w", padx=20, pady=5)

        # Botón Guardar
        self.btn_save = ctk.CTkButton(
            self.tab_config,
            text="GUARDAR CAMBIOS",
            command=self.guardar_datos,
            height=40,
            font=("Roboto", 14, "bold"),
            fg_color="green",
            hover_color="darkgreen",
        )
        self.btn_save.pack(fill="x", padx=20, pady=(20, 10))

        # ==========================================
        #           PESTAÑA LOGS
        # ==========================================
        self.textbox_logs = ctk.CTkTextbox(self.tab_logs, width=360, height=350)
        self.textbox_logs.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.btn_refresh_logs = ctk.CTkButton(
            self.tab_logs,
            text="🔄 Actualizar Logs",
            command=self.cargar_logs
        )
        self.btn_refresh_logs.pack(pady=5)
        
        # Cargar logs al iniciar
        self.cargar_logs()

    def cargar_logs(self):
        self.textbox_logs.configure(state="normal")
        self.textbox_logs.delete("0.0", "end")
        
        if os.path.exists(config_manager.PATH_LOG):
            try:
                with open(config_manager.PATH_LOG, "r", encoding="utf-8") as f:
                    # Leer últimas 50 líneas para no saturar
                    lines = f.readlines()[-50:]
                    self.textbox_logs.insert("0.0", "".join(lines))
            except Exception as e:
                self.textbox_logs.insert("0.0", f"Error leyendo logs: {e}")
        else:
            self.textbox_logs.insert("0.0", "No hay archivo de logs aún.")
            
        self.textbox_logs.configure(state="disabled")

    def update_slider(self, value):
        self.lbl_interval.configure(
            text=f"Velocidad de Actualización: {int(value)} seg"
        )

    def guardar_datos(self):
        # Procesar Modo de Tiempo
        modo = self.time_mode_var.get()
        fixed_minutes = 24 if modo == "Anime" else 0

        # Crear diccionario
        datos_nuevos = self.current_config.copy()
        datos_nuevos["client_id"] = self.entry_id.get().strip()
        datos_nuevos["update_interval"] = int(self.slider_interval.get())
        datos_nuevos["show_search_button"] = bool(self.switch_btn.get())
        datos_nuevos["fixed_duration_minutes"] = fixed_minutes

        # Guardar JSON
        config_manager.guardar_config(datos_nuevos)

        # Aplicar Auto-Start real
        deseo_autostart = bool(self.switch_autostart.get())
        utils.set_autostart(deseo_autostart)

        print("Configuración guardada.")
        self.cerrar_ventana()

    def cerrar_ventana(self):
        self.destroy()
        self.quit()


def abrir_ventana():
    app = ConfigWindow()
    app.after(100, app.focus_force)
    app.mainloop()


if __name__ == "__main__":
    abrir_ventana()
