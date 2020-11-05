from join_data import join_spotify_genius

# Function will recursively scrape discogs by features and stop when it has 100 discogs
# The parameters are a set of the artists we have already scrapped
    # A dictionary to contain all the artists data (the dict passed in initially will be empty)
    # and the artist name we are looking at features/discog of
def get_featured_artist_discography(discog_set, artist_dict, artist):

    # check if the length of the keys of artist dict is already 100 or greater
        # if yes, just return the artist dict passed in

    # Get primary artist discog
    primary_artist_discography = join_spotify_genius(artist)

    # add primary artist discography to artist_dict

    # iterate over dictionary in discography dict
    for id, items in primary_artist_discography.items():

        # iterate over featured artists in each featured list
        for artist in items['features']:
            # if artist not in discog set and artist not in keys of artist dict
                # call get_featured_artist_discography and read into sub_artist dict
                # add only new keys to artist dict
       
                   
    return artist_dict
    

# get_featured_artist_discography("redveil")