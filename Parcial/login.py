import tkinter as tk  #Usuario = Dairo Contraseña = 123
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import json

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Veterinaria")
        self.geometry("900x700")

        self.frame_izquierda = tk.Frame(self, width = 200, height = 200, bg="white")
        self.frame_izquierda.pack(side="left", fill="both", expand=True)

        self.logo_original = Image.open("vet3.png")
        self.logo_redimensionado = self.redimensionar_imagen(self.logo_original, 700 , 700)
        self.logo = ImageTk.PhotoImage(self.logo_redimensionado)

        self.logo_label = tk.Label(self.frame_izquierda, image=self.logo)
        self.logo_label.pack(pady=100)

        self.frame_derecha = tk.Frame(self, width=200, height=200, bg="lightblue")
        self.frame_derecha.pack(side="right", fill="both", expand=True)

        self.label_titulo = tk.Label(self.frame_derecha, text="Veterinaria",bg="white", font=("Arial black", 20))
        self.label_titulo.pack(pady=70)

        self.label_usuario = tk.Label(self.frame_derecha, text="Usuario:", font=("Arial black", 12))
        self.label_usuario.pack()
        self.entry_usuario = tk.Entry(self.frame_derecha, font=("Arial", 12))
        self.entry_usuario.pack(pady=10)

        self.label_clave = tk.Label(self.frame_derecha, text="Contraseña:", font=("Arial black", 12))
        self.label_clave.pack()
        self.entry_clave = tk.Entry(self.frame_derecha, show="*", font=("Arial", 12))
        self.entry_clave.pack(pady=10)

        self.boton_ingresar = tk.Button(self.frame_derecha, text="Ingresar", font=("Arial black", 12), command=self.ingresar)
        self.boton_ingresar.pack(pady=20)

    def redimensionar_imagen(self, imagen, ancho, alto):
        return imagen.resize((ancho, alto ))

    def ingresar(self):
        usuario = self.entry_usuario.get()
        clave = self.entry_clave.get()

        if usuario == "Dairo" and clave == "123":
            messagebox.showinfo("Veterinaria", "¡Bienvenido!")
            self.show_menu()
        else:
            messagebox.showerror("Inicio de Sesión", "Usuario o contraseña incorrectos")

    def show_menu(self):
        self.frame_derecha.destroy()
        self.frame_izquierda.destroy()

        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack()

        self.boton_animales = tk.Button(self.menu_frame, text="Animales", command=self.show_animals, font=("Arial", 14), width=15, height=2)
        self.boton_animales.pack()

        self.boton_tipos = tk.Button(self.menu_frame, text="Tipos", command=self.show_types, font=("Arial", 14), width=15, height=2)
        self.boton_tipos.pack()

        self.boton_clientes = tk.Button(self.menu_frame, text="Clientes", command=self.show_clients, font=("Arial", 14), width=15, height=2)
        self.boton_clientes.pack()

        self.boton_atenciones = tk.Button(self.menu_frame, text="Atenciones", command=self.show_attentions, font=("Arial", 14), width=15, height=2)
        self.boton_atenciones.pack()

    def show_animals(self):
        self.clear_frame()
        tk.Label(self, text="Animales").pack()
        tk.Button(self, text="Agregar Animal", command=self.add_animal).pack()
        tk.Button(self, text="Listar Animales", command=self.list_animals).pack()
        tk.Button(self, text="Eliminar Animal", command=self.delete_animal).pack()
        tk.Button(self, text="Actualizar Animal", command=self.update_animal).pack()
        tk.Button(self, text="Back", command=self.show_menu).pack(pady=10)

    def add_animal(self):
        add_window = tk.Toplevel(self)
        add_window.title("Agregar Animal")
        
        tk.Label(add_window, text="Nombre:").pack()
        animal_name_entry = tk.Entry(add_window)
        animal_name_entry.pack()
        
        tk.Label(add_window, text="Tipo:").pack()
        self.type_names = [type_info["nombre"] for type_info in self.load_data("tipos.json")]
        self.selected_type = tk.StringVar(add_window)
        self.selected_type.set(self.type_names[0] if self.type_names else "No hay tipos")
        tk.OptionMenu(add_window, self.selected_type, *self.type_names).pack()

        tk.Button(add_window, text="Agregar", command=lambda: self.save_animal(animal_name_entry.get(), self.selected_type.get(), add_window)).pack()
        tk.Button(add_window, text="Back", command=add_window.destroy).pack(pady=10)

    def save_animal(self, name, type, window):
        if name and type:
            new_animal = {"nombre": name, "tipo": type}
            animals_data = self.load_data("animals.json")
            animals_data.append(new_animal)
            self.save_data("animals.json", animals_data)
            window.destroy()
            self.list_animals()
            messagebox.showinfo("Éxito", "Animal agregado correctamente")
        else:
            messagebox.showerror("Error", "Por favor, ingresa todos los datos del animal")

    def list_animals(self):
        self.clear_frame()
        animals_data = self.load_data("animals.json")

        if animals_data:
            for animal in animals_data:
                tk.Label(self, text=f"Nombre: {animal['nombre']} - Tipo: {animal['tipo']}").pack()
        else:
            tk.Label(self, text="No hay animales registrados").pack()
        tk.Button(self, text="Back", command=self.show_menu).pack(pady=10)

    def delete_animal(self):
        delete_window = tk.Toplevel(self)
        delete_window.title("Eliminar Animal")

        animals_data = self.load_data("animals.json")
        animal_names = [animal["nombre"] for animal in animals_data]

        tk.Label(delete_window, text="Selecciona el animal a eliminar:").pack()
        animal_choice = tk.StringVar(delete_window)
        animal_choice.set(animal_names[0] if animal_names else "No hay animales")
        tk.OptionMenu(delete_window, animal_choice, *animal_names).pack()

        tk.Button(delete_window, text="Eliminar", command=lambda: self.confirm_delete(animal_choice.get(), delete_window)).pack()
        tk.Button(delete_window, text="Back", command=delete_window.destroy).pack(pady=10)

    def confirm_delete(self, animal_name, window):
        animals_data = self.load_data("animals.json")
        updated_animals = [animal for animal in animals_data if animal["nombre"] != animal_name]
        self.save_data("animals.json", updated_animals)
        window.destroy()
        self.list_animals()
        messagebox.showinfo("Éxito", f"Animal '{animal_name}' eliminado correctamente")
        tk.Button(self, text="Back", command=self.show_animals).pack(pady=10)

    def update_animal(self):
        update_window = tk.Toplevel(self)
        update_window.title("Actualizar Animal")

        animals_data = self.load_data("animals.json")
        animal_names = [animal["nombre"] for animal in animals_data]

        tk.Label(update_window, text="Selecciona el animal a actualizar:").pack()
        animal_choice = tk.StringVar(update_window)
        animal_choice.set(animal_names[0] if animal_names else "No hay animales")
        tk.OptionMenu(update_window, animal_choice, *animal_names).pack()

        tk.Label(update_window, text="Nuevo nombre:").pack()
        new_name_entry = tk.Entry(update_window)
        new_name_entry.pack()

        tk.Label(update_window, text="Nuevo tipo:").pack()
        new_type_entry = tk.Entry(update_window)
        new_type_entry.pack()

        tk.Button(update_window, text="Actualizar", command=lambda: self.save_updated_animal(animal_choice.get(), new_name_entry.get(), new_type_entry.get(), update_window)).pack()
        tk.Button(update_window, text="Back", command=update_window.destroy).pack(pady=10)

    def save_updated_animal(self, old_name, new_name, new_type, window):
        if new_name and new_type:
            animals_data = self.load_data("animals.json")
            for animal in animals_data:
                if animal["nombre"] == old_name:
                    animal["nombre"] = new_name
                    animal["tipo"] = new_type
                    break
            self.save_data("animals.json", animals_data)
            window.destroy()
            self.list_animals()
            messagebox.showinfo("Éxito", "Animal actualizado correctamente")
        else:
            messagebox.showerror("Error", "Por favor, ingresa todos los datos del animal")

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def load_data(self, filename):
        data = []
        filepath = os.path.join("data", filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        return data

    def save_data(self, filename, data):
        filepath = os.path.join("data", filename)
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)

    def show_types(self):
        self.clear_frame()
        types_data = self.load_data("tipos.json")

        if types_data:
            tk.Label(self, text="Tipos").pack()
            for type_info in types_data:
                tk.Label(self, text=f"ID: {type_info['id']} - Nombre: {type_info['nombre']}").pack()
        else:
            tk.Label(self, text="No hay tipos registrados").pack()

        tk.Button(self, text="Agregar Tipo", command=self.add_type_window).pack()
        tk.Button(self, text="Back", command=self.show_menu).pack(pady=10)

    def add_type_window(self):
        add_type_window = tk.Toplevel(self)
        add_type_window.title("Agregar Tipo")

        tk.Label(add_type_window, text="Nombre:").pack()
        type_name_entry = tk.Entry(add_type_window)
        type_name_entry.pack()

        tk.Button(add_type_window, text="Agregar", command=lambda: self.save_type(type_name_entry.get(), add_type_window)).pack()
        tk.Button(add_type_window, text="Cancelar", command=add_type_window.destroy).pack(pady=10)

    def save_type(self, name, window):
        if name:
            new_type = {"id": len(self.load_data("tipos.json")) + 1, "nombre": name}
            types_data = self.load_data("tipos.json")
            types_data.append(new_type)
            self.save_data("tipos.json", types_data)
            window.destroy()
            self.show_types()
            messagebox.showinfo("Éxito", "Tipo agregado correctamente")
        else:
            messagebox.showerror("Error", "Por favor, ingresa el nombre del tipo")

    def show_clients(self):
        self.clear_frame()
        clients_data = self.load_data("clientes.json")

        if clients_data:
            tk.Label(self, text="Clientes").pack()
            for client_info in clients_data:
                tk.Label(self, text=f"ID: {client_info['id']} - Nombre: {client_info['nombre']}").pack()
        else:
            tk.Label(self, text="No hay clientes registrados").pack()

        tk.Button(self, text="Agregar Cliente", command=self.add_client_window).pack()
        tk.Button(self, text="Editar Cliente", command=self.edit_client_window).pack()
        tk.Button(self, text="Eliminar Cliente", command=self.delete_client_window).pack()
        tk.Button(self, text="Back", command=self.show_menu).pack(pady=10)

    def add_client_window(self):
        add_client_window = tk.Toplevel(self)
        add_client_window.title("Agregar Cliente")

        tk.Label(add_client_window, text="Nombre:").pack()
        client_name_entry = tk.Entry(add_client_window)
        client_name_entry.pack()

        tk.Button(add_client_window, text="Agregar", command=lambda: self.save_client(client_name_entry.get(), add_client_window)).pack()
        tk.Button(add_client_window, text="Cancelar", command=add_client_window.destroy).pack(pady=10)

    def edit_client_window(self):
        edit_client_window = tk.Toplevel(self)
        edit_client_window.title("Editar Cliente")

        clients_data = self.load_data("clientes.json")
        client_names = [client["nombre"] for client in clients_data]

        tk.Label(edit_client_window, text="Selecciona el cliente a editar:").pack()
        client_choice = tk.StringVar(edit_client_window)
        client_choice.set(client_names[0] if client_names else "No hay clientes")
        tk.OptionMenu(edit_client_window, client_choice, *client_names).pack()

        tk.Label(edit_client_window, text="Nuevo nombre:").pack()
        new_name_entry = tk.Entry(edit_client_window)
        new_name_entry.pack()

        tk.Button(edit_client_window, text="Guardar Cambios", command=lambda: self.save_edited_client(client_choice.get(), new_name_entry.get(), edit_client_window)).pack()
        tk.Button(edit_client_window, text="Cancelar", command=edit_client_window.destroy).pack(pady=10)

    def delete_client_window(self):
        delete_client_window = tk.Toplevel(self)
        delete_client_window.title("Eliminar Cliente")

        clients_data = self.load_data("clientes.json")
        client_names = [client["nombre"] for client in clients_data]

        tk.Label(delete_client_window, text="Selecciona el cliente a eliminar:").pack()
        client_choice = tk.StringVar(delete_client_window)
        client_choice.set(client_names[0] if client_names else "No hay clientes")
        tk.OptionMenu(delete_client_window, client_choice, *client_names).pack()

        tk.Button(delete_client_window, text="Eliminar", command=lambda: self.confirm_delete_client(client_choice.get(), delete_client_window)).pack()
        tk.Button(delete_client_window, text="Cancelar", command=delete_client_window.destroy).pack(pady=10)

    def save_client(self, name, window):
        if name:
            new_client = {"id": len(self.load_data("clientes.json")) + 1, "nombre": name}
            clients_data = self.load_data("clientes.json")
            clients_data.append(new_client)
            self.save_data("clientes.json", clients_data)
            window.destroy()
            self.show_clients()
            messagebox.showinfo("Éxito", "Cliente agregado correctamente")
        else:
            messagebox.showerror("Error", "Por favor, ingresa el nombre del cliente")

    def save_edited_client(self, old_name, new_name, window):
        if new_name:
            clients_data = self.load_data("clientes.json")
            for client in clients_data:
                if client["nombre"] == old_name:
                    client["nombre"] = new_name
                    break
            self.save_data("clientes.json", clients_data)
            window.destroy()
            self.show_clients()
            messagebox.showinfo("Éxito", "Cliente editado correctamente")
        else:
            messagebox.showerror("Error", "Por favor, ingresa el nuevo nombre del cliente")

    def confirm_delete_client(self, client_name, window):
        clients_data = self.load_data("clientes.json")
        updated_clients = [client for client in clients_data if client["nombre"] != client_name]
        self.save_data("clientes.json", updated_clients)
        window.destroy()
        self.show_clients()
        messagebox.showinfo("Éxito", f"Cliente '{client_name}' eliminado correctamente")

    def show_attentions(self):
       self.clear_frame()
       attentions_data = self.load_data("atenciones.json")

       if attentions_data:
         tk.Label(self, text="Atenciones").pack()
         for attention in attentions_data:
            id_text = f"ID: {attention.get('id', 'N/A')}"
            cliente_text = f"Cliente: {attention.get('cliente', 'N/A')}"
            animal_text = f"Animal: {attention.get('animal', 'N/A')}"
            fecha_text = f"Fecha: {attention.get('fecha', 'N/A')}"
            descripcion_text = f"Descripción: {attention.get('descripcion', 'N/A')}"
            
            tk.Label(self, text=f"{id_text} - {cliente_text} - {animal_text} - {fecha_text} - {descripcion_text}").pack()
       else:
          tk.Label(self, text="No hay atenciones registradas").pack()

       tk.Button(self, text="Agregar Atención", command=self.add_attention_window).pack()
       tk.Button(self, text="Editar Atención", command=self.edit_attention_window).pack()
       tk.Button(self, text="Eliminar Atención", command=self.delete_attention_window).pack()
       tk.Button(self, text="Back", command=self.show_menu).pack(pady=10)


    def add_attention_window(self):
        add_attention_window = tk.Toplevel(self)
        add_attention_window.title("Agregar Atención")

        tk.Label(add_attention_window, text="Cliente:").pack()
        client_names = [client["nombre"] for client in self.load_data("clientes.json")]
        selected_client = tk.StringVar(add_attention_window)
        selected_client.set(client_names[0] if client_names else "No hay clientes")
        tk.OptionMenu(add_attention_window, selected_client, *client_names).pack()

        tk.Label(add_attention_window, text="Animal:").pack()
        animal_names = [animal["nombre"] for animal in self.load_data("animals.json")]
        selected_animal = tk.StringVar(add_attention_window)
        selected_animal.set(animal_names[0] if animal_names else "No hay animales")
        tk.OptionMenu(add_attention_window, selected_animal, *animal_names).pack()

        tk.Label(add_attention_window, text="Fecha:").pack()
        date_entry = tk.Entry(add_attention_window)
        date_entry.pack()

        tk.Label(add_attention_window, text="Descripción:").pack()
        description_entry = tk.Entry(add_attention_window)
        description_entry.pack()

        tk.Button(add_attention_window, text="Agregar", command=lambda: self.save_attention(selected_client.get(), selected_animal.get(), date_entry.get(), description_entry.get(), add_attention_window)).pack()
        tk.Button(add_attention_window, text="Cancelar", command=add_attention_window.destroy).pack(pady=10)

    def save_attention(self, client, animal, date, description, window):
        if client and animal and date and description:
            new_attention = {
                "id": len(self.load_data("atenciones.json")) + 1,
                "cliente": client,
                "animal": animal,
                "fecha": date,
                "descripcion": description
            }
            attentions_data = self.load_data("atenciones.json")
            attentions_data.append(new_attention)
            self.save_data("atenciones.json", attentions_data)
            window.destroy()
            self.show_attentions()
            messagebox.showinfo("Éxito", "Atención agregada correctamente")
        else:
            messagebox.showerror("Error", "Por favor, ingresa todos los datos de la atención")

    def edit_attention_window(self):
        edit_attention_window = tk.Toplevel(self)
        edit_attention_window.title("Editar Atención")

        attentions_data = self.load_data("atenciones.json")
        attention_ids = [attention["id"] for attention in attentions_data]

        tk.Label(edit_attention_window, text="Selecciona la atención a editar:").pack()
        attention_choice = tk.StringVar(edit_attention_window)
        attention_choice.set(attention_ids[0] if attention_ids else "No hay atenciones")
        tk.OptionMenu(edit_attention_window, attention_choice, *attention_ids).pack()

        tk.Label(edit_attention_window, text="Nueva fecha:").pack()
        new_date_entry = tk.Entry(edit_attention_window)
        new_date_entry.pack()

        tk.Label(edit_attention_window, text="Nueva descripción:").pack()
        new_description_entry = tk.Entry(edit_attention_window)
        new_description_entry.pack()

        tk.Button(edit_attention_window, text="Guardar Cambios", command=lambda: self.save_edited_attention(attention_choice.get(), new_date_entry.get(), new_description_entry.get(), edit_attention_window)).pack()
        tk.Button(edit_attention_window, text="Cancelar", command=edit_attention_window.destroy).pack(pady=10)

    def save_edited_attention(self, attention_id, new_date, new_description, window):
        if new_date and new_description:
            attentions_data = self.load_data("atenciones.json")
            for attention in attentions_data:
                if attention["id"] == int(attention_id):
                    attention["fecha"] = new_date
                    attention["descripcion"] = new_description
                    break
            self.save_data("atenciones.json", attentions_data)
            window.destroy()
            self.show_attentions()
            messagebox.showinfo("Éxito", "Atención editada correctamente")
        else:
            messagebox.showerror("Error", "Por favor, ingresa todos los nuevos datos de la atención")

    def delete_attention_window(self):
        delete_attention_window = tk.Toplevel(self)
        delete_attention_window.title("Eliminar Atención")

        attentions_data = self.load_data("atenciones.json")
        attention_ids = [attention["id"] for attention in attentions_data]

        tk.Label(delete_attention_window, text="Selecciona la atención a eliminar:").pack()
        attention_choice = tk.StringVar(delete_attention_window)
        attention_choice.set(attention_ids[0] if attention_ids else "No hay atenciones")
        tk.OptionMenu(delete_attention_window, attention_choice, *attention_ids).pack()

        tk.Button(delete_attention_window, text="Eliminar", command=lambda: self.confirm_delete_attention(attention_choice.get(), delete_attention_window)).pack()
        tk.Button(delete_attention_window, text="Cancelar", command=delete_attention_window.destroy).pack(pady=10)

    def confirm_delete_attention(self, attention_id, window):
        attentions_data = self.load_data("atenciones.json")
        updated_attentions = [attention for attention in attentions_data if attention["id"] != int(attention_id)]
        self.save_data("atenciones.json", updated_attentions)
        window.destroy()
        self.show_attentions()
        messagebox.showinfo("Éxito", f"Atención '{attention_id}' eliminada correctamente")

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()