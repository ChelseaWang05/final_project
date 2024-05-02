import pandas as pd
import streamlit as st

def load_data():
    # Load data
    details = pd.read_csv('details.csv')
    movie_list = pd.read_csv('movie_list.csv')
    movie_rate = pd.read_csv('movie_rate.csv')

    # Merge movie_list with details first
    merged_with_details = pd.merge(movie_list, details, on='index', how='left')

    # Then merge the result with movie_rate
    final_merged = pd.merge(merged_with_details, movie_rate, on='index', how='left')

    # Calculate frequency of directors and countries (areas)
    director_counts = final_merged['director'].value_counts().nlargest(20)
    country_counts = final_merged['area'].value_counts().nlargest(20)

    return final_merged, director_counts, country_counts

# Load merged data and frequency data
final_merged, director_counts, country_counts = load_data()

# Webpage title
st.title('Movie Data Explorer')

# Introduction and other paragraphs
st.write("""
Chenxi Wang<br>
In this page I will show some information about Chinese netizens' top 250 movies in recent years. From it, we can find out what kind of movies they are most interested in, what movie directors they are interested in, and which region is the most popular. The whole page consists of three parts, Movie Data Explorer, Top 20 Most Frequent Directors and Top 20 Most Frequent Areas.

In the first part, Movie Data Explorer contains detailed information of all Top 250 movies, which are combined into two tables by indexing movie_rate, movie_details and movie_name. You can find specific movie information by movie_name, director. It is also possible to find specific movie information by setting the range of movie_rate.

In the second part, in order to find out the favorite directors of the netizens, the twenty directors with the highest current rating were selected, and the results were plotted as a bar chart for easy visualization. Obviously, Hayao Miyazaki is the most popular director, which shows the popularity of animation.

In the third section, the frequency of occurrence of the region is counted to find out which countries and regions are the most popular among the netizens. In the third section, the frequency of occurrence of regions is used to find out which countries are the most popular among internet users, and Japan and the United States are far ahead of the others, which shows that these two countries have done a better job of promoting their cultures, and that people like movies from these two countries more.
""", unsafe_allow_html=True)

# Sidebar filters
movie_title = st.sidebar.text_input('Movie Name')
director = st.sidebar.text_input("Director")
rating_range = st.sidebar.slider(
    "Select a range of ratings",
    float(final_merged['Movie Rate'].min()), float(final_merged['Movie Rate'].max()), 
    (float(final_merged['Movie Rate'].min()), float(final_merged['Movie Rate'].max()))
)

# Sidebar submit button
if st.sidebar.button("Submit"):
    filtered_details = final_merged

    # # Filter by movie name
    if movie_title:
        filtered_details = filtered_details[filtered_details['Movie Name'].str.contains(movie_title, case=False, na=False)]

    # Filter by director
    if director:
        filtered_details = filtered_details[filtered_details['director'].str.contains(director, case=False, na=False)]

    # Filter by rating range
    filtered_details = filtered_details[(filtered_details['Movie Rate'] >= rating_range[0]) &
                                        (filtered_details['Movie Rate'] <= rating_range[1])]

    # Display filtered details and ratings
    st.write("Filtered Movie Details", filtered_details)
else:
    # If no filters are selected, display the original data
    st.write("Movie Details", final_merged)

# Display top 20 most frequent directors and areas using bar charts
st.header("Top 20 Most Frequent Directors")
st.bar_chart(director_counts)

st.header("Top 20 Most Frequent Areas")
st.bar_chart(country_counts)
