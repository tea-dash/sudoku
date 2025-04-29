import argparse
import os
import time
from sudoku.grid import SudokuGrid
from sudoku.solver import solve
from sudoku.generator import generate, generate_easy, generate_medium, generate_hard, generate_expert

def print_board(board, highlight_pos=None):
    """
    Print the Sudoku board with formatting.
    
    Args:
        board: 9x9 list of integers representing the board
        highlight_pos: Optional tuple (r, c) of position to highlight
    """
    print("┌───────┬───────┬───────┐")
    for r in range(9):
        print("│", end=" ")
        for c in range(9):
            val = str(board[r][c]) if board[r][c] != 0 else "."
            
            # Highlight the position if specified
            if highlight_pos and (r, c) == highlight_pos:
                print(f"\033[1m{val}\033[0m", end=" ")
            else:
                print(val, end=" ")
                
            if c % 3 == 2 and c < 8:  # Add vertical separator
                print("│", end=" ")
        print("│")
        
        # Add horizontal separator
        if r % 3 == 2 and r < 8:
            print("├───────┼───────┼───────┤")
    print("└───────┴───────┴───────┘")

def load_board_from_file(filename):
    """
    Load a Sudoku board from a file.
    The file should contain 9 lines with 9 numbers each.
    0 or . can be used for empty cells.
    """
    board = []
    with open(filename, 'r') as f:
        for line in f:
            # Clean the line and replace . with 0
            line = line.strip().replace(".", "0")
            # Split by any whitespace and convert to integers
            row = [int(c) for c in line.split()]
            if len(row) != 9:
                raise ValueError(f"Invalid row length: {len(row)} (expected 9)")
            board.append(row)
    
    if len(board) != 9:
        raise ValueError(f"Invalid number of rows: {len(board)} (expected 9)")
        
    return board

def save_board_to_file(board, filename):
    """
    Save a Sudoku board to a file.
    """
    with open(filename, 'w') as f:
        for row in board:
            f.write(" ".join(str(n) if n != 0 else "." for n in row) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Sudoku Puzzle Generator & Solver")
    
    # Generator options
    generator_group = parser.add_argument_group("Generator Options")
    generator_group.add_argument("--new", action="store_true", help="Generate a new puzzle")
    generator_group.add_argument("--difficulty", choices=["easy", "medium", "hard", "expert"],
                             default="medium", help="Difficulty level for generated puzzle")
    generator_group.add_argument("--clues", type=int, help="Custom number of clues (17-81)")
    generator_group.add_argument("--save", type=str, help="Save generated puzzle to file")
    
    # Solver options
    solver_group = parser.add_argument_group("Solver Options")
    solver_group.add_argument("--solve", type=str, help="Solve a puzzle from file")
    solver_group.add_argument("--output", type=str, help="Save solution to file")
    solver_group.add_argument("--stats", action="store_true", help="Show solving statistics")

    args = parser.parse_args()
    
    # Handle puzzle generation
    if args.new:
        # Generate puzzle based on difficulty
        clues = args.clues
        if clues and (clues < 17 or clues > 81):
            print("Error: Number of clues must be between 17 and 81")
            return
        
        print(f"Generating {args.difficulty} puzzle...")
        start_time = time.time()
        
        if args.difficulty == "easy":
            grid, solution = generate_easy(clues=clues or 40)
        elif args.difficulty == "medium":
            grid, solution = generate_medium(clues=clues or 30)
        elif args.difficulty == "hard":
            grid, solution = generate_hard(clues=clues or 25)
        elif args.difficulty == "expert":
            grid, solution = generate_expert(clues=clues or 20)
            
        end_time = time.time()
        
        if args.stats:
            print(f"Generation time: {end_time - start_time:.2f} seconds")
            actual_clues = sum(1 for r in range(9) for c in range(9) if grid.board[r][c] != 0)
            print(f"Clues: {actual_clues}")
        
        print("\nPuzzle:")
        print_board(grid.board)
        
        # Save puzzle if requested
        if args.save:
            save_board_to_file(grid.board, args.save)
            print(f"Puzzle saved to {args.save}")
        
    # Handle puzzle solving
    elif args.solve:
        try:
            board = load_board_from_file(args.solve)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading puzzle: {e}")
            return
            
        grid = SudokuGrid(board)
        
        print("Puzzle to solve:")
        print_board(grid.board)
        
        print("\nSolving...")
        start_time = time.time()
        solved = solve(grid)
        end_time = time.time()
        
        if solved:
            print("\nSolution:")
            print_board(grid.board)
            
            if args.stats:
                print(f"Solving time: {end_time - start_time:.4f} seconds")
                
            # Save solution if requested
            if args.output:
                save_board_to_file(grid.board, args.output)
                print(f"Solution saved to {args.output}")
        else:
            print("No solution found. The puzzle may be invalid.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
