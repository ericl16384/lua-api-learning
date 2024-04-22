import math, time
import pygame

screen = None

tile_colors = {
    "empty": "white",
    "wall": "red"
}

tile_size = 20
def transform(pos, tile_offset=False):
    if tile_offset:
        pos = [i-0.5 for i in pos]
    center = screen.get_rect().center
    return (
        pos[0]*tile_size+center[0],
        pos[1]*tile_size+center[1]
    )

def init():
    pygame.init()

    global screen
    screen = pygame.display.set_mode((1024, 576))

def draw_map(map, robo_pos, facing):
    screen.fill("black")
    for pos, value in map.items():
        pygame.draw.rect(screen, tile_colors[value], (
            transform(pos, True), (tile_size, tile_size)
        ))
        pygame.draw.rect(screen, "black", (
            transform(pos, True), (tile_size, tile_size)
        ), 1)

    robot_angles = (0, math.pi*3/4, math.pi*5/4)
    r = facing * math.pi/2
    robot_points = [(math.cos(t+r)/2, math.sin(t+r)/2) for t in robot_angles]
    robot_points = [(p[0]+robo_pos[0], p[1]+robo_pos[1]) for p in robot_points]

    # print(robo_pos)

    pygame.draw.polygon(screen, "blue", [transform(p) for p in robot_points])

    for i in range(100 * 1):
        pygame.display.flip()
        pygame.event.get()
        time.sleep(1 / 100)