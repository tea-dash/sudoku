from flask import Flask, render_template, request, jsonify
from sudoku.grid import SudokuGrid
from sudoku.solver import solve
from sudoku.generator import generate_easy, generate_medium, generate_hard, generate_expert
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

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

@app.route('/solve', methods=['POST'])
def solve_puzzle():
    """Solve a Sudoku puzzle"""
    data = request.get_json()
    board = data.get('board')
    show_steps = data.get('show_steps', False)
    
    logging.debug(f"Received solve request with show_steps={show_steps}")
    
    if not board:
        return jsonify({'error': 'No board provided'}), 400
    
    try:
        grid = SudokuGrid(board)
        if show_steps:
            success, steps = solve(grid, record_steps=True)
            logging.debug(f"Solve completed with success={success}, steps count={len(steps) if steps else 0}")
            
            if success:
                # Format the response with steps and progress information
                solution_steps = []
                for i, step in enumerate(steps):
                    explanation = step.get('explanation', 'No explanation')
                    app.logger.debug(f"Step {i} explanation: {explanation}")
                    
                    solution_steps.append({
                        'board': step['board'],
                        'position': step['position'],
                        'value': step['value'],
                        'step_number': i + 1,
                        'total_steps': len(steps),
                        'progress': step['progress'],
                        'explanation': explanation
                    })
                
                if solution_steps:
                    app.logger.debug(f"First step explanation: {solution_steps[0]['explanation']}")
                    app.logger.debug(f"Last step explanation: {solution_steps[-1]['explanation']}")
                
                response_data = {
                    'solved': True,
                    'board': grid.board,
                    'steps': solution_steps
                }
                
                # Log response size
                import json
                response_size = len(json.dumps(response_data))
                app.logger.debug(f"Response size: {response_size} bytes")
                
                return jsonify(response_data)
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
        logging.exception("Error solving puzzle")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 