import streamlit as st

def apply_custom_styling():
    """Apply custom CSS styling to the Streamlit app."""
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1E3A8A;
            text-align: center;
            margin-bottom: 1.5rem;
            background: linear-gradient(90deg, #EEF2FF, #E0E7FF);
            padding: 1rem;
            border-radius: 12px;
        }

        .subheader {
            font-size: 1.5rem;
            font-weight: 600;
            color: #1E3A8A;
            margin: 1.5rem 0 1rem;
            padding-left: 0.75rem;
            border-left: 5px solid #3B82F6;
        }

        .card {
            background-color: #F9FAFB;
            border-radius: 12px;
            padding: 1.25rem;
            margin: 1rem 0;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        }

        .metric-label {
            font-size: 1rem;
            color: #6B7280;
        }

        .metric-value {
            font-size: 1.75rem;
            font-weight: 700;
        }

        .positive-value {
            color: #10B981;
            font-weight: 600;
        }

        .negative-value {
            color: #EF4444;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)

def create_main_header(title: str):
    """Display a large styled page header."""
    st.markdown(f"<div class='main-header'>{title}</div>", unsafe_allow_html=True)

