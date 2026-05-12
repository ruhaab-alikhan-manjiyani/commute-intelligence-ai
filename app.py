import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(
    page_title="Commute Intelligence AI",
    page_icon="🚦",
    layout="wide"
)

# Load CSV
df = pd.read_csv("areas.csv")

# Title
st.title("🚦 Commute Intelligence AI")
st.markdown(
    "Smart Bangalore area recommendations based on budget, commute, and lifestyle."
)

# Sidebar
st.sidebar.header("User Preferences")

office = st.sidebar.text_input(
    "Office Location",
    placeholder="Example: Whitefield"
)

budget = st.sidebar.slider(
    "Monthly Rent Budget",
    10000,
    50000,
    25000
)

# Button
search = st.sidebar.button("Find Best Areas")

# Main Logic
if search:

    recommendations = df.copy()

    # Budget filter
    recommendations = recommendations[
        recommendations["AvgRent"] <= budget
    ]

    # Score system
    recommendations["Score"] = 0

    # Metro scoring
    recommendations.loc[
        recommendations["Metro"] == "Yes",
        "Score"
    ] += 3

    # Traffic scoring
    recommendations.loc[
        recommendations["Traffic"] == "High",
        "Score"
    ] -= 2

    recommendations.loc[
        recommendations["Traffic"] == "Medium",
        "Score"
    ] += 1

    recommendations.loc[
        recommendations["Traffic"] == "Low",
        "Score"
    ] += 3

    # Office matching
    if office.lower() == "whitefield":

        preferred_areas = [
            "Brookefield",
            "Hoodi",
            "Kundalahalli",
            "Marathahalli"
        ]

        recommendations.loc[
            recommendations["Area"].isin(preferred_areas),
            "Score"
        ] += 5

    elif office.lower() == "electronic city":

        preferred_areas = [
            "Electronic City",
            "HSR Layout"
        ]

        recommendations.loc[
            recommendations["Area"].isin(preferred_areas),
            "Score"
        ] += 5

    # Sort results
    recommendations = recommendations.sort_values(
        by="Score",
        ascending=False
    )

    top_areas = recommendations.head(3)

    # Results
    st.subheader("🏆 Top Recommendations")

    if not top_areas.empty:

        col1, col2, col3 = st.columns(3)

        columns = [col1, col2, col3]

        for idx, (_, row) in enumerate(top_areas.iterrows()):

            with columns[idx]:

                st.container()

                st.markdown(
                    f"""
                    ### 📍 {row['Area']}

                    💰 **Average Rent:** ₹{row['AvgRent']}

                    🚇 **Metro Access:** {row['Metro']}

                    🚦 **Traffic Level:** {row['Traffic']}

                    🏙️ **Best For:** {row['BestFor']}

                    ⭐ **Recommendation Score:** {row['Score']}
                    """
                )

    else:
        st.warning("No suitable recommendations found.")

# Footer
st.markdown("---")
st.caption("Built with Python + Streamlit")
st.caption("Datasourced from local Bangalore area data, may not be fully accurate.")
st.caption("Built by Ruhaab")