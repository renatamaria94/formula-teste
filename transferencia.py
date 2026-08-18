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
st.caption("João Campos x Raquel Lyra")



# ============================================================
# ELEITORADO MUNICIPAL - DADOS INCORPORADOS AO CÓDIGO
# Fonte original: eleitores_percentual.xlsx
# "percentual" = participação percentual do município
# no eleitorado total de Pernambuco. Soma = 100%.
# O aplicativo NÃO precisa do XLSX para funcionar.
# ============================================================

ELEITORADO_MUNICIPIOS = {
    'Abreu e Lima': {"mesorregiao": 'Metropolitana do Recife', "eleitores": 79490, "percentual": 1.099906945852},
    'Afogados da Ingazeira': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 30184, "percentual": 0.417657456958},
    'Afrânio': {"mesorregiao": 'São Francisco Pernambucano', "eleitores": 17564, "percentual": 0.243033911145},
    'Agrestina': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 20957, "percentual": 0.289983015024},
    'Água Preta': {"mesorregiao": 'Mata Pernambucana', "eleitores": 20245, "percentual": 0.280131036845},
    'Águas Belas': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 35345, "percentual": 0.489070461708},
    'Alagoinha': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 12093, "percentual": 0.167331421515},
    'Aliança': {"mesorregiao": 'Mata Pernambucana', "eleitores": 29251, "percentual": 0.404747491170},
    'Altinho': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 17314, "percentual": 0.239574649144},
    'Amaraji': {"mesorregiao": 'Mata Pernambucana', "eleitores": 17398, "percentual": 0.240736961177},
    'Angelim': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 9131, "percentual": 0.126346085326},
    'Araçoiaba': {"mesorregiao": 'Metropolitana do Recife', "eleitores": 17440, "percentual": 0.241318117193},
    'Araripina': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 60214, "percentual": 0.833184008524},
    'Arcoverde': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 51898, "percentual": 0.718115117321},
    'Barra de Guabiraba': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 10121, "percentual": 0.140044762850},
    'Barreiros': {"mesorregiao": 'Mata Pernambucana', "eleitores": 30558, "percentual": 0.422832512912},
    'Belém de Maria': {"mesorregiao": 'Mata Pernambucana', "eleitores": 9188, "percentual": 0.127134797062},
    'Belém do São Francisco': {"mesorregiao": 'São Francisco Pernambucano', "eleitores": 15650, "percentual": 0.216549801265},
    'Belo Jardim': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 60970, "percentual": 0.843644816815},
    'Betânia': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 10119, "percentual": 0.140017088754},
    'Bezerros': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 48387, "percentual": 0.669533241778},
    'Bodocó': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 27882, "percentual": 0.385804572453},
    'Bom Conselho': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 34234, "percentual": 0.473697501375},
    'Bom Jardim': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 30693, "percentual": 0.424700514392},
    'Bonito': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 30776, "percentual": 0.425848989377},
    'Brejão': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 9711, "percentual": 0.134371573169},
    'Brejinho': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 7824, "percentual": 0.108261063585},
    'Brejo da Madre de Deus': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 36312, "percentual": 0.502450887128},
    'Buenos Aires': {"mesorregiao": 'Mata Pernambucana', "eleitores": 12015, "percentual": 0.166252131770},
    'Buíque': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 42648, "percentual": 0.590122423282},
    'Cabo de Santo Agostinho': {"mesorregiao": 'Metropolitana do Recife', "eleitores": 171662, "percentual": 2.375295334493},
    'Cabrobó': {"mesorregiao": 'São Francisco Pernambucano', "eleitores": 25755, "percentual": 0.356373171348},
    'Cachoeirinha': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 16110, "percentual": 0.222914843347},
    'Caetés': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 20698, "percentual": 0.286399219590},
    'Calçado': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 7911, "percentual": 0.109464886761},
    'Calumbi': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 7399, "percentual": 0.102380318183},
    'Camaragibe': {"mesorregiao": 'Metropolitana do Recife', "eleitores": 127008, "percentual": 1.757415792915},
    'Camocim de São Félix': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 15660, "percentual": 0.216688171745},
    'Camutanga': {"mesorregiao": 'Mata Pernambucana', "eleitores": 7347, "percentual": 0.101660791687},
    'Canhotinho': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 17189, "percentual": 0.237845018144},
    'Capoeiras': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 16561, "percentual": 0.229155351997},
    'Carnaíba': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 16933, "percentual": 0.234302733855},
    'Carnaubeira da Penha': {"mesorregiao": 'São Francisco Pernambucano', "eleitores": 12616, "percentual": 0.174568197621},
    'Carpina': {"mesorregiao": 'Mata Pernambucana', "eleitores": 60140, "percentual": 0.832160066971},
    'Caruaru': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 254240, "percentual": 3.517931084582},
    'Casinhas': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 12103, "percentual": 0.167469791995},
    'Catende': {"mesorregiao": 'Mata Pernambucana', "eleitores": 25942, "percentual": 0.358960699324},
    'Cedro': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 10210, "percentual": 0.141276260123},
    'Chã de Alegria': {"mesorregiao": 'Mata Pernambucana', "eleitores": 11611, "percentual": 0.160661964377},
    'Chã Grande': {"mesorregiao": 'Mata Pernambucana', "eleitores": 18879, "percentual": 0.261229629271},
    'Condado': {"mesorregiao": 'Mata Pernambucana', "eleitores": 19804, "percentual": 0.274028898675},
    'Correntes': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 14608, "percentual": 0.202131597245},
    'Cortês': {"mesorregiao": 'Mata Pernambucana', "eleitores": 11278, "percentual": 0.156054227391},
    'Cumaru': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 14530, "percentual": 0.201052307501},
    'Cupira': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 19894, "percentual": 0.275274232995},
    'Custódia': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 29706, "percentual": 0.411043348012},
    'Dormentes': {"mesorregiao": 'São Francisco Pernambucano', "eleitores": 16200, "percentual": 0.224160177668},
    'Escada': {"mesorregiao": 'Mata Pernambucana', "eleitores": 48289, "percentual": 0.668177211074},
    'Exu': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 29308, "percentual": 0.405536202906},
    'Feira Nova': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 18056, "percentual": 0.249841738763},
    'Ferreiros': {"mesorregiao": 'Mata Pernambucana', "eleitores": 10158, "percentual": 0.140556733626},
    'Flores': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 16581, "percentual": 0.229432092957},
    'Floresta': {"mesorregiao": 'São Francisco Pernambucano', "eleitores": 25424, "percentual": 0.351793108458},
    'Frei Miguelinho': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 12953, "percentual": 0.179231282798},
    'Gameleira': {"mesorregiao": 'Mata Pernambucana', "eleitores": 14911, "percentual": 0.206324222790},
    'Garanhuns': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 99649, "percentual": 1.378847996568},
    'Glória do Goitá': {"mesorregiao": 'Mata Pernambucana', "eleitores": 23493, "percentual": 0.325073768762},
    'Goiana': {"mesorregiao": 'Mata Pernambucana', "eleitores": 67178, "percentual": 0.929545210825},
    'Granito': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 6963, "percentual": 0.096347365253},
    'Gravatá': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 67957, "percentual": 0.940324271220},
    'Iati': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 16338, "percentual": 0.226069690292},
    'Ibimirim': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 21782, "percentual": 0.301398579627},
    'Ibirajuba': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 6827, "percentual": 0.094465526725},
    'Igarassu': {"mesorregiao": 'Metropolitana do Recife', "eleitores": 89979, "percentual": 1.245043742368},
    'Iguaracy': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 9134, "percentual": 0.126387596470},
    'Ilha de Itamaracá': {"mesorregiao": 'Metropolitana do Recife', "eleitores": 18630, "percentual": 0.257784204318},
    'Inajá': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 15927, "percentual": 0.220382663563},
    'Ingazeira': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 4256, "percentual": 0.058890476306},
    'Ipojuca': {"mesorregiao": 'Metropolitana do Recife', "eleitores": 89251, "percentual": 1.234970371421},
    'Ipubi': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 24842, "percentual": 0.343739946520},
    'Itacuruba': {"mesorregiao": 'São Francisco Pernambucano', "eleitores": 4774, "percentual": 0.066058067172},
    'Itaíba': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 21207, "percentual": 0.293442277025},
    'Itambé': {"mesorregiao": 'Mata Pernambucana', "eleitores": 24489, "percentual": 0.338855468574},
    'Itapetim': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 11981, "percentual": 0.165781672138},
    'Itapissuma': {"mesorregiao": 'Metropolitana do Recife', "eleitores": 21460, "percentual": 0.296943050170},
    'Itaquitinga': {"mesorregiao": 'Mata Pernambucana', "eleitores": 12852, "percentual": 0.177833740950},
    'Jaboatão dos Guararapes': {"mesorregiao": 'Metropolitana do Recife', "eleitores": 498190, "percentual": 6.893478945202},
    'Jaqueira': {"mesorregiao": 'Mata Pernambucana', "eleitores": 9239, "percentual": 0.127840486511},
    'Jataúba': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 15841, "percentual": 0.219192677434},
    'Jatobá': {"mesorregiao": 'São Francisco Pernambucano', "eleitores": 11644, "percentual": 0.161118586961},
    'João Alfredo': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 24788, "percentual": 0.342992745928},
    'Joaquim Nabuco': {"mesorregiao": 'Mata Pernambucana', "eleitores": 14138, "percentual": 0.195628184683},
    'Jucati': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 10188, "percentual": 0.140971845067},
    'Jupi': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 13030, "percentual": 0.180296735494},
    'Jurema': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 12388, "percentual": 0.171413350676},
    'Lagoa de Itaenga': {"mesorregiao": 'Mata Pernambucana', "eleitores": 18519, "percentual": 0.256248291989},
    'Lagoa do Carro': {"mesorregiao": 'Mata Pernambucana', "eleitores": 15737, "percentual": 0.217753624442},
    'Lagoa do Ouro': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 12060, "percentual": 0.166874798930},
    'Lagoa dos Gatos': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 11212, "percentual": 0.155140982223},
    'Lagoa Grande': {"mesorregiao": 'São Francisco Pernambucano', "eleitores": 20682, "percentual": 0.286177826822},
    'Lajedo': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 32480, "percentual": 0.449427319176},
    'Limoeiro': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 45675, "percentual": 0.632007167591},
    'Macaparana': {"mesorregiao": 'Mata Pernambucana', "eleitores": 20068, "percentual": 0.277681879348},
    'Machados': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 11132, "percentual": 0.154034018383},
    'Manari': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 14259, "percentual": 0.197302467492},
    'Maraial': {"mesorregiao": 'Mata Pernambucana', "eleitores": 8012, "percentual": 0.110862428609},
    'Mirandiba': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 11993, "percentual": 0.165947716714},
    'Moreilândia': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 9954, "percentual": 0.137733975834},
    'Moreno': {"mesorregiao": 'Metropolitana do Recife', "eleitores": 48840, "percentual": 0.675801424524},
    'Nazaré da Mata': {"mesorregiao": 'Mata Pernambucana', "eleitores": 25711, "percentual": 0.355764341235},
    'Olinda': {"mesorregiao": 'Metropolitana do Recife', "eleitores": 301760, "percentual": 4.175467605741},
    'Orobó': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 18360, "percentual": 0.254048201357},
    'Orocó': {"mesorregiao": 'São Francisco Pernambucano', "eleitores": 12506, "percentual": 0.173046122340},
    'Ouricuri': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 48673, "percentual": 0.673490637507},
    'Palmares': {"mesorregiao": 'Mata Pernambucana', "eleitores": 40929, "percentual": 0.566336537763},
    'Palmeirina': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 6520, "percentual": 0.090217552987},
    'Panelas': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 19630, "percentual": 0.271621252322},
    'Paranatama': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 11960, "percentual": 0.165491094130},
    'Parnamirim': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 18599, "percentual": 0.257355255830},
    'Passira': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 26193, "percentual": 0.362433798373},
    'Paudalho': {"mesorregiao": 'Mata Pernambucana', "eleitores": 45882, "percentual": 0.634871436528},
    'Paulista': {"mesorregiao": 'Metropolitana do Recife', "eleitores": 237143, "percentual": 3.281359074855},
    'Pedra': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 18769, "percentual": 0.259707553990},
    'Pesqueira': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 52577, "percentual": 0.727510472916},
    'Petrolândia': {"mesorregiao": 'São Francisco Pernambucano', "eleitores": 26557, "percentual": 0.367470483847},
    'Petrolina': {"mesorregiao": 'São Francisco Pernambucano', "eleitores": 248232, "percentual": 3.434798100173},
    'Poção': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 10344, "percentual": 0.143130424555},
    'Pombos': {"mesorregiao": 'Mata Pernambucana', "eleitores": 20463, "percentual": 0.283147513310},
    'Primavera': {"mesorregiao": 'Mata Pernambucana', "eleitores": 11012, "percentual": 0.152373572622},
    'Quipapá': {"mesorregiao": 'Mata Pernambucana', "eleitores": 15475, "percentual": 0.214128317865},
    'Quixaba': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 6231, "percentual": 0.086218646114},
    'Recife': {"mesorregiao": 'Metropolitana do Recife', "eleitores": 1228645, "percentual": 17.000819845094},
    'Riacho das Almas': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 20977, "percentual": 0.290259755984},
    'Ribeirão': {"mesorregiao": 'Mata Pernambucana', "eleitores": 28400, "percentual": 0.392972163319},
    'Rio Formoso': {"mesorregiao": 'Mata Pernambucana', "eleitores": 16963, "percentual": 0.234717845295},
    'Sairé': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 11293, "percentual": 0.156261783111},
    'Salgadinho': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 7158, "percentual": 0.099045589614},
    'Salgueiro': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 43593, "percentual": 0.603198433646},
    'Saloá': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 13683, "percentual": 0.189332327841},
    'Sanharó': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 16350, "percentual": 0.226235734868},
    'Santa Cruz': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 12836, "percentual": 0.177612348182},
    'Santa Cruz da Baixa Verde': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 9930, "percentual": 0.137401886681},
    'Santa Cruz do Capibaribe': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 66215, "percentual": 0.916220133597},
    'Santa Filomena': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 12113, "percentual": 0.167608162475},
    'Santa Maria da Boa Vista': {"mesorregiao": 'São Francisco Pernambucano', "eleitores": 30662, "percentual": 0.424271565904},
    'Santa Maria do Cambucá': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 11552, "percentual": 0.159845578544},
    'Santa Terezinha': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 8068, "percentual": 0.111637303298},
    'São Benedito do Sul': {"mesorregiao": 'Mata Pernambucana', "eleitores": 7843, "percentual": 0.108523967497},
    'São Bento do Una': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 38255, "percentual": 0.529336271400},
    'São Caitano': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 30915, "percentual": 0.427772339049},
    'São João': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 18196, "percentual": 0.251778925484},
    'São Joaquim do Monte': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 17655, "percentual": 0.244293082514},
    'São José da Coroa Grande': {"mesorregiao": 'Mata Pernambucana', "eleitores": 17814, "percentual": 0.246493173146},
    'São José do Belmonte': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 28448, "percentual": 0.393636341623},
    'São José do Egito': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 24191, "percentual": 0.334732028269},
    'São Lourenço da Mata': {"mesorregiao": 'Metropolitana do Recife', "eleitores": 83729, "percentual": 1.158562192342},
    'São Vicente Férrer': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 14583, "percentual": 0.201785671045},
    'Serra Talhada': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 63867, "percentual": 0.883730744883},
    'Serrita': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 17116, "percentual": 0.236834913640},
    'Sertânia': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 27510, "percentual": 0.380657190595},
    'Sirinhaém': {"mesorregiao": 'Mata Pernambucana', "eleitores": 28615, "percentual": 0.395947128640},
    'Solidão': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 5556, "percentual": 0.076878638711},
    'Surubim': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 48595, "percentual": 0.672411347763},
    'Tabira': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 21466, "percentual": 0.297026072458},
    'Tacaimbó': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 11018, "percentual": 0.152456594910},
    'Tacaratu': {"mesorregiao": 'São Francisco Pernambucano', "eleitores": 18272, "percentual": 0.252830541132},
    'Tamandaré': {"mesorregiao": 'Mata Pernambucana', "eleitores": 20316, "percentual": 0.281113467253},
    'Taquaritinga do Norte': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 22262, "percentual": 0.308040362669},
    'Terezinha': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 6636, "percentual": 0.091822650556},
    'Terra Nova': {"mesorregiao": 'São Francisco Pernambucano', "eleitores": 8871, "percentual": 0.122748452845},
    'Timbaúba': {"mesorregiao": 'Mata Pernambucana', "eleitores": 42106, "percentual": 0.582622743264},
    'Toritama': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 35242, "percentual": 0.487645245763},
    'Tracunhaém': {"mesorregiao": 'Mata Pernambucana', "eleitores": 12092, "percentual": 0.167317584467},
    'Trindade': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 25123, "percentual": 0.347628157009},
    'Triunfo': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 12233, "percentual": 0.169268608235},
    'Tupanatinga': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 16657, "percentual": 0.230483708606},
    'Tuparetama': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 8028, "percentual": 0.111083821378},
    'Venturosa': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 14828, "percentual": 0.205175747806},
    'Verdejante': {"mesorregiao": 'Sertão Pernambucano', "eleitores": 8435, "percentual": 0.116715499915},
    'Vertente do Lério': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 8321, "percentual": 0.115138076443},
    'Vertentes': {"mesorregiao": 'Agreste Pernambucano', "eleitores": 16750, "percentual": 0.231770554070},
    'Vicência': {"mesorregiao": 'Mata Pernambucana', "eleitores": 22289, "percentual": 0.308413962965},
    'Vitória de Santo Antão': {"mesorregiao": 'Mata Pernambucana', "eleitores": 103932, "percentual": 1.438112073170},
    'Xexéu': {"mesorregiao": 'Mata Pernambucana', "eleitores": 11221, "percentual": 0.155265515655},
}

