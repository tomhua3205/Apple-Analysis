import dash
from dash import dcc, html, callback, Output, Input
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from pymongo import MongoClient

# Replace <password> with your actual MongoDB password
connection_string = "mongodb+srv://tomhua3205:Eg3402945@cluster0.jwjueqf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a MongoClient object
client = MongoClient(connection_string)


# Test the connection
try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    #print("MongoDB connection successful!")
except Exception as e:
    print(f"Error: {e}")

# Connect to the 'Apple' database and the 'AAPL' collection
db = client['Apple']
collection = db['AAPL']

# Retrieve all documents from the collection
data = list(collection.find())

# Convert the data to a pandas DataFrame
df1 = pd.DataFrame(data)

# Ensure 'Date' is in datetime format
df1['Date'] = pd.to_datetime(df1['Date'])

# Sort the DataFrame by 'Date'
df1 = df1.sort_values('Date')

report_dates = [
    '2023-08-03',  # financial report release 23 q3
    '2023-11-02',  # financial report release 23 q4
    '2024-02-03',  # financial report release 24 q1
    '2024-05-03'   # financial report release 24 q2
]
product_dates = [
    '2023-06-13',  # mac studio, mac pro, macbook air
    '2023-09-22',  # apple watch 9 and ultr 2, iphone 15 family, airpods 2, earpods
    '2023-11-07',  # imac 24, macbook pro M3
    '2024-02-02',  # vision pro
    '2024-03-08',  # macbook air m3
    '2024-05-15'   # ipad air M2, ipad pro M4
]
report_dates = pd.to_datetime(report_dates)
product_dates = pd.to_datetime(product_dates)

# Create the main plot
fig = go.Figure()

fig.add_trace(go.Scatter(x=df1['Date'], y=df1['Close'], mode='lines', name='Close Price'))

# Add vertical lines for report dates
for vline_date in report_dates:
    fig.add_vline(x=vline_date, line=dict(color='blue', dash='dash'))
    fig.add_annotation(
        x=vline_date, 
        y=max(df1['Close']), 
        text='Report Date', 
        showarrow=True, 
        arrowhead=1, 
        ax=40,  # Move text to the right
        ay=-40,
        textangle=-90  # Rotate text to vertical
    )
# Add vertical lines for product dates
for vline_date in product_dates:
    fig.add_vline(x=vline_date, line=dict(color='red', dash='dash'))
    fig.add_annotation(
        x=vline_date, 
        y=max(df1['Close']), 
        text='Product Date', 
        showarrow=True, 
        arrowhead=1, 
        ax=-40,  # Move text to the left
        ay=-40,
        textangle=-90  # Rotate text to vertical
    )

# Customize the layout to make the plot bigger
fig.update_layout(
    title='AAPL Close Price Over Time',
    xaxis_title='Date',
    yaxis_title='Close Price',
    xaxis=dict(tickmode='array', tickvals=df1['Date'][::7], tickangle=45),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=20, r=20, t=40, b=20),
    template='plotly_white',
    width=900,  # Adjust the width
    height=600  # Adjust the height
)

# Smart Phone Market Last Year Plot
# Data for 2022 and 2023
data_2022 = {
    "Apple": 18.8,
    "Samsung": 21.7,
    "Xiaomi": 12.7,
    "OPPO": 9.5,
    "Transsion": 6.0
}
data_2023 = {
    "Apple": 20.1,
    "Samsung": 19.4,
    "Xiaomi": 12.5,
    "OPPO": 8.8,
    "Transsion": 8.1
}

# Calculate 'Other' percentages
data_2022['Other'] = 100 - sum(data_2022.values())
data_2023['Other'] = 100 - sum(data_2023.values())

# Labels and sizes
labels_2022 = list(data_2022.keys())
sizes_2022 = list(data_2022.values())

labels_2023 = list(data_2023.keys())
sizes_2023 = list(data_2023.values())

# Colors
colors = ['red', 'blue', 'green', 'orange', 'purple', 'grey']

# Create subplots for pie charts
fig_market = make_subplots(rows=1, cols=2, subplot_titles=("Smartphone Market Share 2022", "Smartphone Market Share 2023"), specs=[[{'type':'domain'}, {'type':'domain'}]])

