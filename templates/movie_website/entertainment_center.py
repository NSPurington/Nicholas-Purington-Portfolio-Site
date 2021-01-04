import fresh_tomatoes
import media

back_to_the_future = media.Movie("Back to the Future",
                          "A Teenager Travels Back In Time",
                          "http://www.movieposter.com/posters/archive/main/50/MPW-25074",
                          "https://www.youtube.com/watch?v=qvsgGtivCgs")

the_big_lebowski = media.Movie("The Big Lebowski",
                        "A convergence of events creates a memorable story",
                        "http://www.hometheaterseattle.com/assets/images/movies/the-big-lebowski-movie-1998.jpg",
                        "https://www.youtube.com/watch?v=cd-go0oBF4Y")

pulp_fiction = media.Movie("Pulp Fiction",
                    "A hitman is asked to look after the boss' wife",
                    "https://tribkswb.files.wordpress.com/2014/12/movie-poster-pulp-fiction.jpg",
                    "https://www.youtube.com/watch?v=s7EdQ4FqbhY")

bullitt = media.Movie("Bullitt",
               "A cop investigates a murder and car chases ensue",
               "https://bamfstyle.files.wordpress.com/2016/09/bullitt-poster.jpg",
               "https://www.youtube.com/watch?v=BsvD806qNM8")

the_life_aquatic = media.Movie("The Life Aquatic",
                        "A sea captain and his son are re-united",
                        "https://robpg.files.wordpress.com/2012/05/the-life-aquatic-with-steve-zissou-movie-poster-2004-1020237005.jpg",
                        "https://www.youtube.com/watch?v=yh401Rmkq0o")

machete = media.Movie("Machete",
               "A double-crossed Federale seeks revenge",
               "http://3.bp.blogspot.com/_Fxf2MsuHlys/THcd53fSeZI/AAAAAAAAADc/S9W-R04sgf4/s1600/Machete+Poster+1.jpg",
               "https://www.youtube.com/watch?v=jMn3hiIzkHM")

movies = [back_to_the_future, the_big_lebowski, pulp_fiction, bullitt, the_life_aquatic, machete]
fresh_tomatoes.open_movies_page(movies)


