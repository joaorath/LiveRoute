import math


def calcular_distancia(lat1, lon1, lat2, lon2):
    """
    Calcula a distância aproximada entre dois pontos
    da Terra utilizando a fórmula de Haversine.

    Retorna a distância em quilômetros.
    """

    raio_terra = 6371

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    diferenca_lat = lat2 - lat1
    diferenca_lon = lon2 - lon1

    a = (
        math.sin(diferenca_lat / 2) ** 2
        +
        math.cos(lat1)
        * math.cos(lat2)
        * math.sin(diferenca_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    distancia = raio_terra * c

    return distancia

def ordenar_por_proximidade(resultados):

    if len(resultados) <= 1:
        return resultados


    # O primeiro lugar continua sendo o que teve
    # maior compatibilidade com o usuário.

    primeiro = resultados[0]

    roteiro_ordenado = [primeiro]

    restantes = resultados[1:]


    while restantes:

        lugar_atual = roteiro_ordenado[-1]["lugar"]

        latitude_atual = lugar_atual["latitude"]
        longitude_atual = lugar_atual["longitude"]


        mais_proximo = None
        menor_distancia = float("inf")


        for candidato in restantes:

            lugar = candidato["lugar"]

            distancia = calcular_distancia(
                latitude_atual,
                longitude_atual,
                lugar["latitude"],
                lugar["longitude"]
            )


            if distancia < menor_distancia:

                menor_distancia = distancia

                mais_proximo = candidato


        mais_proximo["distancia_anterior"] = menor_distancia

        roteiro_ordenado.append(
            mais_proximo
        )

        restantes.remove(
            mais_proximo
        )


    return roteiro_ordenado