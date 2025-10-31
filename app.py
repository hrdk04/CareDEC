# ==================== IMPORTS ====================
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_cors import CORS
from functools import wraps
import os
import requests
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# ==================== APP CONFIGURATION ====================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

CORS(app, supports_credentials=True)

# Django API URL (for backend integration)
DJANGO_API_URL = os.getenv('DJANGO_API_URL', 'http://localhost:8000/api')

# ==================== HELPER FUNCTIONS ====================

def make_api_request(endpoint, method='GET', data=None, headers=None):
    """
    Helper function to make requests to Django backend
    UNCOMMENT THIS WHEN BACKEND IS READY
    """
    # try:
    #     url = f"{DJANGO_API_URL}/{endpoint}"
    #     
    #     # Add auth token if user is logged in
    #     if headers is None:
    #         headers = {}
    #     
    #     if 'auth_token' in session:
    #         headers['Authorization'] = f"Bearer {session['auth_token']}"
    #     
    #     if method == 'GET':
    #         response = requests.get(url, headers=headers, timeout=10)
    #     elif method == 'POST':
    #         response = requests.post(url, json=data, headers=headers, timeout=10)
    #     elif method == 'PUT':
    #         response = requests.put(url, json=data, headers=headers, timeout=10)
    #     elif method == 'DELETE':
    #         response = requests.delete(url, headers=headers, timeout=10)
    #     
    #     return response.json() if response.status_code < 400 else None
    # 
    # except requests.exceptions.RequestException as e:
    #     print(f"API Error: {e}")
    #     return None
    pass


def login_required(f):
    """
    Decorator to require login for certain routes
    UNCOMMENT THIS WHEN AUTHENTICATION IS READY
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # if 'user_id' not in session:
        #     flash('Please login to access this page', 'warning')
        #     return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def verify_flow(required_flow):
    """
    Decorator to verify user came from correct flow
    Example: @verify_flow('signup')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # auth_flow = session.get('auth_flow')
            # if auth_flow != required_flow:
            #     flash('Invalid access. Please complete the registration process.', 'error')
            #     return redirect(url_for('register'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    """
    Homepage - Caregiver listing page
    """
    # BACKEND INTEGRATION:
    # caregivers = make_api_request('caregivers', method='GET')
    # filters = request.args.to_dict()
    # if filters:
    #     caregivers = make_api_request('caregivers/filter', method='POST', data=filters)
    
    return render_template('index.html')


@app.route('/landing')
def landing():
    """
    Language selection landing page
    First page users see before login/signup
    """
    return render_template('pages/landingPage.html')


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page with OTP flow
    Flow: Login → OTP → Dashboard/Index
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # BACKEND INTEGRATION:
        # response = make_api_request('auth/login', method='POST', data={
        #     'email': email,
        #     'password': password
        # })
        # 
        # if response and response.get('success'):
        #     session['auth_flow'] = 'login'
        #     session['user_email'] = email
        #     session['temp_user_id'] = response.get('user_id')
        #     
        #     # Send OTP
        #     otp_sent = make_api_request('auth/send-otp', method='POST', data={
        #         'email': email,
        #         'type': 'login'
        #     })
        #     
        #     if otp_sent:
        #         flash('OTP sent to your email', 'success')
        #         return redirect(url_for('otp_verify', **{'from': 'login'}))
        #     else:
        #         flash('Error sending OTP', 'error')
        # else:
        #     flash('Invalid credentials', 'error')
        
        # For demo (remove in production):
        session['auth_flow'] = 'login'
        session['user_email'] = email
        return redirect(url_for('otp_verify', **{'from': 'login'}))
    
    return render_template('pages/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registration page with OTP flow
    Flow: Register → OTP → Who-need-care → Member-details → Patient-details → Index
    """
    if request.method == 'POST':
        data = {
            'full_name': request.form.get('fullName'),
            'dob': request.form.get('dob'),
            'email': request.form.get('email'),
            'mobile': request.form.get('mobile'),
            'password': request.form.get('password'),
            'gender': request.form.get('gender')
        }
        
        # BACKEND INTEGRATION:
        # response = make_api_request('auth/register', method='POST', data=data)
        # 
        # if response and response.get('success'):
        #     session['auth_flow'] = 'signup'
        #     session['user_email'] = data['email']
        #     session['temp_user_id'] = response.get('user_id')
        #     
        #     # Send OTP
        #     otp_sent = make_api_request('auth/send-otp', method='POST', data={
        #         'email': data['email'],
        #         'type': 'signup'
        #     })
        #     
        #     if otp_sent:
        #         flash('Please verify your email with OTP', 'success')
        #         return redirect(url_for('otp_verify', **{'from': 'signup'}))
        #     else:
        #         flash('Error sending OTP', 'error')
        # else:
        #     flash('Registration failed. Email may already exist.', 'error')
        
        # For demo (remove in production):
        session['auth_flow'] = 'signup'
        session['user_email'] = data['email']
        session['signup_data'] = data
        return redirect(url_for('otp_verify', **{'from': 'signup'}))
    
    return render_template('pages/register.html')


