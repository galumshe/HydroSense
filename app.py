from flask import Flask, render_template, request, send_file
from utils.calculator import calculate_water_usage
from utils.report_generator import generate_csv_report
import plotly.express as px
import plotly.utils
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    usage_data = {
        'shower_minutes': float(request.form.get('shower_minutes', 0)),
        'dishes_minutes': float(request.form.get('dishes_minutes', 0)),
        'laundry_loads': float(request.form.get('laundry_loads', 0)),
        'other_usage': float(request.form.get('other_usage', 0))
    }
    
    result = calculate_water_usage(usage_data)
    
    # Create visualization
    usage_breakdown = {
        'Shower': result['shower_usage'],
        'Dishes': result['dishes_usage'],
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
        'dishes_minutes': float(request.form.get('dishes_minutes', 0)),
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