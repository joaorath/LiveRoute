import os

import telebot
from dotenv import load_dotenv
from telebot import types

from data import IDIOMAS, TEXTOS
from recommendation import recomendar_lugares


load_dotenv()

TOKEN_TELE = os.getenv("TOKEN_TELE")

if not TOKEN_TELE:
    raise ValueError(
        "TOKEN_TELE não foi encontrado no arquivo .env"
    )


bot = telebot.TeleBot(TOKEN_TELE)


# Temporário.
# Futuramente ficará no Supabase.
usuarios = {}


# =========================
# START
# =========================

@bot.message_handler(commands=["start"])
def iniciar_live_route(mensagem):

    chat_id = mensagem.chat.id

    usuarios[chat_id] = {}

    teclado = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    for idioma in IDIOMAS.keys():
        teclado.add(
            types.KeyboardButton(idioma)
        )

    texto = (
        "🌎 LiveRoute\n\n"
        "Escolha seu idioma / Choose your language / "
        "Elige tu idioma:"
    )

    msg = bot.send_message(
        chat_id,
        texto,
        reply_markup=teclado
    )

    bot.register_next_step_handler(
        msg,
        receber_idioma
    )


# =========================
# IDIOMA
# =========================

def receber_idioma(mensagem):

    chat_id = mensagem.chat.id
    escolha = mensagem.text

    if escolha not in IDIOMAS:

        bot.send_message(
            chat_id,
            "⚠️ Escolha uma das opções disponíveis."
        )

        iniciar_live_route(mensagem)
        return

    idioma = IDIOMAS[escolha]

    usuarios[chat_id]["idioma"] = idioma

    texto = (
        TEXTOS[idioma]["boas_vindas"]
        + "\n\n"
        + TEXTOS[idioma]["perguntar_nome"]
    )

    msg = bot.send_message(
        chat_id,
        texto,
        reply_markup=types.ReplyKeyboardRemove()
    )

    bot.register_next_step_handler(
        msg,
        receber_nome
    )


# =========================
# NOME
# =========================

def receber_nome(mensagem):

    chat_id = mensagem.chat.id

    nome = mensagem.text.strip()

    usuarios[chat_id]["nome"] = nome

    mostrar_menu_principal(chat_id)


# =========================
# MENU PRINCIPAL
# =========================

def mostrar_menu_principal(chat_id):

    usuario = usuarios[chat_id]

    nome = usuario["nome"]
    idioma = usuario["idioma"]

    teclado = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    cultural = TEXTOS[idioma]["cultural"]
    gastronomico = TEXTOS[idioma]["gastronomico"]

    teclado.add(
        types.KeyboardButton(cultural),
        types.KeyboardButton(gastronomico)
    )

    texto = TEXTOS[idioma]["menu"].format(
        nome=nome
    )

    msg = bot.send_message(
        chat_id,
        texto,
        reply_markup=teclado
    )

    bot.register_next_step_handler(
        msg,
        receber_tipo_roteiro
    )


# =========================
# TIPO DE ROTEIRO
# =========================

def receber_tipo_roteiro(mensagem):

    chat_id = mensagem.chat.id

    usuario = usuarios[chat_id]

    idioma = usuario["idioma"]

    cultural = TEXTOS[idioma]["cultural"]
    gastronomico = TEXTOS[idioma]["gastronomico"]

    escolha = mensagem.text

    if escolha == cultural:

        usuario["tipo_roteiro"] = "cultural"

    elif escolha == gastronomico:

        usuario["tipo_roteiro"] = "gastronomico"

    else:

        bot.send_message(
            chat_id,
            "⚠️ Opção inválida."
        )

        mostrar_menu_principal(chat_id)
        return

    perguntar_tempo(chat_id)


# =========================
# TEMPO
# =========================

def perguntar_tempo(chat_id):

    usuario = usuarios[chat_id]

    idioma = usuario["idioma"]

    teclado = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    algumas_horas = TEXTOS[idioma]["algumas_horas"]
    um_dia = TEXTOS[idioma]["um_dia"]
    fim_semana = TEXTOS[idioma]["fim_semana"]

    teclado.add(
        types.KeyboardButton(algumas_horas)
    )

    teclado.add(
        types.KeyboardButton(um_dia),
        types.KeyboardButton(fim_semana)
    )

    msg = bot.send_message(
        chat_id,
        TEXTOS[idioma]["tempo"],
        reply_markup=teclado
    )

    bot.register_next_step_handler(
        msg,
        receber_tempo
    )