@app.route('/otp')
def otp_verify():
    """
    OTP verification page - handles multiple flows
    Flows:
    - login: OTP → Index
    - signup: OTP → Who-need-care
    - forgot-password: OTP → Reset-password
    """
    otp_from = request.args.get('from', 'login')
    
    # Store flow type in session
    if otp_from in ['login', 'signup', 'forgot-password']:
        session['otp_type'] = otp_from
    
    return render_template('pages/otp-verification.html', otp_from=otp_from)


@app.route('/api/verify-otp', methods=['POST'])
def api_verify_otp():
    """
    API endpoint to verify OTP
    Called from frontend JavaScript
    """
    data = request.get_json()
    otp = data.get('otp')
    email = data.get('email')
    otp_type = data.get('type')
    
    # BACKEND INTEGRATION:
    # response = make_api_request('auth/verify-otp', method='POST', data={
    #     'email': email,
    #     'otp': otp,
    #     'type': otp_type
    # })
    # 
    # if response and response.get('success'):
    #     if otp_type == 'login':
    #         session['user_id'] = response.get('user_id')
    #         session['auth_token'] = response.get('token')
    #         session['is_authenticated'] = True
    #         session.pop('auth_flow', None)
    #         return jsonify({'success': True, 'redirect': '/'})
    #     
    #     elif otp_type == 'signup':
    #         session['user_id'] = response.get('user_id')
    #         session['is_verified'] = True
    #         return jsonify({'success': True, 'redirect': '/whoneedcare'})
    #     
    #     elif otp_type == 'forgot-password':
    #         session['reset_token'] = response.get('reset_token')
    #         return jsonify({'success': True, 'redirect': '/reset-pass'})
    # 
    # return jsonify({'success': False, 'message': 'Invalid OTP'}), 400
    
    # For demo (remove in production):
    return jsonify({'success': True, 'redirect': '/whoneedcare' if otp_type == 'signup' else '/'})


@app.route('/api/resend-otp', methods=['POST'])
def api_resend_otp():
    """
    API endpoint to resend OTP
    """
    data = request.get_json()
    email = data.get('email')
    otp_type = data.get('type')
    
    # BACKEND INTEGRATION:
    # response = make_api_request('auth/resend-otp', method='POST', data={
    #     'email': email,
    #     'type': otp_type
    # })
    # 
    # if response and response.get('success'):
    #     return jsonify({'success': True, 'message': 'OTP resent successfully'})
    # 
    # return jsonify({'success': False, 'message': 'Failed to resend OTP'}), 400
    
    # For demo:
    return jsonify({'success': True, 'message': 'OTP resent successfully'})


