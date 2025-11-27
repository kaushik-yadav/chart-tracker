import streamlit as st
import datetime
from utils.llm_utils import get_daily_guidance
from utils.ui_utils import render_card, generate_date_labels, hide_streamlit_elements, plot_immunity
from utils.cache_utils import load_cache, get_browser_id, save_cache
from utils.status_utils import get_status
from config import PAGE_TITLE, PAGE_ICON, BASE_DATE, IMMUNITY

def main():
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="centered")
    hide_streamlit_elements()
    
    # Load cache
    cache_data = load_cache()
    
    browser_id = get_browser_id()
    if browser_id not in cache_data:
        cache_data[browser_id] = {"last_date": BASE_DATE.isoformat()}
        save_cache(cache_data)
    
    last_date = datetime.date.fromisoformat(cache_data[browser_id]["last_date"])
    
    st.title("🧬 R-CHOP Immunity Tracker")
    selected_date = st.date_input(
        "Select your chemotherapy start date",
        value=last_date,
        min_value=BASE_DATE - datetime.timedelta(days=365),
        max_value=BASE_DATE + datetime.timedelta(days=365),
        help="Choose the first day of your current R-CHOP cycle"
    )
    
    if selected_date != last_date:
        cache_data[browser_id]["last_date"] = selected_date.isoformat()
        save_cache(cache_data)
        st.toast("✓ Date saved successfully", icon="✅")
    
    date_labels = generate_date_labels(selected_date, len(IMMUNITY))
    
    show_today, today_index = plot_immunity(date_labels, IMMUNITY, selected_date)
    
    if show_today:
        days_into_cycle = today_index + 1
        current_immunity = IMMUNITY[today_index]
        status = get_status(current_immunity)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Day in Cycle", f"{days_into_cycle}/{len(IMMUNITY)}")
        col2.metric("Current Immunity", f"{current_immunity}%")
        col3.metric("Status", status)
        
        # Fetch LLM data
        daily_data = get_daily_guidance(str(days_into_cycle))
        
        # Render Cards
        risk_class_map = {
            "Low": "card-risk-low",
            "Moderate": "card-risk-moderate",
            "High": "card-risk-high"
        }
        render_card(f"🩺 Immune Risk — {daily_data['immune_risk']}", daily_data['summary'], risk_class=risk_class_map.get(daily_data['immune_risk']))
        render_card("🥗 What to Eat", daily_data["what_to_eat"])
        render_card("🚫 What NOT to Eat", daily_data["what_not_to_eat"])
        render_card("🎯 Priorities for Today", daily_data["priorities"])
        render_card("⚠️ Avoid", daily_data["avoid"])

if __name__ == "__main__":
    main()
