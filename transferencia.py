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
# CATEGORIAS
# ============================================================

CATEGORIAS = [
    "Muito fraco",
    "Fraco",
    "Moderado",
    "Forte",
    "Muito forte"
]


# ============================================================
# PARÂMETROS PADRÃO
# ============================================================

PARAMETROS_PADRAO = {

    "empenho": {
        "Muito fraco": 0.00,
        "Fraco": 0.10,
        "Moderado": 0.50,
        "Forte": 0.80,
        "Muito forte": 1.00
    },

    "avaliacao": {
        "Muito fraco": 0.00,
        "Fraco": 0.10,
        "Moderado": 0.50,
        "Forte": 0.80,
        "Muito forte": 1.00
    },

    "lula": {
        "Muito fraco": 0.00,
        "Fraco": 0.10,
        "Moderado": 0.50,
        "Forte": 0.80,
        "Muito forte": 1.00
    }
}


# ============================================================
# PARÂMETROS DA PESQUISA
# ============================================================

PARAMETROS_PESQUISA = {
    "0 a 5 p.p.": 0.20,
    "5 a 10 p.p.": 0.20,
    "10 p.p. ou mais": 0.20
}


# ============================================================
# SESSION STATE
# ============================================================

for variavel, escala in PARAMETROS_PADRAO.items():

    for categoria, valor in escala.items():

        chave = f"param_{variavel}_{categoria}"

        if chave not in st.session_state:
            st.session_state[chave] = valor


for faixa, valor in PARAMETROS_PESQUISA.items():

    chave = f"pesquisa_{faixa}"

    if chave not in st.session_state:
        st.session_state[chave] = valor


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def limitar(valor):
    return max(0.0, min(100.0, valor))


def normalizar(a, b):

    total = a + b

    if total <= 0:
        return None, None

    return (
        a / total * 100,
        b / total * 100
    )


def obter_fator_pesquisa(gap):

    if gap <= 5:

        return (
            st.session_state["pesquisa_0 a 5 p.p."],
            "0 a 5 p.p."
        )

    elif gap < 10:

        return (
            st.session_state["pesquisa_5 a 10 p.p."],
            "5 a 10 p.p."
        )

    else:

        return (
            st.session_state["pesquisa_10 p.p. ou mais"],
            "10 p.p. ou mais"
        )


# ============================================================
# FUNÇÃO — APLICAR PESQUISA
# ============================================================