@app.route('/forget-pass', methods=['GET', 'POST'])
def forget_password():
    """
    Forgot password page
    Flow: Forget-password → OTP → Reset-password → Login
    """
    if request.method == 'POST':
        email = request.form.get('email')
        
        # BACKEND INTEGRATION:
        # response = make_api_request('auth/forgot-password', method='POST', data={
        #     'email': email
        # })
        # 
        # if response and response.get('success'):
        #     session['auth_flow'] = 'forgot-password'
        #     session['user_email'] = email
        #     flash('OTP sent to your email', 'success')
        #     return redirect(url_for('otp_verify', **{'from': 'forgot-password'}))
        # else:
        #     flash('Email not found', 'error')
        
        # For demo:
        session['auth_flow'] = 'forgot-password'
        session['user_email'] = email
        return redirect(url_for('otp_verify', **{'from': 'forgot-password'}))
    
    return render_template('pages/forget-password.html')


@app.route('/reset-pass', methods=['GET', 'POST'])
def reset_password():
    """
    Reset password page
    Requires valid reset token from OTP verification
    """
    # Verify user came from OTP verification
    # if 'reset_token' not in session:
    #     flash('Invalid or expired reset link', 'error')
    #     return redirect(url_for('forget_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        email = session.get('user_email')
        
        # BACKEND INTEGRATION:
        # response = make_api_request('auth/reset-password', method='POST', data={
        #     'email': email,
        #     'password': password,
        #     'token': session.get('reset_token')
        # })
        # 
        # if response and response.get('success'):
        #     session.pop('reset_token', None)
        #     session.pop('auth_flow', None)
        #     session.pop('user_email', None)
        #     flash('Password reset successfully! Please login.', 'success')
        #     return redirect(url_for('login'))
        # else:
        #     flash('Error resetting password', 'error')
        
        # For demo:
        flash('Password reset successfully!', 'success')
        return redirect(url_for('login'))
    
    return render_template('pages/reset-password.html')


@app.route('/logout')
def logout():
    """
    Logout user and clear session
    """
    # BACKEND INTEGRATION:
    # if 'auth_token' in session:
    #     make_api_request('auth/logout', method='POST')
    
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('landing'))


# ==================== ONBOARDING FLOW (After Signup) ====================

@app.route('/whoneedcare', methods=['GET', 'POST'])
# @verify_flow('signup')  # Uncomment in production
def who_need_care():
    """
    Multi-step form: Who needs care
    Flow after signup: Who-need-care → Member-details → Patient-details → Index
    """
    if request.method == 'POST':
        data = request.get_json()
        
        # BACKEND INTEGRATION:
        # response = make_api_request('care-needs', method='POST', data={
        #     'user_id': session.get('user_id'),
        #     'who_needs_care': data.get('whoNeedsCare'),
        #     'age': data.get('age'),
        #     'postcode': data.get('postcode'),
        #     'help_option': data.get('helpOption'),
        #     'services': data.get('services')
        # })
        # 
        # if response and response.get('success'):
        #     session['care_need_id'] = response.get('care_need_id')
        #     return jsonify({'success': True, 'redirect': '/enter-member-details'})
        # 
        # return jsonify({'success': False}), 400
        
        # For demo:
        return jsonify({'success': True})
    
    return render_template('pages/who-need-care.html')


@app.route("/enter-member-details", methods=["GET", "POST"])
# @login_required  # Uncomment in production
def enter_member_details():
    """
    Enter member details form
    Part of signup onboarding flow
    """
    if request.method == "POST":
        data = request.form.to_dict()
        
        # BACKEND INTEGRATION:
        # response = make_api_request('members', method='POST', data={
        #     'user_id': session.get('user_id'),
        #     'care_need_id': session.get('care_need_id'),
        #     'full_name': data.get('fullName'),
        #     'dob': data.get('dob'),
        #     'phone': data.get('phone'),
        #     'gender': data.get('gender'),
        #     'address1': data.get('address1'),
        #     'address2': data.get('address2'),
        #     'country': data.get('country'),
        #     'state': data.get('state'),
        #     'city': data.get('city'),
        #     'pincode': data.get('pincode')
        # })
        # 
        # if response and response.get('success'):
        #     session['member_id'] = response.get('member_id')
        #     return redirect(url_for('enter_patient_details'))
        # else:
        #     flash('Error saving member details', 'error')
        
        print("Received member details:", data)
        return redirect(url_for('enter_patient_details'))
    
    return render_template("pages/enter-member-details.html")


