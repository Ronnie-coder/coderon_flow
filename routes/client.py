from flask import Blueprint, render_template
from flask_login import login_required

client_bp = Blueprint('client', __name__)

@client_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/client.html')

@client_bp.route('/request-service', methods=['POST'])
@login_required
def request_service():
    # Implementation for service request
    pass

@client_bp.route('/download-invoice/<int:invoice_id>')
@login_required
def download_invoice(invoice_id):
    # Implementation for invoice download
    pass