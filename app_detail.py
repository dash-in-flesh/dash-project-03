import dash
import dash_bootstrap_components as dbc
import dash_html_components as html




app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("The best movie I've ever seen", className="card-title"),
            html.H2("9.7", className="card-rate",
                    style={"color":"grey"}),
            html.P(
                "There only thing mature about this movie is the emotional maturity. Kids can watch this as a great action "
                "movie and young adults and older can watch this movie as a thrilling adventure of emotion and reflection. Would recommend to everyone.",
                className="card-text",
            ),
            dbc.CardLink("Card link", href="#"),
            dbc.CardLink("External link", href="https://google.com"),
        ]
    )
)



app.layout=html.Div(
    [
        html.H1("MONAME", style={'margin-bottom':'20px', "color":"blck"}),
        html.H3("Details", style={ "color":"grey"}),
        dbc.Row([
            dbc.Col(html.Img(src= "images/blueprint.jpeg"), md=4),
            dbc.Col(
                html.Div(
                    [html.H4("Movie Summary", style={"color": "grey"}),
                     html.H6(
                         "Interstellar is a 2014 American-British epic science fiction film directed and produced by Christopher Nolan. "
                         "It stars Matthew McConaughey, Anne Hathaway, Jessica Chastain, Bill Irwin, Ellen Burstyn, John Lithgow, Michael Caine, and Matt Damon. "
                         "Set in a dystopian future where humanity is struggling to survive, the film follows a group of astronauts who travel through a wormhole near Saturn in search of a new home for mankind.")
                     ]
                ), md=8),
        ]),
        html.H3("Reviews", style={ "color":"grey"}),
        card
    ])

if __name__ == '__main__':
    app.run_server(debug=True)