@app.route("/enter-patient-details", methods=["GET", "POST"])
# @login_required  # Uncomment in production
def enter_patient_details():
    """
    Enter patient details form
    Final step of signup onboarding flow
    """
    if request.method == "POST":
        data = request.form.to_dict()
        
        # BACKEND INTEGRATION:
        # response = make_api_request('patients', method='POST', data={
        #     'user_id': session.get('user_id'),
        #     'member_id': session.get('member_id'),
        #     'address1': data.get('address1'),
        #     'address2': data.get('address2'),
        #     'country': data.get('country'),
        #     'state': data.get('state'),
        #     'city': data.get('city'),
        #     'pincode': data.get('pincode')
        # })
        # 
        # if response and response.get('success'):
        #     # Complete onboarding
        #     session['onboarding_completed'] = True
        #     session.pop('auth_flow', None)
        #     flash('Registration completed successfully!', 'success')
        #     return redirect(url_for('index'))
        # else:
        #     flash('Error saving patient details', 'error')
        
        print("Patient details received:", data)
        return redirect(url_for('success'))
    
    return render_template("pages/enter_patient_details.html")


# ==================== CAREGIVER & BOOKING ROUTES ====================

@app.route('/booking')
def booking():
    """
    Caregiver detail page
    Shows detailed information about a specific caregiver
    """
    # caregiver_id = request.args.get('id')
    
    # BACKEND INTEGRATION:
    # caregiver = make_api_request(f'caregivers/{caregiver_id}', method='GET')
    # reviews = make_api_request(f'caregivers/{caregiver_id}/reviews', method='GET')
    
    return render_template('pages/caregiver-detail.html')


@app.route("/book-user")
def book_user():
    """
    Redirect from caregiver detail "Book" button to booking form
    """
    # caregiver_id = request.args.get('id')
    # return redirect(url_for('book_patient', caregiver_id=caregiver_id))
    
    return redirect(url_for('book_patient'))


@app.route("/book-patient", methods=['GET', 'POST'])
# @login_required  # Uncomment in production
def book_patient():
    """
    Book patient form - select patient and time slot
    """
    if request.method == 'POST':
        data = request.get_json()
        
        # BACKEND INTEGRATION:
        # response = make_api_request('bookings', method='POST', data={
        #     'user_id': session.get('user_id'),
        #     'caregiver_id': data.get('caregiver_id'),
        #     'patient_id': data.get('patient_id'),
        #     'booking_date': data.get('date'),
        #     'booking_time': data.get('time'),
        #     'hourly_rate': data.get('hourly_rate')
        # })
        # 
        # if response and response.get('success'):
        #     return jsonify({
        #         'success': True,
        #         'booking_id': response.get('booking_id'),
        #         'redirect': '/appointment'
        #     })
        # 
        # return jsonify({'success': False, 'message': 'Booking failed'}), 400
        
        # For demo:
        return jsonify({'success': True})
    
    # GET: Show booking form
    # BACKEND INTEGRATION:
    # patients = make_api_request(f"users/{session.get('user_id')}/patients", method='GET')
    
    return render_template("pages/book_patient.html")


@app.route('/appointment')
# @login_required  # Uncomment in production
def appointment():
    """
    User's appointments page
    Shows current and upcoming appointments
    """
    # BACKEND INTEGRATION:
    # appointments = make_api_request(f"users/{session.get('user_id')}/appointments", method='GET')
    # current = [a for a in appointments if a['status'] == 'active']
    # upcoming = [a for a in appointments if a['status'] == 'upcoming']
    
    return render_template('pages/appointments.html')


