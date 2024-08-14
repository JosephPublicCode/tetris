import pygame
import random
import sys
from piece import Piece
from shapes import Shapes
from settings import Settings
# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main
 
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
pygame.font.init()
 
# GLOBALS VARS
settings = Settings()
shapes = Shapes()

 
 
# SHAPE FORMATS


# index 0 - 6 represent shape
 
 

def create_grid(locked_pos={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    
    for i in range(len(grid)): 
        for j in range(len(grid[i])): 
            if (j,i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c 

    return grid
                
 
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format): 
        row = list(line)
        for j, column in enumerate(row):
            if column == '0': 
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions): 
        positions[i] = (pos[0]-2,pos[1]-4)
    
    return positions
 
def valid_space(shape, grid):
    accepted_positions = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
 
    formatted = convert_shape_format(shape)

    for pos in formatted: 
        if pos not in accepted_positions: 
            if pos[1] > -1: 
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x,y = pos
        if y < 1: 
            return True
    return False
 
def get_shape():
    return Piece(5, 0, random.choice(shapes.shapes))
 
 
def draw_text_middle(text, size, color, surface):
   font = pygame.font.SysFont('arial',size)
   label = font.render(text, 1, color)

   surface.blit(label,(settings.top_left_x + settings.play_width/2 - (label.get_width()/2),\
                       settings.top_left_y + settings.play_height/2 - label.get_height()/2) )
   
def draw_grid(surface, grid):
    
    sx = settings.top_left_x
    sy = settings.top_left_y

    for i in range(len(grid)): 
        pygame.draw.line(surface, (128,128,128), (sx,sy+i*settings.block_size),(sx+settings.play_width,sy + i*settings.block_size))
        for j in range(len(grid[i])): 
            pygame.draw.line(surface, (128,128,128), (sx + j*settings.block_size,sy),\
                             (sx + j*settings.block_size,sy + settings.play_height))
    
def clear_rows(grid, locked):
    
    inc = 0 

    for i in range(len(grid)-1,-1,-1): 
        row = grid[i]
        if (0,0,0) not in row: 
            inc += 1 
            ind = i 
            for j in range(len(row)): 
                try: 
                    del locked[(j,i)]
                except: 
                    continue
    if inc > 0: 
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]: 
            x,y = key
            if y < ind: 
                new_key = (x,y + inc)
                locked[new_key] = locked.pop(key)
    return inc
 
def update_score(new_score): 
    with open("tetris/high_score.txt","r") as f: 
        lines = f.readlines()
        score = lines[0].strip()
    
    with open("tetris/high_score.txt",'w') as f: 
        if int(score) > new_score:
            f.write(str(score))
        else:
            f.write(str(new_score))



def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans',30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = settings.top_left_x + settings.play_width
    sy = settings.top_left_y + settings.play_height/2
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format): 
        row = list(line)
        for j, column in enumerate(row): 
            if column == '0': 
                pygame.draw.rect(surface, shape.color, (sx + j*settings.block_size, sy + i*settings.block_size, settings.block_size, settings.block_size),0)
    
    surface.blit(label, (sx + 10, sy - 30))

    

def draw_window(surface,grid,score=0):
    surface.fill((200,200,200))

    font = pygame.font.SysFont('comicsans',60)
    label = font.render('Tetris',1,(255,255,255))

    surface.blit(label,(settings.top_left_x + settings.play_width/2 - (label.get_width()/2),30))

    for i in range(len(grid)): 
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],\
                        (settings.top_left_x + j*settings.block_size, settings.top_left_y + i*settings.block_size,\
                        settings.block_size, settings.block_size),0)

    # do we need a create grid here as well? 
    draw_grid(surface,grid)
    pygame.draw.rect(surface, (255,0,0),(settings.top_left_x,settings.top_left_y,settings.play_width,settings.play_height),5)

    font = pygame.font.SysFont('arial',30)
    label = font.render('score: ' + str(score), 1, (255,255,255))

    sx = settings.top_left_x + settings.play_width + 50 
    sy = settings.top_left_y + settings.play_height/2 - 100 

    surface.blit(label,(sx + 10,sy + 200))


 
def main(win):
    
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape() 
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0 
    fall_speed = 0.27
    level_time = 0 
    score = 0 

    while run: 
        

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5: 
            level_time = 0 
            if fall_speed > 0.12: 
                fall_speed -= 0.005


        if fall_time / 1000 >= fall_speed: 
            fall_time = 0 
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y >0: 
                    current_piece.y -= 1
                    change_piece = True



        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False
        
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT or event.key == pygame.K_a: 
                    current_piece.x -= 1 
                    if not(valid_space(current_piece, grid)): 
                        current_piece.x += 1 
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: 
                    current_piece.x += 1 
                    if not(valid_space(current_piece, grid)): 
                        current_piece.x -= 1 
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s: 
                    current_piece.y += 1 
                    if not(valid_space(current_piece, grid)): 
                        current_piece.y -= 1 
                elif event.key == pygame.K_UP or event.key == pygame.K_w: 
                    current_piece.rotation += 1 
                    if not(valid_space(current_piece, grid)): 
                        current_piece.rotation -= 1 

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)): 
            x,y = shape_pos[i]
            if y > -1: 
                grid[y][x] = current_piece.color
        
        if change_piece: 
            for pos in shape_pos: 
                p = (pos[0],pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid,locked_positions)*10 
            

        
        draw_window(win, grid,score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle('YOU LOST', 80, (255,255,255),win)
            pygame.display.update()
            pygame.time.delay(1500) 
            run = False
            update_score(score)




def main_menu(win):
    run = True
    while run: 
        win.fill((0,0,0))
        draw_text_middle('Press Any Key to Start', 60, (255,255,255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN: 
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((settings.s_width,settings.s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game