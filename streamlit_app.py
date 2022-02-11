import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.read_csv('data.csv')
categories = ['emission_group', 'site_location', 'scope', 'category', 'source_type', 'isic', 'emission_factor']

"""
# Emissions explorer

Use this dashboard to explore your current emissions
"""

total_emissions = f"{df['quantity_ghg_emissions'].sum() / 1000:,.0f} tonnes"
st.metric('Current annual CO2 emmissions', total_emissions, delta=None, delta_color="normal")

with st.expander("Build your exploration with the dropdowns here:"):
    category_select = st.selectbox('Select the category to split by', categories)
    color_select = st.selectbox('Select the bar breakdown', ['none'] + categories)
    filter_select = st.selectbox('Select a filter dimension', ['none'] + categories)
    group_filter = st.multiselect('Choose filters', df[filter_select].unique().tolist() if filter_select != 'none' else [])
    row_filter = st.number_input('Top n items to show', format='%d', value=20)

if color_select == 'none':
    group_list = [category_select]
else:
    group_list = [category_select, color_select]

if filter_select == 'none': 
    detailed_df = df.groupby(group_list)['quantity_ghg_emissions'].sum() / 1000
else:
    detailed_df = df[df[filter_select].isin(group_filter)].groupby(group_list)['quantity_ghg_emissions'].sum() / 1000

detailed_df = detailed_df.to_frame().reset_index().sort_values(by='quantity_ghg_emissions').tail(row_filter)

fig_detail = px.bar(detailed_df, 
                    y=category_select, 
                    x='quantity_ghg_emissions', 
                    color=color_select if color_select != 'none' else None, 
                    orientation='h', 
                    #text='quantity_ghg_emissions', 
                    title=f'Emissions by {category_select}')
st.plotly_chart(fig_detail)