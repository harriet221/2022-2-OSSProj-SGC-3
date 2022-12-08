import pygame
import pygame_menu
from os import system
import register
import pyautogui as pg
import dataLoad
from Defs import *

pygame.mixer.init()


# game variables
bgmsound = pygame.mixer.Sound(Sounds.bgm.value)

pygame.init()
infoObject = pygame.display.Info()
size = [int(infoObject.current_w*Display.w_init.value),
        int(infoObject.current_h*Display.h_init.value)]
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption(Content.gamename.value)

# 창이 resize되었는지 여부 체크
def on_resize() -> None:
    window_size = screen.get_size()
    new_w, new_h = window_size[Utilization.x.value], window_size[Utilization.y.value]
    menu.resize(new_w, new_h)


# 로그인 전 보여지는 메뉴 화면(로그인, 회원가입)

def show_signinup():
    menu.clear()
    menu.add.image(Images.logo.value,
                   angle=Display.angle.value, scale=Display.large_scale.value)
    menu.add.button(Content.signin_btn.value, login)
    menu.add.button(Content.signup_btn.value, sign_up)
    menu.add.button(Content.quit_btn.value, pygame_menu.events.EXIT)

# 로그인 후 보여지는 메뉴 화면
def show_mode():
    menu.clear()
    menu.add.image(Images.logo.value,
                   angle=Display.angle.value, scale=Display.large_scale.value)
    menu.add.button(Content.start_btn.value, start_the_game)
    menu.add.button(Content.rank_btn.value, rank)
    menu.add.button(Content.store_btn.value, store)
    menu.add.button(Content.help_btn.value, help)
    menu.add.button(Content.about_btn.value, about)
    menu.add.toggle_switch(Content.sound_btn.value, False, sound)
    menu.add.button(Content.quit_btn.value, pygame_menu.events.EXIT)

def start_the_game():
    from mainGame import startGame
    startGame(True)

def rank(): # 랭킹페이지
    menu.clear()
    table=menu.add.table(table_id=Content.tb_rank.value) # 랭킹 테이블 생성
    table.default_cell_padding=Display.rank_padding.value
    table.default_cell_align=pygame_menu.locals.ALIGN_CENTER
    table.add_row(Content.rank_rowname.value,cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD,cell_padding=Display.rank_idx_padding.value)

    rank_list=dataLoad.rankList_get() # DB에서 랭킹리스트 가져오기
    for rank in rank_list:
        rank[2]=format(rank[2],',') # 큰 숫자는 ,로 구분
        table.add_row(rank,cell_font_size=Display.description_fontsize.value)

    menu.add.vertical_margin(Display.small_margin.value)
    menu.add.button(Content.back_btn.value, show_mode) # 뒤로가기 버튼

