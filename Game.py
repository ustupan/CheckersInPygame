from Graphics import *
from Board import *


class Game(SetupWindow):
    def __init__(self):
        super().__init__()
        self.players = ('W', 'B')
        self.turn = self.players[0]
        self.graphics = Graphics()
        self.board = Board()
        self.board.initializePieces()
        self.selectedLegalMoves = []
        self.buttonActions = ['Reset', 'Menu']
        self.backMenu = False
        self.buttonSize = [200, 50]

    def eventLoopPvP(self):
        for event in pygame.event.get():  #uwaga tu tez rzucac wyjatki
            if event.type == pygame.QUIT:
                self.terminate_game()
            for action, i in zip(self.buttonActions, [540, 480]):
                self.gameButtons(action, 60, self.displayWidth - (self.displayWidth - self.graphics.boardSize)/2 - self.buttonSize[0]/2,
                                 i, self.buttonSize[0], self.buttonSize[1],
                                 colors["SUMMER_SUN"], colors["BRIGHT_SUMMER_SUN"], action)
            self.graphics.message_display(self.turndisplay(self.turn), 50, self.displayWidth/2, self.displayHeight/20, colors["BRIGHT_SUMMER_SUN"])
            self.graphics.drawBoardSquares(self.board)
            self.graphics.drawPieceCircles(self.board)
            pygame.display.update()
            self.clock.tick(60)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

    def terminate_game(self):
        pygame.quit()
        quit()

    def end_turn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]
        self.selectedLegalMoves = []

        if self.checkEndgame():
            if self.turn == self.players[0]:
                print('Wygral 1')  # tu zamienic na normalne wyswietlanie
            else:
                print('Wygral 2')

    def turndisplay(self, turn):
        if turn == 'W':
            return 'Tura gracza 1'
        else:
            return 'Tura gracza 2'

    def checkEndgame(self):
        for x in range(8):
            for y in range(8):
                if self.board.location((x, y)).color == '1' and self.board.location((x, y)).occupant is not None and self.board.location((x, y)).occupant.color == self.turn:
                    if self.board.legalMoves((x, y)) is not None:
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

    def resetGame(self): #tu wrzucac wszystko z init
        self.turn = self.players[0]
        self.board = Board()
        self.board.initializePieces()
        self.selectedLegalMoves = []






