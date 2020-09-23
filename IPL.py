import pandas as pd
import altair as alt



import streamlit as st


@st.cache(allow_output_mutation=True)
def get_data(selYear,graph_option):

    #Reading Data
    data = pd.read_csv("./data/matches.csv")

    # Formatting date
    data['clean_date'] = pd.to_datetime(data['date'], dayfirst=False, yearfirst=False)
    data['clean_date'] = pd.to_datetime(data['clean_date'])

    # Filtering data as per user selection
    data = data[data['clean_date'].dt.year == int(Year)]

    if graph_option == 'player_of_match':


        # Calculation
        players = pd.DataFrame(data['player_of_match'].value_counts())
        players_data = players.reset_index()
        players_data.columns = ["Player Name", "No of Man of the Matches"]
        players_data = players_data[players_data["No of Man of the Matches"] >= 2]
        return players_data

    elif graph_option == 'total_wins_by_team':
        # Calculation
        wins = pd.DataFrame(data['winner'].value_counts())
        wins_data = wins.reset_index()
        wins_data.columns = ["winner", "No of Matches"]
        return wins_data

    elif graph_option == 'matches_by_city':
        # Calculation
        city = pd.DataFrame(data['city'].value_counts())
        city_data = city.reset_index()
        city_data.columns = ["City", "No of Matches"]
        return city_data


if __name__ == '__main__':
    # CSS to display content correctly
    st.markdown(
        f"""
            <style>
                .reportview-container .main .block-container{{
                    max-width: 95%;
                }}
            </style>
            """,
        unsafe_allow_html=True,
    )

    st.sidebar.header("Menu")

    # Sidebar drop down
    Year = st.sidebar.selectbox("Year", ('2008', '2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019'))

    # Header
    st.markdown("<h1 style='text-align: center; color: black;'>Analysis :- IPL 2008 - 2019</h1>", unsafe_allow_html=True)

    # Inserting Image
    st.image('./IPLteams.png',caption= 'IPL teams', use_column_width=True, outpuy_format='PNG')


    st.markdown(f"<h3 style=font-weight: bold; color: black;'>Wins by team for year :  {Year} </h3>",
                unsafe_allow_html=True)

    ###### Get data for wins by team
    wins_data = get_data(Year, "total_wins_by_team")


    #bar chart for wins data
    st.write(alt.Chart(wins_data).mark_bar().encode(
        x=alt.X('winner', sort=None),
        y='No of Matches',
        color=alt.Color('winner', legend=None),

    ).properties(
        width=800,
        height=350
    ))

    #Sub header
    st.markdown(f"<h3 style=font-weight: bold; color: black;'>Players with at least 2 Man of the match awards for year : {Year}</h3>" ,
                unsafe_allow_html=True)


    # Get data for Player of the match
    players_data = get_data(Year, "player_of_match")

    #Bar chart to display
    st.write(alt.Chart(players_data).mark_bar().encode(
        x=alt.X('Player Name', sort=None),
        y='No of Man of the Matches',
        color = alt.Color('Player Name',legend=None),

    ).properties(
    width=800,
    height=350
    ))

    st.markdown(f"<h3 style=font-weight: bold; color: black;'>Matches by City :  {Year} </h3>",
                unsafe_allow_html=True)

    # Get data for Player of the match
    city_data = get_data(Year, "matches_by_city")

    # Bar chart to display
    st.write(alt.Chart(city_data).mark_bar().encode(
        x=alt.X('City', sort=None),
        y='No of Matches',
        color=alt.Color('City', legend=None),

    ).properties(
        width=800,
        height=350
    ))