import json
from pathlib import Path

import customtkinter as ctk


ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

ARQUIVO_DADOS = Path(__file__).with_name("dados_salvos.json")

app = ctk.CTk()
app.title("Verificador de maioridade")
app.geometry("460x540")
app.minsize(400, 500)

titulo = ctk.CTkLabel(
    app,
    text="Verificador de maioridade",
    font=ctk.CTkFont(size=24, weight="bold"),
)
titulo.pack(pady=(36, 8))

subtitulo = ctk.CTkLabel(
    app,
    text="Informe seus dados para consultar o resultado.",
    font=ctk.CTkFont(size=14),
    text_color=("#5b6472", "#aab2bf"),
)
subtitulo.pack(pady=(0, 24))

campo_nome = ctk.CTkEntry(
    app,
    placeholder_text="Seu nome",
    width=320,
    height=42,
)
campo_nome.pack(pady=8)

campo_email = ctk.CTkEntry(
    app,
    placeholder_text="Seu e-mail",
    width=320,
    height=42,
)
campo_email.pack(pady=8)

campo_idade = ctk.CTkEntry(
    app,
    placeholder_text="Sua idade",
    width=320,
    height=42,
)
campo_idade.pack(pady=8)

resultado = ctk.CTkLabel(
    app,
    text="",
    font=ctk.CTkFont(size=15, weight="bold"),
    wraplength=360,
)
resultado.pack(pady=(18, 8))


def obter_dados_formulario():
    nome = campo_nome.get().strip()
    email = campo_email.get().strip()
    idade_texto = campo_idade.get().strip()

    if not nome:
        resultado.configure(text="Digite seu nome.", text_color="#c2410c")
        campo_nome.focus()
        return None

    if not email:
        resultado.configure(text="Digite seu e-mail.", text_color="#c2410c")
        campo_email.focus()
        return None

    try:
        idade = int(idade_texto)
    except ValueError:
        resultado.configure(
            text="Digite uma idade válida usando números inteiros.",
            text_color="#c2410c",
        )
        campo_idade.focus()
        return None

    if idade < 0:
        resultado.configure(text="A idade não pode ser negativa.", text_color="#c2410c")
        campo_idade.focus()
        return None

    return {"nome": nome, "email": email, "idade": idade}


def carregar_dados():
    if not ARQUIVO_DADOS.exists():
        return []

    with ARQUIVO_DADOS.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, list):
        raise ValueError("O arquivo de dados não contém uma lista.")

    return dados


def verificar_idade():
    dados = obter_dados_formulario()
    if dados is None:
        return

    if dados["idade"] >= 18:
        mensagem = (
            f"Olá, {dados['nome']}! Você tem {dados['idade']} anos e é maior de idade. "
            f"E-mail: {dados['email']}"
        )
        cor = ("#16794b", "#5dd39e")
    else:
        mensagem = (
            f"Olá, {dados['nome']}! Você tem {dados['idade']} anos e ainda é menor de idade. "
            f"E-mail: {dados['email']}"
        )
        cor = ("#a15c00", "#f4bd50")

    resultado.configure(text=mensagem, text_color=cor)


def salvar_dados():
    dados = obter_dados_formulario()
    if dados is None:
        return

    try:
        cadastros = carregar_dados()
        cadastros.append(dados)
        with ARQUIVO_DADOS.open("w", encoding="utf-8") as arquivo:
            json.dump(cadastros, arquivo, ensure_ascii=False, indent=2)
    except (OSError, ValueError):
        resultado.configure(
            text="Não foi possível salvar. Verifique o arquivo de dados.",
            text_color="#c2410c",
        )
        return

    resultado.configure(
        text=f"Dados de {dados['nome']} salvos com sucesso.",
        text_color=("#16794b", "#5dd39e"),
    )


def mostrar_dados_salvos():
    janela = ctk.CTkToplevel(app)
    janela.title("Dados salvos")
    janela.geometry("760x500")
    janela.minsize(560, 360)

    cabecalho = ctk.CTkFrame(janela, fg_color="transparent")
    cabecalho.pack(fill="x", padx=24, pady=(22, 12))
    cabecalho.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        cabecalho,
        text="Cadastros salvos",
        font=ctk.CTkFont(size=22, weight="bold"),
    ).grid(row=0, column=0, sticky="w")

    resumo = ctk.CTkLabel(cabecalho, text="")
    resumo.grid(row=1, column=0, sticky="w", pady=(4, 0))

    lista = ctk.CTkScrollableFrame(janela, corner_radius=8)
    lista.pack(fill="both", expand=True, padx=24, pady=(0, 16))

    def atualizar_lista():
        for item in lista.winfo_children():
            item.destroy()

        try:
            cadastros = carregar_dados()
        except (OSError, ValueError):
            resumo.configure(text="Não foi possível ler o arquivo de dados.")
            return

        resumo.configure(text=f"{len(cadastros)} cadastro(s)")

        if not cadastros:
            ctk.CTkLabel(
                lista,
                text="Ainda não há dados salvos.",
                text_color=("#5b6472", "#aab2bf"),
            ).grid(row=0, column=0, padx=12, pady=20, sticky="w")
            return

        for coluna, texto in enumerate(("Nome", "E-mail", "Idade")):
            ctk.CTkLabel(
                lista,
                text=texto,
                font=ctk.CTkFont(weight="bold"),
                anchor="w",
            ).grid(row=0, column=coluna, padx=10, pady=(8, 12), sticky="ew")

        lista.grid_columnconfigure(0, weight=2)
        lista.grid_columnconfigure(1, weight=3)
        lista.grid_columnconfigure(2, weight=1)

        for linha, cadastro in enumerate(cadastros, start=1):
            valores = (
                cadastro.get("nome", ""),
                cadastro.get("email", ""),
                str(cadastro.get("idade", "")),
            )
            for coluna, valor in enumerate(valores):
                ctk.CTkLabel(lista, text=valor, anchor="w").grid(
                    row=linha,
                    column=coluna,
                    padx=10,
                    pady=8,
                    sticky="ew",
                )

    botao_atualizar = ctk.CTkButton(
        cabecalho,
        text="Atualizar",
        command=atualizar_lista,
        width=100,
        height=34,
    )
    botao_atualizar.grid(row=0, column=1, rowspan=2, padx=(12, 0))

    atualizar_lista()


botao_verificar = ctk.CTkButton(
    app,
    text="Verificar idade",
    command=verificar_idade,
    width=320,
    height=44,
    font=ctk.CTkFont(size=15, weight="bold"),
)
botao_verificar.pack(pady=(12, 0))

acoes = ctk.CTkFrame(app, fg_color="transparent")
acoes.pack(pady=(10, 0))

botao_salvar = ctk.CTkButton(
    acoes,
    text="Salvar dados",
    command=salvar_dados,
    width=155,
    height=40,
)
botao_salvar.grid(row=0, column=0, padx=5)

botao_mostrar = ctk.CTkButton(
    acoes,
    text="Ver dados salvos",
    command=mostrar_dados_salvos,
    width=155,
    height=40,
    fg_color="transparent",
    border_width=1,
    text_color=("#1f2937", "#e5e7eb"),
    hover_color=("#e5e7eb", "#293241"),
)
botao_mostrar.grid(row=0, column=1, padx=5)

campo_nome.bind("<Return>", lambda _evento: campo_email.focus())
campo_email.bind("<Return>", lambda _evento: campo_idade.focus())
campo_idade.bind("<Return>", lambda _evento: verificar_idade())
campo_nome.focus()

app.mainloop()