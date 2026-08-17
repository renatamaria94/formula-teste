import streamlit as st

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Simulador de Transferência",
    page_icon="🗳️",
    layout="wide"
)

st.title("Simulador de Transferência de Votos")
st.caption("João Campos × Raquel Lyra")


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def limitar(valor, minimo=0.0, maximo=100.0):
    """
    Impede percentuais abaixo de 0 ou acima de 100.
    """
    return max(minimo, min(maximo, valor))


def normalizar_base(esquerda, direita):
    """
    Garante que João + Raquel = 100%.
    """

    total = esquerda + direita

    if total <= 0:
        return None, None

    esquerda = 100 * esquerda / total
    direita = 100 * direita / total

    return esquerda, direita


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def calcular_transferencia(
    esquerda_base,
    direita_base,
    pct_prefeito,
    lado_prefeito,
    empenho,
    avaliacao,
    pct_lula,
    forca_lula
):

    # ========================================================
    # 0. BASE 0
    # ========================================================

    esquerda_base, direita_base = normalizar_base(
        esquerda_base,
        direita_base
    )

    if esquerda_base is None:
        return None


    # --------------------------------------------------------
    # Fatores
    # --------------------------------------------------------

    fator_empenho = empenho / 100
    fator_avaliacao = avaliacao / 100
    fator_lula = forca_lula / 100


    # ========================================================
    # 1. IDENTIFICAR A BASE DO CANDIDATO APOIADO
    # ========================================================

    if lado_prefeito == "Esquerda — João Campos":

        candidato_apoiado = "João Campos"
        base_apoiado = esquerda_base

    else:

        candidato_apoiado = "Raquel Lyra"
        base_apoiado = direita_base


    # ========================================================
    # 2. GAP DO PREFEITO
    #
    # Exemplo:
    #
    # Raquel = 44%
    # Prefeito = 65%
    #
    # gap = 65 - 44 = 21 p.p.
    #
    # Se o prefeito tiver MENOS votos que a base do candidato,
    # não existe gap positivo para transferir.
    # ========================================================

    gap_prefeito_bruto = (
        pct_prefeito - base_apoiado
    )

    if gap_prefeito_bruto > 0:

        gap_prefeito = gap_prefeito_bruto

    else:

        gap_prefeito = 0


    # ========================================================
    # 3. EMPENHO
    #
    # Quanto do gap o prefeito tenta transferir.
    #
    # Exemplo:
    #
    # gap = 21
    # empenho = 80%
    #
    # 21 × 0.80 = 16.8 p.p.
    # ========================================================

    transferencia_empenho = (
        gap_prefeito * fator_empenho
    )


    # ========================================================
    # 4. AVALIAÇÃO
    #
    # A avaliação NÃO multiplica o percentual total
    # de João ou Raquel.
    #
    # Ela atua apenas sobre a transferência produzida
    # pelo empenho.
    #
    # Exemplo:
    #
    # transferência pelo empenho = 16.8
    # avaliação = 80%
    #
    # transferência efetiva =
    # 16.8 × 0.80 = 13.44 p.p.
    #
    # Avaliação = 100%:
    # mantém toda a transferência.
    #
    # Avaliação = 10%:
    # mantém apenas 10% da transferência.
    # ========================================================

    transferencia_prefeito_bruta = (
        transferencia_empenho *
        fator_avaliacao
    )


    # --------------------------------------------------------
    # O prefeito não pode transferir mais que seu gap original.
    #
    # Isso evita que avaliação > 100% ultrapasse a votação
    # que constitui a reserva do prefeito.
    # --------------------------------------------------------

    transferencia_prefeito = min(
        transferencia_prefeito_bruta,
        gap_prefeito
    )

    transferencia_prefeito = max(
        transferencia_prefeito,
        0
    )


    # ========================================================
    # 5. RESULTADO APÓS PREFEITO
    # ========================================================

    if lado_prefeito == "Esquerda — João Campos":

        joao_prefeito = (
            esquerda_base +
            transferencia_prefeito
        )

        joao_prefeito = limitar(
            joao_prefeito
        )

        raquel_prefeito = (
            100 - joao_prefeito
        )

    else:

        raquel_prefeito = (
            direita_base +
            transferencia_prefeito
        )

        raquel_prefeito = limitar(
            raquel_prefeito
        )

        joao_prefeito = (
            100 - raquel_prefeito
        )


    # ========================================================
    # 6. GAP DE LULA
    #
    # Lula funciona como uma reserva adicional para João.
    #
    # O gap é calculado em relação ao resultado de João
    # DEPOIS do efeito do prefeito.
    #
    # gap Lula = Lula - João após prefeito
    #
    # REGRA:
    #
    # Se gap <= 0:
    # Lula NÃO entra no cálculo.
    # ========================================================

    gap_lula_bruto = (
        pct_lula - joao_prefeito
    )


    if gap_lula_bruto > 0:

        gap_lula = gap_lula_bruto

        transferencia_lula = (
            gap_lula *
            fator_lula
        )

    else:

        gap_lula = 0
        transferencia_lula = 0


    # ========================================================
    # 7. RESULTADO FINAL
    # ========================================================

    joao_final = (
        joao_prefeito +
        transferencia_lula
    )

    joao_final = limitar(
        joao_final
    )

    raquel_final = (
        100 - joao_final
    )


    # ========================================================
    # RETORNO
    # ========================================================

    return {

        # Base
        "esquerda_base":
            esquerda_base,

        "direita_base":
            direita_base,


        # Prefeito
        "candidato_apoiado":
            candidato_apoiado,

        "pct_prefeito":
            pct_prefeito,

        "base_apoiado":
            base_apoiado,


        # Gap
        "gap_prefeito_bruto":
            gap_prefeito_bruto,

        "gap_prefeito":
            gap_prefeito,


        # Empenho
        "fator_empenho":
            fator_empenho,

        "transferencia_empenho":
            transferencia_empenho,


        # Avaliação
        "fator_avaliacao":
            fator_avaliacao,

        "transferencia_prefeito_bruta":
            transferencia_prefeito_bruta,

        "transferencia_prefeito":
            transferencia_prefeito,


        # Resultado após prefeito
        "joao_prefeito":
            joao_prefeito,

        "raquel_prefeito":
            raquel_prefeito,


        # Lula
        "pct_lula":
            pct_lula,

        "gap_lula_bruto":
            gap_lula_bruto,

        "gap_lula":
            gap_lula,

        "fator_lula":
            fator_lula,

        "transferencia_lula":
            transferencia_lula,


        # Final
        "joao_final":
            joao_final,

        "raquel_final":
            raquel_final
    }


