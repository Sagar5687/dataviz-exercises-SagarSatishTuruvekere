import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------------
st.set_page_config(
    page_title="World Happiness Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ------------------------------------------------------------------
# Load Data
# ------------------------------------------------------------------
df = pd.read_csv("data/world_happiness_2023.csv")

df.columns = [
    "Country",
    "Region",
    "Score",
    "GDP",
    "Social_Support",
    "Life_Expectancy",
    "Freedom",
    "Generosity",
    "Corruption"
]

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.header("Filters")

    regions = ["All"] + sorted(df["Region"].unique().tolist())

    selected_region = st.selectbox(
        "Region",
        regions
    )

    top_n = st.slider(
        "Show Top N Countries",
        min_value=5,
        max_value=25,
        value=15
    )

# ------------------------------------------------------------------
# Filter Data
# ------------------------------------------------------------------
if selected_region == "All":
    filtered = df.copy()
else:
    filtered = df[df["Region"] == selected_region].copy()

# ------------------------------------------------------------------
# Title
# ------------------------------------------------------------------
st.title("🌍 World Happiness Dashboard")

st.caption("Source: World Happiness Report 2023")

# ------------------------------------------------------------------
# KPI Row
# ------------------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Countries",
        len(filtered)
    )

with col2:
    st.metric(
        "Average Score",
        f"{filtered['Score'].mean():.2f}",
        f"{filtered['Score'].mean() - df['Score'].mean():+.2f} vs Global"
    )

with col3:
    happiest = filtered.loc[
        filtered["Score"].idxmax(),
        "Country"
    ]

    st.metric(
        "Happiest Country",
        happiest
    )

st.divider()

# ------------------------------------------------------------------
# Two Charts
# ------------------------------------------------------------------
left, right = st.columns(2)

# ---------------- Chart 1 ----------------
with left:

    st.subheader("Top Countries")

    top = (
        filtered
        .nlargest(top_n, "Score")
        .sort_values("Score")
    )

    fig1 = px.bar(
        top,
        x="Score",
        y="Country",
        orientation="h",
        color_discrete_sequence=["#2E75B6"],
        labels={
            "Score": "Happiness Score",
            "Country": ""
        }
    )

    fig1.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(range=[0, 8.5]),
        font=dict(size=12)
    )

    fig1.update_traces(marker_line_width=0)

    st.plotly_chart(fig1, use_container_width=True)

# ---------------- Chart 2 ----------------
with right:

    st.subheader("GDP vs Happiness")

    fig2 = px.scatter(
        filtered,
        x="GDP",
        y="Score",
        hover_name="Country",
        color_discrete_sequence=["#E63946"]
    )

    fig2.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(size=12)
    )

    st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------------------------
# Step 6
# ------------------------------------------------------------------
st.divider()

st.subheader("Difference from Regional Average")

avg_score = filtered["Score"].mean()

filtered["Score_Diff"] = filtered["Score"] - avg_score

fig3 = px.bar(
    filtered.sort_values("Score_Diff"),
    x="Score_Diff",
    y="Country",
    orientation="h",
    color="Score_Diff",
    color_continuous_scale="RdBu",
    color_continuous_midpoint=0,
    labels={
        "Score_Diff": "Difference",
        "Country": ""
    }
)

fig3.add_annotation(
    x=0,
    y=1.02,
    xref="x",
    yref="paper",
    text=f"Regional Average = {avg_score:.2f}",
    showarrow=False,
    font=dict(size=12)
)

fig3.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=10, r=10, t=10, b=10),
    font=dict(size=12),
    coloraxis_showscale=True
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

st.caption("Built with Streamlit + Plotly")
