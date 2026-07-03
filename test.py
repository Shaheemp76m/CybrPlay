import library

songs, genres = library.scan_music()
no = 0
for genre, songs in genres.items():
    print(no, genre)
    no += 1
    #for song in songs:
    #    print("     ", song)
