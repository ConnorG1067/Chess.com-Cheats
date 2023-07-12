import chess
import chess.svg
import chess.engine
import time
from stockfish import Stockfish
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import cv2
import random
driver = webdriver.Chrome()

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    usernameField = driver.find_element(By.XPATH , "//*[@id=\"username\"]")
    passwordField = driver.find_element(By.XPATH , "//*[@id=\"password\"]")


    loginBtn = driver.find_element(By.XPATH , "//*[@id=\"login\"]")


    usernameField.send_keys(username)
    passwordField.send_keys(password)

    loginBtn.click()

    
def playGame():
    playGameBtn = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[1]/div/a[2]')
    playGameBtn.click()
    confirmPlayBtn = driver.find_element(By.XPATH, '//*[@id="board-layout-sidebar"]/div/div[2]/div/div[1]/div[1]/button')
    confirmPlayBtn.click()

def readMoves():
    isWhiteInput = input("Is White (y/n)")
    isWhiteBool = True if isWhiteInput == 'y' else False
    stockfish = Stockfish('stockfish-windows-2022-x86-64-avx2.exe')
    isGameOver = False
    previousFen = ""
    # Run while the game is not over
    while not isGameOver:
        # Set fen
        fen = driver.execute_script("return document.getElementsByTagName('chess-board')[0].game.getFEN()")
        board = chess.Board(fen)
        isGameOver = board.is_checkmate() or board.is_stalemate() or board.outcome() or board.can_claim_draw() or board.can_claim_threefold_repetition() or board.can_claim_fifty_moves() or board.is_insufficient_material() or board.is_fivefold_repetition() or board.is_seventyfive_moves()
        turnInt = 1 if isWhiteBool else 0
        currentTurnInt = driver.execute_script("return document.getElementsByTagName('chess-board')[0].game.getTurn();")
        if(fen != previousFen and currentTurnInt%2 == turnInt):
            waitTime = random.randint(1, 6)
            time.sleep(waitTime)
            # Set stockfish to view the current board position
            stockfish.set_fen_position(board.fen())
            # Preform the best possible move
            stockFishBestMove = stockfish.get_best_move()
            # Get legal moves
            legalMoves = driver.execute_script("return document.getElementsByTagName('chess-board')[0].game.getLegalMoves();")
            # get the index of the legal move
            indexOfStockFish = findLegalStockFishMove(legalMoves, stockFishBestMove)
            # Run the best move
            driver.execute_script("var move = document.getElementsByTagName('chess-board')[0].game.getLegalMoves()[" + str(indexOfStockFish) + "];document.getElementsByTagName('chess-board')[0].game.move({...move,promotion: 'false',animate: false,userGenerated: true});")
            #Check if the game is over
            isGameOver = board.is_checkmate() or board.is_stalemate() or board.outcome() or board.can_claim_draw() or board.can_claim_threefold_repetition() or board.can_claim_fifty_moves() or board.is_insufficient_material() or board.is_fivefold_repetition() or board.is_seventyfive_moves()
        # Set the previous Fen to the current Fen
        previousFen = fen

    rematch()

def findLegalStockFishMove(legalMoves, stockFishBestMove):
    toFromList = [stockFishBestMove[i:i+2] for i in range(0, len(stockFishBestMove), 2)]
    for x in range (len(legalMoves)):
        if(legalMoves[x]['from'] == toFromList[0] and legalMoves[x]['to'] == toFromList[1]):
            return x


def launchChess():
    driver.get("https://www.chess.com/login_and_go?returnUrl=https://www.chess.com/")
    login()
    time.sleep(3)
    playGame()
    time.sleep(10)
    readMoves()
    

def rematch():
    rematch = input("Rematch (y/n)?")
    if(rematch == 'y'):
        newGameBtn = driver.find_element(By.XPATH, '//*[@id="board-layout-sidebar"]/div/div[2]/div[4]/button[1]')
        newGameBtn.click()
        readMoves()
    else:
        exit()
    

driver = launchChess()