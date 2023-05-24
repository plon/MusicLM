from MusicLM import Music

# Create a new instance of Music
music = Music()

input = "Ambient, soft sounding music I can study to"
tracks = music.get_tracks(input, 2)
if tracks != "Oops, can't generate audio for that.":
    music.base64toMP3(tracks, input)