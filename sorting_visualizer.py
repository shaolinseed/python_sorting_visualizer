import pygame
import random
from pygame.constants import QUIT


pygame.init()

class DrawInformation:
    #initalize color constants (tuples)
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
   
    BACKGROUND_COLOR = WHITE

    #grays to color bars
    GRADIENTS = [(128, 128, 128), (160, 160, 160), (192, 192, 192)]

    SIDE_PADDING = 100
    TOP_PADDING = 150

    #constructor 
    def __init__(self, width, height, list):
        self.width = width
        self.height = height
        self.BLACK = 0, 0, 0
        
        #setup window passing width and height as tuple
        self.window = pygame.display.set_mode((width, height))
        self.FONT = pygame.font.SysFont('calibribody', 28)
        self.LARGE_FONT = pygame.font.SysFont('calibribody', 38)
        pygame.display.set_caption("Sorting Algorithm Visualizer")



        self.set_list(list)


    #function to setup dynamic list
    def set_list(self, list):
        self.list = list
        #store the min and max values of list
        self.min_value = min (list)
        self.max_value = max(list)

        #calculate area for each block
        self.block_width = round((self.width - self.SIDE_PADDING) / len(list))
        self.block_height = (self.height - self.TOP_PADDING) // (self.max_value - self.min_value)

        #floor division 
        self.start_x = self.SIDE_PADDING // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Sort | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 35))

    controls = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 65))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_background=False):
    list = draw_info.list
    #only render necessary area of screen (area of bars - text does not change at any point)
    if (clear_background):
        clear_rect = (draw_info.SIDE_PADDING//2, draw_info.TOP_PADDING, 
                    draw_info.width - draw_info.SIDE_PADDING, draw_info.height - draw_info.TOP_PADDING)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(list):
        #starting x position + (number of blocks * block width)
        x = draw_info.start_x + i * draw_info.block_width
        #subtract from min value to find the height relative to the min value
        y =  draw_info.height - (val - draw_info.min_value) * draw_info.block_height

        #every 3 elements reset the gradient of the bar
        color = draw_info.GRADIENTS[i % 3]

        if (i in color_positions):
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x,y, draw_info.block_width, draw_info.height))

    if (clear_background):
        pygame.display.update()



#function to generate random list to sort
def generate_starting_list(n, min_value, max_value):
    list = []

    for i in range(n):
        value = random.randint(min_value, max_value)
        list.append(value)

    return list
        

def main():
    run = True
    clock = pygame.time.Clock()
    
    n = 50
    min_value = 0
    max_value = 100
    sorting = False
    ascending = True

    sorting_algo = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None

    list = generate_starting_list(n, min_value, max_value)
    draw_info = DrawInformation(800, 600, list)

    while run:
        clock.tick(20)

        if sorting:
            try:
                #run next yield of generator
                next(sorting_algo_generator)
            #generator completed    
            except StopIteration:
                sorting = False
        else:
            #update the display
            draw(draw_info, sorting_algo_name, ascending)
        

        pygame.display.update()

        #return list of events since last loop
        for event in pygame.event.get():
            #exit window on exit button click
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                #generate new random list of values
                list = generate_starting_list(n, min_value, max_value)
                #update draw_info
                draw_info.set_list(list)
                sorting = False

            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generator = sorting_algo(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_b and not sorting:
                sorting_algo = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_i and not sorting:
                sorting_algo = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algo = selection_sort
                sorting_algo_name = "Selection Sort"

        
        
    pygame.quit()

#sorting algorithms
def bubble_sort(draw_info, ascending = True):
    list = draw_info.list
    unsorted_until_index = len(list) - 1
    for i in range(unsorted_until_index):
        for j in range(unsorted_until_index - i):
            num1 = list[j]
            num2 = list[j + 1]
            #   ascending case                 descending case
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                #swap variables with 1 line 
                list[j], list[j+1] = list[j + 1], list[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                #yield to give enable main loop to receive input 
                yield True
    return list

def insertion_sort(draw_info, ascending=True):
    list = draw_info.list
    for i in range(1, len(list)):
        current = list[i]
        while True:
            ascending_sort = i > 0 and list[i - 1] > current and ascending
            descending_sort = i > 0 and list[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                #if no condition is true
                break
        
            #swap the values
            list[i] = list[i -1]
            i = i - 1
            list[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            #yield to give enable main loop to receive input 
            yield True

    return list


def selection_sort(draw_info, ascending=True):
    list = draw_info.list

    for i in range(0, len(list) - 1):
        edge_value = i

        for j in range(i + 1, len(list)):
            if (ascending):
                if list[j] < list[edge_value]:
                    edge_value = j
            else:
                if list[j] > list[edge_value]:
                    edge_value = j
        if (edge_value != i):
            list[edge_value], list[i] = list[i], list[edge_value]
            draw_list(draw_info, {i: draw_info.GREEN, edge_value: draw_info.RED}, True)
            yield True


    return list


#if module is directly run execute main function
if __name__ == "__main__":
    main()




