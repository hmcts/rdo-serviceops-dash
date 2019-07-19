from flask import Blueprint, render_template

documents = Blueprint('documents', __name__)

@documents.route('/documents')
def documents_main():
    return render_template('cloud_services/documents/documents.html')

@documents.route('/documents/confluence')
def documents_confluence():
    return render_template('cloud_services/documents/confluence.html')