import os
import sys
import json
import random
from functools import wraps
from flask import Flask, request, jsonify, render_template, send_from_directory

# Add backend directory to path so we can import modules if running from root
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.services.auth_service import AuthService
from backend.services.account_service import AccountService
from backend.domain.exceptions import BankError

# Setup paths for Frontend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')
TEMPLATE_DIR = os.path.join(FRONTEND_DIR, 'templates')
STATIC_DIR = os.path.join(FRONTEND_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = "learning-secret-key"

# Services
auth_service = AuthService()
account_service = AccountService()

# --- Helpers ---

def token_required(f):
    """Simple decorator to check for Authorization header (User ID)."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        
        # In a real app, verify signature/expiration. 
        # Here, token IS the user_id.
        try:
            # Simple check if user exists (optional, strictly speaking)
            # We'll just pass the user_id (token) to the route
            request.user_id = token
        except Exception:
            return jsonify({'error': 'Token is invalid!'}), 401
            
        return f(*args, **kwargs)
    return decorated

@app.errorhandler(BankError)
def handle_bank_error(e):
    """Global handler for our custom domain exceptions."""
    return jsonify({"error": str(e)}), 400

@app.errorhandler(Exception)
def handle_generic_error(e):
    """Fallback for unexpected crashes."""
    print(f"Unexpected Error: {e}")
    return jsonify({"error": "Internal Server Error"}), 500

# --- Routes: Pages ---

@app.route('/')
def landing_page():
    return render_template('learn/intro.html')

@app.route('/learn/problem')
def learn_problem():
    return render_template('learn/problem.html')

@app.route('/learn/design')
def learn_design():
    return render_template('learn/design.html')

@app.route('/learn/oop')
def learn_oop():
    return render_template('learn/oop.html')

@app.route('/learn/oop/encapsulation')
def learn_encapsulation():
    return render_template('learn/concepts/encapsulation.html')

@app.route('/learn/oop/inheritance')
def learn_inheritance():
    return render_template('learn/concepts/inheritance.html')

@app.route('/learn/oop/polymorphism')
def learn_polymorphism():
    return render_template('learn/concepts/polymorphism.html')

@app.route('/learn/oop/abstraction')
def learn_abstraction():
    return render_template('learn/concepts/abstraction.html')

@app.route('/learn/interview')
def interview_prep():
    return render_template('learn/interview.html')

@app.route('/learn/interview/preparation')
def interview_preparation():
    return render_template('learn/interview_preparation.html')

@app.route('/learn/interview/assessment')
def interview_assessment():
    return render_template('learn/interview_assessment.html')

@app.route('/learn/revision')
def revision():
    return render_template('learn/revision.html')

@app.route('/app/login')
def login_page():
    return render_template('app/login.html')

@app.route('/app/register')
def register_page():
    return render_template('app/register.html')

@app.route('/app/dashboard')
def dashboard_page():
    return render_template('app/dashboard.html')

# --- Routes: API ---

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    user = auth_service.register(
        username=data.get('username'),
        password=data.get('password'),
        account_type=data.get('account_type')
    )
    return jsonify({"message": "User created", "user_id": user.user_id}), 201

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    user, token = auth_service.login(
        username=data.get('username'),
        password=data.get('password')
    )
    return jsonify({"token": token, "username": user.username}), 200

@app.route('/api/me', methods=['GET'])
@token_required
def api_me():
    # request.user_id comes from @token_required
    summary = account_service.get_user_summary(request.user_id)
    return jsonify(summary), 200

@app.route('/api/deposit', methods=['POST'])
@token_required
def api_deposit():
    amount = request.json.get('amount', 0)
    new_bal = account_service.deposit(request.user_id, int(amount))
    return jsonify({"message": "Deposit successful", "balance": new_bal}), 200

@app.route('/api/withdraw', methods=['POST'])
@token_required
def api_withdraw():
    amount = request.json.get('amount', 0)
    new_bal = account_service.withdraw(request.user_id, int(amount))
    return jsonify({"message": "Withdraw successful", "balance": new_bal}), 200

@app.route('/api/transactions', methods=['GET'])
@token_required
def api_transactions():
    history = account_service.get_history(request.user_id)
    return jsonify({"transactions": history}), 200

# --- Interview & Assessment API ---

@app.route('/api/interview/questions', methods=['GET'])
def api_interview_questions():
    """Get interview preparation questions by difficulty level."""
    difficulty = request.args.get('difficulty', 'easy')
    data_file = os.path.join(BASE_DIR, '..', 'data', 'interview_preparation.json')
    
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
            questions = data.get(difficulty, [])
            return jsonify({"questions": questions, "difficulty": difficulty}), 200
    except FileNotFoundError:
        return jsonify({"error": "Questions file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/assessment/questions', methods=['GET'])
def api_assessment_questions():
    """Get random assessment questions (MCQ format) based on user level."""
    count = int(request.args.get('count', 10))
    level = request.args.get('level', 'beginner')  # interns, beginner, intermediate, expert
    
    data_file = os.path.join(BASE_DIR, '..', 'data', 'assessment_questions.json')
    
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
            all_questions = data.get('questions', [])
            
            # Filter questions based on user level
            if level == 'interns' or level == 'beginner':
                # Mix of easy and medium (70% easy, 30% medium)
                easy_questions = [q for q in all_questions if q.get('difficulty') == 'easy']
                medium_questions = [q for q in all_questions if q.get('difficulty') == 'medium']
                easy_count = int(count * 0.7)
                medium_count = count - easy_count
                selected = random.sample(easy_questions, min(easy_count, len(easy_questions)))
                selected.extend(random.sample(medium_questions, min(medium_count, len(medium_questions))))
            elif level == 'intermediate':
                # Mix of medium and hard (60% medium, 40% hard)
                medium_questions = [q for q in all_questions if q.get('difficulty') == 'medium']
                hard_questions = [q for q in all_questions if q.get('difficulty') == 'hard']
                medium_count = int(count * 0.6)
                hard_count = count - medium_count
                selected = random.sample(medium_questions, min(medium_count, len(medium_questions)))
                selected.extend(random.sample(hard_questions, min(hard_count, len(hard_questions))))
            elif level == 'expert':
                # Mix of hard and expert (50% hard, 50% expert)
                hard_questions = [q for q in all_questions if q.get('difficulty') == 'hard']
                expert_questions = [q for q in all_questions if q.get('difficulty') == 'expert']
                hard_count = int(count * 0.5)
                expert_count = count - hard_count
                selected = random.sample(hard_questions, min(hard_count, len(hard_questions)))
                selected.extend(random.sample(expert_questions, min(expert_count, len(expert_questions))))
            else:
                # Default: random from all
                selected = random.sample(all_questions, min(count, len(all_questions)))
            
            # Shuffle the selected questions
            random.shuffle(selected)
            
            # Remove correct_answer from response (client shouldn't see it)
            for q in selected:
                q.pop('correct_answer', None)
                q.pop('explanation', None)
            
            return jsonify({"questions": selected, "total": len(selected), "level": level}), 200
    except FileNotFoundError:
        return jsonify({"error": "Assessment file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/assessment/submit', methods=['POST'])
def api_assessment_submit():
    """Evaluate assessment answers and return score."""
    answers = request.json.get('answers', {})  # {question_id: selected_option_index}
    
    data_file = os.path.join(BASE_DIR, '..', 'data', 'assessment_questions.json')
    
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
            all_questions = {q['id']: q for q in data.get('questions', [])}
        
        correct = 0
        total = len(answers)
        results = []
        
        for q_id, user_answer in answers.items():
            question = all_questions.get(q_id)
            if not question:
                continue
            
            correct_answer = question.get('correct_answer')
            is_correct = (user_answer == correct_answer)
            
            if is_correct:
                correct += 1
            
            results.append({
                'question_id': q_id,
                'question': question.get('question'),
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': question.get('explanation', ''),
                'difficulty': question.get('difficulty', 'unknown')
            })
        
        score_percentage = (correct / total * 100) if total > 0 else 0
        
        # Determine grade
        if score_percentage >= 90:
            grade = "Excellent"
        elif score_percentage >= 75:
            grade = "Good"
        elif score_percentage >= 60:
            grade = "Average"
        else:
            grade = "Needs Improvement"
        
        return jsonify({
            "score": correct,
            "total": total,
            "percentage": round(score_percentage, 2),
            "grade": grade,
            "results": results
        }), 200
        
    except FileNotFoundError:
        return jsonify({"error": "Assessment file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Bank System...")
    print(f"Serving Frontend from: {FRONTEND_DIR}")
    app.run(debug=True, port=5000)
