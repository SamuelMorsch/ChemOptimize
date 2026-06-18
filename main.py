import random
import math
import matplotlib.pyplot as plt

random.seed(42)

VOLUME_TOTAL_L = 500
DENSIDADE = 1.2

MASSA_TOTAL_KG = VOLUME_TOTAL_L * DENSIDADE

FRASCOS = [
    {"nome": "IBC 1000L",   "capacidade": 1000, "custo": 350.0, "peso_max": 1250.0},
    {"nome": "Tanque 200L", "capacidade": 200,  "custo": 80.0,  "peso_max": 240.0},
    {"nome": "Tanque 100L", "capacidade": 100,  "custo": 50.0,  "peso_max": 125.0},
    {"nome": "Tambor 50L",  "capacidade": 50,   "custo": 30.0,  "peso_max": 65.0},
    {"nome": "Bombona 20L", "capacidade": 20,   "custo": 15.0,  "peso_max": 30.0},
    {"nome": "Galão 5L",    "capacidade": 5,    "custo": 6.0,   "peso_max": 8.0}
]

def calcular_volume(estado):
    return sum(
        estado[i] * FRASCOS[i]["capacidade"]
        for i in range(len(FRASCOS))
    )

def calcular_custo_real(estado):
    return sum(
        estado[i] * FRASCOS[i]["custo"]
        for i in range(len(FRASCOS))
    )

# ==========================
# FUNÇÃO OBJETIVO (3 PENALIDADES)
# ==========================

def calcular_custo(estado):

    volume = calcular_volume(estado)
    custo = calcular_custo_real(estado)

    # Penalidade 1: Falta de volume
    penalidade_falta = 0
    if volume < VOLUME_TOTAL_L:
        penalidade_falta = (VOLUME_TOTAL_L - volume) * 5000

    # Penalidade 2: Excesso de volume
    penalidade_excesso = 0
    if volume > VOLUME_TOTAL_L:
        penalidade_excesso = (volume - VOLUME_TOTAL_L) * 5000

    # Penalidade 3: Restrição de peso
    penalidade_peso = 0
    for i in range(len(FRASCOS)):
        if estado[i] > 0:
            peso_liquido = FRASCOS[i]["capacidade"] * DENSIDADE

            if peso_liquido > FRASCOS[i]["peso_max"]:
                penalidade_peso += 1000000

    return (
        custo
        + penalidade_falta
        + penalidade_excesso
        + penalidade_peso
    )

# ==========================
# SOLUÇÃO INICIAL
# ==========================

def gerar_solucao_inicial():

    estado = [0] * len(FRASCOS)

    volume_restante = VOLUME_TOTAL_L

    for i in range(len(FRASCOS)):
        capacidade = FRASCOS[i]["capacidade"]

        qtd = volume_restante // capacidade

        estado[i] = int(qtd)

        volume_restante -= qtd * capacidade

    return estado

# ==========================
# GERAR VIZINHO
# ==========================

def gerar_vizinho(estado):

    vizinho = estado[:]

    acao = random.choice([
        "adicionar",
        "remover",
        "trocar",
        "reiniciar"
    ])

    idx = random.randint(0, len(FRASCOS) - 1)

    if acao == "adicionar":
        vizinho[idx] += random.randint(1, 3)

    elif acao == "remover":
        if vizinho[idx] > 0:
            vizinho[idx] -= random.randint(
                1,
                min(3, vizinho[idx])
            )

    elif acao == "trocar":

        idx2 = random.randint(
            0,
            len(FRASCOS) - 1
        )

        if idx != idx2 and vizinho[idx2] > 0:
            vizinho[idx2] -= 1
            vizinho[idx] += 1

    elif acao == "reiniciar":

        vizinho = [
            random.randint(0, max(1, VOLUME_TOTAL_L // 1000)),
            random.randint(0, max(1, VOLUME_TOTAL_L // 200)),
            random.randint(0, max(1, VOLUME_TOTAL_L // 100)),
            random.randint(0, max(1, VOLUME_TOTAL_L // 50)),
            random.randint(0, max(1, VOLUME_TOTAL_L // 20)),
            random.randint(0, max(1, VOLUME_TOTAL_L // 5))
        ]

    return vizinho

# ==========================
# SIMULATED ANNEALING
# ==========================

def otimizar_envase():

    estado_atual = gerar_solucao_inicial()

    custo_atual = calcular_custo(estado_atual)

    melhor_estado = estado_atual[:]
    melhor_custo = custo_atual

    temperatura = 50000.0
    taxa_resfriamento = 0.9995

    iteracoes = 100000

    historico_atual = []
    historico_melhor = []

    for _ in range(iteracoes):

        historico_atual.append(custo_atual)
        historico_melhor.append(melhor_custo)

        vizinho = gerar_vizinho(estado_atual)

        custo_vizinho = calcular_custo(vizinho)

        delta = custo_vizinho - custo_atual

        if (
            delta < 0
            or random.random() < math.exp(-delta / temperatura)
        ):

            estado_atual = vizinho
            custo_atual = custo_vizinho

            volume = calcular_volume(estado_atual)

            if (
                volume == VOLUME_TOTAL_L
                and custo_atual < melhor_custo
            ):
                melhor_estado = estado_atual[:]
                melhor_custo = custo_atual

        temperatura *= taxa_resfriamento

        if temperatura < 0.0001:
            break

    return (
        melhor_estado,
        melhor_custo,
        historico_atual,
        historico_melhor
    )

# ==========================
# EXECUÇÃO
# ==========================

if __name__ == "__main__":

    print("Iniciando Agente ChemOptima...\\n")

    (
        melhor_estado,
        melhor_custo,
        historico_atual,
        historico_melhor
    ) = otimizar_envase()

    print("=== RELATÓRIO DE ENVASE OTIMIZADO ===")

    print(
        f"Lote Total: {VOLUME_TOTAL_L} Litros "
        f"(Densidade: {DENSIDADE} | "
        f"Massa: {MASSA_TOTAL_KG:.1f} kg)"
    )

    print("-" * 40)
    print("Distribuição Ideal:")

    for i, qtd in enumerate(melhor_estado):

        if qtd > 0:

            peso_unitario = (
                FRASCOS[i]["capacidade"] *
                DENSIDADE
            )

            print(
                f" -> {qtd}x {FRASCOS[i]['nome']} "
                f"(Peso unitário com líquido: "
                f"{peso_unitario:.1f} kg)"
            )

    volume_final = calcular_volume(melhor_estado)

    custo_real = calcular_custo_real(melhor_estado)

    aproveitamento = (
        (VOLUME_TOTAL_L / volume_final) * 100
        if volume_final > 0
        else 0
    )

    print("-" * 40)
    print(f"Espaço Total Alocado: {volume_final} Litros")
    print(f"Aproveitamento: {aproveitamento:.1f}%")
    print(f"Custo Final: R$ {custo_real:.2f}")

    plt.figure(figsize=(12, 6))

    plt.plot(historico_atual, label="Custo Atual")
    plt.plot(historico_melhor, label="Melhor Solução")

    plt.title("Aprendizado do Agente - Simulated Annealing")
    plt.xlabel("Iterações")
    plt.ylabel("Custo")

    plt.grid(True)
    plt.legend()

    plt.show()
