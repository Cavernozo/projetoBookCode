import random
import pandas as pd

def apurar_equipes():
    equipes_apuradas = [] #lista vazia
    dados = [] #lista vazia
    equipes_ranking = [] #lista vazia
    #procedimento para apurar equipes
    try:
        dados = open("equipas.csv", "r", encoding="utf-8")
    except:
        exit()

    #obter cada campo atraves do separador de linhas
    for d in dados:
        campos = list(d.strip().split(","))
        if len(campos) >= 3:
            equipes_ranking.append(campos)


    # de acordo com a estrutura do ficheiro equipas, o ranking encontr-se na ultima posiçao dos quatro campos, começando na posiçao 0, ocupa a posiçao 3.
    #lista fica ordenada pelo ranking
    equipes_ranking.sort(key= lambda i : int(i[2]))
    for eq in equipes_ranking:
        tam = len(equipes_apuradas)
        #limitar tam 16
        if (tam == 16):
            break
        #adicionar a lista de equipas apuradas as 12 primeiras do ranking e quatro com ranking superior a 20
        if (tam < 12):
            equipes_apuradas.append(eq)
        elif (tam > 11 and tam < 16):
            if (int(eq[2]) > 20):
                equipes_apuradas.append(eq)
    return equipes_apuradas    

#criando calendario
def criar_calenario(equipes_apuradas):
    calendario = []#lista vazia
    estadios = ["municipal de coimbra", "municipal de braga", "municipa de leiria", "nacional", "estadio do alarve", "estadio da luz", 'estadio jose alvalade', "estadio do dragao"]
    eliminatoria = fase_eliminatoria(equipes_apuradas)
    random.shuffle(equipes_apuradas)#embaralhar equipes

    eq_atual = 0#indece atual para acompanhar equipes na lista de apurados

    #para cada jogo em eliminatoria
    for jogo in range(eliminatoria[2]):
        chaveTuplo = (eliminatoria[0], eliminatoria[1],jogo)
        if eq_atual < len(equipes_apuradas):
            eq_casa = equipes_apuradas[eq_atual]
            eq_fora = equipes_apuradas[eq_atual + 1]
            chaveTuplo = [eliminatoria[0], "17:00", eliminatoria[1],estadios[jogo], eq_casa,eq_fora]
            calendario.append(chaveTuplo)
            eq_atual += 2
        else:
            break
    return calendario
    


#selecionando eliminatoria
def fase_eliminatoria(equipes):
    #acesso a variavel global
    global indeice_eliminatoria

    eliminatorias = [["oitavas", "16-08-2023", 8], ["quartas", "23-08-2023", 4], ["semi-final","29-08-2023", 2], ["final", "31-08-2023", 1]]
    #verificando se o indice atual esta dentro dos limites da lista eliminatoria
    if indeice_eliminatoria < len(eliminatorias):
        eliminatoria = eliminatorias[indeice_eliminatoria]
        indeice_eliminatoria += 1
        return eliminatoria
    else:
        exit()

#definindo vencedores
def vencedores(calendario):
    eq_vencedores = [] # lista vazia
    for chave in calendario:
        eliminatoria, hora, data,estadio, eq_casa, eq_fora,  = chave
        #obtendo gols equipes casa e fora
        gols_casa = obter_Gols()
        gols_fora = obter_Gols()
        print(f"{'-=' * 20} Resultados {'-=' * 20}")
        print(f"{eliminatoria} - {hora} - {data} - {eq_casa[0]} {gols_casa} vc {gols_fora} {eq_fora[0]} - estadio: {estadio}")
        if gols_casa > gols_fora:
            print(f"Equipe {eq_casa[0]} venceu!")
            print()
            eq_vencedores.append(eq_casa)
        elif gols_fora > gols_casa:
            print(f"Equipe {eq_fora[0]} venceu!")
            print()
            eq_vencedores.append(eq_fora)
        else:
            #dicisao de penaltis
            print("Empate!")
            p_casa = penalti()
            p_fora = penalti()
            if p_casa > p_fora:
                print(f"Equipe {eq_casa[0]} ganhou na decisao de penaltis por {p_casa} vs {p_fora}")
                print()
                eq_vencedores.append(eq_casa)
            elif p_fora > p_casa:
                print(f"Equipe {eq_fora[0]} ganhou na decisao de penaltis por {p_fora} vs {p_casa}")
                print()
                eq_vencedores.append(eq_fora)
            else:
                #decisao de penaltis com 1 cobrança
                while p_casa == p_fora:
                    p_casa = random.randint(0, 1)
                    p_fora = random.randint(0, 1)
                    if p_casa > p_fora:
                        print(f"Equipe {eq_casa[0]} ganhou na decisao de penaltis por {p_casa} vs {p_fora}")
                        print()
                        eq_vencedores.append(eq_casa)
                    else:
                        print(f"Equipe {eq_fora[0]} ganhou na decisao de penaltis por {p_fora} vs {p_casa}")
                        print()
                        eq_vencedores.append(eq_fora)
    return eq_vencedores    

#funçao para criar gols
def obter_Gols():
    gols = random.randint(0,9)
    return gols

#funçao para criar penaltis
def penalti():
    gols = random.randint(0, 5)
    return gols

#funçao para criar uma nova fase
def proxima_fase(nfase):
    print("Classificados para nova fase!")
    for team in nfase:
        print(team[0])
        print()
    
    #verificando se a mais de uma equipe na proxima fase
    if len(nfase) >= 2:

        n_calendario = criar_calenario(nfase)

        print(f"{'-=' * 23} Calendario de jogos {'-=' * 23}")
        print(pd.DataFrame(n_calendario, columns = ['Fase', 'Hora', 'Data', 'Esatdio', 'Equipe casa', 'Equipe fora']))
        print()

    #chamando a funçao de determinar vencedores para a proxima fase
        vencedores_n_fase = vencedores(n_calendario)
        if len(vencedores_n_fase) >= 2:
            #chamando recursivamentea funçao para a proxima fase
            proxima_fase(vencedores_n_fase)
        else:
            print(f"{vencedores_n_fase[0][0]} é campeão da copa do mundo!!!")

#variavel global para o indice da eliminatoria
indeice_eliminatoria = 0 
def main():
    #chamar procedimento apurar equipes
    equipes_apuradas = apurar_equipes()
    print(f"{'-=' * 10} Eequipes apuradas para a Copa do Mundo {'-=' * 10}")
    print(pd.DataFrame(equipes_apuradas, columns = ['Pais', 'Regiao', 'Ranking']))
    print()
    
    calendario = criar_calenario(equipes_apuradas)
    print(f"{'-=' * 23} Calendario de jogos {'-=' * 23}")
    print(pd.DataFrame(calendario, columns = ['Fase', 'Hora', 'Data', 'Esatdio', 'Equipe casa', 'Equipe fora']))
    print()
        
        #chamar procedimento vencedores
    nFase = vencedores(calendario)
    if len(nFase) >= 2:
        proxima_fase(nFase)
    
if __name__ == "__main__":
    main()