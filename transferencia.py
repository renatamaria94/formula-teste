import streamlit as st

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Simulador de Transferência de Votos",
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
    """
    Normaliza dois percentuais para que somem 100.
    """

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
    parametro_territorial,
    parametro_empenho,
    parametro_avaliacao,
    pct_lula,
    parametro_lula
):

    # ========================================================
    # 1. BASE ESTADUAL
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
    # 3. AJUSTE TERRITORIAL
    #
    # Mede quanto a esquerda municipal está acima/abaixo
    # da esquerda estadual.
    #
    # Exemplo:
    #
    # Estado    = 56
    # Município = 67
    #
    # diferencial = +11
    #
    # O parâmetro territorial determina quanto dessa diferença
    # entra no ponto de partida municipal.
    #
    # 100% = utiliza toda a diferença
    # 50%  = utiliza metade
    # 0%   = ignora a diferença municipal
    # ========================================================

    diferencial_municipal = (
        esquerda_municipio -
        joao_estado
    )

    fator_territorial = (
        parametro_territorial / 100
    )

    ajuste_territorial = (
        diferencial_municipal *
        fator_territorial
    )

    joao_inicial = limitar(
        joao_estado +
        ajuste_territorial
    )

    raquel_inicial = (
        100 - joao_inicial
    )


    # ========================================================
    # 4. CANDIDATO APOIADO PELO PREFEITO
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
    # votação prefeito - votação atual candidato apoiado
    #
    # Só utilizamos gap positivo.
    # ========================================================

    gap_prefeito_bruto = (
        pct_prefeito -
        base_apoiado
    )

    gap_prefeito = max(
        gap_prefeito_bruto,
        0
    )


    # ========================================================
    # 6. EMPENHO
    #
    # Percentual do gap que o prefeito mobiliza.
    # ========================================================

    fator_empenho = (
        parametro_empenho / 100
    )

    transferencia_empenho = (
        gap_prefeito *
        fator_empenho
    )


    # ========================================================
    # 7. AVALIAÇÃO
    #
    # A avaliação atua SOBRE A TRANSFERÊNCIA.
    #
    # Não multiplica a votação total do candidato.
    #
    # 100% = mantém toda a transferência do empenho
    # 50%  = mantém metade
    # 0%   = zera a transferência
    # >100 = potencializa, limitado pelo gap disponível
    # ========================================================

    fator_avaliacao = (
        parametro_avaliacao / 100
    )

    transferencia_prefeito_bruta = (
        transferencia_empenho *
        fator_avaliacao
    )

    # Não ultrapassar o gap disponível
    transferencia_prefeito = min(
        transferencia_prefeito_bruta,
        gap_prefeito
    )

    transferencia_prefeito = max(
        transferencia_prefeito,
        0
    )


    # ========================================================
    # 8. RESULTADO APÓS PREFEITO
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
            100 -
            joao_apos_prefeito
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
            100 -
            raquel_apos_prefeito
        )


    # ========================================================
    # 9. GAP DE LULA
    #
    # AUTOMÁTICO.
    #
    # Lula no município
    # -
    # esquerda depois das transferências anteriores
    #
    # Se <= 0, Lula não entra.
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
    # 10. APROVEITAMENTO DO GAP DE LULA
    #
    # O gap é automático.
    #
    # Este parâmetro determina quanto do gap positivo
    # efetivamente migra para João.
    #
    # Sugestão inicial = 20%
    # mas pode ser alterada pelo usuário.
    # ========================================================

    fator_lula = (
        parametro_lula / 100
    )

    transferencia_lula = (
        gap_lula *
        fator_lula
    )


    # ========================================================
    # 11. RESULTADO FINAL
    # ========================================================

    joao_final = (
        joao_apos_prefeito +
        transferencia_lula
    )

    joao_final = limitar(
        joao_final
    )

    raquel_final = (
        100 -
        joao_final
    )


    # ========================================================
    # RETORNO
    # ========================================================

    return {

        # Base estadual
        "joao_estado":
            joao_estado,

        "raquel_estado":
            raquel_estado,


        # Base municipal
        "esquerda_municipio":
            esquerda_municipio,

        "direita_municipio":
            direita_municipio,


        # Territorial
        "diferencial_municipal":
            diferencial_municipal,

        "fator_territorial":
            fator_territorial,

        "ajuste_territorial":
            ajuste_territorial,

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


        # Depois do prefeito
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

st.markdown(
    """
    Os valores abaixo podem ser alterados livremente.
    Os parâmetros do modelo já aparecem com valores sugeridos,
    mas não são fixos.
    """
)


# ============================================================
# 1. DADOS DO CENÁRIO
# ============================================================

st.header("Dados do cenário")

col1, col2, col3 = st.columns(3)


# ------------------------------------------------------------
# BASE ESTADUAL
# ------------------------------------------------------------

with col1:

    st.subheader("Base 0 — Pernambuco")

    joao_estado = st.number_input(
        "João Campos no Estado (%)",
        min_value=0.0,
        max_value=100.0,
        value=56.0,
        step=0.1,
        key="joao_estado"
    )

    raquel_estado = st.number_input(
        "Raquel Lyra no Estado (%)",
        min_value=0.0,
        max_value=100.0,
        value=44.0,
        step=0.1,
        key="raquel_estado"
    )


# ------------------------------------------------------------
# BASE MUNICIPAL
# ------------------------------------------------------------

with col2:

    st.subheader("Base do município")

    esquerda_municipio = st.number_input(
        "Esquerda no município (%)",
        min_value=0.0,
        max_value=100.0,
        value=67.0,
        step=0.1,
        key="esquerda_municipio"
    )

    direita_municipio = st.number_input(
        "Direita no município (%)",
        min_value=0.0,
        max_value=100.0,
        value=33.0,
        step=0.1,
        key="direita_municipio"
    )


# ------------------------------------------------------------
# DADOS LOCAIS
# ------------------------------------------------------------

with col3:

    st.subheader("Dados locais")

    pct_prefeito = st.number_input(
        "Votação do prefeito (%)",
        min_value=0.0,
        max_value=100.0,
        value=56.0,
        step=0.1,
        key="pct_prefeito"
    )

    lado_prefeito = st.selectbox(
        "Quem o prefeito apoia?",
        [
            "Esquerda — João Campos",
            "Direita — Raquel Lyra"
        ],
        index=1,
        key="lado_prefeito"
    )

    pct_lula = st.number_input(
        "Votação de Lula no município (%)",
        min_value=0.0,
        max_value=100.0,
        value=86.0,
        step=0.1,
        key="pct_lula"
    )


# ============================================================
# 2. PARÂMETROS DO MODELO
# ============================================================

st.divider()

st.header("Parâmetros do modelo")

st.caption(
    "Os valores abaixo são sugestões iniciais. "
    "Todos podem ser alterados para testar cenários."
)

p1, p2, p3, p4 = st.columns(4)


# ------------------------------------------------------------
# PARÂMETRO TERRITORIAL
# ------------------------------------------------------------

with p1:

    st.markdown("#### Ajuste territorial")

    parametro_territorial = st.number_input(
        "Peso da base municipal (%)",
        min_value=0.0,
        max_value=100.0,
        value=100.0,
        step=1.0,
        key="parametro_territorial",
        help=(
            "Define quanto da diferença entre a base municipal "
            "e a base estadual entra no ponto de partida local. "
            "100% usa toda a diferença; 50% usa metade."
        )
    )

    st.caption("Sugestão: 100%")


# ------------------------------------------------------------
# EMPENHO
# ------------------------------------------------------------

with p2:

    st.markdown("#### Empenho")

    parametro_empenho = st.number_input(
        "Empenho do prefeito (%)",
        min_value=0.0,
        max_value=100.0,
        value=80.0,
        step=1.0,
        key="parametro_empenho",
        help=(
            "Define quanto do gap disponível do prefeito "
            "é mobilizado."
        )
    )

    st.caption("Sugestão: 80%")


# ------------------------------------------------------------
# AVALIAÇÃO
# ------------------------------------------------------------

with p3:

    st.markdown("#### Avaliação")

    parametro_avaliacao = st.number_input(
        "Efeito da avaliação (%)",
        min_value=0.0,
        max_value=150.0,
        value=100.0,
        step=1.0,
        key="parametro_avaliacao",
        help=(
            "Ajusta a transferência produzida pelo empenho. "
            "100% mantém o efeito; abaixo reduz; acima aumenta, "
            "sem ultrapassar o gap disponível."
        )
    )

    st.caption("Sugestão: 100%")


# ------------------------------------------------------------
# LULA
# ------------------------------------------------------------

with p4:

    st.markdown("#### Lula")

    parametro_lula = st.number_input(
        "Aproveitamento do gap de Lula (%)",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        step=1.0,
        key="parametro_lula",
        help=(
            "O gap é calculado automaticamente. "
            "Este parâmetro define quanto do gap positivo "
            "é transferido para João."
        )
    )

    st.caption("Sugestão: 20%")


# ============================================================
# 3. EXECUTAR CÁLCULO
# ============================================================

resultado = calcular_transferencia(

    joao_estado=joao_estado,

    raquel_estado=raquel_estado,

    esquerda_municipio=esquerda_municipio,

    direita_municipio=direita_municipio,

    pct_prefeito=pct_prefeito,

    lado_prefeito=lado_prefeito,

    parametro_territorial=parametro_territorial,

    parametro_empenho=parametro_empenho,

    parametro_avaliacao=parametro_avaliacao,

    pct_lula=pct_lula,

    parametro_lula=parametro_lula
)


# ============================================================
# 4. RESULTADO FINAL
# ============================================================

st.divider()

st.header("Resultado projetado")


if resultado is None:

    st.error(
        "As bases estadual e municipal precisam ter "
        "soma maior que zero."
    )

else:

    r1, r2 = st.columns(2)

    with r1:

        st.metric(
            "João Campos",
            f"{resultado['joao_final']:.2f}%"
        )

    with r2:

        st.metric(
            "Raquel Lyra",
            f"{resultado['raquel_final']:.2f}%"
        )


    st.progress(
        resultado["joao_final"] / 100,
        text=(
            f"João {resultado['joao_final']:.1f}%"
            f" × "
            f"Raquel {resultado['raquel_final']:.1f}%"
        )
    )


    # ========================================================
    # 5. FLUXO RESUMIDO
    # ========================================================

    st.subheader("Evolução do cenário")

    e1, e2, e3 = st.columns(3)

    with e1:

        st.markdown("**Após ajuste municipal**")

        st.metric(
            "João",
            f"{resultado['joao_inicial']:.2f}%"
        )

        st.metric(
            "Raquel",
            f"{resultado['raquel_inicial']:.2f}%"
        )

    with e2:

        st.markdown("**Após prefeito**")

        st.metric(
            "João",
            f"{resultado['joao_apos_prefeito']:.2f}%"
        )

        st.metric(
            "Raquel",
            f"{resultado['raquel_apos_prefeito']:.2f}%"
        )

    with e3:

        st.markdown("**Após Lula**")

        st.metric(
            "João",
            f"{resultado['joao_final']:.2f}%"
        )

        st.metric(
            "Raquel",
            f"{resultado['raquel_final']:.2f}%"
        )


    # ========================================================
    # 6. MEMÓRIA DE CÁLCULO
    # ========================================================

    st.divider()

    st.header("Memória de cálculo")


    # --------------------------------------------------------
    # BASE ESTADUAL
    # --------------------------------------------------------

    with st.expander(
        "1. Base 0 estadual",
        expanded=False
    ):

        st.write(
            f"João Campos: "
            f"**{resultado['joao_estado']:.2f}%**"
        )

        st.write(
            f"Raquel Lyra: "
            f"**{resultado['raquel_estado']:.2f}%**"
        )


    # --------------------------------------------------------
    # AJUSTE MUNICIPAL
    # --------------------------------------------------------

    with st.expander(
        "2. Ajuste municipal",
        expanded=True
    ):

        st.write(
            f"Esquerda no município: "
            f"**{resultado['esquerda_municipio']:.2f}%**"
        )

        st.write(
            f"Esquerda estadual: "
            f"**{resultado['joao_estado']:.2f}%**"
        )

        st.write(
            f"Diferença territorial: "
            f"**{resultado['diferencial_municipal']:+.2f} p.p.**"
        )

        st.write(
            f"Peso territorial utilizado: "
            f"**{parametro_territorial:.0f}%**"
        )

        st.code(
            f"{resultado['diferencial_municipal']:.2f} "
            f"× {parametro_territorial / 100:.2f} "
            f"= {resultado['ajuste_territorial']:.2f} p.p."
        )

        st.write("Ponto de partida municipal:")

        c1, c2 = st.columns(2)

        c1.metric(
            "João",
            f"{resultado['joao_inicial']:.2f}%"
        )

        c2.metric(
            "Raquel",
            f"{resultado['raquel_inicial']:.2f}%"
        )


    # --------------------------------------------------------
    # PREFEITO
    # --------------------------------------------------------

    with st.expander(
        "3. Gap do prefeito",
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

        st.code(
            f"{resultado['pct_prefeito']:.2f} "
            f"- {resultado['base_apoiado']:.2f} "
            f"= {resultado['gap_prefeito_bruto']:.2f} p.p."
        )


        if resultado["gap_prefeito"] <= 0:

            st.info(
                "O gap do prefeito é zero ou negativo. "
                "Não há transferência adicional do prefeito."
            )

        else:

            st.success(
                f"Gap disponível: "
                f"{resultado['gap_prefeito']:.2f} p.p."
            )


    # --------------------------------------------------------
    # EMPENHO
    # --------------------------------------------------------

    with st.expander(
        "4. Empenho",
        expanded=True
    ):

        st.write(
            f"Gap disponível: "
            f"**{resultado['gap_prefeito']:.2f} p.p.**"
        )

        st.write(
            f"Parâmetro de empenho: "
            f"**{parametro_empenho:.0f}%**"
        )

        st.code(
            f"{resultado['gap_prefeito']:.2f} "
            f"× {parametro_empenho / 100:.2f} "
            f"= {resultado['transferencia_empenho']:.2f} p.p."
        )


    # --------------------------------------------------------
    # AVALIAÇÃO
    # --------------------------------------------------------

    with st.expander(
        "5. Avaliação",
        expanded=True
    ):

        st.write(
            f"Transferência após empenho: "
            f"**{resultado['transferencia_empenho']:.2f} p.p.**"
        )

        st.write(
            f"Parâmetro de avaliação: "
            f"**{parametro_avaliacao:.0f}%**"
        )

        st.code(
            f"{resultado['transferencia_empenho']:.2f} "
            f"× {parametro_avaliacao / 100:.2f} "
            f"= {resultado['transferencia_prefeito_bruta']:.2f} p.p."
        )

        st.success(
            f"Transferência efetiva do prefeito: "
            f"{resultado['transferencia_prefeito']:.2f} p.p."
        )


    # --------------------------------------------------------
    # RESULTADO ANTES DE LULA
    # --------------------------------------------------------

    with st.expander(
        "6. Resultado antes de Lula",
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


    # --------------------------------------------------------
    # LULA
    # --------------------------------------------------------

    with st.expander(
        "7. Gap de Lula",
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

        st.code(
            f"{resultado['pct_lula']:.2f} "
            f"- {resultado['joao_apos_prefeito']:.2f} "
            f"= {resultado['gap_lula_bruto']:.2f} p.p."
        )


        if resultado["gap_lula"] <= 0:

            st.info(
                "O gap de Lula é zero ou negativo. "
                "Lula não entra no cálculo final."
            )

        else:

            st.write(
                f"Gap positivo: "
                f"**{resultado['gap_lula']:.2f} p.p.**"
            )

            st.write(
                f"Aproveitamento definido: "
                f"**{parametro_lula:.0f}%**"
            )

            st.code(
                f"{resultado['gap_lula']:.2f} "
                f"× {parametro_lula / 100:.2f} "
                f"= {resultado['transferencia_lula']:.2f} p.p."
            )

            st.success(
                f"Transferência adicional para João: "
                f"{resultado['transferencia_lula']:.2f} p.p."
            )


    # ========================================================
    # 8. RESUMO DOS PARÂMETROS
    # ========================================================

    with st.expander(
        "Parâmetros utilizados neste cenário",
        expanded=False
    ):

        st.write(
            f"**Peso da base municipal:** "
            f"{parametro_territorial:.0f}%"
        )

        st.write(
            f"**Empenho do prefeito:** "
            f"{parametro_empenho:.0f}%"
        )

        st.write(
            f"**Efeito da avaliação:** "
            f"{parametro_avaliacao:.0f}%"
        )

        st.write(
            f"**Aproveitamento do gap de Lula:** "
            f"{parametro_lula:.0f}%"
        )


    # ========================================================
    # 9. RESULTADO FINAL
    # ========================================================

    st.divider()

    st.subheader("Cenário final")

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
        "Base estadual → ajuste territorial → "
        "gap do prefeito → empenho → avaliação → "
        "gap automático de Lula → resultado final."
    )
