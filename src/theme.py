import streamlit as st

def apply_corporate_theme():
    st.markdown("""
    <style>
        /* Corporate Global Styles (No Emojis allowed) */
        .stApp {
            background-color: #f8f9fa;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333333;
        }
        
        h1, h2, h3 {
            color: #003366;
            font-weight: 600;
        }

        /* Clean Dashboard Cards */
        .css-1r6slb0, .css-1y4p8pa {
            background-color: #ffffff !important;
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            border: 1px solid #e0e0e0;
        }
        
        /* Corporate Blue Buttons */
        .stButton>button {
            background-color: #004080;
            color: white;
            border: 1px solid #003366;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
            width: 100%;
        }
        
        .stButton>button:hover {
            background-color: #00264d;
            border-color: #001a33;
            color: white;
        }

        /* Clean Inputs */
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            border-radius: 4px;
            border: 1px solid #cccccc;
            padding: 0.5rem;
        }
        
        .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
            border-color: #004080;
            box-shadow: 0 0 0 1px #004080;
        }

        /* Subdued Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            border-bottom: 2px solid #e0e0e0;
        }

        .stTabs [data-baseweb="tab"] {
            height: 40px;
            background-color: transparent;
            color: #666666;
            font-weight: 500;
            padding: 8px 16px;
            border: none;
        }

        .stTabs [aria-selected="true"] {
            color: #004080;
            border-bottom: 3px solid #004080;
        }
        
        /* Key Metrics */
        [data-testid="stMetricValue"] {
            font-size: 2.2rem;
            color: #004080;
            font-weight: 700;
        }
        
        /* Divider */
        hr {
            margin: 2rem 0;
            border-color: #e0e0e0;
        }
    </style>
    """, unsafe_allow_html=True)
