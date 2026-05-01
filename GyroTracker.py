import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client
import os

# Initialize Supabase client
SUPABASE_URL="https://zprmhdtcsjrlqibqhglv.supabase.co"
SUPABASE_KEY="sb_publishable_H1fGiOIh0bC7pmmeoUW00Q_NFMuLzp8"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.markdown("""
<style>

/* Reduce padding for mobile feel */
.block-container {
    padding: 1rem 1rem 2rem 1rem;
}

/* Make buttons big and thumb-friendly */
.stButton>button {
    width: 100%;
    padding: 0.8rem;
    font-size: 18px;
    border-radius: 12px;
    background-color: #0D5EAF;
    color: white;
}

/* Inputs larger */
input, .stSelectbox, .stSlider {
    font-size: 18px !important;
}

/* Cards */
.card {
    background: #F5F9FF;
    padding: 1rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    border-left: 5px solid #0D5EAF;
}
            
/* Target st.text output */
.stText {
    font-size: 14px !important;  /* Smaller than default (~16px) */
    line-height: 1.4;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# APP CONFIG
# -------------------------
st.set_page_config(page_title="Gyro Tracker", page_icon="🌯", layout="centered")

st.title("🌯 Gyro Tracker")

# -------------------------
# TAB NAV
# -------------------------
tab_log, tab_leaderboard = st.tabs(["➕ Log", "🏆 Leaderboard"])



# -------------------------
# PAGE 1: LOG A GYRO
# -------------------------
def log_a_gyro():
    st.header("Log a Gyro")

    name = st.selectbox(
        "Who are you?",
        ["", "Sam","Abbie","Michael","Ruby","Xander","Liv"]
    )
    
    st.text("⭐ Rate your gyro")
    
    rating = st.feedback("stars")

    location = st.text_input("📍 Where did you get it?")

    if st.button("Submit 🌯"):
        if name and location:
            try:
                supabase.table("gyros").insert({
                    "name": name,
                    "rating": rating+1,  # feedback component is 0-indexed
                    "location": location
                }).execute()

                st.success("Gyro logged successfully! 🌯")

            except Exception as e:
                st.error(f"Error logging gyro: {e}")
        else:
            st.warning("Please fill in all fields.")

    st.divider()

    # Show recent entries
    st.subheader("Recent Gyros")

    try:
        response = supabase.table("gyros") \
            .select("*") \
            .order("created_at", desc=True) \
            .limit(10) \
            .execute()

        recent_df = pd.DataFrame(response.data)

        if not recent_df.empty:
            recent_df["created_at"] = pd.to_datetime(recent_df["created_at"])
            st.dataframe(recent_df[["name", "rating", "location", "created_at"]])
        else:
            st.info("No gyros logged yet.")

    except Exception as e:
        st.error(f"Error fetching data: {e}")

# -------------------------
# PAGE 2: LEADERBOARD
# -------------------------
def leaderboard():
    # st.header("Leaderboard")

    # auto_refresh = st.checkbox("Auto refresh every 10s")

    # if auto_refresh:
    #     st.experimental_rerun()

    # try:
    #     response = supabase.table("gyros").select("*").execute()
    #     df = pd.DataFrame(response.data)

    #     if df.empty:
    #         st.info("No gyros logged yet.")
    #     else:
    #         df["created_at"] = pd.to_datetime(df["created_at"])

    #         start = pd.to_datetime("2026-04-27 00:00:00.000+00:00")
    #         end = pd.to_datetime("2026-05-08 23:59:59.999+00:00")

    #         filtered = df[
    #             (df["created_at"] >= start) &
    #             (df["created_at"] <= end)
    #         ]

    #         if filtered.empty:
    #             st.warning("No gyros logged in this period yet.")
    #         else:
    #             # -------------------------
    #             # TOTALS
    #             # -------------------------
    #             totals = (
    #                 filtered.groupby("name")
    #                 .size()
    #                 .reset_index(name="gyros")
    #                 .sort_values(by="gyros", ascending=False)
    #             )

    #             st.subheader("🏆 Total Gyros")
    #             #st.dataframe(totals, use_container_width=True)
    #             st.bar_chart(totals.set_index("name"))

    #             # -------------------------
    #             # AVERAGE RATINGS
    #             # -------------------------
    #             avg_rating = (
    #                 filtered.groupby("name")["rating"]
    #                 .mean()
    #                 .reset_index()
    #             )

    #             st.subheader("⭐ Average Rating")
    #             #st.dataframe(avg_rating, use_container_width=True)

    #             # -------------------------
    #             # TIMELINE
    #             # -------------------------
    #             st.subheader("📈 Gyros Over Time")

    #             timeline = filtered.copy()
    #             timeline["date"] = timeline["created_at"].dt.date

    #             timeline_counts = (
    #                 timeline.groupby(["date", "name"])
    #                 .size()
    #                 .unstack(fill_value=0)
    #             )

    #             st.line_chart(timeline_counts)

    #             # -------------------------
    #             # TIMELINE Trial
    #             # -------------------------
    #             people = ["Sam", "Abbie", "Michael", "Ruby", "Xander", "Liv"]
    #             import plotly.graph_objects as go

    #             df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
    #             df["created_at"] = df["created_at"].dt.tz_convert("Europe/London")

    #             # Ensure datetime
    #             filtered["date"] = filtered["created_at"].dt.tz_convert("Europe/London").dt.date

    #             start_date = pd.Timestamp("2026-04-26", tz="Europe/London")
    #             end_date = pd.Timestamp("2026-05-08 23:59:59", tz="Europe/London")

    #             # Find last date where ANY data exists
    #             if not filtered.empty:
    #                 max_data_date = filtered["date"].max()
    #             else:
    #                 max_data_date = start_date

    #             st.text(f"Data available up to: {max_data_date}")

    #             # Create full date range (for axis)
    #             all_dates = pd.date_range(start_date, end_date)
    #             st.text(f"Full date range: {all_dates[0].date()} to {all_dates[-1].date()}")
                
    #             # Create cumulative counts per person
    #             plot_df = pd.DataFrame(index=all_dates)
                
    #             st.text(f"Filtered data date range: {filtered['date'].min()} to {filtered['date'].max()}")

    #             for person in people:
    #                 person_data = filtered[filtered["name"] == person]

    #                 daily_counts = (
    #                     person_data.groupby("date")
    #                     .size()
    #                     .reindex(all_dates.date, fill_value=0)
    #                 )

    #                 cumulative = daily_counts.cumsum()
                

    #                 # Force everything after last real data date to NaN (so lines stop)
    #                 cumulative.index = pd.to_datetime(cumulative.index)
    #                 cumulative[cumulative.index.date > max_data_date] = None

    #                 plot_df[person] = cumulative.values


    #             fig = go.Figure()
    #             for person in people:
    #                 fig.add_trace(go.Scatter(
    #                     x=plot_df.index,
    #                     y=plot_df[person],
    #                     mode="lines+markers",
    #                     name=person
    #                 ))
    #             fig.update_layout(
    #                 title="Cumulative Gyros Over Time",
    #                 xaxis_title="Date",
    #                 yaxis_title="Cumulative Gyros",
    #                 xaxis=dict(tickformat="%Y-%m-%d"),
    #                 legend_title="Person"
    #             )
    #             st.plotly_chart(fig, use_container_width=True)


    # except Exception as e:
    #     st.error(f"Error loading leaderboard: {e}")

    st.title("🏆 Gyro Leaderboard")

    people = ["Sam", "Abbie", "Michael", "Ruby", "Xander", "Rosi"]
    response = supabase.table("gyros").select("*").execute()
    df = pd.DataFrame(response.data)


    if not df.empty:
        df["created_at"] = pd.to_datetime(df["created_at"], utc=True)

        start = pd.Timestamp("2026-05-01", tz="UTC")
        end = pd.Timestamp("2026-05-08", tz="UTC")

        filtered = df[(df["created_at"] >= start) & (df["created_at"] <= end)]

        # Count gyros per person, force all people to appear
        totals = (
            filtered.groupby("name")
            .size()
            .reindex(people, fill_value=0)
            .reset_index(name="gyros")
        )

        # Rank with ties (1 = best)
        totals["rank"] = totals["gyros"].rank(method="min", ascending=False).astype(int)

        # Sort for display
        totals = totals.sort_values(["rank", "name"]).reset_index(drop=True)

    else:
        # No data case → everyone at 0
        totals = pd.DataFrame({
            "name": people,
            "gyros": [0] * len(people)
        })
        totals["rank"] = 1
    
    # -------------------------
    # MEDAL FUNCTION
    # -------------------------
    def get_medal(rank):
        if rank == 1:
            return "🥇"
        elif rank == 2:
            return "🥈"
        elif rank == 3:
            return "🥉"
        return ""

    # -------------------------
    # RENDER (MOBILE CARDS)
    # -------------------------
    #st.subheader("🏆 Gyro Leaderboard")

    max_gyros = totals["gyros"].max() if not totals.empty else 1

    for _, row in totals.iterrows():
        medal = get_medal(row["rank"])

        # Highlight leaders
        highlight = "#FFF3CD" if row["rank"] == 1 else "#F5F9FF"

        # Avoid divide by zero
        progress = row["gyros"] / max_gyros if max_gyros > 0 else 0

        st.markdown(f"""
    <div style="
        background:{highlight};
        padding:1rem;
        border-radius:12px;
        margin-bottom:0.75rem;
        border-left:6px solid #0D5EAF;
    ">
        <h3 style="margin-bottom:0.3rem;">
            {medal} {row['name']}
        </h3>
        <p style="margin:0;">
            <b>{row['gyros']}</b> gyros eaten
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    import plotly.graph_objects as go

    df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
    df["created_at"] = df["created_at"].dt.tz_convert("Europe/London")

    # Ensure datetime
    filtered["date"] = filtered["created_at"].dt.tz_convert("Europe/London").dt.date

    start_date = pd.Timestamp("2026-05-01", tz="Europe/London")
    end_date = pd.Timestamp("2026-05-08 23:59:59", tz="Europe/London")

    # Find last date where ANY data exists
    if not filtered.empty:
        max_data_date = filtered["date"].max()
    else:
        max_data_date = start_date

    #st.text(f"Data available up to: {max_data_date}")

    # Create full date range (for axis)
    all_dates = pd.date_range(start_date, end_date)
    #st.text(f"Full date range: {all_dates[0].date()} to {all_dates[-1].date()}")
    
    # Create cumulative counts per person
    plot_df = pd.DataFrame(index=all_dates)
    
    #st.text(f"Filtered data date range: {filtered['date'].min()} to {filtered['date'].max()}")

    for person in people:
        person_data = filtered[filtered["name"] == person]

        daily_counts = (
            person_data.groupby("date")
            .size()
            .reindex(all_dates.date, fill_value=0)
        )

        cumulative = daily_counts.cumsum()
    

        # Force everything after last real data date to NaN (so lines stop)
        cumulative.index = pd.to_datetime(cumulative.index)
        cumulative[cumulative.index.date > max_data_date] = None

        plot_df[person] = cumulative.values


    fig = go.Figure()
    for person in people:
        fig.add_trace(go.Scatter(
            x=plot_df.index,
            y=plot_df[person],
            mode="lines+markers",
            name=person
        ))
    fig.update_layout(
        title="Cumulative Gyros Over Time",
        xaxis_title="Date",
        yaxis_title="Cumulative Gyros",
        xaxis=dict(tickformat="%Y-%m-%d"),
        legend_title="Person"
    )
    st.plotly_chart(fig, use_container_width=True)


with tab_log:
    log_a_gyro()

with tab_leaderboard:
    leaderboard()