def receber_tempo(mensagem):

    chat_id = mensagem.chat.id

    usuario = usuarios[chat_id]

    idioma = usuario["idioma"]

    opcoes = {
        TEXTOS[idioma]["algumas_horas"]:
            "algumas_horas",

        TEXTOS[idioma]["um_dia"]:
            "um_dia",

        TEXTOS[idioma]["fim_semana"]:
            "fim_semana"
    }

    escolha = mensagem.text

    if escolha not in opcoes:

        bot.send_message(
            chat_id,
            "⚠️ Opção inválida."
        )

        perguntar_tempo(chat_id)
        return

    usuario["tempo"] = opcoes[escolha]

    if usuario["tipo_roteiro"] == "cultural":
        perguntar_companhia(chat_id)

    elif usuario["tipo_roteiro"] == "gastronomico":
        perguntar_refeicao(chat_id)

# =========================
# CULTURAL - COMPANHIA
# =========================

def perguntar_companhia(chat_id):

    usuario = usuarios[chat_id]
    idioma = usuario["idioma"]

    teclado = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    teclado.add(
        types.KeyboardButton(TEXTOS[idioma]["sozinho"]),
        types.KeyboardButton(TEXTOS[idioma]["casal"])
    )

    teclado.add(
        types.KeyboardButton(TEXTOS[idioma]["amigos"]),
        types.KeyboardButton(TEXTOS[idioma]["familia"])
    )

    teclado.add(
        types.KeyboardButton(TEXTOS[idioma]["criancas"])
    )

    msg = bot.send_message(
        chat_id,
        TEXTOS[idioma]["companhia"],
        reply_markup=teclado
    )

    bot.register_next_step_handler(
        msg,
        receber_companhia
    )


def receber_companhia(mensagem):

    chat_id = mensagem.chat.id
    usuario = usuarios[chat_id]
    idioma = usuario["idioma"]

    opcoes = {
        TEXTOS[idioma]["sozinho"]: "sozinho",
        TEXTOS[idioma]["casal"]: "casal",
        TEXTOS[idioma]["amigos"]: "amigos",
        TEXTOS[idioma]["familia"]: "familia",
        TEXTOS[idioma]["criancas"]: "criancas"
    }

    escolha = mensagem.text

    if escolha not in opcoes:

        perguntar_companhia(chat_id)
        return

    usuario["companhia"] = opcoes[escolha]

    perguntar_experiencia_cultural(chat_id)

# =========================
# CULTURAL - EXPERIÊNCIA
# =========================

def perguntar_experiencia_cultural(chat_id):

    usuario = usuarios[chat_id]
    idioma = usuario["idioma"]

    teclado = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    teclado.add(
        types.KeyboardButton(TEXTOS[idioma]["historia"])
    )

    teclado.add(
        types.KeyboardButton(TEXTOS[idioma]["museus"])
    )

    teclado.add(
        types.KeyboardButton(TEXTOS[idioma]["ar_livre"])
    )

    teclado.add(
        types.KeyboardButton(TEXTOS[idioma]["misturado"])
    )

    msg = bot.send_message(
        chat_id,
        TEXTOS[idioma]["ambiente_cultural"],
        reply_markup=teclado
    )

    bot.register_next_step_handler(
        msg,
        receber_experiencia_cultural
    )


def receber_experiencia_cultural(mensagem):

    chat_id = mensagem.chat.id
    usuario = usuarios[chat_id]
    idioma = usuario["idioma"]

    opcoes = {
        TEXTOS[idioma]["historia"]: "historia",
        TEXTOS[idioma]["museus"]: "museus",
        TEXTOS[idioma]["ar_livre"]: "ar_livre",
        TEXTOS[idioma]["misturado"]: "misturado"
    }

    escolha = mensagem.text

    if escolha not in opcoes:

        perguntar_experiencia_cultural(chat_id)
        return

    usuario["experiencia"] = opcoes[escolha]

    perguntar_preferencia(chat_id)

