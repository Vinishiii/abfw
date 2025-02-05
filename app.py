import streamlit as st
import pandas as pd
import plotly.express as px
import unidecode
from difflib import SequenceMatcher

# Dicionário de palavras corretas e suas possíveis variações
PALAVRAS_CORRETAS = {
    "mascara": "máscara",
    "macala": "máscara",
    "casa": "casa",
    "caza": "casa",
    "arvore": "árvore",
    "avore": "árvore",
    "cachorro": "cachorro",
    "caxorro": "cachorro",
    "casa": "casa",
    "caza": "casa",
    "kaza": "casa",
    "caca": "casa",
    
    # Animais
    "cachorro": "cachorro",
    "caxorro": "cachorro",
    "cachoro": "cachorro",
    "caxoro": "cachorro",
    
    "gato": "gato",
    "gatu": "gato",
    "cato": "gato",
    
    "passaro": "pássaro",
    "passaru": "pássaro",
    "pasaro": "pássaro",
    "passalinho": "passarinho",
    "passarinhu": "passarinho",
    
    # Alimentos
    "leite": "leite",
    "lete": "leite",
    "leiti": "leite",
    
    "pao": "pão",
    "paum": "pão",
    
    "bolacha": "bolacha",
    "bolaxa": "bolacha",
    "bolaxa": "bolacha",
    
    "chocolate": "chocolate",
    "xocolate": "chocolate",
    "chocolati": "chocolate",
    
    # Objetos
    "bola": "bola",
    "bolla": "bola",
    "boua": "bola",
    
    "cadeira": "cadeira",
    "cadera": "cadeira",
    "cadela": "cadeira",
    
    "telefone": "telefone",
    "telefoni": "telefone",
    "telafone": "telefone",
    
    # Roupas
    "sapato": "sapato",
    "sapatu": "sapato",
    "zapato": "sapato",
    
    "vestido": "vestido",
    "vestidu": "vestido",
    "vestito": "vestido",
    
    # Partes do corpo
    "cabeca": "cabeça",
    "cabessa": "cabeça",
    "cabeça": "cabeça",
    
    "braco": "braço",
    "brasso": "braço",
    "baço": "braço",
    
    "perna": "perna",
    "pena": "perna",
    "pelna": "perna",
    
    # Natureza
    "arvore": "árvore",
    "arvere": "árvore",
    "avore": "árvore",
    
    "flor": "flor",
    "folor": "flor",
    "fror": "flor",
    
    "passaro": "pássaro",
    "passaru": "pássaro",
    "pasaro": "pássaro",
    
    # Cores
    "vermelho": "vermelho",
    "velemelho": "vermelho",
    "vemelho": "vermelho",
    
    "amarelo": "amarelo",
    "amarelo": "amarelo",
    "marelo": "amarelo",
    
    # Família
    "mae": "mãe",
    "mai": "mãe",
    
    "pai": "pai",
    "pahí": "pai",
    
    "irmao": "irmão",
    "irmau": "irmão",
    "imao": "irmão",
    
    # Escola
    "professor": "professor",
    "pofessor": "professor",
    "professol": "professor",
    
    "lapis": "lápis",
    "lapi": "lápis",
    "rapis": "lápis",
    
    "caderno": "caderno",
    "cadenu": "caderno",
    "cardeno": "caderno",
    
    # Números
    "um": "um",
    "hum": "um",
    
    "dois": "dois",
    "doiz": "dois",
    "dois": "dois",
    
    "tres": "três",
    "trez": "três",
    "teis": "três",
    
    # Brinquedos
    "boneca": "boneca",
    "boneka": "boneca",
    "buneca": "boneca",
    
    "carrinho": "carrinho",
    "carinho": "carrinho",
    "calinho": "carrinho",
    
    # Higiene
    "banho": "banho",
    "bano": "banho",
    "banhu": "banho",
    
    "escova": "escova",
    "iscova": "escova",
    "eskova": "escova",
    
    # Ações comuns
    "dormir": "dormir",
    "dorme": "dormir",
    "domir": "dormir",
    
    "comer": "comer",
    "come": "comer",
    "kome": "comer",
    
    "brincar": "brincar",
    "bincar": "brincar",
    "bricar": "brincar",
    
    # Objetos da casa
    "mesa": "mesa",
    "meza": "mesa",
    "mesa": "mesa",
    
    "cama": "cama",
    "kama": "cama",
    
    "porta": "porta",
    "pocta": "porta",
    "pohta": "porta",
    
    # Meios de transporte
    "carro": "carro",
    "caro": "carro",
    "carru": "carro",
    
    "onibus": "ônibus",
    "onibus": "ônibus",
    "onibuz": "ônibus",
    
    # Lugares
    "escola": "escola",
    "iscola": "escola",
    "escora": "escola",
    
    "parque": "parque",
    "parqui": "parque",
    "palque": "parque",
    
    # Clima
    "chuva": "chuva",
    "xuva": "chuva",
    "juva": "chuva",
    
    "sol": "sol",
    "sou": "sol",
    "sol": "sol",
    
    # Alimentos
    "arroz": "arroz",
    "aroz": "arroz",
    "arois": "arroz",
    
    "feijao": "feijão",
    "fejao": "feijão",
    "feijau": "feijão",
    
    # Bebidas
    "agua": "água",
    "agoa": "água",
    "auá": "água",
    
    "suco": "suco",
    "suku": "suco",
    "çuco": "suco",
    
    # Frutas
    "banana": "banana",
    "banana": "banana",
    "banan": "banana",
    
    "maca": "maçã",
    "massa": "maçã",
    "maça": "maçã",
    
    # Material escolar
    "borracha": "borracha",
    "boracha": "borracha",
    "bolacha": "borracha",
    
    "tesoura": "tesoura",
    "tesora": "tesoura",
    "tizora": "tesoura",
}

