import streamlit as st
import time

# Page configuration
st.set_page_config(
    page_title="🎮 Tic Tac Toe Pro",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #e94560;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        text-align: center;
        color: #f39c12;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .score-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .score-item {
        text-align: center;
        margin: 0 1rem;
    }
    
    .score-label {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .score-value {
        font-size: 2rem;
        font-weight: bold;
    }
    
    .player-x {
        color: #e94560;
    }
    
    .player-o {
        color: #f39c12;
    }
    
    .draw-color {
        color: #27ae60;
    }
    
    .game-status {
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        background: linear-gradient(135deg, #0f3460 0%, #533483 100%);
    }
    
    .winner-status {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .board-container {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
        padding: 20px;
        background: linear-gradient(135deg, #0f3460 0%, #533483 100%);
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4);
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .game-board {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 4px;
        background: #1a1a2e;
        padding: 8px;
        border-radius: 15px;
        width: 100%;
    }
    
    .stButton > button {
        width: 120px !important;
        height: 120px !important;
        font-size: 4rem !important;
        border-radius: 8px !important;
        border: none !important;
        background: linear-gradient(135deg, #16213e 0%, #0f3460 100%) !important;
        color: white !important;
        transition: all 0.2s ease !important;
        margin: 0 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        background: linear-gradient(135deg, #533483 0%, #0f3460 100%) !important;
        box-shadow: 0 8px 25px rgba(83, 52, 131, 0.6) !important;
    }
    
    .stButton > button:active {
        transform: scale(0.95) !important;
    }
    
    .stButton > button:disabled {
        opacity: 1 !important;
        cursor: default !important;
    }
    
    .winning-cell {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%) !important;
        animation: glow 1.5s ease-in-out infinite alternate !important;
    }
    
    @keyframes glow {
        from { box-shadow: 0 4px 15px rgba(39, 174, 96, 0.4) !important; }
        to { box-shadow: 0 8px 30px rgba(39, 174, 96, 0.8) !important; }
    }
    
    .control-buttons {
        text-align: center;
        margin: 2rem 0;
    }
    
    .new-game-btn {
        background: linear-gradient(135deg, #0f3460 0%, #533483 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        margin: 0 0.5rem !important;
    }
    
    .reset-btn {
        background: linear-gradient(135deg, #e94560 0%, #c0392b 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        margin: 0 0.5rem !important;
    }
    
    .celebration {
        text-align: center;
        font-size: 4rem;
        animation: bounce 1s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-30px); }
        60% { transform: translateY(-15px); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = [['', '', ''], ['', '', ''], ['', '', '']]
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.scores = {'X': 0, 'O': 0, 'Draw': 0}
    st.session_state.winning_line = []
    st.session_state.show_celebration = False
    st.session_state.auto_reset_time = None

def check_winner():
    board = st.session_state.board
    
    # Check rows
    for i, row in enumerate(board):
        if row[0] == row[1] == row[2] != '':
            st.session_state.winning_line = [(i, 0), (i, 1), (i, 2)]
            return row[0]
    
    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != '':
            st.session_state.winning_line = [(0, j), (1, j), (2, j)]
            return board[0][j]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        st.session_state.winning_line = [(0, 0), (1, 1), (2, 2)]
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        st.session_state.winning_line = [(0, 2), (1, 1), (2, 0)]
        return board[0][2]
    
    return None

def check_draw():
    for row in st.session_state.board:
        if '' in row:
            return False
    return True

def make_move(row, col):
    if st.session_state.board[row][col] == '' and not st.session_state.game_over:
        st.session_state.board[row][col] = st.session_state.current_player
        
        winner = check_winner()
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
            st.session_state.scores[winner] += 1
            st.session_state.show_celebration = True
            st.session_state.auto_reset_time = time.time() + 3
        elif check_draw():
            st.session_state.game_over = True
            st.session_state.winner = 'Draw'
            st.session_state.scores['Draw'] += 1
            st.session_state.show_celebration = True
            st.session_state.auto_reset_time = time.time() + 3
        else:
            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'

def new_game():
    st.session_state.board = [['', '', ''], ['', '', ''], ['', '', '']]
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.winning_line = []
    st.session_state.show_celebration = False
    st.session_state.auto_reset_time = None

def reset_scores():
    st.session_state.scores = {'X': 0, 'O': 0, 'Draw': 0}
    new_game()

# Auto-reset functionality
if (st.session_state.auto_reset_time and 
    time.time() > st.session_state.auto_reset_time and 
    st.session_state.game_over):
    new_game()
    st.rerun()

# Main UI
st.markdown('<h1 class="main-header">🎮 TIC TAC TOE PRO</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Modern Gaming Experience</p>', unsafe_allow_html=True)

# Scoreboard
st.markdown('<div class="score-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'''
    <div class="score-item">
        <div class="score-label player-x">❌ Player X</div>
        <div class="score-value player-x">{st.session_state.scores["X"]}</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''
    <div class="score-item">
        <div class="score-label draw-color">🤝 Draws</div>
        <div class="score-value draw-color">{st.session_state.scores["Draw"]}</div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown(f'''
    <div class="score-item">
        <div class="score-label player-o">⭕ Player O</div>
        <div class="score-value player-o">{st.session_state.scores["O"]}</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Game status
if st.session_state.show_celebration and st.session_state.winner:
    if st.session_state.winner == 'Draw':
        st.markdown('<div class="celebration">🤝</div>', unsafe_allow_html=True)
        st.markdown('<div class="game-status winner-status">🤝 It\'s a Draw!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="celebration">🎉</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="game-status winner-status">🎉 Player {st.session_state.winner} Wins!</div>', unsafe_allow_html=True)
    
    # Show countdown
    if st.session_state.auto_reset_time:
        remaining = max(0, int(st.session_state.auto_reset_time - time.time()))
        if remaining > 0:
            st.markdown(f'<p style="text-align: center; font-size: 1.2rem; color: #f39c12;">New game starting in {remaining} seconds...</p>', unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()
elif st.session_state.game_over:
    st.markdown('<div class="game-status winner-status">Game Over</div>', unsafe_allow_html=True)
else:
    player_color = "player-x" if st.session_state.current_player == 'X' else "player-o"
    st.markdown(f'<div class="game-status"><span class="{player_color}">🎯 Player {st.session_state.current_player}\'s Turn</span></div>', unsafe_allow_html=True)

# Game board
st.markdown('<div class="board-container"><div class="game-board">', unsafe_allow_html=True)

# Create a 3x3 grid using columns
board_cols = st.columns(3)
for i in range(3):
    for j in range(3):
        with board_cols[j]:
            cell_content = st.session_state.board[i][j]
            
            # Determine button display
            if cell_content == 'X':
                display_text = '❌'
            elif cell_content == 'O':
                display_text = '⭕'
            else:
                display_text = ''
            
            # Check if this cell is part of winning line
            is_winning_cell = (i, j) in st.session_state.winning_line
            
            # Create button with winning cell styling
            button_key = f"cell_{i}_{j}"
            if st.button(display_text, key=button_key, 
                        disabled=st.session_state.game_over or cell_content != '',
                        help=f"Row {i+1}, Column {j+1}",
                        use_container_width=True):
                make_move(i, j)
                st.rerun()

st.markdown('</div></div>', unsafe_allow_html=True)

# Control buttons
st.markdown('<div class="control-buttons">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🔄 New Game", key="new_game", help="Start a new game"):
        new_game()
        st.rerun()

with col2:
    st.write("")  # Spacer

with col3:
    if st.button("🗑️ Reset Scores", key="reset_scores", help="Reset all scores"):
        reset_scores()
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Instructions
with st.expander("📖 How to Play"):
    st.markdown("""
    **🎯 Objective:** Get three of your symbols (❌ or ⭕) in a row, column, or diagonal.
    
    **🎮 How to Play:**
    1. Player ❌ goes first
    2. Click on any empty cell to place your symbol
    3. Players alternate turns
    4. First to get 3 in a row wins!
    5. If all cells are filled without a winner, it's a draw
    
    **✨ Features:**
    - 🏆 Score tracking across multiple games
    - 🔄 Automatic new game after 3 seconds
    - 🎊 Winning animations and celebrations
    - 📱 Responsive design for all devices
    """)

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #f39c12; font-size: 1rem; font-weight: bold; margin-top: 10px;">Built by Mohammad Kasim</p>', 
    unsafe_allow_html=True
)

st.markdown(
    '<p style="text-align: center; color: #888; font-size: 0.9rem;">Enjoy your game!</p>', 
    unsafe_allow_html=True
)
