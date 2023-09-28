from playwright.sync_api import sync_playwright
import os 
from style.models import Image as Picture
from app import db
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import PythonLexer
from PIL import Image
from app import basedir
from pygments.lexers import get_lexer_by_name, TextLexer

def take_image(id):
    # Define the screenshot path and filename
    screenshot_filename = f"screenshot_{id}.png"
    screenshot_directory = os.path.join(basedir,'static', "screenshots")
    screenshot_path = os.path.join(screenshot_directory, screenshot_filename)
    image = Picture.query.get(id)
    try:
        try:
            lexer = get_lexer_by_name(image.current_lang)
            print(lexer)
        except Exception as e:
            lexer = TextLexer()
       
        # Create an ImageFormatter with the desired options
        
        font = image.font.split(',')[0].replace("'","").replace(' ','') + '.ttf'
       
        
        path_to_font = os.path.join(basedir,f'fonts/{font}')
        
        formatter = ImageFormatter(style=image.style, font_size=16, line_numbers=False,font_name=path_to_font)

        highlighted_code = highlight(image.code, lexer, formatter)

        # Create a custom stylesheet with your additional styles
        
        with open(screenshot_path, 'wb') as image_file:
            image_file.write(highlighted_code)
            
    except Exception as e:
        # Handle exceptions, log errors, or return an appropriate response
        print(f"Error: {e}")
        return None

    try:
        # Update the image path in the database
        
        image.image_file = screenshot_path
        db.session.commit()
        return image
    except Exception as e:
        # Handle database update errors
        print(f"Database Error: {e}")
        return None
    
    