def calcular_similaridade(s1, s2):
    """Calcula a similaridade entre duas strings"""
    return SequenceMatcher(None, s1, s2).ratio()

def encontrar_palavra_correta(palavra_teste):
    """Encontra a palavra correta mais próxima no dicionário"""
    palavra_teste = unidecode.unidecode(palavra_teste.lower())
    
    if palavra_teste in PALAVRAS_CORRETAS:
        return PALAVRAS_CORRETAS[palavra_teste]
    
    maior_similaridade = 0
    palavra_correta = None
    
    for palavra_dict in set(PALAVRAS_CORRETAS.values()):
        similaridade = calcular_similaridade(palavra_teste, unidecode.unidecode(palavra_dict.lower()))
        if similaridade > maior_similaridade and similaridade > 0.6:
            maior_similaridade = similaridade
            palavra_correta = palavra_dict
    
    return palavra_correta

def classificar_erro_fonologico(palavra):
    """Classifica o tipo de erro fonológico"""
    palavra = palavra.lower()
    
    # Verificações básicas
    if len(palavra) <= 2:
        return "Omissão"
    
    if any(char.isdigit() for char in palavra):
        return "Distorção"
    
    # Encontrar palavra correta no dicionário
    palavra_correta = encontrar_palavra_correta(palavra)
    if not palavra_correta:
        return "Distorção"
    
    palavra = unidecode.unidecode(palavra)
    palavra_correta = unidecode.unidecode(palavra_correta.lower())
    
    # Se são idênticas (ignorando acentos)
    if palavra == palavra_correta:
        return "Nenhum"
    
    # Verifica omissão
    if len(palavra) < len(palavra_correta):
        letras_faltantes = set(palavra_correta) - set(palavra)
        if letras_faltantes:
            return "Omissão"
    
    # Verifica substituições comuns
    substituicoes = {
        'r': 'l',
        's': 'x',
        'j': 'z',
        'c': 'k',
    }
    
    for original, substituto in substituicoes.items():
        if original in palavra_correta and substituto in palavra:
            return "Substituição"
    
    # Verifica padrões específicos
    padroes_substituicao = ['x', 'z', 'ç', 'ch']
    padroes_distorcao = ['qu', 'nh', 'lh']
    
    for padrao in padroes_substituicao:
        if padrao in palavra:
            return "Substituição"
    
    for padrao in padroes_distorcao:
        if padrao in palavra:
            return "Distorção"
    
    # Se as palavras são muito diferentes
    if calcular_similaridade(palavra, palavra_correta) < 0.6:
        return "Distorção"
    
    return "Substituição"

