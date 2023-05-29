from MusicLM import Music

# Create a new instance of Music
music = Music()

input = "Taylor Swift"
tracks = music.get_tracks(input, 2)
if not (tracks == "Oops, can't generate audio for that." or tracks == "Can't connect to the server."):
    music.base64toMP3(tracks, input)