def aplicar_pesquisa(
    joao_atual,
    raquel_atual,
    pesquisa_joao,
    pesquisa_raquel
):

    # --------------------------------------------------------
    # Normaliza a pesquisa
    # --------------------------------------------------------

    pesquisa_joao, pesquisa_raquel = normalizar(
        pesquisa_joao,
        pesquisa_raquel
    )

    if pesquisa_joao is None:
        return None


    # --------------------------------------------------------
    # IDENTIFICA QUEM ESTÁ GANHANDO NA PESQUISA
    # --------------------------------------------------------

    if pesquisa_joao > pesquisa_raquel:

        lider = "João Campos"

        pct_lider_pesquisa = pesquisa_joao
        pct_lider_simulacao = joao_atual


    elif pesquisa_raquel > pesquisa_joao:

        lider = "Raquel Lyra"

        pct_lider_pesquisa = pesquisa_raquel
        pct_lider_simulacao = raquel_atual


    else:

        return {

            "lider": "Empate",

            "pesquisa_joao": pesquisa_joao,
            "pesquisa_raquel": pesquisa_raquel,

            "pct_lider_pesquisa": 0.0,
            "pct_lider_simulacao": 0.0,

            "gap_bruto": 0.0,
            "gap": 0.0,

            "faixa": None,
            "fator": 0.0,

            "efeito": 0.0,

            "joao_final": joao_atual,
            "raquel_final": raquel_atual
        }


    # --------------------------------------------------------
    # GAP DA PESQUISA
    # --------------------------------------------------------

    gap_bruto = (
        pct_lider_pesquisa
        -
        pct_lider_simulacao
    )


    # --------------------------------------------------------
    # SE A PESQUISA FOR MENOR QUE A SIMULAÇÃO,
    # NÃO HÁ EFEITO
    # --------------------------------------------------------

    gap = max(
        gap_bruto,
        0.0
    )


    faixa = None
    fator = 0.0
    efeito = 0.0


    # --------------------------------------------------------
    # CALCULAR EFEITO
    # --------------------------------------------------------

    if gap > 0:

        fator, faixa = obter_fator_pesquisa(
            gap
        )

        efeito = (
            gap
            *
            fator
        )


    # --------------------------------------------------------
    # APLICAÇÃO AO CANDIDATO QUE GANHA A PESQUISA
    # --------------------------------------------------------

    if lider == "João Campos":

        joao_final = limitar(
            joao_atual
            +
            efeito
        )

        raquel_final = (
            100
            -
            joao_final
        )


    else:

        raquel_final = limitar(
            raquel_atual
            +
            efeito
        )

        joao_final = (
            100
            -
            raquel_final
        )


    return {

        "lider": lider,

        "pesquisa_joao": pesquisa_joao,
        "pesquisa_raquel": pesquisa_raquel,

        "pct_lider_pesquisa":
            pct_lider_pesquisa,

        "pct_lider_simulacao":
            pct_lider_simulacao,

        "gap_bruto":
            gap_bruto,

        "gap":
            gap,

        "faixa":
            faixa,

        "fator":
            fator,

        "efeito":
            efeito,

        "joao_final":
            joao_final,

        "raquel_final":
            raquel_final
    }


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def calcular_cenario(

    # Base 0 Pernambuco
    joao_estado,
    raquel_estado,

    # Base municipal
    esquerda_municipio,
    direita_municipio,

    # Prefeito
    usar_prefeito,
    pct_prefeito,
    lado_prefeito,

    # Empenho
    usar_empenho,
    fator_empenho,

    # Avaliação
    usar_avaliacao,
    fator_avaliacao,

    # Lula
    usar_lula,
    pct_lula,
    fator_lula,

    # Pesquisa
    usar_pesquisa,
    abrangencia_pesquisa,
    pesquisa_joao,
    pesquisa_raquel
):


    # ========================================================
    # 1. BASE 0 — PERNAMBUCO
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

    joao_inicial, raquel_inicial = normalizar(
        esquerda_municipio,
        direita_municipio
    )

    if joao_inicial is None:
        return None


    # ========================================================
    # 3. DIFERENÇA MUNICIPAL EM RELAÇÃO AO ESTADO
    # ========================================================

    diferenca_base_joao = (
        joao_inicial
        -
        joao_estado
    )

    diferenca_base_raquel = (
        raquel_inicial
        -
        raquel_estado
    )


    # ========================================================
    # 4. PREFEITO
    # ========================================================

    joao_apos_prefeito = joao_inicial
    raquel_apos_prefeito = raquel_inicial


    candidato_apoiado = None

    base_candidato_apoiado = 0.0

    gap_prefeito_bruto = 0.0
    gap_prefeito = 0.0

    efeito_empenho = 0.0
    efeito_avaliacao = 0.0

    gap_restante = 0.0

    efeito_prefeito = 0.0


    if usar_prefeito:


        # ----------------------------------------------------
        # CANDIDATO APOIADO
        # ----------------------------------------------------

        if lado_prefeito == "Esquerda — João Campos":

            candidato_apoiado = "João Campos"

            base_candidato_apoiado = (
                joao_inicial
            )

        else:

            candidato_apoiado = "Raquel Lyra"

            base_candidato_apoiado = (
                raquel_inicial
            )


        # ----------------------------------------------------
        # GAP DO PREFEITO
        # ----------------------------------------------------

        gap_prefeito_bruto = (
            pct_prefeito
            -
            base_candidato_apoiado
        )


        # Gap negativo não entra
        gap_prefeito = max(
            gap_prefeito_bruto,
            0.0
        )


        # ----------------------------------------------------
        # EMPENHO
        # ----------------------------------------------------

        if usar_empenho:

            efeito_empenho = (
                gap_prefeito
                *
                fator_empenho
            )


        # ----------------------------------------------------
        # GAP RESTANTE
        # ----------------------------------------------------

        gap_restante = max(
            gap_prefeito
            -
            efeito_empenho,
            0.0
        )


        # ----------------------------------------------------
        # AVALIAÇÃO
        # ----------------------------------------------------

        if usar_avaliacao:

            efeito_avaliacao = (
                gap_restante
                *
                fator_avaliacao
            )


        # ----------------------------------------------------
        # EFEITO TOTAL DO PREFEITO
        # ----------------------------------------------------

        efeito_prefeito = (
            efeito_empenho
            +
            efeito_avaliacao
        )


        # ----------------------------------------------------
        # APLICAÇÃO
        # ----------------------------------------------------

        if candidato_apoiado == "João Campos":

            joao_apos_prefeito = limitar(
                joao_inicial
                +
                efeito_prefeito
            )

            raquel_apos_prefeito = (
                100
                -
                joao_apos_prefeito
            )


        else:

            raquel_apos_prefeito = limitar(
                raquel_inicial
                +
                efeito_prefeito
            )

            joao_apos_prefeito = (
                100
                -
                raquel_apos_prefeito
            )


    # ========================================================
    # 5. LULA
    # ========================================================

    gap_lula_bruto = 0.0
    gap_lula = 0.0

    efeito_lula = 0.0


    if usar_lula:


        # ----------------------------------------------------
        # GAP:
        # Lula - esquerda após prefeito
        # ----------------------------------------------------

        gap_lula_bruto = (
            pct_lula
            -
            joao_apos_prefeito
        )


        # Gap negativo não entra
        gap_lula = max(
            gap_lula_bruto,
            0.0
        )


        efeito_lula = (
            gap_lula
            *
            fator_lula
        )


    # ========================================================
    # 6. RESULTADO APÓS LULA
    # ========================================================

    joao_apos_lula = limitar(
        joao_apos_prefeito
        +
        efeito_lula
    )


    raquel_apos_lula = (
        100
        -
        joao_apos_lula
    )


    # ========================================================
    # 7. PESQUISA MUNICIPAL
    # ========================================================

    resultado_pesquisa_municipal = None


    joao_final_municipio = (
        joao_apos_lula
    )

    raquel_final_municipio = (
        raquel_apos_lula
    )


    if (
        usar_pesquisa
        and abrangencia_pesquisa == "Município"
    ):


        resultado_pesquisa_municipal = aplicar_pesquisa(

            joao_atual=
                joao_apos_lula,

            raquel_atual=
                raquel_apos_lula,

            pesquisa_joao=
                pesquisa_joao,

            pesquisa_raquel=
                pesquisa_raquel
        )


        if resultado_pesquisa_municipal is not None:

            joao_final_municipio = (
                resultado_pesquisa_municipal[
                    "joao_final"
                ]
            )

            raquel_final_municipio = (
                resultado_pesquisa_municipal[
                    "raquel_final"
                ]
            )


    # ========================================================
    # 8. VARIAÇÃO TOTAL NO MUNICÍPIO
    # ========================================================

    variacao_municipal_joao = (
        joao_final_municipio
        -
        joao_inicial
    )


    variacao_municipal_raquel = (
        raquel_final_municipio
        -
        raquel_inicial
    )


    # ========================================================
    # 9. CENÁRIO ESTADUAL
    #
    # Mantemos a Base 0 de Pernambuco como ponto de partida.
    # ========================================================

    joao_estado_antes_pesquisa = (
        joao_estado
    )

    raquel_estado_antes_pesquisa = (
        raquel_estado
    )


    # ========================================================
    # 10. PESQUISA REGIONAL
    # ========================================================

    resultado_pesquisa_regional = None


    if (
        usar_pesquisa
        and abrangencia_pesquisa == "Região"
    ):


        resultado_pesquisa_regional = aplicar_pesquisa(

            joao_atual=
                joao_estado_antes_pesquisa,

            raquel_atual=
                raquel_estado_antes_pesquisa,

            pesquisa_joao=
                pesquisa_joao,

            pesquisa_raquel=
                pesquisa_raquel
        )


    # ========================================================
    # 11. PESQUISA ESTADUAL
    # ========================================================

    resultado_pesquisa_estadual = None


    joao_estado_final = (
        joao_estado_antes_pesquisa
    )

    raquel_estado_final = (
        raquel_estado_antes_pesquisa
    )


    if (
        usar_pesquisa
        and abrangencia_pesquisa == "Estado"
    ):


        resultado_pesquisa_estadual = aplicar_pesquisa(

            joao_atual=
                joao_estado_antes_pesquisa,

            raquel_atual=
                raquel_estado_antes_pesquisa,

            pesquisa_joao=
                pesquisa_joao,

            pesquisa_raquel=
                pesquisa_raquel
        )


        if resultado_pesquisa_estadual is not None:

            joao_estado_final = (
                resultado_pesquisa_estadual[
                    "joao_final"
                ]
            )

            raquel_estado_final = (
                resultado_pesquisa_estadual[
                    "raquel_final"
                ]
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
        "joao_inicial":
            joao_inicial,

        "raquel_inicial":
            raquel_inicial,

        "diferenca_base_joao":
            diferenca_base_joao,

        "diferenca_base_raquel":
            diferenca_base_raquel,

        # Prefeito
        "usar_prefeito":
            usar_prefeito,

        "candidato_apoiado":
            candidato_apoiado,

        "pct_prefeito":
            pct_prefeito,

        "base_candidato_apoiado":
            base_candidato_apoiado,

        "gap_prefeito_bruto":
            gap_prefeito_bruto,

        "gap_prefeito":
            gap_prefeito,

        "efeito_empenho":
            efeito_empenho,

        "gap_restante":
            gap_restante,

        "efeito_avaliacao":
            efeito_avaliacao,

        "efeito_prefeito":
            efeito_prefeito,

        "joao_apos_prefeito":
            joao_apos_prefeito,

        "raquel_apos_prefeito":
            raquel_apos_prefeito,

        # Lula
        "usar_lula":
            usar_lula,

        "pct_lula":
            pct_lula,

        "gap_lula_bruto":
            gap_lula_bruto,

        "gap_lula":
            gap_lula,

        "fator_lula":
            fator_lula,

        "efeito_lula":
            efeito_lula,

        "joao_apos_lula":
            joao_apos_lula,

        "raquel_apos_lula":
            raquel_apos_lula,

        # Pesquisa
        "usar_pesquisa":
            usar_pesquisa,

        "abrangencia_pesquisa":
            abrangencia_pesquisa,

        "pesquisa_joao":
            pesquisa_joao,

        "pesquisa_raquel":
            pesquisa_raquel,

        "resultado_pesquisa_municipal":
            resultado_pesquisa_municipal,

        "resultado_pesquisa_regional":
            resultado_pesquisa_regional,

        "resultado_pesquisa_estadual":
            resultado_pesquisa_estadual,

        # Município final
        "joao_final_municipio":
            joao_final_municipio,

        "raquel_final_municipio":
            raquel_final_municipio,

        "variacao_municipal_joao":
            variacao_municipal_joao,

        "variacao_municipal_raquel":
            variacao_municipal_raquel,

        # Estado
        "joao_estado_antes_pesquisa":
            joao_estado_antes_pesquisa,

        "raquel_estado_antes_pesquisa":
            raquel_estado_antes_pesquisa,

        "joao_estado_final":
            joao_estado_final,

        "raquel_estado_final":
            raquel_estado_final
    }