# ============================================================
# INTERFACE
# ============================================================

st.subheader("Parâmetros")

col1, col2, col3 = st.columns(3)


# ============================================================
# COLUNA 1 — BASE 0
# ============================================================

with col1:

    st.markdown("### Base 0")

    esquerda_base = st.number_input(
        "Esquerda — João Campos (%)",
        min_value=0.0,
        max_value=100.0,
        value=56.0,
        step=0.1
    )

    direita_base = st.number_input(
        "Direita — Raquel Lyra (%)",
        min_value=0.0,
        max_value=100.0,
        value=44.0,
        step=0.1
    )


# ============================================================
# COLUNA 2 — PREFEITO
# ============================================================

with col2:

    st.markdown("### Prefeito")

    pct_prefeito = st.number_input(
        "Votação do prefeito (%)",
        min_value=0.0,
        max_value=100.0,
        value=65.0,
        step=0.1
    )

    lado_prefeito = st.selectbox(
        "Quem o prefeito apoia?",
        [
            "Esquerda — João Campos",
            "Direita — Raquel Lyra"
        ],
        index=1
    )

    empenho = st.number_input(
        "Empenho (%)",
        min_value=0.0,
        max_value=100.0,
        value=100.0,
        step=1.0
    )

    avaliacao = st.number_input(
        "Avaliação (%)",
        min_value=0.0,
        max_value=150.0,
        value=100.0,
        step=1.0
    )


# ============================================================
# COLUNA 3 — LULA
# ============================================================

with col3:

    st.markdown("### Lula")

    pct_lula = st.number_input(
        "Votação de Lula (%)",
        min_value=0.0,
        max_value=100.0,
        value=86.0,
        step=0.1
    )

    forca_lula = st.number_input(
        "Força de Lula sobre o gap (%)",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        step=1.0
    )


# ============================================================
# EXECUTAR CÁLCULO
# ============================================================

resultado = calcular_transferencia(

    esquerda_base=esquerda_base,

    direita_base=direita_base,

    pct_prefeito=pct_prefeito,

    lado_prefeito=lado_prefeito,

    empenho=empenho,

    avaliacao=avaliacao,

    pct_lula=pct_lula,

    forca_lula=forca_lula
)


# ============================================================
# RESULTADO FINAL
# ============================================================

st.divider()

st.subheader("Resultado final")


if resultado is None:

    st.error(
        "A soma da Base 0 precisa ser maior que zero."
    )

