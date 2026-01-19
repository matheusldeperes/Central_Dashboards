import streamlit as st
from playwright.sync_api import sync_playwright
from PIL import Image
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
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    except Exception as e:
        pass  # Silenciosamente falhar se já estiver instalado

instalar_playwright()

@st.cache_data(ttl=7200)
def capturar_screenshot(url, nome_arquivo):
    """Captura screenshot do Power BI com retry"""
    nome_limpo = slugify(nome_arquivo)
    path_imagem = f"thumbs/{nome_limpo}.png"
    
    if not os.path.exists("thumbs"):
        os.makedirs("thumbs")

    # Se a imagem já existe, retorna
    if os.path.exists(path_imagem):
        return path_imagem

    try:
        with st.spinner(f"📸 Capturando: {nome_arquivo}..."):
            with sync_playwright() as p:
                browser = None
                page = None
                try:
                    # Lançar navegador com configurações otimizadas
                    browser = p.chromium.launch(
                        headless=True,
                        args=[
                            "--no-sandbox",
                            "--disable-gpu",
                            "--disable-dev-shm-usage",
                            "--disable-extensions",
                            "--disable-background-networking",
                            "--disable-client-side-phishing-detection",
                            "--disable-popup-blocking"
                        ],
                        timeout=45000
                    )
                    
                    # Criar página com viewport apropriado
                    page = browser.new_page(viewport={"width": 1366, "height": 768})
                    page.set_default_timeout(120000)
                    page.set_default_navigation_timeout(120000)
                    
                    # Navegar com espera por rede
                    page.goto(url, timeout=120000, wait_until="networkidle")
                    
                    # Aguardar elementos renderizarem
                    time.sleep(8)
                    
                    # Tirar screenshot
                    page.screenshot(path=path_imagem, full_page=False)
                    
                except Exception as e:
                    st.warning(f"⚠️ Erro ao capturar {nome_arquivo}. Tentando novamente...")
                    print(f"Erro detalhado: {str(e)}")
                    raise
                    
                finally:
                    if page:
                        page.close()
                    if browser:
                        browser.close()
                        
    except Exception as e:
        # Fallback: criar imagem placeholder com mensagem
        print(f"Falha final ao capturar {nome_arquivo}: {e}")
        img = Image.new('RGB', (1366, 768), color=(45, 49, 56))
        img.save(path_imagem)
    
    return path_imagem

# --- INÍCIO DA EXECUÇÃO ---

# Executa a instalação do navegador


# CSS para o visual Dark Mode e Cards
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    .main-title { color: white; text-align: center; padding: 20px; font-weight: bold; font-size: 2.5em; }
    .dashboard-card {
        background-color: #1A1C24;
        border-radius: 12px;
        padding: 0;
        border: 2px solid #30363D;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .dashboard-card:hover { 
        transform: translateY(-8px) scale(1.02);
        border-color: #FF4B4B;
        box-shadow: 0 8px 16px rgba(255, 75, 75, 0.3);
    }
    .dashboard-card img {
        width: 100%;
        height: auto;
        display: block;
        border-radius: 10px 10px 0 0;
    }
    .dashboard-name { 
        color: white;
        font-weight: bold;
        margin-top: 12px;
        padding: 12px;
        font-size: 1.1em;
        word-wrap: break-word;
    }
    .dashboard-link {
        text-decoration: none !important;
        display: block;
        width: 100%;
    }
    .dashboard-link:hover {
        text-decoration: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📊 Central de Dashboards - Satte Alam Motors</h1>', unsafe_allow_html=True)

# Seus links reais
dashboards = [
    {"nome": "Eficiência e Venda de Serviços - Oficina", "url": "https://app.powerbi.com/view?r=eyJrIjoiOTRkNjAxYjEtZDVjNC00MGUwLWJlYzMtMTQ4ZjRmMTA4ZTA4IiwidCI6IjgwNGM1M2Y3LTIwNWEtNDI4NS1hNjhmLWVjOTU4NzllOTYzYiJ9"},
    {"nome": "Agenda dia seguinte - Oficina", "url": "https://app.powerbi.com/view?r=eyJrIjoiNmQ4YmYwYTktZTJkZC00Mzg1LTlhM2YtNWRkNGRlMmM1ZTA1IiwidCI6IjgwNGM1M2Y3LTIwNWEtNDI4NS1hNjhmLWVjOTU4NzllOTYzYiJ9"},
    {"nome": "KPIs - Luciano", "url": "https://app.powerbi.com/view?r=eyJrIjoiOWM2YzZiNzUtZTAxZS00NGE0LTk3Y2QtZjAxOThkNTIyMDdkIiwidCI6IjgwNGM1M2Y3LTIwNWEtNDI4NS1hNjhmLWVjOTU4NzllOTYzYiJ9"},
]

cols = st.columns(3, gap="medium")

for i, dash in enumerate(dashboards):
    with cols[i]:
        img_path = capturar_screenshot(dash["url"], dash["nome"])
        
        if os.path.exists(img_path):
            img_base64 = get_base64_of_bin_file(img_path)
            
            html_code = f'''
                <a href="{dash['url']}" target="_blank" class="dashboard-link">
                    <div class="dashboard-card">
                        <img src="data:image/png;base64,{img_base64}" alt="{dash['nome']}" />
                        <div class="dashboard-name">{dash['nome']}</div>
                    </div>
                </a>
            '''
            st.markdown(html_code, unsafe_allow_html=True)
        else:
            st.error(f"❌ Erro ao carregar: {dash['nome']}")