from places import LUGARES
from geo import ordenar_por_proximidade


def calcular_pontuacao(lugar, usuario):

    pontos = 0

    tipo_roteiro = usuario["tipo_roteiro"]

    # =========================
    # FILTRO PRINCIPAL
    # =========================

    if tipo_roteiro not in lugar["categorias"]:
        return -1


    # =========================
    # CULTURAL
    # =========================

    if tipo_roteiro == "cultural":

        experiencia = usuario.get("experiencia")
        companhia = usuario.get("companhia")

        if experiencia == "misturado":
            pontos += 1

        elif experiencia in lugar["experiencias"]:
            pontos += 3

        if companhia in lugar["companhias"]:
            pontos += 2


    # =========================
    # GASTRONÔMICO
    # =========================

    elif tipo_roteiro == "gastronomico":

        refeicao = usuario.get("refeicao")
        experiencia = usuario.get("experiencia")

        if refeicao in lugar["refeicoes"]:
            pontos += 3

        if experiencia == "surpresa":
            pontos += 1

        elif experiencia in lugar["experiencias"]:
            pontos += 3

        elif experiencia in lugar["caracteristicas"]:
            pontos += 3


    # =========================
    # PREFERÊNCIA GERAL
    # =========================

    preferencia = usuario.get("preferencia")

    if preferencia == "nenhuma":
        pontos += 1

    elif preferencia in lugar["caracteristicas"]:
        pontos += 2


    return pontos


from places import LUGARES


def calcular_pontuacao(lugar, usuario):

    pontos = 0

    tipo_roteiro = usuario["tipo_roteiro"]

    # =========================
    # FILTRO PRINCIPAL
    # =========================

    if tipo_roteiro not in lugar["categorias"]:
        return -1


    # =========================
    # CULTURAL
    # =========================

    if tipo_roteiro == "cultural":

        experiencia = usuario.get("experiencia")
        companhia = usuario.get("companhia")

        if experiencia == "misturado":
            pontos += 1

        elif experiencia in lugar["experiencias"]:
            pontos += 3

        if companhia in lugar["companhias"]:
            pontos += 2


    # =========================
    # GASTRONÔMICO
    # =========================

    elif tipo_roteiro == "gastronomico":

        refeicao = usuario.get("refeicao")
        experiencia = usuario.get("experiencia")

        if refeicao in lugar["refeicoes"]:
            pontos += 3

        if experiencia == "surpresa":
            pontos += 1

        elif experiencia in lugar["experiencias"]:
            pontos += 3

        elif experiencia in lugar["caracteristicas"]:
            pontos += 3


    # =========================
    # PREFERÊNCIA GERAL
    # =========================

    preferencia = usuario.get("preferencia")

    if preferencia == "nenhuma":
        pontos += 1

    elif preferencia in lugar["caracteristicas"]:
        pontos += 2


    return pontos


def obter_tempo_disponivel(usuario):

    tempos = {
        "algumas_horas": 240,
        "um_dia": 480,
        "fim_semana": 960
    }

    return tempos.get(
        usuario.get("tempo"),
        240
    )


def recomendar_lugares(usuario):

    TEMPO_DESLOCAMENTO = 20

    resultados = []

    for lugar in LUGARES:

        pontos = calcular_pontuacao(
            lugar,
            usuario
        )

        if pontos >= 0:

            resultados.append({
                "lugar": lugar,
                "pontos": pontos
            })


    # Primeiro os lugares com maior compatibilidade
    resultados.sort(
        key=lambda item: item["pontos"],
        reverse=True
    )


    tempo_disponivel = obter_tempo_disponivel(
        usuario
    )

    roteiro = []

    tempo_usado = 0


    for resultado in resultados:

        lugar = resultado["lugar"]

        duracao = lugar["duracao_minutos"]


        tempo_extra = duracao

    if roteiro:
        tempo_extra += TEMPO_DESLOCAMENTO


    if tempo_usado + tempo_extra <= tempo_disponivel:

        roteiro.append(resultado)

        tempo_usado += tempo_extra

        roteiro = ordenar_por_proximidade(
        roteiro
        )
        
        return {
            "lugares": roteiro,
            "tempo_usado": tempo_usado,
            "tempo_disponivel": tempo_disponivel
        }