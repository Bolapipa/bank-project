import customtkinter as ctk
from tkinter import messagebox
import bank_logic as bl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# --- Paletas de Temas ---
THEMES = {
    "EpicBlue (Default)": {
        "bg_light": "#F5F7FA", "frame": "#FFFFFF", "sidebar": "#2C3E50", "sidebar_button": "#34495E",
        "primary": "#3498DB", "primary_hover": "#2980B9", "text": "#2C3E50",
        "sidebar_text": "#ECF0F1", "success": "#2ECC71", "error": "#E74C3C"
    },
    "Dark Mode": {
        "bg_light": "#2C3E50", "frame": "#34495E", "sidebar": "#212F3D", "sidebar_button": "#34495E",
        "primary": "#5DADE2", "primary_hover": "#85C1E9", "text": "#ECF0F1",
        "sidebar_text": "#ECF0F1", "success": "#2ECC71", "error": "#E74C3C"
    },
    "Forest Green": {
        "bg_light": "#E8F8F5", "frame": "#FFFFFF", "sidebar": "#1E8449", "sidebar_button": "#28B463",
        "primary": "#2ECC71", "primary_hover": "#28B463", "text": "#145A32",
        "sidebar_text": "#FFFFFF", "success": "#2ECC71", "error": "#E74C3C"
    }
}

FONTS = {
    "large": ("Roboto", 24, "bold"), "medium": ("Roboto", 16, "bold"),
    "small": ("Roboto", 12), "small_bold": ("Roboto", 12, "bold")
}

class EpicBankApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EpicBank")
        self.geometry("900x650")
        self.current_user_cpf = None
        self.theme_name = "EpicBlue (Default)"

        bl.carregar_dados()

        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, RegisterPage, MainPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, 'update_on_show'):
            frame.update_on_show()
        frame.tkraise()

    def login_success(self, cpf):
        self.current_user_cpf = cpf
        self.show_frame("MainPage")

    def get_colors(self):
        return THEMES[self.theme_name]

    def apply_theme(self, theme_name):
        self.theme_name = theme_name
        colors = self.get_colors()
        ctk.set_appearance_mode("Dark" if theme_name == "Dark Mode" else "Light")
        # Recriar frames para aplicar o tema completamente
        for F in (LoginPage, RegisterPage, MainPage):
            page_name = F.__name__
            self.frames[page_name].destroy()
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainPage.__name__ if self.current_user_cpf else LoginPage.__name__)


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.colors = self.controller.get_colors()
        super().__init__(parent, fg_color=self.colors["bg_light"])

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        login_frame = ctk.CTkFrame(self, fg_color=self.colors["frame"], corner_radius=10)
        login_frame.grid(row=0, column=0, padx=20, pady=20)

        title = ctk.CTkLabel(login_frame, text="EpicBank", font=FONTS["large"], text_color=self.colors["primary"])
        title.pack(pady=(40, 20))

        self.cpf_entry = ctk.CTkEntry(login_frame, placeholder_text="CPF", width=250, height=40)
        self.cpf_entry.pack(pady=10, padx=40)
        self.password_entry = ctk.CTkEntry(login_frame, placeholder_text="Senha", show="*", width=250, height=40)
        self.password_entry.pack(pady=10, padx=40)

        login_button = ctk.CTkButton(login_frame, text="Login", command=self.login, width=250, height=40, fg_color=self.colors["primary"], hover_color=self.colors["primary_hover"])
        login_button.pack(pady=20, padx=40)

        register_button = ctk.CTkButton(login_frame, text="Não tem conta? Cadastre-se", command=lambda: controller.show_frame("RegisterPage"), fg_color="transparent", text_color=self.colors["primary"])
        register_button.pack(pady=(0, 40))

    def login(self):
        success, message, user_cpf = bl.login_user(self.cpf_entry.get(), self.password_entry.get())
        if success:
            self.controller.login_success(user_cpf)
        else:
            messagebox.showerror("Erro de Login", message)