# =========================
# GASTRONÔMICO - REFEIÇÃO
# =========================

def perguntar_refeicao(chat_id):

    usuario = usuarios[chat_id]
    idioma = usuario["idioma"]

    teclado = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    teclado.add(
        types.KeyboardButton(TEXTOS[idioma]["cafe"]),
        types.KeyboardButton(TEXTOS[idioma]["almoco"])
    )

    teclado.add(
        types.KeyboardButton(TEXTOS[idioma]["jantar"])
    )

    teclado.add(
        types.KeyboardButton(TEXTOS[idioma]["comida_tipica"])
    )

    msg = bot.send_message(
        chat_id,
        TEXTOS[idioma]["refeicao"],
        reply_markup=teclado
    )

    bot.register_next_step_handler(
        msg,
        receber_refeicao
    )


def receber_refeicao(mensagem):

    chat_id = mensagem.chat.id
    usuario = usuarios[chat_id]
    idioma = usuario["idioma"]

    opcoes = {
        TEXTOS[idioma]["cafe"]: "cafe",
        TEXTOS[idioma]["almoco"]: "almoco",
        TEXTOS[idioma]["jantar"]: "jantar",
        TEXTOS[idioma]["comida_tipica"]: "comida_tipica"
    }

    escolha = mensagem.text

    if escolha not in opcoes:

        perguntar_refeicao(chat_id)
        return

    usuario["refeicao"] = opcoes[escolha]

    perguntar_experiencia_gastronomica(chat_id)

# =========================
# GASTRONÔMICO - EXPERIÊNCIA
# =========================

def perguntar_experiencia_gastronomica(chat_id):

    usuario = usuarios[chat_id]
    idioma = usuario["idioma"]

    teclado = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    teclado.add(
        types.KeyboardButton(TEXTOS[idioma]["regional"])
    )

    teclado.add(
        types.KeyboardButton(TEXTOS[idioma]["economico"])
    )

    teclado.add(
        types.KeyboardButton(TEXTOS[idioma]["vista"])
    )

    teclado.add(
        types.KeyboardButton(TEXTOS[idioma]["surpresa"])
    )

    msg = bot.send_message(
        chat_id,
        TEXTOS[idioma]["experiencia_gastro"],
        reply_markup=teclado
    )

    bot.register_next_step_handler(
        msg,
        receber_experiencia_gastronomica
    )


def receber_experiencia_gastronomica(mensagem):

    chat_id = mensagem.chat.id
    usuario = usuarios[chat_id]
    idioma = usuario["idioma"]

    opcoes = {
        TEXTOS[idioma]["regional"]: "regional",
        TEXTOS[idioma]["economico"]: "economico",
        TEXTOS[idioma]["vista"]: "vista",
        TEXTOS[idioma]["surpresa"]: "surpresa"
    }

    escolha = mensagem.text

    if escolha not in opcoes:

        perguntar_experiencia_gastronomica(chat_id)
        return

    usuario["experiencia"] = opcoes[escolha]

    perguntar_preferencia(chat_id)

# =========================
# PREFERÊNCIAS
# =========================

def perguntar_preferencia(chat_id):

    usuario = usuarios[chat_id]
    idioma = usuario["idioma"]

    teclado = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    teclado.add(
        types.KeyboardButton(
            TEXTOS[idioma]["evitar_cheio"]
        )
    )

    teclado.add(
        types.KeyboardButton(
            TEXTOS[idioma]["facil_acesso"]
        )
    )

    teclado.add(
        types.KeyboardButton(
            TEXTOS[idioma]["preferir_ar_livre"]
        )
    )

    teclado.add(
        types.KeyboardButton(
            TEXTOS[idioma]["sem_restricao"]
        )
    )

    msg = bot.send_message(
        chat_id,
        TEXTOS[idioma]["preferencia"],
        reply_markup=teclado
    )

    bot.register_next_step_handler(
        msg,
        receber_preferencia
    )


