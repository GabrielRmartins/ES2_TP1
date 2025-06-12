import tkinter as tk
from tkinter import messagebox
from database_manager import DatabaseManager
from movie import Movie

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meu Gerenciador de Filmes")
        self.root.geometry("500x600")

        self.db = DatabaseManager()

        # Título
        self.title_label = tk.Label(root, text="Cadastrar Filme", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        # Entradas do formulário
        self.name_entry = self._create_entry("Nome do Filme:")
        self.desc_entry = self._create_entry("Descrição:")
        self.dir_entry = self._create_entry("Diretor:")
        self.cat_entry = self._create_entry("Categorias (separadas por vírgula):")
        self.rating_entry = self._create_entry("Nota (0 a 10):")

        self.add_button = tk.Button(root, text="Adicionar Filme", command=self.add_movie, bg="blue", fg="white")
        self.add_button.pack(pady=10)

        # Botão para visualizar perfil
        self.profile_button = tk.Button(root, text="Ver Perfil", command=self.generate_profile, bg="green", fg="white")
        self.profile_button.pack(pady=5)

        # Lista de filmes
        self.movies_listbox = tk.Listbox(root, width=60, height=15)
        self.movies_listbox.pack(pady=10)

        self.load_movies()

    def _create_entry(self, label_text):
        label = tk.Label(self.root, text=label_text)
        label.pack()
        entry = tk.Entry(self.root, width=50)
        entry.pack()
        return entry

    def add_movie(self):
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        director = self.dir_entry.get()
        categories = [c.strip() for c in self.cat_entry.get().split(",") if c.strip()]

        try:
            rating = float(self.rating_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Nota inválida.")
            return

        if not (name and rating >= 0 and rating <= 10):
            messagebox.showwarning("Aviso", "Preencha todos os campos corretamente.")
            return

        movie = Movie(name, desc, categories, rating, director)

        try:
            self.db.add_movie(movie)
            messagebox.showinfo("Sucesso", f"Filme '{name}' adicionado!")
            self.load_movies()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar filme: {e}")

    def load_movies(self):
        self.movies_listbox.delete(0, tk.END)
        try:
            movies = self.db.get_all_movies_with_ratings()
            for m in movies:
                self.movies_listbox.insert(tk.END, f"{m.get_name()} - Nota: {m.get_rating()}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar filmes: {e}")

    def generate_profile(self):
        media, filmes = self.db.get_last_movies_with_average(5)
        categorias_raw = self.db.get_top_categories(5)

        categorias_labels = [x[0] for x in categorias_raw]
        categorias_counts = [x[1] for x in categorias_raw]

        filmes_html = ""
        for idx, f in enumerate(filmes, 1):
            filmes_html += f"<tr><td>{idx}</td><td>{f['title']}</td><td>{f['director']}</td><td>{', '.join(f['categories'])}</td><td>{f['rating']}</td></tr>"

        with open("templates/profile.html", "r", encoding="utf-8") as file:
            html = file.read()

        html = html.replace("{{usuario}}", "Você")
        html = html.replace("{{n}}", str(len(filmes)))
        html = html.replace("{{media}}", f"{media:.2f}")
        html = html.replace("{{categorias_labels}}", str(categorias_labels))
        html = html.replace("{{categorias_counts}}", str(categorias_counts))
        html = html.replace("{{filmes}}", filmes_html)

        with open("profile_rendered.html", "w", encoding="utf-8") as out:
            out.write(html)

        messagebox.showinfo("Perfil Gerado", "Arquivo 'profile_rendered.html' criado com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()