# ============================================================
# ABAS
# ============================================================

aba_simulador, aba_parametros = st.tabs(
    [
        "Simulador",
        "Configurar parâmetros"
    ]
)


# ============================================================
# ABA — SIMULADOR
# ============================================================

with aba_simulador:


    # ========================================================
    # BASE 0 — PERNAMBUCO
    # ========================================================

    st.header("Base 0 — Pernambuco")

    st.caption(
        "Cenário estadual de referência."
    )


    c1, c2 = st.columns(2)


    with c1:

        joao_estado = st.number_input(
            "João Campos — Estado (%)",
            min_value=0.0,
            max_value=100.0,
            value=56.0,
            step=0.1
        )


    with c2:

        raquel_estado = st.number_input(
            "Raquel Lyra — Estado (%)",
            min_value=0.0,
            max_value=100.0,
            value=44.0,
            step=0.1
        )


    # ========================================================
    # BASE MUNICIPAL
    # ========================================================

    st.divider()

    st.header("Base do município")


    c1, c2 = st.columns(2)


    with c1:

        esquerda_municipio = st.number_input(
            "Esquerda no município (%)",
            min_value=0.0,
            max_value=100.0,
            value=67.0,
            step=0.1
        )


    with c2:

        direita_municipio = st.number_input(
            "Direita no município (%)",
            min_value=0.0,
            max_value=100.0,
            value=33.0,
            step=0.1
        )


    # ========================================================
    # PREFEITO
    # ========================================================

    st.divider()

    st.header("Prefeito")


    usar_prefeito = st.toggle(
        "Incluir efeito do prefeito",
        value=True
    )


    pct_prefeito = 0.0
    lado_prefeito = "Direita — Raquel Lyra"

    usar_empenho = False
    usar_avaliacao = False

    fator_empenho = 0.0
    fator_avaliacao = 0.0

    categoria_empenho = "Muito fraco"
    categoria_avaliacao = "Muito fraco"


    if usar_prefeito:


        c1, c2 = st.columns(2)


        with c1:

            pct_prefeito = st.number_input(
                "Votação do prefeito (%)",
                min_value=0.0,
                max_value=100.0,
                value=56.0,
                step=0.1
            )


        with c2:

            lado_prefeito = st.selectbox(
                "Quem o prefeito apoia?",
                [
                    "Esquerda — João Campos",
                    "Direita — Raquel Lyra"
                ],
                index=1
            )


        c1, c2 = st.columns(2)


        # ----------------------------------------------------
        # EMPENHO
        # ----------------------------------------------------

        with c1:

            st.subheader("Empenho")

            usar_empenho = st.toggle(
                "Usar empenho",
                value=True
            )


            if usar_empenho:

                categoria_empenho = st.selectbox(
                    "Nível de empenho",
                    CATEGORIAS,
                    index=3
                )


                fator_empenho = st.session_state[
                    f"param_empenho_{categoria_empenho}"
                ]


                st.metric(
                    "Fator utilizado",
                    f"{fator_empenho:.2f}"
                )


        # ----------------------------------------------------
        # AVALIAÇÃO
        # ----------------------------------------------------

        with c2:

            st.subheader("Avaliação")

            usar_avaliacao = st.toggle(
                "Usar avaliação",
                value=True
            )


            if usar_avaliacao:

                categoria_avaliacao = st.selectbox(
                    "Nível de avaliação",
                    CATEGORIAS,
                    index=4
                )


                fator_avaliacao = st.session_state[
                    f"param_avaliacao_{categoria_avaliacao}"
                ]


                st.metric(
                    "Fator utilizado",
                    f"{fator_avaliacao:.2f}"
                )


    # ========================================================
    # LULA
    # ========================================================

    st.divider()

    st.header("Lula")


    usar_lula = st.toggle(
        "Incluir efeito de Lula",
        value=True
    )


    pct_lula = 0.0
    fator_lula = 0.0

    categoria_lula = "Muito fraco"


    if usar_lula:


        c1, c2 = st.columns(2)


        with c1:

            pct_lula = st.number_input(
                "Votação de Lula no município (%)",
                min_value=0.0,
                max_value=100.0,
                value=86.0,
                step=0.1
            )


        with c2:

            categoria_lula = st.selectbox(
                "Intensidade do efeito de Lula",
                CATEGORIAS,
                index=0
            )


            fator_lula = st.session_state[
                f"param_lula_{categoria_lula}"
            ]


            st.metric(
                "Fator utilizado",
                f"{fator_lula:.2f}"
            )


        st.caption(
            "O gap de Lula é calculado automaticamente: "
            "votação de Lula menos o resultado de João "
            "após o efeito do prefeito."
        )


    # ========================================================
    # PESQUISA
    # ========================================================

    st.divider()

    st.header("Pesquisa")


    usar_pesquisa = st.toggle(
        "Incluir efeito da pesquisa",
        value=True
    )


    abrangencia_pesquisa = "Município"

    pesquisa_joao = 65.0
    pesquisa_raquel = 35.0


    if usar_pesquisa:


        abrangencia_pesquisa = st.selectbox(
            "Abrangência da pesquisa",
            [
                "Município",
                "Região",
                "Estado"
            ]
        )


        c1, c2 = st.columns(2)


        with c1:

            pesquisa_joao = st.number_input(
                "João Campos — Pesquisa (%)",
                min_value=0.0,
                max_value=100.0,
                value=65.0,
                step=0.1
            )


        with c2:

            pesquisa_raquel = st.number_input(
                "Raquel Lyra — Pesquisa (%)",
                min_value=0.0,
                max_value=100.0,
                value=35.0,
                step=0.1
            )


        if abrangencia_pesquisa == "Município":

            st.info(
                "A pesquisa será aplicada ao cenário municipal "
                "depois dos efeitos de prefeito e Lula."
            )


        elif abrangencia_pesquisa == "Região":

            st.info(
                "A pesquisa será tratada como uma pesquisa regional."
            )


        else:

            st.info(
                "A pesquisa será aplicada diretamente ao cenário "
                "de Pernambuco."
            )


        st.caption(
            "O sistema identifica automaticamente quem está "
            "ganhando na pesquisa. O fator é aplicado somente "
            "ao gap positivo desse candidato."
        )


    # ========================================================
    # CALCULAR
    # ========================================================

    resultado = calcular_cenario(

        joao_estado=joao_estado,
        raquel_estado=raquel_estado,

        esquerda_municipio=esquerda_municipio,
        direita_municipio=direita_municipio,

        usar_prefeito=usar_prefeito,

        pct_prefeito=pct_prefeito,

        lado_prefeito=lado_prefeito,

        usar_empenho=usar_empenho,

        fator_empenho=fator_empenho,

        usar_avaliacao=usar_avaliacao,

        fator_avaliacao=fator_avaliacao,

        usar_lula=usar_lula,

        pct_lula=pct_lula,

        fator_lula=fator_lula,

        usar_pesquisa=usar_pesquisa,

        abrangencia_pesquisa=
            abrangencia_pesquisa,

        pesquisa_joao=pesquisa_joao,

        pesquisa_raquel=pesquisa_raquel
    )


    # ========================================================
    # RESULTADO
    # ========================================================

    st.divider()

    st.header("Resultado projetado")


    if resultado is None:

        st.error(
            "Não foi possível calcular o cenário."
        )


    else:


        # ====================================================
        # RESULTADO MUNICIPAL
        # ====================================================

        st.subheader("Resultado no município")


        c1, c2 = st.columns(2)


        with c1:

            st.metric(
                "João Campos",
                f"{resultado['joao_final_municipio']:.2f}%"
            )


        with c2:

            st.metric(
                "Raquel Lyra",
                f"{resultado['raquel_final_municipio']:.2f}%"
            )


        st.progress(
            resultado["joao_final_municipio"] / 100,

            text=(
                f"João "
                f"{resultado['joao_final_municipio']:.1f}% "
                f"× Raquel "
                f"{resultado['raquel_final_municipio']:.1f}%"
            )
        )


        # ====================================================
        # EVOLUÇÃO
        # ====================================================

        st.subheader("Evolução do cenário municipal")


        e1, e2, e3, e4 = st.columns(4)


        e1.metric(
            "Ponto de partida",
            f"{resultado['joao_inicial']:.2f}%"
        )


        e2.metric(
            "Após prefeito",
            f"{resultado['joao_apos_prefeito']:.2f}%"
        )


        e3.metric(
            "Após Lula",
            f"{resultado['joao_apos_lula']:.2f}%"
        )


        e4.metric(
            "Após pesquisa",
            f"{resultado['joao_final_municipio']:.2f}%"
        )


        # ====================================================
        # EFEITOS
        # ====================================================

        st.subheader("Efeitos considerados")


        efeito_prefeito_joao = (
            resultado["joao_apos_prefeito"]
            -
            resultado["joao_inicial"]
        )


        efeito_pesquisa_joao = (
            resultado["joao_final_municipio"]
            -
            resultado["joao_apos_lula"]
        )


        c1, c2, c3, c4 = st.columns(4)


        c1.metric(
            "Base",
            f"{resultado['joao_inicial']:.2f}%"
        )


        c2.metric(
            "Prefeito",
            f"{efeito_prefeito_joao:+.2f} p.p."
        )


        c3.metric(
            "Lula",
            f"{resultado['efeito_lula']:+.2f} p.p."
        )


        c4.metric(
            "Pesquisa",
            f"{efeito_pesquisa_joao:+.2f} p.p."
        )


        # ====================================================
        # RESULTADO DE PERNAMBUCO
        # ====================================================

        st.divider()

        st.subheader("Cenário de Pernambuco")


        c1, c2 = st.columns(2)


        with c1:

            st.metric(
                "João Campos",
                f"{resultado['joao_estado_final']:.2f}%"
            )


        with c2:

            st.metric(
                "Raquel Lyra",
                f"{resultado['raquel_estado_final']:.2f}%"
            )


        st.progress(
            resultado["joao_estado_final"] / 100,

            text=(
                f"João "
                f"{resultado['joao_estado_final']:.1f}% "
                f"× Raquel "
                f"{resultado['raquel_estado_final']:.1f}%"
            )
        )


        # ====================================================
        # MEMÓRIA DE CÁLCULO
        # ====================================================

        st.divider()

        st.header("Memória de cálculo")


        # ====================================================
        # BASE
        # ====================================================

        with st.expander(
            "1. Ponto de partida",
            expanded=False
        ):


            st.write(
                f"Base 0 Pernambuco: "
                f"**João {resultado['joao_estado']:.2f}% × "
                f"Raquel {resultado['raquel_estado']:.2f}%**"
            )


            st.write(
                f"Base municipal: "
                f"**Esquerda {resultado['joao_inicial']:.2f}% × "
                f"Direita {resultado['raquel_inicial']:.2f}%**"
            )


            st.write(
                f"Diferença da esquerda no município em relação "
                f"ao Estado: "
                f"**{resultado['diferenca_base_joao']:+.2f} p.p.**"
            )


        # ====================================================
        # PREFEITO
        # ====================================================

        with st.expander(
            "2. Prefeito",
            expanded=False
        ):


            if not resultado["usar_prefeito"]:

                st.info(
                    "O efeito do prefeito não foi utilizado."
                )


            else:


                st.write(
                    f"Apoio: "
                    f"**{resultado['candidato_apoiado']}**"
                )


                st.write(
                    f"Votação do prefeito: "
                    f"**{resultado['pct_prefeito']:.2f}%**"
                )


                st.write(
                    f"Base do candidato apoiado: "
                    f"**{resultado['base_candidato_apoiado']:.2f}%**"
                )


                st.code(
                    f"{resultado['pct_prefeito']:.2f} "
                    f"- "
                    f"{resultado['base_candidato_apoiado']:.2f} "
                    f"= "
                    f"{resultado['gap_prefeito_bruto']:.2f} p.p."
                )


                st.write(
                    f"Gap positivo disponível: "
                    f"**{resultado['gap_prefeito']:.2f} p.p.**"
                )


                # --------------------------------------------
                # EMPENHO
                # --------------------------------------------

                if usar_empenho:

                    st.write(
                        f"Empenho: "
                        f"**{categoria_empenho} "
                        f"({fator_empenho:.2f})**"
                    )


                    st.code(
                        f"{resultado['gap_prefeito']:.2f} "
                        f"× "
                        f"{fator_empenho:.2f} "
                        f"= "
                        f"{resultado['efeito_empenho']:.2f} p.p."
                    )


                # --------------------------------------------
                # AVALIAÇÃO
                # --------------------------------------------

                if usar_avaliacao:

                    st.write(
                        f"Gap restante: "
                        f"**{resultado['gap_restante']:.2f} p.p.**"
                    )


                    st.write(
                        f"Avaliação: "
                        f"**{categoria_avaliacao} "
                        f"({fator_avaliacao:.2f})**"
                    )


                    st.code(
                        f"{resultado['gap_restante']:.2f} "
                        f"× "
                        f"{fator_avaliacao:.2f} "
                        f"= "
                        f"{resultado['efeito_avaliacao']:.2f} p.p."
                    )


                st.success(
                    f"Efeito total do prefeito: "
                    f"{resultado['efeito_prefeito']:.2f} p.p. "
                    f"para {resultado['candidato_apoiado']}."
                )


                st.write(
                    f"Resultado após prefeito: "
                    f"**João "
                    f"{resultado['joao_apos_prefeito']:.2f}% × "
                    f"Raquel "
                    f"{resultado['raquel_apos_prefeito']:.2f}%**"
                )


        # ====================================================
        # LULA
        # ====================================================

        with st.expander(
            "3. Lula",
            expanded=False
        ):


            if not resultado["usar_lula"]:

                st.info(
                    "O efeito de Lula não foi utilizado."
                )


            else:


                st.write(
                    f"Lula no município: "
                    f"**{resultado['pct_lula']:.2f}%**"
                )


                st.write(
                    f"João antes de Lula: "
                    f"**{resultado['joao_apos_prefeito']:.2f}%**"
                )


                st.code(
                    f"{resultado['pct_lula']:.2f} "
                    f"- "
                    f"{resultado['joao_apos_prefeito']:.2f} "
                    f"= "
                    f"{resultado['gap_lula_bruto']:.2f} p.p."
                )


                if resultado["gap_lula"] <= 0:

                    st.info(
                        "O gap é zero ou negativo. "
                        "Lula não produz efeito."
                    )


                else:

                    st.write(
                        f"Gap positivo: "
                        f"**{resultado['gap_lula']:.2f} p.p.**"
                    )


                    st.write(
                        f"Intensidade: "
                        f"**{categoria_lula} "
                        f"({fator_lula:.2f})**"
                    )


                    st.code(
                        f"{resultado['gap_lula']:.2f} "
                        f"× "
                        f"{fator_lula:.2f} "
                        f"= "
                        f"{resultado['efeito_lula']:.2f} p.p."
                    )


                    st.success(
                        f"Efeito de Lula sobre João: "
                        f"+{resultado['efeito_lula']:.2f} p.p."
                    )


                st.write(
                    f"Resultado após Lula: "
                    f"**João "
                    f"{resultado['joao_apos_lula']:.2f}% × "
                    f"Raquel "
                    f"{resultado['raquel_apos_lula']:.2f}%**"
                )


        # ====================================================
        # PESQUISA
        # ====================================================

        with st.expander(
            "4. Pesquisa",
            expanded=True
        ):


            if not resultado["usar_pesquisa"]:

                st.info(
                    "O efeito da pesquisa não foi utilizado."
                )


            else:


                st.write(
                    f"Abrangência: "
                    f"**{resultado['abrangencia_pesquisa']}**"
                )


                st.write(
                    f"Pesquisa: "
                    f"**João {pesquisa_joao:.2f}% × "
                    f"Raquel {pesquisa_raquel:.2f}%**"
                )


                # --------------------------------------------
                # SELECIONAR A PESQUISA CORRETA
                # --------------------------------------------

                if abrangencia_pesquisa == "Município":

                    rp = resultado[
                        "resultado_pesquisa_municipal"
                    ]


                elif abrangencia_pesquisa == "Região":

                    rp = resultado[
                        "resultado_pesquisa_regional"
                    ]


                else:

                    rp = resultado[
                        "resultado_pesquisa_estadual"
                    ]


                if rp is not None:


                    # ----------------------------------------
                    # EMPATE
                    # ----------------------------------------

                    if rp["lider"] == "Empate":

                        st.info(
                            "A pesquisa está empatada. "
                            "Nenhum candidato recebe efeito."
                        )


                    # ----------------------------------------
                    # TEM VENCEDOR
                    # ----------------------------------------

                    else:


                        st.write(
                            f"Candidato que lidera a pesquisa: "
                            f"**{rp['lider']}**"
                        )


                        st.write(
                            f"{rp['lider']} na pesquisa: "
                            f"**{rp['pct_lider_pesquisa']:.2f}%**"
                        )


                        st.write(
                            f"{rp['lider']} na simulação antes "
                            f"da pesquisa: "
                            f"**{rp['pct_lider_simulacao']:.2f}%**"
                        )


                        st.code(
                            f"{rp['pct_lider_pesquisa']:.2f} "
                            f"- "
                            f"{rp['pct_lider_simulacao']:.2f} "
                            f"= "
                            f"{rp['gap_bruto']:.2f} p.p."
                        )


                        # ------------------------------------
                        # SEM EFEITO
                        # ------------------------------------

                        if rp["gap"] <= 0:

                            st.info(
                                f"{rp['lider']} já possui na "
                                f"simulação um percentual igual ou "
                                f"superior ao resultado da pesquisa. "
                                f"Portanto, a pesquisa não produz efeito."
                            )


                        # ------------------------------------
                        # COM EFEITO
                        # ------------------------------------

                        else:


                            st.write(
                                f"Gap positivo: "
                                f"**{rp['gap']:.2f} p.p.**"
                            )


                            st.write(
                                f"Faixa: "
                                f"**{rp['faixa']}**"
                            )


                            st.write(
                                f"Fator: "
                                f"**{rp['fator']:.2f}**"
                            )


                            st.code(
                                f"{rp['gap']:.2f} "
                                f"× "
                                f"{rp['fator']:.2f} "
                                f"= "
                                f"{rp['efeito']:.2f} p.p."
                            )


                            st.success(
                                f"A pesquisa acrescenta "
                                f"{rp['efeito']:.2f} p.p. "
                                f"a {rp['lider']}."
                            )


                            st.write(
                                f"Resultado após a pesquisa: "
                                f"**João "
                                f"{rp['joao_final']:.2f}% × "
                                f"Raquel "
                                f"{rp['raquel_final']:.2f}%**"
                            )


