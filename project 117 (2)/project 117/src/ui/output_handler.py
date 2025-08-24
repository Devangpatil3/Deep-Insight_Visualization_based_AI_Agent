import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import base64
from io import BytesIO
from typing import List, Any, Optional
import json
import logging

class OutputHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def display_results(self, code_results: Optional[List[Any]], llm_response: str, exec_code: str):
        """Display execution results with proper formatting"""
        
        # Display LLM Response
        st.subheader("🤖 AI Analysis")
        with st.expander("View Full Response", expanded=True):
            st.markdown(llm_response)
        
        # Display Executed Code
        st.subheader("💻 Generated Code")
        with st.expander("View Python Code", expanded=False):
            st.code(exec_code, language='python')
        
        # Display Results
        if code_results:
            st.subheader("📊 Results")
            self._process_results(code_results)
        else:
            st.info("No output generated from code execution.")
    
    def _process_results(self, results: List[Any]):
        """Process and display different types of results"""
        for i, result in enumerate(results):
            if hasattr(result, 'is_main_result') and result.is_main_result:
                if result.text:
                    st.text(result.text)
                
                if hasattr(result, 'formats'):
                    self._display_formats(result.formats)
            else:
                # Handle string results
                if isinstance(result, str):
                    # Try to parse as JSON for structured data
                    try:
                        json_data = json.loads(result)
                        st.json(json_data)
                    except:
                        st.text(result)
                else:
                    st.write(result)
    
    def _display_formats(self, formats):
        """Display different format types (images, tables, etc.)"""
        for format_item in formats:
            if hasattr(format_item, 'type'):
                if format_item.type == 'image':
                    self._display_image(format_item)
                elif format_item.type == 'html':
                    self._display_html(format_item)
                elif format_item.type == 'json':
                    self._display_json(format_item)
                else:
                    st.write(format_item)
    
    def _display_image(self, image_result):
        """Display image results"""
        try:
            if hasattr(image_result, 'data'):
                # Decode base64 image
                image_data = base64.b64decode(image_result.data)
                image = Image.open(BytesIO(image_data))
                st.image(image, caption="Generated Visualization", use_column_width=True)
        except Exception as e:
            self.logger.error(f"Error displaying image: {str(e)}")
            st.error("Failed to display image")
    
    def _display_html(self, html_result):
        """Display HTML results"""
        try:
            if hasattr(html_result, 'data'):
                st.components.v1.html(html_result.data, height=400)
        except Exception as e:
            self.logger.error(f"Error displaying HTML: {str(e)}")
            st.error("Failed to display HTML content")
    
    def _display_json(self, json_result):
        """Display JSON results"""
        try:
            if hasattr(json_result, 'data'):
                st.json(json_result.data)
        except Exception as e:
            self.logger.error(f"Error displaying JSON: {str(e)}")
            st.error("Failed to display JSON content")
    
    def display_dataframe_analysis(self, df: pd.DataFrame):
        """Display comprehensive DataFrame analysis"""
        st.subheader("📈 Data Analysis")
        
        tabs = st.tabs(["Summary", "Statistics", "Correlations", "Missing Data"])
        
        with tabs[0]:
            self._display_basic_info(df)
        
        with tabs[1]:
            self._display_statistics(df)
        
        with tabs[2]:
            self._display_correlations(df)
        
        with tabs[3]:
            self._display_missing_data(df)
    
    def _display_basic_info(self, df: pd.DataFrame):
        """Display basic DataFrame information"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Shape:**", df.shape)
            st.write("**Memory Usage:**", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            
        with col2:
            st.write("**Column Types:**")
            dtype_counts = df.dtypes.value_counts()
            for dtype, count in dtype_counts.items():
                st.write(f"- {dtype}: {count}")
    
    def _display_statistics(self, df: pd.DataFrame):
        """Display statistical summary"""
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            st.write("**Numeric Columns Summary:**")
            st.dataframe(numeric_df.describe())
        else:
            st.info("No numeric columns found for statistical analysis.")
    
    def _display_correlations(self, df: pd.DataFrame):
        """Display correlation matrix"""
        numeric_df = df.select_dtypes(include=['number'])
        if len(numeric_df.columns) > 1:
            corr_matrix = numeric_df.corr()
            
            # Create heatmap using Plotly
            fig = px.imshow(
                corr_matrix,
                title="Correlation Matrix",
                color_continuous_scale="RdBu",
                aspect="auto"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 numeric columns for correlation analysis.")
    
    def _display_missing_data(self, df: pd.DataFrame):
        """Display missing data analysis"""
        missing_data = df.isnull().sum()
        missing_pct = (missing_data / len(df)) * 100
        
        missing_df = pd.DataFrame({
            'Column': missing_data.index,
            'Missing Count': missing_data.values,
            'Missing Percentage': missing_pct.values
        })
        
        missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values(
            'Missing Count', ascending=False
        )
        
        if not missing_df.empty:
            st.dataframe(missing_df, use_container_width=True)
            
            # Create bar chart for missing data
            fig = px.bar(
                missing_df,
                x='Column',
                y='Missing Percentage',
                title="Missing Data by Column",
                labels={'Missing Percentage': 'Missing %'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No missing data found!")