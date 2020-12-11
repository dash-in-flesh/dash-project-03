import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL, MATCH
from tmdb_apis import *


app = dash.Dash(
    name=__name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

### In Memory Cache
cache = {
    "search_query": "",
    "search_results": [],
    "display_count": 0, 
    "movie_id": None,
}


### Component
def make_movie_card(i):
    item = cache["search_results"][i]
    img_src = "https://via.placeholder.com/100x150.png?text=No+Poster"
    if item["poster_path"] != None:
        img_src = f'https://image.tmdb.org/t/p/w200/{item["poster_path"]}'

    return html.Div(
        [
            # Left Side： Picture
            html.Img(
                src=img_src,
                style={'width':'100px','height':'150px'}
            ),
            # Right side: Movie Overview
            html.Div(
                [
                    html.P(item["original_title"], 
                        style={
                            "margin-bottom": "4px", 
                            "font-size":"24px", 
                            "width":"100%", 
                            'height':'36px', 
                            "overflow":"hidden", 
                            "text-overflow": "ellipsis", 
                        }
                    ),
                    html.P(f'Vote Average: {item["vote_average"]} ({item["vote_count"]} votes)', style={"margin-bottom": "4px", "font-size":"14px", "width":"100%", 'height':'20px'}),
                    html.P(f'Release Date: {item.get("release_date", "Unknown")}', style={"margin-bottom": "4px", "font-size":"14px", "width":"100%", 'height':'20px'}),
                    html.P(f'Overview: {item["overview"]}', 
                        style={
                            "margin-bottom": "0", 
                            "font-size":"14px", 
                            "overflow":"hidden", 
                            "white-space":"prewrap", 
                            "text-overflow": "ellipsis", 
                            "width":"100%", 
                            'height':'60px',
                            "display": "-webkit-box",
                            "-webkit-line-clamp": "3",
                            "-webkit-box-orient": "vertical",
                        }
                    ),
                ] , 
                style={'margin-left':'20px',"flex-grow":"1"}
            )
        ],
        className="movie-card",
        id={"index": i, "type": "movie-card"}
    )


def make_movie_list():
    sz = min(cache['display_count'], len(cache['search_results']))
    return [make_movie_card(i) for i in range(sz)]

### Pages
def make_home_page():
    return html.Div(
        [   
            html.H1("C&Z Movie Hub", style={'margin-bottom':'50px','color':'blck','text-align':'center'}),
            dbc.Input(id="search-input", placeholder="Type something...", type="text", value=""),
            dbc.Button(
                "Search", 
                id="search-btn",
                href="movie-list",
                style={
                    'width':'250px',
                    'margin':'0 auto',
                    'margin-top':'30px', 
                    'color': '#ffffff',
                    'background-color': '#decbd7',
                    'border':'0',
                    'display': 'block'
                }
            ),
        ],
        style={'width':'800px', 'margin':'0 auto','margin-top':'20vh'} 
    )

def make_list_page():
    search_info = f"Search {cache['search_query']}, {len(cache['search_results'])} results"
    movie_list = make_movie_list()
    style = {}
    if cache['display_count'] >= len(cache['search_results']):
        style["display"] = "none"
    return html.Div(
        [
            html.H2("C&Z Movie Hub", style={'margin-bottom':'40px','color':'black','text-align':'center'}),
            html.H6(search_info, style={'margin-bottom':'20px'}),    
            html.Div(movie_list, id="movie-list"),
            dbc.Button(
                "Show More Results", 
                id="show-more-btn",
                className="magic-button",
                style=style
            ),
            dbc.Button(
                "Back", 
                id="back-home-btn",
                href="/",
                className="magic-button"
            )
        ],
        style={'width':'700px', 'margin':'0 auto','margin-top':'3vh', "margin-bottom": "100px"} 
    )

def make_404_page():
    return html.Div([
        html.H3("404 Not Found.", style={"text-align": "center"}),
        html.P("Please try again.", style={"text-align": "center"})
    ], style={"width": "100%", "margin-top": "200px" })

def make_movie_detail():
    movie_detail = get_movie_detail(cache['movie_id'])
    img = movie_detail['backdrop_path']
    if img == None:
        img = movie_detail['poster_path']
    genres = ' / '.join([cat['name'] for cat in movie_detail["genres"]])
    return html.Div([
        html.H2("C&Z Movie Hub", style={'margin-bottom': '40px', 'color': 'black', 'text-align': 'center'}),
        html.Div(
            [
                html.H4(movie_detail["original_title"], style={"margin-bottom": "20px"}),
                html.Div(
                    [   
                        html.Div(
                            [
                                html.Img(src=f"https://image.tmdb.org/t/p/w500/{img}", style={'width':'450px','height':'auto'})
                            ],
                            style={"width": "480px"}
                        ),
                        html.Div(
                            [
                                html.P([html.Span("Genres"), f': {genres}'], className="detail-meta"),
                                html.P([html.Span("Homepage"), f': {movie_detail["homepage"]}'], className="detail-meta"),
                                html.P([html.Span("Popularity"), f': {movie_detail["popularity"]}'], className="detail-meta"),
                                html.P([html.Span("Release Date"), f': {movie_detail["release_date"]}'], className="detail-meta"),
                                html.P([html.Span("Revenue"), f': {movie_detail["revenue"]}'], className="detail-meta"),
                                html.P([html.Span("Status"), f': {movie_detail["status"]}'], className="detail-meta"),
                                html.P([html.Span("Vote Average"), f': {movie_detail["vote_average"]}'], className="detail-meta"),
                                html.P([html.Span("Vote Count"), f': {movie_detail["vote_count"]}'], className="detail-meta"),
                            ],
                            style={"flex-grow":"1", "overflow": "hidden"})
                    ],
                    style={
                        "display": "flex",
                        "width": "100%",
                    }
                ),
            ],
            style={
                "padding": "20px",
                "border": "1px solid rgba(0,0,0,.125)",
                "border-radius": ".25rem",
                "margin-bottom": "20px",
            }
        ),
        html.Div(
            [
                html.H4("Movie Summary", style={"margin-bottom": "20px"}),
                html.P(movie_detail["overview"], 
                    style={
                        "margin-bottom": "0", 
                        "font-size":"14px", 
                        "overflow":"hidden", 
                        "white-space":"prewrap", 
                        "text-overflow": "ellipsis", 
                    }
                ),
            ],
            style={
                "width": "100%",
                "padding": "20px",
                "border": "1px solid rgba(0,0,0,.125)",
                "border-radius": ".25rem",
                "margin-bottom": "20px",
            }
        ),
        make_review_list()  
    ], style={'width':'900px', 'margin':'0 auto','margin-top':'3vh', "margin-bottom": "100px", } )



def make_review(review):
    return html.Div(
        [
            html.P(review['author'], style={"font-weight": "bold"}),
            html.P(str(review['author_details']['rating']), style={"font-size": "30px", "color":"lightgrey"}),
            html.P(review['content'], style={
                "font-size":"14px", 
                "overflow":"hidden", 
                "white-space":"prewrap", 
                "text-overflow": "ellipsis",
                "text-align": "justify",
                "margin": "5px auto"
            }),
            html.P(review['created_at'][:10], style={"color":"lightgrey"})
        ],
        className="review"
    )


def make_review_list():
    reviews = get_movie_reviews(cache['movie_id'])
    children = [html.H4("Reviews", style={"margin-bottom": "20px"})]
    for review in reviews:
        children.append(make_review(review))
    return html.Div(
        children,
        style={
            "width": "100%",
            "padding": "20px",
            "border": "1px solid rgba(0,0,0,.125)",
            "border-radius": ".25rem",
            "margin-bottom": "20px",
        }
    )




### Page Frame
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(make_home_page(), id='page-content')
])





