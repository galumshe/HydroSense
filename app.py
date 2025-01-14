from flask import Flask, render_template, request, send_file
from utils.calculator import calculate_water_usage
from utils.report_generator import generate_csv_report
import plotly.express as px
import plotly.utils
import json

app = Flask(__name__)
# routes 
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    usage_data = {
        'shower_minutes': float(request.form.get('shower_minutes', 0)),
        'toilet_flushes': float(request.form.get('toilet_flushes', 0)),
        'dishes_minutes': float(request.form.get('dishes_minutes', 0)),
        'cooking_minutes': float(request.form.get('cooking_minutes', 0)),
        'laundry_loads': float(request.form.get('laundry_loads', 0)),
        'other_usage': float(request.form.get('other_usage', 0))
    }
    
    result = calculate_water_usage(usage_data)
    
    # Create visualization
    usage_breakdown = {
        'Shower': result['shower_usage'],
        'Toilet': result['toilet_usage'],
        'Dishes': result['dishes_usage'],
        'Cooking': result['cooking_usage'],
        'Laundry': result['laundry_usage'],
        'Other': result['other_usage']
    }
    
    fig = px.pie(
        values=list(usage_breakdown.values()),
        names=list(usage_breakdown.keys()),
        title='Water Usage Breakdown'
    )
    
    chart_json = json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template(
        'result.html',
        result=result,
        chart_json=chart_json
    )

@app.route('/download-report', methods=['POST'])
def download_report():
    usage_data = {
        'shower_minutes': float(request.form.get('shower_minutes', 0)),
        'toilet_flushes': float(request.form.get('toilet_flushes', 0)),
        'dishes_minutes': float(request.form.get('dishes_minutes', 0)),
        'cooking_minutes': float(request.form.get('cooking_minutes', 0)),  # Corrected key
        'laundry_loads': float(request.form.get('laundry_loads', 0)),
        'other_usage': float(request.form.get('other_usage', 0))
    }
    
    csv_path = generate_csv_report(usage_data)
    return send_file(
        csv_path,
        mimetype='text/csv',
        as_attachment=True,
        download_name='water_usage_report.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)

# error handling after route definitions in app.py
@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', message="Something went wrong. Please try again later."), 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', message="Page not found."), 404
