from agents import function_tool

@function_tool
def create_song(lyric: str, genre: str):
    """
    Create a song based on a lyrics and genre

    Args: 
        - lyric: The lyric to create a song with
        - Genre: The genre to create the song with 
    """
    print(lyric, genre)