@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
    prevent_initial_call=True
)
def display_page(pathname):
    #print(pathname)
    if pathname == "/movie-list":
        if cache["search_query"] == "":
            return make_404_page()
        if cache["display_count"] == 0:
            cache["search_results"] = get_search_results(cache["search_query"])
            cache["display_count"] = 10
        return make_list_page()
    elif pathname == "/movie-detail":
        if cache['movie_id'] == None:
            return make_404_page()
        return make_movie_detail()

    cache['search_query'] = ""
    cache['search_results'] = []
    cache['display_count'] = 0
    cache['movie_id'] = None
    return make_home_page()



@app.callback(
    Output('search-input', 'value'),
    Input('search-btn', 'n_clicks'),
    State('search-input', 'value'),
    prevent_initial_call=True
)
def search(n_clicks, query):
    query = query.strip()
    cache["search_query"] = query
    return query



@app.callback(
    [
        Output('movie-list', 'children'),
        Output('show-more-btn', 'style'),
    ],
    Input('show-more-btn', 'n_clicks'),
    prevent_initial_call=True
)
def show_more(n_clicks):
    style = {}
    cache["display_count"] += 10
    if cache["display_count"] >= len(cache['search_results']):
        style["display"] = "none"
    return make_movie_list(), style


@app.callback(
    Output('url', 'pathname'),
    Input({"type": "movie-card", "index": ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def show_detail(cards_clicks):
    idx = -1
    for i in range(len(cards_clicks)):
        if cards_clicks[i] == 1:
            idx = i
            break
    if idx == -1:
        return "/movie-list"
    cache["movie_id"] = cache["search_results"][idx]["id"]
    return "/movie-detail"












if __name__ == '__main__':
    app.run_server(debug=True)