def main():
    st.set_page_config(
        page_title="Análise Fonológica Infantil",
        page_icon="🧠",
        layout="wide"
    )

    st.title("📊 Análise Fonológica Infantil")
    
    if 'df_dinamico' not in st.session_state:
        st.session_state.df_dinamico = pd.DataFrame(columns=["Vocábulo", "Erro"])

    st.subheader("➕ Adicionar Novo Vocábulo")
    col1, col2 = st.columns([3, 1])

    with col1:
        novo_vocabulo = st.text_input("Digite o novo vocábulo:")
    
    with col2:
        classificacao_manual = st.selectbox(
            "Ou classifique manualmente:", 
            ["Automático", "Omissão", "Substituição", "Distorção", "Nenhum"]
        )

    if st.button("Adicionar Vocábulo"):
        if novo_vocabulo:
            if classificacao_manual == "Automático":
                erro = classificar_erro_fonologico(novo_vocabulo)
            else:
                erro = classificacao_manual
            
            novo_dado = pd.DataFrame({"Vocábulo": [novo_vocabulo], "Erro": [erro]})
            st.session_state.df_dinamico = pd.concat([
                st.session_state.df_dinamico, 
                novo_dado
            ], ignore_index=True)
            
            st.success(f"Vocábulo '{novo_vocabulo}' adicionado com classificação: {erro}")

    st.subheader("📋 Tabela de Vocábulos")
    edited_df = st.data_editor(
        st.session_state.df_dinamico, 
        num_rows="dynamic",
        column_config={
            "Vocábulo": st.column_config.TextColumn(
                "Vocábulo",
                help="Digite os vocábulos aqui"
            ),
            "Erro": st.column_config.SelectboxColumn(
                "Tipo de Erro",
                options=["Omissão", "Substituição", "Distorção", "Nenhum"],
                help="Selecione o tipo de erro"
            )
        },
        hide_index=True
    )

    st.session_state.df_dinamico = edited_df

    if not st.session_state.df_dinamico.empty:
        st.subheader("📊 Análise de Erros Fonológicos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            contagem_erros = st.session_state.df_dinamico["Erro"].value_counts()
            fig_pizza = px.pie(
                names=contagem_erros.index,
                values=contagem_erros.values,
                title="Distribuição de Erros"
            )
            st.plotly_chart(fig_pizza, use_container_width=True)
        
        with col2:
            fig_barras = px.bar(
                x=contagem_erros.index,
                y=contagem_erros.values,
                title="Frequência de Erros Fonológicos",
                labels={"x": "Tipo de Erro", "y": "Quantidade"},
                color=contagem_erros.index
            )
            st.plotly_chart(fig_barras, use_container_width=True)

        st.subheader("📈 Estatísticas")
        total_palavras = len(st.session_state.df_dinamico)
        erros_por_tipo = st.session_state.df_dinamico["Erro"].value_counts()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Palavras", total_palavras)
        with col2:
            st.metric("Omissões", erros_por_tipo.get("Omissão", 0))
        with col3:
            st.metric("Substituições", erros_por_tipo.get("Substituição", 0))
        with col4:
            st.metric("Distorções", erros_por_tipo.get("Distorção", 0))

    st.markdown("---")
    st.markdown("📌 **Análise Fonológica Infantil** | 🧠 Ferramenta de Apoio Fonoaudiológico | 2025 BY : Vinicius Andrey")
    
            

if __name__ == "__main__":
    main()










