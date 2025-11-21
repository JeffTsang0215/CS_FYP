import pygame, random, os, math, json
from copy import deepcopy

#basic set up for pygame
pygame.init()
pygame.font.init()

new_game = True
god_mod = True

save = {
    'unlock': [True, False, False, False, False],
    'star': [0, 0, 0, 0, 0],
    'current_stage': 0,
}

WIDTH  = int(pygame.display.Info().current_w * 0.65)
HEIGHT = int(WIDTH/1440*960)

def transform_scale(arr):
    return [int(n*WIDTH/1440) for n in arr]
# draw text on screen
# draw text on screen
def text(screen, text_string, color, size, pos, align="left"):
    try:
        my_font = pygame.font.Font('media/LXGWMarkerGothic-Regular.ttf', transform_scale([size])[0])
    except Exception:
        my_font = pygame.font.Font(pygame.font.get_default_font(), transform_scale([size])[0])

    lines = text_string.split('\n')
    x, y = pos
    line_height = my_font.get_linesize()

    # Adjust starting y for centered text block
    if align == "center" or align == "centre":
        total_height = line_height * len(lines)
        y -= total_height / 2

    for line in lines:
        text_surface = my_font.render(line, True, color)
        if align == "left":
            screen.blit(text_surface, (x, y))
        elif align == "center" or align == "centre":
            # For centering, we use the original x from pos, but adjust y for each line
            text_rect = text_surface.get_rect(center=(pos[0], y + text_surface.get_height() / 2))
            screen.blit(text_surface, text_rect)
        y += line_height # Move y down for the next line

def text_sp(screen, text_string, color, size, pos, alpha, align="left"):
    try:
        my_font = pygame.font.Font('media/YujiSyuku-Regular.ttf', transform_scale([size])[0])
    except Exception:
        my_font = pygame.font.Font(pygame.font.get_default_font(), transform_scale([size])[0])

    lines = text_string.split('\n')
    x, y = pos
    line_height = my_font.get_linesize()

    # Adjust starting y for centered text block
    if align == "center" or align == "centre":
        total_height = line_height * len(lines)
        y = pos[1] - total_height / 2

    for line in lines:
        text_surface = my_font.render(line, True, color)
        text_surface.set_alpha(alpha)
        if align == "left":
            screen.blit(text_surface, (x, y))
        elif align == "center" or align == "centre":
            text_rect = text_surface.get_rect(center=(pos[0], y + text_surface.get_height() / 2))
            screen.blit(text_surface, text_rect)
        y += line_height

