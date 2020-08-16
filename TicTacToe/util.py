import time
import json
import requests
import matplotlib.pyplot as plt

# ⚠ If hosting the server locally, change this to your server's address ⚠
# Ex:
# SERVER_URL = 'http://127.0.0.1:5000'
SERVER_URL = 'https://ryans-ttt.herokuapp.com'


def checkWin(cells):
    c = cells
    # Getting a slice of all 3s
    tr = c[0]  # Top Row
    mr = c[1]  # Middle Row
    br = c[2]  # Bottom Row
    lc = [c[i][0] for i in range(3)]  # Left Column
    mc = [c[i][1] for i in range(3)]  # Middle Column
    rc = [c[i][2] for i in range(3)]  # Right Column
    d1 = [c[i][i] for i in range(3)]  # Diagonal \
    d2 = [c[2 - i][i] for i in range(3)]  # Diagonal /

    draw = True
    for line in [tr, mr, br, lc, mc, rc, d1, d2]:
        if line[0] != 0 and line[0] == line[1] == line[2]: return line[0]  # 1 or 2 has Won
        if 0 in line: draw = False
    if draw: return 0  # All cells filled
    return None  # Game is still inconclusive


def getFormattedCells(cells, key=None):
    f = cells
    formattedCells = (
        f'{f[0][0]}|{f[0][1]}|{f[0][2]}\n'
        f'{f[1][0]}|{f[1][1]}|{f[1][2]}\n'
        f'{f[2][0]}|{f[2][1]}|{f[2][2]}\n'
    )

    if key is not None:
        for k, v in key.items():
            formattedCells = formattedCells.replace(str(k), str(v))

    return formattedCells


def getAllPossibleMoves(cells):
    return [(i // 3, i % 3) for i in range(9) if cells[i // 3][i % 3] == 0]


def checkIsWanted(d):
    return 'Player' == d['player1'] and ('AIPlayer' == d['player2'] or 'RandomAIPlayer' == d['player2'])


def saveData(gameData):
    if checkIsWanted(gameData):
        try:
            res = requests.post(f'{SERVER_URL}/score', json=gameData)
            if res.status_code != 201:
                return print(f'Could not save data to the Cloud!\n'
                             f'Error code: {res.status_code}\n'
                             f'Error message: {res.text}')
        except Exception as e:
            print(f'Error saving data to the Cloud: {e.__class__.__name__}: {e}')


def analyzeData(name, gameDataList):
    AIData = {
        'games': 0,
        'draws': 0,
        'AIWins': 0,
        'movesPerGame': 0,
        'percentageWin': 0,
        'pie': {
            'labels': ['Wins', 'Draws', 'Losses'],
            'data': [0, 0, 0],
        }
    }

    for game in gameDataList:
        AIData['games'] += 1
        AIData['movesPerGame'] += game['moves']
        if game['draw']: AIData['draws'] += 1
        if game['win'] and game['winner'] == name: AIData['AIWins'] += 1

    if AIData['games'] == 0: return AIData

    AIData['movesPerGame'] //= AIData['games']
    AIData['percentageWin'] = f"{AIData['AIWins'] / AIData['games']:.2f}"
    AIData['pie']['data'] = [AIData['AIWins'], AIData['draws'], AIData['games'] - AIData['AIWins'] - AIData['draws']]
    return AIData


def displayData():
    res = requests.get(f'{SERVER_URL}/score')
    if res.status_code != 200: return print(f"Server down! Could not retrieve data! Error code: {res.status_code}")
    data = res.json()

    playerVsAIData = list(filter(checkIsWanted, data))
    randomAIGames = list(filter(lambda x: x['player2'] == 'RandomAIPlayer', playerVsAIData))
    MinmaxAIGames = list(filter(lambda x: x['player2'] == 'AIPlayer', playerVsAIData))

    randomAIData = analyzeData('RandomAIPlayer', randomAIGames)
    minmaxAIData = analyzeData('AIPlayer', MinmaxAIGames)

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.canvas.set_window_title('Game Analytics')
    fig.suptitle('TicTacToe Games', fontsize=16)
    plotPieChart(randomAIData, 'Random AI', ax1)
    plotPieChart(minmaxAIData, 'Minmax AI', ax2)

    plt.tight_layout()
    plt.show()


def plotPieChart(analyzedData, label, axis):
    axis.set_title(label, loc='center')
    axis.pie(analyzedData['pie']['data'],
             labels=analyzedData['pie']['labels'],
             radius=3,
             startangle=0,
             autopct='%1.0f%%',
             pctdistance=0.75,
             explode=(0.2, 0.2, 0.2)
             )
    axis.axis('equal')

    additionalData = (
        f"\n"
        f"Games: {analyzedData['games']}\n"
        f"AI Wins: {analyzedData['AIWins']}\n"
        f"Draws: {analyzedData['draws']}\n"
        f"AI Losses: {analyzedData['games'] - analyzedData['AIWins'] - analyzedData['draws']}\n"
        f"Moves per Game: {analyzedData['movesPerGame']}\n"
    )

    axis.text(0.75, 0.75, additionalData,
              horizontalalignment='left',
              verticalalignment='center',
              transform=axis.transAxes)
