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

    total = esquerda + direita

    if total <= 0:
        return None, None

    return (
        esquerda / total * 100,
        direita / total * 100
    )


# ============================================================
# PARÂMETROS PADRÃO DO EXCEL
# ============================================================

PARAMETROS_PADRAO = {
    "Muito fraco": 0.00,
    "Fraco": 0.10,
    "Moderado": 0.50,
    "Forte": 0.80,
    "Muito forte": 1.00
}


# ============================================================
# INICIALIZAR PARÂMETROS NA SESSÃO
#
# Eles começam com os valores do Excel, mas podem ser
# alterados pelo usuário.
# ============================================================

for nome, valor in PARAMETROS_PADRAO.items():

    chave = f"param_{nome}"

    if chave not in st.session_state:
        st.session_state[chave] = valor


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
    # 3. AJUSTE MUNICIPAL
    #
    # A diferença entre a esquerda municipal e a estadual
    # ajusta o ponto de partida local.
    #
    # Exemplo:
    #
    # João Estado = 56
    # Esquerda município = 67
    #
    # diferença = +11
    #
    # João local = 67
    # ========================================================

    diferencial_municipal = (
        esquerda_municipio -
        joao_estado
    )

    joao_inicial = limitar(
        joao_estado +
        diferencial_municipal
    )

    raquel_inicial = (
        100 -
        joao_inicial
    )


    # ========================================================
    # 4. IDENTIFICAR O CANDIDATO APOIADO PELO PREFEITO
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
    # votação prefeito - base do candidato apoiado
    #
    # Só utilizamos valores positivos.
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
    # O fator vem da escala:
    #
    # Muito fraco = 0.00
    # Fraco       = 0.10
    # Moderado    = 0.50
    # Forte       = 0.80
    # Muito forte = 1.00
    #
    # Exemplo:
    #
    # gap = 20
    # empenho = Forte = 0.80
    #
    # 20 × 0.80 = 16 p.p.
    # ========================================================

    transferencia_empenho = (
        gap_prefeito *
        empenho_fator
    )


    # ========================================================
    # 7. AVALIAÇÃO
    #
    # A avaliação também usa a escala configurável.
    #
    # Ela atua SOBRE A TRANSFERÊNCIA.
    #
    # Exemplo:
    #
    # transferência após empenho = 16
    # avaliação = Moderado = 0.50
    #
    # 16 × 0.50 = 8 p.p.
    # ========================================================

    transferencia_prefeito_bruta = (
        transferencia_empenho *
        avaliacao_fator
    )


    # --------------------------------------------------------
    # Não permitir transferência maior que o gap disponível
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
    # AUTOMÁTICO:
    #
    # Lula no município
    # -
    # esquerda após as transferências anteriores
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
    # 10. TRANSFERÊNCIA DE LULA
    #
    # O GAP é automático.
    #
    # O fator determina quanto desse gap é aproveitado.
    #
    # Também utiliza a escala:
    #
    # Muito fraco
    # Fraco
    # Moderado
    # Forte
    # Muito forte
    # ========================================================

    transferencia_lula = (
        gap_lula *
        lula_fator
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

        # Estado
        "joao_estado": joao_estado,
        "raquel_estado": raquel_estado,

        # Município
        "esquerda_municipio": esquerda_municipio,
        "direita_municipio": direita_municipio,
        "diferencial_municipal": diferencial_municipal,

        # Ponto inicial
        "joao_inicial": joao_inicial,
        "raquel_inicial": raquel_inicial,

        # Prefeito
        "candidato_apoiado": candidato_apoiado,
        "pct_prefeito": pct_prefeito,
        "base_apoiado": base_apoiado,

        "gap_prefeito_bruto": gap_prefeito_bruto,
        "gap_prefeito": gap_prefeito,

        # Empenho
        "empenho_fator": empenho_fator,
        "transferencia_empenho": transferencia_empenho,

        # Avaliação
        "avaliacao_fator": avaliacao_fator,
        "transferencia_prefeito_bruta":
            transferencia_prefeito_bruta,

        "transferencia_prefeito":
            transferencia_prefeito,

        # Após prefeito
        "joao_apos_prefeito": joao_apos_prefeito,
        "raquel_apos_prefeito": raquel_apos_prefeito,

        # Lula
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

    st.header("Dados do cenário")

    st.caption(
        "Informe os dados eleitorais do município "
        "e escolha a intensidade de cada efeito."
    )


    # ========================================================
    # DADOS
    # ========================================================

    col1, col2, col3 = st.columns(3)


    # --------------------------------------------------------
    # BASE 0 ESTADUAL
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
        "Escolha a categoria. O valor correspondente pode ser "
        "alterado na aba “Configurar parâmetros”."
    )

    i1, i2, i3 = st.columns(3)


    # --------------------------------------------------------
    # EMPENHO
    # --------------------------------------------------------

    with i1:

        st.subheader("Empenho do prefeito")

        categoria_empenho = st.selectbox(
            "Nível de empenho",
            list(PARAMETROS_PADRAO.keys()),
            index=3,  # Forte
            key="categoria_empenho"
        )

        empenho_fator = st.session_state[
            f"param_{categoria_empenho}"
        ]

        st.metric(
            "Fator aplicado",
            f"{empenho_fator:.2f}"
        )


    # --------------------------------------------------------
    # AVALIAÇÃO
    # --------------------------------------------------------

    with i2:

        st.subheader("Avaliação do prefeito")

        categoria_avaliacao = st.selectbox(
            "Nível de avaliação",
            list(PARAMETROS_PADRAO.keys()),
            index=2,  # Moderado
            key="categoria_avaliacao"
        )

        avaliacao_fator = st.session_state[
            f"param_{categoria_avaliacao}"
        ]

        st.metric(
            "Fator aplicado",
            f"{avaliacao_fator:.2f}"
        )


    # --------------------------------------------------------
    # LULA
    # --------------------------------------------------------

    with i3:

        st.subheader("Efeito de Lula")

        categoria_lula = st.selectbox(
            "Intensidade da transferência",
            list(PARAMETROS_PADRAO.keys()),
            index=2,  # Moderado
            key="categoria_lula"
        )

        lula_fator = st.session_state[
            f"param_{categoria_lula}"
        ]

        st.metric(
            "Fator aplicado",
            f"{lula_fator:.2f}"
        )

        st.caption(
            "O gap de Lula é calculado automaticamente."
        )


    # ========================================================
    # CALCULAR
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
            "As bases estadual e municipal precisam "
            "ter soma maior que zero."
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

            st.markdown("**Base municipal**")

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


        # ====================================================
        # MEMÓRIA DE CÁLCULO
        # ====================================================

        st.divider()

        st.header("Memória de cálculo")


        # ----------------------------------------------------
        # AJUSTE MUNICIPAL
        # ----------------------------------------------------

        with st.expander(
            "1. Base estadual e ajuste municipal",
            expanded=True
        ):

            st.write(
                f"Base estadual de João: "
                f"**{resultado['joao_estado']:.2f}%**"
            )

            st.write(
                f"Base municipal da esquerda: "
                f"**{resultado['esquerda_municipio']:.2f}%**"
            )

            st.write(
                f"Diferença municipal: "
                f"**{resultado['diferencial_municipal']:+.2f} p.p.**"
            )

            st.write(
                f"Ponto de partida de João no município: "
                f"**{resultado['joao_inicial']:.2f}%**"
            )

            st.write(
                f"Ponto de partida de Raquel no município: "
                f"**{resultado['raquel_inicial']:.2f}%**"
            )


        # ----------------------------------------------------
        # PREFEITO
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
                    "O prefeito não possui votos adicionais "
                    "para transferir."
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
            "3. Empenho",
            expanded=True
        ):

            st.write(
                f"Categoria: **{categoria_empenho}**"
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


        # ----------------------------------------------------
        # AVALIAÇÃO
        # ----------------------------------------------------

        with st.expander(
            "4. Avaliação",
            expanded=True
        ):

            st.write(
                f"Categoria: **{categoria_avaliacao}**"
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
                f"{resultado['transferencia_prefeito_bruta']:.2f} p.p."
            )

            st.success(
                f"Transferência efetiva do prefeito: "
                f"{resultado['transferencia_prefeito']:.2f} p.p."
            )


        # ----------------------------------------------------
        # RESULTADO ANTES DE LULA
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
                f"Esquerda após as transferências anteriores: "
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
                    f"Gap positivo: "
                    f"**{resultado['gap_lula']:.2f} p.p.**"
                )

                st.write(
                    f"Intensidade: "
                    f"**{categoria_lula}**"
                )

                st.write(
                    f"Fator: "
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
                    f"Transferência de Lula para João: "
                    f"{resultado['transferencia_lula']:.2f} p.p."
                )


