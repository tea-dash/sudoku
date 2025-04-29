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

@app.route('/generate', methods=['POST'])
def generate_puzzle():
    difficulty = request.form.get('difficulty', 'medium')
    
    if difficulty == 'easy':
        grid, solution = generate_easy()
    elif difficulty == 'medium':
        grid, solution = generate_medium()
    elif difficulty == 'hard':
        grid, solution = generate_hard()
    else:  # expert
        grid, solution = generate_expert()
    
    return jsonify({
        'puzzle': [row[:] for row in grid.board],
        'solution': [row[:] for row in solution.board]
    })

@app.route('/solve', methods=['POST'])
def solve_puzzle():
    data = request.json
    board = data.get('board')
    show_steps = data.get('show_steps', False)
    
    app.logger.debug(f"Received board to solve: {len(board)} x {len(board[0])} grid")
    app.logger.debug(f"Show steps: {show_steps}")
    
    grid = SudokuGrid(board)
    
    if show_steps:
        app.logger.debug("Solving with steps recording enabled")
        solved, steps = solve(grid, record_steps=True)
        app.logger.debug(f"Solver returned {len(steps)} steps")
        
        # Ensure steps have the right format
        for step in steps[:3]:  # Log first few steps for debugging
            app.logger.debug(f"Step: {step.keys()}")
        
        return jsonify({
            'solved': solved,
            'board': [row[:] for row in grid.board],
            'steps': steps
        })
    else:
        solved = solve(grid)
        return jsonify({
            'solved': solved,
            'board': [row[:] for row in grid.board]
        })

if __name__ == '__main__':
    app.run(debug=True, port=5001) 