# convert romaji to katagana
def textinput(inp):
    out = []
    # read input, remove already read character
    while len(inp) != 0:
        try:
            if inp[0] == "a":
                out.append("あ")
                inp = inp[1:]
            elif inp[0] == "i":
                out.append("い")
                inp = inp[1:]
            elif inp[0] == "u":
                out.append("う")
                inp = inp[1:]
            elif inp[0] == "e":
                out.append("え")
                inp = inp[1:]
            elif inp[0] == "o":
                out.append("お")
                inp = inp[1:]
            elif inp[0] == "k":
                if inp[1] == "k":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "a":
                    out.append("か")
                    inp = inp[2:]
                elif inp[1] == "i":
                    out.append("き")
                    inp = inp[2:]
                elif inp[1] == "u":
                    out.append("く")
                    inp = inp[2:]
                elif inp[1] == "e":
                    out.append("け")
                    inp = inp[2:]
                elif inp[1] == "o":
                    out.append("こ")
                    inp = inp[2:]
                elif inp[1] == "y" and inp [2] == "a":
                    out.append("きゃ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "u":
                    out.append("きゅ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "o":
                    out.append("きょ")
                    inp = inp[3:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            elif inp[0] == "g":
                if inp[1] == "g":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "a":
                    out.append("が")
                    inp = inp[2:]
                elif inp[1] == "i":
                    out.append("ぎ")
                    inp = inp[2:]
                elif inp[1] == "u":
                    out.append("ぐ")
                    inp = inp[2:]
                elif inp[1] == "e":
                    out.append("げ")
                    inp = inp[2:]
                elif inp[1] == "o":
                    out.append("ご")
                    inp = inp[2:]
                elif inp[1] == "y" and inp [2] == "a":
                    out.append("ぎゃ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "u":
                    out.append("ぎゅ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "o":
                    out.append("ぎょ")
                    inp = inp[3:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            elif inp[0] == "s":
                if inp[1] == "s":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "a":
                    out.append("さ")
                    inp = inp[2:]
                elif inp[1] == "i":
                    out.append("し")
                    inp = inp[2:]
                elif inp[1] == "h" and inp [2] == "i":
                    out.append("し")
                    inp = inp[3:]
                elif inp[1] == "u":
                    out.append("す")
                    inp = inp[2:]
                elif inp[1] == "e":
                    out.append("せ")
                    inp = inp[2:]
                elif inp[1] == "o":
                    out.append("そ")
                    inp = inp[2:]
                elif inp[1] == "y" and inp [2] == "a":
                    out.append("しゃ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "u":
                    out.append("しゅ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "o":
                    out.append("しょ")
                    inp = inp[3:]
                elif inp[1] == "h" and inp [2] == "a":
                    out.append("しゃ")
                    inp = inp[3:]
                elif inp[1] == "h" and inp [2] == "u":
                    out.append("しゅ")
                    inp = inp[3:]
                elif inp[1] == "h" and inp [2] == "o":
                    out.append("しょ")
                    inp = inp[3:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            elif inp[0] == "z":
                if inp[1] == "z":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "a":
                    out.append("ざ")
                    inp = inp[2:]
                elif inp[1] == "i":
                    out.append("じ")
                    inp = inp[2:]
                elif inp[1] == "u":
                    out.append("ず")
                    inp = inp[2:]
                elif inp[1] == "e":
                    out.append("ぜ")
                    inp = inp[2:]
                elif inp[1] == "o":
                    out.append("ぞ")
                    inp = inp[2:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            elif inp[0] == "j":
                if inp[1] == "j":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "i":
                    out.append("じ")
                    inp = inp[2:]
                elif inp[1] == "y" and inp [2] == "a":
                    out.append("じゃ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "u":
                    out.append("じゅ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "o":
                    out.append("じょ")
                    inp = inp[3:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            elif inp[0] == "t":
                if inp[1] == "t":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "a":
                    out.append("た")
                    inp = inp[2:]
                elif inp[1] == "i":
                    out.append("ち")
                    inp = inp[2:]
                elif inp[1] == "u":
                    out.append("つ")
                    inp = inp[2:]
                elif inp[1] == "s" and inp [2] == "u":
                    out.append("つ")
                    inp = inp[3:]
                elif inp[1] == "e":
                    out.append("て")
                    inp = inp[2:]
                elif inp[1] == "o":
                    out.append("と")
                    inp = inp[2:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            elif inp[0] == "c":
                if inp[1] == "c":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "h" and inp[2] == "i":
                    out.append("ち")
                    inp = inp[3:]
                elif inp[1] == "h" and inp [2] == "a":
                    out.append("ちゃ")
                    inp = inp[3:]
                elif inp[1] == "h" and inp [2] == "u":
                    out.append("ちゅ")
                    inp = inp[3:]
                elif inp[1] == "h" and inp [2] == "o":
                    out.append("ちょ")
                    inp = inp[3:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            elif inp[0] == "d":
                if inp[1] == "d":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "a":
                    out.append("だ")
                    inp = inp[2:]
                elif inp[1] == "i":
                    out.append("ぢ")
                    inp = inp[2:]
                elif inp[1] == "u":
                    out.append("づ")
                    inp = inp[2:]
                elif inp[1] == "e":
                    out.append("で")
                    inp = inp[2:]
                elif inp[1] == "o":
                    out.append("ど")
                    inp = inp[2:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            elif inp[0] == "n":
                if(len(inp) == 1):
                    out.append("ん")
                    inp = inp[1:]
                else:
                    if inp[1] == "a":
                        out.append("な")
                        inp = inp[2:]
                    elif inp[1] == "i":
                        out.append("に")
                        inp = inp[2:]
                    elif inp[1] == "u":
                        out.append("ぬ")
                        inp = inp[2:]
                    elif inp[1] == "e":
                        out.append("ね")
                        inp = inp[2:]
                    elif inp[1] == "o":
                        out.append("の")
                        inp = inp[2:]
                    elif inp[1] == "y" and inp [2] == "a":
                        out.append("にゃ")
                        inp = inp[3:]
                    elif inp[1] == "y" and inp [2] == "u":
                        out.append("にゅ")
                        inp = inp[3:]
                    elif inp[1] == "y" and inp [2] == "o":
                        out.append("にょ")
                        inp = inp[3:]
                    else:
                        out.append("ん")
                        inp = inp[1:]
            elif inp[0] == "h":
                if inp[1] == "h":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "a":
                    out.append("は")
                    inp = inp[2:]
                elif inp[1] == "i":
                    out.append("ひ")
                    inp = inp[2:]
                elif inp[1] == "u":
                    out.append("ふ")
                    inp = inp[2:]
                elif inp[1] == "e":
                    out.append("へ")
                    inp = inp[2:]
                elif inp[1] == "o":
                    out.append("ほ")
                    inp = inp[2:]
                elif inp[1] == "y" and inp [2] == "a":
                    out.append("ひゃ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "u":
                    out.append("ひゅ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "o":
                    out.append("ひょ")
                    inp = inp[3:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            elif inp[0] == "f":
                if inp[1] == "f":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "u":
                    out.append("ふ")
                    inp = inp[2:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            elif inp[0] == "b":
                if inp[1] == "b":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "a":
                    out.append("ば")
                    inp = inp[2:]
                elif inp[1] == "i":
                    out.append("び")
                    inp = inp[2:]
                elif inp[1] == "u":
                    out.append("ぶ")
                    inp = inp[2:]
                elif inp[1] == "e":
                    out.append("べ")
                    inp = inp[2:]
                elif inp[1] == "o":
                    out.append("ぼ")
                    inp = inp[2:]
                elif inp[1] == "y" and inp [2] == "a":
                    out.append("びゃ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "u":
                    out.append("びゅ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "o":
                    out.append("びょ")
                    inp = inp[3:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            elif inp[0] == "p":
                if inp[1] == "p":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "a":
                    out.append("ぱ")
                    inp = inp[2:]
                elif inp[1] == "i":
                    out.append("ぴ")
                    inp = inp[2:]
                elif inp[1] == "u":
                    out.append("ぷ")
                    inp = inp[2:]
                elif inp[1] == "e":
                    out.append("ぺ")
                    inp = inp[2:]
                elif inp[1] == "o":
                    out.append("ぽ")
                    inp = inp[2:]
                elif inp[1] == "y" and inp [2] == "a":
                    out.append("ぴゃ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "u":
                    out.append("ぴゅ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "o":
                    out.append("ぴょ")
                    inp = inp[3:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            elif inp[0] == "m":
                if inp[1] == "m":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "a":
                    out.append("ま")
                    inp = inp[2:]
                elif inp[1] == "i":
                    out.append("み")
                    inp = inp[2:]
                elif inp[1] == "u":
                    out.append("む")
                    inp = inp[2:]
                elif inp[1] == "e":
                    out.append("め")
                    inp = inp[2:]
                elif inp[1] == "o":
                    out.append("も")
                    inp = inp[2:]
                elif inp[1] == "y" and inp [2] == "a":
                    out.append("みゃ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "u":
                    out.append("みゅ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "o":
                    out.append("みょ")
                    inp = inp[3:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            elif inp[0] == "r":
                if inp[1] == "r":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "a":
                    out.append("ら")
                    inp = inp[2:]
                elif inp[1] == "i":
                    out.append("り")
                    inp = inp[2:]
                elif inp[1] == "u":
                    out.append("る")
                    inp = inp[2:]
                elif inp[1] == "e":
                    out.append("れ")
                    inp = inp[2:]
                elif inp[1] == "o":
                    out.append("ろ")
                    inp = inp[2:]
                elif inp[1] == "y" and inp [2] == "a":
                    out.append("りゃ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "u":
                    out.append("りゅ")
                    inp = inp[3:]
                elif inp[1] == "y" and inp [2] == "o":
                    out.append("りょ")
                    inp = inp[3:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            elif inp[0] == "y":
                if inp[1] == "y":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "a":
                    out.append("や")
                    inp = inp[2:]
                elif inp[1] == "u":
                    out.append("ゆ")
                    inp = inp[2:]
                elif inp[1] == "o":
                    out.append("よ")
                    inp = inp[2:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            elif inp[0] == "w":
                if inp[1] == "w":
                    out.append("っ")
                    inp = inp[1:]
                if inp[1] == "a":
                    out.append("わ")
                    inp = inp[2:]
                elif inp[1] == "o":
                    out.append("を")
                    inp = inp[2:]
                else:
                    out.append(inp[0])
                    inp = inp[1:]
            else:
                out.append(inp[0])
                inp = inp[1:]
        except IndexError:
            out.append(inp)
            inp = ""
        except:
            out.append(inp[0])
            inp = inp[1:]
    
    outstr = ""
    for element in out:
        outstr = outstr + element
    return outstr

#ckeck if pos [x, y] is inside rect_prop [x1, y1, w, h]
def click_check(pos, rect_prop):
    if rect_prop[0] <= pos[0] and pos[0] <= rect_prop[0]+rect_prop[2]:
        if rect_prop[1] <= pos[1] and pos[1] <= rect_prop[1]+rect_prop[3]:
            return True
    return False

def load():
    global save
    try:
        with open('udata.sf') as load_file:
            save = deepcopy(json.load(load_file))
            # try to ensure save fiel is complitable with new stages
            if len(save['unlock']) < 3:
                save['unlock'].extend([False] * (3 - len(save['unlock'])))
                save['star'].extend([0] * (3 - len(save['star'])))
                write()
            print("Loaded data:", save)
    except:
        print("File not found. Creating a new one.")
        with open('udata.sf', 'w') as store_file:
            json.dump(deepcopy(save), store_file)

def write():
    with open('udata.sf', 'w') as store_data:
        json.dump(save, store_data)

def draw_stage_selection(n):
    match n:
        case 0:
            bg = 10
            center = 17
            title = 12
            if save["unlock"][n+1]:
                next = 17
            else:
                next = 18
            prev = None
        case 1:
            # later stage can just copy from this

            # bg image
            bg = 10

            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 17
            else:
                center = 18

            # the title text, but in image format, Jeff can help gen
            title = 21

            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 20
                else:
                    next = 19
            else:
                next = None

            # image of previos stage
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18

        case 2:
            bg = 10
            # Center stage (Stage 3) is Type 1
            if save["unlock"][n]:
                center = 20
            else:
                center = 19
            title = 23
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 20
                else:
                    next = 19
            else:
                next = None
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        
        case 3:
            bg = 10
            if save["unlock"][n]:
                center = 20
            else:
                center = 19
            title = 24
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 27
                else:
                    next = 26
            else:
                next = None
            if save["unlock"][n-1]:
                prev = 20
            else:
                prev = 19
        case 4:
            bg = 25
            if save["unlock"][n]:
                center = 27
            else:
                center = 26
            title = 28
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 20
                else:
                    next = 19
            else:
                next = None
            if save["unlock"][n-1]:
                prev = 20
            else:
                prev = 19

    screen.blit(images[bg], transform_scale([0, 0]))
    screen.blit(images[center], transform_scale([297, 198]))

    r = images[title].get_rect()
    r.center = screen.get_rect().center
    r.y = HEIGHT*0.08
    screen.blit(images[title], r)

    if next:
        screen.blit(images[next], transform_scale([1287, 198]))
    if prev:
        screen.blit(images[prev], transform_scale([-694, 198]))

def draw_story_bg(stage):
    match stage:
        case 0:
            screen.blit(images[3], (0, 0))
        case 1:
            screen.blit(images[3], (0, 0))
        case 2:
            screen.blit(images[3], (0, 0))
        case 3:
            screen.blit(images[3], (0, 0))
        case 4:
            screen.blit(images[25], (0, 0))
            


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((pygame.display.get_desktop_sizes()[0][0]-WIDTH)/2, 20)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Learn Japanese!")
clock = pygame.time.Clock()
fps = 60

load()

if new_game:
    save = {
        'unlock': [True, False, False, False, False],
        'star': [0, 0, 0, 0, 0],
        'current_stage': 0,
    }
if god_mod:
    save = {
        'unlock': [True, True, True, True, True],
        'star': [0, 0, 0, 0, 0],
        'current_stage': 0,
    }
# question bank: verb form convertion
# size: 27
# choose_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# not_chosen_list = []

verb = {
        "verb_ru": ["いる", "行く", "来る", "帰る", "出掛ける", "する", "食べる", "飲む", "見る", "読む", "書く", "聞く", "買う", "起きる", "寝る", "乗る", "売る", "降(お)りる", "迎える", "会う", "働く", "休む", "入る", "出る", "着る", "履く", "脱ぐ", "座る", "渡る", "通る", "置く", "使う", "刺す", "押す", "話す", "言う", "替える", "走る", "戻る", "泊まる", "止める", "教える", "習う", "泳ぐ", "弾く", "開ける", "閉める", "付ける", "消す", "洗う", "入れる", "取る", "打つ", "作る", "焼く", "歩く", "曲がる"],
        "verb_ru_hira": ["いる", "いく", "くる", "かえる", "でかける", "する", "たべる", "のむ", "みる", "よむ", "かく", "きく", "かう", "おきる", "ねる", "のる", "うる", "おりる", "むかえる", "あう", "はたらく", "やすむ", "はいる", "でる", "きる", "はく", "ぬぐ", "すわる", "わたる", "とおる", "おく", "つかう", "さす", "おす", "はなす", "いう", "かえる", "はしる", "もどる", "とまる", "やむ", "おしえる", "ならう", "およぐ", "ひく", "あける", "しめる", "つける", "けす", "あらう", "いれる", "とる", "うつ", "つくる", "やく", "あるく", "まがる"],

        "verb_masu": ["います", "行きます", "来ます", "帰ります", "出掛けます", "します", "食べます", "飲みます", "見ます", "読みます", "書きます", "聞きます", "買います", "起きます", "寝ます", "乗ります", "売ります", "降(お)ります", "迎えます", "会います", "働きます", "休みます", "入ります", "出ます", "着ます", "穿きます", "脱ぎます", "座ります", "渡ります", "通ります", "置きます", "使います", "挿します", "押します", "話します", "言います", "替えます", "走ります", "戻ります", "泊まります", "止めます", "教えます", "習います", "泳ぎます", "弾きます", "開けます", "閉めます", "つけます", "消します", "洗います", "入れます", "取ります", "打ちます", "作ります", "焼きます", "歩きます", "曲がります"],
        "verb_masu_hira": ["います", "いきます", "きます", "かえります", "でかけます", "します", "たべます", "のみます", "みます", "よみます", "かきます", "ききます", "かいます", "おきます", "ねます", "のります", "うります", "おります", "むかえます", "あいます", "はたらきます", "やすみます", "はいります", "でます", "きます", "はきます", "ぬぎます", "すわります", "わたります", "とおります", "おきます", "つかいます", "さしいます", "おします", "はなします", "いいます", "かえます", "はしります", "もどります", "とまります", "やめます", "おしえます", "なります", "およぎます", "ひきます", "あけます", "しめます", "つけます", "けします", "あらいます", "いれます", "とります", "うちます", "つくります", "やきます", "あるきます", "まがります"],

        "verb_te": ["いって", "行って", "来て", "帰って", "出掛けて", "して", "食べて", "飲んで", "見て", "読んで", "書いて", "聞いて", "買って", "起きて", "寝て", "乗って", "売って", "降(お)りて", "迎えて", "会って", "働いて", "休んで", "入って", "出て", "着て", "履いて", "脱いで", "座って", "渡って", "通って", "置いて", "使って", "刺して", "押して", "話して", "言って", "替えて", "走って", "戻って", "泊まって", "止めて", "教えて", "習って", "泳いで", "弾いて", "開けて", "閉めて", "付けて", "消して", "洗って", "入れて", "取って", "打って", "作って", "焼いて", "歩いて", "曲がって"],
        "verb_te_hira": ["いって", "いって", "きて", "かえって", "でかけて", "して", "たべて", "のんで", "みて", "よんで", "かいて", "きいて", "かって", "おきて", "ねて", "のって", "うって", "おりて", "むかえて", "あって", "はたらいて", "やすんで", "はいって", "でて", "きて", "はいて", "ぬいで", "すわって", "わたって", "とおって", "おいて", "つかって", "さして", "おして", "はなして", "いって", "かえて", "はしって", "もどって", "とまって", "やめて", "おしえて", "ならって", "およいで", "ひいて", "あけて", "しめて", "つけて", "けして", "あらって", "いれて", "とって", "うって", "つくって", "やいて", "あるいて", "まがって"],

        "verb_ta": ["いた", "行った", "来た", "帰った", "出掛けた", "した", "食べた", "飲んだ", "見た", "読んだ", "書いた", "聞いた", "買った", "起きた", "寝た", "乗った", "売った", "降(お)りた", "迎えた", "会った", "働いた", "休んだ", "入った", "出た", "着た", "履いた", "脱いだ", "座った", "渡った", "通った", "置いた", "使った", "刺した", "押した", "話した", "言った", "替えた", "走った", "戻った", "泊まった", "止めた", "教えた", "習った", "泳いだ", "弾いた", "開けた", "閉めた", "付けた", "消した", "洗った", "入れた", "取った", "打った", "作った", "焼いた", "歩いた", "曲がった"],
        "verb_ta_hira": ["いた", "いった", "きた", "かえった", "でかけた", "した", "たべた", "のんだ", "みた", "よんだ", "かいた", "きいた", "かった", "おきた", "ねた", "のった", "うった", "おりた", "むかえた", "あった", "はたらいた", "やすんだ", "はいった", "でた", "きた", "はいた", "ぬいだ", "すわった", "わたった", "とおった", "おいた", "つかった", "さした", "おした", "はなした", "いった", "かえた", "はしった", "もどった", "とまった", "やんだ", "おしえた", "ならった", "およいだ", "ひいた", "あけた", "しめた", "つけた", "けした", "あらった", "いれた", "とった", "うった", "つくった", "やいた", "あるいた", "まがった"],

        "verb_nai": ["いない", "行かない", "来ない", "帰らない", "出掛けない", "しない", "食べない", "飲まない", "見ない", "読まない", "書かない", "聞かない", "買わない", "起きない", "寝ない", "乗らない", "売らない", "降(お)りない", "迎えない", "会わない", "働かない", "休まない", "入らない", "出ない", "着ない", "履かない", "脱がない", "座らない", "渡らない", "通らない", "置かない", "使わない", "刺さない", "押さない", "話さない", "言わない", "替えない", "走らない", "戻らない", "泊まらない", "止めない", "教えない", "習わない", "泳がない", "弾かない", "開けない", "閉めない", "付けない", "消さない", "洗わない", "入れない", "取らない", "打たない", "作らない", "焼かない", "歩かない", "曲がらない"],
        "verb_nai_hira": ["いない", "いかない", "こない", "かえらない", "でかけない", "しない", "たべない", "のまない", "みない", "よまない", "かかない", "きかない", "かわない", "おきない", "ねない", "のらない", "うらない", "おりない", "むかえない", "あわない", "はたらかない", "やすまない", "はいらない", "でない", "こない", "きない", "はかない", "ぬがない", "すわらない", "わたらない", "とおらない", "おかない", "つかわない", "ささない", "おさない", "はなさない", "いわない", "かえない", "はしらない", "もどらない", "とまらない", "やめない", "おしえない", "ならわない", "およがない", "ひかない", "あけない", "しめない", "つけない", "けさない", "あらわない", "いれない", "とらない", "うたない", "つくらない", "やかない", "あるかない", "まがらない"],

        "verb_ikou": ["いよう", "行こう", "来よう", "帰ろう", "出掛けよう", "しよう", "食べよう", "飲もう", "見よう", "読もう", "書こう", "聞こう", "買おう", "起きよう", "寝よう", "乗ろう", "売ろう", "降(お)りよう", "迎えよう", "会おう", "働こう", "休もう", "入ろう", "出よう", "着よう", "履こう", "脱ごう", "座ろう", "渡ろう", "通ろう", "置こう", "使おう", "刺そう", "押そう", "話そう", "言おう", "替えよう", "走ろう", "戻ろう", "泊まろう", "止めよう", "教えよう", "習おう", "泳ごう", "弾こう", "開けよう", "閉めよう", "付けよう", "消そう", "洗おう", "入れよう", "取ろう", "打とう", "作ろう", "焼こう", "歩こう", "曲がろう"],
        "verb_ikou_hira": ["いよう", "いこう", "こよう", "かえろう", "でかけよう", "しよう", "たべよう", "のもう", "みよう", "よもう", "かこう", "きこう", "かおう", "おきよう", "ねよう", "のろう", "うろう", "おりよう", "むかえよう", "あおう", "はたらこう", "やすもう", "はいろう", "でよう", "きよう", "きよう", "はこう", "ぬごう", "すわろう", "わたろう", "とおろう", "おこう", "つかおう", "さそう", "おそう", "はなそう", "いおう", "かえよう", "はしろう", "もどろう", "とまろう", "やめよう", "おしえよう", "ならおう", "およごう", "ひこう", "あけよう", "しめよう", "つけよう", "けそう", "あらおう", "いれよう", "とろう", "うとう", "つくろう", "やこう", "あるこう", "まがろう"],

        "verb_kanou": ["いられる", "行ける", "来られる", "帰れる", "出掛けられる", "できる", "食べられる", "飲める", "見られる", "読める", "書ける", "聞ける", "買える", "起きられる", "寝られる", "乗れる", "売れる", "降(お)りられる", "迎えられる", "会える", "働ける", "休める", "入れる", "出られる", "着られる", "履ける", "脱げる", "座れる", "渡れる", "通れる", "置ける", "使える", "刺せる", "押せる", "話せる", "言える", "替えられる", "走れる", "戻れる", "泊まれる", "止められる", "教えられる", "習える", "泳げる", "弾ける", "開けられる", "閉められる", "付けられる", "消せる", "洗える", "入れられる", "取れる", "打てる", "作れる", "焼ける", "歩ける", "曲がれる"],
        "verb_kanou_hira": ["いられる", "いける", "こられる", "かえれる", "でかけられる", "できる", "たべられる", "のめる", "みられる", "よめる", "かける", "きける", "かえる", "おきられる", "ねられる", "のれる", "うれる", "おりられる", "むかえられる", "あえる", "はたらける", "やすめる", "はいれる", "でられる", "きられる", "きれる", "はける", "ぬげる", "すわれる", "わたれる", "とおれる", "おける", "つかえる", "させる", "おせる", "はなせる", "いえる", "かえられる", "はしれる", "もどれる", "とまれる", "やめられる", "おしえられる", "ならえる", "およげる", "ひける", "あけられる", "しめられる", "つけられる", "けせる", "あらえる", "いれられる", "とれる", "うてる", "つくれる", "やける", "あるける", "まがれる"],

        "verb_ba": ["いれば", "行けば", "来れば", "帰れば", "出掛ければ", "すれば", "食べれば", "飲めば", "見れば", "読めば", "書けば", "聞けば", "買えば", "起きれば", "寝れば", "乗れば", "売れば", "降(お)りれば", "迎えれば", "会えば", "働けば", "休めば", "入れば", "出れば", "着れば", "履けば", "脱げば", "座れば", "渡れば", "通れば", "置けば", "使えば", "刺せば", "押せば", "話せば", "言えば", "替えれば", "走れば", "戻れば", "泊まれば", "止められれば", "教えれば", "習えば", "泳げば", "弾けば", "開ければ", "閉めれば", "付ければ", "消せば", "洗えば", "入れれば", "取れば", "打てば", "作れば", "焼けば", "歩けば", "曲がれば"],
        "verb_ba_hira": ["いれば", "いけば", "これば", "かえれば", "でかければ", "すれば", "たべれば", "のめば", "みれば", "よめば", "かけば", "きけば", "かえば", "おきれば", "ねれば", "のれば", "うれば", "おりれば", "むかえれば", "あえば", "はたらけば", "やすめば", "はいれば", "でれば", "きれば", "きれば", "はけば", "ぬげば", "すわれば", "わたれば", "とおれば", "おけば", "つかえば", "させば", "おせば", "はなせば", "いえば", "かえれば", "はしれば", "もどれば", "とまれば", "やめれば", "おしえれば", "ならえば", "およげば", "ひけば", "あければ", "しめれば", "つければ", "けせば", "あらえば", "いれれば", "とれば", "うてば", "つくれば", "やけば", "あるけば", "まがれば"],

        "verb_ro": ["いろ", "行け", "来い", "帰れ", "出掛けろ", "しろ", "食べろ", "飲め", "見ろ", "読め", "書け", "聞け", "買え", "起きろ", "寝ろ", "乗れ", "売れ", "降(お)りろ", "迎えろ", "会え", "働け", "休め", "入れ", "出ろ", "着ろ", "履け", "脱げ", "座れ", "渡れ", "通れ", "置け", "使え", "刺せ", "押せ", "話せ", "言え", "替えろ", "走れ", "戻れ", "泊まれ", "止められろ", "教えろ", "習え", "泳げ", "弾け", "開けろ", "閉めろ", "付けろ", "消せ", "洗え", "入れろ", "取れ", "打て", "作れ", "焼けろ", "歩け", "曲がれ"],
        "verb_ro_hira": ["いろ", "いけ", "こい", "かえれ", "でかけろ", "しろ", "たべろ", "のめ", "みろ", "よめ", "かけ", "きけ", "かえ", "おきろ", "ねろ", "のれ", "うれ", "おりろ", "むかえろ", "あえ", "はたらけ", "やすめ", "はいれ", "でろ", "きろ", "きれ", "はけ", "ぬげ", "すわれ", "わたれ", "とおれ", "おけ", "つかえ", "させ", "おせ", "はなせ", "いえ", "かえろ", "はしれ", "もどれ", "とまれ", "やめろ", "おしえろ", "ならえ", "およげ", "ひけ", "あけろ", "しめろ", "つけろ", "けせ", "あらえ", "いれろ", "とれ", "うて", "つくれ", "やけろ", "あるけ", "まがれ"],

        "verb_na": ["いるな", "行くな", "来るな", "帰るな", "出掛けるな", "するな", "食べるな", "飲むな", "見るな", "読むな", "書くな", "聞くな", "買うな", "起きるな", "寝るな", "乗るな", "売るな", "降(お)りるな", "迎えるな", "会うな", "働くな", "休むな", "入るな", "出るな", "着るな", "履くな", "脱ぐな", "座るな", "渡るな", "通るな", "置くな", "使うな", "刺すな", "押すな", "話すな", "言うな", "替えるな", "走るな", "戻るな", "泊まるな", "止められるな", "教えるな", "習うな", "泳ぐな", "弾くな", "開けるな", "閉めるな", "付けるな", "消すな", "洗うな", "入れるな", "取るな", "打つな", "作るな", "焼けるな", "歩くな", "曲がるな"],
        "verb_na_hira": ["いるな", "いくな", "くるな", "かえるな", "でかけるな", "するな", "たべるな", "のむな", "みるな", "よむな", "かくな", "きくな", "かうな", "おきるな", "ねるな", "のるな", "うるな", "おりるな", "むかえるな", "あうな", "はたらくな", "やすむな", "はいるな", "でるな", "きるな", "きるな", "はくな", "ぬぐな", "すわるな", "わたるな", "とおるな", "おくな", "つかうな", "させな", "おすな", "はなすな", "いうな", "かえるな", "はしるな", "もどるな", "とまるな", "やめるな", "おしえるな", "ならうな", "およぐな", "ひくな", "あけるな", "しめるな", "つけるな", "けすな", "あらうな", "いれるな", "とるな", "うつな", "つくるな", "やけるな", "あるくな", "まがるな"],

        "verb_rareru": ["いられる", "行かれる", "来られる", "帰られる", "出掛けられる", "される", "食べられる", "飲まれる", "見られる", "読まれる", "書かれる", "聞かれる", "買われる", "起きられる", "寝られる", "乗られる", "売られる", "降(お)りられる", "迎えられる", "会われる", "働かれる", "休まれる", "入られる", "出られる", "着られる", "履かれる", "脱がれる", "座られる", "渡られる", "通られる", "置かれる", "使われる", "刺される", "押される", "話される", "言われる", "替えられる", "走られる", "戻られる", "泊まられる", "止められる", "教えられる", "習われる", "泳がれる", "弾かれる", "開けられる", "閉められる", "付けられる", "消される", "洗われる", "入れられる", "取られる", "打たれる", "作られる", "焼かれる", "歩かれる", "曲げられる"],
        "verb_rareru_hira": ["いられる", "いかれる", "こられる", "かえられる", "でかけられる", "される", "たべられる", "のまれる", "みられる", "よまれる", "かかれる", "きかれる", "かわれる", "おきられる", "ねられる", "のられる", "うられる", "おりられる", "むかえられる", "あわれる", "はたらかれる", "やすまれる", "はいられる", "でられる", "きられる", "きられる", "はかれる", "ぬがれる", "すわられる", "わたられる", "とおられる", "おかれる", "つかわれる", "される", "おされる", "はなされる", "いわれる", "かえられる", "はされる", "もどられる", "とまられる", "やめられる", "おしえられる", "ならわれる", "およがれる", "ひかれる", "あけられる", "しめられる", "つけられる", "keされる", "あられる", "いれられる", "とられる", "うたれる", "つくられる", "やかれる", "あるかれる", "まげられる"],

        "verb_saseru": ["いらせる", "行かせる", "来させる", "帰らせる", "出掛けさせる", "させる", "食べさせる", "飲ませる", "見させる", "読ませる", "書かせる", "聞かせる", "買わせる", "起きさせる", "寝させる", "乗らせる", "売らせる", "降(お)りさせる", "迎えさせる", "会わせる", "働かせる", "休ませる", "入らせる", "出させる", "着させる", "履かせる", "脱がせる", "座らせる", "渡らせる", "通らせる", "置かせる", "使わせる", "刺させる", "押させる", "話させる", "言わせる", "替えさせる", "走らせる", "戻らせる", "泊まらせる", "止めさせる", "教えさせる", "習わせる", "泳がせる", "弾かせる", "開けさせる", "閉めさせる", "付けさせる", "消させる", "洗わせる", "入れさせる", "取らせる", "打たせる", "作らせる", "焼かせる", "歩かせる", "曲げさせる"],
        "verb_saseru_hira": ["いらせる", "いかせる", "こさせる", "かえらせる", "でかけさせる", "させる", "たべさせる", "のませる", "みさせる", "よませる", "かかせる", "きかせる", "かわせる", "おきさせる", "ねさせる", "のらせる", "うらせる", "おりさせる", "むかえさせる", "あわせる", "はたらかせる", "やすませる", "はいらせる", "ださせる", "きさせる", "きさせる", "はかせる", "ぬがせる", "すわらせる", "わたらせる", "とおらせる", "おかせる", "つかわせる", "させる", "おさせる", "はなさせる", "いわせる", "かえさせる", "はさせる", "もどらせる", "とまらせる", "やめさせる", "おしえさせる", "ならわせる", "およがせる", "ひかせる", "あけさせる", "しめさせる", "つけさせる", "keさせる", "あらわせる", "いれさせる", "とらせる", "うたせる", "つくらせる", "やかせる", "あるかせる", "まげさせる"],

        "verb_saseru_rareru": ["いらせられる", "行かせられる", "来させられる", "帰らせられる", "出掛けさせられる", "させられる", "食べさせられる", "飲ませられる", "見させられる", "読ませられる", "書かせられる", "聞かせられる", "買わせられる", "起きさせられる", "寝させられる", "乗らせられる", "売らせられる", "降(お)りさせられる", "迎えさせられる", "会わせられる", "働かせられる", "休ませられる", "入らせられる", "出させられる", "着させられる", "履かせられる", "脱がせられる", "座らせられる", "渡らせられる", "通らせられる", "置かせられる", "使わせられる", "刺させられる", "押させられる", "話させられる", "言わせられる", "替えさせられる", "走らせられる", "戻らせられる", "泊まらせられる", "止めさせられる", "教えさせられる", "習わせられる", "泳がせられる", "弾かせられる", "開けさせられる", "閉めさせられる", "付けさせられる", "消させられる", "洗わせられる", "入れさせられる", "取らせられる", "打たせられる", "作らせられる", "焼かせられる", "歩かせられる", "曲げさせられる"],
        "verb_saseru_rareru_hira": ["いらせられる", "いかせられる", "こさせられる", "かえらせられる", "でかけさせられる", "させられる", "たべさせられる", "のませられる", "みさせられる", "よませられる", "かかせられる", "きかせられる", "かわせられる", "おきさせられる", "ねさせられる", "のらせられる", "うらせられる", "おりさせられる", "むかえさせられる", "あわせられる", "はたらかせられる", "やすませられる", "はいらせられる", "ださせられる", "きさせられる", "きさせられる", "はかせられる", "ぬがせられる", "すわらせられる", "わたらせられる", "とおらせられる", "おかせられる", "つかわせられる", "させられる", "おさせられる", "はなさせられる", "いわせられる", "かえさせられる", "はさせられる", "もどらせられる", "とまらせられる", "やめさせられる", "おしえさせられる", "ならわせられる", "およがせられる", "ひかせられる", "あけさせられる", "しめさせられる", "つけさせられる", "keさせられる", "あらわせられる", "いれさせられる", "とらせられる", "うたせられる", "つくらせられる", "やかせられる", "あるかせられる", "まげさせられる"],

}
# basic initialize of variables for the game loop
game_state = "menu"          # this determine initial gamestate
running = True

inputArr = ""
outputArr = ""
# no_of_qs = 3
# no_of_heart = 3
# heart = pygame.image.load("media/heart.png").convert_alpha()
# heart = pygame.transform.scale(heart, transform_scale([32, 32]))
# kara = "masu"                               
# made = "masu"                               
# verb = ""                                   
# pause = False                               
# temptime = pygame.time.get_ticks()          
# score = 0                                
# prevScore = 0       


time = 0                                
menu_effect_timer = 0                        
win_lose_effect_timer = 0    


images = [
    pygame.transform.scale(pygame.image.load("media/dungeon_crystal_1.png"), [WIDTH, HEIGHT]),                   # 0
    pygame.transform.scale(pygame.image.load("media/title_text.png"), transform_scale([816, 144])),              # 1
    pygame.transform.scale(pygame.image.load("media/press_to_start.png"), transform_scale([269, 36])),           # 2
    pygame.transform.scale(pygame.image.load("media/forest_1.png"), [WIDTH, HEIGHT]),                            # 3
    pygame.transform.scale(pygame.image.load("media/main_char.png"), transform_scale([640, 768])),               # 4
    pygame.transform.scale(pygame.image.load("media/teacher_no_glasses.png"), transform_scale([517, 680])),      # 5
    pygame.transform.scale(pygame.image.load("media/skip.png"), transform_scale([310, 80])),                     # 6
    pygame.transform.scale(pygame.image.load("media/main_char_gray.png"), transform_scale([640, 768])),          # 7
    pygame.transform.scale(pygame.image.load("media/teacher_no_glasses_gray.png"), transform_scale([517, 680])), # 8
    pygame.transform.scale(pygame.image.load("media/purple_slime_1.png"),transform_scale([532, 572])),           # 9
    pygame.transform.scale(pygame.image.load("media/forest_river_sky.png"),transform_scale([1440, 1080])),       #10
    pygame.transform.scale(pygame.image.load("media/stage_arrow.png"),transform_scale([75, 110])),               #11
    pygame.transform.scale(pygame.image.load("media/stage1_title.png"),transform_scale([200, 60])),              #12
    pygame.transform.scale(pygame.image.load("media/star0.png"),transform_scale([360, 100])),                    #13
    pygame.transform.scale(pygame.image.load("media/star1.png"),transform_scale([360, 100])),                    #14
    pygame.transform.scale(pygame.image.load("media/star2.png"),transform_scale([360, 100])),                    #15
    pygame.transform.scale(pygame.image.load("media/star3.png"),transform_scale([360, 100])),                    #16
    pygame.transform.scale(pygame.image.load("media/stage_type_1_img_light.png"),transform_scale([847, 635])),   #17
    pygame.transform.scale(pygame.image.load("media/stage_type_1_img_dark.png"),transform_scale([847, 635])),    #18
    pygame.transform.scale(pygame.image.load("media/stage_type_2_img_dark.png"),transform_scale([847, 635])),    #19
    pygame.transform.scale(pygame.image.load("media/stage_type_2_img_light.png"),transform_scale([847, 635])),   #20
    pygame.transform.scale(pygame.image.load("media/stage2_title.png"),transform_scale([185, 60])),              #21
    pygame.transform.scale(pygame.image.load("media/continue.png"),transform_scale([520, 110])),                 #22
    pygame.transform.scale(pygame.image.load("media/stage3_title.png"), transform_scale([186, 60])),             #23
    pygame.transform.scale(pygame.image.load("media/stage4_title.png"), transform_scale([187, 60])),             #24
    pygame.transform.scale(pygame.image.load("media/hell_bg.png"), [WIDTH, HEIGHT]),                             #25
    pygame.transform.scale(pygame.image.load("media/hell_bg_dark.png"),transform_scale([847, 635])),             #26
    pygame.transform.scale(pygame.image.load("media/hell_bg_light.png"),transform_scale([847, 635])),            #27
    pygame.transform.scale(pygame.image.load("media/finalstage1_title.png"),transform_scale([299, 60])),         #28
    pygame.transform.scale(pygame.image.load("media/demon_1.png"), transform_scale([685, 400])),                 #29
    pygame.transform.scale(pygame.image.load("media/high_demon_1.png"), transform_scale([187, 60])),  # unused

]                                                              

# 基礎言靈魔法表示: <あ>
dialog = [
    [
        (2, "？？？：\nおいおい！起[お]きろ！"),
        (1, "？？？：\n什麼？我在哪裡？那個女孩在說什麼？"),
        (2, "？？？：\n終於醒了。這裡是春日森林，我在旁邊路過就看到你\n躺在這裡。"),
        (2, "莉子：\n我叫莉子[りこ]，你還記得你的名字嗎？\n（幸好我在學校學過中文..."),
        (1, "赤真：\n我好像叫赤真。春日森林...是在日本嗎？"),
        (2, "莉子：\n日本？這裡是東瀛喔！\n我從未聽說過你所說的日本呢。（難道他失憶了？"),
        (1, "赤真：\n欸欸欸？！難道我像漫畫中一樣穿越到異世界了嗎？？"),
        (2, "莉子：\n什麼是漫畫？異世界？"),
        (1, "赤真：\n沒什麼！（看來是真的了，\n我的宅男之夢終於成真了！！"),
        (2, "莉子：\n。。。"),
        (1, "赤真：\n請問你知道冒險者、魔物、魔法嗎？（期待"),
        (2, "莉子：\n看來你沒有失憶呢。沒錯，本小姐正是\nD級冒險者，剛接下討伐史萊姆的任務！"),
        (1, "赤真：\n史萊姆！！你要如何跟史萊姆戰鬥？"),
        (2, "莉子：\n我用的是言靈魔法啊！你呢？"),
        (1, "赤真：\n言靈魔法聽起來很酷呢！我也能用魔法嗎？"),
        (2, "莉子：\n你不會用魔法嗎？讓本小姐教你吧！"),
        (2, "莉子：\n言靈魔法需要東瀛語來發動，最初階的言靈魔法是\n「五十音」。"),
        (3, "*作者：本作中的東瀛語=日語"),
        (2, "莉子：\n雖然比較難理解，但是「五十音」不只有50個音喔！"),
        (2, "莉子：\n不管了，讓我先開始教你吧！\n施法時要全力大聲地喊出來。"),
        (2, "莉子：\n先記下這5個音。\n「あ」a、「い」i、「う」u、「え」e、「お」o"),
        (1, "赤真：\n「あ」a、「い」i、「う」u、「え」e、「お」o\n。。。"),
        (1, "赤真：\n這五個音有什麼意思嗎？"),
        (2, "莉子：\n單獨來看的話沒有什麼意思，\n要組成詞語和句子才有意思喔！"),
        (1, "赤真：\n原來如此。我先試試看。"),
        (1.1, "赤真：\n<あ>！"),
        (2, "莉子：\n嘩，真厲害！只教了你一次就發動成功了！\n本小姐教得真好！（嘿嘿！成功得到一個免費打手～"),
        (2, "莉子：\n看那邊！那裡有隻史萊姆，立刻實戰一下吧！"),
        (1, "赤真：\n等...等一下！能再說多次那5個音嗎？"),
        (2, "莉子：\n真拿你沒辦法～ 聽好了哦！\n「あ」a、「い」i、「う」u、「え」e、「お」o"),
        (2, "莉子：\n準備好了嗎？"),
        (1, "赤真：\n準備好了！來吧！")
    ],
    [
        (2, '莉子：\n不錯不錯！你成為一個合格的冒險者了！'),
        (1, '赤真：\n呼～（好險'),
        (2, '莉子：\n既然你學會了首5個音，我就開始教你更多吧！'),
        (2, '莉子：\n聽好了，這個是か行。\n 「か」ka、「き」ki、「く」ku、「け」ke、「こ」ko'),
        (2, '莉子：\n這些跟上次的5個音一樣，都是屬於清音。其他種類\n還有濁音、半濁音、拗音。'),
        (1, '赤真：\n清音？濁音？'),
        (2, '莉子：\n正好か行有濁音，順便也教你吧！'),
        (2, '莉子：\n「が」ga、「ぎ」gi、「ぐ」gu、「げ」ge、「ご」go'),
        (1, '赤真：\n看不出有什麼分別...'),
        (2, '莉子：\n你再看仔細點！右上角多了2點，讀音也會有所不同喔！\n「か」ka、「が」ga'),
        (1, '赤真：\n看到了。'),
        (2, '莉子：\n另外，東瀛語的書寫方法亦有兩種，分別是平假名和\n片假名。我們正在學的全都是平假名喔！'),
        (1, '赤真：\n(好複雜...'),
        (2, '莉子：\n不過也不用一次過全部記得，我們慢慢來吧！'),
        (1, '赤真：\n謝謝你，莉子小姐。'),
        (2, '莉子：\n嘿嘿～呀！差點忘了！'),
        (1, '赤真：\n怎麼了？'),
        (2, '莉子：\n差點忘記教你言靈魔法的回復術。'),
        (2, '莉子：\n我先示範一次，之後你應該就能學會了。何況本小姐\n教得這麼好，對吧？'),
        (1, '赤真：\n點頭(滴汗...'),
        (2.1, '莉子：\n<か>！'),
        (1, '赤真：\n身上的疼痛疲勞都消失了！'),
        (2, '莉子：\n正好，前面有另一隻史萊姆，試試吧！'),
        (1, '赤真：\n好，來吧！')
    ],
    [
        (2, '莉子：\n你越來越熟練了呢！'),
        (1, '赤真：\n這都多虧了莉子小姐的教導。'),
        (2, '莉子：\n哼哼，那是當然的！'),
        (2, '莉子：\n接下來，我們要學習如何將單字組成句子。'),
        (1, '赤真：\n喔喔！'),
        (2, '莉子：\n看看這個句子，然後把正確的詞語拖到空格裡吧！'),
        (1, '赤真：\n好的，我試試看！'),
    ],
    [
        (1, '赤真：\n好的，我試試看！'),
    ],
    [
        (1, '赤真：\n好的，我試試看！'),
    ]

]
# 0: both gray; 1: left talking; 2: right talking; 3: both talking
story_num = 0
stage = 0
dialog_num = 0

#this part is for drag type
draggable_rects = []
draggable_rects_initial_pos = []
dragged_item_index = -1
is_dragging = False
drag_offset_x = 0
drag_offset_y = 0
drop_target_rect = pygame.Rect(0,0,0,0) # Initialize with a dummy rect
parts = []


# question type: MC, Drag, input
battle_detail = [
    # 0
    {
        "question_type": "MC",
        "question": ["あ","い","う","え","お"],
        "answer": {
            "あ": ("a", ["a", "i", "u", "e"]),
            "い": ("i", ["i", "u", "e", "o"]),
            "う": ("u", ["u", "e", "o", "a"]),
            "え": ("e", ["e", "o", "a", "i"]),
            "お": ("o", ["o", "a", "i", "u"])
        },
        "word_size": 64,
        "order": [],
        "enemy_surf": 9,
        "enemy_attack_word": "む" ,
        "target": [5, 7],
        "enemy_hp": 100,
        "discription": "以滑鼠點擊正確的選項",
    },
    # 1
    {
        "question_type": "MC",
        "question": ["か","き","く","け","こ", "が","ぎ","ぐ","げ","ご"],
        "answer": {
            "か": ("ka", ["ka", "ga", "ha", "wa"]),
            "き": ("ki", ["ki", "sa", "chi", "gi"]),
            "く": ("ku", ["ka", "ga", "ku", "su"]),
            "け": ("ke", ["ke", "ka", "ki", "gi"]),
            "こ": ("ko", ["ko", "go", "wo", "ka"]),
            "が": ("ga", ["ga", "ka", "na", "ra"]),
            "ぎ": ("gi", ["gi", "ki", "shi", "bi"]),
            "ぐ": ("gu", ["gu", "ku", "su", "bu"]),
            "げ": ("ge", ["ge", "ke", "ko", "go"]),
            "ご": ("go", ["go", "ko", "so", "ga"])
        },
        "word_size": 64,
        "order": [],
        "enemy_surf": 9,
        "enemy_attack_word": "む" ,
        "target": [10, 14],
        "enemy_hp": 200,
        "discription": "以滑鼠點擊正確的選項",
    },
    #2
    {
        "question_type": "Drag",
         "questions": [
            { "sentence": "貓_", "answer": "ねこ", "options": ["ねこ", "いぬ", "とり", "さかな"] },
            { "sentence": "狗_", "answer": "いぬ", "options": ["いぬ", "ねこ", "うさぎ", "へび"] },
            { "sentence": "書_", "answer": "ほん", "options": ["ほん", "えんぴつ", "かばん", "とけい"] },
            { "sentence": "水_", "answer": "みず", "options": ["みず", "おちゃ", "ごはん", "ぱん"] },
            { "sentence": "人_", "answer": "ひと", "options": ["ひと", "おとこ", "おんな", "こども"] },
        ],
        "order": [],
        "enemy_surf": 9,
        "enemy_attack_word": "む",
        "target": [7, 9],
        "enemy_hp": 140,
        "discription": "以滑鼠拖拉正確的選項至空格內",
    },
    #3 (kanji to hiragana 1 )
    {
        "question_type": "MC",
        "question": ["行きます","来ます", "帰ります", "出掛けます","食べます", "飲みます", "見ます", "読みます", "書きます", "聞きます"],
        "answer": {
            "行きます": ("いきます", ["いきます", "ひきます", "いくきます", "ちきます"]),
            "来ます": ("きます", ["きます", "くます", "います", "いきます"]),
            "帰ります": ("かえります", ["かえります", "かります", "もどります", "でかります"]),
            "出掛けます": ("でかけます", ["でかけます", "てかけます", "てがけます", "けがけます"]),
            "食べます": ("たべます", ["たべます", "しゃべます", "だべます", "くべます"]),
            "飲みます": ("のみます", ["のみます", "いんみます", "おんみます", "のみみます"]),
            "見ます": ("みます", ["みます", "みえます", "けんます", "みせます"]),
            "読みます": ("よみます", ["よみます", "どくみます", "とくみます", "のみます"]),
            "書きます": ("かきます", ["かきます", "がきます", "しょきます", "よみます"]),
            "聞きます": ("ききます", ["ききます", "みにます", "こくます", "きます"])
        },
        "word_size": 36,
        "order": [],
        "enemy_surf": 9,
        "enemy_attack_word": "む" ,
        "target": [5, 7],
        "enemy_hp": 100,
        "discription": "以滑鼠點擊正確的選項",
    },
    #4 (masu to ru)
    {
        "question_type": "input",
        "question": "verb_masu",
        "answer": "verb_ru",
        "enemy_surf": 29,
        "counter": 0,
        "enemy_attack_word": "打",
        "target": [7, 10],
        "enemy_hp": 140,
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音\nます形 → 辞書形",
    }
    

]

battle_detail_backup = deepcopy(battle_detail)

player_hp = 100
enemy_hp = 100
question_num = 0
    

s = pygame.Surface((WIDTH,HEIGHT))
s.fill((0,0,0))

# main game loop
while running: 
    if game_state == "menu":

        # BG image
        screen.blit(images[0], (0, 0))

        # Title text
        r = images[1].get_rect()
        r.center = screen.get_rect().center
        screen.blit(images[1], r)

        # press any button to start text
        images[2].set_alpha(int(205+math.sin(menu_effect_timer)*50))
        screen.blit(images[2], transform_scale([586, 787]))
        menu_effect_timer += 0.1
        if menu_effect_timer > 100000:
            menu_effect_timer = 0
        
        if(time != 0):
            time += 1
            s.set_alpha(int(time/fps/2*255))
            screen.blit(s, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if (time == 0):
                    time += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                    if (time == 0):
                        time += 1

        # enter game
        if(time > fps*2):
            print(save["unlock"])
            if save["unlock"][1]:
                game_state = "select_stage"
                time=0
            else:
                game_state = "story"
                story_num = 0
                dialog_num = 0
                time = 0
                    
    if game_state == "story":
        # end story
        if dialog_num == len(dialog[story_num]):
            battle_detail = deepcopy(battle_detail_backup)
            time = 0
            game_state = "playing"
            
            stage = story_num
            player_hp = 100
            enemy_hp = battle_detail[stage]["enemy_hp"]

            if battle_detail[stage]["question_type"] == "MC":
                battle_detail[stage]["order"] = [random.randint(0, len(battle_detail[stage]["question"])-1)]
                if stage == 0:
                    action = "attack"
                else:
                    action = None
                question_num = 0
                correct = None
                random.shuffle(battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1])

            elif battle_detail[stage]["question_type"] == "Drag":
                # For Drag type, create a shuffled list of all question indices
                battle_detail[stage]["order"] = list(range(len(battle_detail[stage]["questions"])))
                random.shuffle(battle_detail[stage]["order"])
                # Make sure the UI elements are cleared before the battle starts
                draggable_rects.clear() 
                draggable_rects_initial_pos.clear()
                is_dragging = False
                dragged_item_index = -1
                action = None
                question_num = 0
                correct = None

            elif battle_detail[stage]["question_type"] == "input":
                action = None
                battle_detail[stage]["curr_qs"] = random.randint(0, len(verb[battle_detail[stage]["question"]])-1)
                correct = None
        else:
            
            # BG image
            draw_story_bg(stage)
            

            # left character
            talking = int(dialog[story_num][dialog_num][0])
            if talking == 1 or talking == 0:
                screen.blit(images[4], transform_scale([-139, 218]))
            else:
                screen.blit(images[7], transform_scale([-139, 218]))

            # right character
            if talking == 2 or talking == 0:
                screen.blit(images[5], transform_scale([1013, 280]))
            else:
                screen.blit(images[8], transform_scale([1013, 280]))

            # skip button
            screen.blit(images[6], transform_scale([1111, 35]))

            # dialog box
            pygame.draw.rect(screen, pygame.Color("#e8e8e8"), transform_scale([123, 766, 1193, 184]), border_radius=5)
            text(screen, dialog[story_num][dialog_num][1], (0, 0, 0), 48, transform_scale([153, 776]))

            #  effect
            if (dialog[story_num][dialog_num][0] == 1.1):
                if(time > 0 and time < fps*2):
                    time += 1
                    text_sp(screen, "あ", (120, 0, 0), 200, [WIDTH/2, HEIGHT/2], int((fps*2-time)/(fps*2)*255), "center")
                elif(time >= fps*2):
                    time = 0
            elif (dialog[story_num][dialog_num][0] == 2.1):
                if(time > 0 and time < fps*2):
                    time += 1
                    text_sp(screen, "か", (120, 255, 120), 200, transform_scale([220, 520]), int((fps*2-time)/(fps*2)*255), "center")
                elif(time >= fps*2):
                    time = 0
            elif time != 0:
                time = 0

            
            for event in pygame.event.get():
                # allow close game
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        
                        if click_check(pygame.mouse.get_pos(), transform_scale([1111, 35, 310, 80])):
                            # skip button
                            dialog_num = len(dialog[story_num])
                        else:
                            # next sentence
                            dialog_num += 1
                            if dialog_num != len(dialog[story_num]):
                                # effect list
                                if dialog[story_num][dialog_num][0] == 1.1 or dialog[story_num][dialog_num][0] == 2.1:
                                    time = 1

    if game_state == "playing":
        if battle_detail[stage]["question_type"] == "MC":
            # BG image
            screen.blit(images[3], (0, 0))

            # right character
            screen.blit(pygame.transform.flip(images[4], flip_x=True, flip_y=False), transform_scale([959, 263]))
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([1130, 0, 310, 80]))
            text(screen, "HP", (0, 0, 0), 24, transform_scale([1158, 22]))
            pygame.draw.rect(screen, (0, 0, 0), transform_scale([1209, 34, 204, 13]))
            pygame.draw.rect(screen, (255, 0, 0), transform_scale([1209, 34, player_hp/100*204, 13]))
            

            # left enemy
            screen.blit(pygame.transform.flip(images[battle_detail[stage]["enemy_surf"]], flip_x=True, flip_y=False), transform_scale([-51, 100]))
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([0, 0, 310, 80]))
            text(screen, "HP", (0, 0, 0), 24, transform_scale([28, 22]))
            pygame.draw.rect(screen, (0, 0, 0), transform_scale([79, 34, 204, 13]))
            pygame.draw.rect(screen, (255, 0, 0), transform_scale([79, 34, enemy_hp/battle_detail[stage]["enemy_hp"]*204, 13]))

            # discription
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([320, 0, 800, 80]))
            text(screen, battle_detail[stage]["discription"], (20, 20, 20), transform_scale([35])[0], transform_scale([720, 48]), "center")

            # Q&A box
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([324, 552, 791, 408]))
            if action == "attack" or action == "recover":
                pygame.draw.rect(screen, pygame.Color("#ececec"), transform_scale([407, 729, 194, 94]))
                pygame.draw.rect(screen, pygame.Color("#ececec"), transform_scale([840, 729, 194, 94]))
                pygame.draw.rect(screen, pygame.Color("#ececec"), transform_scale([407, 842, 194, 94]))
                pygame.draw.rect(screen, pygame.Color("#ececec"), transform_scale([840, 842, 194, 94]))

                text(screen, battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]], (0, 0, 0), 64, transform_scale([688, 601]), "center")
                
                text(screen, battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][0], (0, 0, 0), battle_detail[stage]["word_size"], transform_scale([504, 776]), "center")
                text(screen, battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][1], (0, 0, 0), battle_detail[stage]["word_size"], transform_scale([937, 776]), "center")
                text(screen, battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][2], (0, 0, 0), battle_detail[stage]["word_size"], transform_scale([504, 889]), "center")
                text(screen, battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][3], (0, 0, 0), battle_detail[stage]["word_size"], transform_scale([937, 889]), "center")
            else:
                pygame.draw.rect(screen, pygame.Color("#ececec"), transform_scale([407, 729, 194, 207]))
                pygame.draw.rect(screen, pygame.Color("#ececec"), transform_scale([840, 729, 194, 207]))
                text(screen, "攻擊", (0, 0, 0), 64, transform_scale([504, 813]), "center")
                text(screen, "回復", (0, 0, 0), 64, transform_scale([937, 813]), "center")


            for event in pygame.event.get():
                # allow close game
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        if action == "attack" or action == "recover":
                            if time == 0:
                                if click_check(pos, transform_scale([407, 729, 194, 94])):
                                    time = 1
                                    if battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][0] == battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][0]:
                                        correct = True
                                    else:
                                        correct = False
                                elif click_check(pos, transform_scale([840, 729, 194, 94])):
                                    time = 1
                                    if battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][1] == battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][0]:
                                        correct = True
                                    else:
                                        correct = False
                                elif click_check(pos, transform_scale([407, 842, 194, 94])):
                                    time = 1
                                    if battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][2] == battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][0]:
                                        correct = True
                                    else:
                                        correct = False
                                elif click_check(pos, transform_scale([840, 842, 194, 94])):
                                    time = 1
                                    if battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][3] == battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][0]:
                                        correct = True
                                    else:
                                        correct = False
                        else:
                            if click_check(pos, transform_scale([407, 729, 194, 207])):
                                action = "attack"
                            elif click_check(pos, transform_scale([840, 729, 194, 207])):
                                action = "recover"

            if correct == True:
                if action == "attack":
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]][0], (120, 0, 0), 200, transform_scale([220, 330]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    if time == 0:
                        enemy_hp -= 20 if not(god_mod) else 9999
                        correct = None
                        if stage == 0:
                            action = "attack"
                        else:
                            action = None
                        question_num += 1
                        if enemy_hp <= 0:
                            time = -1*fps
                            if (len(battle_detail[stage]["order"]) <= battle_detail[stage]["target"][0]):
                                save["star"][stage] = 3
                            elif (len(battle_detail[stage]["order"]) <= battle_detail[stage]["target"][1]):
                                if save["star"][stage] < 2:
                                    save["star"][stage] = 2
                            else:
                                if save["star"][stage] < 1:
                                    save["star"][stage] = 1
                            if len(save["unlock"])>save["current_stage"]+1:
                                save["unlock"][save["current_stage"]+1]=True
                            write()
                            game_state = "win"
                        else:
                            temp = random.randint(0, len(battle_detail[stage]["question"])-1)
                            while temp == battle_detail[stage]["order"][-1]:
                                temp = random.randint(0, len(battle_detail[stage]["question"])-1)
                            battle_detail[stage]["order"].append(temp)
                            random.shuffle(battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1])
                elif action == "recover":
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]][0], (120, 255, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    if time == 0:
                        player_hp = min(player_hp+20, 100)
                        correct = None
                        action = None
                        question_num += 1
                        temp = random.randint(0, len(battle_detail[stage]["question"])-1)
                        while temp == battle_detail[stage]["order"][-1]:
                            temp = random.randint(0, len(battle_detail[stage]["question"])-1)
                        battle_detail[stage]["order"].append(temp)
                        random.shuffle(battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1])
            elif correct == False:
                if action == "attack":
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, battle_detail[stage]["enemy_attack_word"], (120, 0, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    if time == 0:
                        player_hp -= 40
                        correct = None
                        if stage == 0:
                            action = "attack"
                        else:
                            action = None
                        question_num += 1
                        if player_hp <= 0:
                            time = -1*fps
                            game_state = "lose"
                        else:
                            temp = random.randint(0, len(battle_detail[stage]["question"])-1)
                            while temp == battle_detail[stage]["order"][-1]:
                                temp = random.randint(0, len(battle_detail[stage]["question"])-1)
                            battle_detail[stage]["order"].append(temp)
                            random.shuffle(battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1])
                elif action == "recover":
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]][0], (120, 255, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                        text_sp(screen, "╳", (120, 255, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    if time == 0:
                        player_hp -= 10
                        correct = None
                        action = None
                        question_num += 1
                        if player_hp <= 0:
                            time = -1*fps
                            game_state = "lose"
                        else:
                            temp = random.randint(0, len(battle_detail[stage]["question"])-1)
                            while temp == battle_detail[stage]["order"][-1]:
                                temp = random.randint(0, len(battle_detail[stage]["question"])-1)
                            battle_detail[stage]["order"].append(temp)
                            random.shuffle(battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1])

        elif battle_detail[stage]["question_type"] == "Drag":
            # BG image
            screen.blit(images[3], (0, 0))

            # right character
            screen.blit(pygame.transform.flip(images[4], flip_x=True, flip_y=False), transform_scale([959, 263]))
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([1130, 0, 310, 80]))
            text(screen, "HP", (0, 0, 0), 24, transform_scale([1158, 22]))
            pygame.draw.rect(screen, (0, 0, 0), transform_scale([1209, 34, 204, 13]))
            pygame.draw.rect(screen, (255, 0, 0), transform_scale([1209, 34, player_hp/100*204, 13]))


            # left enemy
            screen.blit(pygame.transform.flip(images[battle_detail[stage]["enemy_surf"]], flip_x=True, flip_y=False), transform_scale([-51, 100]))
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([0, 0, 310, 80]))
            text(screen, "HP", (0, 0, 0), 24, transform_scale([28, 22]))
            pygame.draw.rect(screen, (0, 0, 0), transform_scale([79, 34, 204, 13]))
            pygame.draw.rect(screen, (255, 0, 0), transform_scale([79, 34, enemy_hp/battle_detail[stage]["enemy_hp"]*204, 13]))

            # discription
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([320, 0, 800, 80]))
            text(screen, battle_detail[stage]["discription"], (20, 20, 20), transform_scale([35])[0], transform_scale([720, 48]), "center")

            q_index = battle_detail[stage]["order"][question_num]
            current_q = battle_detail[stage]["questions"][q_index]

            # If no action is chosen, show Attack/Recover options
            if action is None:
                pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([324, 552, 791, 408]))
                pygame.draw.rect(screen, pygame.Color("#ececec"), transform_scale([407, 729, 194, 207]))
                pygame.draw.rect(screen, pygame.Color("#ececec"), transform_scale([840, 729, 194, 207]))
                text(screen, "攻擊", (0, 0, 0), 64, transform_scale([504, 813]), "center")
                text(screen, "回復", (0, 0, 0), 64, transform_scale([937, 813]), "center")
            else: # An action has been chosen, show the question
                # Create rects for options if they don't exist for the current question
                if not draggable_rects:
                    options = current_q["options"]
                    option_y = transform_scale([800])[0]
                    option_width, option_height = transform_scale([180, 90])
                    total_width = len(options) * option_width + (len(options) - 1) * 20
                    start_x = (WIDTH - total_width) / 2
                    for i, option_text in enumerate(options):
                        rect = pygame.Rect(start_x + i * (option_width + 20), option_y, option_width, option_height)
                        draggable_rects.append(rect)
                        draggable_rects_initial_pos.append(rect.copy())

                # Draw question sentence with a blank
                sentence = current_q["sentence"]
                part1_text, separator, part2_text = sentence.partition('_')
                font_size = 64
                try: my_font = pygame.font.Font('media/LXGWMarkerGothic-Regular.ttf', transform_scale([font_size])[0])
                except: my_font = pygame.font.Font(pygame.font.get_default_font(), transform_scale([font_size])[0])

                part1_surf = my_font.render(part1_text, True, (0,0,0))
                part2_surf = my_font.render(part2_text, True, (0,0,0))
                box_width, box_height = transform_scale([120, 80])
                total_q_width = part1_surf.get_width() + box_width + part2_surf.get_width()

                start_q_x = (WIDTH - total_q_width) / 2
                q_y = transform_scale([400])[0]

                #grey box behind question area
                pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([324, 350, 791, 200]), border_radius=10)
                
                # Draw the first part of the sentence
                screen.blit(part1_surf, (start_q_x, q_y))
                
                # Define the drop target rect and draw it
                drop_target_rect = pygame.Rect(start_q_x + part1_surf.get_width(), q_y, box_width, box_height)
                pygame.draw.rect(screen, pygame.Color("#d9d9d9"), drop_target_rect, border_radius=5)
                pygame.draw.rect(screen, (0,0,0), drop_target_rect, 3, 5)

                # Draw the second part of the sentence
                screen.blit(part2_surf, (drop_target_rect.right, q_y))

                # Draw draggable options
                for i, rect in enumerate(draggable_rects):
                    if i != dragged_item_index: # Don't draw the original if it's being dragged
                        pygame.draw.rect(screen, pygame.Color("#ececec"), rect, border_radius=10)
                        text(screen, current_q["options"][i], (0,0,0), 50, rect.center, "center")

                if is_dragging and dragged_item_index != -1: # Draw dragged item on top
                    rect = draggable_rects[dragged_item_index]
                    pygame.draw.rect(screen, pygame.Color("#aaddff"), rect, border_radius=10)
                    text(screen, current_q["options"][dragged_item_index], (0,0,0), 50, rect.center, "center")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if time == 0:
                    if action is None:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if click_check(pos, transform_scale([407, 729, 194, 207])):
                                action = "attack"
                            elif click_check(pos, transform_scale([840, 729, 194, 207])):
                                action = "recover"
                    else: # Action is "attack" or "recover"
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not is_dragging:
                            for i, rect in enumerate(draggable_rects):
                                if rect.collidepoint(event.pos):
                                    is_dragging = True
                                    dragged_item_index = i
                                    drag_offset_x = event.pos[0] - rect.x
                                    drag_offset_y = event.pos[1] - rect.y
                                    break
                        elif event.type == pygame.MOUSEMOTION and is_dragging:
                            if dragged_item_index != -1:
                                draggable_rects[dragged_item_index].x = event.pos[0] - drag_offset_x
                                draggable_rects[dragged_item_index].y = event.pos[1] - drag_offset_y
                        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and is_dragging:
                            if drop_target_rect.colliderect(draggable_rects[dragged_item_index]):
                                selected_option = current_q["options"][dragged_item_index]
                                correct = (selected_option == current_q["answer"])
                                time = 1 # Trigger post-answer animation and logic
                            else: # If not on target, snap back to original position
                                draggable_rects[dragged_item_index] = draggable_rects_initial_pos[dragged_item_index].copy()

                            is_dragging = False
                            dragged_item_index = -1


            if correct == True:
                if action == "attack":
                    if(time > 0 and time < fps*1):
                        time += 1
                        q_text = current_q["answer"]
                        text_sp(screen, q_text, (120, 0, 0), 200, transform_scale([220, 330]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1): 
                        time = 0
                    
                    if time == 0:
                        enemy_hp -= 20 if not(god_mod) else 9999

                elif action == "recover":
                    if(time > 0 and time < fps*1):
                        time += 1
                        q_text = current_q["answer"]
                        text_sp(screen, q_text, (120, 255, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1): time = 0
                    
                    if time == 0:
                        player_hp = min(player_hp+20, 100)

                if time == 0:
                    correct = None 
                    question_num += 1
                    action = None
                    
                    if enemy_hp <= 0:
                        time = -1*fps 
                        if (question_num <= battle_detail[stage]["target"][0]):
                            save["star"][stage] = 3
                        elif (question_num <= battle_detail[stage]["target"][1]):
                            save["star"][stage] = max(save["star"][stage], 2)
                        else:
                            save["star"][stage] = max(save["star"][stage], 1)
                        
                        if save["current_stage"] + 1 < len(save["unlock"]):
                            save["unlock"][save["current_stage"]+1]=True
                        write()
                        game_state = "win"
                    else: 
                        draggable_rects.clear() 
                        draggable_rects_initial_pos.clear()
                        if question_num >= len(battle_detail[stage]["order"]):
                            random.shuffle(battle_detail[stage]["order"])
                            question_num = 0

            elif correct == False:
                if action == "attack":
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, battle_detail[stage]["enemy_attack_word"], (120, 0, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    
                    if time == 0:
                        player_hp -= 40
                        correct = None
                        question_num += 1
                        action = None
                        
                        if player_hp <= 0:
                            time = -1*fps
                            game_state = "lose"
                        else: 
                            draggable_rects.clear()
                            draggable_rects_initial_pos.clear()
                            if question_num >= len(battle_detail[stage]["order"]):
                                random.shuffle(battle_detail[stage]["order"])
                                question_num = 0
                elif action == "recover":
                    if(time > 0 and time < fps*1):
                        time += 1
                        q_text = current_q["answer"]
                        text_sp(screen, q_text, (120, 255, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                        text_sp(screen, "╳", (120, 255, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0

                    if time == 0:
                        player_hp -= 10
                        correct = None
                        question_num += 1
                        action = None
                        
                        if player_hp <= 0:
                            time = -1*fps
                            game_state = "lose"
                        else: 
                            draggable_rects.clear()
                            draggable_rects_initial_pos.clear()
                            if question_num >= len(battle_detail[stage]["order"]):
                                random.shuffle(battle_detail[stage]["order"])
                                question_num = 0

        elif battle_detail[stage]["question_type"] == "input":
            # BG image
            screen.blit(images[3], (0, 0))

            # right character
            screen.blit(pygame.transform.flip(images[4], flip_x=True, flip_y=False), transform_scale([959, 263]))
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([1130, 0, 310, 80]))
            text(screen, "HP", (0, 0, 0), 24, transform_scale([1158, 22]))
            pygame.draw.rect(screen, (0, 0, 0), transform_scale([1209, 34, 204, 13]))
            pygame.draw.rect(screen, (255, 0, 0), transform_scale([1209, 34, player_hp/100*204, 13]))
                

            # left enemy
            screen.blit(pygame.transform.flip(images[battle_detail[stage]["enemy_surf"]], flip_x=True, flip_y=False), transform_scale([-51, 100]))
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([0, 0, 310, 80]))
            text(screen, "HP", (0, 0, 0), 24, transform_scale([28, 22]))
            pygame.draw.rect(screen, (0, 0, 0), transform_scale([79, 34, 204, 13]))
            pygame.draw.rect(screen, (255, 0, 0), transform_scale([79, 34, enemy_hp/battle_detail[stage]["enemy_hp"]*204, 13]))

            # discription
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([320, 0, 800, 80]))
            text(screen, battle_detail[stage]["discription"], (20, 20, 20), transform_scale([35])[0], transform_scale([720, 48]), "center")

            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([324, 702, 791, 258]))
            

            if action == "attack" or action == "recover":
                # quesrion
                text(screen, verb[battle_detail[stage]["question"]][battle_detail[stage]["curr_qs"]], (0, 0, 0), transform_scale([64])[0], transform_scale([720, 751]), "center")

                # display input as hiragana
                pygame.draw.rect(screen, pygame.Color("#ececec"), transform_scale([400, 780, 640, 64]))
                text(screen, outputArr, (0, 0, 0), transform_scale([64])[0], transform_scale([720, 805]), "center")
                # display input as romaji
                pygame.draw.rect(screen, pygame.Color("#ececec"), transform_scale([400, 865, 640, 64]))
                text(screen, inputArr, (0, 0, 0), transform_scale([64])[0], transform_scale([720, 900]), "center")
            else:
                pygame.draw.rect(screen, pygame.Color("#ececec"), transform_scale([407, 729, 194, 207]))
                pygame.draw.rect(screen, pygame.Color("#ececec"), transform_scale([840, 729, 194, 207]))
                text(screen, "攻擊", (0, 0, 0), 64, transform_scale([504, 813]), "center")
                text(screen, "回復", (0, 0, 0), 64, transform_scale([937, 813]), "center")
            
            
            for event in pygame.event.get():
                # allow close game
                if event.type == pygame.QUIT:
                    running = False
                # set up in-game keyboard input
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        if action == None:
                            if click_check(pos, transform_scale([407, 729, 194, 207])):
                                action = "attack"
                            elif click_check(pos, transform_scale([840, 729, 194, 207])):
                                action = "recover"
                if event.type == pygame.KEYDOWN and time == 0:
                    if action == "attack" or action == "recover":
                        if event.type == pygame.KEYDOWN and time == 0:
                            print(verb[battle_detail[stage]["answer"]+"_hira"][battle_detail[stage]["curr_qs"]])
                            if event.key != pygame.K_RETURN and event.key != pygame.K_KP_ENTER:
                                if event.key == pygame.K_a:
                                    inputArr = inputArr + 'a'
                                if event.key == pygame.K_b:
                                    inputArr = inputArr + 'b'
                                if event.key == pygame.K_c:
                                    inputArr = inputArr + 'c'
                                if event.key == pygame.K_d:
                                    inputArr = inputArr + 'd'
                                if event.key == pygame.K_e:
                                    inputArr = inputArr + 'e'
                                if event.key == pygame.K_f:
                                    inputArr = inputArr + 'f'
                                if event.key == pygame.K_g:
                                    inputArr = inputArr + 'g'
                                if event.key == pygame.K_h:
                                    inputArr = inputArr + 'h'
                                if event.key == pygame.K_i:
                                    inputArr = inputArr + 'i'
                                if event.key == pygame.K_j:
                                    inputArr = inputArr + 'j'
                                if event.key == pygame.K_k:
                                    inputArr = inputArr + 'k'
                                if event.key == pygame.K_l:
                                    inputArr = inputArr + 'l'
                                if event.key == pygame.K_m:
                                    inputArr = inputArr + 'm'
                                if event.key == pygame.K_n:
                                    inputArr = inputArr + 'n'
                                if event.key == pygame.K_o:
                                    inputArr = inputArr + 'o'
                                if event.key == pygame.K_p:
                                    inputArr = inputArr + 'p'
                                if event.key == pygame.K_q:
                                    inputArr = inputArr + 'q'
                                if event.key == pygame.K_r:
                                    inputArr = inputArr + 'r'
                                if event.key == pygame.K_s:
                                    inputArr = inputArr + 's'
                                if event.key == pygame.K_t:
                                    inputArr = inputArr + 't'
                                if event.key == pygame.K_u:
                                    inputArr = inputArr + 'u'
                                if event.key == pygame.K_v:
                                    inputArr = inputArr + 'v'
                                if event.key == pygame.K_w:
                                    inputArr = inputArr + 'w'
                                if event.key == pygame.K_x:
                                    inputArr = inputArr + 'x'
                                if event.key == pygame.K_y:
                                    inputArr = inputArr + 'y'
                                if event.key == pygame.K_z:
                                    inputArr = inputArr + 'z'
                                if event.key == pygame.K_BACKSPACE:
                                    inputArr = inputArr[:-1]
                                outputArr = textinput(inputArr)
                            else:
                                # event after pressing Enter key
                                time = 1
                                battle_detail[stage]["counter"] += 1
                                if verb[battle_detail[stage]["answer"]+"_hira"][battle_detail[stage]["curr_qs"]] == outputArr:
                                    correct = True
                                else:
                                    correct = False


                
            
            if correct == True:
                if action == "attack":
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, verb[battle_detail[stage]["question"]][battle_detail[stage]["curr_qs"]][0], (120, 0, 0), 200, transform_scale([220, 330]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    if time == 0:
                        enemy_hp -= 20 if not(god_mod) else 9999
                        correct = None
                        action = None
                        if enemy_hp <= 0:
                            time = -1*fps
                            if (battle_detail[stage]["counter"] <= battle_detail[stage]["target"][0]):
                                save["star"][stage] = 3
                            elif (battle_detail[stage]["counter"] <= battle_detail[stage]["target"][1]):
                                if save["star"][stage] < 2:
                                    save["star"][stage] = 2
                            else:
                                if save["star"][stage] < 1:
                                    save["star"][stage] = 1
                            if len(save["unlock"])>save["current_stage"]+1:
                                save["unlock"][save["current_stage"]+1]=True
                            write()
                            game_state = "win"
                        else:
                            temp = random.randint(0, len(verb[battle_detail[stage]["question"]])-1)
                            while temp == battle_detail[stage]["curr_qs"]:
                                temp = random.randint(0, len(verb[battle_detail[stage]["question"]])-1)
                            battle_detail[stage]["curr_qs"] = temp
                            inputArr = ""
                            outputArr = ""
                elif action == "recover":
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, verb[battle_detail[stage]["question"]][battle_detail[stage]["curr_qs"]][0], (120, 255, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    if time == 0:
                        player_hp = min(player_hp+20, 100)
                        correct = None
                        action = None
                        temp = random.randint(0, len(verb[battle_detail[stage]["question"]])-1)
                        while temp == battle_detail[stage]["curr_qs"]:
                            temp = random.randint(0, len(verb[battle_detail[stage]["question"]])-1)
                        battle_detail[stage]["curr_qs"] = temp
                        inputArr = ""
                        outputArr = ""
            elif correct == False:
                if action == "attack":
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, battle_detail[stage]["enemy_attack_word"], (120, 0, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    if time == 0:
                        player_hp -= 40
                        correct = None
                        if stage == 0:
                            action = "attack"
                        else:
                            action = None
                        if player_hp <= 0:
                            time = -1*fps
                            game_state = "lose"
                        else:
                            temp = random.randint(0, len(verb[battle_detail[stage]["question"]])-1)
                            while temp == battle_detail[stage]["curr_qs"]:
                                temp = random.randint(0, len(verb[battle_detail[stage]["question"]])-1)
                            battle_detail[stage]["curr_qs"] = temp
                            inputArr = ""
                            outputArr = ""
                elif action == "recover":
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, verb[battle_detail[stage]["question"]][battle_detail[stage]["curr_qs"]][0], (120, 255, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                        text_sp(screen, "╳", (120, 255, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    if time == 0:
                        player_hp -= 10
                        correct = None
                        action = None
                        if player_hp <= 0:
                            time = -1*fps
                            game_state = "lose"
                        else:
                            temp = random.randint(0, len(verb[battle_detail[stage]["question"]])-1)
                            while temp == battle_detail[stage]["curr_qs"]:
                                temp = random.randint(0, len(verb[battle_detail[stage]["question"]])-1)
                            battle_detail[stage]["curr_qs"] = temp
                            inputArr = ""
                            outputArr = ""

    # stage select
    if game_state == "select_stage":
        

        # bg image, text, center image, nearby image
        draw_stage_selection(save['current_stage'])
        
        # left right arrow
        if (save['current_stage'] != 0):
            screen.blit(images[11], transform_scale([162, 424]))
        if (save['current_stage']+1 != len(save["star"])):
            screen.blit(pygame.transform.flip(images[11], flip_x=True, flip_y=False), transform_scale([1186, 424]))

        # star
        if save['star'][save['current_stage']] == 0:
            screen.blit(images[13], transform_scale([540, 139]))
        elif save['star'][save['current_stage']] == 1:
            screen.blit(images[14], transform_scale([540, 139]))
        elif save['star'][save['current_stage']] == 2:
            screen.blit(images[15], transform_scale([540, 139]))
        elif save['star'][save['current_stage']] == 3:
            screen.blit(images[16], transform_scale([540, 139]))

        if(time != 0):
            time += 1
            s.set_alpha(int(time/fps/2*255))
            screen.blit(s, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if click_check(pygame.mouse.get_pos(), transform_scale([1186, 424, 75, 110])):
                        if (save['current_stage']+1 < len(save["star"])):
                            save['current_stage'] += 1
                            write()
                    if click_check(pygame.mouse.get_pos(), transform_scale([162, 424, 75, 110])):
                        if (save['current_stage'] > 0):
                            save['current_stage'] -= 1
                            write()
                    if click_check(pygame.mouse.get_pos(), transform_scale([297, 198, 847, 635])):
                        if (save['unlock'][save["current_stage"]]):
                            if (time == 0):
                                time += 1
        # enter story
        if(time > fps*2):
            game_state = "story"
            story_num = save["current_stage"]
            dialog_num = 0
            time = 0

    # this is game state of winning the game
    if game_state == "win" or game_state == "lose":
        # BG image
        screen.blit(images[3], (0, 0))

        # right character
        screen.blit(pygame.transform.flip(images[4], flip_x=True, flip_y=False), transform_scale([959, 263]))
        pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([1130, 0, 310, 80]))
        text(screen, "HP", (0, 0, 0), 24, transform_scale([1158, 22]))
        pygame.draw.rect(screen, (0, 0, 0), transform_scale([1209, 34, 204, 13]))
        pygame.draw.rect(screen, (255, 0, 0), transform_scale([1209, 34, player_hp/100*204, 13]))
        

        # left enemy
        screen.blit(pygame.transform.flip(images[battle_detail[stage]["enemy_surf"]], flip_x=True, flip_y=False), transform_scale([-51, 100]))
        pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([0, 0, 310, 80]))
        text(screen, "HP", (0, 0, 0), 24, transform_scale([28, 22]))
        pygame.draw.rect(screen, (0, 0, 0), transform_scale([79, 34, 204, 13]))
        pygame.draw.rect(screen, (255, 0, 0), transform_scale([79, 34, enemy_hp/battle_detail[stage]["enemy_hp"]*204, 13]))

        # darken the screen
        s.set_alpha(125)
        screen.blit(s, (0,0))

        # continue
        if (time>=0):
            screen.blit(images[22], transform_scale([460, 760]))
            text(screen, "繼續", (0, 0, 0), transform_scale([50])[0], transform_scale([720, 815]), "center")
        
        if game_state == "win":
            text_sp(screen, "靈\n殺", (200, 200, 200), transform_scale([200])[0], [WIDTH/2, HEIGHT/2], 255, "center")
        elif game_state == "lose":
            text_sp(screen, "死", (150, 0, 0), transform_scale([200])[0], [WIDTH/2, HEIGHT/2], 255, "center")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if click_check(pygame.mouse.get_pos(), transform_scale([460, 760, 520, 110])):
                            if (time == 0):
                                time += 1
        if (time<0):
            time += 1

        if(time > 0):
            time += 1
            s.set_alpha(int(time/fps/1*255))
            screen.blit(s, (0,0))

        # enter story
        if(time > fps*1):
            game_state = "select_stage"
            time = 0


        

    clock.tick(fps)
    pygame.display.update()