TOTAL_ELEITORES_PE = sum(
    item["eleitores"] for item in ELEITORADO_MUNICIPIOS.values()
)

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
# FUNÇÃO - APLICAR PESQUISA
# ============================================================

# ============================================================
# FUNÇÃO - APLICAR PESQUISA
# A pesquisa pode aumentar OU reduzir João Campos
# ============================================================

def aplicar_pesquisa(
    joao_atual,
    raquel_atual,
    pesquisa_joao,
    pesquisa_raquel
):

    # --------------------------------------------------------
    # 1. NORMALIZA A PESQUISA
    # --------------------------------------------------------

    pesquisa_joao, pesquisa_raquel = normalizar(
        pesquisa_joao,
        pesquisa_raquel
    )

    if pesquisa_joao is None:
        return None


    # --------------------------------------------------------
    # 2. DIFERENÇA ENTRE PESQUISA E SIMULAÇÃO DE JOÃO
    #
    # Positivo = pesquisa melhora João
    # Negativo = pesquisa piora João
    # --------------------------------------------------------

    gap_bruto = (
        pesquisa_joao
        -
        joao_atual
    )


    # --------------------------------------------------------
    # 3. TAMANHO ABSOLUTO DO GAP
    #
    # A faixa do parâmetro depende do tamanho da diferença,
    # independentemente de ela ser positiva ou negativa.
    # --------------------------------------------------------

    gap_absoluto = abs(
        gap_bruto
    )


    faixa = None
    fator = 0.0
    efeito = 0.0


    # --------------------------------------------------------
    # 4. CALCULAR O EFEITO DA PESQUISA
    # --------------------------------------------------------

    if gap_absoluto > 0:

        fator, faixa = obter_fator_pesquisa(
            gap_absoluto
        )

        # IMPORTANTE:
        # usamos gap_bruto, e não gap_absoluto,
        # para preservar o sinal positivo ou negativo.
        efeito = (
            gap_bruto
            *
            fator
        )


    # --------------------------------------------------------
    # 5. APLICAR O EFEITO A JOÃO
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # 6. IDENTIFICAR DIREÇÃO DO EFEITO
    # --------------------------------------------------------

    if efeito > 0:

        direcao = "Positivo para João Campos"

    elif efeito < 0:

        direcao = "Negativo para João Campos"

    else:

        direcao = "Sem efeito"


    # --------------------------------------------------------
    # 7. RETORNO
    # --------------------------------------------------------

    return {

        "lider":
            (
                "João Campos"
                if pesquisa_joao > pesquisa_raquel
                else
                "Raquel Lyra"
                if pesquisa_raquel > pesquisa_joao
                else
                "Empate"
            ),

        "pesquisa_joao":
            pesquisa_joao,

        "pesquisa_raquel":
            pesquisa_raquel,

        # Mantidos para compatibilidade com o restante do app
        "pct_lider_pesquisa":
            pesquisa_joao,

        "pct_lider_simulacao":
            joao_atual,

        "gap_bruto":
            gap_bruto,

        "gap":
            gap_absoluto,

        "faixa":
            faixa,

        "fator":
            fator,

        "efeito":
            efeito,

        "direcao":
            direcao,

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
    pesquisa_raquel,

    # Peso do município no cenário estadual
    percentual_eleitores_municipio
):


    # ========================================================
    # 1. BASE 0 - PERNAMBUCO
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

        if lado_prefeito == "Esquerda - João Campos":

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
    # 9. IMPACTO DA TRANSFERÊNCIA MUNICIPAL EM PERNAMBUCO
    #
    # A transferência observada no município é convertida
    # em impacto estadual pelo percentual de eleitores do município
    # no eleitorado total de Pernambuco.
    # ========================================================

    # O percentual já representa quanto o município pesa
    # no eleitorado estadual. Convertemos % para proporção.
    peso_municipio_estado = (
        percentual_eleitores_municipio / 100
    )


    impacto_estado_joao = (
        variacao_municipal_joao
        *
        peso_municipio_estado
    )

    impacto_estado_raquel = (
        variacao_municipal_raquel
        *
        peso_municipio_estado
    )


    joao_estado_apos_transferencia = limitar(
        joao_estado
        +
        impacto_estado_joao
    )

    raquel_estado_apos_transferencia = (
        100
        -
        joao_estado_apos_transferencia
    )


    # Este é o cenário estadual antes de eventual
    # pesquisa estadual.
    joao_estado_antes_pesquisa = (
        joao_estado_apos_transferencia
    )

    raquel_estado_antes_pesquisa = (
        raquel_estado_apos_transferencia
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

        # Impacto do município em Pernambuco
        "percentual_eleitores_municipio":
            percentual_eleitores_municipio,

        "peso_municipio_estado":
            peso_municipio_estado,

        "impacto_estado_joao":
            impacto_estado_joao,

        "impacto_estado_raquel":
            impacto_estado_raquel,

        "joao_estado_apos_transferencia":
            joao_estado_apos_transferencia,

        "raquel_estado_apos_transferencia":
            raquel_estado_apos_transferencia,

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
# ABA - SIMULADOR
# ============================================================

with aba_simulador:


    # ========================================================
    # BASE 0 - PERNAMBUCO
    # ========================================================

    st.header("Base 0 - Pernambuco")

    st.caption(
        "Cenário estadual de referência."
    )


    c1, c2 = st.columns(2)


    with c1:

        joao_estado = st.number_input(
            "João Campos - Estado (%)",
            min_value=0.0,
            max_value=100.0,
            value=56.0,
            step=0.1
        )


    with c2:

        raquel_estado = st.number_input(
            "Raquel Lyra - Estado (%)",
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
    # PESO DO MUNICÍPIO EM PERNAMBUCO
    # ========================================================

    st.subheader("Peso do município em Pernambuco")

    municipios_lista = sorted(ELEITORADO_MUNICIPIOS.keys())

    municipio_selecionado = st.selectbox(
        "Município para ponderação estadual",
        municipios_lista,
        index=(
            municipios_lista.index("Sertânia")
            if "Sertânia" in municipios_lista
            else 0
        )
    )

    dados_eleitorado = ELEITORADO_MUNICIPIOS[
        municipio_selecionado
    ]

    percentual_eleitores_municipio = (
        dados_eleitorado["percentual"]
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Eleitores do município",
        f"{dados_eleitorado['eleitores']:,}".replace(",", ".")
    )

    c2.metric(
        "% dos eleitores de PE",
        f"{percentual_eleitores_municipio:.4f}%"
    )

    c3.metric(
        "Eleitores de Pernambuco",
        f"{TOTAL_ELEITORES_PE:,}".replace(",", ".")
    )

    st.caption(
        "O impacto da transferência municipal no cenário estadual "
        "é ponderado pela participação do município no eleitorado "
        "de Pernambuco. Os dados estão incorporados ao código."
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
    lado_prefeito = "Direita - Raquel Lyra"

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
                    "Esquerda - João Campos",
                    "Direita - Raquel Lyra"
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
                "João Campos - Pesquisa (%)",
                min_value=0.0,
                max_value=100.0,
                value=65.0,
                step=0.1
            )


        with c2:

            pesquisa_raquel = st.number_input(
                "Raquel Lyra - Pesquisa (%)",
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

        pesquisa_raquel=pesquisa_raquel,

        percentual_eleitores_municipio=
            percentual_eleitores_municipio
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
                f"x Raquel "
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

        st.caption(
            "O cenário estadual incorpora a transferência "
            "calculada no município, ponderada pelo percentual "
            "dos eleitores do município em Pernambuco."
        )

        e1, e2, e3 = st.columns(3)

        e1.metric(
            "Base 0 - João",
            f"{resultado['joao_estado']:.2f}%"
        )

        e2.metric(
            "Impacto deste município",
            f"{resultado['impacto_estado_joao']:+.4f} p.p."
        )

        e3.metric(
            "João após transferência",
            f"{resultado['joao_estado_apos_transferencia']:.4f}%"
        )

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "João Campos - PE",
                f"{resultado['joao_estado_final']:.4f}%"
            )

        with c2:
            st.metric(
                "Raquel Lyra - PE",
                f"{resultado['raquel_estado_final']:.4f}%"
            )

        st.progress(
            resultado["joao_estado_final"] / 100,
            text=(
                f"João "
                f"{resultado['joao_estado_final']:.4f}% "
                f"x Raquel "
                f"{resultado['raquel_estado_final']:.4f}%"
            )
        )

        st.write(
            f"Peso do município em Pernambuco: "
            f"**{resultado['peso_municipio_estado'] * 100:.4f}%**"
        )

        st.code(
            f"Variação municipal de João: "
            f"{resultado['variacao_municipal_joao']:+.4f} p.p.\n"
            f"Peso do município: "
            f"{resultado['peso_municipio_estado']:.6f}\n"
            f"Impacto em PE: "
            f"{resultado['variacao_municipal_joao']:+.4f} x "
            f"{resultado['peso_municipio_estado']:.6f} = "
            f"{resultado['impacto_estado_joao']:+.4f} p.p.\n"
            f"João PE: {resultado['joao_estado']:.4f} "
            f"{resultado['impacto_estado_joao']:+.4f} = "
            f"{resultado['joao_estado_apos_transferencia']:.4f}%"
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
                f"**João {resultado['joao_estado']:.2f}% x "
                f"Raquel {resultado['raquel_estado']:.2f}%**"
            )


            st.write(
                f"Base municipal: "
                f"**Esquerda {resultado['joao_inicial']:.2f}% x "
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
                        f"x "
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
                        f"x "
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
                    f"{resultado['joao_apos_prefeito']:.2f}% x "
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
                        f"x "
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
                    f"{resultado['joao_apos_lula']:.2f}% x "
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
                    f"**João {pesquisa_joao:.2f}% x "
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
                                f"x "
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
                                f"{rp['joao_final']:.2f}% x "
                                f"Raquel "
                                f"{rp['raquel_final']:.2f}%**"
                            )



        # ====================================================
        # IMPACTO EM PERNAMBUCO
        # ====================================================

        with st.expander(
            "5. Impacto da transferência municipal em Pernambuco",
            expanded=True
        ):

            st.write(
                f"Município: **{municipio_selecionado}**"
            )

            st.write(
                f"Eleitores do município: "
                f"**{dados_eleitorado['eleitores']:,}**"
            )

            st.write(
                f"Participação no eleitorado de Pernambuco: "
                f"**{resultado['percentual_eleitores_municipio']:.4f}%**"
            )

            st.write(
                f"Peso usado no cálculo: "
                f"**{resultado['peso_municipio_estado']:.6f}**"
            )

            st.code(
                f"{resultado['variacao_municipal_joao']:+.4f} "
                f"x {resultado['peso_municipio_estado']:.6f} "
                f"= {resultado['impacto_estado_joao']:+.4f} p.p."
            )

            st.write(
                f"Base 0 de Pernambuco: "
                f"**João {resultado['joao_estado']:.4f}% x "
                f"Raquel {resultado['raquel_estado']:.4f}%**"
            )

            st.write(
                f"Após incorporar a transferência deste município: "
                f"**João {resultado['joao_estado_apos_transferencia']:.4f}% x "
                f"Raquel {resultado['raquel_estado_apos_transferencia']:.4f}%**"
            )


# ============================================================
# ABA - CONFIGURAR PARÂMETROS
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
            "Pesquisa 0-5",
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
            "Pesquisa 5-10",
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
