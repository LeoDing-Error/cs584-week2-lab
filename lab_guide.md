# Week 2 Lab Guide: Interactive Health Dashboard

## Goal

Build an interactive Flask app that collects user health data through forms and provides personalized feedback.

---

## Part 1: Understanding the Starting Point (5 min)

You already have a simple working app that shows:

- Current time
- Days until weekend

**Open your app in the browser and verify it works. (See README.md for a reminder on Flask run instructions)**

---

## Part 2: Add a Form (15 min)

### Step 1: Update `templates/index.html`

Add this new form section **after** the `.info-section` closing `</div>`:

```html
<!-- Health Data Form -->
<section class="form-section">
  <h2>Log Your Daily Health</h2>
  <form action="/submit" method="POST" class="health-form">
    <div class="form-group">
      <label for="name">Your Name:</label>
      <input
        type="text"
        id="name"
        name="name"
        placeholder="Enter your name"
        required
      />
    </div>

    <div class="form-group">
      <label for="sleep_hours">Hours of Sleep:</label>
      <input
        type="number"
        id="sleep_hours"
        name="sleep_hours"
        placeholder="7.5"
        step="0.5"
        required
      />
    </div>

    <button type="submit" class="submit-btn">Save</button>
  </form>
</section>
```

### Step 2: Add Basic Form CSS

Add to `static/style.css`:

```css
.form-section {
  padding: 40px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1em;
}

.submit-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 15px 40px;
  border: none;
  border-radius: 8px;
  font-size: 1.1em;
  cursor: pointer;
}

.submit-btn:hover {
  transform: translateY(-2px);
}
```

**Refresh your browser.** You should see a form!

**Try clicking Submit.** What happens? (Hint: It breaks! That's expected.)

---

## Part 3: Handle Form Submission (20 min)

### Why It Broke

The form sends a **POST request** to `/submit`, but we don't have that route yet.

### Key Concept: GET vs POST

- **GET**: Request data from server (what we've been doing)
- **POST**: Send data to server (what forms do)

### Step 1: Import `request` in `app.py`

Change the first line to:

```python
from flask import Flask, render_template, request, redirect, url_for
```

### Step 2: Add In-Memory Storage

Add this **after** creating the Flask app:

```python
# In-memory storage (resets when app restarts)
user_data = {}
```

### Step 3: Pass `user_data` to Template

Update your index route:

```python
@app.route('/')
def index():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    day_num = datetime.now().weekday()
    days_to_weekend = 5 - day_num if day_num < 5 else 0

    return render_template('index.html',
                         time=current_time,
                         days_to_weekend=days_to_weekend,
                         user_data=user_data)  # <- NEW!
```

### Step 4: Create `/submit` Route

Add this new route **before** `if __name__ == '__main__':`:

```python
@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission"""
    # Get form data
    name = request.form.get('name', '')
    sleep_hours = request.form.get('sleep_hours', '')

    # Store it
    user_data['name'] = name
    user_data['sleep_hours'] = sleep_hours

    # Generate feedback
    try:
        hours = float(sleep_hours)
        if hours < 7:
            user_data['feedback'] = "⚠️ Try to get more sleep!"
        else:
            user_data['feedback'] = "✅ Great sleep!"
    except ValueError:
        user_data['feedback'] = "Please enter valid hours."

    print("DEBUG - Data stored:", user_data) # <-- Show your collected variable in terminal.
    # ... it's being stored as an in-memory Python dict... it's not going to an API or database yet! We'll work on that in a future lecture.

    # Redirect back to home
    return redirect(url_for('index'))
```

**What's happening here?**

1. `request.form.get()` retrieves form data
2. We store it in our dictionary
3. We calculate feedback
4. We redirect back to `/` (PRG pattern)

---

## Part 4: Display Feedback (10 min)

### Add Feedback Section to `index.html`

Add this **after** your form section, but **before** `<footer>`:

```html
<!-- Display Feedback -->
{% if user_data.name %}
<section class="feedback-section">
  <h2>Hello, {{ user_data.name }}! 👋</h2>
  <p>You slept {{ user_data.sleep_hours }} hours.</p>
  <p><strong>{{ user_data.feedback }}</strong></p>
</section>
{% endif %}
```

**Key Concept: Conditional Rendering**

- `{% if user_data.name %}` only shows section if name exists
- This is how you build dynamic interfaces!

### Add CSS for Feedback

```css
.feedback-section {
  padding: 40px;
  background: #f8f9fa;
}

.feedback-section h2 {
  color: #333;
  margin-bottom: 15px;
}

.feedback-section p {
  color: #555;
  font-size: 1.1em;
  margin: 10px 0;
}
```

**Test it!** Fill out the form and submit. You should see personalized feedback.

---

## Part 5: Lab Challenges (Remaining Time)

### Challenge 1: Add Water Tracking

Add another form field for glasses of water. Provide feedback if < 8 glasses.

**Hints:**

- Add `<input type="number" name="water_glasses">` to form
- Get it with `request.form.get('water_glasses', '')`
- Calculate feedback and display it

### Challenge 2: Make Form Values Persist

After submission, the form goes blank. Fix it!

**Hint:** Use Jinja in the input value:

```html
<input type="text" name="name" value="{{ user_data.name or '' }}" />
```

### Challenge 3: Style It Better

Make it look professional:

- Use CSS Grid for form layout: [Mozilla - CSS grid layout](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout)
- Change color scheme: here's one of many sites you could explore [https://coolors.co/palettes/trending](https://coolors.co/palettes/trending) -- you can click on any palette and copy as CSS. Typically you would be using a front-end framework to help with this, but it's still good to dig into some raw CSS a bit.
- Add hover effects: [Mozilla - CSS hover effects](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:hover)
- Create styled feedback cards

## Extra Lab Challenges

### Challenge 4: Add Another Health Metric

Add a new form field to track something else (e.g., exercise minutes, mood rating).

- Update the form in `index.html`
- Add a new feedback function in `app.py`
- Display feedback in the template

### Challenge 5: Better Feedback Logic

Improve the feedback functions to be more specific:

- Sleep: Different messages for < 5hrs, 5-6hrs, 7-9hrs, > 9hrs
- Water: Consider age/activity level (you'll need more form fields!)

---

## Key Takeaways

✅ **Forms** let users send data to your server  
✅ **GET** requests display pages, **POST** requests process data  
✅ **PRG pattern** (Post-Redirect-Get) prevents duplicate submissions  
✅ **In-memory storage** is temporary (database is permanent)  
✅ **Conditional rendering** creates dynamic UIs

---

## What's Next?

For the assignment (due Week 4), you'll:

1. Use **Git branches** for each feature
2. Create **pull requests** to merge features
3. Track work on a **GitHub Project board**
4. Build something creative with these concepts

This workflow is similar to what you'll use with your GH partner :)
