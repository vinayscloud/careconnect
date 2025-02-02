# Description: This is the main file that runs the Flask application. It imports the create_app function from the app package and runs the application. 
# The create_app function initializes the Flask app, sets the configuration, and registers the routes blueprint. 
# The app.run() method starts the Flask development server.

# from app import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template

app = Flask(__name__, template_folder="../frontend/pages", static_folder="../frontend/assets")  # ✅ Load from frontend/

@app.route('/')
def index():
    return render_template("index.html")  # Default page

# ✅ Dynamic Route to Load Any HTML File
@app.route('/pages/<page_name>')
def load_page(page_name):
    try:
        return render_template(f"{page_name}.html")  # Load requested HTML file
    except:
        return "Page not found", 404

if __name__ == '__main__':
    app.run(debug=True)


