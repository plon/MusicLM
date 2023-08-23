from MusicLM import Music

# Create a new instance of Music
music = Music()

input = "Ambient, soft sounding music I can study to"
tracks = music.get_tracks(input, 2)

if isinstance(tracks, list):
    music.b64toMP3(tracks, input)
