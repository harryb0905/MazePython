import os
import pygame
from pygame.locals import *
import random

up_img = pygame.image.load(os.path.join('img', 'up.png'))
right_img = pygame.image.load(os.path.join('img', 'right.png'))
down_img = pygame.image.load(os.path.join('img', 'down.png'))
left_img = pygame.image.load(os.path.join('img', 'left.png'))

class Maze:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 800, 800
        self.PIXEL_SIZE = 80
        self.ROWS = self.COLS = int(self.height / self.PIXEL_SIZE)
        self.ENTRY_X, self.ENTRY_Y = (2,0)
        self.EXIT_X, self.EXIT_Y = (random.randint(0,self.COLS-1), self.ROWS-1)
        self.init_x = self.init_y = -1

    def search(self, x, y, grid):

        # Image logic
        img = None
        if x > self.init_x and y == self.init_y:
            img = right_img
        elif y < self.init_y and x == self.init_x:
            img = up_img
        elif y > self.init_y and x == self.init_x:
            img = down_img
        elif x < self.init_x and y == self.init_y:
            img = left_img
        
        # Detection logic
        if grid[x][y] == 3:
            print('found exit at %d,%d' % (x, y))
            return True
        elif grid[x][y] == 1:
            print('wall at %d,%d' % (x, y))
            return False
        elif grid[x][y] == 4:
            print('visited before at %d,%d' % (x, y))
            return False
        
        print('visiting %d,%d' % (x, y))
        self.init_x = x
        self.init_y = y

        # mark as visited
        grid[x][y] = 4

        # Display image
        if img is not None:
            self._display_surf.blit(img, (x*self.PIXEL_SIZE+(self.PIXEL_SIZE/3),y*self.PIXEL_SIZE+(self.PIXEL_SIZE/4)))
            pygame.display.flip()

        # explore neighbors clockwise starting by the one on the right
        if ((x < len(grid)-1 and self.search(x+1, y, grid))
            or (y > 0 and self.search(x, y-1, grid))
            or (x > 0 and self.search(x-1, y, grid))
            or (y < len(grid)-1 and self.search(x, y+1, grid))):
            return True

        return False


    def on_init(self):

        # Init modules and window
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        
        # Init maze grid
        grid = [[0 for i in range(self.ROWS)] for j in range(self.COLS)]
        # Entry and exit
        grid[self.ENTRY_X][self.ENTRY_Y] = 2
        grid[self.EXIT_X][self.EXIT_Y] = 3

        # Draw random maze
        num_blocks = random.randint(1,self.ROWS)
        for i in range(num_blocks):
            x = random.randint(4, self.ROWS) - 1
            y = random.randint(4, self.ROWS) - 1
            grid[x][y] = 1

        # Draw starting grid
        for i in range(self.ROWS):
            for j in range(self.COLS):
                square = pygame.Rect(i*(self.PIXEL_SIZE+1), j*(self.PIXEL_SIZE+1), self.PIXEL_SIZE, self.PIXEL_SIZE)
                # Wall
                if grid[i][j] == 1:
                    pygame.draw.rect(self._display_surf, (102, 102, 102), square)
                # Start point
                elif grid[i][j] == 2:
                    pygame.draw.rect(self._display_surf, (0, 0, 0), square)
                # Exit point
                elif grid[i][j] == 3:
                    pygame.draw.rect(self._display_surf, (0, 153, 51), square)
                # Empty space
                else:
                    pygame.draw.rect(self._display_surf, (255, 255, 230), square)
                
        # Update UI
        pygame.display.flip()

        # Perform search algorithm
        found = self.search(self.ENTRY_X, self.ENTRY_Y, grid)
        print("Found: ", found)

        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        try:
            while( self._running ):
                for event in pygame.event.get():
                    self.on_event(event)
                self.on_loop()
                self.on_render()
        except KeyboardInterrupt:
            pass
        self.on_cleanup()
 
if __name__ == "__main__" :
    maze = Maze()
    maze.on_execute()