# help 페이지
def help():
    menu.clear()
    menu.add.label(Content.help_title.value, font_size=Display.title_fontsize.value, padding=Display.padding_large.value)
    # story
    menu.add.label(Content.story.value, font_size=Display.description_fontsize.value)

    # game rule
    # key control
    menu.add.label(Content.rule.value, font_size=Display.description_fontsize.value)
    # key images
    left_img = menu.add.image(Images.key_left.value,
                              angle=Display.angle.value, scale=Display.small_scale.value)
    right_img = menu.add.image(Images.key_right.value,
                               angle=Display.angle.value, scale=Display.small_scale.value)
    # key table
    table = menu.add.table(font_size=Display.description_fontsize.value, padding=Display.padding_small.value)
    table.add_row([left_img, Content.ruletable_row1.value])
    table.add_row([right_img, Content.ruletable_row2.value])
    menu.add.vertical_margin(Display.small_margin.value)

    # enemy HP detail
    menu.add.label(Content.hp.value, font_size=Display.description_fontsize.value)
    # enemy1 images
    enemy1_img1 = menu.add.image(Images.black_knight.value, angle=Display.angle.value, scale=Display.large_scale.value)
    enemy1_img2 = menu.add.image(Images.bat.value, angle=Display.angle.value, scale=Display.large_scale.value)
    enemy1_img3 = menu.add.image(Images.pirate_ship.value, angle=Display.angle.value, scale=Display.large_scale.value)
    enemy1_img4 = menu.add.image(Images.card_jack.value, angle=Display.angle.value, scale=Display.large_scale.value)
    enemy1_img5 = menu.add.image(Images.snake.value, angle=Display.angle.value, scale=Display.large_scale.value)
    # enemy2 images
    enemy2_img1 = menu.add.image(Images.white_king.value, angle=Display.angle.value, scale=Display.large_scale.value)
    enemy2_img2 = menu.add.image(Images.lizard.value, angle=Display.angle.value, scale=Display.large_scale.value)
    enemy2_img3 = menu.add.image(Images.kraken.value, angle=Display.angle.value, scale=Display.large_scale.value)
    enemy2_img4 = menu.add.image(Images.card_queen.value, angle=Display.angle.value, scale=Display.large_scale.value)
    enemy2_img5 = menu.add.image(Images.desert_scolpion.value, angle=Display.angle.value, scale=Display.large_scale.value)
    # enemy table
    table2 = menu.add.table(font_color=Color.black.value, font_size=Display.description_fontsize.value,
                            padding=Display.padding_small.value, background_color=Color.white.value)
    table2.add_row([enemy1_img1, enemy1_img2, enemy1_img3, enemy1_img4, enemy1_img5, Content.hptable_row1.value])
    table2.add_row([enemy2_img1, enemy2_img2, enemy2_img3, enemy2_img4, enemy2_img5, Content.hptable_row2.value])
    menu.add.vertical_margin(Display.small_margin.value)
    menu.add.button(Content.back_btn.value, show_mode)

# about 페이지
def about():
    menu.clear()
    menu.add.label(Content.about_title.value, font_size=Display.title_fontsize.value,
                   padding=Display.padding_large.value)  # about page title

    menu.add.label(Content.license.value, font_size=Display.description_fontsize.value)
    menu.add.label(Content.license_detail.value, font_size=Display.description_fontsize.value)
    menu.add.vertical_margin(Display.small_margin.value)

    menu.add.label(Content.source.value, font_size=Display.description_fontsize.value)
    menu.add.url(Url.basecode1.value, Content.basecode1.value, underline=False, font_color=Color.white.value, font_size=Display.reference_fontsize.value)
    menu.add.url(Url.basecode2.value, Content.basecode2.value, underline=False, font_color=Color.white.value, font_size=Display.reference_fontsize.value)
    menu.add.url(Url.pixabay.value, Content.imagesource.value, underline=False, font_color=Color.white.value, font_size=Display.reference_fontsize.value)
    menu.add.url(Url.envato.value, Content.soundesource.value, underline=False, font_color=Color.white.value, font_size=Display.reference_fontsize.value)

    menu.add.label(Content.creators.value, font_size=Display.description_fontsize.value)

    menu.add.url(Url.ourgithub.value, Content.github.value, font_color=Color.white.value, font_size=Display.reference_fontsize.value)
    menu.add.vertical_margin(Display.small_margin.value)
    menu.add.button(Content.back_btn.value, show_mode)

# True가 반환될경우 소리가 켜지고 아니면 꺼짐
def sound(sound):
    if sound == True:
        bgmsound.play()
    else:
        bgmsound.stop()


# 회원가입 기능
def sign_up():
    menu.clear()
    email = menu.add.text_input(Content.email_input.value, id=Content.email.value) # 이메일 입력
    password = menu.add.text_input(Content.pw_input.value, password=True, id=Content.pw.value) # 비밀번호 입력
    menu.add.label(Content.pwref.value, font_size=Display.reference_fontsize.value)
    conFirmPassword = menu.add.text_input(Content.confirm_pw_input.value, password=True, id=Content.pw.value) # 비밀번호 재입력
    menu.add.button(Content.submit_btn.value, sign_up_button, email, password, conFirmPassword) # 제출버튼
    menu.add.button(Content.back_btn.value, show_signinup)


