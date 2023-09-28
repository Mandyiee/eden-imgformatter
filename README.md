# Eden

This web application allows you to style and format code snippets using various programming languages and styles. It is built using Flask, Pygments, and other web technologies.

## Table of Contents
- Getting Started
- Usage
- Routes and Functionality
- Dependencies
- Contributing
- License

## Getting Started
To run this web application locally, follow these steps:

**Clone this repository to your local machine:**
```
git clone https://github.com/Mandyiee/eden-imgformatter.git
```

- **Create a virtual environment and activate:**
```
python -m venv && source venv/bin/activate
```

- **Install the required dependencies:**
```
pip install -r requirements.txt
```

- **Set up the database by running the following commands:**
```
flask db init
flask db migrate
flask db upgrade
```

- **Start the Flask development server:**
```
flask run
```
Access the application in your web browser at http://localhost:5000.

### Usage
Visit the homepage to create or edit code snippets.
Customize the code, style, and language.
View the styled code and download images of the code snippet.
Change code styles, languages, and fonts on the style page.
Reset the session to start fresh.

## Dependencies
This application relies on several Python packages and technologies, including:
Flask: A micro web framework for Python.
Pygments: A syntax highlighting library.
SQLAlchemy: An Object-Relational Mapping (ORM) library.
Pillow: A Python Imaging Library.
Other dependencies listed in requirements.txt.

## Contributing
Contributions to this project are welcome! If you find a bug or want to enhance the functionality, please open an issue or submit a pull request following our contribution guidelines.

## License
This project is licensed under the MIT License - see the LICENSE file for details.


