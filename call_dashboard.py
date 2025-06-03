
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns

# Page setup
st.set_page_config(page_title="📞 Call Metrics: Unpacking Support Satisfaction", layout="centered")

# Title
st.title("📞 Call Metrics: Unpacking Support Satisfaction")
st.write("The Customer Support team at Halo, a subscription-based digital content platform, is analyzing support call data for Q1 of 2021 to understand what drives customer satisfaction. This project explores patterns in call metadata, agent performance, and customer outcomes to identify ways to improve service quality.")
st.markdown("[Click here to explore the project code on GitHub.](https://github.com/Grace-OO/Call_Metrics)")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Call_Center_Dataset.csv")
    df.columns = (
    df.columns.str.strip()                             # Remove leading/trailing spaces
              .str.replace(' ', '_')                   # Replace spaces with underscores
              .str.replace(r'\W+', '', regex=True)     # Remove non-alphanumeric characters
              .str.lower())                             # Lowercase everything

    df['date'] = pd.to_datetime(df['date'])
    df['avgtalkduration'] = pd.to_timedelta(df['avgtalkduration'])
    df['talk_minutes'] = df['avgtalkduration'].dt.total_seconds() / 60
    df['talk_minutes_rounded'] = df['talk_minutes'].round()
    df['speed_of_answer_in_seconds']= df['speed_of_answer_in_seconds'].fillna(df['speed_of_answer_in_seconds'].mean())
    df['satisfaction_rating']= df['satisfaction_rating'].fillna(df['satisfaction_rating'].mean())
    df['resolved_numeric'] = df['resolved'].map({'Y': 1, 'N': 0})
    df['avgtalkduration'] = df['avgtalkduration'].fillna(df['avgtalkduration'].mean())
    df['day_of_week'] = pd.Categorical(
        df['date'].dt.day_name(),
        categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        ordered=True
    )
    df['speed_rounded'] = df['speed_of_answer_in_seconds'].round()
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.time
    df['hour'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.hour
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("📊 Filters")

# Date range filter
min_date = df['date'].min()
max_date = df['date'].max()
start_date, end_date = st.sidebar.date_input("Select date range:", [min_date, max_date], min_value=min_date, max_value=max_date)

# Day of week filter
days = st.sidebar.multiselect("Select days of the week:", options=df['day_of_week'].cat.categories, default=list(df['day_of_week'].cat.categories))

# Chart toggles
show_chart1 = st.sidebar.checkbox("📈 Satisfaction vs Talk Duration", value=True)
show_chart2 = st.sidebar.checkbox("📈 Satisfaction vs Speed of Answer", value=True)
show_chart3 = st.sidebar.checkbox("📈 Satisfaction by Hour", value=True)
show_chart4 = st.sidebar.checkbox("📈 Satisfaction by Day", value=True)
show_chart5 = st.sidebar.checkbox("📈 Satisfaction by Topic", value=True)
show_chart6 = st.sidebar.checkbox("📈 Satisfaction by Agent", value=True)
show_chart7 = st.sidebar.checkbox("📈 Satisfaction by Resolution Status", value=True)
# Filtered data
filtered_df = df[
    (df['date'] >= pd.to_datetime(start_date)) &
    (df['date'] <= pd.to_datetime(end_date)) &
    (df['day_of_week'].isin(days))
]

# current satisfaction rating
metric= filtered_df['satisfaction_rating'].mean()
st.metric('##### Average Satisfaction Rating:', f"⭐{metric:.1f}/5.0")

st.markdown("---")


# Charts

if show_chart1:
    st.subheader("**1. How does call duration relate to satisfaction ratings?**")
    
    duration_satisfaction = filtered_df.groupby('talk_minutes_rounded')['satisfaction_rating'].mean()
    style.use('ggplot')
    fig, ax = plt.subplots(figsize= (10,7))
    duration_satisfaction.plot(kind='line', marker='o', ax=ax, color= 'steelblue')
    ax.set_title("Satisfaction vs Call Duration")
    ax.set_xlabel("Call Duration (minutes)")
    ax.set_ylabel("Average Satisfaction Rating")
    ax.grid(True)
    st.pyplot(fig)
    st.write("""
    Keeping call durations under one minute is linked to higher satisfaction scores, indicating that faster interactions may enhance the customer experience.
    
    Streamlining issue resolution could help improve service satisfaction.
    """)

if show_chart2:
    st.subheader("**2. Does the speed of answer impact satisfaction?**")

    speed_satisfaction = filtered_df.groupby('speed_rounded')['satisfaction_rating'].mean()

    fig2, ax = plt.subplots(figsize= (10,7))
    speed_satisfaction.plot(kind='line', marker='o', ax=ax, color= 'steelblue')
    ax.set_title("Satisfaction vs Speed of Answer")
    ax.set_xlabel("Speed of Answer (seconds)")
    ax.set_ylabel("Average Satisfaction Rating")
    ax.grid(True)
    st.pyplot(fig2)
    st.write("""
    Quick response times alone do not lead to higher satisfaction ratings, indicating that what happens during the call may be more important than how quickly it's answered. Calls answered after the 2-minute mark noticeably rank lower.

    Focus should shift toward enhancing call quality and issue resolution.
    """)

if show_chart3:
    st.subheader("**3. Does the hour of day impact satisfaction?**")
    
    hourly_satisfaction = filtered_df.groupby('hour')['satisfaction_rating'].mean()

    fig3, ax = plt.subplots(figsize= (10,7))
    hourly_satisfaction.plot(kind='line', marker='o', ax=ax, color= 'steelblue')
    ax.set_title("Satisfaction by Hour of Day")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Avg Satisfaction Rating")
    ax.grid(True)
    st.pyplot(fig3)
    st.write("""
    Customer satisfaction ratings dip noticeably around 2 PM before rising again at 6 PM. 
    
    This trend suggests a need for further investigation into what occurs during the 2 PM period that may be impacting service quality
    """)


if show_chart4: 
    st.subheader("**4. Does the day of the week affect satisfaction ratings?**")
    avg_satisfaction_by_day = filtered_df.groupby('day_of_week')['satisfaction_rating'].mean()

    fig4, ax = plt.subplots(figsize= (10,7))
    avg_satisfaction_by_day.plot(kind= 'line', ax=ax, marker= 'o', color= 'steelblue')
    ax.set_title("Average Satisfaction by Day of the Week")
    ax.set_xlabel("Day")
    ax.set_ylabel("Average Satisfaction Rating")
    ax.set_xticks(range(len(avg_satisfaction_by_day.index)))
    ax.set_xticklabels(avg_satisfaction_by_day.index, rotation=45)
    ax.grid(True)
    st.pyplot(fig4)
    st.write("Satisfaction ratings drop on Fridays, Saturdays, and Sundays, but this decline is not linked to call volume.")
    summary = filtered_df.groupby('day_of_week', observed=True).agg({
        'satisfaction_rating': 'mean',
        'call_id': 'count'
    }).rename(columns={'call_id': 'call_volume'})

    fig, ax1 = plt.subplots(figsize= (10,7))
    ax1.bar(summary.index, summary['call_volume'], color='darkgray', label='Call Volume')
    ax2 = ax1.twinx()
    ax2.plot(summary.index, summary['satisfaction_rating'], color='steelblue', marker='o', label='Satisfaction')
    ax1.set_ylabel("Call Volume")
    ax2.set_ylabel("Avg Satisfaction Rating")
    ax1.set_title("Satisfaction and Call Volume by Day")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.write('Further investigation into service quality or staffing factors during weekends may be warranted.')

if show_chart5:
    st.subheader("**5. Do certain call topics consistently result in higher or lower satisfaction?**")
    topic_rating = filtered_df.groupby('topic')['satisfaction_rating'].mean().sort_values()
    
    fig5, ax = plt.subplots(figsize= (10,7))
    topic_rating.plot(kind='barh', ax= ax, color= 'steelblue')
    ax.set_title('Average Satisfaction by Topic')
    ax.set_ylabel("Support Topic")
    ax.set_xlabel("Average Satisfaction Rating")
    ax.grid(True)
    st.pyplot(fig5)
    st.write("Satisfaction levels remain relatively consistent regardless of the call topic, suggesting that factors other than topic drive customer satisfaction.")

if show_chart6:
    st.subheader("**6. Are there noticeable differences in agent performance based on satisfaction ratings?**")
    agent_perf = df.groupby('agent')['satisfaction_rating'].mean().sort_values(ascending=False)

    fig6, ax= plt.subplots(figsize= (10,7))
    agent_perf.plot(kind='barh', ax= ax, color= 'steelblue')
    ax.set_title('Average Satisfaction by Agent')
    ax.set_xlabel('Average Satisfaction Rating')
    ax.set_ylabel('Agent')
    ax.grid(True)
    st.pyplot(fig6)
    st.write("Agent performance appears consistent, with no significant impact on customer satisfaction ratings.")

if show_chart7:
    st.subheader("**7.** How does **resolution status** affect customer satisfaction?")
    resolution_rating= df.groupby('resolved_numeric')['satisfaction_rating'].mean()

    fig7, ax= plt.subplots(figsize= (10,7))
    sns.boxplot(x='resolved_numeric', y='satisfaction_rating', data=df, ax=ax, color='steelblue')
    ax.set_xlabel('Resolved (0 = No, 1 = Yes)')
    ax.set_ylabel('Satisfaction Rating')
    ax.set_title('Satisfaction by Resolution Status')
    ax.grid(True)
    st.pyplot(fig7)
    st.write('Customers whose issues were resolved reported higher satisfaction (median rating ~4), while unresolved cases had lower satisfaction (median ~3.5) and more low outliers. This shows resolution improves customer satisfaction.')

st.title('Executive Summary')
st.write('''
The analysis of Q1 2021 support call data shows that customer satisfaction at Halo is driven more by **call quality** and **resolution efficiency** than by response speed, call topic, or agent identity.

**Key findings:**

1. **Shorter calls (<1 min)** correlate with higher satisfaction.

2. **Answer speed** has minimal impact on satisfaction.

3. **Satisfaction consistently dips around 2 PM each day and remains lower on weekends**, with no correlation to call volume, suggesting other operational or customer experience factors may be affecting performance.

4. **Call topic and agent** differences show no significant influence on ratings.

5. **Resolved issues lead to higher satisfaction,** while unresolved cases often result in lower ratings and more dissatisfaction.

The customer support department should shift its focus towards improving resolution quality and investigating time-based performance patterns to enhance customer satisfaction.
''')


# Display filtered data
with st.expander("📄 View Filtered Data"):
    st.dataframe(filtered_df)