# 회원가입 제출 버튼
def sign_up_button(email, password, conFirmPassword):
    registerReturn = register.register(
        email.get_value(), password.get_value(), conFirmPassword.get_value())
    if registerReturn == 1: # 회원가입 성공시, 성공 메시지 출력
        print(pg.alert(text=Content.signupmsg.value, title=Content.signup.value))
    else:
        print(pg.alert(text=Content.errormsg.value, title=Content.error.value))


# 비밀번호 재설정 페이지
def resetPassword():
    menu.clear()
    email = menu.add.text_input(Content.email_input.value, id=Content.email.value)
    menu.add.button(Content.submit_btn.value, resetPassword_Button, email)
    menu.add.button(Content.signin_btn.value, login) # 로그인 페이지로 이동
    menu.add.button(Content.back_btn.value, show_signinup)


def resetPassword_Button(email): 
    register.passwordReset(email.get_value()) # 비밀번호 재설정 수행
    print(pg.alert(text=Content.resetmsg.value, title=Content.reset.value)) 

# 로그인

def login():
    menu.clear()
    # 개발시 편의를 위해 default값 추가함 (추후 삭제 예정)
    email = menu.add.text_input(Content.email_input.value, id=Content.email.value, default=Content.default_email.value) # check
    password = menu.add.text_input(Content.pw_input.value, password=True, id=Content.pw.value)
    menu.add.button(Content.submit_btn.value, loginButton, email, password)  # submit 버튼을 누르면 로그인 시도
    menu.add.button(Content.reset_btn.value, resetPassword)
    menu.add.button(Content.back_btn.value, show_signinup)


def loginButton(email, password):
    
    user_email = email.get_value()
    register.email=user_email
    login = register.Login(email.get_value(), password.get_value())
    if login != 0:  # 로그인에 성공하면 다음으로 넘어감
        show_mode()  # 메인 메뉴 페이지로 넘어가기
    else:
        print(pg.alert(text=Content.errormsg.value, title=Content.error.value)) # 실패시, 실패 안내 메시지창 출력

# 상점
def store():
    menu.clear()
    menu.add.label(Content.store_title.value, font_size=Display.title_fontsize.value, padding=Display.padding_large.value)  # page title
    menu.add.button(Content.buyitem_btn.value,Buy_page) # 아이템 구매페이지로 이동
    menu.add.button(Content.applyitem_btn.value,apply_item_page) # 아이템 적용 페이지로 이동
    menu.add.button(Content.givecoin_btn.value,give_coin_page) # 코인 선물 페이지
    menu.add.vertical_margin(Display.small_margin.value)
    menu.add.button(Content.back_btn.value, show_mode) # 뒤로가기 버튼

def Buy_page():
    menu.clear()
    menu.add.label(Content.coin.value)
    menu.add.label(dataLoad.coin_get(register.user)) #  현재 코인 표시
    menu.add.label(Content.item_category.value)
    item_list= Content.items.value
    buy_list = dataLoad.item_buyList_get(register.user) # 사용자가 구매한 아이템 리스트 가져옴
    for item in item_list: 
        if item in buy_list: # 구매한 아이템일 경우, 흑색 이미지 사용 및 구매 버튼 비활성화
            image_path=Content.img_path.value + item + Content.img_have.value
            menu.add.image(image_path,
                        angle=Display.angle.value, scale=Display.medium_scale.value)
            menu.add.button(Content.buy_btn.value, Buy_check)
        else: # 구매하지 않은 아이템일 경우, 컬러 이미지 사용 및 구매 버튼 활성화
            weapon_image_path=Content.img_path.value+item+Content.img_size256.value
            price_image_path=Content.img_path.value+item+Content.img_price.value
            menu.add.image(weapon_image_path,
                    angle=Display.angle.value, scale=Display.medium_scale.value)
            menu.add.image(price_image_path,
                    angle=Display.angle.value, scale=Display.medium_scale.value)
            menu.add.button(Content.buy_btn.value, Buy, register.user,item)

    menu.add.vertical_margin(Display.small_margin.value)
    menu.add.button(Content.back_btn.value, store) # 뒤로가기 버튼


