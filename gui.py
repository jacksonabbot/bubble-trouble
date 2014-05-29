from pygame.locals import *
from collections import OrderedDict

from game import *
from menu import *

pygame.init()
pygame.display.set_caption('Bubble Trouble')
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 30)
game = Game()


def start_level(level):
    game.load_level(level)
    main_menu.is_active = False
    pygame.mouse.set_visible(False)
    while game.is_running:
        draw_world()
        handle_game_event()
        pygame.display.update()
        game.update()
        clock.tick(FPS)


#def load_level_menu():




def load_level():
    while load_level_menu.is_active:
        load_level_menu.draw()
        handle_menu_event(load_level_menu)
        pygame.display.update()
        clock.tick(FPS)


def quit_game():
    game.is_running = False
    main_menu.is_active = False
    pygame.quit()
    sys.exit()



main_menu = Menu(screen, OrderedDict([('New game', (start_level, 1)), ('Load level', load_level), ('Quit', quit_game)]))

#x = [(comp_lvl, (game.load_level, comp_lvl) for comp_lvl in game.levels_available)]
load_level_menu = Menu(screen, OrderedDict(
    [(str(comp_lvl), (start_level, comp_lvl)) for comp_lvl in game.levels_available]
))

def draw_ball(ball):
    screen.blit(ball.image, ball.rect)


def draw_player(player):
    screen.blit(player.image, player.rect)


def draw_weapon(weapon):
    screen.blit(weapon.image, weapon.rect)


def draw_message(message, colour):
    label = font.render(message, 1, colour)
    rect = label.get_rect()
    rect.centerx = screen.get_rect().centerx
    rect.centery = screen.get_rect().centery
    screen.blit(label, rect)


def draw_timer():
    timer = font.render(str(game.time_left), 1, RED)
    rect = timer.get_rect()
    rect.bottomleft = 10, WINDOWHEIGHT - 10
    screen.blit(timer, rect)


def draw_world():
    screen.fill((250, 250, 250))
    if game.game_over:
        draw_message("Game over!", RED)
    if game.level_completed:
        draw_message("Well done! Level completed!", BLUE)
    for ball in game.balls:
        draw_ball(ball)
    draw_player(game.player)
    if game.player.weapon.is_active:
        draw_weapon(game.player.weapon)
    draw_timer()


def handle_game_event():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                game.player.moving_left = True
            elif event.key == K_RIGHT:
                game.player.moving_right = True
            elif event.key == K_SPACE and not game.player.weapon.is_active:
                game.player.shoot()
            elif event.key == K_ESCAPE:
                quit_game()
        if event.type == KEYUP:
            if event.key == K_LEFT:
                game.player.moving_left = False
            elif event.key == K_RIGHT:
                game.player.moving_right = False
        if event.type == QUIT:
            quit_game()


def handle_menu_event(menu):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_game()
            if (event.key == pygame.K_UP or event.key == pygame.K_DOWN) and menu.current_option is None:
                menu.current_option = 0
                pygame.mouse.set_visible(False)
            elif event.key == pygame.K_UP and menu.current_option > 0:
                menu.current_option -= 1
            elif event.key == pygame.K_UP and main_menu.current_option == 0:
                menu.current_option = len(menu.options) - 1
            elif event.key == pygame.K_DOWN and menu.current_option < len(menu.options) - 1:
                menu.current_option += 1
            elif event.key == pygame.K_DOWN and menu.current_option == len(menu.options) - 1:
                menu.current_option = 0
            elif event.key == pygame.K_RETURN:
                if not isinstance(menu.functions[menu.options[menu.current_option].text], tuple):
                    menu.functions[menu.options[menu.current_option].text]()
                else:
                    menu.functions[menu.options[menu.current_option].text][0](menu.functions[menu.options[menu.current_option].text][1])

        elif event.type == MOUSEBUTTONUP:
            for option in menu.options:
                if option.is_selected:
                    if not isinstance(menu.functions[option.text], tuple):
                        menu.functions[option.text]()
                    else:
                        menu.functions[option.text][0](menu.functions[option.text][1])
        if pygame.mouse.get_rel() != (0, 0):
            pygame.mouse.set_visible(True)
            menu.current_option = None


while main_menu.is_active:
    main_menu.draw()
    handle_menu_event(main_menu)
    pygame.display.update()
    clock.tick(FPS)