# RegisterPage (sem grandes mudanças de design, apenas cores)
class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.colors = self.controller.get_colors()
        super().__init__(parent, fg_color=self.colors["bg_light"])
        # ... (código de widgets similar ao anterior, mas usando self.colors)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        register_frame = ctk.CTkFrame(self, fg_color=self.colors["frame"], corner_radius=10)
        register_frame.grid(row=0, column=0, padx=20, pady=20)

        title = ctk.CTkLabel(register_frame, text="Cadastro de Usuário", font=FONTS["large"], text_color=self.colors["primary"])
        title.pack(pady=(20, 10))

        self.cpf_entry = ctk.CTkEntry(register_frame, placeholder_text="CPF (só números)", width=300, height=35)
        self.cpf_entry.pack(pady=5, padx=20)
        self.nome_entry = ctk.CTkEntry(register_frame, placeholder_text="Nome Completo", width=300, height=35)
        self.nome_entry.pack(pady=5, padx=20)
        self.email_entry = ctk.CTkEntry(register_frame, placeholder_text="Email", width=300, height=35)
        self.email_entry.pack(pady=5, padx=20)
        self.telefone_entry = ctk.CTkEntry(register_frame, placeholder_text="Telefone", width=300, height=35)
        self.telefone_entry.pack(pady=5, padx=20)
        self.senha_entry = ctk.CTkEntry(register_frame, placeholder_text="Senha (4 dígitos)", show="*", width=300, height=35)
        self.senha_entry.pack(pady=5, padx=20)
        self.confirma_senha_entry = ctk.CTkEntry(register_frame, placeholder_text="Confirmar Senha", show="*", width=300, height=35)
        self.confirma_senha_entry.pack(pady=5, padx=20)

        register_button = ctk.CTkButton(register_frame, text="Cadastrar", command=self.register, width=300, height=40, fg_color=self.colors["primary"], hover_color=self.colors["primary_hover"])
        register_button.pack(pady=20, padx=20)

        back_button = ctk.CTkButton(register_frame, text="Voltar para Login", command=lambda: controller.show_frame("LoginPage"), fg_color="transparent", text_color=self.colors["primary"])
        back_button.pack(pady=(0, 20))

    def register(self):
        success, message = bl.registrar_usuario(
            cpf=self.cpf_entry.get(), nome=self.nome_entry.get(), email=self.email_entry.get(),
            telefone=self.telefone_entry.get(), senha=self.senha_entry.get(), confirma_senha=self.confirma_senha_entry.get()
        )
        if success:
            messagebox.showinfo("Sucesso", message)
            self.controller.show_frame("LoginPage")
        else:
            messagebox.showerror("Erro no Cadastro", message)

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.colors = self.controller.get_colors()
        super().__init__(parent, fg_color=self.colors["bg_light"])

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=self.colors["sidebar"], corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)

        logo_label = ctk.CTkLabel(self.sidebar, text="EpicBank", font=FONTS["large"], text_color=self.colors["sidebar_text"])
        logo_label.grid(row=0, column=0, padx=20, pady=30)

        buttons = {
            "Dashboard": self.show_dashboard_frame,
            "Operações": self.show_operations_frame,
            "Investimentos": self.show_investments_frame,
            "Análise Gráfica": self.show_analytics_frame,
        }
        for i, (text, command) in enumerate(buttons.items()):
            ctk.CTkButton(self.sidebar, text=text, command=command, height=40, corner_radius=0, fg_color="transparent", text_color=self.colors["sidebar_text"], hover_color="#34495E", anchor="w", font=FONTS["small_bold"]).grid(row=i+1, column=0, sticky="ew", padx=10, pady=5)

        # --- Theme Menu ---
        theme_menu = ctk.CTkOptionMenu(self.sidebar, values=list(THEMES.keys()), command=self.controller.apply_theme, fg_color=self.colors["sidebar_button"], button_color=self.colors["sidebar_button"], button_hover_color=self.colors["primary_hover"])
        theme_menu.grid(row=8, column=0, padx=20, pady=10, sticky="s")

        self.logout_button = ctk.CTkButton(self.sidebar, text="Sair", command=self.logout, fg_color=self.colors["error"], hover_color="#c0392b")
        self.logout_button.grid(row=9, column=0, padx=20, pady=20, sticky="s")

        # --- Header ---
        self.header = ctk.CTkFrame(self, height=80, fg_color=self.colors["frame"], corner_radius=0)
        self.header.grid(row=0, column=1, sticky="nsew")
        self.header.grid_columnconfigure(0, weight=1)
        self.welcome_label = ctk.CTkLabel(self.header, text="", font=FONTS["medium"], text_color=self.colors["text"])
        self.welcome_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.balance_label = ctk.CTkLabel(self.header, text="", font=FONTS["large"], text_color=self.colors["primary"])
        self.balance_label.grid(row=0, column=1, padx=20, pady=10, sticky="e")

        # --- Main Content Area ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=1)

        self.operation_frames = {}
        self._create_frames()
        self.show_dashboard_frame()

    def _create_frames(self):
        # --- Dashboard ---
        self.operation_frames["dashboard"] = self._create_dashboard_frame(self.main_content)
        # --- Operações (Depósito, Saque, PIX) ---
        self.operation_frames["operations"] = self._create_operations_frame(self.main_content)
        # --- Investimentos ---
        self.operation_frames["investments"] = self._create_investments_frame(self.main_content)
        # --- Análise Gráfica ---
        self.operation_frames["analytics"] = self._create_analytics_frame(self.main_content)

        for frame in self.operation_frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def _create_dashboard_frame(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        ctk.CTkLabel(frame, text="Transações Recentes", font=FONTS["medium"], text_color=self.colors["text"]).pack(anchor="w", pady=(0,10))
        self.recent_transactions_text = ctk.CTkTextbox(frame, wrap="word", height=300, fg_color=self.colors["frame"], text_color=self.colors["text"])
        self.recent_transactions_text.pack(fill="both", expand=True)
        return frame

    def _create_operations_frame(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid_columnconfigure((0,1,2), weight=1)

        # Depósito
        dep_card = ctk.CTkFrame(frame, fg_color=self.colors["frame"])
        dep_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(dep_card, text="Depósito", font=FONTS["small_bold"]).pack(pady=10)
        self.deposito_entry = ctk.CTkEntry(dep_card, placeholder_text="Valor")
        self.deposito_entry.pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(dep_card, text="Confirmar", command=self.realizar_deposito, fg_color=self.colors["primary"], hover_color=self.colors["primary_hover"]).pack(pady=10)

        # Saque
        saq_card = ctk.CTkFrame(frame, fg_color=self.colors["frame"])
        saq_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(saq_card, text="Saque", font=FONTS["small_bold"]).pack(pady=10)
        self.saque_entry = ctk.CTkEntry(saq_card, placeholder_text="Valor")
        self.saque_entry.pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(saq_card, text="Confirmar", command=self.realizar_saque, fg_color=self.colors["primary"], hover_color=self.colors["primary_hover"]).pack(pady=10)

        # PIX
        pix_card = ctk.CTkFrame(frame, fg_color=self.colors["frame"])
        pix_card.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(pix_card, text="PIX", font=FONTS["small_bold"]).pack(pady=10)
        self.pix_cpf_entry = ctk.CTkEntry(pix_card, placeholder_text="CPF Destino")
        self.pix_cpf_entry.pack(pady=5, padx=10, fill="x")
        self.pix_valor_entry = ctk.CTkEntry(pix_card, placeholder_text="Valor")
        self.pix_valor_entry.pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(pix_card, text="Confirmar", command=self.realizar_pix, fg_color=self.colors["primary"], hover_color=self.colors["primary_hover"]).pack(pady=10)

        return frame

    def _create_investments_frame(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        # Market Prices
        market_frame = ctk.CTkFrame(frame, fg_color=self.colors["frame"])
        market_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(market_frame, text="Mercado Agora", font=FONTS["medium"]).pack()
        self.market_label = ctk.CTkLabel(market_frame, text="", font=FONTS["small"], justify="left")
        self.market_label.pack(pady=5)

        # Portfolio
        portfolio_frame = ctk.CTkFrame(frame, fg_color=self.colors["frame"])
        portfolio_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(portfolio_frame, text="Meu Portfólio", font=FONTS["medium"]).pack(pady=10)
        self.portfolio_text = ctk.CTkTextbox(portfolio_frame, fg_color=self.colors["frame"], text_color=self.colors["text"])
        self.portfolio_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Buy/Sell
        trade_frame = ctk.CTkFrame(frame, fg_color=self.colors["frame"])
        trade_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(trade_frame, text="Operar Ativos", font=FONTS["medium"]).pack(pady=10)
        self.asset_entry = ctk.CTkEntry(trade_frame, placeholder_text="Ativo (ex: BTC, EPIC-A)")
        self.asset_entry.pack(pady=5, padx=10, fill="x")
        self.quantity_entry = ctk.CTkEntry(trade_frame, placeholder_text="Quantidade")
        self.quantity_entry.pack(pady=5, padx=10, fill="x")
        buy_button = ctk.CTkButton(trade_frame, text="Comprar", command=self.comprar_ativo, fg_color=self.colors["success"])
        buy_button.pack(pady=10, padx=10, fill="x")
        sell_button = ctk.CTkButton(trade_frame, text="Vender", command=self.vender_ativo, fg_color=self.colors["error"])
        sell_button.pack(pady=10, padx=10, fill="x")

        return frame

    def _create_analytics_frame(self, parent):
        frame = ctk.CTkFrame(parent, fg_color=self.colors["frame"], corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor=self.colors["frame"])
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
        return frame

    def show_dashboard_frame(self): self.show_operation_frame("dashboard")
    def show_operations_frame(self): self.show_operation_frame("operations")
    def show_investments_frame(self): self.show_operation_frame("investments")
    def show_analytics_frame(self): self.show_operation_frame("analytics")

    def show_operation_frame(self, name):
        for frame_name, frame in self.operation_frames.items():
            frame.grid_remove()
        self.operation_frames[name].grid()
        self.update_on_show() # Always update data when changing view

    def update_on_show(self):
        if not self.controller.current_user_cpf: return
        user_data = bl.get_user_data(self.controller.current_user_cpf)
        if not user_data: return

        # Header
        nome = user_data.get("nome", "").split()[0]
        saldo = user_data.get("saldo", 0.0)
        self.welcome_label.configure(text=f"Olá, {nome}!")
        self.balance_label.configure(text=f"R$ {saldo:.2f}")

        # Dashboard
        extrato, _ = bl.get_extrato(self.controller.current_user_cpf)
        recent = "\n".join(extrato.strip().split("\n")[-10:])
        self.recent_transactions_text.delete("1.0", "end")
        self.recent_transactions_text.insert("1.0", recent if recent else "Nenhuma transação.")

        # Investments
        self.update_market_prices()
        self.update_portfolio_display()

        # Analytics
        self.update_analytics_chart()

    def update_market_prices(self):
        prices = bl.get_market_prices()
        price_text = ""
        for cat, assets in prices.items():
            price_text += f"{cat.upper()}:\n"
            for asset, price in assets.items():
                price_text += f"  {asset}: R$ {price:.2f}\n"
        self.market_label.configure(text=price_text)

    def update_portfolio_display(self):
        user_data = bl.get_user_data(self.controller.current_user_cpf)
        portfolio = user_data.get("portfolio", {})
        portfolio_text = ""
        total_value = 0
        prices = bl.get_market_prices()
        for cat, assets in portfolio.items():
            if assets:
                portfolio_text += f"{cat.upper()}:\n"
                for asset, qty in assets.items():
                    price = prices.get(cat, {}).get(asset, 0)
                    value = qty * price
                    total_value += value
                    portfolio_text += f"  {asset}: {qty:.4f} (R$ {value:.2f})\n"
        self.portfolio_text.delete("1.0", "end")
        self.portfolio_text.insert("1.0", portfolio_text if portfolio_text else "Nenhum ativo na carteira.")

    def update_analytics_chart(self):
        user_data = bl.get_user_data(self.controller.current_user_cpf)
        if not user_data: return

        labels = ['Saldo em Conta']
        sizes = [user_data.get("saldo", 0)]
        portfolio_value = 0
        prices = bl.get_market_prices()

        for cat, assets in user_data.get("portfolio", {}).items():
            for asset, qty in assets.items():
                portfolio_value += qty * prices.get(cat, {}).get(asset, 0)
        
        if portfolio_value > 0:
            labels.append('Investimentos')
            sizes.append(portfolio_value)

        self.ax.clear()
        if sum(sizes) > 0:
            self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
                        colors=[self.colors["primary"], self.colors["success"]],
                        textprops={'color': self.colors["text"]})
        else:
            self.ax.text(0.5, 0.5, "Sem dados para exibir", ha='center', va='center', color=self.colors["text"])
        
        self.ax.axis('equal')
        self.fig.set_facecolor(self.colors["frame"])
        self.canvas.draw()

    def _handle_operation(self, func, entry, *args):
        try:
            val = float(entry.get())
            success, msg = func(self.controller.current_user_cpf, *args, val)
            messagebox.showinfo("Sucesso" if success else "Erro", msg)
            if success: entry.delete(0, 'end')
            self.update_on_show()
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")

    def realizar_deposito(self): self._handle_operation(bl.depositar, self.deposito_entry)
    def realizar_saque(self): self._handle_operation(bl.sacar, self.saque_entry)
    def realizar_pix(self):
        self._handle_operation(bl.pix, self.pix_valor_entry, self.pix_cpf_entry.get())
        self.pix_cpf_entry.delete(0, 'end')

    def _trade_asset(self, trade_func):
        asset = self.asset_entry.get().upper()
        quantity_str = self.quantity_entry.get()
        cat = 'cripto' if asset in bl.SIMULATED_MARKET['cripto'] else 'acoes'
        if asset not in bl.SIMULATED_MARKET[cat]:
            messagebox.showerror("Erro", "Ativo não encontrado.")
            return
        try:
            quantity = float(quantity_str)
            success, msg = trade_func(self.controller.current_user_cpf, cat, asset, quantity)
            messagebox.showinfo("Sucesso" if success else "Erro", msg)
            if success:
                self.asset_entry.delete(0, 'end')
                self.quantity_entry.delete(0, 'end')
            self.update_on_show()
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")

    def comprar_ativo(self): self._trade_asset(bl.comprar_investimento)
    def vender_ativo(self): self._trade_asset(bl.vender_investimento)

    def logout(self):
        self.controller.current_user_cpf = None
        self.controller.show_frame("LoginPage")

if __name__ == "__main__":
    app = EpicBankApp()
    app.mainloop()
