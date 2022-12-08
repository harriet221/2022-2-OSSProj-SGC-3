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
pygame.display.set_caption(Content.main.value)

# 창이 resize되었는지 여부 체크
def on_resize() -> None:
    window_size = screen.get_size()
    new_w, new_h = window_size[Utilization.x.value], window_size[Utilization.y.value]
    menu.resize(new_w, new_h)
    print(f'New menu size: {menu.get_size()}') # check


# 스코어, 랭킹, restart, main 페이지 연결
score = mainGame.total_score
def game_end():
    menu.clear()
    menu.add.label(Content.end.value, font_size=Display.title_fontsize.value, padding=Display.padding_large.value)
    dataLoad.coin_set(user,score) # DB에 코인 저장 기능
    dataLoad.rank(user,score)
    comma_score=format(score,',')
    menu.add.label('Score: %s'%comma_score) ## Defs.py에 저장
    rank_list=dataLoad.rankList_get()
    for rank in rank_list:
        if rank[1]==user:
            current_rank=rank[0]
    print(current_rank)
    menu.add.label('Rank: %d'%current_rank) # rank DB 연결 필요 # 추후 수정  ## Defs.py에 저장
    total_coin=dataLoad.coin_get(user)
    total_coin=format(total_coin,',')
    menu.add.label('Total Coins: %s'%total_coin) ## Defs.py 에 저장
    menu.add.vertical_margin(Display.small_margin.value)
    menu.add.button('Restart',start_the_game) # 수정
    menu.add.button('Main',start_the_mainMenu)
    menu.add.button('Quit',pygame_menu.events.EXIT)

def start_the_game():
    from mainGame import startGame
    startGame(True)

def start_the_mainMenu():
    from mainMenu import show_mode
    show_mode()


# 여기서부터가 메인화면
menu_image = pygame_menu.baseimage.BaseImage(image_path=Images.background.value,drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY)
mytheme = pygame_menu.themes.THEME_GREEN.copy()

mytheme.background_color = menu_image 
mytheme.title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE

# 첫 화면 페이지(로그인, 회원가입 버튼)
menu = pygame_menu.Menu('', size[Utilization.x.value], size[Utilization.y.value], theme=mytheme)


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

# menu.mainloop(screen)
# pygame.quit()