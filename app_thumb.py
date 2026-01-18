import streamlit as st
from playwright.sync_api import sync_playwright
import os
import base64

# --- FUNÇÕES DE SUPORTE ---

def get_base64_of_bin_file(bin_file):
    """Converte a imagem em base64 para o HTML conseguir ler"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def capturar_screenshot(url, nome_arquivo):
    path_imagem = f"thumbs/{nome_arquivo}.png"
    if not os.path.exists("thumbs"):
        os.makedirs("thumbs")

    if not os.path.exists(path_imagem):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_viewport_size({"width": 1280, "height": 720})
            try:
                page.goto(url, timeout=60000)
                page.wait_for_load_state("networkidle")
                page.screenshot(path=path_imagem)
            finally:
                browser.close()
    return path_imagem

# --- INTERFACE ---

st.title("Central de Dashboards - Satte Alam Motors")

dashboards = [
    {"nome": "Eficiência e Venda de Serviços - Oficina", "url": "https://app.powerbi.com/view?r=eyJrIjoiOTRkNjAxYjEtZDVjNC00MGUwLWJlYzMtMTQ4ZjRmMTA4ZTA4IiwidCI6IjgwNGM1M2Y3LTIwNWEtNDI4NS1hNjhmLWVjOTU4NzllOTYzYiJ9"},
    {"nome": "Agenda dia seguinte - Oficina", "url": "https://app.powerbi.com/view?r=eyJrIjoiNmQ4YmYwYTktZTJkZC00Mzg1LTlhM2YtNWRkNGRlMmM1ZTA1IiwidCI6IjgwNGM1M2Y3LTIwNWEtNDI4NS1hNjhmLWVjOTU4NzllOTYzYiJ9"},
    {"nome": "KPIs - Luciano", "url": "https://app.powerbi.com/view?r=eyJrIjoiOWM2YzZiNzUtZTAxZS00NGE0LTk3Y2QtZjAxOThkNTIyMDdkIiwidCI6IjgwNGM1M2Y3LTIwNWEtNDI4NS1hNjhmLWVjOTU4NzllOTYzYiJ9"},
]

cols = st.columns(len(dashboards), gap="large")

for i, dash in enumerate(dashboards):
    with cols[i]:
        # 1. Gera ou recupera o caminho da imagem
        img_path = capturar_screenshot(dash["url"], dash["nome"].lower())
        
        # 2. Converte para base64
        img_base64 = get_base64_of_bin_file(img_path)
        
        # 3. Cria o HTML da imagem com o link
        # Adicionamos um pouco de CSS para dar efeito de brilho/escala ao passar o mouse
        html_code = f'''
            <a href="{dash['url']}" target="_blank" style="text-decoration: none;">
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{img_base64}" 
                         style="width: 100%; border-radius: 10px; transition: transform .2s; cursor: pointer; border: 1px solid #ddd;"
                         onmouseover="this.style.transform='scale(1.02)';" 
                         onmouseout="this.style.transform='scale(1)';" />
                    <p style="color: #31333F; font-weight: bold; margin-top: 10px;">{dash['nome']}</p>
                </div>
            </a>
        '''
        st.markdown(html_code, unsafe_allow_html=True)