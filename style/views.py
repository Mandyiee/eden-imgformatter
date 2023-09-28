from . import style
from flask import Flask, render_template,session, request, redirect, url_for,jsonify,abort
from style.forms import CodeForm, StyleForm
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer, guess_lexer, get_lexer_by_name, TextLexer
from pygments.styles import get_all_styles
from utils import take_image
from pygments import lexers
from pygments.lexers import guess_lexer_for_filename, get_lexer_by_name
from .models import Image
from app import db
import base64, uuid

PLACEHOLDER_CODE = "print('HELLO WORLD')"
DEFAULT_STYLE = "monokai"

from app import app


@style.route('/', methods=["GET"])
def home():
    id = uuid.uuid4()
    return redirect(url_for("style.index", id=id))

@style.route('/<id>', methods=["GET","POST"])
def index(id):
   
    print(id)    
    form = CodeForm()
    if request.method == 'GET':
        try:
            image = Image.query.get(id)
            if image:
                form.code.data = image.code
            else:
                form.code.data = "print('HELLO WORLD')"
        except Exception as e:
            print(e)
            form.code.data = "print('HELLO WORLD')"
            
    if form.validate_on_submit():
        image = Image.query.get(id)
        if image:
            # print(form.code.data)
            image.code = form.code.data
            # print(image.code)
            db.session.commit()
        else:
            new_image = Image(id=id,code=form.code.data)
            db.session.add(new_image)
            db.session.commit()
        return redirect(url_for('style.show_style', id=id))
  
    context = {
        
        "form": form, 
        
    }
    return render_template("index.html", **context)



@style.route("/reset_session", methods=["POST"])
def reset_session():
    id = uuid.uuid4()
    return redirect(url_for("style.index", id=id))


@style.route("/style/<id>", methods=["GET"])
def show_style(id):
    try:
        image = Image.query.get(id)
        if not image:
            return redirect(url_for("style.home"))
    except Exception as e:
        print(e)
        return redirect(url_for("style.home"))
    context = {
        "image": image,
        "current_style":image.style,
        "current_lang":session.get('lexer','Text'),
        "all_styles": list(get_all_styles()),
        "all_lexers": list(lexers.get_all_lexers()),
        "font":image.font
    }
    
    return render_template("show_style.html", **context)


@style.route("/save_style/<id>", methods=["POST"])
def save_style(id):
    try:
        data = request.get_json()
        style = data.get('style', DEFAULT_STYLE)
        
        if style is not None:
            image = Image.query.get(id)
            image.style = style
            db.session.commit()
        
        response_data = {'status': 'done'}
        
        return jsonify(response_data)
    except Exception as e:
        print(e)
        return redirect(url_for("style.show_style",id=id))
   

@style.route("/save_lexer/<id>", methods=["POST"])
def save_lexer(id):
    data = request.get_json()
    lexer = data.get('lexer', None)
    if lexer is not None:
        lexer_specification = lexer.split(",,")
        try:
            lexer = lexer_specification[0]
        except Exception as e:
            lexer = 'Text'
            print(e)
        image = Image.query.get(id)
        image.lexer = lexer
        image.current_lang=lexer
        db.session.commit()
        
    response_data = {'status': 'done'}
    
    return jsonify(response_data)

@style.route("/save_font/<id>", methods=["POST"])
def save_font(id):
    data = request.get_json()
    font = data.get('font', None)
    print(font)
    if font is not None:
        image = Image.query.get(id)
        image.font = font
        db.session.commit()
        
        
    response_data = {'status': 'done'}
    
    return jsonify(response_data)

@style.route("/image/<id>", methods=["GET"])
def image(id):
    try:
        image = Image.query.get(id)
    except Exception as e:
        print(e)
        return redirect(url_for('style.home'))
    
    try:
        
        image = take_image(id=id)
        if not image:
            abort(500)
    except Exception as e:
        print(e)
    context = {
        'image':image
        
    }
    return render_template("image.html", **context)

from flask import send_file

@app.route('/display_image/<id>')
def display_image(id):
    try:
        image = Image.query.get(id)
        if image:
            return send_file(image.image_file, mimetype='image/png')
        else:
            abort(404)
    except Exception as e:
        # Handle exceptions as needed
        abort(500)

@style.route("/text/<id>", methods=["GET"])
def text(id):
    try:
        image = Image.query.get(id)
    except Exception as e:
        print(e)
        return redirect(url_for('style.home'))    
    context = {
        'image':image,
        
    }
    return render_template("text.html", **context)