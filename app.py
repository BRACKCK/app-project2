from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
import numpy as np
from scipy.stats import norm
from datetime import datetime
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)  # More secure random key

    # Ensure database exists and has proper structure
    def init_db():
        if not os.path.exists('home_energy.db'):
            import database  # This will create the database
            import insert    # This will populate sample data

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            session['name'] = request.form.get('name')
            session['email'] = request.form.get('email')
            session['phone'] = request.form.get('phone')
            return redirect(url_for('assessment'))
        return render_template('index.html')

    @app.route('/assessment', methods=['GET', 'POST'])
    def assessment():
        if request.method == 'POST':
            session['assessment_data'] = request.form.to_dict()
            return redirect(url_for('results'))
        return render_template('assessment.html')

    class EnergyInferenceEngine:
        def __init__(self):
            self.db_path = 'home_energy.db'  # Corrected database file
            self.size_thresholds = {
                'very_small': 500,
                'small': 1000,
                'medium': 2000,
                'large': 3000,
                'very_large': 4000
            }
            self.usage_thresholds = {
                'very_low': 3,
                'low': 6,
                'medium': 12,
                'high': 18,
                'very_high': 24
            }
            self.default_recommendations = [
                "Install LED bulbs for better energy efficiency",
                "Use natural light when possible",
                "Unplug devices when not in use",
                "Regular maintenance of HVAC systems",
                "Consider using smart power strips"
            ]
            self.temp_params = {
                'cold': (16, 20),
                'comfort': (20, 24),
                'hot': (24, 30)
            }
            self.appliance_high_usage_prior = 0.3

        def validate_assessment_data(self, assessment_data):
            try:
                return {
                    'homeSize': float(assessment_data.get('homeSize', 1000)),
                    'occupants': int(assessment_data.get('occupants', 1)),
                    'location': str(assessment_data.get('location', '')),
                    'homeType': str(assessment_data.get('homeType', '')),
                    'acHours': float(assessment_data.get('acHours', 0)),
                    'preferredTemp': float(assessment_data.get('preferredTemp', 23))
                }
            except (ValueError, TypeError):
                return None

        def get_similar_homes(self, size, occupants, location, home_type):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT h.id, h.size, h.occupants, b.peak_usage_hours, b.daily_usage_hours
                    FROM home h
                    JOIN behavior b ON h.id = b.home_id
                    WHERE h.home_type = ? AND h.location = ?
                    AND ABS(h.size - ?) <= 500
                    AND ABS(h.occupants - ?) <= 2
                """, (home_type, location, size, occupants))
                
                similar_homes = cursor.fetchall()
                
                if not similar_homes:
                    cursor.execute("""
                        SELECT h.id, h.size, h.occupants, b.peak_usage_hours, b.daily_usage_hours
                        FROM home h
                        JOIN behavior b ON h.id = b.home_id
                        WHERE ABS(h.size - ?) <= 1000
                        LIMIT 5
                    """, (size,))
                    similar_homes = cursor.fetchall()
                
                conn.close()
                return similar_homes
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                return []

        def apply_rule_based_logic(self, assessment_data):
            rules = []
            size = float(assessment_data.get('homeSize', 0))
            if size < self.size_thresholds['small']:
                rules.append("Consider using space-efficient appliances")
            elif size > self.size_thresholds['large']:
                rules.append("Implement zone-based heating/cooling")
            
            ac_hours = float(assessment_data.get('acHours', 0))
            if ac_hours > self.usage_thresholds['high']:
                rules.append("High AC usage detected. Consider programmable thermostat")
            
            return rules
        
        def apply_fuzzy_logic(self, assessment_data):
            recommendations = []
            temp = float(assessment_data.get('preferredTemp', 23))
            
            cold_degree = max(0, min(1, (self.temp_params['cold'][1] - temp) / 
                                      (self.temp_params['cold'][1] - self.temp_params['cold'][0])))
            hot_degree = max(0, min(1, (temp - self.temp_params['hot'][0]) / 
                                      (self.temp_params['hot'][1] - self.temp_params['hot'][0])))
            comfort_degree = max(0, min(1, 1 - cold_degree - hot_degree))
            
            if cold_degree > 0.6:
                recommendations.append("Temperature settings suggest high heating needs")
            elif hot_degree > 0.6:
                recommendations.append("Consider natural cooling methods")
                
            return recommendations
        
        def apply_bayesian_reasoning(self, assessment_data, similar_homes):
            insights = []
            
            if similar_homes:
                high_usage_count = sum(1 for home in similar_homes if home[4] > self.usage_thresholds['high'])
                likelihood = high_usage_count / len(similar_homes) if similar_homes else 0
                
                posterior = (likelihood * self.appliance_high_usage_prior) / (
                    (likelihood * self.appliance_high_usage_prior) + 
                    ((1 - likelihood) * (1 - self.appliance_high_usage_prior))
                )

                if posterior > 0.7:
                    insights.append("High probability of excessive energy usage compared to similar homes")
                elif posterior < 0.3:
                    insights.append("Your usage pattern is more efficient than similar homes")
                    
            return insights
        
        def get_recommendations(self, assessment_data):
            recommendations = set()
            
            validated_data = self.validate_assessment_data(assessment_data)
            if not validated_data:
                return self.default_recommendations[:3]
            
            similar_homes = self.get_similar_homes(
                validated_data['homeSize'],
                validated_data['occupants'],
                validated_data['location'],
                validated_data['homeType']
            )
            
            try:
                rule_based = self.apply_rule_based_logic(validated_data)
                recommendations.update(rule_based)
            except Exception as e:
                print(f"Rule-based error: {e}")
                recommendations.add(self.default_recommendations[0])
                
            try:
                fuzzy_logic = self.apply_fuzzy_logic(validated_data)
                recommendations.update(fuzzy_logic)
            except Exception as e:
                print(f"Fuzzy logic error: {e}")
                recommendations.add(self.default_recommendations[1])
                
            try:
                bayesian = self.apply_bayesian_reasoning(validated_data, similar_homes)
                recommendations.update(bayesian)
            except Exception as e:
                print(f"Bayesian error: {e}")
                recommendations.add(self.default_recommendations[2])
            
            recommendations_list = list(recommendations)
            while len(recommendations_list) < 3:
                for rec in self.default_recommendations:
                    if rec not in recommendations_list:
                        recommendations_list.append(rec)
                        break
            
            return recommendations_list[:5]

    @app.route('/results')
    def results():
        if 'assessment_data' not in session:
            return redirect(url_for('index'))
            
        engine = EnergyInferenceEngine()
        recommendations = engine.get_recommendations(session['assessment_data'])
        
        return render_template('results.html', 
                             recommendations=recommendations,
                             assessment_data=session['assessment_data'],
                             date=datetime.now().strftime('%B %d, %Y'))

    # Initialize database when app starts
    init_db()
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
