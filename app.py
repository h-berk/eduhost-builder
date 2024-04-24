from flask import Flask, request, render_template, make_response
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/submit', methods=['POST'])
def submit():
    if not request.is_json:
        return make_response({"error": "Request must be JSON"}, 400)

    data = request.get_json()

    # Get the template identifier from the data
    template_name = data.get('template', 'default')  # default is a fallback template name

    # Define the name for the temporary HTML file
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f'{template_name}_{timestamp}.html'
    file_path = os.path.join('tmp', filename)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Template file selection based on the template identifier
    template_file = f'{template_name}.html'
    if not os.path.exists(f'templates/{template_file}'):
        return make_response({"error": f"Template '{template_name}' not found"}, 404)

    # Render the chosen template with the data
    rendered_html = render_template(template_file, **data)

    with open(file_path, 'w') as f:
        f.write(rendered_html)

    response = make_response(rendered_html)
    response.headers['Content-Type'] = 'text/html'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'

    @response.call_on_close
    def remove_file():
        os.remove(file_path)

    return response

if __name__ == '__main__':
    app.run(debug=False)