def receber_preferencia(mensagem):

    chat_id = mensagem.chat.id
    usuario = usuarios[chat_id]
    idioma = usuario["idioma"]

    opcoes = {
        TEXTOS[idioma]["evitar_cheio"]:
            "evitar_cheio",

        TEXTOS[idioma]["facil_acesso"]:
            "facil_acesso",

        TEXTOS[idioma]["preferir_ar_livre"]:
            "ar_livre",

        TEXTOS[idioma]["sem_restricao"]:
            "nenhuma"
    }

    escolha = mensagem.text

    if escolha not in opcoes:

        perguntar_preferencia(chat_id)
        return

    usuario["preferencia"] = opcoes[escolha]

    mostrar_recomendacoes(chat_id)


# =========================
# APENAS PARA TESTARMOS
# =========================

def mostrar_recomendacoes(chat_id):

    usuario = usuarios[chat_id]

    idioma = usuario["idioma"]

    resultado = recomendar_lugares(
        usuario
    )

    lugares = resultado["lugares"]
    tempo_usado = resultado["tempo_usado"]
    tempo_disponivel = resultado["tempo_disponivel"]


    if not lugares:

        bot.send_message(
            chat_id,
            "😕 Não encontramos lugares para esse perfil."
        )

        return


    if idioma == "pt":

        texto = (
            f"🌴 {usuario['nome']}, preparei um roteiro "
            "para você!\n\n"
        )

    elif idioma == "en":

        texto = (
            f"🌴 {usuario['nome']}, I've prepared a route "
            "for you!\n\n"
        )

    else:

        texto = (
            f"🌴 {usuario['nome']}, preparé una ruta "
            "para ti!\n\n"
        )


    for numero, item in enumerate(
    lugares,
    start=1
    ):

        lugar = item["lugar"]
        pontos = item["pontos"]

        nome = lugar["nome"][idioma]

        duracao = lugar["duracao_minutos"]

        texto += (
            f"{numero}️⃣ {nome}\n"
            f"⏱ {duracao} min\n"
            f"🧠 Compatibilidade: {pontos} pontos\n"
        )


        if "distancia_anterior" in item:

            distancia = item["distancia_anterior"]

            texto += (
                f"📍 {distancia:.1f} km "
                "do ponto anterior\n"
            )


        texto += "\n"

        lugar = item["lugar"]
        pontos = item["pontos"]

        nome = lugar["nome"][idioma]

        duracao = lugar["duracao_minutos"]

        texto += (
            f"{numero}️⃣ {nome}\n"
            f"⏱ {duracao} min\n"
            f"🧠 Compatibilidade: {pontos} pontos\n\n"
        )


    horas_usadas = tempo_usado // 60
    minutos_usados = tempo_usado % 60


    texto += (
        "━━━━━━━━━━━━━━\n"
        f"⏱ Tempo estimado: "
        f"{horas_usadas}h {minutos_usados}min\n"
    )

    link_mapa = criar_link_mapa(
    lugares
    )


    teclado = types.InlineKeyboardMarkup()


    if link_mapa:

        botao_mapa = types.InlineKeyboardButton(
            "🗺 Abrir roteiro no mapa",
            url=link_mapa
        )

        teclado.add(
            botao_mapa
        )

    bot.send_message(
        chat_id,
        texto,
        reply_markup=teclado
    )

def criar_link_mapa(lugares):

    if not lugares:
        return None


    coordenadas = []

    for item in lugares:

        lugar = item["lugar"]

        coordenada = (
            f"{lugar['latitude']},"
            f"{lugar['longitude']}"
        )

        coordenadas.append(
            coordenada
        )


    if len(coordenadas) == 1:

        return (
            "https://www.google.com/maps/search/"
            f"?api=1&query={coordenadas[0]}"
        )


    origem = coordenadas[0]

    destino = coordenadas[-1]

    intermediarios = coordenadas[1:-1]


    link = (
        "https://www.google.com/maps/dir/"
        f"?api=1"
        f"&origin={origem}"
        f"&destination={destino}"
    )


    if intermediarios:

        waypoints = "|".join(
            intermediarios
        )

        link += (
            f"&waypoints={waypoints}"
        )


    return link

print("🌴 LiveRoute está rodando...")

bot.infinity_polling()