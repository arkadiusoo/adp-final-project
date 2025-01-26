html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Mapy Miast</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
        }}
        .city-map {{
            margin-bottom: 40px;
        }}
        h2 {{
            margin-bottom: 10px;
        }}
        iframe {{
            width: 100%;
            height: 500px;
            border: none;
        }}
    </style>
</head>
<body>
    <h1>Mapy Miast</h1>
    {map_sections}
</body>
</html>
"""