def apply_item_page():
    menu.clear()
    buy_list = dataLoad.item_buyList_get(register.email)
    for item in buy_list:  # 사용자가 구매한 아이템 리스트 보여줌
        image_path = Content.img_path.value+item+Content.img_size256.value
        menu.add.image(image_path, angle=Display.angle.value, scale=Display.medium_scale.value)  # 구매한 아이템 이미지
        menu.add.button(Content.apply_btn.value, apply_current_item,register.email,item)  # 아이템 적용 버튼

    menu.add.vertical_margin(Display.small_margin.value)
    menu.add.label(Content.applied_item.value)
    item = dataLoad.item_apply_get(register.email)  # 현재 게임에 적용된 아이템 보여줌
    image_path = Content.img_path.value+item+Content.img_size256.value #### Defs.py에 추가

    menu.add.button(Content.reload.value, apply_item_page) # 현재적용 아이템 보기
    menu.add.image(image_path, angle=Display.angle.value, scale=Display.medium_scale.value)

    menu.add.vertical_margin(Display.small_margin.value)
    menu.add.button(Content.back_btn.value, store)

def give_coin_page(): # 코인 선물 페이지
    menu.clear()
    menu.add.label(Content.gift_info.value)
    friend_email = menu.add.text_input(Content.email_input.value) # 친구 이메일 입력
    coin = menu.add.text_input(Content.coin_input.value) # 선물하고자 하는 코인량 입력
    menu.add.button(Content.submit_btn.value,giveButton,friend_email,coin) # 입력값 제출 버튼

    menu.add.vertical_margin(Display.small_margin.value)
    menu.add.button(Content.back_btn.value, store) # 뒤로가기 버튼

def giveButton(friend_email,coin): 
    dataLoad.coin_give(register.email,friend_email.get_value(),coin.get_value()) # 친구에게 메일 선물하기 기능 수행
    print(pg.alert(text=Content.giveok_msg.value, title=Content.giveok_msgtitle.value))

def Buy(user,item): #아이템 구매 함수
    dataLoad.item_buy(user,item)

def Buy_check(): # 이미 구매한 아이템의 경우, 안내 메시지 출력
    print(pg.alert(text=Content.have_msg.value, title=Content.have_msgtitle.value))

def apply_current_item(user,item): # 게임play에 아이템 적용 함수
    dataLoad.item_apply(user,item)

def give_coin(user,coin): # 코인 선물하기 함수
    dataLoad.coin_give(user,coin)

# 여기서부터가 메인화면
menu_image = pygame_menu.baseimage.BaseImage(
    image_path=Images.background.value, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY)
mytheme = pygame_menu.themes.THEME_GREEN.copy()

mytheme.background_color = menu_image
mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE

# 첫 화면 페이지(로그인, 회원가입 버튼)
menu = pygame_menu.Menu(Content.none.value, size[Utilization.x.value], size[Utilization.y.value], theme=mytheme)


if __name__ == Content.main.value:
    # 첫 화면 페이지(로그인, 회원가입 버튼)
    show_signinup()
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

else:
    size = [int(infoObject.current_w),
        int(infoObject.current_h)]
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    show_mode()
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

        menu.update(events)
        menu.draw(screen)

        pygame.display.flip()

    
# menu.mainloop(screen)
# pygame.quit()