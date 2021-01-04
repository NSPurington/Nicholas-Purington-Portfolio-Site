import webbrowser

class Movie(object):
    def __init__ (self, movie_title, movie_storyline, poster_image, trailer_youtube):
        """
        Initializes the movie instance.
        Arguments:
        movie_title: title of movie
        movie_storyline: storyline of movie
        poster_image: movie poster image
        trailer_youtube_url: youtube movie trailer
        ...
        Returns:
        None
        """
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube

    def show_trailer(self):
        """
        Opens the web browser to start playing the youtube movie trailer
        Arguments: None
        ...
        Returns: None
        """
        webbrowser.open(self.trailer_youtube_url)
