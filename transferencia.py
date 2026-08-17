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

def limitar(valor, minimo=0.0, maximo=100.0):

    return max(
        minimo,
        min(maximo, valor)
    )


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
# FUNÇÃO DA PESQUISA
#
# REGRA:
#
# 1. identifica quem lidera a pesquisa
# 2. compara o percentual desse candidato na pesquisa
#    com o percentual dele na simulação
# 3. se pesquisa <= simulação:
#       efeito = 0
# 4. se pesquisa > simulação:
#       gap = pesquisa - simulação
#       efeito = gap × fator
# 5. soma o efeito ao candidato que lidera a pesquisa
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
    # EMPATE NA PESQUISA
    # --------------------------------------------------------

    if abs(pesquisa_joao - pesquisa_raquel) < 0.000001:

        return {

            "joao_final": joao_atual,
            "raquel_final": raquel_atual,

            "lider_pesquisa": "Empate",

            "percentual_lider_pesquisa": pesquisa_joao,
            "percentual_lider_simulacao": None,

            "gap_bruto": 0.0,
            "gap": 0.0,

            "faixa": None,
            "fator": 0.0,

            "efeito": 0.0
        }


    # --------------------------------------------------------
    # JOÃO LIDERA A PESQUISA
    # --------------------------------------------------------

    if pesquisa_joao > pesquisa_raquel:

        lider_pesquisa = "João Campos"

        percentual_lider_pesquisa = pesquisa_joao

        percentual_lider_simulacao = joao_atual


    # --------------------------------------------------------
    # RAQUEL LIDERA A PESQUISA
    # --------------------------------------------------------

    else:

        lider_pesquisa = "Raquel Lyra"

        percentual_lider_pesquisa = pesquisa_raquel

        percentual_lider_simulacao = raquel_atual


    # --------------------------------------------------------
    # GAP
    # --------------------------------------------------------

    gap_bruto = (
        percentual_lider_pesquisa
        -
        percentual_lider_simulacao
    )


    # --------------------------------------------------------
    # REGRA FUNDAMENTAL
    #
    # Se o candidato já tem na simulação um percentual
    # igual ou superior ao da pesquisa, efeito = zero.
    # --------------------------------------------------------

    gap = max(
        gap_bruto,
        0
    )


    fator = 0.0
    faixa = None
    efeito = 0.0


    # --------------------------------------------------------
    # APLICAÇÃO DO FATOR
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
    # APLICAÇÃO AO LÍDER DA PESQUISA
    # --------------------------------------------------------

    if lider_pesquisa == "João Campos":

        joao_final = limitar(
            joao_atual +
            efeito
        )

        raquel_final = (
            100 -
            joao_final
        )


    elif lider_pesquisa == "Raquel Lyra":

        raquel_final = limitar(
            raquel_atual +
            efeito
        )

        joao_final = (
            100 -
            raquel_final
        )


    else:

        joao_final = joao_atual
        raquel_final = raquel_atual


    return {

        "joao_final": joao_final,
        "raquel_final": raquel_final,

        "lider_pesquisa": lider_pesquisa,

        "percentual_lider_pesquisa":
            percentual_lider_pesquisa,

        "percentual_lider_simulacao":
            percentual_lider_simulacao,

        "gap_bruto": gap_bruto,
        "gap": gap,

        "faixa": faixa,
        "fator": fator,

        "efeito": efeito
    }


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def calcular_transferencia(

    # Estado
    joao_estado,
    raquel_estado,

    # Município
    usar_base_municipal,
    esquerda_municipio,
    direita_municipio,

    votos_validos_municipio,
    votos_validos_estado,

    # Prefeito
    usar_prefeito,
    pct_prefeito,
    lado_prefeito,

    # Empenho
    usar_empenho,
    empenho_fator,

    # Avaliação
    usar_avaliacao,
    avaliacao_fator,

    # Lula
    usar_lula,
    pct_lula,
    lula_fator,

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

    if joao_estado is None:
        return None


    # ========================================================
    # 2. PESOS AUTOMÁTICOS
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

        peso_municipio = 0
        peso_regiao = 0


    # ========================================================
    # 3. BASE MUNICIPAL
    # ========================================================

    if usar_base_municipal:

        esquerda_municipio, direita_municipio = normalizar(
            esquerda_municipio,
            direita_municipio
        )

        if esquerda_municipio is None:
            return None

        joao_inicial = esquerda_municipio
        raquel_inicial = direita_municipio

    else:

        joao_inicial = joao_estado
        raquel_inicial = raquel_estado


    # ========================================================
    # 4. PREFEITO
    # ========================================================

    candidato_apoiado = None
    base_apoiado = None

    gap_prefeito_bruto = 0.0
    gap_prefeito = 0.0

    transferencia_empenho = 0.0
    transferencia_avaliacao = 0.0

    gap_apos_empenho = 0.0

    transferencia_prefeito = 0.0


    if usar_prefeito:


        # ----------------------------------------------------
        # CANDIDATO APOIADO
        # ----------------------------------------------------

        if lado_prefeito == "Esquerda — João Campos":

            candidato_apoiado = "João Campos"
            base_apoiado = joao_inicial

        else:

            candidato_apoiado = "Raquel Lyra"
            base_apoiado = raquel_inicial


        # ----------------------------------------------------
        # GAP
        # ----------------------------------------------------

        gap_prefeito_bruto = (
            pct_prefeito -
            base_apoiado
        )

        gap_prefeito = max(
            gap_prefeito_bruto,
            0
        )


        # ----------------------------------------------------
        # EMPENHO
        # ----------------------------------------------------

        if usar_empenho:

            transferencia_empenho = (
                gap_prefeito *
                empenho_fator
            )

        else:

            transferencia_empenho = 0


        # ----------------------------------------------------
        # GAP RESTANTE
        # ----------------------------------------------------

        gap_apos_empenho = max(
            gap_prefeito
            -
            transferencia_empenho,
            0
        )


        # ----------------------------------------------------
        # AVALIAÇÃO
        # ----------------------------------------------------

        if usar_avaliacao:

            transferencia_avaliacao = (
                gap_apos_empenho
                *
                avaliacao_fator
            )

        else:

            transferencia_avaliacao = 0


        # ----------------------------------------------------
        # TOTAL
        # ----------------------------------------------------

        transferencia_prefeito = (
            transferencia_empenho
            +
            transferencia_avaliacao
        )


        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------

        if candidato_apoiado == "João Campos":

            joao_apos_prefeito = limitar(
                joao_inicial
                +
                transferencia_prefeito
            )

            raquel_apos_prefeito = (
                100 -
                joao_apos_prefeito
            )

        else:

            raquel_apos_prefeito = limitar(
                raquel_inicial
                +
                transferencia_prefeito
            )

            joao_apos_prefeito = (
                100 -
                raquel_apos_prefeito
            )


    else:

        joao_apos_prefeito = joao_inicial
        raquel_apos_prefeito = raquel_inicial


    # ========================================================
    # 5. LULA
    # ========================================================

    gap_lula_bruto = 0.0
    gap_lula = 0.0

    transferencia_lula = 0.0


    if usar_lula:

        gap_lula_bruto = (
            pct_lula
            -
            joao_apos_prefeito
        )

        gap_lula = max(
            gap_lula_bruto,
            0
        )

        transferencia_lula = (
            gap_lula
            *
            lula_fator
        )


    # ========================================================
    # 6. RESULTADO APÓS LULA
    # ========================================================

    joao_apos_lula = limitar(
        joao_apos_prefeito
        +
        transferencia_lula
    )

    raquel_apos_lula = (
        100 -
        joao_apos_lula
    )


    # ========================================================
    # 7. PESQUISA MUNICIPAL
    # ========================================================

    resultado_pesquisa = None


    if (
        usar_pesquisa
        and abrangencia_pesquisa == "Município"
    ):

        resultado_pesquisa = aplicar_pesquisa(

            joao_apos_lula,
            raquel_apos_lula,

            pesquisa_joao,
            pesquisa_raquel
        )


        joao_final_municipio = (
            resultado_pesquisa["joao_final"]
        )

        raquel_final_municipio = (
            resultado_pesquisa["raquel_final"]
        )


    else:

        joao_final_municipio = joao_apos_lula

        raquel_final_municipio = raquel_apos_lula


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
    # 9. IMPACTO MUNICIPAL EM PERNAMBUCO
    #
    # PASSO 2 (2)
    # ========================================================

    impacto_municipal_estado_joao = (
        variacao_municipal_joao
        *
        peso_municipio
    )


    joao_estado_apos_municipio = limitar(
        joao_estado
        +
        impacto_municipal_estado_joao
    )

    raquel_estado_apos_municipio = (
        100 -
        joao_estado_apos_municipio
    )


    # ========================================================
    # 10. PESQUISA REGIONAL
    # ========================================================

    impacto_pesquisa_estado = 0.0


    if (
        usar_pesquisa
        and abrangencia_pesquisa == "Região"
    ):

        # A pesquisa regional é comparada ao cenário
        # estadual atual como referência da região.

        resultado_pesquisa = aplicar_pesquisa(

            joao_estado_apos_municipio,
            raquel_estado_apos_municipio,

            pesquisa_joao,
            pesquisa_raquel
        )


        efeito_pesquisa_regional_joao = (
            resultado_pesquisa["joao_final"]
            -
            joao_estado_apos_municipio
        )


        # Efeito regional ponderado pelo peso da região

        impacto_pesquisa_estado = (
            efeito_pesquisa_regional_joao
            *
            peso_regiao
        )


        joao_estado_final = limitar(
            joao_estado_apos_municipio
            +
            impacto_pesquisa_estado
        )

        raquel_estado_final = (
            100 -
            joao_estado_final
        )


    # ========================================================
    # 11. PESQUISA ESTADUAL
    # ========================================================

    elif (
        usar_pesquisa
        and abrangencia_pesquisa == "Estado"
    ):

        resultado_pesquisa = aplicar_pesquisa(

            joao_estado_apos_municipio,
            raquel_estado_apos_municipio,

            pesquisa_joao,
            pesquisa_raquel
        )


        # Pesquisa estadual atua diretamente sobre PE

        joao_estado_final = (
            resultado_pesquisa["joao_final"]
        )

        raquel_estado_final = (
            resultado_pesquisa["raquel_final"]
        )


        impacto_pesquisa_estado = (
            joao_estado_final
            -
            joao_estado_apos_municipio
        )


    # ========================================================
    # 12. SEM PESQUISA REGIONAL/ESTADUAL
    # ========================================================

    else:

        joao_estado_final = (
            joao_estado_apos_municipio
        )

        raquel_estado_final = (
            raquel_estado_apos_municipio
        )


    # ========================================================
    # 13. IMPACTO TOTAL SOBRE PERNAMBUCO
    # ========================================================

    impacto_estado_joao = (
        joao_estado_final
        -
        joao_estado
    )

    impacto_estado_raquel = (
        -impacto_estado_joao
    )


    # ========================================================
    # RETORNO
    # ========================================================

    return {

        # Estado inicial
        "joao_estado": joao_estado,
        "raquel_estado": raquel_estado,

        # Município inicial
        "joao_inicial": joao_inicial,
        "raquel_inicial": raquel_inicial,

        # Pesos
        "peso_municipio": peso_municipio,
        "peso_regiao": peso_regiao,

        "peso_municipio_pct":
            peso_municipio * 100,

        "peso_regiao_pct":
            peso_regiao * 100,

        # Prefeito
        "usar_prefeito": usar_prefeito,
        "candidato_apoiado": candidato_apoiado,

        "pct_prefeito": pct_prefeito,
        "base_apoiado": base_apoiado,

        "gap_prefeito_bruto": gap_prefeito_bruto,
        "gap_prefeito": gap_prefeito,

        # Empenho
        "usar_empenho": usar_empenho,
        "empenho_fator": empenho_fator,

        "transferencia_empenho":
            transferencia_empenho,

        "gap_apos_empenho":
            gap_apos_empenho,

        # Avaliação
        "usar_avaliacao": usar_avaliacao,
        "avaliacao_fator": avaliacao_fator,

        "transferencia_avaliacao":
            transferencia_avaliacao,

        # Prefeito total
        "transferencia_prefeito":
            transferencia_prefeito,

        "joao_apos_prefeito":
            joao_apos_prefeito,

        "raquel_apos_prefeito":
            raquel_apos_prefeito,

        # Lula
        "usar_lula": usar_lula,
        "pct_lula": pct_lula,

        "gap_lula_bruto": gap_lula_bruto,
        "gap_lula": gap_lula,

        "lula_fator": lula_fator,

        "transferencia_lula":
            transferencia_lula,

        "joao_apos_lula":
            joao_apos_lula,

        "raquel_apos_lula":
            raquel_apos_lula,

        # Pesquisa
        "usar_pesquisa": usar_pesquisa,

        "abrangencia_pesquisa":
            abrangencia_pesquisa,

        "pesquisa_joao":
            pesquisa_joao,

        "pesquisa_raquel":
            pesquisa_raquel,

        "resultado_pesquisa":
            resultado_pesquisa,

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
        "impacto_municipal_estado_joao":
            impacto_municipal_estado_joao,

        "joao_estado_apos_municipio":
            joao_estado_apos_municipio,

        "raquel_estado_apos_municipio":
            raquel_estado_apos_municipio,

        "impacto_pesquisa_estado":
            impacto_pesquisa_estado,

        "impacto_estado_joao":
            impacto_estado_joao,

        "impacto_estado_raquel":
            impacto_estado_raquel,

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
    # BASE 0
    # ========================================================

    st.header("Base 0 — Pernambuco")

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


    usar_base_municipal = st.toggle(
        "Usar base municipal",
        value=True
    )


    if usar_base_municipal:

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


        # ----------------------------------------------------
        # VOTOS VÁLIDOS
        #
        # Estes campos substituem o input manual de peso.
        # ----------------------------------------------------

        st.caption(
            "O peso eleitoral é calculado automaticamente "
            "a partir dos votos válidos."
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
            f"Peso eleitoral calculado automaticamente: "
            f"**{peso_visual:.3f}%** de Pernambuco."
        )


    else:

        esquerda_municipio = joao_estado
        direita_municipio = raquel_estado

        votos_validos_municipio = 0
        votos_validos_estado = 5000000


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

    lado_prefeito = "Esquerda — João Campos"

    usar_empenho = False
    usar_avaliacao = False

    empenho_fator = 0.0
    avaliacao_fator = 0.0

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


                empenho_fator = st.session_state[
                    f"param_empenho_{categoria_empenho}"
                ]


                st.metric(
                    "Fator",
                    f"{empenho_fator:.2f}"
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


                avaliacao_fator = st.session_state[
                    f"param_avaliacao_{categoria_avaliacao}"
                ]


                st.metric(
                    "Fator",
                    f"{avaliacao_fator:.2f}"
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
    lula_fator = 0.0

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
                index=4
            )


            lula_fator = st.session_state[
                f"param_lula_{categoria_lula}"
            ]


            st.metric(
                "Fator",
                f"{lula_fator:.2f}"
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
                f"Peso eleitoral da região calculado: "
                f"**{peso_regiao_visual:.2f}%** de Pernambuco."
            )


        elif abrangencia_pesquisa == "Estado":

            st.info(
                "Pesquisa estadual atua diretamente sobre "
                "o cenário estadual."
            )


        else:

            st.info(
                "Pesquisa municipal atua sobre o resultado "
                "do município antes da ponderação estadual."
            )


        st.caption(
            "O sistema identifica automaticamente quem lidera "
            "a pesquisa. O efeito é aplicado somente a esse candidato."
        )


    # ========================================================
    # CALCULAR
    # ========================================================

    resultado = calcular_transferencia(

        joao_estado=joao_estado,
        raquel_estado=raquel_estado,

        usar_base_municipal=usar_base_municipal,

        esquerda_municipio=esquerda_municipio,
        direita_municipio=direita_municipio,

        votos_validos_municipio=
            votos_validos_municipio,

        votos_validos_estado=
            votos_validos_estado,

        usar_prefeito=usar_prefeito,

        pct_prefeito=pct_prefeito,

        lado_prefeito=lado_prefeito,

        usar_empenho=usar_empenho,

        empenho_fator=empenho_fator,

        usar_avaliacao=usar_avaliacao,

        avaliacao_fator=avaliacao_fator,

        usar_lula=usar_lula,

        pct_lula=pct_lula,

        lula_fator=lula_fator,

        usar_pesquisa=usar_pesquisa,

        abrangencia_pesquisa=
            abrangencia_pesquisa,

        pesquisa_joao=pesquisa_joao,

        pesquisa_raquel=pesquisa_raquel,

        votos_validos_regiao=
            votos_validos_regiao
    )


    # ========================================================
    # RESULTADOS
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


        c1.metric(
            "João Campos",
            f"{resultado['joao_final_municipio']:.2f}%"
        )


        c2.metric(
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
        # PERNAMBUCO
        # ====================================================

        st.divider()

        st.subheader("Resultado em Pernambuco")


        c1, c2 = st.columns(2)


        c1.metric(
            "João Campos",
            f"{resultado['joao_estado_final']:.2f}%",
            delta=(
                f"{resultado['impacto_estado_joao']:+.3f} p.p."
            )
        )


        c2.metric(
            "Raquel Lyra",
            f"{resultado['raquel_estado_final']:.2f}%",
            delta=(
                f"{resultado['impacto_estado_raquel']:+.3f} p.p."
            )
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
        # EVOLUÇÃO MUNICIPAL
        # ====================================================

        st.divider()

        st.subheader("Evolução no município")


        c1, c2, c3 = st.columns(3)


        c1.metric(
            "Base",
            f"{resultado['joao_inicial']:.2f}%"
        )


        c2.metric(
            "Após prefeito",
            f"{resultado['joao_apos_prefeito']:.2f}%"
        )


        c3.metric(
            "Após Lula",
            f"{resultado['joao_apos_lula']:.2f}%"
        )


        # ====================================================
        # MEMÓRIA — PREFEITO
        # ====================================================

        st.divider()

        st.header("Memória de cálculo")


        with st.expander(
            "1. Prefeito",
            expanded=False
        ):


            if not resultado["usar_prefeito"]:

                st.info(
                    "Prefeito não utilizado."
                )


            else:

                st.write(
                    f"Apoia: "
                    f"**{resultado['candidato_apoiado']}**"
                )


                st.code(
                    f"{resultado['pct_prefeito']:.2f} "
                    f"- {resultado['base_apoiado']:.2f} "
                    f"= {resultado['gap_prefeito_bruto']:.2f} p.p."
                )


                if resultado["usar_empenho"]:

                    st.code(
                        f"{resultado['gap_prefeito']:.2f} "
                        f"× {resultado['empenho_fator']:.2f} "
                        f"= {resultado['transferencia_empenho']:.2f} p.p."
                    )


                if resultado["usar_avaliacao"]:

                    st.code(
                        f"{resultado['gap_apos_empenho']:.2f} "
                        f"× {resultado['avaliacao_fator']:.2f} "
                        f"= {resultado['transferencia_avaliacao']:.2f} p.p."
                    )


                st.success(
                    f"Efeito total: "
                    f"{resultado['transferencia_prefeito']:.2f} p.p. "
                    f"para {resultado['candidato_apoiado']}."
                )


        # ====================================================
        # MEMÓRIA — LULA
        # ====================================================

        with st.expander(
            "2. Lula",
            expanded=False
        ):


            if not resultado["usar_lula"]:

                st.info(
                    "Lula não utilizado."
                )


            else:

                st.code(
                    f"{resultado['pct_lula']:.2f} "
                    f"- {resultado['joao_apos_prefeito']:.2f} "
                    f"= {resultado['gap_lula_bruto']:.2f} p.p."
                )


                if resultado["gap_lula"] <= 0:

                    st.info(
                        "Gap zero ou negativo. "
                        "Lula não produz efeito."
                    )


                else:

                    st.code(
                        f"{resultado['gap_lula']:.2f} "
                        f"× {resultado['lula_fator']:.2f} "
                        f"= {resultado['transferencia_lula']:.2f} p.p."
                    )


                    st.success(
                        f"Efeito de Lula: "
                        f"+{resultado['transferencia_lula']:.2f} p.p. "
                        f"para João."
                    )


        # ====================================================
        # MEMÓRIA — PESQUISA
        # ====================================================

        with st.expander(
            "3. Pesquisa",
            expanded=True
        ):


            if not resultado["usar_pesquisa"]:

                st.info(
                    "Pesquisa não utilizada."
                )


            elif resultado["resultado_pesquisa"] is None:

                st.info(
                    "Pesquisa sem efeito neste cenário."
                )


            else:

                rp = resultado[
                    "resultado_pesquisa"
                ]


                st.write(
                    f"Abrangência: "
                    f"**{resultado['abrangencia_pesquisa']}**"
                )


                st.write(
                    f"Pesquisa: "
                    f"**João {resultado['pesquisa_joao']:.2f}% × "
                    f"Raquel {resultado['pesquisa_raquel']:.2f}%**"
                )


                # --------------------------------------------
                # EMPATE
                # --------------------------------------------

                if rp["lider_pesquisa"] == "Empate":

                    st.info(
                        "A pesquisa está empatada. "
                        "Nenhum candidato recebe efeito."
                    )


                # --------------------------------------------
                # TEM LÍDER
                # --------------------------------------------

                else:

                    st.write(
                        f"Líder da pesquisa: "
                        f"**{rp['lider_pesquisa']}**"
                    )


                    st.write(
                        f"{rp['lider_pesquisa']} na pesquisa: "
                        f"**{rp['percentual_lider_pesquisa']:.2f}%**"
                    )


                    st.write(
                        f"{rp['lider_pesquisa']} na simulação "
                        f"antes da pesquisa: "
                        f"**{rp['percentual_lider_simulacao']:.2f}%**"
                    )


                    st.code(
                        f"{rp['percentual_lider_pesquisa']:.2f} "
                        f"- "
                        f"{rp['percentual_lider_simulacao']:.2f} "
                        f"= "
                        f"{rp['gap_bruto']:.2f} p.p."
                    )


                    # ----------------------------------------
                    # SEM EFEITO
                    # ----------------------------------------

                    if rp["gap"] <= 0:

                        st.info(
                            f"{rp['lider_pesquisa']} já possui na "
                            f"simulação um percentual igual ou maior "
                            f"que o observado na pesquisa. "
                            f"Portanto, a pesquisa não produz efeito."
                        )


                    # ----------------------------------------
                    # COM EFEITO
                    # ----------------------------------------

                    else:

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
                            f"× {rp['fator']:.2f} "
                            f"= {rp['efeito']:.2f} p.p."
                        )


                        st.success(
                            f"A pesquisa acrescenta "
                            f"{rp['efeito']:.2f} p.p. "
                            f"a {rp['lider_pesquisa']}."
                        )


        # ====================================================
        # MEMÓRIA — PERNAMBUCO
        # ====================================================

        with st.expander(
            "4. Impacto em Pernambuco",
            expanded=True
        ):


            st.write(
                f"Base 0: "
                f"**João {resultado['joao_estado']:.2f}% × "
                f"Raquel {resultado['raquel_estado']:.2f}%**"
            )


            st.write(
                f"Peso eleitoral do município: "
                f"**{resultado['peso_municipio_pct']:.3f}%**"
            )


            st.code(
                f"{resultado['variacao_municipal_joao']:+.2f} "
                f"× {resultado['peso_municipio']:.6f} "
                f"= "
                f"{resultado['impacto_municipal_estado_joao']:+.4f} p.p."
            )


            if (
                resultado["usar_pesquisa"]
                and resultado["abrangencia_pesquisa"] == "Região"
            ):

                st.write(
                    f"Peso eleitoral da região: "
                    f"**{resultado['peso_regiao_pct']:.2f}%**"
                )


                st.write(
                    f"Impacto específico da pesquisa regional: "
                    f"**{resultado['impacto_pesquisa_estado']:+.4f} p.p.**"
                )


            if (
                resultado["usar_pesquisa"]
                and resultado["abrangencia_pesquisa"] == "Estado"
            ):

                st.write(
                    f"Efeito direto da pesquisa estadual: "
                    f"**{resultado['impacto_pesquisa_estado']:+.2f} p.p.**"
                )


            st.success(
                f"Pernambuco final: "
                f"João {resultado['joao_estado_final']:.2f}% × "
                f"Raquel {resultado['raquel_estado_final']:.2f}%"
            )


            st.caption(
                f"Com uma casa decimal: "
                f"João {resultado['joao_estado_final']:.1f}% × "
                f"Raquel {resultado['raquel_estado_final']:.1f}%."
            )


# ============================================================
# ABA — CONFIGURAR PARÂMETROS
# ============================================================

with aba_parametros:


    st.header("Configurar parâmetros")

    st.write(
        "Todos os parâmetros podem ser alterados "
        "independentemente."
    )


    # ========================================================
    # EDITOR
    # ========================================================

    def criar_editor_parametros(
        titulo,
        variavel,
        descricao
    ):


        st.subheader(titulo)

        st.caption(descricao)


        cols = st.columns(5)


        for i, categoria in enumerate(CATEGORIAS):

            with cols[i]:

                st.markdown(
                    f"**{categoria}**"
                )


                st.number_input(
                    "Fator",
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

    criar_editor_parametros(
        "Empenho do prefeito",
        "empenho",
        "Quanto do gap do prefeito é mobilizado pelo empenho."
    )


    st.divider()


    # ========================================================
    # AVALIAÇÃO
    # ========================================================

    criar_editor_parametros(
        "Avaliação do prefeito",
        "avaliacao",
        "Quanto do gap restante é mobilizado pela avaliação."
    )


    st.divider()


    # ========================================================
    # LULA
    # ========================================================

    criar_editor_parametros(
        "Efeito de Lula",
        "lula",
        "Quanto do gap positivo de Lula é transferido para João."
    )


    # ========================================================
    # PESQUISA
    # ========================================================

    st.divider()

    st.subheader("Efeito da pesquisa")

    st.caption(
        "O fator é aplicado ao gap positivo do candidato "
        "que estiver liderando a pesquisa."
    )


    p1, p2, p3 = st.columns(3)


    with p1:

        st.markdown(
            "**0 a 5 p.p.**"
        )

        st.number_input(
            "Fator",
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
            "Fator",
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
            "Fator",
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
