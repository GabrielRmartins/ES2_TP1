import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
from database_manager import DatabaseManager
from movie import Movie

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meu Catálogo de Filmes")
        self.db = DatabaseManager()
        self._setup_ui()

    def _setup_ui(self):
        self.root.option_add("*Font", ("Segoe UI", 10))

        title = ttk.Label(self.root, text="Meu Catálogo de Filmes", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, pady=(10, 5))

        form_frame = ttk.LabelFrame(self.root, text="Adicionar Filme", padding=15)
        form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        labels = ["Nome do Filme:", "Descrição:", "Diretor:", "Categorias (separadas por vírgula):", "Nota (0 a 10):"]
        self.entries = []

        for i, label_text in enumerate(labels):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky="e", padx=5, pady=4)
            entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, sticky="w", pady=4)
            self.entries.append(entry)

        self.name_entry, self.desc_entry, self.dir_entry, self.cat_entry, self.rating_entry = self.entries

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=(10, 0))
        ttk.Button(button_frame, text="Adicionar Filme", command=self.add_movie).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Carregar Filmes", command=self.load_movies).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Ver Perfil", command=self.ver_perfil).grid(row=0, column=2, padx=5)

        table_frame = ttk.LabelFrame(self.root, text="Filmes Cadastrados", padding=10)
        table_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(table_frame, columns=("Nome", "Nota"), show="headings", height=8)
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Nota", text="Nota")
        self.tree.column("Nome", anchor="w", width=280)
        self.tree.column("Nota", anchor="center", width=60)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.status_label = ttk.Label(self.root, text="", foreground="green")
        self.status_label.grid(row=3, column=0, pady=(0, 15))

        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def load_movies(self):
        try:
            movies = self.db.get_all_movies_with_ratings()
            self.tree.delete(*self.tree.get_children())
            for m in movies:
                self.tree.insert("", "end", values=(m.get_name(), m.get_rating()))
            self.status_label.config(text=f"{len(movies)} filme(s) carregado(s)")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar filmes: {e}")

    def add_movie(self):
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        director = self.dir_entry.get()
        categories = [c.strip() for c in self.cat_entry.get().split(",")]
        try:
            rating = float(self.rating_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Nota inválida.")
            return

        if not name:
            messagebox.showwarning("Aviso", "Preencha o nome do filme.")
            return

        movie = Movie(name, desc, categories, rating, director)
        try:
            self.db.add_movie(movie)
            self.status_label.config(text=f"Filme '{name}' adicionado com sucesso!", foreground="green")
            self.load_movies()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar filme: {e}")

    def ver_perfil(self):
        try:
            media, filmes = self.db.get_last_movies_with_average(limit=5)
            categorias = self.db.get_top_categories(limit=5)

            with open("templates/profile.html", "r", encoding="utf-8") as f:
                html_template = f.read()

            html_resultado = html_template.replace("{{usuario}}", "Você")
            html_resultado = html_resultado.replace("{{n}}", str(len(filmes)))
            html_resultado = html_resultado.replace("{{media}}", f"{media:.2f}")

            filmes_html = ""
            for i, m in enumerate(filmes, 1):
                filmes_html += f"""
                <tr>
                    <td>{i}</td>
                    <td>{m['title']}</td>
                    <td>{m['director']}</td>
                    <td>{', '.join(m['categories'])}</td>
                    <td>{m['rating']}</td>
                </tr>"""

            html_resultado = html_resultado.replace("{{filmes}}", filmes_html)
            html_resultado = html_resultado.replace("{{categorias_labels}}", str([c[0] for c in categorias]))
            html_resultado = html_resultado.replace("{{categorias_counts}}", str([c[1] for c in categorias]))

            with open("perfil_usuario.html", "w", encoding="utf-8") as f:
                f.write(html_resultado)
            webbrowser.open("perfil_usuario.html")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar perfil: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()