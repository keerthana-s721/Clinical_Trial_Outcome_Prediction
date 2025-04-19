import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    # Fix the file path, remove any unwanted characters
    df = pd.read_csv(r'D:\10th sem project\db2\clinical_trial_cleaned.csv')
    return df

df = load_data()

# Set the page layout
st.set_page_config(page_title="Clinical Trials Dashboard", layout="wide")
st.title("🧪 Clinical Trials Dashboard")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
selected_disease = st.sidebar.multiselect("Select Disease", df['disease'].dropna().unique())
selected_gender = st.sidebar.selectbox("Select Gender", ['All'] + list(df['Gender'].dropna().unique()))
selected_age = st.sidebar.selectbox("Select Age Group", ['All'] + list(df['Population Age'].dropna().unique()))
selected_phase = st.sidebar.multiselect("Trial Phases", df['Phase'].dropna().unique())

filtered_df = df.copy()
if selected_disease:
    filtered_df = filtered_df[filtered_df['disease'].isin(selected_disease)]
if selected_gender != 'All':
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
if selected_age != 'All':
    filtered_df = filtered_df[filtered_df['Population Age'] == selected_age]
if selected_phase:
    filtered_df = filtered_df[filtered_df['Phase'].isin(selected_phase)]

# ----------- 1. Sponsor and Trial Details ----------- 
st.subheader("🏢 Sponsor & Trial Details")
sponsor_counts = filtered_df['sponsor_name'].value_counts().reset_index()
sponsor_counts.columns = ['Sponsor', 'Trial Count']
fig_sponsor = px.bar(sponsor_counts.head(10), x='Sponsor', y='Trial Count', title="Top Sponsors")
st.plotly_chart(fig_sponsor, use_container_width=True)

# ----------- 2. Trial Information ----------- 
st.subheader("📋 Trial Information")
with st.expander("📄 View Trial Details"):
    trial_info = filtered_df[['a_protocol_code', 'a_title_full', 'a_title_eclang', 'disease', 'Phase', 'Start Date']]
    st.dataframe(trial_info)

# ----------- 3. Disease & Treatment Information ----------- 
st.subheader("💊 Disease & Treatment Details")
disease_treatment = filtered_df[['disease', 'e_therapy', 'e_safety', 'e_efficacy', 'e_pharmacokinetic']].dropna()
fig_disease_treatment = px.sunburst(disease_treatment, path=['disease', 'e_therapy', 'e_efficacy'], title="Disease and Treatment Overview")
st.plotly_chart(fig_disease_treatment, use_container_width=True)

# ----------- 4. Population Demographics ----------- 
st.subheader("👥 Population Demographics")
col1, col2 = st.columns(2)
with col1:
    fig_gender = px.pie(filtered_df, names='Gender', title='Gender Distribution')
    st.plotly_chart(fig_gender, use_container_width=True)

with col2:
    fig_age = px.pie(filtered_df, names='Population Age', title='Age Group Distribution')
    st.plotly_chart(fig_age, use_container_width=True)

# ----------- 5. Trial Phases ----------- 
st.subheader("🧬 Clinical Trial Phases")
phase_counts = filtered_df['Phase'].value_counts().reset_index()
phase_counts.columns = ['Phase', 'Trial Count']
fig_phase = px.bar(phase_counts, x='Phase', y='Trial Count', title='Trial Count per Phase', color='Trial Count')
st.plotly_chart(fig_phase, use_container_width=True)

# ----------- 6. Trial End Status ----------- 
st.subheader("✅ Trial End Status")
status_counts = filtered_df['End of Trial Status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']
fig_status = px.pie(status_counts, names='Status', values='Count', title='Distribution of Trial End Status')
st.plotly_chart(fig_status, use_container_width=True)

# ----------- 7. Investigational Medicinal Product (IMP) Details ----------- 
st.subheader("💊 Investigational Medicinal Product (IMP)")
imp_drug_info = filtered_df[['imp_product_name', 'imp_role', 'imp_marketing_auth', 'imp_pharma_form', 'imp_admin_routes']]
with st.expander("💊 View IMP Information"):
    st.dataframe(imp_drug_info)

# ----------- 8. Trial Inclusion/Exclusion Criteria ----------- 
st.subheader("📋 Inclusion/Exclusion Criteria")
criteria_info = filtered_df[['e_inclusion', 'e_exclusion']].dropna()
with st.expander("📋 View Inclusion/Exclusion Criteria"):
    st.dataframe(criteria_info)

# ----------- 9. Competent Authority and Ethics Committee ----------- 
st.subheader("📜 Competent Authority & Ethics Committee")
competent_authority = filtered_df[['Competent Authority Decision', 'Competent Authority Decision Date']].dropna()
ethics_committee = filtered_df[['Ethics Committee Opinion', 'Ethics Committee Opinion Date']].dropna()

with st.expander("📜 View Competent Authority & Ethics Committee Decisions"):
    st.subheader("Competent Authority Decisions")
    st.dataframe(competent_authority)
    st.subheader("Ethics Committee Opinions")
    st.dataframe(ethics_committee)

# ----------- Final Data Table ----------- 
with st.expander("📄 View Filtered Clinical Trials Data"):
    st.dataframe(filtered_df)
