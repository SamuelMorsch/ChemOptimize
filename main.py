import random
import math
import matplotlib.pyplot as plt

# --- 1. CONFIGURAÇÕES DO LOTE (ENTRADAS) ---
VOLUME_TOTAL_L = 500  # Volume a ser envasado em Litros
DENSIDADE = 1.2       # Exemplo de densidade do líquido
MASSA_TOTAL_KG = VOLUME_TOTAL_L * DENSIDADE

# Catálogo de frascos disponíveis: (capacidade em L, custo financeiro)
FRASCOS = [
    {"nome": "Tanque 100L", "capacidade": 100, "custo": 50.0},
    {"nome": "Tambor 50L", "capacidade": 50, "custo": 30.0},
    {"nome": "Bombona 20L", "capacidade": 20, "custo": 15.0}
]

# --- 2. FUNÇÃO DE CUSTO (O OBJETIVO DO AGENTE) ---
def calcular_custo(estado):
    """
    estado: lista com a quantidade de cada frasco, ex: [4, 2, 0]
    Retorna o 'custo' daquela configuração. Quanto menor, melhor.
    """
    volume_alocado = sum(estado[i] * FRASCOS[i]["capacidade"] for i in range(len(estado)))
    custo_financeiro = sum(estado[i] * FRASCOS[i]["custo"] for i in range(len(estado)))
    
    # Penalidade severa se faltar espaço (o líquido vaza)
    if volume_alocado < VOLUME_TOTAL_L:
        return float('inf')
    
    # Penalidade por espaço ocioso (desperdício)
    espaco_vazio = volume_alocado - VOLUME_TOTAL_L
    penalidade_vazio = espaco_vazio * 2.0  # Peso do desperdício
    
    return custo_financeiro + penalidade_vazio

# --- 3. HEURÍSTICA: SIMULATED ANNEALING ---
def otimizar_envase():
    # Estado inicial aleatório ou básico (ex: tenta colocar tudo no menor frasco)
    estado_atual = [0, 0, math.ceil(VOLUME_TOTAL_L / FRASCOS[2]["capacidade"])]
    custo_atual = calcular_custo(estado_atual)
    
    melhor_estado = estado_atual[:]
    melhor_custo = custo_atual
    
    # Parâmetros da Têmpera Simulada
    temperatura = 1000.0
    taxa_resfriamento = 0.95
    iteracoes = 500
    historico_custos = []
    
    for _ in range(iteracoes):
        historico_custos.append(melhor_custo if melhor_custo != float('inf') else 1000)
        
        # Gera um estado vizinho (altera a quantidade de algum frasco aleatoriamente)
        vizinho = estado_atual[:]
        idx = random.randint(0, len(FRASCOS) - 1)
        vizinho[idx] += random.choice([-1, 1])
        if vizinho[idx] < 0:
            vizinho[idx] = 0
            
        custo_vizinho = calcular_custo(vizinho)
        
        # Diferença de custo
        delta_e = custo_vizinho - custo_atual
        
        # Critério de aceitação: aceita se for melhor, ou se a probabilidade da temperatura permitir
        if delta_e < 0 or random.random() < math.exp(-delta_e / temperatura):
            estado_atual = vizinho
            custo_atual = custo_vizinho
            
            # Atualiza o melhor global
            if custo_atual < melhor_custo:
                melhor_estado = estado_atual[:]
                melhor_custo = custo_atual
                
        # Resfria o sistema
        temperatura *= taxa_resfriamento
        if temperatura < 0.1:
            break
            
    return melhor_estado, melhor_custo, historico_custos

# --- 4. EXECUÇÃO E DEMONSTRAÇÃO ---
if __name__ == "__main__":
    print("Iniciando Agente ChemOptima...\n")
    melhor_estado, melhor_custo, historico = otimizar_envase()
    
    print("=== RELATÓRIO DE ENVASE OTIMIZADO ===")
    print(f"Lote Total: {VOLUME_TOTAL_L} Litros (Massa: {MASSA_TOTAL_KG} kg)")
    print("Distribuição Ideal:")
    for i, qtd in enumerate(melhor_estado):
        print(f" -> {qtd}x {FRASCOS[i]['nome']}")
        
    volume_final = sum(melhor_estado[i] * FRASCOS[i]["capacidade"] for i in range(len(melhor_estado)))
    aproveitamento = (VOLUME_TOTAL_L / volume_final) * 100 if volume_final > 0 else 0
    
    print(f"\nEspaço Total Alocado: {volume_final} Litros")
    print(f"Aproveitamento: {aproveitamento:.1f}%")
    print(f"Pontuação de Custo Final: {melhor_custo:.2f}")
    
    # Plotagem do gráfico de convergência
    plt.plot(historico, color='blue')
    plt.title("Aprendizado do Agente - Simulated Annealing")
    plt.xlabel("Iterações")
    plt.ylabel("Custo (Penalidades + Financeiro)")
    plt.grid(True)
    plt.show()