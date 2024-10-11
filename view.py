import pygame
from minesweeper import Minesweeper

BACKGROUND_COLOR = pygame.Color(214,214,214)
MINE_COLOR = pygame.Color(0,0,0)
UNCOVERED_BG_COLOR = pygame.Color(175,175,175)
UNCOVERED_TEXT_COLORS = {0: pygame.Color(175,175,175),1: pygame.Color(1,0,253), 2: pygame.Color(19,129,1),
                         3: pygame.Color(252,0,5), 4: pygame.Color(1,0,126),
                         5: pygame.Color(128,0,2), 6: pygame.Color(18,129,128),
                         7: pygame.Color(0,0,0), 8: pygame.Color(128,128,128)}
CELL_SELECTED_COLOR = pygame.Color(175,175,175)
CLICKED_MINE_COLOR = pygame.Color(252,0,5)
LABEL_COLOR = pygame.Color(252,0,5)

class MineSweeperGame:

    def __init__(self):
        self._running = True
        self._state = None #game starts when first click is made
        self._surface = pygame.display.get_surface()
        self._resize_surface((900, 900))
        self._columns = 16
        self._rows = 16
        self._mines = 40
        self._started = False
        self._cells = {} ## key will be tuple coords and value will be 3 tuple, x,y, side_length, will store borders
        self._selected = None
        self._covered = set()
        self._flagged = set()
        self._game_over = False

    def run(self) -> None:

        pygame.init()
        self.font = pygame.font.SysFont('pressstart2p', 20)
        self._time = 0
        self._flag_text = self.font.render(str(self._mines - len(self._flagged)), True, LABEL_COLOR)
        self._time_text = self.font.render(str(self._time).zfill(3), True, LABEL_COLOR)
        #print(sorted(pygame.font.get_fonts()))
        self._surface = pygame.display.get_surface()

        clock = pygame.time.Clock()
        self._surface.fill(BACKGROUND_COLOR)
        self._draw_user_board()
        self._draw_flag_counter()
        self._draw_reset_button()


        self._draw_timer()
        seconds = 30
        while self._running:
            clock.tick(30)
            if self._handle_events():
                self._draw_user_board()
                self._draw_flag_counter()


            if self._started and not self._game_over:
                self._draw_reset_button()
                seconds-=1

            if seconds == 0:
                self._time += 1
                self._draw_timer()
                seconds = 30

        pygame.quit()


    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()

            if event.type == pygame.MOUSEBUTTONDOWN:


                    cell = self._get_cell_clicked(*pygame.mouse.get_pos())
                    if cell:
                        if not self._game_over and not self._started and event.button == 1:
                            self._draw_reset_button(tile_clicked=True)
                            self._started = True
                            self._state = Minesweeper(self._rows,self._columns, self._mines, *cell)

                        elif not self._game_over and event.button == 1:
                            if cell not in self._flagged:
                                self._state.uncover_tile(*cell)
                                self._draw_reset_button(tile_clicked = True)

                                if len(self._covered) == self._mines + 1:
                                    self._draw_reset_button(won= True)
                                    self._game_over = True

                        elif not self._game_over and self._started and event.button == 3:

                            if self._state.is_flagged(*cell):
                                self._state.remove_flag(*cell)

                                if cell in self._flagged:
                                    self._flagged.remove(cell)
                            else:
                                if self._state.place_flag(*cell):

                                    self._flagged.add(cell)

                        return True

                    elif self._reset_button.collidepoint(pygame.mouse.get_pos()):
                        self._started = False
                        self._state = None
                        self._time = 0
                        self._game_over = False
                        self._draw_timer()
                        self._draw_reset_button()
                        return True
                    return False



            if event.type == pygame.MOUSEMOTION:
                cell = self._get_cell_clicked(*pygame.mouse.get_pos())

                if cell != self._selected and cell != None:

                    if self._selected:
                        old_cell = self._cells[self._selected]

                        if self._selected in self._covered:
                            self._draw_covered_tile(old_cell[0],old_cell[1],.05)

                        if self._selected in self._flagged:
                            self._draw_flag_tile(old_cell[0], old_cell[1], .05)


                    self._selected = cell
                    if cell in self._covered and cell not in self._flagged:
                        self._highlight_selected_cell(self._cells[cell][0], self._cells[cell][1], .05)
                        pygame.display.flip()

    def _draw_reset_button(self, tile_clicked = False, game_over = False, won = False):

        surface = self._surface
        height = surface.get_height()
        width = surface.get_width()
        x = .47 * width
        y = .02 * height
        side = max(width, height) * .06
        
        image = 'assets/'
        if tile_clicked:
            image += "click.png"
        elif game_over:
            image += "gameover.png"
        elif won:
            image += "winner.png"
        else:
            image += "reset.png"
        button = pygame.Rect(x,y,side,side)
        pygame.draw.rect(surface, pygame.Color(214, 214, 214), button)

        mine_image = pygame.transform.scale(pygame.image.load(image), (side,side))
        surface.blit(mine_image, (x,y))
        self._reset_button = button
        #pygame.display.flip()

    def _draw_flag_counter(self):

        surface = self._surface
        height = surface.get_height()
        width = surface.get_width()
        label_x = .12 * width
        label_y = .08 * height
        white_rect = pygame.Rect(self._flag_text.get_rect(center=(label_x, label_y)))
        pygame.draw.rect(surface, BACKGROUND_COLOR, white_rect)
        self._flag_text = self.font.render(str(self._mines - len(self._flagged)), True, LABEL_COLOR)
        text_rect = self._flag_text.get_rect(center = (label_x,label_y))
        surface.blit(self._flag_text, text_rect)
        pygame.display.flip()

    def _draw_timer(self):

        surface = self._surface
        height = surface.get_height()
        width = surface.get_width()
        label_x = .87 * width
        label_y = .08 * height
        white_rect = pygame.Rect(self._time_text.get_rect(center=(label_x, label_y)))
        pygame.draw.rect(surface, BACKGROUND_COLOR, white_rect)

        self._time_text = self.font.render(str(self._time).zfill(3), True, LABEL_COLOR)
        text_rect = self._time_text.get_rect(center = (label_x,label_y))
        surface.blit(self._time_text, text_rect)
        pygame.display.flip()

    def _draw_user_board(self):

        surface = self._surface
        height = surface.get_height()
        width = surface.get_width()
        cell_field_startX = .1 * width
        cell_field_startY =  .1 * height
        tile_size = .05
        for r in range(self._rows):
            for c in range(self._columns):
                topX = cell_field_startX + (r * tile_size * max(width,height))
                topY = cell_field_startY + (c * tile_size * max(height,width))
                #print(topX, topY, tile_size)
                if self._state == None or self._state.get_cell(c,r) == -1:
                    self._cells[(c,r)] = self._draw_covered_tile(topX, topY, tile_size)
                    self._covered.add((c,r))

                elif self._state.get_cell(c,r) == 'F':
                    self._draw_flag_tile(topX, topY, tile_size)

                elif self._state.get_cell(c,r) == '*':
                    self._draw_mine_tile(topX,topY, tile_size)
                    if (c,r) in self._covered:
                        self._covered.remove((c,r))

                elif self._state.get_cell(c,r) == '**':
                    self._draw_mine_tile(topX, topY, tile_size, True)
                    if (c,r) in self._covered:
                        self._covered.remove((c,r))
                else:
                    self._draw_uncovered_tile(topX, topY, tile_size, self._state.get_cell(c,r))
                    if (c,r) in self._covered:
                        self._covered.remove((c,r))

        pygame.display.flip()


    def _get_cell_clicked(self,x,y):


        for coord,cell in self._cells.items():
            topX, topY, side = cell
            if x >= topX and x <= topX + side and  y >= topY and y <= topY + side:
                return coord

    def _highlight_selected_cell(self, x,y, tile_size ):

        surface = self._surface
        height = surface.get_height()
        width = surface.get_width()
        factor = max(width, height)
        border_side = factor * tile_size
        tile_side = factor * tile_size * .95
        tile_border = pygame.Rect(x, y, border_side, border_side)
        tile = pygame.Rect(x + (border_side - tile_side) // 2, y + (border_side - tile_side) // 2, tile_side, tile_side)
        pygame.draw.rect(surface, pygame.Color(0, 0, 0), tile_border)
        pygame.draw.rect(surface, CELL_SELECTED_COLOR, tile)


    def _draw_mine_tile(self, x,y, tile_size, clicked = False):

        surface = self._surface
        height = surface.get_height()
        width = surface.get_width()
        factor = max(width, height)
        border_side = factor * tile_size
        tile_side = factor * tile_size * .95
        tile_border = pygame.Rect(x, y, border_side, border_side)
        tile = pygame.Rect(x + (border_side - tile_side) // 2, y + (border_side - tile_side) // 2, tile_side, tile_side)
        pygame.draw.rect(surface, pygame.Color(0, 0, 0), tile_border)
        color = CLICKED_MINE_COLOR if clicked else UNCOVERED_BG_COLOR
        self._game_over = True
        self._draw_reset_button(game_over=True)
        pygame.draw.rect(surface, color, tile)
        mine_image = pygame.transform.scale(pygame.image.load("assets/bomb.png"), (tile_side, tile_side))
        surface.blit(mine_image, (x + (border_side - tile_side) // 2, y + (border_side - tile_side) // 2))

    def _draw_flag_tile(self, x,y, tile_size):

        surface = self._surface
        height = surface.get_height()
        width = surface.get_width()
        factor = max(width, height)
        border_side = factor * tile_size
        tile_side = factor * tile_size * .95
        tile_border = pygame.Rect(x, y, border_side, border_side)
        tile = pygame.Rect(x + (border_side - tile_side) // 2, y + (border_side - tile_side) // 2, tile_side, tile_side)
        pygame.draw.rect(surface, pygame.Color(0, 0, 0), tile_border)

        pygame.draw.rect(surface,pygame.Color(214,214,214), tile)
        mine_image = pygame.transform.scale(pygame.image.load("assets/flag.png"), (tile_side, tile_side))
        surface.blit(mine_image, (x + (border_side - tile_side) // 2, y + (border_side - tile_side) // 2))


    def _draw_uncovered_tile(self,x,y,tile_size,number):

        surface = self._surface
        height = surface.get_height()
        width = surface.get_width()
        factor = max(width, height)
        border_side = factor * tile_size
        tile_side = factor * tile_size * .95

        tile_border = pygame.Rect(x, y, border_side, border_side)
        tile = pygame.Rect(x + (border_side - tile_side) // 2, y + (border_side - tile_side) // 2, tile_side, tile_side)
        pygame.draw.rect(surface, pygame.Color(0, 0, 0), tile_border)
        pygame.draw.rect(surface, UNCOVERED_BG_COLOR, tile)
        text = self.font.render(str(number), True, UNCOVERED_TEXT_COLORS[number])
        text_rect = text.get_rect(center=(x + (border_side - tile_side) // 2 + tile_side //2, y + (border_side - tile_side) // 2 + tile_side //2))
        surface.blit(text, text_rect)
        #pygame.display.flip()

    def _draw_covered_tile(self, x, y, tile_size):

        surface = self._surface
        height = surface.get_height()
        width = surface.get_width()
        factor = max(width,height)
        border_side = factor * tile_size
        tile_side = factor * tile_size * .95
        tile_border = pygame.Rect(x,y, border_side, border_side )
        tile = pygame.Rect(x + (border_side - tile_side) //2, y + (border_side - tile_side) // 2 , tile_side, tile_side  )
        pygame.draw.rect(surface, pygame.Color(0,0,0), tile_border)
        pygame.draw.rect(surface, pygame.Color(214,214,214), tile)
        #pygame.display.flip()
        return (x, y, border_side)



    def _resize_surface(self, size: (int, int)) -> None:
        '''
        Takes in an intial size that is specified in the __init__ method
        and sets the size of the display to that size. The mode of the display
        is also set to resizable allowing for the user to resize the window
        '''
        pygame.display.set_mode(size)


    def _end_game(self):
        self._running = False

if __name__ == '__main__':
    MineSweeperGame().run()
