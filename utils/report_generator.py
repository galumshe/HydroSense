import pandas as pd
import os
from datetime import datetime

def generate_csv_report(data):
    """
    Generate a CSV report of water usage data.
    
    Parameters:
    - data: dict containing water usage data
    
    Returns:
    - str: path to generated CSV file
    """
    from .calculator import calculate_water_usage
    
    # Calculate detailed usage
    result = calculate_water_usage(data)
    
    # Prepare data for CSV
    report_data = {
        'Category': ['Shower', 'Dishes', 'Laundry', 'Other', 'Total'],
        'Usage (Liters)': [
            result['shower_usage'],
            result['dishes_usage'],
            result['laundry_usage'],
            result['other_usage'],
            result['total_usage']
        ]
    }
    
    # Create DataFrame
    df = pd.DataFrame(report_data)
    
    # Generate unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'water_usage_report_{timestamp}.csv'
    filepath = os.path.join('static', 'reports', filename)
    
    # Ensure reports directory exists
    os.makedirs(os.path.join('static', 'reports'), exist_ok=True)
    
    # Save to CSV
    df.to_csv(filepath, index=False)
    
    return filepath