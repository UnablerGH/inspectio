from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def dziekan_menu():
    return render_template('dziekan-menu.html')

@views_bp.route('/edycja-szablonu')
def edycja_szablonu():
    return render_template('edycja-szablonu.html')

@views_bp.route('/menu')
def hospitacje_menu():
    return render_template('hospitacje-menu.html')

@views_bp.route('/dotyczace-mnie')
def hospitacje_dotyczace_mnie():
    return render_template('hospitacje-dotyczace-mnie.html')

@views_bp.route('/zlecone-mi')
def hospitacje_zlecone_mi():
    return render_template('zlecone-hospitacje.html')

@views_bp.route('/zatwierdzenie-hospitacji/<int:id>')
def zatwierdzenie_hospitacji(id):
    return render_template('zatwierdzenie-hospitacji.html', id=id)