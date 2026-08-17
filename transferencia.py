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
    peso_municipio_pct,

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
    peso_pesquisa_pct
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

        esquerda_municipio = joao_inicial
        direita_municipio = raquel_inicial


    # ========================================================
    # 3. PREFEITO
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
        # Lado apoiado
        # ----------------------------------------------------

        if lado_prefeito == "Esquerda — João Campos":

            candidato_apoiado = "João Campos"
            base_apoiado = joao_inicial

        else:

            candidato_apoiado = "Raquel Lyra"
            base_apoiado = raquel_inicial


        # ----------------------------------------------------
        # Gap
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
        # Empenho
        # ----------------------------------------------------

        if usar_empenho:

            transferencia_empenho = (
                gap_prefeito *
                empenho_fator
            )

        else:

            transferencia_empenho = 0


        # ----------------------------------------------------
        # Gap restante
        # ----------------------------------------------------

        gap_apos_empenho = max(
            gap_prefeito -
            transferencia_empenho,
            0
        )


        # ----------------------------------------------------
        # Avaliação
        # ----------------------------------------------------

        if usar_avaliacao:

            transferencia_avaliacao = (
                gap_apos_empenho *
                avaliacao_fator
            )

        else:

            transferencia_avaliacao = 0


        # ----------------------------------------------------
        # Total prefeito
        # ----------------------------------------------------

        transferencia_prefeito = (
            transferencia_empenho +
            transferencia_avaliacao
        )


        # ----------------------------------------------------
        # Resultado
        # ----------------------------------------------------

        if lado_prefeito == "Esquerda — João Campos":

            joao_apos_prefeito = limitar(
                joao_inicial +
                transferencia_prefeito
            )

            raquel_apos_prefeito = (
                100 -
                joao_apos_prefeito
            )

        else:

            raquel_apos_prefeito = limitar(
                raquel_inicial +
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
    # 4. LULA
    # ========================================================

    gap_lula_bruto = 0.0
    gap_lula = 0.0
    transferencia_lula = 0.0


    if usar_lula:

        # Lula menos esquerda depois do prefeito
        gap_lula_bruto = (
            pct_lula -
            joao_apos_prefeito
        )

        # Só gap positivo
        gap_lula = max(
            gap_lula_bruto,
            0
        )

        transferencia_lula = (
            gap_lula *
            lula_fator
        )


    # ========================================================
    # 5. RESULTADO DEPOIS DE LULA
    # ========================================================

    joao_apos_lula = limitar(
        joao_apos_prefeito +
        transferencia_lula
    )

    raquel_apos_lula = (
        100 -
        joao_apos_lula
    )


    # ========================================================
    # 6. PESQUISA
    # ========================================================

    gap_pesquisa_bruto = 0.0
    gap_pesquisa = 0.0

    fator_pesquisa = 0.0
    faixa_pesquisa = None

    transferencia_pesquisa = 0.0


    # ========================================================
    # PESQUISA MUNICIPAL OU REGIONAL
    #
    # Atua sobre o resultado territorial antes da pesquisa.
    # ========================================================

    if (
        usar_pesquisa
        and abrangencia_pesquisa in ["Município", "Região"]
    ):

        pesquisa_joao, pesquisa_raquel = normalizar(
            pesquisa_joao,
            pesquisa_raquel
        )

        # ----------------------------------------------------
        # Pesquisa menos resultado atual de João
        # ----------------------------------------------------

        gap_pesquisa_bruto = (
            pesquisa_joao -
            joao_apos_lula
        )


        # ----------------------------------------------------
        # Só gap positivo
        # ----------------------------------------------------

        gap_pesquisa = max(
            gap_pesquisa_bruto,
            0
        )


        if gap_pesquisa > 0:

            fator_pesquisa, faixa_pesquisa = (
                obter_fator_pesquisa(
                    gap_pesquisa
                )
            )


            transferencia_pesquisa = (
                gap_pesquisa *
                fator_pesquisa
            )


        # ----------------------------------------------------
        # Resultado após pesquisa
        # ----------------------------------------------------

        joao_final_municipio = limitar(
            joao_apos_lula +
            transferencia_pesquisa
        )

        raquel_final_municipio = (
            100 -
            joao_final_municipio
        )


    # ========================================================
    # SEM PESQUISA TERRITORIAL
    # ========================================================

    else:

        joao_final_municipio = joao_apos_lula

        raquel_final_municipio = (
            100 -
            joao_final_municipio
        )


    # ========================================================
    # 7. VARIAÇÃO MUNICIPAL TOTAL
    # ========================================================

    variacao_municipal_joao = (
        joao_final_municipio -
        joao_inicial
    )

    variacao_municipal_raquel = (
        raquel_final_municipio -
        raquel_inicial
    )


    # ========================================================
    # 8. PESO DO MUNICÍPIO
    # ========================================================

    peso_municipio = (
        peso_municipio_pct /
        100
    )


    # ========================================================
    # 9. IMPACTO MUNICIPAL SOBRE O ESTADO
    #
    # PASSO 2 (2)
    # ========================================================

    impacto_estado_joao = (
        variacao_municipal_joao *
        peso_municipio
    )

    impacto_estado_raquel = (
        variacao_municipal_raquel *
        peso_municipio
    )


    # ========================================================
    # 10. ESTADO APÓS TRANSFERÊNCIAS TERRITORIAIS
    # ========================================================

    joao_estado_antes_pesquisa = limitar(
        joao_estado +
        impacto_estado_joao
    )

    raquel_estado_antes_pesquisa = (
        100 -
        joao_estado_antes_pesquisa
    )


    # ========================================================
    # 11. PESQUISA ESTADUAL
    #
    # Quando a pesquisa é estadual, ela não usa o peso
    # municipal. Atua diretamente sobre Pernambuco.
    # ========================================================

    if (
        usar_pesquisa
        and abrangencia_pesquisa == "Estado"
    ):

        pesquisa_joao, pesquisa_raquel = normalizar(
            pesquisa_joao,
            pesquisa_raquel
        )


        # ----------------------------------------------------
        # Pesquisa estadual - cenário estadual atual
        # ----------------------------------------------------

        gap_pesquisa_bruto = (
            pesquisa_joao -
            joao_estado_antes_pesquisa
        )


        gap_pesquisa = max(
            gap_pesquisa_bruto,
            0
        )


        if gap_pesquisa > 0:

            fator_pesquisa, faixa_pesquisa = (
                obter_fator_pesquisa(
                    gap_pesquisa
                )
            )


            transferencia_pesquisa = (
                gap_pesquisa *
                fator_pesquisa
            )


        # ----------------------------------------------------
        # Aplicação direta no Estado
        # ----------------------------------------------------

        joao_estado_final = limitar(
            joao_estado_antes_pesquisa +
            transferencia_pesquisa
        )

        raquel_estado_final = (
            100 -
            joao_estado_final
        )


    else:

        joao_estado_final = (
            joao_estado_antes_pesquisa
        )

        raquel_estado_final = (
            raquel_estado_antes_pesquisa
        )


    # ========================================================
    # 12. PESQUISA REGIONAL
    #
    # O resultado regional foi calculado sobre o território.
    # O peso informado da região define o impacto no Estado.
    #
    # Se a pesquisa é municipal, usamos o peso do município.
    # Se regional, usamos peso_pesquisa_pct.
    # ========================================================

    impacto_pesquisa_estado = 0.0


    if (
        usar_pesquisa
        and abrangencia_pesquisa == "Região"
    ):

        # Retiramos primeiro a parcela da pesquisa que entrou
        # na variação municipal com peso municipal.

        efeito_sem_pesquisa = (
            joao_apos_lula -
            joao_inicial
        )

        impacto_sem_pesquisa = (
            efeito_sem_pesquisa *
            peso_municipio
        )


        # Efeito específico da pesquisa regional
        efeito_pesquisa_regional = (
            transferencia_pesquisa
        )


        peso_regiao = (
            peso_pesquisa_pct /
            100
        )


        impacto_pesquisa_estado = (
            efeito_pesquisa_regional *
            peso_regiao
        )


        joao_estado_final = limitar(
            joao_estado
            + impacto_sem_pesquisa
            + impacto_pesquisa_estado
        )

        raquel_estado_final = (
            100 -
            joao_estado_final
        )


        # Corrigir impacto total estadual
        impacto_estado_joao = (
            joao_estado_final -
            joao_estado
        )

        impacto_estado_raquel = (
            -impacto_estado_joao
        )


    # ========================================================
    # RETORNO
    # ========================================================

    return {

        # Estado
        "joao_estado": joao_estado,
        "raquel_estado": raquel_estado,

        # Município
        "joao_inicial": joao_inicial,
        "raquel_inicial": raquel_inicial,

        "peso_municipio_pct": peso_municipio_pct,
        "peso_municipio": peso_municipio,

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
        "transferencia_empenho": transferencia_empenho,

        # Avaliação
        "usar_avaliacao": usar_avaliacao,
        "avaliacao_fator": avaliacao_fator,
        "gap_apos_empenho": gap_apos_empenho,
        "transferencia_avaliacao": transferencia_avaliacao,

        # Prefeito total
        "transferencia_prefeito": transferencia_prefeito,

        "joao_apos_prefeito": joao_apos_prefeito,
        "raquel_apos_prefeito": raquel_apos_prefeito,

        # Lula
        "usar_lula": usar_lula,
        "pct_lula": pct_lula,

        "gap_lula_bruto": gap_lula_bruto,
        "gap_lula": gap_lula,

        "lula_fator": lula_fator,
        "transferencia_lula": transferencia_lula,

        "joao_apos_lula": joao_apos_lula,
        "raquel_apos_lula": raquel_apos_lula,

        # Pesquisa
        "usar_pesquisa": usar_pesquisa,
        "abrangencia_pesquisa": abrangencia_pesquisa,

        "pesquisa_joao": pesquisa_joao,
        "pesquisa_raquel": pesquisa_raquel,

        "gap_pesquisa_bruto": gap_pesquisa_bruto,
        "gap_pesquisa": gap_pesquisa,

        "faixa_pesquisa": faixa_pesquisa,
        "fator_pesquisa": fator_pesquisa,

        "transferencia_pesquisa":
            transferencia_pesquisa,

        "peso_pesquisa_pct":
            peso_pesquisa_pct,

        "impacto_pesquisa_estado":
            impacto_pesquisa_estado,

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
        "impacto_estado_joao":
            impacto_estado_joao,

        "impacto_estado_raquel":
            impacto_estado_raquel,

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
    # BASE 0
    # ========================================================

    st.header("Base 0 — Pernambuco")

    st.caption(
        "Cenário estadual inicial antes das transferências."
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
    # MUNICÍPIO
    # ========================================================

    st.divider()

    st.header("Base do município")


    usar_base_municipal = st.toggle(
        "Usar base municipal",
        value=True
    )


    if usar_base_municipal:

        c1, c2, c3 = st.columns(3)


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


        with c3:

            peso_municipio_pct = st.number_input(
                "Peso do município em Pernambuco (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.36,
                step=0.01,
                format="%.2f"
            )


    else:

        esquerda_municipio = joao_estado
        direita_municipio = raquel_estado
        peso_municipio_pct = 0.0


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


        st.caption(
            "Gap automático: Lula menos João após "
            "as transferências anteriores."
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

    peso_pesquisa_pct = 0.0


    if usar_pesquisa:


        abrangencia_pesquisa = st.selectbox(
            "Abrangência da pesquisa",
            [
                "Município",
                "Região",
                "Estado"
            ]
        )


        st.caption(
            "A pesquisa aproxima parcialmente o cenário calculado "
            "do resultado observado na pesquisa."
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

            peso_pesquisa_pct = st.number_input(
                "Peso eleitoral da região em Pernambuco (%)",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=0.1,
                help=(
                    "Percentual dos votos de Pernambuco "
                    "correspondente à região da pesquisa."
                )
            )


        # ----------------------------------------------------
        # MUNICÍPIO
        # ----------------------------------------------------

        elif abrangencia_pesquisa == "Município":

            peso_pesquisa_pct = (
                peso_municipio_pct
            )


            st.info(
                f"A pesquisa municipal utilizará o peso eleitoral "
                f"do município: {peso_municipio_pct:.2f}%."
            )


        # ----------------------------------------------------
        # ESTADO
        # ----------------------------------------------------

        else:

            peso_pesquisa_pct = 100.0


            st.info(
                "A pesquisa estadual atua diretamente sobre "
                "o cenário de Pernambuco."
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
        peso_municipio_pct=peso_municipio_pct,

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
        abrangencia_pesquisa=abrangencia_pesquisa,
        pesquisa_joao=pesquisa_joao,
        pesquisa_raquel=pesquisa_raquel,
        peso_pesquisa_pct=peso_pesquisa_pct
    )


    # ========================================================
    # RESULTADOS
    # ========================================================

    st.divider()

    st.header("Resultado projetado")


    if resultado is None:

        st.error(
            "As bases precisam ter soma maior que zero."
        )


    else:


        # ====================================================
        # MUNICÍPIO
        # ====================================================

        st.subheader("Resultado no município")


        c1, c2 = st.columns(2)


        c1.metric(
            "João Campos",
            f"{resultado['joao_final_municipio']:.2f}%",
            delta=(
                f"{resultado['variacao_municipal_joao']:+.2f} p.p."
            )
        )


        c2.metric(
            "Raquel Lyra",
            f"{resultado['raquel_final_municipio']:.2f}%",
            delta=(
                f"{resultado['variacao_municipal_raquel']:+.2f} p.p."
            )
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
        # EVOLUÇÃO
        # ====================================================

        st.divider()

        st.header("Evolução do cenário")


        e1, e2, e3, e4 = st.columns(4)


        e1.metric(
            "Base municipal",
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
                    f"Apoio: **{resultado['candidato_apoiado']}**"
                )

                st.write(
                    f"Votação do prefeito: "
                    f"**{resultado['pct_prefeito']:.2f}%**"
                )

                st.write(
                    f"Base do candidato apoiado: "
                    f"**{resultado['base_apoiado']:.2f}%**"
                )

                st.code(
                    f"{resultado['pct_prefeito']:.2f} "
                    f"- {resultado['base_apoiado']:.2f} "
                    f"= {resultado['gap_prefeito_bruto']:.2f} p.p."
                )

                if resultado["usar_empenho"]:

                    st.write(
                        f"Empenho: "
                        f"**{resultado['gap_prefeito']:.2f} "
                        f"× {resultado['empenho_fator']:.2f} "
                        f"= {resultado['transferencia_empenho']:.2f} p.p.**"
                    )

                if resultado["usar_avaliacao"]:

                    st.write(
                        f"Avaliação: "
                        f"**{resultado['gap_apos_empenho']:.2f} "
                        f"× {resultado['avaliacao_fator']:.2f} "
                        f"= {resultado['transferencia_avaliacao']:.2f} p.p.**"
                    )

                st.success(
                    f"Efeito total do prefeito: "
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
                        "Lula não acrescenta votos."
                    )

                else:

                    st.code(
                        f"{resultado['gap_lula']:.2f} "
                        f"× {resultado['lula_fator']:.2f} "
                        f"= {resultado['transferencia_lula']:.2f} p.p."
                    )

                    st.success(
                        f"Lula acrescenta "
                        f"{resultado['transferencia_lula']:.2f} p.p. "
                        f"a João."
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

            else:

                st.write(
                    f"Abrangência: "
                    f"**{resultado['abrangencia_pesquisa']}**"
                )

                st.write(
                    f"Pesquisa: "
                    f"**João {resultado['pesquisa_joao']:.2f}% × "
                    f"Raquel {resultado['pesquisa_raquel']:.2f}%**"
                )


                if resultado["abrangencia_pesquisa"] == "Estado":

                    base_comparacao = (
                        resultado["joao_estado_antes_pesquisa"]
                    )

                    st.write(
                        f"Cenário estadual antes da pesquisa: "
                        f"**{base_comparacao:.2f}% para João**"
                    )

                else:

                    base_comparacao = (
                        resultado["joao_apos_lula"]
                    )

                    st.write(
                        f"Cenário antes da pesquisa: "
                        f"**{base_comparacao:.2f}% para João**"
                    )


                st.code(
                    f"{resultado['pesquisa_joao']:.2f} "
                    f"- {base_comparacao:.2f} "
                    f"= {resultado['gap_pesquisa_bruto']:.2f} p.p."
                )


                if resultado["gap_pesquisa"] <= 0:

                    st.info(
                        "A pesquisa está igual ou abaixo do cenário "
                        "calculado. Portanto, não acrescenta votos."
                    )

                else:

                    st.write(
                        f"Faixa: "
                        f"**{resultado['faixa_pesquisa']}**"
                    )

                    st.write(
                        f"Fator utilizado: "
                        f"**{resultado['fator_pesquisa']:.2f}**"
                    )

                    st.code(
                        f"{resultado['gap_pesquisa']:.2f} "
                        f"× {resultado['fator_pesquisa']:.2f} "
                        f"= {resultado['transferencia_pesquisa']:.2f} p.p."
                    )

                    st.success(
                        f"Efeito da pesquisa: "
                        f"+{resultado['transferencia_pesquisa']:.2f} p.p."
                    )


        # ====================================================
        # MEMÓRIA — ESTADO
        # ====================================================

        with st.expander(
            "4. Impacto sobre Pernambuco",
            expanded=True
        ):

            st.write(
                f"Base 0 de Pernambuco: "
                f"**João {resultado['joao_estado']:.2f}% × "
                f"Raquel {resultado['raquel_estado']:.2f}%**"
            )


            if resultado["abrangencia_pesquisa"] != "Estado":

                st.write(
                    f"Peso do município: "
                    f"**{resultado['peso_municipio_pct']:.2f}%**"
                )


            if (
                resultado["usar_pesquisa"]
                and resultado["abrangencia_pesquisa"] == "Região"
            ):

                st.write(
                    f"Peso da região: "
                    f"**{resultado['peso_pesquisa_pct']:.2f}%**"
                )


            st.write(
                f"Impacto líquido sobre João em Pernambuco: "
                f"**{resultado['impacto_estado_joao']:+.4f} p.p.**"
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
# ABA — PARÂMETROS
# ============================================================

with aba_parametros:


    st.header("Configurar parâmetros")

    st.caption(
        "Os parâmetros são independentes e podem ser alterados "
        "livremente nesta sessão."
    )


    # ========================================================
    # EDITOR PADRÃO
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
        "Parâmetros do efeito do empenho sobre o gap do prefeito."
    )


    st.divider()


    # ========================================================
    # AVALIAÇÃO
    # ========================================================

    criar_editor_parametros(
        "Avaliação do prefeito",
        "avaliacao",
        "Parâmetros da avaliação sobre o gap restante."
    )


    st.divider()


    # ========================================================
    # LULA
    # ========================================================

    criar_editor_parametros(
        "Efeito de Lula",
        "lula",
        "Parâmetros da transferência do gap positivo de Lula."
    )


    st.divider()


    # ========================================================
    # PESQUISA
    # ========================================================

    st.subheader("Efeito da pesquisa")

    st.caption(
        "Percentual do gap entre o cenário calculado "
        "e o resultado da pesquisa que será incorporado."
    )


    p1, p2, p3 = st.columns(3)


    with p1:

        st.markdown(
            "**0 a 5 p.p.**"
        )

        st.number_input(
            "Fator 0–5",
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
            "Fator 5–10",
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
            "Fator 10+",
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
        "Restaurar valores sugeridos",
        type="secondary"
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
