import streamlit as st

# ============================================================
# CONFIGURAÇÃO
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
    return max(minimo, min(maximo, valor))


def normalizar(esquerda, direita):
    total = esquerda + direita

    if total <= 0:
        return None, None

    return (
        esquerda / total * 100,
        direita / total * 100
    )


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def calcular_transferencia(
    joao_estado,
    raquel_estado,
    esquerda_municipio,
    direita_municipio,
    pct_prefeito,
    lado_prefeito,
    empenho,
    avaliacao,
    pct_lula
):

    # ========================================================
    # 1. BASE 0 ESTADUAL
    # ========================================================

    joao_estado, raquel_estado = normalizar(
        joao_estado,
        raquel_estado
    )

    if joao_estado is None:
        return None


    # ========================================================
    # 2. BASE MUNICIPAL
    # ========================================================

    esquerda_municipio, direita_municipio = normalizar(
        esquerda_municipio,
        direita_municipio
    )

    if esquerda_municipio is None:
        return None


    # ========================================================
    # 3. EFEITO TERRITORIAL DO MUNICÍPIO
    #
    # Comparamos a estrutura municipal com a estadual.
    #
    # Exemplo:
    #
    # Estado:    esquerda = 56
    # Município: esquerda = 67
    #
    # efeito municipal = +11 p.p.
    #
    # João:
    # 56 + 11 = 67
    #
    # Nesse caso, a base municipal já representa diretamente
    # o ponto de partida local.
    # ========================================================

    diferencial_municipal = (
        esquerda_municipio - joao_estado
    )

    joao_inicial = limitar(
        joao_estado + diferencial_municipal
    )

    raquel_inicial = (
        100 - joao_inicial
    )


    # ========================================================
    # 4. IDENTIFICAR CANDIDATO APOIADO PELO PREFEITO
    # ========================================================

    if lado_prefeito == "Esquerda — João Campos":

        candidato_apoiado = "João Campos"
        base_apoiado = joao_inicial

    else:

        candidato_apoiado = "Raquel Lyra"
        base_apoiado = raquel_inicial


    # ========================================================
    # 5. GAP DO PREFEITO
    #
    # votação do prefeito - votação atual do candidato apoiado
    #
    # Se <= 0:
    # não há reserva adicional para transferir.
    # ========================================================

    gap_prefeito_bruto = (
        pct_prefeito - base_apoiado
    )

    gap_prefeito = max(
        gap_prefeito_bruto,
        0
    )


    # ========================================================
    # 6. EMPENHO
    #
    # Quanto do gap o prefeito mobiliza.
    #
    # Exemplo:
    #
    # gap = 20
    # empenho = 80%
    #
    # transferência = 16 p.p.
    # ========================================================

    fator_empenho = empenho / 100

    transferencia_empenho = (
        gap_prefeito *
        fator_empenho
    )


    # ========================================================
    # 7. AVALIAÇÃO
    #
    # A avaliação atua SOBRE A TRANSFERÊNCIA,
    # não sobre a votação total do candidato.
    #
    # 100% = mantém toda a transferência
    # 50%  = mantém metade
    # 0%   = nenhuma transferência efetiva
    # ========================================================

    fator_avaliacao = avaliacao / 100

    transferencia_prefeito = (
        transferencia_empenho *
        fator_avaliacao
    )

    # Não pode ultrapassar o gap original
    transferencia_prefeito = min(
        transferencia_prefeito,
        gap_prefeito
    )

    transferencia_prefeito = max(
        transferencia_prefeito,
        0
    )


    # ========================================================
    # 8. RESULTADO APÓS O PREFEITO
    # ========================================================

    if lado_prefeito == "Esquerda — João Campos":

        joao_apos_prefeito = (
            joao_inicial +
            transferencia_prefeito
        )

        joao_apos_prefeito = limitar(
            joao_apos_prefeito
        )

        raquel_apos_prefeito = (
            100 - joao_apos_prefeito
        )

    else:

        raquel_apos_prefeito = (
            raquel_inicial +
            transferencia_prefeito
        )

        raquel_apos_prefeito = limitar(
            raquel_apos_prefeito
        )

        joao_apos_prefeito = (
            100 - raquel_apos_prefeito
        )


    # ========================================================
    # 9. GAP DE LULA
    #
    # AGORA É AUTOMÁTICO.
    #
    # Lula é comparado com a esquerda DEPOIS das
    # transferências anteriores.
    #
    # gap Lula =
    #
    # % Lula no município
    # -
    # % João após efeito do prefeito
    #
    # Se <= 0:
    # Lula NÃO entra.
    # ========================================================

    gap_lula_bruto = (
        pct_lula -
        joao_apos_prefeito
    )

    gap_lula = max(
        gap_lula_bruto,
        0
    )


    # ========================================================
    # 10. RESULTADO FINAL
    #
    # O gap positivo de Lula entra automaticamente.
    # Não existe mais input de "força de Lula".
    # ========================================================

    transferencia_lula = gap_lula

    joao_final = (
        joao_apos_prefeito +
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

        # Estado
        "joao_estado":
            joao_estado,

        "raquel_estado":
            raquel_estado,


        # Município
        "esquerda_municipio":
            esquerda_municipio,

        "direita_municipio":
            direita_municipio,

        "diferencial_municipal":
            diferencial_municipal,


        # Ponto de partida local
        "joao_inicial":
            joao_inicial,

        "raquel_inicial":
            raquel_inicial,


        # Prefeito
        "candidato_apoiado":
            candidato_apoiado,

        "pct_prefeito":
            pct_prefeito,

        "base_apoiado":
            base_apoiado,

        "gap_prefeito_bruto":
            gap_prefeito_bruto,

        "gap_prefeito":
            gap_prefeito,


        # Empenho
        "transferencia_empenho":
            transferencia_empenho,


        # Avaliação
        "transferencia_prefeito":
            transferencia_prefeito,


        # Após prefeito
        "joao_apos_prefeito":
            joao_apos_prefeito,

        "raquel_apos_prefeito":
            raquel_apos_prefeito,


        # Lula
        "pct_lula":
            pct_lula,

        "gap_lula_bruto":
            gap_lula_bruto,

        "gap_lula":
            gap_lula,

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


# ============================================================
# LINHA 1
# BASE ESTADUAL + BASE MUNICIPAL
# ============================================================

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# BASE 0 ESTADUAL
# ------------------------------------------------------------

with col1:

    st.markdown("### 1. Base 0 — Pernambuco")

    st.caption(
        "Ponto de partida estadual de João Campos e Raquel Lyra."
    )

    joao_estado = st.number_input(
        "João Campos — Estado (%)",
        min_value=0.0,
        max_value=100.0,
        value=56.0,
        step=0.1
    )

    raquel_estado = st.number_input(
        "Raquel Lyra — Estado (%)",
        min_value=0.0,
        max_value=100.0,
        value=44.0,
        step=0.1
    )


# ------------------------------------------------------------
# BASE MUNICIPAL
# ------------------------------------------------------------

with col2:

    st.markdown("### 2. Base do município")

    st.caption(
        "Força histórica da esquerda e da direita no município."
    )

    esquerda_municipio = st.number_input(
        "Esquerda no município (%)",
        min_value=0.0,
        max_value=100.0,
        value=67.0,
        step=0.1
    )

    direita_municipio = st.number_input(
        "Direita no município (%)",
        min_value=0.0,
        max_value=100.0,
        value=33.0,
        step=0.1
    )


st.divider()


# ============================================================
# LINHA 2
# PREFEITO + LULA
# ============================================================

col3, col4 = st.columns(2)


# ------------------------------------------------------------
# PREFEITO
# ------------------------------------------------------------

with col3:

    st.markdown("### 3. Prefeito")

    pct_prefeito = st.number_input(
        "Votação do prefeito (%)",
        min_value=0.0,
        max_value=100.0,
        value=56.0,
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
        "Empenho do prefeito (%)",
        min_value=0.0,
        max_value=100.0,
        value=80.0,
        step=1.0
    )

    avaliacao = st.number_input(
        "Avaliação do prefeito (%)",
        min_value=0.0,
        max_value=150.0,
        value=100.0,
        step=1.0
    )


# ------------------------------------------------------------
# LULA
# ------------------------------------------------------------

with col4:

    st.markdown("### 4. Lula")

    pct_lula = st.number_input(
        "Votação de Lula no município (%)",
        min_value=0.0,
        max_value=100.0,
        value=86.0,
        step=0.1
    )

    st.info(
        "O gap de Lula é calculado automaticamente depois "
        "do efeito do prefeito."
    )


# ============================================================
# CALCULAR
# ============================================================

resultado = calcular_transferencia(

    joao_estado=joao_estado,

    raquel_estado=raquel_estado,

    esquerda_municipio=esquerda_municipio,

    direita_municipio=direita_municipio,

    pct_prefeito=pct_prefeito,

    lado_prefeito=lado_prefeito,

    empenho=empenho,

    avaliacao=avaliacao,

    pct_lula=pct_lula
)


# ============================================================
# RESULTADO
# ============================================================

st.divider()

st.subheader("Resultado projetado no município")


if resultado is None:

    st.error(
        "As bases precisam ter soma maior que zero."
    )

else:

    # ========================================================
    # CARDS FINAIS
    # ========================================================

    c1, c2 = st.columns(2)

    c1.metric(
        "João Campos",
        f"{resultado['joao_final']:.2f}%"
    )

    c2.metric(
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
    # 1. ESTADO
    # ========================================================

    with st.expander(
        "1. Base 0 — Pernambuco",
        expanded=True
    ):

        c1, c2 = st.columns(2)

        c1.metric(
            "João Campos",
            f"{resultado['joao_estado']:.2f}%"
        )

        c2.metric(
            "Raquel Lyra",
            f"{resultado['raquel_estado']:.2f}%"
        )


    # ========================================================
    # 2. MUNICÍPIO
    # ========================================================

    with st.expander(
        "2. Ajuste municipal",
        expanded=True
    ):

        c1, c2 = st.columns(2)

        c1.metric(
            "Esquerda no município",
            f"{resultado['esquerda_municipio']:.2f}%"
        )

        c2.metric(
            "Direita no município",
            f"{resultado['direita_municipio']:.2f}%"
        )

        st.write(
            f"Diferença da esquerda municipal em relação "
            f"à Base 0 estadual: "
            f"**{resultado['diferencial_municipal']:+.2f} p.p.**"
        )

        st.write("Ponto de partida ajustado:")

        c1, c2 = st.columns(2)

        c1.metric(
            "João",
            f"{resultado['joao_inicial']:.2f}%"
        )

        c2.metric(
            "Raquel",
            f"{resultado['raquel_inicial']:.2f}%"
        )


    # ========================================================
    # 3. PREFEITO
    # ========================================================

    with st.expander(
        "3. Transferência do prefeito",
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
            f"Base atual do candidato apoiado: "
            f"**{resultado['base_apoiado']:.2f}%**"
        )

        st.write(
            f"Gap do prefeito: "
            f"**{resultado['gap_prefeito']:.2f} p.p.**"
        )


        if resultado["gap_prefeito"] <= 0:

            st.info(
                "A votação do prefeito não supera a base "
                "do candidato apoiado. Não há gap adicional "
                "para transferir."
            )

        else:

            st.write(
                f"Empenho: **{empenho:.0f}%**"
            )

            st.write(
                f"Após o empenho: "
                f"**{resultado['transferencia_empenho']:.2f} p.p.** "
                f"potenciais."
            )

            st.write(
                f"Avaliação: **{avaliacao:.0f}%**"
            )

            st.success(
                f"Transferência efetiva do prefeito: "
                f"{resultado['transferencia_prefeito']:.2f} p.p."
            )


    # ========================================================
    # 4. RESULTADO ANTES DE LULA
    # ========================================================

    with st.expander(
        "4. Resultado antes de Lula",
        expanded=True
    ):

        c1, c2 = st.columns(2)

        c1.metric(
            "João Campos",
            f"{resultado['joao_apos_prefeito']:.2f}%"
        )

        c2.metric(
            "Raquel Lyra",
            f"{resultado['raquel_apos_prefeito']:.2f}%"
        )


    # ========================================================
    # 5. LULA
    # ========================================================

    with st.expander(
        "5. Gap de Lula",
        expanded=True
    ):

        st.write(
            f"Lula no município: "
            f"**{resultado['pct_lula']:.2f}%**"
        )

        st.write(
            f"Esquerda após as transferências anteriores: "
            f"**{resultado['joao_apos_prefeito']:.2f}%**"
        )

        st.write(
            "Cálculo:"
        )

        st.code(
            f"{resultado['pct_lula']:.2f} "
            f"- "
            f"{resultado['joao_apos_prefeito']:.2f} "
            f"= "
            f"{resultado['gap_lula_bruto']:.2f} p.p."
        )


        if resultado["gap_lula_bruto"] <= 0:

            st.info(
                "O gap é zero ou negativo. "
                "Lula não entra no cálculo final."
            )

        else:

            st.success(
                f"Gap positivo de Lula: "
                f"{resultado['gap_lula']:.2f} p.p."
            )

            st.write(
                f"Transferência de Lula para João: "
                f"**{resultado['transferencia_lula']:.2f} p.p.**"
            )


    # ========================================================
    # 6. RESULTADO FINAL
    # ========================================================

    st.divider()

    st.markdown("## Resultado final")

    c1, c2 = st.columns(2)

    c1.metric(
        "João Campos",
        f"{resultado['joao_final']:.2f}%"
    )

    c2.metric(
        "Raquel Lyra",
        f"{resultado['raquel_final']:.2f}%"
    )

    st.caption(
        "Base estadual → ajuste municipal → gap do prefeito → "
        "empenho → avaliação → gap automático de Lula → resultado."
    )
