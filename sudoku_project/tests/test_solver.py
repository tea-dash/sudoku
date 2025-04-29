import pytest
from sudoku.grid import SudokuGrid
from sudoku.solver import solve, count_solutions

def test_solve_empty_grid():
    """Test solving a completely empty grid."""
    grid = SudokuGrid()
    assert solve(grid)
    
    # Check if solution is valid
    for r in range(9):
        for c in range(9):
            assert grid.board[r][c] != 0  # No empty cells
            
    # Check each row contains numbers 1-9
    for r in range(9):
        assert set(grid.board[r]) == set(range(1, 10))
    
    # Check each column contains numbers 1-9
    for c in range(9):
        assert set(grid.board[r][c] for r in range(9)) == set(range(1, 10))
    
    # Check each 3x3 box contains numbers 1-9
    for box_r in range(0, 9, 3):
        for box_c in range(0, 9, 3):
            box_vals = [grid.board[r][c] for r in range(box_r, box_r + 3) 
                                        for c in range(box_c, box_c + 3)]
            assert set(box_vals) == set(range(1, 10))

def test_solve_easy_puzzle():
    """Test solving an easy puzzle."""
    # Example easy puzzle with a unique solution
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    grid = SudokuGrid(board)
    assert solve(grid)
    
    # Known solution for this puzzle
    expected = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]
    
    assert grid.board == expected

def test_solve_impossible_puzzle():
    """Test solving an impossible puzzle."""
    # Puzzle with contradictions (same number twice in a row)
    board = [
        [1, 1, 0, 0, 0, 0, 0, 0, 0],  # 1 appears twice in first row
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    grid = SudokuGrid(board)
    assert not solve(grid)

def test_count_solutions():
    """Test counting solutions for puzzles."""
    # A puzzle with a unique solution
    unique_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    unique_grid = SudokuGrid(unique_board)
    assert count_solutions(unique_grid) == 1
    
    # A very sparse grid should have multiple solutions
    sparse_board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    sparse_grid = SudokuGrid(sparse_board)
    # There should be at least 2 solutions (our function stops at limit=2)
    assert count_solutions(sparse_grid) >= 2
