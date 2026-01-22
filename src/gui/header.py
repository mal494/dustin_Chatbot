import streamlit as st # type: ignore
from src import memory

def render(settings):
    st.set_page_config(page_title=settings['app_name'], page_icon="🧠")
    
    with st.sidebar:
        st.title(f"⚙️ {settings['app_name']}")
        
        # --- Model Selector ---
        model_options = list(settings['models'].keys())
        
        # Get current selection or default
        current_selection = st.session_state.get("selected_model_key", settings['default_model'])
        
        selected_key = st.selectbox(
            "Select Brain:",
            options=model_options,
            format_func=lambda x: settings['models'][x]['name'],
            index=model_options.index(current_selection)
        )
        
        # Detect if the user changed the model
        if selected_key != current_selection:
            st.session_state["selected_model_key"] = selected_key
            st.session_state["model_changed"] = True
            st.rerun() # Force a reload to swap the brain

        st.divider()
        
        if st.button("Clear Memory", type="primary"):
            memory.clear_memory()
            st.rerun()
            
    return selected_key