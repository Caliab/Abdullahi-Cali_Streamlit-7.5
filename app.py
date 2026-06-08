import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="How Bacteria Respond to Antibiotics", layout="wide")
data = pd.read_json("burtin.json")

st.title("How Bacteria Respond to Antibiotics")
st.write("#### While Neomycin and Streptomycin work consistently well across the board, Penicillin is the opposite it completely destroys Gram-positive bacteria (blue) but is  less effective against Gram-negative strains (red).")
st.write("Click on any bar to filter the data, and on the background of a chart to reset.")


st.markdown("Average MIC")
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    Neomycin_avg = data["Neomycin"].mean().round(2)
    st.metric(label="Neomycin", value=Neomycin_avg)

with metric_col2:
    Streptomycin_avg = data["Streptomycin"].mean().round(2)
    st.metric(label="Streptomycin", value=Streptomycin_avg)

with metric_col3:
    Penicillin_avg = data["Penicillin"].mean().round(2)
    st.metric(label="Penicillin", value=Penicillin_avg)

st.markdown("---")


# --- 1. Define ONE global selection parameter ---
# 'empty="all"' means everything is fully colored by default until you click something
click_selection = alt.selection_point(fields=["Bacteria"], empty="all")

# Common chart properties to keep code clean
axis_config = alt.Axis(labelLimit=300, labelPadding=15, offset=5)

# --- Chart 1: Neomycin ---
chart1 = (
    alt.Chart(data)
    .mark_bar()
    .encode(
        x=alt.X(
            "Neomycin:Q", 
            scale=alt.Scale(type="symlog", constant=0.001, domain=[0.001, 100]), 
            axis=alt.Axis(values=[0.001, 0.01, 0.1, 1, 10, 100], format=".3f"), 
            title="MIC (ug/ml)"
        ),
        y=alt.Y("Bacteria:N", sort="-x", title="Bacteria", axis=alt.Axis(labelLimit=200, labelPadding=15,offset=100)),
        # --- The Magic Highlighting Color Condition ---
        color=alt.condition(
            click_selection,
            alt.Color("Gram_Staining:N", scale=alt.Scale(domain=["positive", "negative"], range=["#1f77b4", "#800000"]), title="Gram Stain"),
            alt.value("#e0e0e0")  # Light gray for unselected bars
        ),
        # --- Opacity Condition makes unselected bars look faint ---
        opacity=alt.condition(click_selection, alt.value(1.0), alt.value(0.20)),
        tooltip=["Bacteria", "Neomycin", "Gram_Staining"],
    )
    .properties(height=400, title="Neomycin: Broad and Potent Antibiotic")
)

# --- Chart 2: Streptomycin ---
chart2 = (
    alt.Chart(data)
    .mark_bar()
    .encode(
        x=alt.X(
            "Streptomycin:Q", 
            scale=alt.Scale(type="symlog", constant=0.001, domain=[0.001, 100]), 
            axis=alt.Axis(values=[0.001, 0.01, 0.1, 1, 10, 100], format=".3f"), 
            title="MIC (ug/ml)"
        ),
        y=alt.Y("Bacteria:N", sort="-x", title="Bacteria", axis=alt.Axis(labelLimit=200, labelPadding=15,offset=100)),
        color=alt.condition(
            click_selection,
            alt.Color("Gram_Staining:N", scale=alt.Scale(domain=["positive", "negative"], range=["#1f77b4", "#800000"]), title="Gram Stain"),
            alt.value("#e0e0e0")
        ),
        opacity=alt.condition(click_selection, alt.value(1.0), alt.value(0.20)),
        tooltip=["Bacteria", "Streptomycin", "Gram_Staining"],
    )
    .properties(height=400, title="Streptomycin: Moderate Effectiveness Across Most Bacteria")
)

# --- Chart 3: Penicillin ---
chart3 = (
    alt.Chart(data)
    .mark_bar()
    .encode(
        x=alt.X(
            "Penicillin:Q", 
            scale=alt.Scale(type="symlog", constant=0.001, domain=[0.001, 1000]), 
            axis=alt.Axis(values=[0.001, 0.01, 0.1, 1, 10, 100, 500], format=".3f"), 
            title="MIC (ug/ml)"
        ),
        y=alt.Y("Bacteria:N", sort="-x", title="Bacteria", axis=alt.Axis(labelLimit=200, labelPadding=15,offset=100)),
        color=alt.condition(
            click_selection,
            alt.Color("Gram_Staining:N", scale=alt.Scale(domain=["positive", "negative"], range=["#1f77b4", "#800000"]), title="Gram Stain"),
            alt.value("#e0e0e0")
        ),
        opacity=alt.condition(click_selection, alt.value(1.0), alt.value(0.20)),
        tooltip=["Bacteria", "Penicillin", "Gram_Staining"],
    )
    .properties(height=600, title="Penicillin: Effective Mainly on Gram Positive Bacteria")
)

# --- 2. STITCH THEM TOGETHER AS ONE DASHBOARD ---
# We add the parameters to the combined dashboard layout, and share the color legend.
dashboard = (
    alt.vconcat(chart1, chart2, chart3)
    .add_params(click_selection)
    .resolve_scale(color="shared")
    .configure_view(stroke=None) # Cleans up border lines between concatenated charts
)

# --- 3. Render the unified layout ---
st.altair_chart(dashboard, use_container_width=True)