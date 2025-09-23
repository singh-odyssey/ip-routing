#!/usr/bin/env python3
"""
WEB UI FOR IP ROUTING BOT
========================

Web interface for the IP routing bot system that allows users to:
1. Generate unique views through Google Ambassador Bot
2. Run seminar parallel bot simulations 
3. Monitor real-time progress and statistics
4. Control bot operations from a browser

Features:
- Clean web interface
- Real-time progress updates
- Bot control (start/stop/pause)
- Statistics dashboard
- IP diversity monitoring
"""

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import threading
import time
import json
import os
import sys
import random
from datetime import datetime
import uuid

# Add current directory to path for importing our bot modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our bot classes
try:
    from google_ambassador_bot import GoogleAmbassadorBot
    from seminar_parallel_bot import SeminarParallelBot
    from smart_indian_simulator import SmartIndianIPSimulator
except ImportError as e:
    print(f"Error importing bot modules: {e}")
    sys.exit(1)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ip-routing-bot-secret-key-2024'

# Configure for production
if os.environ.get('FLASK_ENV') == 'production':
    app.config.update(
        DEBUG=False,
        TESTING=False
    )

socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False)

# Global variables for bot management
active_bots = {}
bot_stats = {}

class WebUIGoogleBot(GoogleAmbassadorBot):
    """Extended Google Ambassador Bot for web UI with real-time updates"""
    
    def __init__(self, target_url, session_id):
        super().__init__(target_url)
        self.session_id = session_id
        self.is_running = False
        self.is_paused = False
        
    def emit_update(self, event_type, data):
        """Emit real-time updates to the web UI"""
        print(f"[DEBUG] Emitting {event_type} event for session {self.session_id}: {data}")
        socketio.emit('bot_update', {
            'session_id': self.session_id,
            'event_type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
    
    def generate_unique_view(self):
        """Override to include web UI updates"""
        if not self.is_running or self.is_paused:
            return False
            
        try:
            # Create enhanced Indian session
            session = self.create_enhanced_indian_session()
            
            # Get session info for logging
            session_info = self.ip_simulator.get_session_info(session)
            
            # Emit session info
            self.emit_update('new_session', {
                'location': f"{session_info['city']}, {session_info['region']}",
                'isp': f"{session_info['isp']} ({session_info['connection_type']})",
                'session_id': session_info['session_id'],
                'ip': session_info['simulated_ip'],
                'user_agent': session_info['user_agent'][:50] + '...'
            })
            
            # Simulate realistic user behavior
            success = self.simulate_user_behavior(session, self.target_url)
            
            if success:
                self.success_count += 1
                self.emit_update('view_success', {
                    'total_success': self.success_count,
                    'total_failed': self.error_count
                })
            else:
                self.error_count += 1
                self.emit_update('view_failed', {
                    'total_success': self.success_count,
                    'total_failed': self.error_count
                })
            
            # Emit statistics update
            total_attempts = self.success_count + self.error_count
            success_rate = (self.success_count / total_attempts * 100) if total_attempts > 0 else 0
            
            self.emit_update('stats_update', {
                'success_count': self.success_count,
                'error_count': self.error_count,
                'success_rate': round(success_rate, 1),
                'total_attempts': total_attempts
            })
            
            return success
            
        except Exception as e:
            self.error_count += 1
            self.emit_update('bot_error', {'error': str(e)})
            return False
        finally:
            # Always close the session
            if 'session' in locals():
                session.close()
    
    def run_continuous_unique_views(self, target_views=None):
        """Override to include web UI updates and controls"""
        self.is_running = True
        self.emit_update('bot_started', {
            'target_url': self.target_url,
            'target_views': target_views,
            'timing_range': self.timing_range
        })
        
        view_count = 0
        
        try:
            while self.is_running and (target_views is None or view_count < target_views):
                if self.is_paused:
                    time.sleep(1)
                    continue
                    
                view_count += 1
                
                self.emit_update('view_start', {'view_number': view_count})
                
                # Generate unique view
                success = self.generate_unique_view()
                
                # Show session diversity every 5 views
                if view_count % 5 == 0:
                    uniqueness = self.ip_simulator.verify_session_uniqueness()
                    self.emit_update('diversity_update', {
                        'unique_ips': uniqueness['unique_ips'],
                        'unique_cities': uniqueness['unique_cities'],
                        'unique_isps': uniqueness['unique_isps'],
                        'cities_used': uniqueness['cities_used'][:10],
                        'isps_used': uniqueness['isps_used']
                    })
                
                # Wait with random timing before next view
                if self.is_running and not self.is_paused and (target_views is None or view_count < target_views):
                    wait_time = random.uniform(self.timing_range[0], self.timing_range[1])
                    self.emit_update('waiting', {'wait_time': round(wait_time, 2)})
                    
                    # Wait in small increments to allow for pause/stop
                    for _ in range(int(wait_time * 10)):
                        if not self.is_running or self.is_paused:
                            break
                        time.sleep(0.1)
                    
        except Exception as e:
            self.emit_update('bot_error', {'error': str(e)})
        finally:
            self.is_running = False
            
            # Final statistics
            uniqueness = self.ip_simulator.verify_session_uniqueness()
            self.emit_update('bot_completed', {
                'success_count': self.success_count,
                'error_count': self.error_count,
                'unique_ips': uniqueness['unique_ips'],
                'unique_cities': uniqueness['unique_cities'],
                'unique_isps': uniqueness['unique_isps'],
                'cities_used': uniqueness['cities_used'],
                'isps_used': uniqueness['isps_used']
            })

class WebUISeminarBot(SeminarParallelBot):
    """Extended Seminar Bot for web UI with real-time updates"""
    
    def __init__(self, max_students, target_url, session_id):
        super().__init__(max_students, target_url)
        self.session_id = session_id
        self.is_running = False
        
    def emit_update(self, event_type, data):
        """Emit real-time updates to the web UI"""
        socketio.emit('seminar_update', {
            'session_id': self.session_id,
            'event_type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })

# Flask Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/google-bot')
def google_bot_page():
    """Google Ambassador Bot page"""
    return render_template('google_bot.html')

@app.route('/seminar-bot')  
def seminar_bot_page():
    """Seminar Parallel Bot page"""
    return render_template('seminar_bot.html')

@app.route('/stats')
def stats_page():
    """Statistics dashboard page"""
    return render_template('stats.html')

# API Routes
@app.route('/api/validate-url', methods=['POST'])
def validate_url():
    """Validate URL endpoint"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'valid': False, 'error': 'URL cannot be empty'})
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        from urllib.parse import urlparse
        result = urlparse(url)
        valid = all([result.scheme, result.netloc])
        
        if valid:
            return jsonify({'valid': True, 'url': url})
        else:
            return jsonify({'valid': False, 'error': 'Invalid URL format'})
    except:
        return jsonify({'valid': False, 'error': 'Invalid URL format'})

@app.route('/api/start-google-bot', methods=['POST'])
def start_google_bot():
    """Start Google Ambassador Bot"""
    data = request.get_json()
    target_url = data.get('url')
    target_views = data.get('views')
    
    if not target_url:
        return jsonify({'success': False, 'error': 'URL is required'})
    
    # Create unique session ID
    session_id = str(uuid.uuid4())
    
    # Create bot instance
    bot = WebUIGoogleBot(target_url, session_id)
    active_bots[session_id] = bot
    
    # Start bot in separate thread
    def run_bot():
        # Small delay to ensure WebSocket connection is established
        time.sleep(0.5)
        try:
            bot.run_continuous_unique_views(target_views)
        except Exception as e:
            bot.emit_update('bot_error', {'error': str(e)})
        finally:
            if session_id in active_bots:
                del active_bots[session_id]
    
    thread = threading.Thread(target=run_bot)
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'session_id': session_id})

@app.route('/api/start-seminar-bot', methods=['POST'])
def start_seminar_bot():
    """Start Seminar Parallel Bot"""
    data = request.get_json()
    target_url = data.get('url')
    num_students = data.get('students', 100)
    
    if not target_url:
        return jsonify({'success': False, 'error': 'URL is required'})
    
    # Create unique session ID
    session_id = str(uuid.uuid4())
    
    # Create bot instance
    bot = WebUISeminarBot(num_students, target_url, session_id)
    active_bots[session_id] = bot
    
    # Start bot in separate thread
    def run_bot():
        try:
            bot.simulate_seminar_qr_scanning(num_students)
        except Exception as e:
            bot.emit_update('bot_error', {'error': str(e)})
        finally:
            if session_id in active_bots:
                del active_bots[session_id]
    
    thread = threading.Thread(target=run_bot)
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'session_id': session_id})

@app.route('/api/control-bot', methods=['POST'])
def control_bot():
    """Control bot (pause/resume/stop)"""
    data = request.get_json()
    session_id = data.get('session_id')
    action = data.get('action')
    
    if session_id not in active_bots:
        return jsonify({'success': False, 'error': 'Bot not found'})
    
    bot = active_bots[session_id]
    
    if action == 'pause':
        bot.is_paused = True
        bot.emit_update('bot_paused', {})
    elif action == 'resume':
        bot.is_paused = False
        bot.emit_update('bot_resumed', {})
    elif action == 'stop':
        bot.is_running = False
        bot.emit_update('bot_stopped', {})
    
    return jsonify({'success': True})

@app.route('/api/get-ip-database')
def get_ip_database():
    """Get IP database information"""
    simulator = SmartIndianIPSimulator()
    
    # Group IPs by city and ISP
    cities = {}
    isps = {}
    
    for ip_info in simulator.indian_ips_db:
        city = ip_info['city']
        isp = ip_info['isp']
        
        if city not in cities:
            cities[city] = 0
        cities[city] += 1
        
        if isp not in isps:
            isps[isp] = 0
        isps[isp] += 1
    
    return jsonify({
        'total_ips': len(simulator.indian_ips_db),
        'cities': cities,
        'isps': isps,
        'sample_ips': simulator.indian_ips_db[:10]  # First 10 for preview
    })

# WebSocket Events
@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    emit('connected', {'status': 'Connected to IP Routing Bot Server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🌐 Starting IP Routing Bot Web UI...")
    print("📡 Server will be available at: http://localhost:5000")
    print("🎯 Features: Google Ambassador Bot, Seminar Bot, Real-time monitoring")
    
    # Add Flask to requirements if not already there
    requirements_path = 'requirements.txt'
    with open(requirements_path, 'r') as f:
        existing_requirements = f.read()
    
    flask_requirements = [
        'flask>=2.3.0',
        'flask-socketio>=5.3.0',
        'python-socketio>=5.8.0'
    ]
    
    needs_update = False
    for req in flask_requirements:
        package_name = req.split('>=')[0]
        if package_name not in existing_requirements:
            existing_requirements += f"\n{req}"
            needs_update = True
    
    if needs_update:
        with open(requirements_path, 'w') as f:
            f.write(existing_requirements)
        print("📝 Updated requirements.txt with Flask dependencies")
    
    # Run the Flask app with SocketIO
    # Use PORT environment variable for deployment platforms like Render
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'development') != 'production'
    
    # For production deployment, we let Gunicorn handle the server
    # Only run the development server when this file is executed directly
    if __name__ == '__main__':
        print("🚀 Starting development server...")
        socketio.run(app, host='0.0.0.0', port=port, debug=debug_mode, allow_unsafe_werkzeug=True)