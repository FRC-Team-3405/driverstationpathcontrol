from networktables import NetworkTables
import math, pygame, pygame.freetype

pygame.init()
window = pygame.display.set_mode((750, 616))
pygame.display.set_caption("Playing Field - 2019")
clock = pygame.time.Clock()

playingfieldimg = pygame.Surface((750, 616))
playingfieldimg.blit(pygame.image.load("playingfield.jpeg"), (0, 0))

MAIN_FONT = pygame.freetype.SysFont("Serif", 18)
LABEL_FONT = pygame.freetype.SysFont("Monospace", 16, bold=True)

NetworkTables.initialize(server='roborio-3405-frc.local')
table = NetworkTables.getTable('SmartDashboard')

listofpoints = []
running = True
global point1
global point2


class Point:
    def __init__(self, pos, id, group):
        self.pos = pos
        self.id = id
        self.group = group
        self.active = False


def activate():
    pos = pygame.mouse.get_pos()
    global point1, point2

    for i in listofpoints:
        xoffset = pos[0] - i.pos[0]
        yoffset = pos[1] - i.pos[1]
        dist = math.sqrt((xoffset ** 2) + (yoffset ** 2))

        if dist < 20:
            i.active = True
            if pygame.mouse.get_pressed()[0] and i.id != "Z":
                if point1 == dummy:
                    point1 = i
                elif point2 == dummy:
                    if point1.group != i.group:
                        point2 = i
        else:
            i.active = False


def draw():
    # Draw an information panel giving details about the currently queued and selected paths.
    pygame.draw.rect(window, (0, 0, 0), (0, 0, 200, 350))
    if point1.id != dummy.id and point2.id != dummy.id:
        MAIN_FONT.render_to(window, (15, 15), "Path: " + point1.id + "-" + point2.id, (255, 0, 0))
    MAIN_FONT.render_to(window, (15, 40), "Queued path: " + table.getString("path", "x"), (0, 255, 0))
    MAIN_FONT.render_to(window, (15, 60), "Current path: " + table.getString("current_path", "x"), (0, 0, 255))

    # Draw all the points
    for i in listofpoints:
        if i.id == point1.id:
            pygame.draw.circle(window, (0, 255, 0), i.pos, 15)
        elif i.id == point2.id:
            pygame.draw.circle(window, (255, 0, 0), i.pos, 15)
        elif i.active and i.group != point1.group:
            pygame.draw.circle(window, (0, 0, 255), i.pos, 15)
        else:
            pygame.draw.circle(window, (150, 150, 150), i.pos, 10)
        LABEL_FONT.render_to(window, (i.pos[0] - 5, i.pos[1] - 5), i.id, (0, 0, 0))


def edit():
    global point1
    global point2
    if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
        if point1.id != dummy.id and point2.id != dummy.id:
            table.putString("path", point1.id + "-" + point2.id)
            point1 = dummy
            point2 = dummy

    if pygame.key.get_pressed()[pygame.K_DELETE]:
        point1 = dummy
        point2 = dummy


def addpoint(pos, id, group):
    listofpoints.append(Point(pos, id, group))


def init():
    global point1, point2, dummy
    dummy = Point((0, 0), "Z", "dummy")

    point1 = dummy
    point2 = dummy

    addpoint((650, 70), "A", "rocket")
    addpoint((590, 120), "B", "rocket")
    addpoint((525, 70), "C", "rocket")

    addpoint((525, 550), "K", "rocket")
    addpoint((590, 500), "L", "rocket")
    addpoint((650, 550), "M", "rocket")

    addpoint((250, 75), "D", "load")
    addpoint((250, 538), "J", "load")

    addpoint((250, 225), "E", "home")
    addpoint((325, 225), "F", "home")
    addpoint((325, 300), "G", "home")
    addpoint((325, 375), "H", "home")
    addpoint((250, 375), "I", "home")

    addpoint((525, 250), "R", "cargo")
    addpoint((525, 350), "Q", "cargo")
    addpoint((600, 200), "S", "cargo")
    addpoint((650, 200), "T", "cargo")
    addpoint((700, 200), "U", "cargo")
    addpoint((600, 400), "P", "cargo")
    addpoint((650, 400), "O", "cargo")
    addpoint((700, 400), "N", "cargo")


init()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((0, 0, 0))
    window.blit(playingfieldimg, (0, 0))

    activate()
    edit()
    draw()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
quit()
