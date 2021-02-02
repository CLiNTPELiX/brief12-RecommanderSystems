from wtforms import form, stringfield, selectfield

class artistsearchform(form):
    select = selectfield('Search for artist:')
    search = stringfield('')