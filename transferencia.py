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
# CATEGORIAS E PARÂMETROS SUGERIDOS
# ============================================================

CATEGORIAS = [
    "Muito fraco",
    "Fraco",
    "Moderado",
    "Forte",
    "Muito forte"
]

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
# INICIALIZAR PARÂMETROS
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
    return max(minimo, min(maximo, valor))


def normalizar(a, b):

    total = a + b

    if total <= 0:
        return None, None

    return (
        a / total * 100,
        b / total * 100
    )


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def calcular_transferencia(

    joao_estado,
    raquel_estado,

    usar_base_municipal,
    esquerda_municipio,
    direita_municipio,

    usar_prefeito,
    pct_prefeito,
    lado_prefeito,

    usar_empenho,
    empenho_fator,

    usar_avaliacao,
    avaliacao_fator,

    usar_lula,
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
    # 2. BASE MUNICIPAL — OPCIONAL
    #
    # Se ligada:
    # usa a distribuição esquerda/direita do município.
    #
    # Se desligada:
    # mantém a Base 0 estadual.
    # ========================================================

    if usar_base_municipal:

        esquerda_municipio, direita_municipio = normalizar(
            esquerda_municipio,
            direita_municipio
        )

        if esquerda_municipio is None:
            return None

        diferencial_municipal = (
            esquerda_municipio -
            joao_estado
        )

        joao_inicial = limitar(
            joao_estado +
            diferencial_municipal
        )

        raquel_inicial = (
            100 - joao_inicial
        )

    else:

        esquerda_municipio = None
        direita_municipio = None

        diferencial_municipal = 0

        joao_inicial = joao_estado
        raquel_inicial = raquel_estado


    # ========================================================
    # VALORES INICIAIS DOS EFEITOS
    # ========================================================

    candidato_apoiado = None
    base_apoiado = None

    gap_prefeito_bruto = 0
    gap_prefeito = 0

    transferencia_empenho = 0
    gap_apos_empenho = 0

    transferencia_avaliacao = 0
    transferencia_prefeito = 0


    # ========================================================
    # 3. PREFEITO — OPCIONAL
    # ========================================================

    if usar_prefeito:

        # ----------------------------------------------------
        # Candidato apoiado
        # ----------------------------------------------------

        if lado_prefeito == "Esquerda — João Campos":

            candidato_apoiado = "João Campos"
            base_apoiado = joao_inicial

        else:

            candidato_apoiado = "Raquel Lyra"
            base_apoiado = raquel_inicial


        # ----------------------------------------------------
        # Gap do prefeito
        # ----------------------------------------------------

        gap_prefeito_bruto = (
            pct_prefeito -
            base_apoiado
        )

        gap_prefeito = max(
            gap_prefeito_bruto,
            0
        )


        # ====================================================
        # 4. EMPENHO — OPCIONAL
        #
        # Se ligado:
        # gap × fator
        #
        # Se desligado:
        # efeito = 0
        # ====================================================

        if usar_empenho:

            transferencia_empenho = (
                gap_prefeito *
                empenho_fator
            )

            transferencia_empenho = max(
                transferencia_empenho,
                0
            )

        else:

            transferencia_empenho = 0


        # ====================================================
        # 5. GAP RESTANTE APÓS EMPENHO
        # ====================================================

        gap_apos_empenho = max(
            gap_prefeito -
            transferencia_empenho,
            0
        )


        # ====================================================
        # 6. AVALIAÇÃO — OPCIONAL
        #
        # A avaliação atua sobre o que RESTOU do gap.
        #
        # Isso significa que avaliação desligada ou = 0
        # NÃO apaga o efeito do empenho.
        # ====================================================

        if usar_avaliacao:

            transferencia_avaliacao = (
                gap_apos_empenho *
                avaliacao_fator
            )

            transferencia_avaliacao = max(
                transferencia_avaliacao,
                0
            )

        else:

            transferencia_avaliacao = 0


        # ====================================================
        # 7. EFEITO TOTAL DO PREFEITO
        # ====================================================

        transferencia_prefeito = (
            transferencia_empenho +
            transferencia_avaliacao
        )


        # ====================================================
        # 8. RESULTADO APÓS PREFEITO
        # ====================================================

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

        # Prefeito desligado:
        # cenário permanece igual ao ponto inicial.

        joao_apos_prefeito = joao_inicial
        raquel_apos_prefeito = raquel_inicial


    # ========================================================
    # 9. LULA — OPCIONAL
    # ========================================================

    gap_lula_bruto = 0
    gap_lula = 0
    transferencia_lula = 0


    if usar_lula:

        # ----------------------------------------------------
        # GAP AUTOMÁTICO
        #
        # Lula
        # -
        # esquerda depois de tudo que veio antes
        # ----------------------------------------------------

        gap_lula_bruto = (
            pct_lula -
            joao_apos_prefeito
        )

        gap_lula = max(
            gap_lula_bruto,
            0
        )


        # ----------------------------------------------------
        # Transferência
        # ----------------------------------------------------

        transferencia_lula = (
            gap_lula *
            lula_fator
        )

        transferencia_lula = max(
            transferencia_lula,
            0
        )


    # ========================================================
    # 10. RESULTADO FINAL
    # ========================================================

    joao_final = limitar(
        joao_apos_prefeito +
        transferencia_lula
    )

    raquel_final = (
        100 -
        joao_final
    )


    # ========================================================
    # RETORNO
    # ========================================================

    return {

        # Estado
        "joao_estado": joao_estado,
        "raquel_estado": raquel_estado,

        # Município
        "usar_base_municipal": usar_base_municipal,
        "esquerda_municipio": esquerda_municipio,
        "direita_municipio": direita_municipio,
        "diferencial_municipal": diferencial_municipal,

        # Inicial
        "joao_inicial": joao_inicial,
        "raquel_inicial": raquel_inicial,

        # Prefeito
        "usar_prefeito": usar_prefeito,
        "candidato_apoiado": candidato_apoiado,
        "base_apoiado": base_apoiado,
        "pct_prefeito": pct_prefeito,

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

        # Total prefeito
        "transferencia_prefeito": transferencia_prefeito,

        # Após prefeito
        "joao_apos_prefeito": joao_apos_prefeito,
        "raquel_apos_prefeito": raquel_apos_prefeito,

        # Lula
        "usar_lula": usar_lula,
        "pct_lula": pct_lula,
        "gap_lula_bruto": gap_lula_bruto,
        "gap_lula": gap_lula,
        "lula_fator": lula_fator,
        "transferencia_lula": transferencia_lula,

        # Final
        "joao_final": joao_final,
        "raquel_final": raquel_final
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
        value=True,
        help=(
            "Se desligado, o município começa diretamente "
            "com a Base 0 de Pernambuco."
        )
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

    else:

        esquerda_municipio = joao_estado
        direita_municipio = raquel_estado

        st.info(
            "Base municipal desativada. "
            "O cálculo parte diretamente da Base 0 estadual."
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


    # Defaults necessários mesmo quando desligado
    pct_prefeito = 0.0
    lado_prefeito = "Esquerda — João Campos"

    usar_empenho = False
    usar_avaliacao = False

    categoria_empenho = "Muito fraco"
    categoria_avaliacao = "Muito fraco"

    empenho_fator = 0.0
    avaliacao_fator = 0.0


    if usar_prefeito:

        c1, c2 = st.columns(2)

        with c1:

            pct_prefeito = st.number_input(
                "Votação do prefeito (%)",
                min_value=0.0,
                max_value=100.0,
                value=65.0,
                step=0.1
            )

        with c2:

            lado_prefeito = st.selectbox(
                "Quem o prefeito apoia?",
                [
                    "Esquerda — João Campos",
                    "Direita — Raquel Lyra"
                ]
            )


        # ====================================================
        # EMPENHO E AVALIAÇÃO
        # ====================================================

        p1, p2 = st.columns(2)


        # ----------------------------------------------------
        # EMPENHO
        # ----------------------------------------------------

        with p1:

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

            else:

                empenho_fator = 0.0

                st.caption(
                    "Empenho não será considerado."
                )


        # ----------------------------------------------------
        # AVALIAÇÃO
        # ----------------------------------------------------

        with p2:

            st.subheader("Avaliação")

            usar_avaliacao = st.toggle(
                "Usar avaliação",
                value=True
            )


            if usar_avaliacao:

                categoria_avaliacao = st.selectbox(
                    "Nível de avaliação",
                    CATEGORIAS,
                    index=2
                )

                avaliacao_fator = st.session_state[
                    f"param_avaliacao_{categoria_avaliacao}"
                ]

                st.metric(
                    "Fator",
                    f"{avaliacao_fator:.2f}"
                )

            else:

                avaliacao_fator = 0.0

                st.caption(
                    "Avaliação não será considerada."
                )

    else:

        st.info(
            "O efeito do prefeito foi desativado. "
            "Empenho e avaliação também não entram no cálculo."
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
    categoria_lula = "Muito fraco"
    lula_fator = 0.0


    if usar_lula:

        l1, l2 = st.columns(2)


        with l1:

            pct_lula = st.number_input(
                "Votação de Lula no município (%)",
                min_value=0.0,
                max_value=100.0,
                value=70.0,
                step=0.1
            )


        with l2:

            categoria_lula = st.selectbox(
                "Intensidade do efeito de Lula",
                CATEGORIAS,
                index=2
            )

            lula_fator = st.session_state[
                f"param_lula_{categoria_lula}"
            ]

            st.metric(
                "Fator",
                f"{lula_fator:.2f}"
            )


        st.caption(
            "O gap de Lula é calculado automaticamente em relação "
            "ao resultado da esquerda após os efeitos anteriores."
        )

    else:

        st.info(
            "Lula não será considerado no cálculo."
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

        usar_prefeito=usar_prefeito,
        pct_prefeito=pct_prefeito,
        lado_prefeito=lado_prefeito,

        usar_empenho=usar_empenho,
        empenho_fator=empenho_fator,

        usar_avaliacao=usar_avaliacao,
        avaliacao_fator=avaliacao_fator,

        usar_lula=usar_lula,
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
            "As bases utilizadas precisam ter soma maior que zero."
        )

    else:

        r1, r2 = st.columns(2)

        r1.metric(
            "João Campos",
            f"{resultado['joao_final']:.2f}%"
        )

        r2.metric(
            "Raquel Lyra",
            f"{resultado['raquel_final']:.2f}%"
        )


        st.progress(
            resultado["joao_final"] / 100,
            text=(
                f"João {resultado['joao_final']:.1f}% "
                f"× Raquel {resultado['raquel_final']:.1f}%"
            )
        )


        # ====================================================
        # RESUMO DOS EFEITOS
        # ====================================================

        st.subheader("Efeitos considerados")

        resumo1, resumo2, resumo3 = st.columns(3)


        with resumo1:

            st.metric(
                "Ponto de partida",
                f"{resultado['joao_inicial']:.2f}%",
                help="Percentual inicial de João no município."
            )


        with resumo2:

            st.metric(
                "Efeito do prefeito",
                f"{resultado['transferencia_prefeito']:+.2f} p.p."
                if lado_prefeito == "Esquerda — João Campos"
                else f"{-resultado['transferencia_prefeito']:+.2f} p.p.",
                help=(
                    "Positivo representa movimento para João; "
                    "negativo representa movimento para Raquel."
                )
            )


        with resumo3:

            st.metric(
                "Efeito de Lula",
                f"{resultado['transferencia_lula']:+.2f} p.p."
            )


        # ====================================================
        # MEMÓRIA DE CÁLCULO
        # ====================================================

        st.divider()

        st.header("Memória de cálculo")


        # ----------------------------------------------------
        # PONTO DE PARTIDA
        # ----------------------------------------------------

        with st.expander(
            "1. Ponto de partida",
            expanded=True
        ):

            st.write(
                f"Base 0 Pernambuco: "
                f"**João {resultado['joao_estado']:.2f}% × "
                f"Raquel {resultado['raquel_estado']:.2f}%**"
            )


            if resultado["usar_base_municipal"]:

                st.write(
                    f"Base municipal: "
                    f"**Esquerda "
                    f"{resultado['esquerda_municipio']:.2f}% × "
                    f"Direita "
                    f"{resultado['direita_municipio']:.2f}%**"
                )

                st.write(
                    f"Diferença municipal da esquerda: "
                    f"**{resultado['diferencial_municipal']:+.2f} p.p.**"
                )

            else:

                st.info(
                    "A base municipal não foi utilizada."
                )


            st.write(
                f"Ponto de partida: "
                f"**João {resultado['joao_inicial']:.2f}% × "
                f"Raquel {resultado['raquel_inicial']:.2f}%**"
            )


        # ----------------------------------------------------
        # PREFEITO
        # ----------------------------------------------------

        with st.expander(
            "2. Prefeito",
            expanded=True
        ):

            if not resultado["usar_prefeito"]:

                st.info(
                    "O efeito do prefeito não foi utilizado."
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

                st.write(
                    f"Gap positivo disponível: "
                    f"**{resultado['gap_prefeito']:.2f} p.p.**"
                )


                # EMPENHO

                if resultado["usar_empenho"]:

                    st.write(
                        f"Empenho: **{categoria_empenho} "
                        f"({resultado['empenho_fator']:.2f})**"
                    )

                    st.code(
                        f"{resultado['gap_prefeito']:.2f} "
                        f"× {resultado['empenho_fator']:.2f} "
                        f"= {resultado['transferencia_empenho']:.2f} p.p."
                    )

                else:

                    st.write(
                        "**Empenho:** não utilizado."
                    )


                # AVALIAÇÃO

                if resultado["usar_avaliacao"]:

                    st.write(
                        f"Gap restante após empenho: "
                        f"**{resultado['gap_apos_empenho']:.2f} p.p.**"
                    )

                    st.write(
                        f"Avaliação: **{categoria_avaliacao} "
                        f"({resultado['avaliacao_fator']:.2f})**"
                    )

                    st.code(
                        f"{resultado['gap_apos_empenho']:.2f} "
                        f"× {resultado['avaliacao_fator']:.2f} "
                        f"= "
                        f"{resultado['transferencia_avaliacao']:.2f} p.p."
                    )

                else:

                    st.write(
                        "**Avaliação:** não utilizada."
                    )


                st.success(
                    f"Efeito total do prefeito: "
                    f"{resultado['transferencia_prefeito']:.2f} p.p. "
                    f"para {resultado['candidato_apoiado']}."
                )


        # ----------------------------------------------------
        # RESULTADO ANTES DE LULA
        # ----------------------------------------------------

        with st.expander(
            "3. Resultado antes de Lula",
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
            "4. Lula",
            expanded=True
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
                    f"- {resultado['joao_apos_prefeito']:.2f} "
                    f"= {resultado['gap_lula_bruto']:.2f} p.p."
                )


                if resultado["gap_lula"] <= 0:

                    st.info(
                        "O gap é zero ou negativo. "
                        "Lula não acrescenta votos ao cenário."
                    )

                else:

                    st.write(
                        f"Gap positivo: "
                        f"**{resultado['gap_lula']:.2f} p.p.**"
                    )

                    st.write(
                        f"Intensidade: **{categoria_lula} "
                        f"({resultado['lula_fator']:.2f})**"
                    )

                    st.code(
                        f"{resultado['gap_lula']:.2f} "
                        f"× {resultado['lula_fator']:.2f} "
                        f"= {resultado['transferencia_lula']:.2f} p.p."
                    )

                    st.success(
                        f"Efeito de Lula sobre João: "
                        f"+{resultado['transferencia_lula']:.2f} p.p."
                    )


# ============================================================
# ABA 2 — CONFIGURAÇÃO DOS PARÂMETROS
# ============================================================

with aba_parametros:

    st.header("Configurar parâmetros")

    st.write(
        "Cada variável possui sua própria escala. "
        "Os valores sugeridos podem ser alterados livremente."
    )

    st.info(
        "As alterações valem apenas para esta sessão. "
        "Nenhum parâmetro é salvo em banco de dados."
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
        "Quanto do gap disponível é mobilizado pelo empenho."
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

        st.rerun()


    st.caption(
        "Sugestões iniciais: "
        "Muito fraco = 0,00 | "
        "Fraco = 0,10 | "
        "Moderado = 0,50 | "
        "Forte = 0,80 | "
        "Muito forte = 1,00."
    )
