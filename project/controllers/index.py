from project import app
from flask import (
    render_template, 
    redirect, 
    url_for, 
    request,
    jsonify
)
import openpyxl
from datetime import datetime
from pyppeteer import launch

data = []

#route export
@app.route('/export', methods = ['GET'])
def export():
    global data
    # Create a new workbook and select the active worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Add some data to the worksheet
    worksheet['A1'] = 'Company'
    worksheet['B1'] = 'Website'
    worksheet['C1'] = 'Company Linkedin Url'
    worksheet['D1'] = 'Company Phone'
    worksheet['E1'] = 'Company Address'
    worksheet['F1'] = 'Company State'
    worksheet['G1'] = 'Company City'
    worksheet['H1'] = 'Company Postal Code'
    worksheet['I1'] = 'Company Country'
    worksheet['J1'] = 'First Name'
    worksheet['K1'] = 'Last Name'
    worksheet['L1'] = 'Title'
    worksheet['M1'] = 'Email'
    worksheet['N1'] = 'Person Linkedin Url'

    for item in data:
        worksheet.append([
            item["company"],
            item["website"],
            item["linkedin_comp"],
            item["phone"],
            item["address"],
            item["state"],
            item["city"],
            item["code"],
            item["country"],
            item["fname"],
            item["lname"],
            item["title"],
            item["email"],
            item["linkedin_pers"],
        ])

    # Save the workbook
    try:
        workbook.save(str(datetime.now())+'.xlsx')
        return jsonify({"status": "success"})
    except Exception as err:
        return jsonify({"status": err})

#route index
@app.route('/', methods = ['GET', 'POST'])
def index():
    data = []
    if request.method == "POST":
        
        data.append({
        "company": "3D CAM International",
        "website": "3d-cam.com",
        "linkedin_comp": "http://www.linkedin.com/company/3d-cam-international-corporation",
        "phone": "818-773-8777",
        "address": "9801 Variel Ave",
        "state": "California",
        "city": "Los Angeles",
        "code": "91311-4317",
        "country": "United States",
        "fname": "Gary",
        "lname": "Vassighi",
        "title": "3d Prinitng, Plastic",
        "email": "gary@3d-cam.com",
        "linkedin_pers": "https://linkedin.com/in/gary-vassighi-931350b9",
    })
    return render_template('index.html', data=data)
