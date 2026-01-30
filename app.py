"""
Health Dashboard - Flask Application Starter
Your task: Follow LAB_GUIDE.md to add form handling!
"""

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-memory storage for user data (we'll add to this during the lab!)
user_data = {}

@app.route('/')
def index():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    day_num = datetime.now().weekday()
    days_to_weekend = 5 - day_num if day_num < 5 else 0
    
    return render_template('index.html', 
                         time=current_time, 
                         days_to_weekend=days_to_weekend,
                         user_data=user_data)  # <- NEW!


@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission"""
    # Get form data
    name = request.form.get('name', '')
    sleep_hours = request.form.get('sleep_hours', '')
    water_glasses = request.form.get('water_glasses', '')
    calorie_intake = request.form.get('calorie_intake', '')
    age = request.form.get('age', '')
    activity_level = request.form.get('activity_level', '')
    mood_rating = request.form.get('mood_rating', '')
    
    # Store it
    user_data['name'] = name
    user_data['sleep_hours'] = sleep_hours
    user_data['water_glasses'] = water_glasses
    user_data['calorie_intake'] = calorie_intake
    user_data['age'] = age
    user_data['activity_level'] = activity_level
    user_data['mood_rating'] = mood_rating
    
    # Generate specific sleep feedback
    try:
        hours = float(sleep_hours)
        if hours < 5:
            user_data['feedback'] = "🚨 Critical! You need much more sleep. Aim for 7-9 hours."
        elif hours < 6:
            user_data['feedback'] = "⚠️ Insufficient sleep. Try to get at least 7 hours."
        elif hours < 7:
            user_data['feedback'] = "😴 Below optimal. Adding 1-2 more hours would help!"
        elif hours <= 9:
            user_data['feedback'] = "✅ Excellent! You're in the optimal sleep range."
        else:
            user_data['feedback'] = "😴 That's a lot of sleep! Make sure you're feeling rested."
    except ValueError:
        user_data['feedback'] = "Please enter valid hours."
    
    # Generate personalized water feedback based on age and activity
    try:
        glasses = int(water_glasses)
        age_num = int(age) if age else 30
        
        # Calculate recommended water intake based on activity level
        base_requirement = 8
        if activity_level == 'light':
            recommended = base_requirement + 1
        elif activity_level == 'moderate':
            recommended = base_requirement + 2
        elif activity_level == 'active':
            recommended = base_requirement + 3
        else:
            recommended = base_requirement + 1  # Default to light
        
        # Adjust for age (older adults need similar amounts)
        if age_num > 65:
            recommended = max(recommended, 8)  # Ensure minimum 8 glasses
        
        diff = glasses - recommended
        
        if diff >= 0:
            user_data['water_feedback'] = f"💦 Great hydration! You're meeting your {recommended}-glass target for your {activity_level or 'current'} activity level."
        elif diff >= -2:
            user_data['water_feedback'] = f"💧 Almost there! Try to reach {recommended} glasses based on your {activity_level or 'current'} activity."
        else:
            user_data['water_feedback'] = f"⚠️ Drink more water! Target: {recommended} glasses for {activity_level or 'your'} activity level (currently at {glasses})."
    except ValueError:
        user_data['water_feedback'] = "Please enter valid values for water, age, and activity level."
    
    # Generate personalized calorie feedback based on activity level
    try:
        calories = int(calorie_intake)
        age_num = int(age) if age else 30
        
        # Calculate recommended calorie ranges based on activity level
        if activity_level == 'light':
            cal_min, cal_max = 1800, 2200
            activity_desc = "light activity"
        elif activity_level == 'moderate':
            cal_min, cal_max = 2000, 2600
            activity_desc = "moderate activity"
        elif activity_level == 'active':
            cal_min, cal_max = 2400, 3000
            activity_desc = "very active lifestyle"
        else:
            cal_min, cal_max = 1800, 2200  # Default to light
            activity_desc = "your activity level"
        
        # Adjust for age (metabolism slows with age)
        if age_num > 50:
            cal_min -= 200
            cal_max -= 200
        elif age_num < 25:
            cal_min += 100
            cal_max += 100
        
        # Generate specific feedback
        if calories < cal_min - 300:
            user_data['calorie_feedback'] = f"🚨 Very low intake! You need {cal_min}-{cal_max} calories for your {activity_desc}. Consider eating more nutrient-dense foods."
        elif calories < cal_min:
            user_data['calorie_feedback'] = f"⚠️ Below target. Aim for {cal_min}-{cal_max} calories to fuel your {activity_desc}."
        elif calories <= cal_max:
            user_data['calorie_feedback'] = f"✅ Perfect! Your {calories} calories are ideal for your {activity_desc}."
        elif calories <= cal_max + 300:
            user_data['calorie_feedback'] = f"📊 Slightly high. Target: {cal_min}-{cal_max} for {activity_desc}. Balance with exercise!"
        else:
            user_data['calorie_feedback'] = f"⚠️ High intake! Recommended: {cal_min}-{cal_max} for {activity_desc}. Monitor portions or increase activity."
    except ValueError:
        user_data['calorie_feedback'] = "Please enter valid calorie amount."
    
    # Generate mood feedback
    try:
        mood = int(mood_rating)
        if mood <= 3:
            user_data['mood_feedback'] = "😟 Low mood detected. Consider talking to someone or doing something you enjoy."
        elif mood <= 5:
            user_data['mood_feedback'] = "😔 Feeling down? Try some exercise or connect with friends."
        elif mood <= 7:
            user_data['mood_feedback'] = "🙂 Decent mood! Keep up the healthy habits."
        elif mood <= 9:
            user_data['mood_feedback'] = "😄 Great mood! You're doing well today!"
        else:
            user_data['mood_feedback'] = "🎉 Excellent! You're feeling fantastic!"
    except ValueError:
        user_data['mood_feedback'] = "Please enter a valid mood rating (1-10)."
    
    print("DEBUG - Data stored:", user_data)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)