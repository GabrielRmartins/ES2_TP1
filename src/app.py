# src/app.py
import tkinter as tk
from tkinter import messagebox
from src.database_manager import DatabaseManager
from src.movie import Movie

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Manager")

        self.db = DatabaseManager()

        # Usuário
        self.user_label = tk.Label(root, text="Usuário:")
        self.user_label.pack()
        self.user_entry = tk.Entry(root)
        self.user_entry.pack()

        # Botão para carregar filmes do usuário
        self.load_button = tk.Button(root, text="Carregar Filmes", command=self.load_movies)
        self.load_button.pack()

        # Área de exibição
        self.movies_listbox = tk.Listbox(root, width=50)
        self.movies_listbox.pack()

        # Formulário para adicionar filme
        self.name_entry = self._create_entry("Nome do Filme:")
        self.desc_entry = self._create_entry("Descrição:")
        self.dir_entry = self._create_entry("Diretor:")
        self.cat_entry = self._create_entry("Categorias (separadas por vírgula):")
        self.rating_entry = self._create_entry("Nota (0 a 10):")

        self.add_button = tk.Button(root, text="Adicionar Filme", command=self.add_movie)
        self.add_button.pack()

    def _create_entry(self, label_text):
        label = tk.Label(self.root, text=label_text)
        label.pack()
        entry = tk.Entry(self.root)
        entry.pack()
        return entry

    def load_movies(self):
        user = self.user_entry.get()
        if not user:
            messagebox.showwarning("Aviso", "Digite um nome de usuário.")
            return

        try:
            movies = self.db.get_all_user_table_movies(user)
            self.movies_listbox.delete(0, tk.END)
            for m in movies:
                self.movies_listbox.insert(tk.END, f"{m.get_name()} (Nota: {m.get_rating()})")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar filmes: {e}")

    def add_movie(self):
        user = self.user_entry.get()
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        director = self.dir_entry.get()
        categories = [c.strip() for c in self.cat_entry.get().split(",")]
        try:
            rating = float(self.rating_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Nota inválida.")
            return

        if not (user and name):
            messagebox.showwarning("Aviso", "Preencha os campos obrigatórios.")
            return

        movie = Movie(name, desc, categories, rating, director)
        try:
            self.db.add_movie_to_user_table(user, movie)
            messagebox.showinfo("Sucesso", f"Filme '{name}' adicionado!")
            self.load_movies()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar filme: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()