@app.route('/payments')
# @login_required  # Uncomment in production
def payment():
    """
    User's payment history
    """
    # BACKEND INTEGRATION:
    # payments = make_api_request(f"users/{session.get('user_id')}/payments", method='GET')
    
    return render_template('pages/payment.html')


# ==================== OTHER PAGES ====================

@app.route('/dashboard')
# @login_required  # Uncomment in production
def dashboard():
    """
    User dashboard
    """
    # BACKEND INTEGRATION:
    # user = make_api_request(f"users/{session.get('user_id')}", method='GET')
    # stats = make_api_request(f"users/{session.get('user_id')}/stats", method='GET')
    
    return render_template('pages/dashboard.html')


@app.route('/contact')
def contact():
    """
    Contact page
    """
    return render_template('pages/contact.html')


@app.route("/success")
def success():
    """
    Generic success page
    """
    message = request.args.get('message', 'Operation completed successfully!')
    return render_template('pages/login.html', message=message)


# ==================== API ROUTES (for AJAX calls) ====================

@app.route('/api/caregivers/filter', methods=['POST'])
def api_filter_caregivers():
    """
    Filter caregivers based on criteria
    Called via AJAX from homepage
    """
    filters = request.get_json()
    
    # BACKEND INTEGRATION:
    # caregivers = make_api_request('caregivers/filter', method='POST', data=filters)
    # return jsonify(caregivers)
    
    # For demo:
    return jsonify({'success': True, 'caregivers': []})


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('pages/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    return render_template('pages/500.html'), 500


@app.errorhandler(403)
def forbidden(e):
    """Handle 403 errors"""
    flash('You do not have permission to access this page', 'error')
    return redirect(url_for('index'))


# ==================== CONTEXT PROCESSORS ====================

@app.context_processor
def inject_globals():
    """
    Inject global variables into all templates
    Available in all templates without passing explicitly
    """
    return {
        'app_name': 'CareDac',
        'api_url': DJANGO_API_URL,
        'current_user': session.get('user_id'),
        'is_authenticated': session.get('is_authenticated', False),
        'user_email': session.get('user_email', '')
    }


# ==================== BEFORE REQUEST HANDLERS ====================

@app.before_request
def before_request():
    """
    Runs before each request
    Use for session management, logging, etc.
    """
    session.permanent = True
    
    # UNCOMMENT FOR PRODUCTION:
    # # Check if auth token is still valid
    # if 'auth_token' in session and 'user_id' in session:
    #     # Verify token with backend
    #     response = make_api_request('auth/verify-token', method='POST', data={
    #         'token': session['auth_token']
    #     })
    #     
    #     if not response or not response.get('valid'):
    #         # Token expired, clear session
    #         session.clear()
    #         flash('Session expired. Please login again.', 'warning')


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('pages/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    import uuid
    request_id = str(uuid.uuid4())[:8]  # Generate unique error ID
    
    # Log error for debugging
    app.logger.error(f'Server Error: {e}, Request ID: {request_id}')
    
    return render_template('pages/500.html', 
                         error=str(e) if app.debug else None,
                         request_id=request_id), 500


@app.errorhandler(403)
def forbidden(e):
    """Handle 403 errors"""
    flash('You do not have permission to access this page', 'error')
    return redirect(url_for('index'))


@app.errorhandler(400)
def bad_request(e):
    """Handle 400 errors"""
    return render_template('pages/400.html', error=str(e)), 400

# ==================== MAIN ====================

if __name__ == '__main__':
    # Development server
    app.run(
        debug=True,
        port=5000,
        host='0.0.0.0'
    )
    
    # PRODUCTION DEPLOYMENT:
    # Use Gunicorn or uWSGI instead
    # gunicorn -w 4 -b 0.0.0.0:5000 app:app