from join_data import join_spotify_genius

# TODO: implement getting the full disocgraphy for all features artist in a given artists full disography
# I realized for this to work we also have to be calling the spotify API, so maybe we should put this function in a different file
def get_featured_artist_discography(artist_set, artist):
    # set is underordered and has unique elements
    artist_set = set()
    counter = 0
    print("...")
    primary_artist_discography = join_spotify_genius(artist)
    for id, items in primary_artist_discography.items():
        for artist in items['features']:
            artist_set.add(artist)
            counter = len(artist_set)
       
                   

    

get_featured_artist_discography("redveil")