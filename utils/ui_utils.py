import streamlit as st
import matplotlib.pyplot as plt
import datetime

# hides streamlit UI elements
def hide_streamlit_elements():
    hide_style = """
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"],
        [data-testid="stHeader"], [data-testid="stSidebarNav"] {display: none;}
        div.block-container {padding-top: 0;}
    </style>
    """
    st.markdown(hide_style, unsafe_allow_html=True)

# Generate the date labels for the chart
def generate_date_labels(start_date, num_days):
    return [(start_date + datetime.timedelta(days=i)).strftime("%b %d") for i in range(num_days)]

# Plots the immunity levels based on start date
def plot_immunity(date_labels, immunity, selected_date):
    today = datetime.date.today()
    cycle_start = selected_date
    cycle_end = selected_date + datetime.timedelta(days=len(immunity)-1)
    show_today = cycle_start <= today <= cycle_end
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Colors
    line_color = "#2E7D96"
    marker_color = "#1A5F7A"
    today_color = "#E63946"
    grid_color = "#E8E8E8"
    
    ax.plot(date_labels, immunity, marker='o', linewidth=2.5, 
            color=line_color, markerfacecolor=marker_color, markersize=6, markeredgewidth=0)
    
    if show_today:
        red_index = (today - selected_date).days
        ax.axvline(date_labels[red_index], color=today_color, linestyle='--', linewidth=2, label="Today", alpha=0.8)
    
    ax.set_facecolor("#F8F9FA")
    fig.patch.set_facecolor('white')
    ax.set_xlabel("Date", fontsize=11, color="#2C3E50")
    ax.set_ylabel("Immunity Level (%)", fontsize=11, color="#2C3E50")
    ax.set_title("Immunity Pattern Over 22-Day Cycle", fontsize=13, weight="bold", color="#2C3E50", pad=15)
    
    if show_today:
        ax.legend(loc='lower right', framealpha=0.95)
    
    ax.grid(True, linestyle='--', alpha=0.3, color=grid_color)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(fontsize=9)
    plt.tight_layout()
    
    st.pyplot(fig)
    
    return show_today, (today - selected_date).days if show_today else None

# Guidance cards render
def render_card(title, body, risk_class=None):
    card_css = """
    <style>
    .card {
        background: #1E1E1E;
        padding: 22px 26px;
        border-radius: 18px;
        margin-bottom: 20px;
        color: white;
        border-left: 6px solid #4CAF50;
        box-shadow: 0px 4px 18px rgba(0,0,0,0.45);
    }
    .card-risk-low { border-left-color: #4CAF50 !important; }
    .card-risk-moderate { border-left-color: #FFC107 !important; }
    .card-risk-high { border-left-color: #FF5252 !important; }
    .card-title { font-size: 22px; font-weight: 700; margin-bottom: 12px; color: #ffffff; }
    .card-body { font-size: 16px; line-height: 1.6; color: #e0e0e0; }
    </style>
    """
    st.markdown(card_css, unsafe_allow_html=True)
    
    risk_class_str = f" {risk_class}" if risk_class else ""
    
    st.markdown(
        f"""
        <div class="card{risk_class_str}">
            <div class="card-title">{title}</div>
            <div class="card-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
