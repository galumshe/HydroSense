def calculate_water_usage(data):
    """
    Calculate water usage based on user input.
    
    Parameters:
    - data: dict containing shower_minutes, dishes_minutes, laundry_loads, and other_usage
    
    Returns:
    - dict containing calculated water usage and analysis
    """
    # Water usage constants (liters)
    SHOWER_RATE = 10  # liters per minute
    DISHES_RATE = 6   # liters per minute
    COOKING_RATE = 6   # liters per minute
    LAUNDRY_LOAD = 50 # liters per load
    STANDARD_DAILY_USAGE = 100  # standard daily usage per person
    
    # Calculate individual usages
    shower_usage = data['shower_minutes'] * SHOWER_RATE
    dishes_usage = data['dishes_minutes'] * DISHES_RATE
    cooking_usage = data['cooking_minutes'] * COOKING_RATE
    laundry_usage = data['laundry_loads'] * LAUNDRY_LOAD / 7  # Convert weekly to daily
    other_usage = data['other_usage']
    
    # Calculate total usage
    total_usage = shower_usage + cooking_usage + dishes_usage + laundry_usage + other_usage
    
    # Determine if usage exceeds standard
    exceeds_standard = total_usage > STANDARD_DAILY_USAGE
    
    # Generate conservation tips if usage exceeds standard
    conservation_tips = []
    if exceeds_standard:
        if shower_usage > 50:
            conservation_tips.append("Consider taking shorter showers")
        if dishes_usage > 30:
            conservation_tips.append("Try using a dishwasher or being more efficient with dish washing")
        if laundry_usage > 20:
            conservation_tips.append("Consider doing full loads of laundry to maximize efficiency")
    
    return {
        'total_usage': round(total_usage, 2),
        'shower_usage': round(shower_usage, 2),
        'dishes_usage': round(dishes_usage, 2),
        'cooking_usage': round(cooking_usage, 2),
        'laundry_usage': round(laundry_usage, 2),
        'other_usage': round(other_usage, 2),
        'exceeds_standard': exceeds_standard,
        'standard_usage': STANDARD_DAILY_USAGE,
        'conservation_tips': conservation_tips
    }