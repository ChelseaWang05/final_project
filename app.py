import pandas as pd
import streamlit as st

# Data loading function
def load_data():
    # Load data from CSV files
    details = pd.read_csv('details.csv')
    movie_list = pd.read_csv('movie_list.csv')
    movie_rate = pd.read_csv('movie_rate.csv')
    # Merge movie_list with details and movie_rate based on 'index'
    merged_with_details = pd.merge(movie_list, details, on='index', how='left')
    final_merged = pd.merge(merged_with_details, movie_rate, on='index', how='left')
    # Calculate frequency of directors and countries (areas)
    director_counts = final_merged['director'].value_counts().nlargest(20)
    country_counts = final_merged['area'].value_counts().nlargest(20)
    return final_merged, director_counts, country_counts

# Load data once and use it across different pages
final_merged, director_counts, country_counts = load_data()

# Functions for different pages
def show_intro():
    st.write("""
    Chenxi Wang<br>
In this page I will show some information about Chinese netizens' top 250 movies in recent years. From it, we can find out what kind of movies they are most interested in, what movie directors they are interested in, and which region is the most popular. The whole page consists of three parts, Movie Data Explorer, Top 20 Most Frequent Directors and Top 20 Most Frequent Areas.

In the first part, Movie Data Explorer contains detailed information of all Top 250 movies, which are combined into two tables by indexing movie_rate, movie_details and movie_name. You can find specific movie information by movie_name, director. It is also possible to find specific movie information by setting the range of movie_rate.

In the second part, in order to find out the favorite directors of the netizens, the twenty directors with the highest current rating were selected, and the results were plotted as a bar chart for easy visualization. Obviously, Hayao Miyazaki is the most popular director, which shows the popularity of animation.

In the third section, the frequency of occurrence of the region is counted to find out which countries and regions are the most popular among the netizens. In the third section, the frequency of occurrence of regions is used to find out which countries are the most popular among internet users, and Japan and the United States are far ahead of the others, which shows that these two countries have done a better job of promoting their cultures, and that people like movies from these two countries more.
""", unsafe_allow_html=True)

def show_explorer():
    movie_title = st.sidebar.text_input('Movie Name')
    director = st.sidebar.text_input("Director")
    rating_range = st.sidebar.slider(
        "Select a range of ratings",
        float(final_merged['Movie Rate'].min()), float(final_merged['Movie Rate'].max()),
        (float(final_merged['Movie Rate'].min()), float(final_merged['Movie Rate'].max()))
    )
    if st.sidebar.button("Submit"):
        filtered_details = final_merged
        if movie_title:
            filtered_details = filtered_details[filtered_details['Movie Name'].str.contains(movie_title, case=False, na=False)]
        if director:
            filtered_details = filtered_details[filtered_details['director'].str.contains(director, case=False, na=False)]
        filtered_details = filtered_details[(filtered_details['Movie Rate'] >= rating_range[0]) &
                                            (filtered_details['Movie Rate'] <= rating_range[1])]
        st.write("Filtered Movie Details", filtered_details)
    else:
        st.write("Movie Details", final_merged)
    st.header("Top 20 Most Frequent Directors")
    st.bar_chart(director_counts)
    st.header("Top 20 Most Frequent Areas")
    st.bar_chart(country_counts)

def show_conclusions():
    st.write("""
    My goal was to determine which movies are currently the most popular among internet users both domestically and internationally. Specifically, I wanted to identify the regions from which the top 250 rated movies originate, the directors behind them, and their available genres. The data clearly show that the United States and Japan lead substantially in terms of popular movies. This underscores their status as the foremost cultural exporters from the Americas and Asia, respectively. Their films have the broadest impact, indicating highly successful cultural exports.

    A significant portion of Japan’s contribution comes from Mr. Hayao Miyazaki, with eight of his animated films receiving high ratings. This highlights the extensive influence and popularity of Japan’s subculture. American directors like Mr. Nolan, known for his drama-adventure films, and Mr. Spielberg, renowned for his drama-action and romance films, also receive widespread acclaim.""")

def show_research_objectives():
    st.write("""
    To investigate China's most popular movie genres, the themes that appeal to audiences, and the most popular directors and their unique styles, I typically analyze data from movie rating sites, assess social media sentiment, study box office data, and possibly conduct surveys. I also obtain data from IMDb to compare the most popular movies in China and the United States.
    
    In the process of acquiring data, I discovered another interesting issue - cultural diversity. More specifically, what regions the most popular movies in both countries come from. Or how much of the movies are in the original English language. Granted it's normal for most of the most popular movies to be in English as a first world language, but I also wonder if other languages have their influence. """)

# Main app structure
st.title('Movie Data Explorer')
page = st.sidebar.selectbox("Choose a page", ["Introduction", "Data Explorer", "Conclusions", "Research Objectives"])

if page == "Introduction":
    show_intro()
elif page == "Data Explorer":
    show_explorer()
elif page == "Conclusions":
    show_conclusions()
elif page == "Research Objectives":
    show_research_objectives()