# ============================================================
# ABA 2 — CONFIGURAÇÃO DOS PARÂMETROS
# ============================================================

with aba_parametros:

    st.header("Configurar parâmetros")

    st.write(
        "Os valores abaixo são os fatores associados às "
        "categorias utilizadas no simulador."
    )

    st.info(
        "As alterações valem apenas enquanto esta sessão "
        "da aplicação estiver aberta. Nenhum valor é salvo "
        "em banco de dados."
    )


    # ========================================================
    # EDITORES
    # ========================================================

    c1, c2, c3, c4, c5 = st.columns(5)


    with c1:

        st.markdown("#### Muito fraco")

        st.number_input(
            "Fator",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            format="%.2f",
            key="param_Muito fraco"
        )


    with c2:

        st.markdown("#### Fraco")

        st.number_input(
            "Fator",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            format="%.2f",
            key="param_Fraco"
        )


    with c3:

        st.markdown("#### Moderado")

        st.number_input(
            "Fator",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            format="%.2f",
            key="param_Moderado"
        )


    with c4:

        st.markdown("#### Forte")

        st.number_input(
            "Fator",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            format="%.2f",
            key="param_Forte"
        )


    with c5:

        st.markdown("#### Muito forte")

        st.number_input(
            "Fator",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            format="%.2f",
            key="param_Muito forte"
        )


    # ========================================================
    # TABELA ATUAL
    # ========================================================

    st.divider()

    st.subheader("Escala atualmente utilizada")

    st.dataframe(
        {
            "Categoria": [
                "Muito fraco",
                "Fraco",
                "Moderado",
                "Forte",
                "Muito forte"
            ],

            "Fator": [
                st.session_state["param_Muito fraco"],
                st.session_state["param_Fraco"],
                st.session_state["param_Moderado"],
                st.session_state["param_Forte"],
                st.session_state["param_Muito forte"]
            ]
        },
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # RESTAURAR PADRÕES
    # ========================================================

    if st.button(
        "Restaurar valores sugeridos",
        type="secondary"
    ):

        for nome, valor in PARAMETROS_PADRAO.items():

            st.session_state[
                f"param_{nome}"
            ] = valor

        st.rerun()


    st.caption(
        "Valores sugeridos: Muito fraco = 0,00 | "
        "Fraco = 0,10 | Moderado = 0,50 | "
        "Forte = 0,80 | Muito forte = 1,00."
    )
