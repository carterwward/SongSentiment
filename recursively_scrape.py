from join_data import join_spotify_genius

# TODO: implement getting the full disocgraphy for all features artist in a given artists full disography
# I realized for this to work we also have to be calling the spotify API, so maybe we should put this function in a different file
def get_featured_artist_discography(artist):
    # set is underordered and has unique elements
    artist_set = set()
    print("...")
    primary_artist_discography = join_spotify_genius(artist)

    for id, items in primary_artist_discography.items():
        for key in items:
            print(items[key])
    
    # return artist_set
    

get_featured_artist_discography("JPEGMAFIA")