# ============================================================
# ABA — CONFIGURAR PARÂMETROS
# ============================================================

with aba_parametros:


    st.header("Configurar parâmetros")

    st.caption(
        "Os valores são sugestões iniciais. "
        "Cada parâmetro pode ser alterado separadamente."
    )


    # ========================================================
    # FUNÇÃO DO EDITOR
    # ========================================================

    def editor_parametros(
        titulo,
        variavel,
        descricao
    ):


        st.subheader(titulo)

        st.caption(descricao)


        colunas = st.columns(5)


        for i, categoria in enumerate(CATEGORIAS):


            with colunas[i]:

                st.markdown(
                    f"**{categoria}**"
                )


                st.number_input(
                    f"{titulo} - {categoria}",
                    min_value=0.0,
                    max_value=10.0,
                    step=0.05,
                    format="%.2f",
                    key=f"param_{variavel}_{categoria}",
                    label_visibility="collapsed"
                )


    # ========================================================
    # EMPENHO
    # ========================================================

    editor_parametros(
        "Empenho do prefeito",
        "empenho",
        "Fator aplicado ao gap disponível do prefeito."
    )


    st.divider()


    # ========================================================
    # AVALIAÇÃO
    # ========================================================

    editor_parametros(
        "Avaliação do prefeito",
        "avaliacao",
        "Fator aplicado ao gap restante depois do empenho."
    )


    st.divider()


    # ========================================================
    # LULA
    # ========================================================

    editor_parametros(
        "Efeito de Lula",
        "lula",
        "Fator aplicado ao gap positivo entre Lula e João."
    )


    st.divider()


    # ========================================================
    # PESQUISA
    # ========================================================

    st.subheader("Efeito da pesquisa")

    st.caption(
        "O fator é aplicado ao gap positivo do candidato "
        "que estiver ganhando na pesquisa."
    )


    p1, p2, p3 = st.columns(3)


    with p1:

        st.markdown(
            "**0 a 5 p.p.**"
        )

        st.number_input(
            "Pesquisa 0–5",
            min_value=0.0,
            max_value=10.0,
            step=0.05,
            format="%.2f",
            key="pesquisa_0 a 5 p.p.",
            label_visibility="collapsed"
        )


    with p2:

        st.markdown(
            "**5 a 10 p.p.**"
        )

        st.number_input(
            "Pesquisa 5–10",
            min_value=0.0,
            max_value=10.0,
            step=0.05,
            format="%.2f",
            key="pesquisa_5 a 10 p.p.",
            label_visibility="collapsed"
        )


    with p3:

        st.markdown(
            "**10 p.p. ou mais**"
        )

        st.number_input(
            "Pesquisa 10+",
            min_value=0.0,
            max_value=10.0,
            step=0.05,
            format="%.2f",
            key="pesquisa_10 p.p. ou mais",
            label_visibility="collapsed"
        )


    st.caption(
        "Sugestão atual: 0,20 em todas as faixas."
    )


    # ========================================================
    # RESTAURAR
    # ========================================================

    st.divider()


    if st.button(
        "Restaurar valores sugeridos"
    ):


        for variavel, escala in PARAMETROS_PADRAO.items():

            for categoria, valor in escala.items():

                st.session_state[
                    f"param_{variavel}_{categoria}"
                ] = valor


        for faixa, valor in PARAMETROS_PESQUISA.items():

            st.session_state[
                f"pesquisa_{faixa}"
            ] = valor


        st.rerun()