else:

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "João Campos",
            f"{resultado['joao_final']:.2f}%"
        )

    with c2:

        st.metric(
            "Raquel Lyra",
            f"{resultado['raquel_final']:.2f}%"
        )


    # ========================================================
    # BARRA
    # ========================================================

    st.progress(
        resultado["joao_final"] / 100,
        text=(
            f"João {resultado['joao_final']:.1f}%"
            f" × "
            f"Raquel {resultado['raquel_final']:.1f}%"
        )
    )


    # ========================================================
    # MEMÓRIA DE CÁLCULO
    # ========================================================

    st.divider()

    st.subheader("Memória de cálculo")


    # ========================================================
    # 1. BASE 0
    # ========================================================

    with st.expander(
        "1. Base 0",
        expanded=True
    ):

        c1, c2 = st.columns(2)

        c1.metric(
            "João Campos",
            f"{resultado['esquerda_base']:.2f}%"
        )

        c2.metric(
            "Raquel Lyra",
            f"{resultado['direita_base']:.2f}%"
        )


    # ========================================================
    # 2. GAP DO PREFEITO
    # ========================================================

    with st.expander(
        "2. Gap do prefeito",
        expanded=True
    ):

        st.write(
            f"O prefeito apoia "
            f"**{resultado['candidato_apoiado']}**."
        )

        st.write(
            f"Votação do prefeito: "
            f"**{resultado['pct_prefeito']:.2f}%**"
        )

        st.write(
            f"Base do candidato apoiado: "
            f"**{resultado['base_apoiado']:.2f}%**"
        )

        st.write(
            f"Gap bruto: "
            f"**{resultado['gap_prefeito_bruto']:.2f} p.p.**"
        )


        if resultado["gap_prefeito"] <= 0:

            st.info(
                "O prefeito não possui gap positivo "
                "em relação à base do candidato apoiado. "
                "Não há votos adicionais para transferir."
            )

        else:

            st.success(
                f"Gap disponível para transferência: "
                f"{resultado['gap_prefeito']:.2f} p.p."
            )


    # ========================================================
    # 3. EMPENHO
    # ========================================================

    with st.expander(
        "3. Empenho do prefeito",
        expanded=True
    ):

        st.write(
            f"Gap disponível: "
            f"**{resultado['gap_prefeito']:.2f} p.p.**"
        )

        st.write(
            f"Empenho: "
            f"**{empenho:.0f}%**"
        )

        st.write(
            f"Transferência após empenho: "
            f"**{resultado['transferencia_empenho']:.2f} p.p.**"
        )

        st.caption(
            "Fórmula: gap do prefeito × empenho."
        )


    # ========================================================
    # 4. AVALIAÇÃO
    # ========================================================

    with st.expander(
        "4. Avaliação do prefeito",
        expanded=True
    ):

        st.write(
            f"Transferência produzida pelo empenho: "
            f"**{resultado['transferencia_empenho']:.2f} p.p.**"
        )

        st.write(
            f"Avaliação: "
            f"**{avaliacao:.0f}%**"
        )

        st.write(
            f"Transferência efetiva do prefeito: "
            f"**{resultado['transferencia_prefeito']:.2f} p.p.**"
        )

        st.caption(
            "A avaliação atua sobre a transferência, "
            "não sobre o percentual total do candidato."
        )


    # ========================================================
    # 5. APÓS PREFEITO
    # ========================================================

    with st.expander(
        "5. Resultado após o efeito do prefeito",
        expanded=True
    ):

        c1, c2 = st.columns(2)

        c1.metric(
            "João Campos",
            f"{resultado['joao_prefeito']:.2f}%"
        )

        c2.metric(
            "Raquel Lyra",
            f"{resultado['raquel_prefeito']:.2f}%"
        )


    # ========================================================
    # 6. LULA
    # ========================================================

    with st.expander(
        "6. Força de Lula",
        expanded=True
    ):

        st.write(
            f"Votação de Lula: "
            f"**{resultado['pct_lula']:.2f}%**"
        )

        st.write(
            f"João após efeito do prefeito: "
            f"**{resultado['joao_prefeito']:.2f}%**"
        )

        st.write(
            f"Gap bruto de Lula: "
            f"**{resultado['gap_lula_bruto']:.2f} p.p.**"
        )


        if resultado["gap_lula"] <= 0:

            st.info(
                "O gap de Lula é zero ou negativo. "
                "Lula não entra no cálculo final."
            )

        else:

            st.write(
                f"Gap utilizado: "
                f"**{resultado['gap_lula']:.2f} p.p.**"
            )

            st.write(
                f"Força de Lula: "
                f"**{forca_lula:.0f}%**"
            )

            st.write(
                f"Transferência adicional para João: "
                f"**{resultado['transferencia_lula']:.2f} p.p.**"
            )

            st.caption(
                "Fórmula: "
                "(Lula − João após prefeito) × força de Lula."
            )


    # ========================================================
    # 7. RESUMO FINAL
    # ========================================================

    st.divider()

    st.markdown("### Cenário projetado")

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "João Campos",
            f"{resultado['joao_final']:.2f}%"
        )

    with c2:

        st.metric(
            "Raquel Lyra",
            f"{resultado['raquel_final']:.2f}%"
        )


    # ========================================================
    # EXPLICAÇÃO CURTA
    # ========================================================

    st.caption(
        "Base 0 → gap do prefeito → empenho → avaliação → "
        "resultado após prefeito → gap de Lula → resultado final."
    )
