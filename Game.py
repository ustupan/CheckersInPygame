from Graphics import *
from Board import *


class Game(SetupWindow):
    def __init__(self):
        super().__init__()
        self.__players = ('W', 'B')
        self.__turn = self.__players[0]
        self.__graphics = Graphics()
        self.__board = Board()
        self.__board.initializePieces('g')
        self.__selectedPiece = None
        self.__jump = False
        self.__buttonActions = ['Reset', 'Menu']
        self.__backMenu = False
        self.__buttonSize = [200, 50]
        self.__endGame = False

    def getBackMenu(self):
        return self.__backMenu

    def eventLoopPvP(self):
        for event in pygame.event.get():
            mousePos = self.__graphics.boardCoord(pygame.mouse.get_pos())
            if event.type == pygame.QUIT:
                self.terminate_game()
            self.buttonFunc()
            self.__board.jumpAvailable(self.__turn)
            self.__graphics.message_display(self.turndisplay(self.__turn), 50, self.getDisplayWidth() / 2, self.getDisplayHeight() / 20, colors["BRIGHT_SUMMER_SUN"])
            self.__graphics.drawBoardSquares(self.__board)
            self.__graphics.drawPieceCircles(self.__board)
            self.clock.tick(60)
            if self.__selectedPiece is not None and self.__jump is True and not self.__board.legalMoves(self.__selectedPiece, self.__jump):
                self.end_turn(self.__board)
            if self.__selectedPiece is not None and not self.__board.legalMoves(self.__selectedPiece):
                    if self.__board.location(self.__selectedPiece).occupant is not None:
                        self.__board.location(self.__selectedPiece).occupant.selected = False
                    self.__selectedPiece = None
                    self.invalidMove()
            if self.__selectedPiece is not None and self.__board.jumpAvailablePieces:
                if self.__selectedPiece not in self.__board.jumpAvailablePieces:
                    self.__board.location(self.__selectedPiece).occupant.selected = False
                    self.__selectedPiece = None
                    self.invalidMove()
            if self.__selectedPiece:
                if self.__jump is False:
                    self.__graphics.highlightMoves(self.__board.legalMoves(self.__selectedPiece))
                else:
                    self.__graphics.highlightMoves(self.__board.legalMoves(self.__selectedPiece, self.__jump))
            if event.type == pygame.MOUSEBUTTONDOWN and self.__board.isOnBoard(mousePos):
                if self.__jump is False:
                    if self.__board.location(mousePos).occupant is not None and self.__board.location(mousePos).occupant.color == self.__turn and self.__selectedPiece is None:
                        self.__selectedPiece = mousePos
                        self.__board.location(mousePos).occupant.selected = True
                    elif self.__selectedPiece is not None:
                        if mousePos in self.__board.legalMoves(self.__selectedPiece):
                            colisionMove = self.__board.checkColision(self.__selectedPiece, mousePos)
                            self.__board.movePiece(self.__selectedPiece, mousePos)
                            if mousePos not in self.__board.adjacent(self.__selectedPiece) and isinstance(self.__board.location(mousePos).occupant, King) is False:
                                self.__board.removePiece((self.__selectedPiece[0] + int((mousePos[0] - self.__selectedPiece[0]) / 2), self.__selectedPiece[1] + int((mousePos[1] - self.__selectedPiece[1]) / 2)))
                                self.__jump = True
                                self.__selectedPiece = mousePos
                                self.__board.location(mousePos).occupant.selected = True
                            elif isinstance(self.__board.location(mousePos).occupant, King) is True and colisionMove:
                                self.__board.removePiece(colisionMove)
                                self.__jump = True
                                self.__selectedPiece = mousePos
                                self.__board.location(mousePos).occupant.selected = True
                            else:
                                self.end_turn(self.__board)
                        else:
                            self.invalidMove()
                else:
                    if self.__selectedPiece is not None and mousePos in self.__board.legalMoves(self.__selectedPiece, self.__jump):
                        self.__board.movePiece(self.__selectedPiece, mousePos)
                        self.__board.removePiece((self.__selectedPiece[0] + int((mousePos[0] - self.__selectedPiece[0]) / 2), self.__selectedPiece[1] + int((mousePos[1] - self.__selectedPiece[1]) / 2)))
                        self.__board.location(mousePos).occupant.selected = True
                        self.__selectedPiece = mousePos
                        if not self.__board.legalMoves(mousePos, self.__jump):
                            self.end_turn(self.__board)
                    else:
                        self.invalidMove()
            if self.__endGame:
                self.endGameDisplay()
            pygame.display.update()

    def invalidMove(self):
        self.__graphics.message_display('Ruch', 40, self.getDisplayWidth() / 2 + 270, self.getDisplayHeight() / 1.5, colors["CHERRY"])
        self.__graphics.message_display('Nieprawidłowy!', 35, self.getDisplayWidth() / 2 + 270, self.getDisplayHeight() / 1.5 + 40, colors["CHERRY"])

    def terminate_game(self):
        pygame.quit()
        quit()

    def end_turn(self, board):
        if self.__turn == self.__players[0]:
            self.__turn = self.__players[1]
        else:
            self.__turn = self.__players[0]
        self.__selectedPiece = None
        for x in range(8):
            for y in range(8):
                if board.matrix[x][y].occupant is not None:
                    board.matrix[x][y].occupant.selected = False
        self.__jump = False
        self.__board.jumpAvailablePieces = []
        self.__board.jump = []
        if self.checkEndgame():
            self.__endGame = True

    def turndisplay(self, turn):
        if turn == 'W':
            return 'Tura gracza 1'
        else:
            return 'Tura gracza 2'

    def checkEndgame(self):
        for x in range(8):
            for y in range(8):
                if self.__board.location((x, y)).color == '1' and self.__board.location((x, y)).occupant is not None and self.__board.location((x, y)).occupant.color == self.__turn:
                    if self.__board.legalMoves((x, y)):
                        return False
        return True

    def gameButtons(self,msg, msg_size, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            colour = ac
            if click[0] == 1 and action is not None:
                if action == self.__buttonActions[0]:
                    self.resetGame()
                else:
                    self.__backMenu = True
        else:
            colour = ic
        pygame.draw.rect(self.screen, colour, (x,y,w,h))
        smallText = pygame.font.Font("freesansbold.ttf", msg_size)
        textSurf, textRect = self.__graphics.text_objects(msg, smallText, colors["MUSTARD"])
        textRect.center = ((x + (w/2)), (y + (h/2))+5)
        self.screen.blit(textSurf, textRect)

    def buttonFunc(self):
        for action, i in zip(self.__buttonActions, [540, 480]):
                    self.gameButtons(action, 60, self.getDisplayWidth() - (self.getDisplayWidth() - self.__graphics.getBoardSize()) / 2 - self.__buttonSize[0] / 2,
                                     i, self.__buttonSize[0], self.__buttonSize[1],
                                     colors["SUMMER_SUN"], colors["BRIGHT_SUMMER_SUN"], action)

    def endGameDisplay(self):
        if self.__turn == self.__players[0]:
            self.__graphics.message_display('Wygrał 2', 100, self.getDisplayWidth() / 2, self.getDisplayHeight() / 2, colors["CHERRY"])
        else:
            self.__graphics.message_display('Wygrał 1', 100, self.getDisplayWidth() / 2, self.getDisplayHeight() / 2, colors["CHERRY"])

    def resetGame(self):
        self.__turn = self.__players[0]
        self.__board = Board()
        self.__board.initializePieces()
        self.__selectedPiece = None
        self.__endGame = False






