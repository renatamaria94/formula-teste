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
#
# IMPORTANTE:
# Cada variável possui sua própria escala.
#
# Portanto:
#
# Forte no empenho pode ser 0.80
# Forte na avaliação pode ser 1.20
# Forte em Lula pode ser 0.60
#
# sem que uma alteração afete as outras.
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
# INICIALIZAR SESSION STATE
# ============================================================

for variavel, escala in PARAMETROS_PADRAO.items():

    for categoria, valor in escala.items():

        chave = f"param_{variavel}_{categoria}"

        if chave not in st.session_state:
            st.session_state[chave] = valor


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def limitar(valor, minimo=0.0, maximo=100.0):
    """
    Mantém o resultado eleitoral entre 0% e 100%.
    """
    return max(minimo, min(maximo, valor))


def normalizar(esquerda, direita):
    """
    Normaliza os dois lados para que somem 100%.
    """

    total = esquerda + direita

    if total <= 0:
        return None, None

    esquerda_norm = (
        esquerda / total
    ) * 100

    direita_norm = (
        direita / total
    ) * 100

    return esquerda_norm, direita_norm


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
    empenho_fator,
    avaliacao_fator,
    pct_lula,
    lula_fator
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

    esquerda_municipio, direita_municipio = normalizar(
        esquerda_municipio,
        direita_municipio
    )

    if esquerda_municipio is None:
        return None


    # ========================================================
    # 3. AJUSTE TERRITORIAL
    #
    # Mede quanto o município é mais ou menos de esquerda
    # do que a Base 0 estadual.
    #
    # Exemplo:
    #
    # João PE = 56%
    # Esquerda municipal = 67%
    #
    # diferencial = +11 p.p.
    #
    # Portanto:
    #
    # João inicial no município = 67%
    # Raquel inicial = 33%
    # ========================================================

    diferencial_municipal = (
        esquerda_municipio -
        joao_estado
    )

    joao_inicial = (
        joao_estado +
        diferencial_municipal
    )

    joao_inicial = limitar(
        joao_inicial
    )

    raquel_inicial = (
        100 -
        joao_inicial
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
    # votação do prefeito
    # -
    # base do candidato que ele apoia
    #
    # Exemplo:
    #
    # Prefeito = 65%
    # Raquel = 44%
    #
    # Gap = 21 p.p.
    #
    # Se o resultado for <= 0:
    # não existe gap disponível.
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
    # 6. EMPENHO DO PREFEITO
    #
    # gap × fator de empenho
    #
    # Exemplo:
    #
    # gap = 21
    # Forte = 0.80
    #
    # 21 × 0.80 = 16.8 p.p.
    # ========================================================

    transferencia_empenho = (
        gap_prefeito *
        empenho_fator
    )


    # ========================================================
    # 7. AVALIAÇÃO DO PREFEITO
    #
    # A avaliação atua SOBRE A TRANSFERÊNCIA.
    #
    # transferência do empenho × fator de avaliação
    #
    # IMPORTANTE:
    #
    # O fator pode ser maior que 1.
    #
    # Exemplo:
    #
    # transferência = 16.8
    # avaliação = 1.20
    #
    # 16.8 × 1.20 = 20.16 p.p.
    #
    # Portanto, NÃO limitamos ao gap original.
    # ========================================================

    transferencia_prefeito = (
        transferencia_empenho *
        avaliacao_fator
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
    # IMPORTANTE:
    #
    # O gap NÃO é um parâmetro digitado.
    #
    # Ele é calculado automaticamente DEPOIS
    # do efeito do prefeito.
    #
    # Fórmula:
    #
    # Lula no município
    # -
    # João após transferências anteriores
    #
    # Se <= 0:
    # Lula não entra.
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
    # 10. EFEITO DE LULA
    #
    # gap automático × fator escolhido
    #
    # O fator também pode ser > 1.
    #
    # Exemplo:
    #
    # gap Lula = 20
    # Forte = 0.80
    #
    # efeito = 16 p.p.
    #
    # Se Forte for alterado para 1.20:
    #
    # efeito = 24 p.p.
    # ========================================================

    transferencia_lula = (
        gap_lula *
        lula_fator
    )

    transferencia_lula = max(
        transferencia_lula,
        0
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

        "diferencial_municipal":
            diferencial_municipal,


        # Inicial municipal
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
        "empenho_fator":
            empenho_fator,

        "transferencia_empenho":
            transferencia_empenho,


        # Avaliação
        "avaliacao_fator":
            avaliacao_fator,

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

        "lula_fator":
            lula_fator,

        "transferencia_lula":
            transferencia_lula,


        # Final
        "joao_final":
            joao_final,

        "raquel_final":
            raquel_final
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
# ABA 1 — SIMULADOR
# ============================================================

with aba_simulador:

    # ========================================================
    # DADOS DO CENÁRIO
    # ========================================================

    st.header("Dados do cenário")

    st.caption(
        "Informe os dados eleitorais utilizados na simulação."
    )

    col1, col2, col3 = st.columns(3)


    # --------------------------------------------------------
    # BASE ESTADUAL
    # --------------------------------------------------------

    with col1:

        st.subheader("Base 0 — Pernambuco")

        joao_estado = st.number_input(
            "João Campos — Estado (%)",
            min_value=0.0,
            max_value=100.0,
            value=56.0,
            step=0.1,
            key="joao_estado"
        )

        raquel_estado = st.number_input(
            "Raquel Lyra — Estado (%)",
            min_value=0.0,
            max_value=100.0,
            value=44.0,
            step=0.1,
            key="raquel_estado"
        )


    # --------------------------------------------------------
    # BASE MUNICIPAL
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # DADOS LOCAIS
    # --------------------------------------------------------

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


    # ========================================================
    # INTENSIDADE DOS EFEITOS
    # ========================================================

    st.divider()

    st.header("Intensidade dos efeitos")

    st.caption(
        "Cada variável possui sua própria escala de parâmetros. "
        "Os valores podem ser alterados na aba "
        "“Configurar parâmetros”."
    )

    i1, i2, i3 = st.columns(3)


    # --------------------------------------------------------
    # EMPENHO
    # --------------------------------------------------------

    with i1:

        st.subheader("Empenho do prefeito")

        categoria_empenho = st.selectbox(
            "Nível de empenho",
            CATEGORIAS,
            index=3,
            key="categoria_empenho"
        )

        empenho_fator = st.session_state[
            f"param_empenho_{categoria_empenho}"
        ]

        st.metric(
            "Fator utilizado",
            f"{empenho_fator:.2f}"
        )


    # --------------------------------------------------------
    # AVALIAÇÃO
    # --------------------------------------------------------

    with i2:

        st.subheader("Avaliação do prefeito")

        categoria_avaliacao = st.selectbox(
            "Nível de avaliação",
            CATEGORIAS,
            index=2,
            key="categoria_avaliacao"
        )

        avaliacao_fator = st.session_state[
            f"param_avaliacao_{categoria_avaliacao}"
        ]

        st.metric(
            "Fator utilizado",
            f"{avaliacao_fator:.2f}"
        )


    # --------------------------------------------------------
    # LULA
    # --------------------------------------------------------

    with i3:

        st.subheader("Efeito de Lula")

        categoria_lula = st.selectbox(
            "Intensidade do efeito",
            CATEGORIAS,
            index=2,
            key="categoria_lula"
        )

        lula_fator = st.session_state[
            f"param_lula_{categoria_lula}"
        ]

        st.metric(
            "Fator utilizado",
            f"{lula_fator:.2f}"
        )

        st.caption(
            "O gap de Lula é calculado automaticamente."
        )


    # ========================================================
    # CÁLCULO
    # ========================================================

    resultado = calcular_transferencia(

        joao_estado=joao_estado,

        raquel_estado=raquel_estado,

        esquerda_municipio=esquerda_municipio,

        direita_municipio=direita_municipio,

        pct_prefeito=pct_prefeito,

        lado_prefeito=lado_prefeito,

        empenho_fator=empenho_fator,

        avaliacao_fator=avaliacao_fator,

        pct_lula=pct_lula,

        lula_fator=lula_fator
    )


    # ========================================================
    # RESULTADO
    # ========================================================

    st.divider()

    st.header("Resultado projetado")


    if resultado is None:

        st.error(
            "As bases precisam ter soma maior que zero."
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


        # ====================================================
        # BARRA
        # ====================================================

        st.progress(
            resultado["joao_final"] / 100,
            text=(
                f"João {resultado['joao_final']:.1f}%"
                f" × "
                f"Raquel {resultado['raquel_final']:.1f}%"
            )
        )


        # ====================================================
        # EVOLUÇÃO
        # ====================================================

        st.subheader("Evolução do cenário")

        e1, e2, e3 = st.columns(3)


        with e1:

            st.markdown("#### Base municipal")

            st.metric(
                "João",
                f"{resultado['joao_inicial']:.2f}%"
            )

            st.metric(
                "Raquel",
                f"{resultado['raquel_inicial']:.2f}%"
            )


        with e2:

            st.markdown("#### Após prefeito")

            st.metric(
                "João",
                f"{resultado['joao_apos_prefeito']:.2f}%"
            )

            st.metric(
                "Raquel",
                f"{resultado['raquel_apos_prefeito']:.2f}%"
            )


        with e3:

            st.markdown("#### Após Lula")

            st.metric(
                "João",
                f"{resultado['joao_final']:.2f}%"
            )

            st.metric(
                "Raquel",
                f"{resultado['raquel_final']:.2f}%"
            )


        # ====================================================
        # MEMÓRIA DE CÁLCULO
        # ====================================================

        st.divider()

        st.header("Memória de cálculo")


        # ----------------------------------------------------
        # BASE MUNICIPAL
        # ----------------------------------------------------

        with st.expander(
            "1. Base estadual e municipal",
            expanded=True
        ):

            st.write(
                f"João na Base 0 estadual: "
                f"**{resultado['joao_estado']:.2f}%**"
            )

            st.write(
                f"Raquel na Base 0 estadual: "
                f"**{resultado['raquel_estado']:.2f}%**"
            )

            st.write(
                f"Esquerda no município: "
                f"**{resultado['esquerda_municipio']:.2f}%**"
            )

            st.write(
                f"Direita no município: "
                f"**{resultado['direita_municipio']:.2f}%**"
            )

            st.write(
                f"Diferença municipal da esquerda: "
                f"**{resultado['diferencial_municipal']:+.2f} p.p.**"
            )

            st.write("Ponto de partida local:")

            c1, c2 = st.columns(2)

            c1.metric(
                "João",
                f"{resultado['joao_inicial']:.2f}%"
            )

            c2.metric(
                "Raquel",
                f"{resultado['raquel_inicial']:.2f}%"
            )


        # ----------------------------------------------------
        # GAP PREFEITO
        # ----------------------------------------------------

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

            st.code(
                f"{resultado['pct_prefeito']:.2f} "
                f"- "
                f"{resultado['base_apoiado']:.2f} "
                f"= "
                f"{resultado['gap_prefeito_bruto']:.2f} p.p."
            )


            if resultado["gap_prefeito"] <= 0:

                st.info(
                    "O gap é zero ou negativo. "
                    "Não há reserva adicional do prefeito."
                )

            else:

                st.success(
                    f"Gap disponível: "
                    f"{resultado['gap_prefeito']:.2f} p.p."
                )


        # ----------------------------------------------------
        # EMPENHO
        # ----------------------------------------------------

        with st.expander(
            "3. Empenho do prefeito",
            expanded=True
        ):

            st.write(
                f"Classificação: "
                f"**{categoria_empenho}**"
            )

            st.write(
                f"Fator utilizado: "
                f"**{resultado['empenho_fator']:.2f}**"
            )

            st.code(
                f"{resultado['gap_prefeito']:.2f} "
                f"× "
                f"{resultado['empenho_fator']:.2f} "
                f"= "
                f"{resultado['transferencia_empenho']:.2f} p.p."
            )

            st.write(
                f"Transferência após empenho: "
                f"**{resultado['transferencia_empenho']:.2f} p.p.**"
            )


        # ----------------------------------------------------
        # AVALIAÇÃO
        # ----------------------------------------------------

        with st.expander(
            "4. Avaliação do prefeito",
            expanded=True
        ):

            st.write(
                f"Classificação: "
                f"**{categoria_avaliacao}**"
            )

            st.write(
                f"Fator utilizado: "
                f"**{resultado['avaliacao_fator']:.2f}**"
            )

            st.code(
                f"{resultado['transferencia_empenho']:.2f} "
                f"× "
                f"{resultado['avaliacao_fator']:.2f} "
                f"= "
                f"{resultado['transferencia_prefeito']:.2f} p.p."
            )

            st.success(
                f"Transferência efetiva do prefeito: "
                f"{resultado['transferencia_prefeito']:.2f} p.p."
            )


        # ----------------------------------------------------
        # ANTES DE LULA
        # ----------------------------------------------------

        with st.expander(
            "5. Resultado antes de Lula",
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


        # ----------------------------------------------------
        # LULA
        # ----------------------------------------------------

        with st.expander(
            "6. Gap de Lula",
            expanded=True
        ):

            st.write(
                f"Lula no município: "
                f"**{resultado['pct_lula']:.2f}%**"
            )

            st.write(
                f"João após as transferências anteriores: "
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
                    "O gap de Lula é zero ou negativo. "
                    "Lula não entra no cálculo."
                )

            else:

                st.write(
                    f"Gap positivo de Lula: "
                    f"**{resultado['gap_lula']:.2f} p.p.**"
                )

                st.write(
                    f"Classificação: "
                    f"**{categoria_lula}**"
                )

                st.write(
                    f"Fator utilizado: "
                    f"**{resultado['lula_fator']:.2f}**"
                )

                st.code(
                    f"{resultado['gap_lula']:.2f} "
                    f"× "
                    f"{resultado['lula_fator']:.2f} "
                    f"= "
                    f"{resultado['transferencia_lula']:.2f} p.p."
                )

                st.success(
                    f"Transferência adicional para João: "
                    f"{resultado['transferencia_lula']:.2f} p.p."
                )


# ============================================================
# ABA 2 — CONFIGURAÇÃO DOS PARÂMETROS
# ============================================================

with aba_parametros:

    st.header("Configurar parâmetros")

    st.write(
        "Cada variável possui sua própria escala. "
        "Alterar um valor de empenho, por exemplo, "
        "não altera a escala de avaliação ou de Lula."
    )

    st.info(
        "Os valores são usados apenas nesta sessão. "
        "Nenhuma alteração é salva em banco de dados."
    )


    # ========================================================
    # FUNÇÃO PARA CRIAR EDITOR
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

                    # permite valores bem acima de 1
                    max_value=10.0,

                    step=0.05,
                    format="%.2f",

                    key=(
                        f"param_"
                        f"{variavel}_"
                        f"{categoria}"
                    ),

                    label_visibility="collapsed"
                )


    # ========================================================
    # EMPENHO
    # ========================================================

    criar_editor_parametros(
        titulo="Empenho do prefeito",
        variavel="empenho",
        descricao=(
            "Define quanto do gap do prefeito é mobilizado."
        )
    )


    st.divider()


    # ========================================================
    # AVALIAÇÃO
    # ========================================================

    criar_editor_parametros(
        titulo="Avaliação do prefeito",
        variavel="avaliacao",
        descricao=(
            "Define como a avaliação potencializa ou reduz "
            "a transferência produzida pelo empenho."
        )
    )


    st.divider()


    # ========================================================
    # LULA
    # ========================================================

    criar_editor_parametros(
        titulo="Efeito de Lula",
        variavel="lula",
        descricao=(
            "Define quanto do gap positivo de Lula é "
            "convertido em transferência para João."
        )
    )


    # ========================================================
    # RESUMO
    # ========================================================

    st.divider()

    st.subheader("Resumo das escalas atuais")


    # --------------------------------------------------------
    # EMPENHO
    # --------------------------------------------------------

    st.markdown("#### Empenho")

    st.dataframe(
        {
            "Classificação": CATEGORIAS,

            "Fator": [
                st.session_state[
                    f"param_empenho_{categoria}"
                ]
                for categoria in CATEGORIAS
            ]
        },
        hide_index=True,
        use_container_width=True
    )


    # --------------------------------------------------------
    # AVALIAÇÃO
    # --------------------------------------------------------

    st.markdown("#### Avaliação")

    st.dataframe(
        {
            "Classificação": CATEGORIAS,

            "Fator": [
                st.session_state[
                    f"param_avaliacao_{categoria}"
                ]
                for categoria in CATEGORIAS
            ]
        },
        hide_index=True,
        use_container_width=True
    )


    # --------------------------------------------------------
    # LULA
    # --------------------------------------------------------

    st.markdown("#### Lula")

    st.dataframe(
        {
            "Classificação": CATEGORIAS,

            "Fator": [
                st.session_state[
                    f"param_lula_{categoria}"
                ]
                for categoria in CATEGORIAS
            ]
        },
        hide_index=True,
        use_container_width=True
    )


    # ========================================================
    # RESTAURAR PADRÕES
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

        st.rerun()


    st.caption(
        "Valores sugeridos inicialmente: "
        "Muito fraco = 0,00 | "
        "Fraco = 0,10 | "
        "Moderado = 0,50 | "
        "Forte = 0,80 | "
        "Muito forte = 1,00."
    )
