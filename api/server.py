from flask import Flask, render_template, request, jsonify
import os
import sys
import importlib.util

# Ensure we're in the right directory
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)

# Add the root and api directories to Python path
sys.path.insert(0, root_dir)
sys.path.insert(0, current_dir)

# Function to check if a module exists
def module_exists(module_name):
    try:
        importlib.util.find_spec(module_name)
        return True
    except ImportError:
        return False

# First try to import from the local directory
if module_exists("sudoku.grid"):
    from sudoku.grid import SudokuGrid
    from sudoku.solver import solve
    from sudoku.generator import generate_easy, generate_medium, generate_hard, generate_expert
# Then try from the root directory
elif module_exists("api.sudoku.grid"):
    from api.sudoku.grid import SudokuGrid
    from api.sudoku.solver import solve
    from api.sudoku.generator import generate_easy, generate_medium, generate_hard, generate_expert
else:
    raise ImportError("Could not find the sudoku module.")

app = Flask(__name__)

# Configure static and template folders
template_dir = os.path.join(root_dir, 'templates')
static_dir = os.path.join(root_dir, 'static')

if os.path.exists(template_dir):
    app.template_folder = template_dir
else:
    # Try the api subdirectory
    template_dir = os.path.join(current_dir, 'templates')
    if os.path.exists(template_dir):
        app.template_folder = template_dir

if os.path.exists(static_dir):
    app.static_folder = static_dir
else:
    # Try the api subdirectory
    static_dir = os.path.join(current_dir, 'static')
    if os.path.exists(static_dir):
        app.static_folder = static_dir

# CORS support
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    """Generate a new Sudoku puzzle"""
    difficulty = 'medium'  # Default difficulty
    
    if request.method == 'POST':
        # Handle both application/json and form-urlencoded content types
        if request.content_type and 'application/json' in request.content_type:
            data = request.get_json()
            difficulty = data.get('difficulty', 'medium') if data else 'medium'
        else:
            # Handle form data or urlencoded data
            difficulty = request.form.get('difficulty', 'medium')
    else:
        # Handle GET requests
        difficulty = request.args.get('difficulty', 'medium')
    
    # Map difficulty to the appropriate generator function
    generator_map = {
        'easy': generate_easy,
        'medium': generate_medium,
        'hard': generate_hard,
        'expert': generate_expert
    }
    
    # If expert difficulty is too hard for the server, automatically
    # fall back to hard difficulty
    generator_func = generator_map.get(difficulty, generate_medium)
    
    try:
        puzzle_grid, solution_grid = generator_func()  # Get both puzzle and solution
        
        return jsonify({
            'puzzle': puzzle_grid.board,
            'solution': solution_grid.board,
            'difficulty': difficulty
        })
    except Exception as e:
        print(f"Error generating puzzle: {str(e)}")
        # Fall back to hard difficulty if expert fails
        if difficulty == 'expert':
            try:
                print("Expert generation failed, falling back to hard difficulty")
                puzzle_grid, solution_grid = generate_hard()
                return jsonify({
                    'puzzle': puzzle_grid.board,
                    'solution': solution_grid.board,
                    'difficulty': 'hard',
                    'message': 'Expert generation failed, falling back to hard difficulty'
                })
            except Exception as e2:
                print(f"Fallback generation also failed: {str(e2)}")
                return jsonify({'error': 'Failed to generate puzzle'}), 500
        else:
            return jsonify({'error': 'Failed to generate puzzle'}), 500

@app.route('/solve', methods=['POST', 'OPTIONS'])
def solve_puzzle():
    """Solve a Sudoku puzzle"""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json()
    board = data.get('board')
    show_steps = data.get('show_steps', False)
    
    if not board:
        return jsonify({'error': 'No board provided'}), 400
    
    try:
        grid = SudokuGrid(board)
        if show_steps:
            success, steps = solve(grid, record_steps=True)
            
            if success:
                # Format the response with steps and progress information
                solution_steps = []
                for i, step in enumerate(steps):
                    # Ensure there's an explanation
                    if 'explanation' not in step:
                        if i == 0:
                            explanation = "Starting to solve the puzzle."
                        else:
                            explanation = f"Placed {step['value']} at position ({step['position'][0]+1}, {step['position'][1]+1})."
                    else:
                        explanation = step.get('explanation', 'No explanation')
                    
                    # Ensure there's backtrack information
                    backtrack = step.get('backtrack', False)
                    
                    solution_steps.append({
                        'board': step['board'],
                        'position': step['position'],
                        'value': step['value'],
                        'step_number': i + 1,
                        'total_steps': len(steps),
                        'progress': step['progress'],
                        'explanation': explanation,
                        'backtrack': backtrack
                    })
                
                return jsonify({
                    'solved': True,
                    'board': grid.board,
                    'steps': solution_steps
                })
            else:
                return jsonify({
                    'solved': False,
                    'error': 'No solution exists'
                })
        else:
            success = solve(grid)
            return jsonify({
                'solved': success,
                'board': grid.board if success else None
            })
    except Exception as e:
        print(f"Error solving puzzle: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Vercel requires a direct export
app.debug = False

# For local testing
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', debug=True, port=port) 