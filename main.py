import streamlit as st
import pandas as pd
import numpy as np
import re
import random
from fuzzywuzzy import process

from streamlit import components

header= st.container()
app= st.container()

with header:
    st.title(" :books: Find Your Next Book Crush!")
    col1,col2=st.columns([1,1])
    col1.markdown("I'll help you find the next book you should read.")

    camera_photo= col1.camera_input("First take a photo!")
    if camera_photo is not None:
        st.write("How can your face be related to what you read darling? You are smarter than this!")


with app:


    final_df = pd.read_csv('/Users/hamidehaghaei/Desktop/Ironhack/Book_recommender_pycharm/data/nineteen_cluster_df.csv')


    def book_recommender(final_df):
        user_book = st.text_input("Choose a book you like, and I'll provide you with a tailored recommendation.")

        if 'recommend_button_clicked' not in st.session_state:
            st.session_state.recommend_button_clicked = False

        if st.button('Recommend'):
            st.session_state.recommend_button_clicked = True

        if st.session_state.recommend_button_clicked:
            matching_books = final_df[final_df['original_title'].str.contains(user_book, case=False)]

            if not matching_books.empty:
                user_book_cluster = matching_books['cluster'].values[0]
                same_cluster_books = final_df[final_df['cluster'] == user_book_cluster]
                recommendation = random.choice(same_cluster_books['original_title'].tolist())
                recommendation_image_url = \
                    same_cluster_books[same_cluster_books['original_title'] == recommendation][
                        'small_image_url'].values[0]
                recommendation_author = \
                    same_cluster_books[same_cluster_books['original_title'] == recommendation]['authors'].values[0]
                st.write("You might also like: ", recommendation)
                st.write("Author: ", recommendation_author)
                st.image(recommendation_image_url)

            else:
                st.info("The book you chose is not in the database. No books found with that title.")
                st.session_state.genre_button_clicked = False

                # Combine all genre strings in the DataFrame
                all_genre_str = ','.join(final_df['genres'])

                # Use regular expressions to clean the string and split it into a list of genres
                all_genres = re.split(",\s*", all_genre_str.replace("'", "").replace("[", "").replace("]", ""))

                # Get the unique genres
                genre_options = list(set(all_genres))

                genre = None
                if 'genre_button_clicked' not in st.session_state:
                    st.session_state.genre_button_clicked = False

                genre = st.selectbox("Enter your favourite genre:", genre_options)
                if st.button('Give me a genre-based recommendation'):
                    st.session_state.genre_button_clicked = True

                if st.session_state.genre_button_clicked:
                    # Find the best match for the user's genre
                    best_match, score = process.extractOne(genre, genre_options)

                    if score >= 80:
                        same_genre_books = final_df[final_df['genres'].apply(lambda genres: best_match in genres) & (
                                final_df['average_rating'] > 4.00)]
                        if len(same_genre_books) > 0:
                            recommendation = random.choice(same_genre_books['original_title'].tolist())
                            recommendation_image_url_genre = \
                                same_genre_books[same_genre_books['original_title'] == recommendation][
                                    'small_image_url'].values[0]
                            recommendation_author_genre = \
                                same_genre_books[same_genre_books['original_title'] == recommendation]['authors'].values[
                                    0]
                            st.write("You might also like: ", recommendation)
                            st.write("Author: ", recommendation_author_genre)
                            st.image(recommendation_image_url_genre)
                    else:
                        st.write("No high-rated books found for your favorite genre or author.")


    book_recommender(final_df)

    #..............

    st.sidebar.header(" We value your opinion")

    NPS = st.sidebar.slider("How likely is it that you would recommend our app to a friend or family member?", min_value=0, max_value=10, value=10, step=1)
    NPS_q = st.sidebar.selectbox("Is this app beneficial for you?",
                                 options=['Yes', 'No'], index=0)
