import pygame
import pygame.freetype

#Credits to plastic astronaut: https://www.reddit.com/r/pygame/comments/v3ofs9/draw_arrow_function/
def draw_arrow(
        surface: pygame.Surface,
        start: pygame.Vector2,
        end: pygame.Vector2,
        color: pygame.Color,
        body_width: int = 5,
        head_width: int = 30,
        head_height: int = 40,
    ):
    """Draw an arrow between start and end with the arrow head at the end.

    Args:
        surface (pygame.Surface): The surface to draw on
        start (pygame.Vector2): Start position
        end (pygame.Vector2): End position
        color (pygame.Color): Color of the arrow
        body_width (int, optional): Defaults to 2.
        head_width (int, optional): Defaults to 4.
        head_height (float, optional): Defaults to 2.
    """
    arrow = start - end
    angle = arrow.angle_to(pygame.Vector2(0, -1))
    body_length = arrow.length() - head_height

    # Create the triangle head around the origin
    head_verts = [
        pygame.Vector2(0, head_height / 2),  # Center
        pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
        pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
    ]
    # Rotate and translate the head into place
    translation = pygame.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
    for i in range(len(head_verts)):
        head_verts[i].rotate_ip(-angle)
        head_verts[i] += translation
        head_verts[i] += start

    pygame.draw.polygon(surface, color, head_verts)

    # Stop weird shapes when the arrow is shorter than arrow head
    if arrow.length() >= head_height:
        # Calculate the body rect, rotate and translate into place
        body_verts = [
            pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
            pygame.Vector2(body_width / 2, body_length / 2),  # Topright
            pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
            pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
        ]
        translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
        for i in range(len(body_verts)):
            body_verts[i].rotate_ip(-angle)
            body_verts[i] += translation
            body_verts[i] += start

        pygame.draw.polygon(surface, color, body_verts)

def render(screen:pygame.Surface, map:list[list[tuple[int, int, int, int, int]]], actions:list[list[int]], purplecash:int, orangecash:int, turn:int, max_turns: int):
    font = pygame.freetype.SysFont("Comic Sans MS", 24)
    bigfont = pygame.freetype.SysFont("Comic Sans MS", 30)
    biggerfont = pygame.freetype.SysFont("Comic Sans MS", 40)
    screen.fill("black")
    for row in range(len(map)):
        for column in range(len(map[0])):
            rect = pygame.Rect(column*100, row*100, 100, 100)
            botrect = pygame.Rect(column*100, row*100+70, 100, 30)
            pygame.draw.rect(screen, (map[row][column][1]*8+63, map[row][column][1]*8+63, map[row][column][1]*8+63), rect, 0)
            pygame.draw.rect(screen, "purple" if map[row][column][3] == 1 else "orange" if map[row][column][3]==-1 else (map[row][column][1]*12+63, map[row][column][1]*12+63, map[row][column][1]*12+63), rect, map[row][column][4]*50//map[row][column][1]+5)
            pygame.draw.rect(screen, "black", rect, 1)
            font.render_to(screen, rect, str(map[row][column][4])+"/"+str(map[row][column][1])+"+"+str(map[row][column][0]), (0, 0, 0))
            if map[row][column][2] > 0: 
                font.render_to(screen, botrect, "$"+str(map[row][column][2]), (0, 255, 0))
    for row in range(len(map)):
        for column in range(len(map[0])):
            midrect = pygame.Rect(column*100+30, row*100+30, 100, 40)
            if actions[row][column] == 0:
                pygame.draw.rect(screen, "blue", pygame.Rect(column*100+30, row*100+45, 40, 10), 0)
                pygame.draw.rect(screen, "blue", pygame.Rect(column*100+45, row*100+30, 10, 40), 0)
            elif actions[row][column] == 5:
                bigfont.render_to(screen, midrect, "$"+str(map[row][column][2]), (0, 255, 0))
            elif actions[row][column] == 1:
                draw_arrow(screen, pygame.Vector2(column*100+35, row*100+30), pygame.Vector2(column*100+35, row*100-30), "red")
            elif actions[row][column] == 2:
                draw_arrow(screen, pygame.Vector2(column*100+70, row*100+35), pygame.Vector2(column*100+130, row*100+35), "red")
            elif actions[row][column] == 3:
                draw_arrow(screen, pygame.Vector2(column*100+65, row*100+70), pygame.Vector2(column*100+65, row*100+130), "red")
            elif actions[row][column] == 4:
                draw_arrow(screen, pygame.Vector2(column*100+30, row*100+65), pygame.Vector2(column*100-30, row*100+65), "red")
    pygame.draw.rect(screen, "black", pygame.Rect(800, 0, 200, 800), 0)
    bigfont.render_to(screen, pygame.Rect(800, 0, 100, 100), f"turn {turn}/{max_turns}" , "red")
    bigfont.render_to(screen, pygame.Rect(850, 100, 100, 100), "$"+str(purplecash), "purple")
    bigfont.render_to(screen, pygame.Rect(850, 600, 100, 100), "$"+str(orangecash), "orange")
    
    