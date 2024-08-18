import pygame
import random
import sys
from piece import Piece
from shapes import Shapes
from settings import Settings
from score import Score
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


class Tetris:
    def __init__(self): 
        pygame.font.init()
        pygame.mixer.init()
        pygame.mixer.music.load('tetris/tetris_theme.mp3')

        self.settings = Settings()
        self.shapes = Shapes()
        self.score = Score()


 

    def create_grid(self,locked_pos={}):
        grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
        
        for i in range(len(grid)): 
            for j in range(len(grid[i])): 
                if (j,i) in locked_pos:
                    c = locked_pos[(j,i)]
                    grid[i][j] = c 

        return grid
                    
    
    def convert_shape_format(self,shape):
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
    
    def valid_space(self,shape, grid):
        accepted_positions = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
        accepted_positions = [j for sub in accepted_positions for j in sub]
    
        formatted = self.convert_shape_format(shape)

        for pos in formatted: 
            if pos not in accepted_positions: 
                if pos[1] > -1: 
                    return False
        return True


    def check_lost(self,positions):
        for pos in positions:
            x,y = pos
            if y < 1: 
                return True
        return False
    
    def get_shape(self):
        return Piece(5, 0, random.choice(self.shapes.shapes))
    
    
    def draw_text_middle(self,text, size, color, surface):
        font = pygame.font.SysFont('arial',size)
        label = font.render(text, 1, color)

        surface.blit(label,(self.settings.top_left_x + self.settings.play_width/2 - (label.get_width()/2),\
                            self.settings.top_left_y + self.settings.play_height/2 - label.get_height()/2) )
        

    def draw_text(self, text, size, color, position_x, position_y, surface): 
        font = pygame.font.SysFont('arial',size)
        label = font.render(text, 1, color)

        surface.blit(label, (position_x- (label.get_width()/2), position_y + (label.get_height()/2)))


    
    def draw_grid(self,surface, grid):
        
        sx = self.settings.top_left_x
        sy = self.settings.top_left_y

        for i in range(len(grid)): 
            pygame.draw.line(surface, self.settings.grid_line_color, (sx,sy+i*self.settings.block_size),
                             (sx+self.settings.play_width,sy + i*self.settings.block_size))
            for j in range(len(grid[i])): 
                pygame.draw.line(surface, self.settings.grid_line_color, (sx + j*self.settings.block_size,sy),\
                                (sx + j*self.settings.block_size,sy + self.settings.play_height))
        
    def clear_rows(self,grid, locked):
        
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
    




    def draw_next_shape(self,shape, surface):
        font = pygame.font.SysFont('arial',30)
        label = font.render('Next Shape', 1, self.settings.text_color)

        sx = self.settings.top_left_x + self.settings.play_width
        sy = self.settings.top_left_y + self.settings.play_height/2
        format = shape.shape[shape.rotation % len(shape.shape)]
    
        for i, line in enumerate(format): 
            row = list(line)
            for j, column in enumerate(row): 
                if column == '0': 
                    pygame.draw.rect(surface, shape.color, (sx + j*self.settings.block_size+10, sy + i*self.settings.block_size - 50 , self.settings.block_size, self.settings.block_size),0)
        
        surface.blit(label, (sx + 20, sy - 100))

        

    def draw_window(self,surface,grid,last_score,score=0):
        surface.fill(self.settings.surface_color)

        font = pygame.font.SysFont('arial',60)
        label = font.render('Tetris',1,self.settings.text_color)

        surface.blit(label,(self.settings.top_left_x + self.settings.play_width/2 - (label.get_width()/2),30))

        for i in range(len(grid)): 
            for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j],\
                            (self.settings.top_left_x + j*self.settings.block_size, \
                             self.settings.top_left_y + i*self.settings.block_size,\
                            self.settings.block_size, self.settings.block_size),0)

        # do we need a create grid here as well? 
        self.draw_grid(surface,grid)
        pygame.draw.rect(surface, self.settings.border_color ,(self.settings.top_left_x,self.settings.top_left_y,
                                             self.settings.play_width,self.settings.play_height),5)

        font = pygame.font.SysFont('arial',30)

        # last score
        label_high = font.render('high score: ' + str(last_score), 1, self.settings.text_color)

        sx_high = 20
        sy_high = self.settings.top_left_y + self.settings.play_height/2 - 300

        surface.blit(label_high,(sx_high,sy_high))


        # current score
        
        label = font.render('score: ' + str(score), 1, self.settings.text_color)

        sx = self.settings.top_left_x + self.settings.play_width + 50 
        sy = self.settings.top_left_y + self.settings.play_height/2 - 300

        surface.blit(label,(sx,sy))

    
    def main(self,win):
        
        last_score = self.score.max_score()


        locked_positions = {}
        grid = self.create_grid(locked_positions)

        change_piece = False
        run = True
        current_piece = self.get_shape() 
        next_piece = self.get_shape()
        clock = pygame.time.Clock()
        fall_time = 0 
        fall_speed = 0.27
        level_time = 0 
        score = 0 

        while run: 
            

            grid = self.create_grid(locked_positions)
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
                if not (self.valid_space(current_piece, grid)) and current_piece.y >0: 
                        current_piece.y -= 1
                        change_piece = True



            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    run = False
            
                if event.type == pygame.KEYDOWN: 
                    self._key_down_event(event,current_piece,grid)

                if event.type == pygame.KEYUP: 
                    self._key_up_event(event,current_piece,grid)
                    

            shape_pos = self.convert_shape_format(current_piece)

            for i in range(len(shape_pos)): 
                x,y = shape_pos[i]
                if y > -1: 
                    grid[y][x] = current_piece.color
            
            if change_piece: 
                for pos in shape_pos: 
                    p = (pos[0],pos[1])
                    locked_positions[p] = current_piece.color
                current_piece = next_piece
                next_piece = self.get_shape()
                change_piece = False
                score += self.clear_rows(grid,locked_positions)*10 
                

            
            self.draw_window(win, grid,last_score,score)
            self.draw_next_shape(next_piece, win)
            pygame.display.update()

            if self.check_lost(locked_positions):
                self.draw_text_middle('YOU LOST', 80, self.settings.text_color,win)
                pygame.display.update()
                pygame.time.delay(1500) 
                run = False
                self.score.update_score(score)
    

    def _key_down_event(self,event,current_piece,grid): 
        if event.key == pygame.K_LEFT or event.key == pygame.K_a: 
            current_piece.x -= 1 
            if not(self.valid_space(current_piece, grid)): 
                current_piece.x += 1 

        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: 
            current_piece.x += 1 
            if not(self.valid_space(current_piece, grid)): 
                current_piece.x -= 1 

        elif event.key == pygame.K_DOWN or event.key == pygame.K_s: 
            current_piece.y += 1 
            if not(self.valid_space(current_piece, grid)): 
                current_piece.y -= 1 

        elif event.key == pygame.K_UP or event.key == pygame.K_w: 
            current_piece.rotation += 1 
            if not(self.valid_space(current_piece, grid)): 
                current_piece.rotation -= 1 

        elif event.key == pygame.K_SPACE: 
            self._move_to_bottom(current_piece, grid)

        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE: 
            sys.exit()

    def _move_to_bottom(self, current_piece, grid): 
        while True: 
            current_piece.y += 1 
            if not(self.valid_space(current_piece, grid)): 
                current_piece.y -= 1 
                break


    def _key_up_event(self,event, current_piece, grid): 
        pass 
        # fast move function with key down button

    def main_menu(self):

    
        win = pygame.display.set_mode((self.settings.s_width,self.settings.s_height))
        pygame.display.set_caption('Tetris')
        run = True
        while run: 
            pygame.mixer.music.play(-1)
            win.fill(self.settings.game_background_color)
            self.draw_text_middle('Press Any Key to Start', 60, self.settings.text_color, win)
            self.draw_text('Tetris', 100, self.settings.text_color,
                           self.settings.top_left_x + self.settings.play_width/2,
                           self.settings.top_left_y + 50,
                            win)
            pygame.display.update() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN: 
                    self.main(win)

        pygame.display.quit()

if __name__ == '__main__':
    tetris = Tetris()
    tetris.main_menu()