# Plot 2022 data
fig_market.add_trace(go.Pie(labels=labels_2022, values=sizes_2022, marker=dict(colors=colors), name="2022"), 1, 1)

# Plot 2023 data
fig_market.add_trace(go.Pie(labels=labels_2023, values=sizes_2023, marker=dict(colors=colors), name="2023"), 1, 2)

# Update layout
fig_market.update_layout(
    title_text="Smartphone Market Share Comparison 2022 vs 2023",
    annotations=[dict(text='2022', x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text='2023', x=0.82, y=0.5, font_size=20, showarrow=False)]
)
##-----------------------------------------------------------------------##
#Apple Revenue by Region Plot_Line
db = client['Apple']
collection_Rev = db['Revenue']

# Fetching data from MongoDB
data = list(collection_Rev.find())
df = pd.DataFrame(data)

# Step 2 and 3: Create 4 line charts, each area using a different color, with value on y-axis and time on x-axis
fig_RRLine = go.Figure()

# Plotting each region's revenue
for region in df["Region"]:
    fig_RRLine.add_trace(go.Scatter(x=df.columns[1:], y=df[df["Region"] == region].values[0][1:], mode='lines', name=region))

# Adding labels and title
fig_RRLine.update_layout(
    title='Apple Revenue by Region Over Time',
    xaxis_title='Time',
    yaxis_title='Revenue (in thousands)',
    xaxis=dict(tickmode='array', tickvals=df.columns[1:], tickangle=45),
    legend_title='Region',
    template='plotly_white'
)
##-----------------------------------------------------------------------##
#Apple Revenue by Region_Pi
# Data for each quarter
quarters = ["2023 Q2", "2023 Q3", "2023 Q4", "2024 Q1"]

# Define colors for each region
colors = {
    "North America": "orange",
    "Europe": "red",
    "Japan": "green",
    "Greater China": "pink",
    "Rest of Asia Pacific": "blue"
}

db = client['Apple']
collection_Rev = db['Revenue']

# Fetching data from MongoDB
data = list(collection_Rev.find())
df = pd.DataFrame(data)

# Create subplots for pie charts
fig_RRPi = make_subplots(rows=2, cols=2, subplot_titles=[f'{quarter}' for quarter in quarters],
                    specs=[[{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}]])

# Plot pie charts for each quarter
for i, quarter in enumerate(quarters):
    sizes = df[quarter].values
    labels = df["Region"].values
    color_list = [colors[label] for label in labels]

    # Determine the subplot position
    row = i // 2 + 1
    col = i % 2 + 1

    # Plot pie chart
    fig_RRPi.add_trace(go.Pie(labels=labels, values=sizes, marker=dict(colors=color_list), name=quarter), row, col)

# Update layout
fig_RRPi.update_layout(
    title_text="Apple Revenue Distribution by Region",
    showlegend=True
)


##-----------------------------------------------------------------------##
# Apple Product Revenue_Line
# Read the CSV file
db = client['Apple']
collection_Rev = db['PD_Revenue']

# Fetching data from MongoDB
data = list(collection_Rev.find())
df = pd.DataFrame(data)

# Create the figure
fig_PRLine = go.Figure()

# Plotting each product's revenue share over time
for product in df["Product"]:
    fig_PRLine.add_trace(go.Scatter(x=df.columns[1:], y=df[df["Product"] == product].values[0][1:], mode='lines', name=product))

# Adding labels and title
fig_PRLine.update_layout(
    title='Apple Product Revenue Share Over Time',
    xaxis_title='Time',
    yaxis_title='Revenue Share (%)',
    xaxis=dict(tickmode='array', tickvals=df.columns[1:], tickangle=45),
    legend_title='Product',
    template='plotly_white'
)

##-----------------------------------------------------------------------##
#Apple Product Revenue_Pi
# Define colors for each product
colors = {
    "iPhone": "blue",
    "iPad": "green",
    "Mac": "red",
    "Services": "pink",
    "Wearables, Home and Accessories": "brown"
}

db = client['Apple']
collection_Rev = db['PD_Revenue']

# Fetching data from MongoDB
data = list(collection_Rev.find())
df = pd.DataFrame(data)

