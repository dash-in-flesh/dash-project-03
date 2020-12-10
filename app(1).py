import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from tmdb_apis import *


app = dash.Dash(name=__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


### Configs
g_search = [[], 0]
# g_search_results: g_search[0]
# g_results_count: g_search[1]


### Component
def make_movie_card(item):
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
    )

review_card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Author_1", className="card-title"),
            html.H2("9.7 (Rating)", className="card-rate",
                    style={"color":"grey"}),
            html.P(
                "There only thing mature about this movie is the emotional maturity. Kids can watch this as a great action "
                "movie and young adults and older can watch this movie as a thrilling adventure of emotion and reflection. Would recommend to everyone.",
                className="card-text",
            ),
            html.P("Date", className="card-date",
                    style={"color":"grey"})
        ]

    ),
    style={
            "width": "1000px",
            "margin":"0 auto",
            "margin-top": "60px",
        }

)

### Pages
page1 = html.Div(
    [   
        html.H1("C&Z Movie Hub", style={'margin-bottom':'50px','color':'blck','text-align':'center'}),
        dbc.Input(id="search-input", placeholder="Type something...", type="text", value=""),
        dbc.Button(
            "Search", 
            id='search',
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

page2 =  html.Div(
    [
        html.H2("C&Z Movie Hub", style={'margin-bottom':'40px','color':'black','text-align':'center'}),
        html.H6('', style={'margin-bottom':'20px'}, id="search-count"),    
        html.Div([], id="movie-list"),
        html.Div(
            html.P(
                "Show More Results", 
                id="show-more",  
            ),
            
            style={"width": "200px", "margin":"0 auto", "margin-bottom": "5px"}   
        ),
        html.Div(
            html.P(
                "Back", 
                id="back",  
            ),
            style={"width": "200px", "margin":"0 auto", "margin-bottom": "5px"}  
        )
    ],
    style={'width':'700px', 'margin':'0 auto','margin-top':'3vh', "margin-bottom": "100px", "display": "none"} 
)


page3 = html.Div(
    [
        html.H2("C&Z Movie Hub", style={'margin-bottom': '40px', 'color': 'black', 'text-align': 'center'}),
        html.H3("Movie Title", style={ 'margin-bottom':'40px','margin-left':'40px',"color":"blck"}),
        dbc.Row([
            dbc.Col(html.Img(src= "images/blueprint.jpeg"), md=4),
            dbc.Col(
                html.Div(
                    [html.H4("Movie Summary", style={"color": "blck"}),
                     html.H6(
                         "Interstellar is a 2014 American-British epic science fiction film directed and produced by Christopher Nolan. "
                         "It stars Matthew McConaughey, Anne Hathaway, Jessica Chastain, Bill Irwin, Ellen Burstyn, John Lithgow, Michael Caine, and Matt Damon. "
                         "Set in a dystopian future where humanity is struggling to survive, the film follows a group of astronauts who travel through a wormhole near Saturn in search of a new home for mankind.")
                     ]
                ), md=7),
        ]),
        html.H3("Reviews", style={ 'margin-bottom':'40px','margin-top':'40px','margin-left':'40px',"color":"blck"}),
        review_card
    ]
)



# Default layout display: page1
app.layout = html.Div(
    [
        page1, 
        page2,
        page3
    ],
    id='page'
)    


@app.callback(
    [
        Output('page','children'),
        Output('search-count', 'children')
    ],
    [
        Input('search','n_clicks'),
        Input('back', 'n_clicks')
    ],
    State('search-input', 'value')
)
def update_page(search_clicked, back_clicked, search_query):
    search_query = search_query.strip()
    if search_clicked == None or back_clicked or search_query == "":
        g_search[1] = 0
        g_search[0] = []
        page1.style["display"] = "block"
        page2.style["display"] = "none"
        return [page1, page2], ''

    g_search[0] = get_search_results(search_query)
    
    page1.style["display"] = "none"
    page2.style["display"] = "block"

    search_cout = f"Search {search_query}, {len(g_search[0])} results"

    return [page1, page2], search_cout



@app.callback(
    [
        Output('movie-list', 'children'),
        Output('show-more', 'style'),
    ],
    [
        Input('show-more', 'n_clicks'),
        Input('search-count', 'children')
    ]
)
def show_more(show_more_clicked, search_count):
    style = {}
    # Check if it is the first time visiting the page (before clicking search button, page1)
    if show_more_clicked == None and search_count=="":
        return [], style
    g_search[1] += 10
    
    if len(g_search[0]) <= g_search[1]:
        style["display"] = "none"
    return [make_movie_card(item) for item in g_search[0][:g_search[1]]], style
    







if __name__ == '__main__':
    app.run_server(debug=True)

