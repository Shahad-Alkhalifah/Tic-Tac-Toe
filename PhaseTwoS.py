import tkinter as tk
from tkinter import messagebox
import random

BG = "#E1DCCA"
BTN = "#FABD32"
TEXT = "#1E459F"
X_COLOR = "#CF2A2A"
O_COLOR = "#1E459F"

board = {i: " " for i in range(1, 10)}
player1 = "X"
player2 = "O"
playerTurn = "X"
mode = "1"
startChoice = "1"          
score = {"Player 1": 0, "Player 2": 0, "Computer": 0}

def checkAvailableSpots(pos):
    return board[pos] == " "

def isWin(currentBoard, symbol):
    winLines = [
        (1,2,3),(4,5,6),(7,8,9),
        (1,4,7),(2,5,8),(3,6,9),
        (1,5,9),(3,5,7)
    ]
    for a,b,c in winLines:
        if currentBoard[a] == currentBoard[b] == currentBoard[c] == symbol:
            return True
    return False

def isDraw():
    return all(board[i] != " " for i in board)

def computerMove(symbol):
    # Try to win
    for i in board:
        if checkAvailableSpots(i):
            temp = board.copy()
            temp[i] = symbol
            if isWin(temp, symbol):
                return i

    # Try to block opponent
    opponent = player1 if symbol == player2 else player2
    for i in board:
        if checkAvailableSpots(i):
            temp = board.copy()
            temp[i] = opponent
            if isWin(temp, opponent):
                return i

    # Center
    if checkAvailableSpots(5):
        return 5

    # Corners
    for i in [1,3,7,9]:
        if checkAvailableSpots(i):
            return i

    # Random move
    free = [i for i in board if checkAvailableSpots(i)]
    return random.choice(free)

def updateTurn():
    if playerTurn == player1:
        name = "Player 1"
    else:
        name = "Computer" if mode == "1" else "Player 2"

    turnLabel.config(text=f"{name} ({playerTurn}) Turn")

def updateScore():
    scoreLabel.config(
        text=f"Score: P1: {score['Player 1']}   P2: {score['Player 2']}   Computer: {score['Computer']}"
    )

def click(pos):
    global playerTurn

    if not checkAvailableSpots(pos):
        return

    board[pos] = playerTurn

    if playerTurn == "X":
        buttons[pos].config(text="X", fg=X_COLOR)
    else:
        buttons[pos].config(text="O", fg=O_COLOR)

    if isWin(board, playerTurn):
        if playerTurn == player1:
            winner = "Player 1"
        else:
            winner = "Computer" if mode == "1" else "Player 2"

        score[winner] += 1
        updateScore()

        messagebox.showinfo("Result", f"{winner} wins!")
        playAgain()
        return

    if isDraw():
        messagebox.showinfo("Result", "It is a Draw!")
        playAgain()
        return

    playerTurn = player2 if playerTurn == player1 else player1
    updateTurn()

    if mode == "1" and playerTurn == player2:
        move = computerMove(player2)
        click(move)

def playAgain():
    answer = messagebox.askyesno("Play Again", "Play again?")
    if answer:
        resetGame()
    else:
        root.destroy()

def resetGame():
    global board, playerTurn
    board = {i: " " for i in range(1, 10)}
    playerTurn = player1 if startChoice == "1" else player2

    for i in buttons:
        buttons[i].config(text=" ", fg=TEXT)

    updateTurn()

    if mode == "1" and playerTurn == player2:
        move = computerMove(player2)
        click(move)

def startGame():
    global player1, player2, playerTurn, mode, startChoice

    mode = modeVar.get()
    player1 = symbolVar.get()
    player2 = "O" if player1 == "X" else "X"
    startChoice = startVar.get()       

    playerTurn = player1 if startChoice == "1" else player2
    updateTurn()

    for w in options:
        w.config(state="disabled")

    startBtn.config(state="disabled")

    if mode == "1" and playerTurn == player2:
        move = computerMove(player2)
        click(move)

root = tk.Tk()
root.title("Tic-Tac-Toe")
root.configure(bg=BG)

modeVar = tk.StringVar(value="1")
symbolVar = tk.StringVar(value="X")
startVar = tk.StringVar(value="1")

options = []

def addOption(widget):
    options.append(widget)
    return widget

tk.Label(root, text="Play With", bg=BG, fg=TEXT, font=("Arial", 11, "bold")).grid(row=0, column=0)
addOption(tk.Radiobutton(root, text="Computer", variable=modeVar, value="1", bg=BG)).grid(row=0, column=1)
addOption(tk.Radiobutton(root, text="Player 2", variable=modeVar, value="2", bg=BG)).grid(row=0, column=2)

tk.Label(root, text="Select", bg=BG, fg=TEXT, font=("Arial", 11, "bold")).grid(row=1, column=0)
addOption(tk.Radiobutton(root, text="X", variable=symbolVar, value="X", bg=BG)).grid(row=1, column=1)
addOption(tk.Radiobutton(root, text="O", variable=symbolVar, value="O", bg=BG)).grid(row=1, column=2)

tk.Label(root, text="Start First", bg=BG, fg=TEXT, font=("Arial", 11, "bold")).grid(row=2, column=0)
addOption(tk.Radiobutton(root, text="Yes", variable=startVar, value="1", bg=BG)).grid(row=2, column=1)
addOption(tk.Radiobutton(root, text="No", variable=startVar, value="2", bg=BG)).grid(row=2, column=2)

startBtn = tk.Button(root, text="Start", command=startGame, bg=BTN, font=("Arial", 11, "bold"))
startBtn.grid(row=3, column=1)

turnLabel = tk.Label(root, text="", bg=BG, fg=TEXT, font=("Arial", 14, "bold"))
turnLabel.grid(row=4, column=0, columnspan=3)

scoreLabel = tk.Label(root, text="Score: P1: 0   P2: 0   Computer: 0", bg=BG, fg=TEXT, font=("Arial", 12))
scoreLabel.grid(row=5, column=0, columnspan=3)

buttons = {}
for i in range(1, 10):
    btn = tk.Button(
        root,
        text=" ",
        width=6,
        height=2,
        bg=BTN,
        font=("Arial", 18, "bold"),
        relief="ridge",
        bd=3,
        command=lambda i=i: click(i)
    )
    btn.grid(row=6 + (i-1)//3, column=(i-1)%3, padx=5, pady=5)
    buttons[i] = btn

root.mainloop() 