# Data for each quarter
quarters = ["2023 Q2", "2023 Q3", "2023 Q4", "2024 Q1"]

# Create subplots for pie charts
fig_PRPi = make_subplots(rows=2, cols=2, subplot_titles=[f'{quarter}' for quarter in quarters],
                    specs=[[{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}]])


# Plot pie charts for each quarter
for i, quarter in enumerate(quarters):
    sizes = df[quarter].values
    labels = df["Product"].values
    color_list = [colors[label] for label in labels]

    # Determine the subplot position
    row = (i // 2) + 1
    col = (i % 2) + 1

    # Plot pie chart
    fig_PRPi.add_trace(go.Pie(labels=labels, values=sizes, marker=dict(colors=color_list), name=quarter), row, col)

# Update layout
fig_PRPi.update_layout(
    title_text="Apple Product Revenue Share by Quarter",
    showlegend=True
)


#_____________________________________________________________________________##
# Create a Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

# Define the layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.H1('Apple Financial Data and News'),
        html.Div([
            dcc.Link('Introduction', href='/'),
            dcc.Link('Stock Last 1 Year', href='/stock-last-year', style={'margin-left': '10px'}),
            dcc.Link('Smart Phone Market Last Year', href='/smart-phone-market', style={'margin-left': '10px'}),
            dcc.Link('Apple Revenue by Region', href='/revenue-by-region', style={'margin-left': '10px'}),
            dcc.Link('Apple Product Revenue', href='/product-revenue', style={'margin-left': '10px'}),
            dcc.Link('Insights and Analysis From ChatGPT', href='/insights', style={'margin-left': '10px'})
        ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '20px'}),
    ], style={'text-align': 'center'}),
    html.Div(id='page-content')
])

