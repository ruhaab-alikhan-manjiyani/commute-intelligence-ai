import streamlit as st
import pandas as pd

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Commute Wise Bengaluru",
    page_icon="🏠",
    layout="wide"
)
st.markdown("""
### Live smarter. Commute shorter.

Discover Bangalore neighborhoods based on
your office location and monthly budget.
""")

# -----------------------------------
# LOAD DATA
# -----------------------------------

df = pd.read_csv("areas.csv")

# -----------------------------------
# COMMUTE DATA
# -----------------------------------

commute_data = {
    "whitefield": {
        "Brookefield": "15 mins",
        "Hoodi": "12 mins",
        "Kundalahalli": "18 mins",
        "Marathahalli": "20 mins"
    },
    "electronic city": {
        "Electronic City": "10 mins",
        "HSR Layout": "25 mins"
    }
}

# -----------------------------------
# HEADER
# -----------------------------------

st.title("🏠 CommuteWise Bengaluru")

st.markdown(
    """
    Find the best Bangalore neighborhoods based on
    your rent budget and office location.
    """
)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.header("User Preferences")

office = st.sidebar.text_input(
    "Office Location",
    placeholder="Example: Whitefield"
)

budget = st.sidebar.number_input(
    "Monthly Rent Budget (₹)",
    min_value=10000,
    max_value=100000,
    value=25000,
    step=1000
)

search = st.sidebar.button(
    "🚀 Discover Areas",
    use_container_width=True
)

# -----------------------------------
# SEARCH LOGIC
# -----------------------------------

if search:

    recommendations = df.copy()

    # Budget filter
    recommendations = recommendations[
        recommendations["AvgRent"] <= budget
    ]

    # Office-specific recommendations

    if office.lower() == "whitefield":

        preferred_areas = [
            "Brookefield",
            "Hoodi",
            "Kundalahalli",
            "Marathahalli"
        ]

        recommendations = recommendations[
            recommendations["Area"].isin(preferred_areas)
        ]

    elif office.lower() == "electronic city":

        preferred_areas = [
            "Electronic City",
            "HSR Layout"
        ]

        recommendations = recommendations[
            recommendations["Area"].isin(preferred_areas)
        ]

    # Prioritize metro-connected areas

    recommendations = recommendations.sort_values(
        by="Metro",
        ascending=False
    )

    top_areas = recommendations.head(3)

    # -----------------------------------
    # RESULTS
    # -----------------------------------

    st.subheader("🏆 Recommended Areas")

    if not top_areas.empty:

        cols = st.columns(3)

        for idx, (_, row) in enumerate(top_areas.iterrows()):

            commute_time = "Approx. 20-30 mins"

            if office.lower() in commute_data:

                commute_time = commute_data[
                    office.lower()
                ].get(
                    row["Area"],
                    "Approx. 20-30 mins"
                )

            with cols[idx]:

                st.markdown(
    f"""
    <div style="
        background: rgba(255,255,255,0.05);
        padding:20px;
        border-radius:20px;
        backdrop-filter: blur(12px);
        border:1px solid rgba(255,255,255,0.1);
        margin-bottom:15px;
    ">
        <h3>📍 {row['Area']}</h3>
        <p>💰 Rent: ₹{row['AvgRent']:,}</p>
        <p>🚗 Commute: {commute_time}</p>
        <p>🚇 Metro: {row['Metro']}</p>
        <p>🏙️ {row['BestFor']}</p>
    </div>
    """,
    unsafe_allow_html=True
)

    else:

        st.warning(
            "No suitable areas found within your budget."
        )

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption("🏠 CommuteWise Bengaluru")
st.caption("🖇️ Built with Python + Streamlit")
st.caption(
    "📊 Area and rent information is indicative and may vary."
)
st.caption("✨ Made by Ruhaab")