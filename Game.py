from Graphics import *
from Board import *


class Game(SetupWindow):
    def __init__(self):
        super().__init__()
        self.players = ('W', 'B')
        self.turn = self.players[0]
        self.graphics = Graphics()
        self.board = Board()
        self.board.initializePieces('g')
        self.selectedPiece = None
        self.jump = False
        self.buttonActions = ['Reset', 'Menu']
        self.backMenu = False
        self.buttonSize = [200, 50]
        self.endGame = False

    def eventLoopPvP(self):
        for event in pygame.event.get():  #uwaga tu tez rzucac wyjatki
            mousePos = self.graphics.boardCoord(pygame.mouse.get_pos())
            if event.type == pygame.QUIT:
                self.terminate_game()
            self.buttonFunc()
            self.board.jumpAvailable(self.turn)
            self.graphics.message_display(self.turndisplay(self.turn), 50, self.displayWidth/2, self.displayHeight/20, colors["BRIGHT_SUMMER_SUN"])
            self.graphics.drawBoardSquares(self.board)
            self.graphics.drawPieceCircles(self.board)
            self.clock.tick(60)
            if self.selectedPiece is not None and self.jump is True and not self.board.legalMoves(self.selectedPiece, self.jump):
                self.end_turn(self.board)
            if self.selectedPiece is not None and not self.board.legalMoves(self.selectedPiece):
                    if self.board.location(self.selectedPiece).occupant is not None:
                        self.board.location(self.selectedPiece).occupant.selected = False
                    self.selectedPiece = None
                    print('Brak mozliwosci Ruchu')
            if self.selectedPiece is not None and self.board.jumpAvailablePieces:
                if self.selectedPiece not in self.board.jumpAvailablePieces:
                    print('Musisz wykonac bicie')
                    self.board.location(self.selectedPiece).occupant.selected = False
                    self.selectedPiece = None
            if event.type == pygame.MOUSEBUTTONDOWN and self.board.isOnBoard(mousePos):
                if self.jump is False:
                    if self.board.location(mousePos).occupant is not None and self.board.location(mousePos).occupant.color == self.turn and self.selectedPiece is None:
                        self.selectedPiece = mousePos
                        self.board.location(mousePos).occupant.selected = True
                    elif self.selectedPiece is not None and mousePos in self.board.legalMoves(self.selectedPiece):
                        colisionMove = self.board.checkColision(self.selectedPiece, mousePos)
                        self.board.movePiece(self.selectedPiece, mousePos)
                        if mousePos not in self.board.adjacent(self.selectedPiece) and isinstance(self.board.location(mousePos).occupant, King) is False:
                            self.board.removePiece((self.selectedPiece[0] + int((mousePos[0] - self.selectedPiece[0]) / 2), self.selectedPiece[1] + int((mousePos[1] - self.selectedPiece[1]) / 2)))
                            self.jump = True
                            self.selectedPiece = mousePos
                            self.board.location(mousePos).occupant.selected = True
                        elif isinstance(self.board.location(mousePos).occupant, King) is True and colisionMove:
                            self.board.removePiece(colisionMove)
                            self.jump = True
                            self.selectedPiece = mousePos
                            self.board.location(mousePos).occupant.selected = True
                        else:
                            self.end_turn(self.board)
                else:
                    if self.selectedPiece is not None and mousePos in self.board.legalMoves(self.selectedPiece, self.jump):
                        self.board.movePiece(self.selectedPiece, mousePos)
                        self.board.removePiece((self.selectedPiece[0] + int((mousePos[0] - self.selectedPiece[0]) / 2), self.selectedPiece[1] + int((mousePos[1] - self.selectedPiece[1]) / 2)))
                        self.board.location(mousePos).occupant.selected = True
                        self.selectedPiece = mousePos
                        if not self.board.legalMoves(mousePos, self.jump):
                            self.end_turn(self.board)
            if self.endGame:
                self.endGameDisplay()
            pygame.display.update()

    def terminate_game(self):
        pygame.quit()
        quit()

    def end_turn(self, board):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]
        self.selectedPiece = None
        for x in range(8):
            for y in range(8):
                if board.matrix[x][y].occupant is not None:
                    board.matrix[x][y].occupant.selected = False
        self.jump = False
        self.board.jumpAvailablePieces = []
        self.board.jump = []
        if self.checkEndgame():
            self.endGame = True


    def turndisplay(self, turn):
        if turn == 'W':
            return 'Tura gracza 1'
        else:
            return 'Tura gracza 2'

    def checkEndgame(self):
        for x in range(8):
            for y in range(8):
                if self.board.location((x, y)).color == '1' and self.board.location((x, y)).occupant is not None and self.board.location((x, y)).occupant.color == self.turn:
                    if self.board.legalMoves((x, y)):
                        return False
        return True

    def gameButtons(self,msg, msg_size, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            colour = ac
            if click[0] == 1 and action is not None:
                if action == self.buttonActions[0]:
                    self.resetGame()
                else:
                    self.backMenu = True
        else:
            colour = ic
        pygame.draw.rect(self.screen, colour, (x,y,w,h))
        smallText = pygame.font.Font("freesansbold.ttf", msg_size)
        textSurf, textRect = self.graphics.text_objects(msg, smallText, colors["MUSTARD"])
        textRect.center = ((x + (w/2)), (y + (h/2))+5)
        self.screen.blit(textSurf, textRect)

    def buttonFunc(self):
        for action, i in zip(self.buttonActions, [540, 480]):
                    self.gameButtons(action, 60, self.displayWidth - (self.displayWidth - self.graphics.boardSize)/2 - self.buttonSize[0]/2,
                                     i, self.buttonSize[0], self.buttonSize[1],
                                     colors["SUMMER_SUN"], colors["BRIGHT_SUMMER_SUN"], action)

    def endGameDisplay(self):
        if self.turn == self.players[0]:
            self.graphics.message_display('Wygrał 2', 100, self.displayWidth/2, self.displayHeight/2, colors["CHERRY"])
        else:
            self.graphics.message_display('Wygrał 1', 100, self.displayWidth/2, self.displayHeight/2, colors["CHERRY"])

    def resetGame(self): #tu wrzucac wszystko z init
        self.turn = self.players[0]
        self.board = Board()
        self.board.initializePieces()
        self.selectedPiece = None
        self.endGame = False






