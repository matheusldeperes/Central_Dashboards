import streamlit as st
from playwright.sync_api import sync_playwright
import os
import base64
import subprocess
import sys
import time
import re

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Portal Satte Alam Motors", layout="wide")

# --- FUNÇÕES DE SUPORTE (Definidas no topo para evitar NameError) ---

def slugify(text):
    return re.sub(r'[\W_]+', '_', text.lower())

def get_base64_of_bin_file(img_path):
    """Lê o arquivo de imagem e converte para texto base64"""
    with open(img_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache_resource
def instalar_playwright():
    """Instala o navegador Chromium na nuvem ou localmente"""
    try:
        # Usamos sys.executable para evitar o erro de 'python' não encontrado
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    except Exception as e:
        st.error(f"Erro na instalação do navegador: {e}")

def capturar_screenshot(url, nome_arquivo):
    nome_limpo = slugify(nome_arquivo)
    path_imagem = f"thumbs/{nome_limpo}.png"
    
    if not os.path.exists("thumbs"):
        os.makedirs("thumbs")

    if not os.path.exists(path_imagem):
        with st.spinner(f"Gerando miniatura para: {nome_arquivo}..."):
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
                )
                page = browser.new_page()
                page.set_viewport_size({"width": 1280, "height": 720})
                try:
                    page.goto(url, timeout=90000, wait_until="networkidle")
                    time.sleep(8) # Tempo para o Power BI carregar
                    page.screenshot(path=path_imagem)
                except Exception as e:
                    st.error(f"Erro ao capturar {nome_arquivo}: {e}")
                finally:
                    browser.close()
    return path_imagem

# --- INÍCIO DA EXECUÇÃO ---

# Executa a instalação do navegador
instalar_playwright()

# CSS para o visual Dark Mode e Cards
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    .main-title { color: white; text-align: center; padding: 20px; font-weight: bold; }
    .dashboard-card {
        background-color: #1A1C24;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #30363D;
        text-align: center;
        transition: transform 0.3s;
    }
    .dashboard-card:hover { transform: translateY(-5px); border-color: #FF4B4B; }
    .dashboard-name { color: white; font-weight: bold; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📊 Central de Dashboards - Satte Alam Motors</h1>', unsafe_allow_html=True)

# Seus links reais
dashboards = [
    {"nome": "Eficiência e Venda de Serviços - Oficina", "url": "https://app.powerbi.com/view?r=eyJrIjoiOTRkNjAxYjEtZDVjNC00MGUwLWJlYzMtMTQ4ZjRmMTA4ZTA4IiwidCI6IjgwNGM1M2Y3LTIwNWEtNDI4NS1hNjhmLWVjOTU4NzllOTYzYiJ9"},
    {"nome": "Agenda dia seguinte - Oficina", "url": "https://app.powerbi.com/view?r=eyJrIjoiNmQ4YmYwYTktZTJkZC00Mzg1LTlhM2YtNWRkNGRlMmM1ZTA1IiwidCI6IjgwNGM1M2Y3LTIwNWEtNDI4NS1hNjhmLWVjOTU4NzllOTYzYiJ9"},
    {"nome": "KPIs - Luciano", "url": "https://app.powerbi.com/view?r=eyJrIjoiOWM2YzZiNzUtZTAxZS00NGE0LTk3Y2QtZjAxOThkNTIyMDdkIiwidCI6IjgwNGM1M2Y3LTIwNWEtNDI4NS1hNjhmLWVjOTU4NzllOTYzYiJ9"},
]

cols = st.columns(3, gap="large")

for i, dash in enumerate(dashboards):
    with cols[i]:
        img_path = capturar_screenshot(dash["url"], dash["nome"])
        
        if os.path.exists(img_path):
            img_base64 = get_base64_of_bin_file(img_path)
            
            html_code = f'''
                <a href="{dash['url']}" target="_blank" style="text-decoration: none;">
                    <div class="dashboard-card">
                        <img src="data:image/png;base64,{img_base64}" style="width: 100%; border-radius: 8px;" />
                        <div class="dashboard-name">{dash['nome']}</div>
                    </div>
                </a>
            '''
            st.markdown(html_code, unsafe_allow_html=True)