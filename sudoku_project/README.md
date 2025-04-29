# Sudoku Generator & Solver

A web-based application for generating and solving Sudoku puzzles with different difficulty levels. This application visualizes the solving process step by step, helping users understand how Sudoku-solving algorithms work.

## Features

- Generate Sudoku puzzles with various difficulty levels (Easy, Medium, Hard, Expert)
- Solve puzzles automatically with visualization of the solving steps
- Interactive step-by-step playback of the solving process
- Manual input for user-created puzzles
- Cute cat animation during puzzle generation

## Technologies Used

- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- Algorithms: Backtracking with constraint propagation for solving and generating puzzles

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sudoku.git
cd sudoku
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://127.0.0.1:5001
```

## How to Use

1. Select the desired difficulty level from the dropdown menu
2. Click "Generate" to create a new puzzle
3. Click "Solve" to see the algorithm solve the puzzle step by step
4. Use the step controls to navigate through the solution process
5. Click "Reset" to return to the original puzzle

## License

This project is open source and available under the [MIT License](LICENSE).
