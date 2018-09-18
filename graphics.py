import pygame, sys, constants, exceptions, random, knightsTour
from pygame.locals import *

class Graphics:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Knight\'s Tour")
        FONT = pygame.font.SysFont('Comic Sans MS', 30)

        self.DISPLAY = pygame.display.set_mode((constants.BOARD_WIDTH + 2 * constants.PAD,
                                                constants.BOARD_HEIGHT + 3 * constants.PAD + constants.BUTTON_HEIGHT))
        self.DISPLAY.fill(constants.BACKGROUND)

        self.BOARD = pygame.Surface((constants.BOARD_WIDTH, constants.BOARD_HEIGHT))
        self.BOARD.fill(constants.GREY)

        self.reset_board()

        # create the start button
        self.button = pygame.Rect((constants.PAD + constants.BOARD_WIDTH / 2 - constants.BUTTON_WIDTH / 2,
                                   2.5 * constants.PAD + constants.BOARD_HEIGHT,
                                   constants.BUTTON_WIDTH,
                                   constants.BUTTON_HEIGHT))
        pygame.draw.rect(self.DISPLAY, constants.BLUE, self.button)

        text = FONT.render("START", True, constants.DARK)
        text_rect = text.get_rect(center=(constants.PAD + constants.BOARD_WIDTH / 2,
                                          2.5 * constants.PAD + constants.BOARD_HEIGHT + constants.BUTTON_HEIGHT / 2))
        self.DISPLAY.blit(text, text_rect)

        # row labels
        for row in constants.ROWS:
            self.DISPLAY.blit(FONT.render(row, True, constants.DARK),
                              (10,
                              (8 - int(row)) * (constants.TILE_WIDTH + constants.SPACE) + constants.PAD + 5,
                              constants.TILE_HEIGHT,
                              constants.TILE_WIDTH))
        # col labels
        for col in constants.COLUMNS:
            self.DISPLAY.blit(FONT.render(col, True, constants.DARK),
                              (constants.COLUMNS.index(col) * (constants.TILE_HEIGHT + constants.SPACE) + constants.PAD + 12,
                              constants.PAD + constants.BOARD_HEIGHT,
                              constants.TILE_HEIGHT,
                              constants.TILE_WIDTH))

        # knight
        self.knight = pygame.image.load("knightPiece.png")
        self.knight = pygame.transform.scale(self.knight, (constants.TILE_WIDTH, constants.TILE_WIDTH))

        self.knight_x, self.knight_y = self.__chess_to_pixel("4", "E")
        self.DISPLAY.blit(self.knight, (self.knight_x, self.knight_y))
        pygame.display.update()

        self.main()

    def reset_board(self):
        for row in range(8):
            for col in range(8):
                color = constants.LIGHT

                if (row + col) % 2 == 1:
                    color = constants.DARK

                pygame.draw.rect(self.BOARD, color, (row * (constants.TILE_WIDTH + constants.SPACE),
                                                     col * (constants.TILE_HEIGHT + constants.SPACE),
                                                     constants.TILE_WIDTH,
                                                     constants.TILE_HEIGHT))

        self.DISPLAY.blit(self.BOARD, (constants.PAD, constants.PAD))

    def __button_clicked(self, x, y):
        return self.button.collidepoint(x, y)

    @staticmethod
    def __chess_to_pixel(row, col):
        x = constants.COLUMNS.index(col) * (constants.TILE_WIDTH + constants.SPACE) + constants.PAD
        y = (7 - constants.ROWS.index(row)) * (constants.TILE_HEIGHT + constants.SPACE) + constants.PAD
        return x, y

    def move_knight(self, row, col):
        if col not in constants.COLUMNS:
            raise exceptions.InvalidColumnError(col)
        if row not in constants.ROWS:
            raise exceptions.InvalidRowError(row)

        # move the knight
        new_x, new_y = self.__chess_to_pixel(row, col)
        x_step = (new_x - self.knight_x) // constants.FPS
        y_step = (new_y - self.knight_y) // constants.FPS

        while self.knight_x != new_x or self.knight_y != new_y:
            self.clock.tick(constants.FPS * constants.SPEED)

            self.knight_x += x_step
            self.knight_y += y_step

            self.DISPLAY.blit(self.BOARD, (constants.PAD, constants.PAD))
            self.DISPLAY.blit(self.knight, (self.knight_x, self.knight_y))
            pygame.display.update()

        pygame.draw.rect(self.BOARD, constants.BLUE, (self.knight_x - constants.PAD,
                                                 self.knight_y - constants.PAD,
                                                 constants.TILE_HEIGHT,
                                                 constants.TILE_WIDTH))
        self.DISPLAY.blit(self.BOARD, (constants.PAD, constants.PAD))
        self.DISPLAY.blit(self.knight, (self.knight_x, self.knight_y))
        pygame.display.update()

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if self.__button_clicked(pos[0], pos[1]):
                        self.reset_board()

                        i = random.randint(0, 7)
                        j = random.randint(0, 7)

                        board = knightsTour.Board()
                        moves = board.knights_tour(constants.COLUMNS[i], constants.ROWS[j])

                        for move in moves:
                            self.move_knight(move[1], move[0])
                            pygame.time.delay(200)

if __name__ == '__main__':
    raise exceptions.ModuleError()