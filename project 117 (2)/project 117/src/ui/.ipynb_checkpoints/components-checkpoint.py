import streamlit as st
import pandas as pd
from config.settings import APP_CONFIG

def display_header():
    """Display application header with logo and title"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #1f77b4; font-size: 3rem; margin-bottom: 0;">
            📊 AI Data Visualization Agent
        </h1>
        <p style="font-size: 1.2rem; color: #666; margin-top: 0;">
            Powered by Together AI & E2B Code Interpreter
        </p>
        <p style="font-size: 1rem; color: #888;">
            Upload your data and let AI create stunning visualizations!
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_footer():
    """Display application footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; color: #666;">
        <p>Built with ❤️ using Streamlit, Together AI & E2B | Version {}</p>
        <p>
            <a href="https://api.together.ai" target="_blank">Together AI</a> | 
            <a href="https://e2b.dev" target="_blank">E2B</a> | 
            <a href="https://streamlit.io" target="_blank">Streamlit</a>
        </p>
    </div>
    """.format(APP_CONFIG['version']), unsafe_allow_html=True)

def display_data_summary(df: pd.DataFrame):
    """Display comprehensive data summary"""
    st.subheader("📊 Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Rows", f"{len(df):,}")
    
    with col2:
        st.metric("Total Columns", len(df.columns))
    
    with col3:
        numeric_cols = df.select_dtypes(include=['number']).columns
        st.metric("Numeric Columns", len(numeric_cols))
    
    with col4:
        missing_values = df.isnull().sum().sum()
        st.metric("Missing Values", f"{missing_values:,}")
    
    # Column information
    with st.expander("📋 Column Details"):
        col_info = []
        for col in df.columns:
            col_type = str(df[col].dtype)
            null_count = df[col].isnull().sum()
            null_pct = (null_count / len(df)) * 100
            unique_count = df[col].nunique()
            
            col_info.append({
                'Column': col,
                'Type': col_type,
                'Null Count': null_count,
                'Null %': f"{null_pct:.1f}%",
                'Unique Values': unique_count
            })
        
        st.dataframe(pd.DataFrame(col_info), use_container_width=True)

def display_error_message(error_msg: str, error_type: str = "Error"):
    """Display formatted error message"""
    st.error(f"❌ {error_type}: {error_msg}")

def display_success_message(msg: str):
    """Display formatted success message"""
    st.success(f"✅ {msg}")

def display_warning_message(msg: str):
    """Display formatted warning message"""
    st.warning(f"⚠️ {msg}")

def display_info_message(msg: str):
    """Display formatted info message"""
    st.info(f"ℹ️ {msg}")

def create_download_button(data, filename: str, label: str = "Download"):
    """Create download button for data"""
    if isinstance(data, pd.DataFrame):
        csv = data.to_csv(index=False)
        st.download_button(
            label=f"📥 {label}",
            data=csv,
            file_name=filename,
            mime='text/csv'
        )
    else:
        st.download_button(
            label=f"📥 {label}",
            data=str(data),
            file_name=filename,
            mime='text/plain'
        )