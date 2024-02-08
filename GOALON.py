#procedimento para apuramento das equipes 
def apura_equipes():
    equipas_apuradas = [] #lista vazia
    dados = [] # lista vazia
    equipas_ranking = [] # lista vazia

#abertura do ficheiro equipas.csv e carregamento da lista equipas_ranking
    try:
        dados = open("equipas.csv", "r", encoding= "utf-8")
    except:
        exit()
    #obter cada campo através do separador de virgula
    for d in dados:
        campos = list(d.strip().split(","))
        if len(campos) >= 3:
            equipas_ranking.append(campos)
    #de acordo com a estrutura do ficheiro equipas, o ranking encontrase na ultima posição dos 3 campos, começando na posição 0, ocupa a posição 2.
    #lista fica ordenada pelo ranking
        equipas_ranking.sort(key = lambda i: int(i[2]))
        for eq in equipas_ranking:
            tam = len(equipas_apuradas)
            #limitar a 16 equipas
            if (tam == 16):
                break
        #print(eq)
    #adicionar a lista de equipas apuradas as 12 primeiras do ranking e quatro com ranking superior 20
        if tam < 12:
            equipas_apuradas.append(eq)
        elif (tam > 11 and tam < 16):
            #print(eq[2])
            if(int(eq[2]) >= 20):
                equipas_apuradas.append(eq)

    return equipas_apuradas


#programa principal
#chamar procedimento apura_equipas
equipas_apuradas = apura_equipes()
#escrever as equipes e o total de equipes seleciondas
print(equipas_apuradas)
print()
print(len(equipas_apuradas))