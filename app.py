import customtkinter as ctk
from database import inicializar_banco, registrar_usuario, verificar_login

# Inicializar o banco ao iniciar o app
inicializar_banco()

# Inicializar o tema do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Classe principal da aplicação
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Login")
        self.geometry("400x440")

        self.frame = ctk.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.label_titulo = ctk.CTkLabel(master=self.frame, text="Login de Usuários", font=("Arial", 20))
        self.label_titulo.pack(pady=12, padx=10)

        self.entry_usuario = ctk.CTkEntry(master=self.frame, placeholder_text="Usuário")
        self.entry_usuario.pack(pady=10, padx=10)

        # Campo de senha + botão de mostrar/ocultar
        self.senha_visivel = False
        self.entry_senha = ctk.CTkEntry(master=self.frame, placeholder_text="Senha", show="•")
        self.entry_senha.pack(pady=10, padx=10)
        self.botao_mostrar_senha = ctk.CTkButton(master=self.frame, text="👁", width=30, command=self.toggle_senha)
        self.botao_mostrar_senha.place(x=320, y=150)

        # Campo confirmar senha (aparece só no registro)
        self.confirmar_visivel = False
        self.entry_confirmar = ctk.CTkEntry(master=self.frame, placeholder_text="Confirmar Senha", show="•")
        self.botao_mostrar_confirmar = ctk.CTkButton(master=self.frame, text="👁", width=30, command=self.toggle_confirmar)

        self.entry_confirmar.pack(pady=10, padx=10)
        self.entry_confirmar.pack_forget()
        self.botao_mostrar_confirmar.place(x=320, y=210)
        self.botao_mostrar_confirmar.place_forget()

        self.label_feedback = ctk.CTkLabel(master=self.frame, text="", text_color="white")
        self.label_feedback.pack(pady=5)

        self.botao_acao = ctk.CTkButton(master=self.frame, text="Entrar", command=self.login)
        self.botao_acao.pack(pady=10, padx=10)

        self.botao_toggle = ctk.CTkButton(master=self.frame, text="Não tem conta? Registrar", command=self.trocar_modo)
        self.botao_toggle.pack(pady=5)

        self.modo = "login"

    def toggle_senha(self):
        self.senha_visivel = not self.senha_visivel
        self.entry_senha.configure(show="" if self.senha_visivel else "•")

    def toggle_confirmar(self):
        self.confirmar_visivel = not self.confirmar_visivel
        self.entry_confirmar.configure(show="" if self.confirmar_visivel else "•")

    def trocar_modo(self):
        if self.modo == "login":
            self.modo = "registro"
            self.label_titulo.configure(text="Registrar Usuário")
            self.botao_acao.configure(text="Registrar", command=self.registrar)
            self.botao_toggle.configure(text="Já tem conta? Login")
            self.entry_confirmar.pack(pady=10, padx=10)
            self.botao_mostrar_confirmar.place(x=320, y=210)
        else:
            self.modo = "login"
            self.label_titulo.configure(text="Login de Usuários")
            self.botao_acao.configure(text="Entrar", command=self.login)
            self.botao_toggle.configure(text="Não tem conta? Registrar")
            self.entry_confirmar.pack_forget()
            self.botao_mostrar_confirmar.place_forget()

        self.label_feedback.configure(text="", text_color="white")
        self.entry_usuario.delete(0, ctk.END)
        self.entry_senha.delete(0, ctk.END)
        self.entry_confirmar.delete(0, ctk.END)
        self.entry_usuario.focus()

    def exibir_popup(self, titulo, mensagem):
        popup = ctk.CTkToplevel(self)
        popup.title(titulo)
        popup.geometry("300x150")
        label = ctk.CTkLabel(popup, text=mensagem, font=("Arial", 16))
        label.pack(pady=30)
        btn = ctk.CTkButton(popup, text="OK", command=popup.destroy)
        btn.pack(pady=10)

    def exibir_boas_vindas(self, usuario):
        boas_vindas = ctk.CTkToplevel(self)
        boas_vindas.title("Bem-vindo")
        boas_vindas.geometry("300x200")
        label = ctk.CTkLabel(boas_vindas, text=f"Bem-vindo, {usuario}!", font=("Arial", 18))
        label.pack(pady=40)
        btn = ctk.CTkButton(boas_vindas, text="Fechar", command=boas_vindas.destroy)
        btn.pack(pady=10)

    def login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        if not usuario or not senha:
            self.label_feedback.configure(text="Preencha todos os campos.", text_color="red")
            return

        sucesso, msg = verificar_login(usuario, senha)
        self.label_feedback.configure(text=msg, text_color="green" if sucesso else "red")

        if sucesso:
            self.entry_usuario.delete(0, ctk.END)
            self.entry_senha.delete(0, ctk.END)
            self.exibir_boas_vindas(usuario)

    def registrar(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()
        confirmar = self.entry_confirmar.get().strip()

        if not usuario or not senha or not confirmar:
            self.label_feedback.configure(text="Preencha todos os campos.", text_color="red")
            return

        if senha != confirmar:
            self.label_feedback.configure(text="As senhas não coincidem.", text_color="red")
            return

        sucesso, msg = registrar_usuario(usuario, senha)
        self.label_feedback.configure(text=msg, text_color="green" if sucesso else "red")

        if sucesso:
            self.entry_usuario.delete(0, ctk.END)
            self.entry_senha.delete(0, ctk.END)
            self.entry_confirmar.delete(0, ctk.END)
            self.exibir_popup("Sucesso", "Usuário registrado com sucesso!")

if __name__ == "__main__":
    app = App()
    app.mainloop()
