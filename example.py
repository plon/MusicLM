from MusicLM import Music

# Create a new instance of Music
music = Music()

input = "Ambient, soft sounding music I can study to"
tracks = music.get_tracks(input, 2)
music.base64toMP3(tracks, input)