
            # Ajustar tamaño de las imágenes en la tabla
            img_size = (75, 70)  # Nuevo tamaño deseado para las imágenes en la tabla
            resized_image = self.load_resized_image(self.png_paths[color], img_size)
            'Item', 'Cantidad'), show='headings')
        self.table_below_canvas.heading('Item', text='Item')
        self.table_below_canvas.heading('Cantidad', text='Cantidad')
        self.table_below_canvas.pack(fill=tk.BOTH, expand=True)

    def create_graph(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 4), dpi=100)
        self.ax.set_title('Acarreo de Mineral por Tiempo')
        self.ax.set_xlabel('Horas')
        self.ax.set_ylabel('Minerales (toneladas)')
        self.ax.set_xlim(0, 24)  # Ajustar según sea necesario
        self.ax.set_ylim(7500, 8300)  # Ajustar según sea necesa

        self.line, = self.ax.plot([], [], 'o-', label='Mineral Acarreado')
        self.ax.legend()

        self.canvas_graph = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_graph.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_graph(self):
        self.hours.append(self.time_counter)
        self.minerals.append(np.random.randint(7500, 8300))  # Generar valor aleatorio entre 400 y 500
        self.line.set_data(self.hours, self.minerals)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas_graph.draw()
        self.update_data_table()  # Actualizar tabla de datos después de actualizar el gráfico

    def start_graph_update(self):
        self.time_counter += 1
        self.update_graph()
        self.graph_update_id = self.root.after(7000, self.start_graph_update)  # Actualizar cada 4 segundos

    def stop_graph_update(self):
        if self.graph_update_id:
            self.root.after_cancel(self.graph_update_id)
            self.graph_update_id = None

    def reset_graph(self):
        self.hours = []
        self.minerals = []
        self.line.set_data([], [])
        self.ax.set_xlim(0, 24)  # Asegúrate de ajustar los límites según sea necesario
        self.ax.set_ylim(7500, 8300)  # Asegúrate de ajustar los límites según sea necesario
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas_graph.draw()

    def create_data_table(self):

        style = ttk.Style()
        style.configure('Treeview', font=('Helvetica', 14))
        style.configure('Treeview.Heading', font=('Helvetica', 16)) #tamaño de fuente -----

        # Crear tabla de datos usando ttk.Treeview
        self.data_table = ttk.Treeview(self.data_table_frame, columns=('Horas', 'Minerales'), show='headings')
        self.data_table.heading('Horas', text='Horas')
        self.data_table.heading('Minerales', text='Minerales (toneladas)')
        self.data_table.pack(fill=tk.BOTH, expand=True)

        # Crear una fila para mostrar el total
        self.total_label = tk.Label(self.data_table_frame, text="Total Acarreo (toneladas):", font=('Helvetica', 15))
        self.total_label.pack(side=tk.LEFT, padx=10, pady=5)
        self.total_value = tk.Label(self.data_table_frame, text="0", font=('Helvetica', 15))
        self.total_value.pack(side=tk.LEFT, padx=10, pady=5)

    def update_data_table(self):
        # Limpiar la tabla antes de agregar nuevos datos
        for row in self.data_table.get_children():
            self.data_table.delete(row)

        # Insertar los datos en la tabla
        for hour, mineral in zip(self.hours, self.minerals):
            self.data_table.insert('', tk.END, values=(hour, mineral))

        # Calcular y mostrar el total
        total_acarreo = sum(self.minerals)
        self.total_value.config(text=str(total_acarreo))
        self.update_table_below_canvas(total_acarreo)  # Actualizar tabla debajo del canvas

    def update_table_below_canvas(self, total_acarreo):
        # Limpiar la tabla antes de agregar nuevos datos
        for row in self.table_below_canvas.get_children():
            self.table_below_canvas.delete(row)

        # Calcular valores
        oro = total_acarreo * 0.02
        cobre = total_acarreo * 0.08     
        plata = total_acarreo * 0.05
        Zinc = total_acarreo * 0.07
        Molibdenita = total_acarreo * 0.4
        desmonte = total_acarreo * 0.74


        # Insertar datos en la tabla
        self.table_below_canvas.insert('', tk.END, values=('oro_Au', f"{oro:.2f} toneladas"))
        self.table_below_canvas.insert('', tk.END, values=('cobre_Cu', f"{cobre:.2f} toneladas"))
        self.table_below_canvas.insert('', tk.END, values=('plata_Ag', f"{plata:.2f} toneladas"))
        self.table_below_canvas.insert('', tk.END, values=('Zinc_Zn', f"{Zinc:.2f} toneladas"))
        self.table_below_canvas.insert('', tk.END, values=('Molibdenita_MoS2', f"{Molibdenita:.2f} toneladas"))
        self.table_below_canvas.insert('', tk.END, values=('desmonte', f"{desmonte:.2f} toneladas"))

    def create_truck_comparison_graph(self):
        self.truck_fig, self.truck_ax = plt.subplots(figsize=(8, 4), dpi=100)
        self.truck_ax.set_title('Comparación de Camiones por Hora')
        self.truck_ax.set_xlabel('Horas')
        self.truck_ax.set_ylabel('Toneladas de Mineral')
        
        self.truck_lines = {}
        for truck in self.truck_data.keys():
            line, = self.truck_ax.plot([], [], 'o-', label=truck)
            self.truck_lines[truck] = line
        
        self.truck_ax.legend()
        self.truck_ax.set_xlim(0, 24)  # Set x-axis limit to 24 hours
        self.truck_ax.set_ylim(0, 8300)  # Set y-axis limit based on your data range

        self.truck_canvas = FigureCanvasTkAgg(self.truck_fig, master=self.tab2)
        self.truck_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_truck_comparison_graph(self):
        if not self.minerals:
            return

        total_mineral = self.minerals[-1]
        
        # Generate a random split ratio between 0.3 and 0.7
        split_ratio = random.uniform(0.3, 0.7)
        
        truck1_mineral = int(total_mineral * split_ratio)
        truck2_mineral = total_mineral - truck1_mineral

        self.truck_data['camion.png'].append(truck1_mineral)
        self.truck_data['camion2.png'].append(truck2_mineral)

        for truck, line in self.truck_lines.items():
            line.set_data(self.hours, self.truck_data[truck])

        self.truck_ax.relim()
        self.truck_ax.autoscale_view()
        self.truck_canvas.draw()

    def start_animation(self):
        self.animating = True
        self.animate()
        self.start_graph_update()

    def stop_animation(self):
        self.animating = False
        self.stop_graph_update()

    def reset_animation(self):
        self.stop_animation()
        self.indices = {color: 0 for color in ['rojo', 'verde', 'amarillo']}
        for color in ['rojo', 'verde', 'amarillo']:
            if self.coordinates[color]:
                self.canvas.coords(self.image_ids[color], *self.coordinates[color][0])
        self.reset_graph()
        self.time_counter = 0
        self.update_data_table()
        self.reset_truck_comparison_graph()

    def reset_truck_comparison_graph(self):
        for truck in self.truck_data:
            self.truck_data[truck] = []
        for line in self.truck_lines.values():
            line.set_data([], [])
        self.truck_ax.relim()
        self.truck_ax.autoscale_view()
        self.truck_canvas.draw()

    def start_graph_update(self):
        self.time_counter += 1
        self.update_graph()
        self.update_truck_comparison_graph()
        self.graph_update_id = self.root.after(7000, self.start_graph_update)
        
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Animador de Camiones")

    image_path = "pw.png"
    png_paths = {
        'rojo': 'camion1.png',
        'verde': 'camion2.png',
        'amarillo': '4x4.png'
    }
    new_sizes = {
        'rojo': (50, 50),
        'verde': (50, 50),
        'amarillo': (50, 50)
    }
    logo_path = 'logo11.png'

    app = TruckAnimator(root, image_path, png_paths, new_sizes, logo_path)
    root.mainloop()
