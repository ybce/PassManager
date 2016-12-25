import facebook

token = 'EAACEdEose0cBAPSSrporWbP8YtTDZCtGZAP5NgseqMEBlSrYVOfjRVzDRsFw77IOF5rEXkXgqg4IQ2ZA8m4wnEjoKh0nnsdJGcTF1lJ1VVYDxapiuiuiuBvaKZCDsxAii7PiNDdnuBN520d1O2Oz7wwrtr7ARYMBzMBLw8d6QAZDZD'

graph = facebook.GraphAPI(token)
friends = graph.get_object("me/friends")
#friends = graph.get_connections("me", "friends")

print friends['data']
