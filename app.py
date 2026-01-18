import streamlit as st
from playwright.sync_api import sync_playwright
import os
import base64
import re
import subprocess

@st.cache_resource
def instalar_playwright_browsers():
    # Verifica se já está instalado para não repetir o processo desnecessariamente
    if not os.path.exists("/home/adminuser/.cache/ms-playwright"):
        try:
            # Instala o chromium e suas dependências de SO
            subprocess.run(["playwright", "install", "chromium"], check=True)
            # Comando extra para garantir as dependências no Linux
            subprocess.run(["playwright", "install-deps"], check=True)
        except Exception as e:
            st.error(f"Erro na instalação: {e}")

instalar_playwright_browsers()

# ... restante do seu código (outros imports, funções de suporte, etc.)

# 1. CONFIGURAÇÃO DA PÁGINA (Deve ser a primeira linha)
st.set_page_config(
    page_title="Portal de Dashboards | Satte Alam", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- CSS PARA PERSONALIZAÇÃO TOTAL (Fundo Escuro e Cards) ---
st.markdown("""
    <style>
    /* Fundo principal */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Título principal */
    .main-title {
        color: #FFFFFF;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        padding: 20px 0px 40px 0px;
        letter-spacing: -1px;
    }

    /* Estilização do Card */
    .dashboard-card {
        background-color: #1A1C24;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #30363D;
        transition: transform 0.3s ease, border-color 0.3s ease;
        text-align: center;
        margin-bottom: 20px;
    }

    .dashboard-card:hover {
        transform: translateY(-10px);
        border-color: #FF8C00;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.4);
    }

    /* Ajuste do Texto do Dashboard */
    .dashboard-name {
        color: #E6EDF3;
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 15px;
        height: 50px; /* Mantém o alinhamento mesmo com nomes longos */
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Remove sublinhado dos links */
    a { text-decoration: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE SUPORTE ---

def slugify(text):
    """Limpa o nome do arquivo para evitar erros com espaços e acentos"""
    text = text.lower()
    return re.sub(r'[\W_]+', '_', text)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def capturar_screenshot(url, nome_arquivo):
    nome_limpo = slugify(nome_arquivo)
    path_imagem = f"thumbs/{nome_limpo}.png"
    
    if not os.path.exists("thumbs"):
        os.makedirs("thumbs")

    if not os.path.exists(path_imagem):
        with st.spinner(f"Gerando miniatura para: {nome_arquivo}..."):
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                # Resolução maior para o print ficar mais nítido
                page.set_viewport_size({"width": 1600, "height": 900})
                try:
                    page.goto(url, timeout=90000)
                    # Espera o Power BI carregar (networkidle aguarda o fim do tráfego de rede)
                    page.wait_for_load_state("networkidle")
                    # Pequena pausa extra para garantir os gráficos renderizados
                    import time
                    time.sleep(5) 
                    page.screenshot(path=path_imagem)
                except Exception as e:
                    st.error(f"Erro ao capturar {nome_arquivo}: {e}")
                finally:
                    browser.close()
    return path_imagem

# --- CONTEÚDO DA INTERFACE ---

st.markdown('<h1 class="main-title">Central de Dashboards Satte Alam Motors</h1>', unsafe_allow_html=True)

dashboards = [
    {
        "nome": "Eficiência e Venda de Serviços - Oficina", 
        "url": "https://app.powerbi.com/view?r=eyJrIjoiOTRkNjAxYjEtZDVjNC00MGUwLWJlYzMtMTQ4ZjRmMTA4ZTA4IiwidCI6IjgwNGM1M2Y3LTIwNWEtNDI4NS1hNjhmLWVjOTU4NzllOTYzYiJ9"
    },
    {
        "nome": "Agenda dia seguinte - Oficina", 
        "url": "https://app.powerbi.com/view?r=eyJrIjoiNmQ4YmYwYTktZTJkZC00Mzg1LTlhM2YtNWRkNGRlMmM1ZTA1IiwidCI6IjgwNGM1M2Y3LTIwNWEtNDI4NS1hNjhmLWVjOTU4NzllOTYzYiJ9"
    },
    {
        "nome": "KPIs - Luciano", 
        "url": "https://app.powerbi.com/view?r=eyJrIjoiOWM2YzZiNzUtZTAxZS00NGE0LTk3Y2QtZjAxOThkNTIyMDdkIiwidCI6IjgwNGM1M2Y3LTIwNWEtNDI4NS1hNjhmLWVjOTU4NzllOTYzYiJ9"
    },
]

# Criando as colunas com um gap maior
cols = st.columns(3, gap="large")

for i, dash in enumerate(dashboards):
    with cols[i]:
        img_path = capturar_screenshot(dash["url"], dash["nome"])
        
        if os.path.exists(img_path):
            img_base64 = get_base64_of_bin_file(img_path)
            
            html_code = f'''
                <a href="{dash['url']}" target="_blank">
                    <div class="dashboard-card">
                        <img src="data:image/png;base64,{img_base64}" style="width: 100%; border-radius: 8px;" />
                        <div class="dashboard-name">{dash['nome']}</div>
                        <div style="color: #FF8C00; font-size: 0.8rem; margin-top: 10px;">Clique para abrir →</div>
                    </div>
                </a>
            '''
            st.markdown(html_code, unsafe_allow_html=True)