# Callbacks to render different pages
@callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return html.Div([
            html.H2('Introduction'),
            html.P('Welcome to this website, designed to analyze Apple\'s financial performance over the past year. We provide insights using data on stock prices, regional revenue, and product revenue share. Our visualizations include stock price trends with key event markers, quarterly regional revenue graphs, and product revenue distributions. These analyses offer a clear understanding of how product launches and financial reports impact Apple\'s market performance, helping investors and enthusiasts make informed decisions.')
        ])
    elif pathname == '/stock-last-year':
        return html.Div([
            html.H2('Stock Last 1 Year'),
            dcc.Graph(
                id='stock-last-year-graph',
                figure=fig
            )
        ])
    elif pathname == '/smart-phone-market':
        return html.Div([
            html.H2('Smart Phone Market Last Year'),
            dcc.Graph(
                id='Smart Phone Market Last Year Plot',
                figure=fig_market
            )
        ])
    elif pathname == '/revenue-by-region':
        return html.Div([
            html.H2('Apple Revenue by Region'),
            dcc.Graph(
                id='Apple Revenue by Region(Line)',
                figure=fig_RRLine
            ),
            dcc.Graph(
                id='Apple Revenue by Region(Pi)',
                figure=fig_RRPi
            )
           
        ])
    elif pathname == '/product-revenue':
        return html.Div([
            html.H2('Apple Product Revenue'),
            dcc.Graph(
                id='Apple Revenue by Product(Line)',
                figure=fig_PRLine
            ),
            dcc.Graph(
                id='Apple Revenue by Product(Pi)',
                figure=fig_PRPi
            )
        ])
    elif pathname == '/insights':
        return html.Div([
            html.H2('Insights and Analysis From ChatGPT'),
    
        html.Ol([
            html.Li('Stock Price Trends:'),
            html.Ul([
                html.Li("The stock price shows significant volatility over the year."),
                html.Li("There's a notable peak around early August 2023, reaching above $195."),
                html.Li("A downward trend is visible from September 2023 to December 2023."),
                html.Li("The stock price dips significantly in January 2024 but starts to recover by March 2024.")
            ]),
            html.Li('Impact of Product Releases:'),
            html.Ul([
                html.Li("Early June 2023: Following a product release, there’s a sharp increase in the stock price, suggesting positive market reception."),
                html.Li("Early September 2023: Another product release coincides with the peak in stock price, indicating that new product launches generally boost investor confidence."),
                html.Li("Early January 2024: A product release during this period seems to have a minimal positive impact, as the price continues to fall.")
            ]),
            html.Li('Impact of Financial Reports:'),
            html.Ul([
                html.Li("Late July 2023: Following a financial report, the stock price continues to rise, indicating strong financial performance."),
                html.Li("Late October 2023: Another financial report coincides with the end of the stock's peak, followed by a decline, possibly due to market corrections or unmet expectations."),
                html.Li("Late January 2024: The stock price remains volatile, with a downward trend indicating possible negative reception of the financial report."),
                html.Li("Late April 2024: The latest financial report seems to have a positive impact, with a noticeable uptick in stock price.")
            ]),
            html.Li('Regional Revenue Trends:'),
            html.Ul([
                html.Li("North America consistently generates the highest revenue, peaking in Q4 2023 and then declining slightly in Q1 2024."),
                html.Li("Europe follows a similar pattern with increasing revenue up to Q4 2023 before a minor drop."),
                html.Li("Greater China shows steady revenue, peaking in Q4 2023 but remains relatively stable compared to other regions."),
                html.Li("Japan and the Rest of Asia Pacific contribute the least to total revenue, with minimal fluctuations over the quarters.")
            ]),
            html.Li('Revenue Distribution by Region:'),
            html.Ul([
                html.Li("North America contributes the largest share of Apple's total revenue, ranging from about 42% to nearly 45%."),
                html.Li("Europe is the second-largest revenue contributor, holding a consistent share of around 25%."),
                html.Li("Greater China's share fluctuates between 17% and 19%, showing a steady but significant contribution."),
                html.Li("Japan and the Rest of Asia Pacific have smaller shares, typically below 10%, indicating lower but stable market performance.")
            ]),
            html.Li('Product Revenue Share:'),
            html.Ul([
                html.Li("iPhone remains the dominant product, consistently contributing around 50% of total revenue, peaking at 58.3% in Q4 2023."),
                html.Li("Services are the second-largest revenue source, with a steady share around 25%, indicating a significant and growing part of Apple's business model."),
                html.Li("Wearables, Home, and Accessories show a consistent contribution around 10%, indicating a stable but secondary revenue source."),
                html.Li("Mac and iPad have the smallest shares, around 6-9%, with little variation, highlighting their role as supplementary products rather than core revenue drivers.")
            ])
        ]),
        html.H3('Conclusions from ChatGPT'),
        html.Ol([
            html.Li('Market Sensitivity to Events:'),
            html.Ul([
                html.Li("Apple’s stock price is highly sensitive to both product releases and financial reports."),
                html.Li("Positive receptions to new products and strong financial results generally lead to stock price increases.")
            ]),
            html.Li('Investor Sentiment:'),
            html.Ul([
                html.Li("Product launches are critical for maintaining investor confidence, often leading to price surges."),
                html.Li("Financial reports have mixed impacts; while they can boost prices when results exceed expectations, they can also lead to corrections or declines if results are disappointing or if market expectations are not met.")
            ]),
            html.Li('Volatility:'),
            html.Ul([
                html.Li("The plot indicates high volatility in Apple's stock price, influenced by external events and internal company milestones."),
                html.Li("Investors should be prepared for significant fluctuations around these key dates.")
            ]),
            html.Li('Seasonal and Event-Based Impact:'),
            html.Ul([
                html.Li("There are notable revenue peaks in Q4 2023, likely due to seasonal factors such as holiday sales and new product launches, followed by a typical decline in Q1 2024."),
                html.Li("The pattern suggests that Apple's revenue is highly influenced by product release cycles and seasonal buying trends, which are crucial for planning and forecasting.")
            ]),
            html.Li('Strategic Insights:'),
            html.Ul([
                html.Li("Maintaining innovation in the iPhone segment is crucial for sustaining high revenue levels."),
                html.Li("Continued growth in Services is essential for diversification and stability."),
                html.Li("Expanding market share in regions outside North America and Europe could help mitigate risks associated with over-reliance on these markets.")
            ])
        ])
        ])
    else:
        return html.Div([
            html.H2('404'),
            html.P('Page not found')
        ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
