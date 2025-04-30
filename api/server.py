from flask import Flask, render_template, request, jsonify
import os
import sys

# Add the root directory to path so we can import the sudoku module
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

# Import our modules
from sudoku.grid import SudokuGrid
from sudoku.solver import solve
from sudoku.generator import generate_easy, generate_medium, generate_hard, generate_expert

app = Flask(__name__, 
            template_folder=os.path.join(root_dir, 'templates'),
            static_folder=os.path.join(root_dir, 'static'))

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
    if request.method == 'POST':
        difficulty = request.get_json().get('difficulty', 'medium')
    else:
        difficulty = request.args.get('difficulty', 'medium')
    
    # Map difficulty to the appropriate generator function
    generator_map = {
        'easy': generate_easy,
        'medium': generate_medium,
        'hard': generate_hard,
        'expert': generate_expert
    }
    
    generator_func = generator_map.get(difficulty, generate_medium)
    puzzle_grid, solution_grid = generator_func()  # Get both puzzle and solution
    
    return jsonify({
        'puzzle': puzzle_grid.board,
        'solution': solution_grid.board,
        'difficulty': difficulty
    })

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
                    explanation = step.get('explanation', 'No explanation')
                    
                    solution_steps.append({
                        'board': step['board'],
                        'position': step['position'],
                        'value': step['value'],
                        'step_number': i + 1,
                        'total_steps': len(steps),
                        'progress': step['progress'],
                        'explanation': explanation
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

# For running locally
if __name__ == '__main__':
    app.run(debug=True, port=5001) 