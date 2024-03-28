# Importações
import random
import math

# Parâmetros
TAXA_DE_SELECAO = 0.15
TAXA_DE_CROSSOVER = 0.07
NUMERO_DE_INDIVIDUOS = 750
NUMERO_DE_ITERACOES = 10000000
ITERACOES_PARA_TRAGEDIA = 1000

# Dados
analises = {
    'Análise 1': ['Espectrofotômetro UV-VIS', 'Cromatógrafo Gasoso'],
    'Análise 2': ['Cromatógrafo Líquido', 'Espectrômetro Infravermelho'],
    'Análise 3': ['Microscópio', 'Balança Analítica'],
    'Análise 4': ['Espectrômetro de Massa'],
    'Análise 5': ['Agitador Magnético', 'Espectrômetro Infravermelho'],
    'Análise 6': ['Cromatógrafo Líquido', 'Espectrofotômetro UV-VIS'],
    'Análise 7': ['Espectrofotômetro UV-VIS', 'Microscópio'],
    'Análise 8': ['Cromatógrafo Gasoso'],
    'Análise 9': ['Espectrômetro Infravermelho', 'Balança Analítica'],
    'Análise 10': ['Espectrômetro de Massa', 'Cromatógrafo Gasoso']
}

restricoes = {
    'Balança Analítica': 6,
    'Agitador Magnético': 4,
    'Cromatógrafo Líquido': 8,
    'Cromatógrafo Gasoso': 6,
    'Espectrofotômetro UV-VIS': 4,
    'Espectrômetro Infravermelho': 6,
    'Espectrômetro de Massa': 4,
    'Microscópio': 6
}

dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
horarios = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

# Funções
def gerar_individuo():
  cronograma = {equipamento: [] for equipamento in restricoes}
  for analise, equipamentos_necessarios in analises.items():
      for equipamento in equipamentos_necessarios:
          if len(cronograma[equipamento]) < restricoes[equipamento]:
              dia = random.choice(dias)
              horario = random.choice(horarios)
              cronograma[equipamento].append((dia, horario, analise))
  return cronograma

def calcular_fitness(cronograma):
  dias_da_semana = {'Segunda': 0, 'Terça': 1, 'Quarta': 2, 'Quinta': 3, 'Sexta': 4}
  tempo_total = 0
  num_analises_mesmo_dia = 0

  for equipamento, agendamentos in cronograma.items():
      dias = set()
      for agendamento in agendamentos:
          dia, horario, _ = agendamento
          tempo_total += dias_da_semana[dia] * 24 + horario - 8  # Somatória de todos os tempos
          if dia in dias:
            num_analises_mesmo_dia += 1
          dias.add(dia)

  return tempo_total + num_analises_mesmo_dia * 10  # Penaliza análises no mesmo dia

def mutacao(individuo, taxa_mutacao):
  novo_individuo = individuo.copy()

  for equipamento, agendamentos in novo_individuo.items():
    novo_agendamento = []
    for agendamento in agendamentos:
        if random.random() < taxa_mutacao:
            # Mutação: alterar apenas a data e/ou a hora aleatoriamente
            nova_data = random.choice(dias)
            novo_horario = random.choice(horarios)
            novo_agendamento.append((nova_data, novo_horario, agendamento[2]))
  if (checar_validade(novo_individuo) and calcular_fitness(novo_individuo) < calcular_fitness(individuo)):
    return novo_individuo
  else:
    return individuo

def crossover(individuo1, individuo2):
  novo_individuo = individuo1.copy()

  for equipamento, agendamentos in novo_individuo.items():
      if random.random() < TAXA_DE_CROSSOVER:
        novo_individuo[equipamento] = individuo2[equipamento].copy()
  if (checar_validade(novo_individuo) and calcular_fitness(novo_individuo) < calcular_fitness(individuo1)):
    return novo_individuo
  else:
    return individuo1

def selecionar_melhores(populacao, n):
  # Ordenar a população pelos valores de fitness de cada indivíduo
  populacao_ordenada = sorted(populacao, key=calcular_fitness)
  # Selecionar os n primeiros indivíduos da lista ordenada (os 1000 menores fitness)
  melhores = populacao_ordenada[:n]
  return melhores

def checar_validade(individuo):
    # Verifica se cada equipamento não é usado mais do que sua capacidade máxima por dia
    for equipamento, agendamentos in individuo.items():
        dias_uso = {}
        for agendamento in agendamentos:
            dia, _, analise = agendamento
            if dia not in dias_uso:
                dias_uso[dia] = set()
            dias_uso[dia].add(analise)
        for dia, analises in dias_uso.items():
            if len(analises) > restricoes[equipamento]:
                return False

    # Verifica se uma análise não está em 2 equipamentos ao mesmo tempo
    horarios_analises = {}
    for equipamento, agendamentos in individuo.items():
        for agendamento in agendamentos:
            dia, horario, analise = agendamento
            if (dia, horario) not in horarios_analises:
                horarios_analises[(dia, horario)] = set()
            horarios_analises[(dia, horario)].add(analise)
    for (dia, horario), analises in horarios_analises.items():
        if len(analises) > 1:
            return False

    return True

def gerar_populacao_inicial(tamanho_populacao):
  return [gerar_individuo() for _ in range(tamanho_populacao)]

# Algoritmo genético
populacao_atual = gerar_populacao_inicial(NUMERO_DE_INDIVIDUOS)
menor_fitness = math.inf
for i in range(NUMERO_DE_ITERACOES):
  populacao_atual = [mutacao(individuo, TAXA_DE_SELECAO) for individuo in populacao_atual]
  populacao_atual = [crossover(populacao_atual[i], populacao_atual[(i+1)%len(populacao_atual)]) for i in range(len(populacao_atual))]

  # Aplica a seleção por tragédia após 2000 iterações
  if i % ITERACOES_PARA_TRAGEDIA == 0 and i > 0:
    populacao_atual = selecionar_melhores(populacao_atual, NUMERO_DE_INDIVIDUOS // 5)  # Mantém apenas os 5% melhores
    # Regenera a população para manter o número de indivíduos constante
    populacao_atual += gerar_populacao_inicial(NUMERO_DE_INDIVIDUOS - len(populacao_atual))
    print(f"== SELEÇÃO POR TRAGÉDIA {i} ==")

  populacao_atual = selecionar_melhores(populacao_atual, NUMERO_DE_INDIVIDUOS)

  melhor_individuo = populacao_atual[0]
  if (calcular_fitness(melhor_individuo) < menor_fitness):
    menor_fitness = calcular_fitness(melhor_individuo)
    print(f"Melhor fitness: {menor_fitness} - Qtd. Iterações: {i} - Tempo médio: {menor_fitness/18:.2f}")
    print(melhor_individuo)

  if (calcular_fitness(melhor_individuo) <= 16):
    print(f"== ENCONTRADO! em {i} iterações com fitness de {menor_fitness} ==")
    print(melhor_individuo)
    break;