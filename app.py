import streamlit as st
import base64
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Portal Satte Alam Motors", layout="wide")

# Função para converter imagem para base64
def get_base64_image(image_path):
    """Converte imagem para base64"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Carregar imagem de fundo
background_image_path = "assets/background.jpg"
if os.path.exists(background_image_path):
    bg_image_base64 = get_base64_image(background_image_path)
else:
    bg_image_base64 = None

# CSS para o visual Dark Mode e Cards com iframes
if bg_image_base64:
    st.markdown(f"""
        <style>
        html, body {{
            margin: 0;
            padding: 0;
        }}
        
        .stApp {{ 
            background: url("data:image/jpeg;base64,{bg_image_base64}") center/cover no-repeat fixed;
            background-color: #0E1117;
            background-attachment: fixed;
        }}
        
        [data-testid="stAppViewContainer"] {{
            background: rgba(14, 17, 23, 0.80);
            backdrop-filter: blur(8px);
        }}
        
        [data-testid="stMainBlockContainer"] {{
            background: transparent;
        }}
        
        .main-title {{ 
            color: white; 
            text-align: center; 
            padding: 20px; 
            font-weight: bold; 
            font-size: 2.5em;
            margin-bottom: 30px;
            text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.9);
        }}
        
        .dashboard-card-container {{
            background-color: rgba(26, 28, 36, 0.95);
            border-radius: 16px;
            border: 2px solid #30363D;
            padding: 0;
            margin: 15px 0;
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
            transition: all 0.3s ease;
            cursor: pointer;
            height: 100%;
            display: flex;
            flex-direction: column;
            position: relative;
        }}
        
        .dashboard-card-container:hover {{
            transform: translateY(-12px) scale(1.02);
            border-color: #FF8C00;
            box-shadow: 0 12px 32px rgba(255, 75, 75, 0.4);
        }}
        
        .card-link-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 10;
            cursor: pointer;
            border-radius: 16px;
        }}
        
        .dashboard-iframe-wrapper {{
            width: 100%;
            height: 380px;
            overflow: hidden;
            border-radius: 14px 14px 0 0;
            position: relative;
            background-color: #0d1117;
        }}
        
        .dashboard-iframe-wrapper iframe {{
            width: 100%;
            height: 100%;
            border: none;
            display: block;
        }}
        
        .dashboard-footer {{
            padding: 18px;
            background: linear-gradient(135deg, #161b22 0%, #1a1f2e 100%);
            border-top: 2px solid #30363D;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-grow: 1;
            gap: 12px;
        }}
        
        .dashboard-name {{
            color: #e8f0fe;
            font-weight: 600;
            font-size: 0.95em;
            word-wrap: break-word;
            flex-grow: 1;
            text-align: left;
            line-height: 1.3;
        }}
        
        .open-btn {{
            background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 8px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            white-space: nowrap;
            margin-left: 8px;
            font-size: 0.9em;
            box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
        }}
        
        .open-btn:hover {{
            background: linear-gradient(135deg, #FF6B6B, #FF8B8B);
            transform: scale(1.08);
            box-shadow: 0 6px 16px rgba(255, 75, 75, 0.5);
        }}
        
        .open-btn:active {{
            transform: scale(0.95);
        }}
        </style>
    """, unsafe_allow_html=True)
else:
    st.error("Erro: Imagem de fundo não encontrada!")

st.markdown('<h1 class="main-title">Central de Dashboards - Satte Alam Motors</h1>', unsafe_allow_html=True)

# Seus links reais
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

# Criar colunas responsivas
cols = st.columns(3, gap="medium")

for i, dash in enumerate(dashboards):
    with cols[i]:
        # HTML customizado para o card com iframe, overlay clicável e botão
        card_html = f"""
        <a href="{dash['url']}" target="_blank" style="text-decoration: none;">
            <div class="dashboard-card-container">
                <div class="card-link-overlay"></div>
                <div class="dashboard-iframe-wrapper">
                    <iframe src="{dash['url']}" allowfullscreen></iframe>
                </div>
                <div class="dashboard-footer">
                    <div class="dashboard-name">{dash['nome']}</div>
                </div>
            </div>
        </a>
        """
        st.markdown(card_html, unsafe_allow_html=True)

# Espaço adicional
st.markdown("<br><br>", unsafe_allow_html=True)