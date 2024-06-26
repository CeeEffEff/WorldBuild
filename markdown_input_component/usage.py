import markdown_input_component
from dash import Dash, callback, html, Input, Output

app = Dash(__name__)

app.layout = html.Div([
    markdown_input_component.MarkdownInputComponent(
        id='input',
        value='*Add a description...*',
    ),
    html.Div(id='output')
])


@callback(Output('output', 'children'), Input('input', 'value'))
def display_output(value):
    return 'You have entered {}'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
