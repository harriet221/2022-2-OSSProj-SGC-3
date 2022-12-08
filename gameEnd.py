import pygame
import pygame_menu
# import mainMenu
import mainGame
import dataLoad
from register import user
from Defs import *

pygame.mixer.init()

# window screen 초기 설정
pygame.init()
infoObject = pygame.display.Info()
size = [int(infoObject.current_w),int(infoObject.current_h)]
screen = pygame.display.set_mode(size,pygame.RESIZABLE)
pygame.display.set_caption(Content.gameend.value)

# 창이 resize되었는지 여부 체크
def on_resize() -> None:
    window_size = screen.get_size()
    new_w, new_h = window_size[Utilization.x.value], window_size[Utilization.y.value]
    menu.resize(new_w, new_h)


# 게임 종료 후 나타나는 페이지
# 스코어, 랭킹, restart, main 페이지 연결
score = mainGame.total_score
def game_end():
    menu.clear()
    menu.add.label(Content.end.value, font_size=Display.title_fontsize.value, padding=Display.padding_large.value)
    # DB에 코인 저장 기능
    dataLoad.coin_set(user,score)
    dataLoad.rank(user,score)
    comma_score = str(format(score,','))
    print(comma_score)
    menu.add.label(Content.score.value+comma_score)
    rank_list=dataLoad.rankList_get()
    for rank in rank_list:
        if rank[Rank.email_col.value]==user:
            current_rank=str(rank[Rank.rank_col.value])
    menu.add.label(Content.rank.value+current_rank)
    total_coin=dataLoad.coin_get(user)
    total_coin=str(format(total_coin,','))
    menu.add.label(Content.coins.value+total_coin)
    menu.add.vertical_margin(Display.small_margin.value)
    menu.add.button(Content.restart_btn.value,start_the_game)
    menu.add.button(Content.main_btn.value,start_the_mainMenu)
    menu.add.button(Content.quit_btn.value,pygame_menu.events.EXIT)

def start_the_game():
    from mainGame import startGame
    startGame(True)

def start_the_mainMenu():
    from mainMenu import show_mode
    show_mode()


# PYGAME MENU #####
menu_image = pygame_menu.baseimage.BaseImage(
    image_path=Images.background.value,drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY)
mytheme = pygame_menu.themes.THEME_GREEN.copy()

mytheme.background_color = menu_image 
mytheme.title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE

menu = pygame_menu.Menu(Content.none.value, size[Utilization.x.value], size[Utilization.y.value], theme=mytheme)

# 첫 화면 페이지
game_end()
menu.enable()
on_resize() # Set initial size
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.VIDEORESIZE:
            # Update the surface
            if event.w <= Display.minscreen_x.value and event.h <= Display.minscreen_y.value:
                screen = pygame.display.set_mode((Display.minscreen_x.value, Display.minscreen_y.value),
                                                pygame.RESIZABLE)
            else:
                screen = pygame.display.set_mode((event.w, event.h),
                                                pygame.RESIZABLE)
            # Call the menu event
            on_resize()
        pygame.display.update()

    menu.update(events)
    menu.draw(screen)

    pygame.display.flip()