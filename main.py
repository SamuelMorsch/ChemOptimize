import random
import math
import matplotlib.pyplot as plt

# --- 1. CONFIGURAÇÕES DO LOTE (ENTRADAS) ---
VOLUME_TOTAL_L = 500  # Volume a ser envasado em Litros
DENSIDADE = 1.2       # Densidade do líquido (ex: 1.2 significa que 1L pesa 1.2kg)
MASSA_TOTAL_KG = VOLUME_TOTAL_L * DENSIDADE

# Catálogo de frascos atualizado (capacidade em L, custo em R$, peso_max suportado em kg)
FRASCOS = [
    {"nome": "IBC 1000L", "capacidade": 1000, "custo": 350.0, "peso_max": 1250.0},
    {"nome": "Tanque 200L", "capacidade": 200, "custo": 80.0, "peso_max": 240.0},
    {"nome": "Tanque 100L", "capacidade": 100, "custo": 50.0, "peso_max": 115.0},
    {"nome": "Tambor 50L", "capacidade": 50, "custo": 30.0, "peso_max": 65.0},
    {"nome": "Bombona 20L", "capacidade": 20, "custo": 15.0, "peso_max": 30.0},
    {"nome": "Galão 5L", "capacidade": 5, "custo": 6.0, "peso_max": 8.0}
]

# --- 2. FUNÇÃO DE CUSTO (O OBJETIVO DO AGENTE) ---
def calcular_custo(estado):
    """
    Avalia o custo financeiro e aplica penalidades matemáticas.
    """
    volume_alocado = sum(estado[i] * FRASCOS[i]["capacidade"] for i in range(len(estado)))
    custo_financeiro = sum(estado[i] * FRASCOS[i]["custo"] for i in range(len(estado)))
    
    # 1. Penalidade por falta de espaço (o líquido vaza)
    if volume_alocado < VOLUME_TOTAL_L:
        return float('inf')
    
    # 2. Penalidade por espaço ocioso (desperdício)
    espaco_vazio = volume_alocado - VOLUME_TOTAL_L
    penalidade_vazio = espaco_vazio * 2.0 
    
    # 3. Penalidade por restrição de peso (Densidade)
    penalidade_peso = 0
    for i in range(len(estado)):
        if estado[i] > 0:
            # O peso do líquido dentro do frasco
            peso_liquido_frasco = FRASCOS[i]["capacidade"] * DENSIDADE
            # Se o peso do líquido ultrapassar o que o frasco suporta, penaliza severamente
            if peso_liquido_frasco > FRASCOS[i]["peso_max"]:
                penalidade_peso += 1000 * estado[i]  # IA vai fugir dessa opção
    
    return custo_financeiro + penalidade_vazio + penalidade_peso

# --- 3. HEURÍSTICA: SIMULATED ANNEALING ---
def otimizar_envase():
    # Estado inicial dinâmico: preenche com zeros e tenta colocar tudo no menor frasco (último da lista)
    estado_atual = [0] * len(FRASCOS)
    estado_atual[-1] = math.ceil(VOLUME_TOTAL_L / FRASCOS[-1]["capacidade"])
    custo_atual = calcular_custo(estado_atual)
    
    melhor_estado = estado_atual[:]
    melhor_custo = custo_atual
    
    temperatura = 1000.0
    taxa_resfriamento = 0.95
    iteracoes = 500
    historico_custos = []
    
    for _ in range(iteracoes):
        historico_custos.append(melhor_custo if melhor_custo != float('inf') else 1000)
        
        # Gera estado vizinho
        vizinho = estado_atual[:]
        idx = random.randint(0, len(FRASCOS) - 1)
        vizinho[idx] += random.choice([-1, 1])
        if vizinho[idx] < 0:
            vizinho[idx] = 0
            
        custo_vizinho = calcular_custo(vizinho)
        delta_e = custo_vizinho - custo_atual
        
        # Critério de aceitação probabilística
        if delta_e < 0 or random.random() < math.exp(-delta_e / temperatura):
            estado_atual = vizinho
            custo_atual = custo_vizinho
            
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
    print(f"Lote Total: {VOLUME_TOTAL_L} Litros (Densidade: {DENSIDADE} | Massa: {MASSA_TOTAL_KG:.1f} kg)")
    print("-" * 40)
    print("Distribuição Ideal:")
    for i, qtd in enumerate(melhor_estado):
        if qtd > 0:
            peso_unitario = FRASCOS[i]["capacidade"] * DENSIDADE
            print(f" -> {qtd}x {FRASCOS[i]['nome']} (Peso unitário com líquido: {peso_unitario:.1f} kg)")
        
    volume_final = sum(melhor_estado[i] * FRASCOS[i]["capacidade"] for i in range(len(melhor_estado)))
    aproveitamento = (VOLUME_TOTAL_L / volume_final) * 100 if volume_final > 0 else 0
    
    print("-" * 40)
    print(f"Espaço Total Alocado: {volume_final} Litros")
    print(f"Aproveitamento: {aproveitamento:.1f}%")
    print(f"Pontuação de Custo Final: {melhor_custo:.2f}")
    
    plt.plot(historico, color='blue')
    plt.title("Aprendizado do Agente - Simulated Annealing")
    plt.xlabel("Iterações")
    plt.ylabel("Custo (Penalidades + Financeiro)")
    plt.grid(True)
    plt.show()