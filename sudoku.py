import pygame
import copy
import random
pygame.init()

WIDTH = 801
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption('Sudoku')

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)

sudoku = [
    [9,0,0,0,8,0,0,0,4],
    [0,1,4,5,0,0,0,0,0],
    [0,0,0,0,0,0,0,6,1],
    [0,8,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,3,2,6],
    [0,0,0,7,0,3,0,0,0],
    [0,0,3,0,7,9,2,0,0],
    [0,0,9,0,0,0,0,0,0],
    [0,0,5,2,0,8,0,9,0]
]
solved_sudoku = copy.deepcopy(sudoku)
#----------------------------------------------------------------------
# Solve Sudoku.
def valid(bd, num, cord):
    #row check
    for i in range(len(bd[0])):
        if bd[cord[0]][i] == num and i != cord[1]:
            return False
    #col check
    for i in range(len(bd)):
        if bd[i][cord[1]] == num and i != cord[0]:
            return False
        
    pt = (cord[0]//3,cord[1]//3)
    for i in range(pt[0]*3,pt[0]*3+3):
        for j in range(pt[1]*3,pt[1]*3+3):
            if bd[i][j] == num and (i,j) != cord:
                return False
    return True

# for finding the first empty space (0)
def first_empty(bd):
    for i in range(len(bd)):
        for j in range(len(bd[0])):
            if bd[i][j] == 0:
                return (i,j)    

#check if the last element is filled
def last_elem(bd):
    for row in bd:
        if 0 in row:
            return False
    return True

# solving Sudoku using backtrack
def fill(bd):
    if last_elem(bd):
        return bd
        
    i , j = first_empty(bd)
    for k in range(1,10):
        if valid(bd,k,(i,j)):
            bd[i][j] = k
            if fill(bd):
                return bd
            bd[i][j] = 0

#-------------------------------------------------------------------------
solved_sudoku = fill(solved_sudoku)

# ------------------------------------------------------------------------

class Box: # class of box of sudoku
    def __init__(self,row,col,width,value,corr_value):
        self.total_box = 9
        self.color = WHITE
        self.border_color = RED
        self.row = row
        self.col = col
        self.width = width
        self.x = (row*width)
        self.y = (col*width)
        self.is_clicked_check = False
        self.value = value
        self.temp_value = ''
        self.correct_value = corr_value
    
    def create_box(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

    def get_pos(self):
        return self.row , self.col
    
    def is_clicked(self,win):
        if self.is_clicked_check:
           draw_boarder(win,self.color,self.border_color,self.x,self.y,self.width,5)
        
    def value_display(self,win,value,color):

        font = pygame.font.SysFont('arial',int(self.width*0.8))
        text = font.render(str(value),True,color)
        x = self.row * self.width + self.width // 2 - text.get_width() // 2
        y = self.col * self.width + self.width // 2 - text.get_height() // 2
        win.blit(text,(x,y))
    
    def is_correct(self):
        if not self.value:
            return self.temp_value == self.correct_value
    
    def display(self,win):
        if self.value== 0 :
            self.value = ''
        self.value_display(win,self.value,BLACK)
        self.display_temp_value(win)
    
    def display_temp_value(self,win):
        if not self.value:
            self.value_display(win,self.temp_value,GREY)
     
def draw_boarder(win,org_color,color,x,y,width,border_width):
    pygame.draw.rect(win,color,(x,y,width,width))
    pygame.draw.rect(win,org_color,(x+border_width,y+border_width,(width)-(border_width*2),(width)-(border_width*2)))
    
def make_boxes(width,sudoku):
    grid = []
    gap = width//9
    for i in range(9):
        grid.append([])
        for j in range(9):
            box = Box(i,j,gap,sudoku[j][i],solved_sudoku[j][i])
            grid[i].append(box)
    
    return grid
    
def draw_grid(win,width):
    rows = 9
    gap = width // rows
    for i in range(rows):
        if i % 3 == 0 and i != 0:
            pygame.draw.line(win,BLACK,(i*gap,0),(i*gap,width),3)
            pygame.draw.line(win,BLACK,(0,i*gap),(width,i*gap),3)
        else:
            pygame.draw.line(win,BLACK,(i*gap,0),(i*gap,width),1)
            pygame.draw.line(win,BLACK,(0,i*gap),(width,i*gap),1)

def draw(win,grid,width):
    win.fill(WHITE)
    
    for row in grid:
        for spot in row:
            spot.create_box(win)
            spot.is_clicked(win)
            spot.display(win)
            
    draw_grid(win,width)
    pygame.display.update()

def get_clicked_pos(pos,width):
    gap= width // 9
    y , x = pos
    row = y // gap
    col = x // gap
    return row,col

def get_pos_selected(grid):
    for row in grid:
        for bx in row:
            if bx.is_clicked_check == True:
                return bx.get_pos()

def move_red_boarder_with_keyboard(event,grid,x,y):
    
    if event.key == pygame.K_DOWN:
        try:
            grid[x][y].is_clicked_check = False
            grid[x][y+1].is_clicked_check = True            
        except IndexError:
            grid[x][y].is_clicked_check = False
            grid[x][0].is_clicked_check = True
            
    if event.key == pygame.K_UP:
        try:
            grid[x][y].is_clicked_check = False
            grid[x][y-1].is_clicked_check = True            
        except IndexError:
            grid[x][y].is_clicked_check = False
            grid[x][y].is_clicked_check = True
            
    if event.key == pygame.K_LEFT:
        try:
            grid[x][y].is_clicked_check = False
            grid[x-1][y].is_clicked_check = True 
                       
        except IndexError:
            grid[x][y].is_clicked_check = False
            grid[x][y].is_clicked_check = True
            
    if event.key == pygame.K_RIGHT:
        try:
            grid[x][y].is_clicked_check = False
            grid[x+1][y].is_clicked_check = True            
        except IndexError:
            grid[x][y].is_clicked_check = False
            grid[0][y].is_clicked_check = True

def change_temp_value(event,grid,x,y,key):
    cmd = 'pygame.K_'+str(key)
    if event.key == eval(cmd):
        grid[x][y].temp_value = key

def if_value_is_correct(grid,x,y):
    if grid[x][y].is_correct():
        grid[x][y].value = grid[x][y].temp_value
        
    else:
        grid[x][y].temp_value = ''

def show_solving(win,width,bd,grid):
    for row in grid:
        for box in row:
            for _ in range(10):
                if not box.value:
                    i = random.randint(1,9)
                    box.temp_value = i
                    draw(win,grid,width)
            box.value = box.correct_value
    
            
def start_screen(win,width):
    win.fill(WHITE)
    txt = '''This is a sudoku Game.
    - Press any key to start
    - The red outline show the selected box. 
    - Any number pressed will be entered in the box.
    - To fix the selection and see if its correct press ENTER.
    - If multiple temp values are entered press SPACE for the same.
    - Press BACKSPACE to solve Sudoku.'''
    font = pygame.font.Font(None, 36)  # You can customize the font or provide a font file path

    # Render each line of the text
    lines = [font.render(line, True, BLACK) for line in txt.split('\n')]

    # Calculate total height for all lines
    total_height = sum(line.get_height() for line in lines)

    # Calculate starting y-coordinate for centering
    y = (width - total_height) // 2

    # Calculate starting x-coordinate for left alignment
    x = 20

    # Blit each line onto the window
    for line in lines:
        win.blit(line, (x, y))
        y += line.get_height()  # Move down for the next line

    pygame.display.update()

 
def main(win,width):
    run = True
    grid = make_boxes(width,sudoku)
    grid[0][0].is_clicked_check = True # make the first box selected
    Started = False
    screen = [True,False]
    while run:
        if screen[0]:
            start_screen(win,width)
        x,y = get_pos_selected(grid)
        if screen[1]:
            draw(win,grid,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if Started:
                continue
            if (event.type == pygame.KEYDOWN )and screen:
                screen[0] = False
                screen[1]= True
                
            if screen[1]:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    row,col = get_clicked_pos(pos,width)
                    box = grid[row][col]
                    grid[x][y].is_clicked_check = False
                    box.is_clicked_check = True
                if event.type == pygame.KEYDOWN:
                    move_red_boarder_with_keyboard(event,grid,x,y) # to move the selected box
                    # Fill the box with number
                    for key in range(1,10):
                        change_temp_value(event,grid,x,y,key)
                    if event.key == pygame.K_RETURN:
                        if_value_is_correct(grid,x,y)
                
                    if event.key == pygame.K_SPACE:
                        for i in range(len(grid)):
                            for j in range(len(grid[0])):
                                if_value_is_correct(grid,i,j)
                                
                    if event.key == pygame.K_BACKSPACE:
                        Started = True
                        
                        show_solving(win,width,sudoku,grid)
                    
    pygame.quit()

main(WIN,WIDTH)
