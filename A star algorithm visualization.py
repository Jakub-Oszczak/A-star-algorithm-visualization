import pygame as pg
from queue import PriorityQueue

WIDTH = 500
WIN = pg.display.set_mode((WIDTH,WIDTH))
pg.display.set_caption('A* algorithm visualization')

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = col * width
        self.y = row * width
        self.color = WHITE
        self.neighbours = []
    
    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE  
    
    def reset(self):
        self.color = WHITE
    
    def make_start(self):
        self.color = ORANGE
    
    def make_closed(self):
        self.color = RED
    
    def make_open(self):
         self.color = GREEN

    def make_barrier(self):
        self.color = BLACK
    
    def make_end(self):
        self.color = TURQUOISE
    
    def make_path(self):
        self.color = PURPLE
    
    def draw(self, win):
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier(): # UP
            self.neighbours.append(grid[self.row-1][self.col])
        
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier(): # DOWN
            self.neighbours.append(grid[self.row+1][self.col])

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): # LEFT
            self.neighbours.append(grid[self.row][self.col-1])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier(): # RIGHT
            self.neighbours.append(grid[self.row][self.col+1])

    def __lt__(self, other):
        return False
    
def h(p1, p2):
        return abs(p1[0] - p2[0]) +  abs(p1[1] - p2[1])

def reconstruct_path(current, came_from, draw):
    while current in came_from:
        current.make_path()
        current = came_from[current]
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_copy = {start}

    while not open_set.empty():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        
        current = open_set.get()[2]
        open_set_copy.remove(current)

        if current == end:
            reconstruct_path(current, came_from, draw)
            end.make_end()
            return True

        for neighour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighour]:
                came_from[neighour] = current
                g_score[neighour] = temp_g_score
                f_score[neighour] = temp_g_score + h(neighour.get_pos(), end.get_pos())
                if neighour not in open_set_copy:
                    count += 1
                    open_set.put((f_score[neighour], count, neighour))
                    open_set_copy.add(neighour)
                    neighour.make_open()
        
        if current != start and current != end:
            current.make_closed()

        draw()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pg.draw.line(win, GREY, (0, i*gap),(width, i*gap))
        for j in range(rows):
            pg.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
        
    draw_grid(win, rows, width)
    pg.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos
    
    row = y//gap
    col = x//gap

    return row, col

def main(win, width):
    ROWS = 25
    grid = make_grid(ROWS, width)

    start = None 
    end = None
    
    lets_go = False
    run = True

    text1 = 'Legend:'
    text2 = '   Left mouse button - place start/end/barrier'
    text3 = '   Right mouse button - reset placed spot'
    text4 = '   Space - start algorithm'
    text5 = '   R - reset (clear screen)'
    text6 = '        '
    text7 = 'Start'

    pg.init()
    font = pg.font.Font('freesansbold.ttf', 20)
    font1 = pg.font.Font('freesansbold.ttf', 50)

    txt1 = font.render(text1, True, BLACK)
    textRect1 = txt1.get_rect()
    textRect1.center = (60, 140)

    txt2 = font.render(text2, True, BLACK)
    textRect2 = txt2.get_rect()
    textRect2.center = (258, 170)

    txt3 = font.render(text3, True, BLACK)
    textRect3 = txt3.get_rect()
    textRect3.center = (239, 200)

    txt4 = font.render(text4, True, BLACK)
    textRect4 = txt4.get_rect()
    textRect4.center = (160, 230)

    txt5 = font.render(text5, True, BLACK)
    textRect5 = txt5.get_rect()
    textRect5.center = (160, 260)

    txt6 = font1.render(text6, True, BLACK, BLACK)
    textRect6 = txt6.get_rect()
    textRect6.center = (250, 350)

    txt7 = font.render(text7, True, WHITE)
    textRect7 = txt7.get_rect()
    textRect7.center = (250, 350)

    while lets_go == False:
        win.fill(TURQUOISE)
        win.blit(txt1, textRect1)
        win.blit(txt2, textRect2)
        win.blit(txt3, textRect3)
        win.blit(txt4, textRect4)
        win.blit(txt5, textRect5)
        win.blit(txt6, textRect6)
        win.blit(txt7, textRect7)
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        if pg.mouse.get_pressed()[0]:
            pos = pg.mouse.get_pos()
            x, y = pos
            if x in range(194, 305) and y in range(325, 374):
                lets_go = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if pg.mouse.get_pressed()[0]: # LEFT
                pos = pg.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    spot.make_start()
                elif not end and spot != start:
                    end = spot
                    spot.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pg.mouse.get_pressed()[2]: # RIGHT
                pos = pg.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
            
                if event.key == pg.K_r:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pg.quit()

main(WIN, WIDTH)