import random

def criar_calendario(equipes_apuradas):
    calendario = {} # calendario vazio
    estadios = ["municipal de coimbra", "municipal de braga", "municipa de leiria", "nacional", "estadio do alarve", "estadio da luz", 'estadio jose alvalade', "estadio do dragao"]
    eliminatorias = [["oitavas", "16-08-2023", 8], ["quartas", "23-08-2023", 4], ["semi-final","29-08-2023", 2], ["final", "31-08-2023", 1]]
    random.shuffle(equipes_apuradas)# Embaralhar a lista de equipes apuradas aleatoriamente

    eq_atual = 0 # Índice para acompanhar a equipe atual na lista de equipes apuradas

    #para cada eliminatoria
    for el in eliminatorias:
        #para cada jogo da eliminatoria
        for j in range(el[2]):
            chaveTuplo = (el[0], el[1], j + 1 )  
            if eq_atual < len(equipes_apuradas):     
                equipe_casa = equipes_apuradas[eq_atual]
                equipe_fora = equipes_apuradas[eq_atual + 1]
                calendario[chaveTuplo] = ["17:00", estadios[j],equipe_casa,equipe_fora,0,0]
                eq_atual += 2
            else:
                break 
    return calendario

def apurar_equipes():
    equipes_apuradas = [] # lista vazia
    dados = [] #lista vazia
    equipas_ranking = [] # lista vazia
    #procedimento para apurar equipes
    try:
        dados = open("equipas.csv", "r",encoding="utf-8" )
    except:
        exit()

    #obter cada campo atraves do separador de linhas
    for d in dados:
        campos = list(d.strip().split(","))
        if len(campos) >= 3:
            equipas_ranking.append(campos)

    # de acordo com a estrutura do ficheiro equipas, o ranking encontr-se na ultima posiçao dos quatro campos, começando na posiçao 0, ocupa a posiçao 3.
    #lista fica ordenada pelo ranking
    equipas_ranking.sort(key = lambda i : int(i[2]))
    for eq in equipas_ranking:
        tam = len(equipes_apuradas)
        #limitar a 16 equipes
        if (tam == 16):
            break
    #adicionar a lista de equipas apuradas as 12 primeiras do ranking e quatro com ranking superior a 20
        if tam < 12:
            equipes_apuradas.append(eq)
        elif (tam > 11 and tam < 16):
            if (int(eq[2]) >= 20):
                equipes_apuradas.append(eq)
    return equipes_apuradas

def imprimir_calendario(calendario):
    eq_vencedoras = [] #lista vazia
    for chave, jogo in calendario.items():
        eliminatoria, data, num_jogo = chave
        hora, estadio, equipe_casa, equipe_fora, _, _ = jogo
        print(f"{eliminatoria} - {data} - {hora}: {equipe_casa} vs {equipe_fora} - estadio: {estadio}")
        gols_casa = obterGols()
        gols_fora = obterGols()
        print(f"resultados: {equipe_casa} {gols_casa} vs {gols_fora} {equipe_fora}")
        if gols_casa > gols_fora:
            print("Equipe da casa ganhou!")
            eq_vencedoras.append(equipe_casa)
        elif gols_fora > gols_casa:
            print("Equipe de fora ganhou!")
            eq_vencedoras.append(equipe_fora)
        else:
            #decisao de penaltis 5 cobranças
            print("Empate!")
            p_casa = penalti()
            p_fora = penalti()
            if p_casa > p_fora:
                print(f"Equipe casa ganhou! por {p_casa} vs {p_fora} nos penaltis")
                eq_vencedoras.append(equipe_casa)
            elif p_fora > p_casa:
                print(f"Equipe fora ganhou! por {p_fora} vs {p_casa} nos penaltis")
                eq_vencedoras.append(equipe_fora)
            else:
                print("Empate nos penaltis!")
                #dicisao de penaltis 1 cobrança
                while p_casa == p_fora:
                    p_casa = random.randint(0,1)
                    p_fora = random.randint(0,1)
                    if p_casa > p_fora:
                        print(f"Equipe casa ganhou! por {p_casa} vs {p_fora} nos penaltis")
                        eq_vencedoras.append(equipe_casa)
                    else:
                        print(f"Equipe fora ganhou! por {p_fora} vs {p_casa} nos penaltis")
                        eq_vencedoras.append(equipe_fora)        
        print()
    return eq_vencedoras

#funçao para gerar gols e atribuir a cada equipe a cada jogo
def obterGols():
    #gerar aleatoriamente o numero de gols
    gols = random.randint(0, 9)
    return gols

def penalti():
    gols = random.randint(0, 5)
    return gols

def proximaFase(vencedores):
    for team in vencedores:
        print(team)
    if len(vencedores) > 1:
        novo_calendario = criar_calendario(vencedores)
        imprimir_calendario(novo_calendario)
    else:
        print("Fim do torneio")

#chamar procedimento apurar_equipes
equipes_apuradas = apurar_equipes()
#chamar procedimento criar_calendario
calendario = criar_calendario(equipes_apuradas)

#imprimir calendario
vencedores = imprimir_calendario(calendario)
proximaFase(vencedores)
