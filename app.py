import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Portal Satte Alam Motors", layout="wide")

# CSS para o visual Dark Mode e Cards com iframes
st.markdown("""
    <style>
    .stApp { 
        background-color: #0E1117; 
    }
    
    .main-title { 
        color: white; 
        text-align: center; 
        padding: 20px; 
        font-weight: bold; 
        font-size: 2.5em;
        margin-bottom: 30px;
    }
    
    .dashboard-card-container {
        background-color: #1A1C24;
        border-radius: 12px;
        border: 2px solid #30363D;
        padding: 0;
        margin: 10px 0;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .dashboard-card-container:hover {
        transform: translateY(-8px) scale(1.01);
        border-color: #FF8C00;
        box-shadow: 0 8px 16px rgba(255, 75, 75, 0.3);
    }
    
    .dashboard-iframe-wrapper {
        width: 100%;
        height: 350px;
        overflow: hidden;
        border-radius: 10px 10px 0 0;
        position: relative;
        background-color: #0d1117;
    }
    
    .dashboard-iframe-wrapper iframe {
        width: 100%;
        height: 100%;
        border: none;
        display: block;
    }
    
    .dashboard-footer {
        padding: 15px;
        background-color: #161b22;
        border-top: 1px solid #30363D;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-grow: 1;
    }
    
    .dashboard-name {
        color: white;
        font-weight: bold;
        font-size: 1em;
        word-wrap: break-word;
        flex-grow: 1;
        text-align: left;
    }
    
    .open-btn {
        background-color: #FF4B4B;
        color: white;
        border: none;
        padding: 8px 15px;
        border-radius: 6px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        white-space: nowrap;
        margin-left: 10px;
        font-size: 0.9em;
    }
    
    .open-btn:hover {
        background-color: #FF6B6B;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

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
        # HTML customizado para o card com iframe e botão
        card_html = f"""
        <div class="dashboard-card-container">
            <div class="dashboard-iframe-wrapper">
                <iframe src="{dash['url']}" allowfullscreen></iframe>
            </div>
            <div class="dashboard-footer">
                <div class="dashboard-name">{dash['nome']}</div>
                <a href="{dash['url']}" target="_blank" style="text-decoration: none;">
                </a>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

# Espaço adicional
st.markdown("<br><br>", unsafe_allow_html=True)