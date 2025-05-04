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

def create_subheader(title: str):
    """Display a styled section subheader."""
    st.markdown(f"<div class='subheader'>{title}</div>", unsafe_allow_html=True)

def render_card(content: str):
    """Wrap custom HTML content inside a styled card."""
    return f"<div class='card'>{content}</div>"

def render_metric(label: str, value: str, change: float = None, change_percent: float = None):
    """
    Create a metric block with optional change indicators.

    Args:
        label (str): Metric label
        value (str): Main value (already formatted as string)
        change (float, optional): Change in value
        change_percent (float, optional): Change in percentage
    Returns:
        str: HTML content to embed in st.markdown
    """
    html = f"<div class='metric-label'>{label}</div>"
    html += f"<div class='metric-value'>{value}</div>"

    if change is not None or change_percent is not None:
        sign = "+" if (change or 0) >= 0 else ""
        change_class = "positive-value" if (change or 0) >= 0 else "negative-value"

        change_parts = []
        if change is not None:
            change_parts.append(f"{sign}{change}")
        if change_percent is not None:
            change_parts.append(f"{sign}{change_percent}%")

        html += f"<div class='{change_class}'>{' '.join(change_parts)}</div>"

    return html
