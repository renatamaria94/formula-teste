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
# PARÂMETROS SUGERIDOS
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
# FUNÇÃO: APLICAR PESQUISA
# ============================================================

def aplicar_pesquisa(
    joao_atual,
    raquel_atual,
    pesquisa_joao,
    pesquisa_raquel
):

    pesquisa_joao, pesquisa_raquel = normalizar(
        pesquisa_joao,
        pesquisa_raquel
    )

    if pesquisa_joao is None:
        return None


    # --------------------------------------------------------
    # IDENTIFICAR QUEM GANHA A PESQUISA
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


    # ========================================================
    # REGRA:
    #
    # Pesquisa menor ou igual ao percentual já simulado
    # para o candidato vencedor -> efeito zero.
    # ========================================================

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
            gap *
            fator
        )


    # --------------------------------------------------------
    # APLICAR AO VENCEDOR DA PESQUISA
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

        "gap_bruto": gap_bruto,
        "gap": gap,

        "faixa": faixa,
        "fator": fator,

        "efeito": efeito,

        "joao_final": joao_final,
        "raquel_final": raquel_final
    }


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def calcular_cenario(

    # Pernambuco
    joao_estado,
    raquel_estado,

    # Município
    esquerda_municipio,
    direita_municipio,

    votos_validos_municipio,
    votos_validos_estado,

    # Prefeito
    usar_prefeito,
    pct_prefeito,
    lado_prefeito,

    usar_empenho,
    fator_empenho,

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
    pesquisa_raquel,

    votos_validos_regiao
):


    # ========================================================
    # 1. BASE 0 — PERNAMBUCO
    # ========================================================

    joao_estado, raquel_estado = normalizar(
        joao_estado,
        raquel_estado
    )


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
    # 3. PESOS AUTOMÁTICOS
    # ========================================================

    if votos_validos_estado > 0:

        peso_municipio = (
            votos_validos_municipio
            /
            votos_validos_estado
        )

        peso_regiao = (
            votos_validos_regiao
            /
            votos_validos_estado
        )

    else:

        peso_municipio = 0.0
        peso_regiao = 0.0


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
        # QUEM O PREFEITO APOIA
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
        # EFEITO TOTAL
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
        # Lula - esquerda após prefeito
        # ----------------------------------------------------

        gap_lula_bruto = (
            pct_lula
            -
            joao_apos_prefeito
        )


        # ----------------------------------------------------
        # Gap negativo não entra
        # ----------------------------------------------------

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


    joao_final_municipio = joao_apos_lula
    raquel_final_municipio = raquel_apos_lula


    if (
        usar_pesquisa
        and abrangencia_pesquisa == "Município"
    ):

        resultado_pesquisa_municipal = aplicar_pesquisa(

            joao_atual=joao_apos_lula,
            raquel_atual=raquel_apos_lula,

            pesquisa_joao=pesquisa_joao,
            pesquisa_raquel=pesquisa_raquel
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
    # 8. VARIAÇÃO MUNICIPAL
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
    # 9. IMPACTO DO MUNICÍPIO SOBRE PERNAMBUCO
    # ========================================================

    impacto_municipio_estado_joao = (
        variacao_municipal_joao
        *
        peso_municipio
    )


    joao_estado_apos_municipio = limitar(
        joao_estado
        +
        impacto_municipio_estado_joao
    )


    raquel_estado_apos_municipio = (
        100
        -
        joao_estado_apos_municipio
    )


    # ========================================================
    # 10. ESTADO ANTES DE PESQUISA REGIONAL/ESTADUAL
    # ========================================================

    joao_estado_final = (
        joao_estado_apos_municipio
    )

    raquel_estado_final = (
        raquel_estado_apos_municipio
    )


    resultado_pesquisa_regional = None
    resultado_pesquisa_estadual = None

    impacto_pesquisa_estado = 0.0


    # ========================================================
    # 11. PESQUISA REGIONAL
    # ========================================================

    if (
        usar_pesquisa
        and abrangencia_pesquisa == "Região"
    ):


        resultado_pesquisa_regional = aplicar_pesquisa(

            joao_atual=joao_estado_apos_municipio,

            raquel_atual=raquel_estado_apos_municipio,

            pesquisa_joao=pesquisa_joao,

            pesquisa_raquel=pesquisa_raquel
        )


        if resultado_pesquisa_regional is not None:


            # ------------------------------------------------
            # Diferença produzida pela pesquisa
            # ------------------------------------------------

            diferenca_regional_joao = (

                resultado_pesquisa_regional[
                    "joao_final"
                ]

                -

                joao_estado_apos_municipio
            )


            # ------------------------------------------------
            # Ponderação pelo tamanho da região
            # ------------------------------------------------

            impacto_pesquisa_estado = (
                diferenca_regional_joao
                *
                peso_regiao
            )


            joao_estado_final = limitar(
                joao_estado_apos_municipio
                +
                impacto_pesquisa_estado
            )


            raquel_estado_final = (
                100
                -
                joao_estado_final
            )


    # ========================================================
    # 12. PESQUISA ESTADUAL
    # ========================================================

    elif (
        usar_pesquisa
        and abrangencia_pesquisa == "Estado"
    ):


        resultado_pesquisa_estadual = aplicar_pesquisa(

            joao_atual=joao_estado_apos_municipio,

            raquel_atual=raquel_estado_apos_municipio,

            pesquisa_joao=pesquisa_joao,

            pesquisa_raquel=pesquisa_raquel
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


            impacto_pesquisa_estado = (

                joao_estado_final

                -

                joao_estado_apos_municipio
            )


    # ========================================================
    # 13. IMPACTO TOTAL NO ESTADO
    # ========================================================

    impacto_total_estado_joao = (
        joao_estado_final
        -
        joao_estado
    )


    impacto_total_estado_raquel = (
        -impacto_total_estado_joao
    )


    # ========================================================
    # RETORNO
    # ========================================================

    return {

        # ---------------- ESTADO ----------------

        "joao_estado":
            joao_estado,

        "raquel_estado":
            raquel_estado,

        # ---------------- MUNICÍPIO ----------------

        "joao_inicial":
            joao_inicial,

        "raquel_inicial":
            raquel_inicial,

        # ---------------- PESOS ----------------

        "peso_municipio":
            peso_municipio,

        "peso_municipio_pct":
            peso_municipio * 100,

        "peso_regiao":
            peso_regiao,

        "peso_regiao_pct":
            peso_regiao * 100,

        # ---------------- PREFEITO ----------------

        "usar_prefeito":
            usar_prefeito,

        "candidato_apoiado":
            candidato_apoiado,

        "base_candidato_apoiado":
            base_candidato_apoiado,

        "pct_prefeito":
            pct_prefeito,

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

        # ---------------- LULA ----------------

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

        # ---------------- PESQUISA ----------------

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

        # ---------------- FINAL MUNICÍPIO ----------------

        "joao_final_municipio":
            joao_final_municipio,

        "raquel_final_municipio":
            raquel_final_municipio,

        "variacao_municipal_joao":
            variacao_municipal_joao,

        "variacao_municipal_raquel":
            variacao_municipal_raquel,

        # ---------------- ESTADO ----------------

        "impacto_municipio_estado_joao":
            impacto_municipio_estado_joao,

        "joao_estado_apos_municipio":
            joao_estado_apos_municipio,

        "raquel_estado_apos_municipio":
            raquel_estado_apos_municipio,

        "impacto_pesquisa_estado":
            impacto_pesquisa_estado,

        "impacto_total_estado_joao":
            impacto_total_estado_joao,

        "impacto_total_estado_raquel":
            impacto_total_estado_raquel,

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
# ABA SIMULADOR
# ============================================================

with aba_simulador:


    # ========================================================
    # BASE 0
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
    # VOTOS VÁLIDOS
    # ========================================================

    st.subheader("Eleitorado")

    st.caption(
        "O sistema calcula automaticamente o peso eleitoral "
        "do município em Pernambuco."
    )


    c1, c2 = st.columns(2)


    with c1:

        votos_validos_municipio = st.number_input(
            "Votos válidos do município",
            min_value=0,
            value=18000,
            step=100
        )


    with c2:

        votos_validos_estado = st.number_input(
            "Votos válidos de Pernambuco",
            min_value=1,
            value=5000000,
            step=1000
        )


    peso_visual = (
        votos_validos_municipio
        /
        votos_validos_estado
        *
        100
    )


    st.caption(
        f"Peso eleitoral calculado: "
        f"**{peso_visual:.3f}%** de Pernambuco."
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
            "O gap de Lula é calculado automaticamente em relação "
            "ao resultado da esquerda após o efeito do prefeito."
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

    votos_validos_regiao = 0


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


        # ----------------------------------------------------
        # REGIÃO
        # ----------------------------------------------------

        if abrangencia_pesquisa == "Região":

            votos_validos_regiao = st.number_input(
                "Votos válidos da região",
                min_value=0,
                value=500000,
                step=1000
            )


            peso_regiao_visual = (
                votos_validos_regiao
                /
                votos_validos_estado
                *
                100
            )


            st.caption(
                f"Peso eleitoral da região: "
                f"**{peso_regiao_visual:.2f}%** de Pernambuco."
            )


        elif abrangencia_pesquisa == "Estado":

            st.info(
                "A pesquisa estadual atua diretamente "
                "sobre o cenário de Pernambuco."
            )


        else:

            st.info(
                "A pesquisa municipal é aplicada ao resultado "
                "do município depois de prefeito e Lula."
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

        votos_validos_municipio=
            votos_validos_municipio,

        votos_validos_estado=
            votos_validos_estado,

        usar_prefeito=
            usar_prefeito,

        pct_prefeito=
            pct_prefeito,

        lado_prefeito=
            lado_prefeito,

        usar_empenho=
            usar_empenho,

        fator_empenho=
            fator_empenho,

        usar_avaliacao=
            usar_avaliacao,

        fator_avaliacao=
            fator_avaliacao,

        usar_lula=
            usar_lula,

        pct_lula=
            pct_lula,

        fator_lula=
            fator_lula,

        usar_pesquisa=
            usar_pesquisa,

        abrangencia_pesquisa=
            abrangencia_pesquisa,

        pesquisa_joao=
            pesquisa_joao,

        pesquisa_raquel=
            pesquisa_raquel,

        votos_validos_regiao=
            votos_validos_regiao
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
        # MUNICÍPIO
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
                f"× "
                f"Raquel "
                f"{resultado['raquel_final_municipio']:.1f}%"
            )
        )


        # ====================================================
        # EVOLUÇÃO MUNICIPAL
        # ====================================================

        st.subheader("Evolução no município")


        e1, e2, e3, e4 = st.columns(4)


        e1.metric(
            "Base",
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
            "Final",
            f"{resultado['joao_final_municipio']:.2f}%"
        )


        # ====================================================
        # PERNAMBUCO
        # ====================================================

        st.divider()

        st.subheader("Resultado em Pernambuco")


        c1, c2 = st.columns(2)


        with c1:

            st.metric(
                "João Campos",
                f"{resultado['joao_estado_final']:.2f}%",

                delta=(
                    f"{resultado['impacto_total_estado_joao']:+.3f} p.p."
                )
            )


        with c2:

            st.metric(
                "Raquel Lyra",
                f"{resultado['raquel_estado_final']:.2f}%",

                delta=(
                    f"{resultado['impacto_total_estado_raquel']:+.3f} p.p."
                )
            )


        st.progress(
            resultado["joao_estado_final"] / 100,

            text=(
                f"João "
                f"{resultado['joao_estado_final']:.1f}% "
                f"× "
                f"Raquel "
                f"{resultado['raquel_estado_final']:.1f}%"
            )
        )


        # ====================================================
        # EFEITOS
        # ====================================================

        st.divider()

        st.header("Efeitos considerados")


        c1, c2, c3, c4 = st.columns(4)


        c1.metric(
            "Ponto de partida",
            f"{resultado['joao_inicial']:.2f}%"
        )


        # ----------------------------------------------------
        # PREFEITO
        # ----------------------------------------------------

        efeito_prefeito_joao = (
            resultado["joao_apos_prefeito"]
            -
            resultado["joao_inicial"]
        )


        c2.metric(
            "Efeito do prefeito",
            f"{efeito_prefeito_joao:+.2f} p.p."
        )


        # ----------------------------------------------------
        # LULA
        # ----------------------------------------------------

        c3.metric(
            "Efeito de Lula",
            f"{resultado['efeito_lula']:+.2f} p.p."
        )


        # ----------------------------------------------------
        # PESQUISA MUNICIPAL
        # ----------------------------------------------------

        efeito_pesquisa_exibicao = 0.0


        if (
            resultado["resultado_pesquisa_municipal"]
            is not None
        ):

            rp = resultado[
                "resultado_pesquisa_municipal"
            ]


            efeito_pesquisa_exibicao = (

                resultado["joao_final_municipio"]

                -

                resultado["joao_apos_lula"]
            )


        c4.metric(
            "Efeito da pesquisa",
            f"{efeito_pesquisa_exibicao:+.2f} p.p."
        )


        # ====================================================
        # MEMÓRIA DE CÁLCULO
        # ====================================================

        st.divider()

        st.header("Memória de cálculo")


        # ====================================================
        # 1. BASE
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


        # ====================================================
        # 2. PREFEITO
        # ====================================================

        with st.expander(
            "2. Prefeito",
            expanded=False
        ):


            if not resultado["usar_prefeito"]:

                st.info(
                    "Efeito do prefeito não utilizado."
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
        # 3. LULA
        # ====================================================

        with st.expander(
            "3. Lula",
            expanded=False
        ):


            if not resultado["usar_lula"]:

                st.info(
                    "Efeito de Lula não utilizado."
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


        # ====================================================
        # 4. PESQUISA
        # ====================================================

        with st.expander(
            "4. Pesquisa",
            expanded=True
        ):


            if not resultado["usar_pesquisa"]:

                st.info(
                    "Efeito da pesquisa não utilizado."
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
                # ESCOLHER RESULTADO DA PESQUISA
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


                    if rp["lider"] == "Empate":

                        st.info(
                            "A pesquisa está empatada. "
                            "Nenhum candidato recebe efeito."
                        )


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
                            f"{rp['lider']} antes da pesquisa: "
                            f"**{rp['pct_lider_simulacao']:.2f}%**"
                        )


                        st.code(
                            f"{rp['pct_lider_pesquisa']:.2f} "
                            f"- "
                            f"{rp['pct_lider_simulacao']:.2f} "
                            f"= "
                            f"{rp['gap_bruto']:.2f} p.p."
                        )


                        if rp["gap"] <= 0:

                            st.info(
                                f"{rp['lider']} já possui na simulação "
                                f"um percentual igual ou superior ao "
                                f"resultado da pesquisa. "
                                f"A pesquisa não produz efeito."
                            )


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
                                f"Fator da pesquisa: "
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


                            # --------------------------------
                            # EXEMPLO DO RESULTADO
                            # --------------------------------

                            if abrangencia_pesquisa == "Município":

                                st.write(
                                    f"Resultado após pesquisa: "
                                    f"**João "
                                    f"{resultado['joao_final_municipio']:.2f}% "
                                    f"× Raquel "
                                    f"{resultado['raquel_final_municipio']:.2f}%**"
                                )


        # ====================================================
        # 5. PERNAMBUCO
        # ====================================================

        with st.expander(
            "5. Impacto em Pernambuco",
            expanded=False
        ):


            st.write(
                f"Base 0: "
                f"**João {resultado['joao_estado']:.2f}% × "
                f"Raquel {resultado['raquel_estado']:.2f}%**"
            )


            st.write(
                f"Peso eleitoral calculado do município: "
                f"**{resultado['peso_municipio_pct']:.3f}%**"
            )


            st.write(
                f"Variação municipal de João: "
                f"**{resultado['variacao_municipal_joao']:+.2f} p.p.**"
            )


            st.code(
                f"{resultado['variacao_municipal_joao']:+.2f} "
                f"× "
                f"{resultado['peso_municipio']:.6f} "
                f"= "
                f"{resultado['impacto_municipio_estado_joao']:+.4f} p.p."
            )


            if abrangencia_pesquisa == "Região":

                st.write(
                    f"Peso eleitoral da região: "
                    f"**{resultado['peso_regiao_pct']:.2f}%**"
                )


                st.write(
                    f"Impacto estadual da pesquisa regional: "
                    f"**{resultado['impacto_pesquisa_estado']:+.4f} p.p.**"
                )


            elif abrangencia_pesquisa == "Estado":

                st.write(
                    f"Efeito direto da pesquisa estadual: "
                    f"**{resultado['impacto_pesquisa_estado']:+.2f} p.p.**"
                )


            st.success(
                f"Pernambuco final: "
                f"João {resultado['joao_estado_final']:.2f}% × "
                f"Raquel {resultado['raquel_estado_final']:.2f}%"
            )


# ============================================================
# ABA — CONFIGURAR PARÂMETROS
# ============================================================

with aba_parametros:


    st.header("Configurar parâmetros")

    st.caption(
        "Os valores abaixo são sugestões iniciais. "
        "Cada parâmetro pode ser alterado separadamente."
    )


    # ========================================================
    # EDITOR
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
            "Pesquisa 0 a 5",
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
            "Pesquisa 5 a 10",
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
