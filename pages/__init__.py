pip install Flask markdown
python app.py


from flask import Flask, render_template_string
import markdown
import os

app = Flask(__name__)

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return markdown.markdown(content)

@app.route('/')
def home():
    content = read_markdown_file('introduccion.md')
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Simulador de Bolsa de Valores</title>
    </head>
    <body>
        <header>
            <h1>Simulador de Bolsa de Valores</h1>
            <nav>
                <ul>
                    <li><a href="/">Inicio</a></li>
                    <!-- Añadir más enlaces conforme se vayan creando otros módulos -->
                </ul>
            </nav>
        </header>
        <main>
            {{ content | safe }}
        </main>
        <footer>
            <p>&copy; 2024 Simulador de Bolsa de Valores</p>
        </footer>
    </body>
    </html>
    """, content=content)

if __name__ == '__main__':
    app.run(debug=True)

