import pygame, random, os, math, json, sys
from copy import deepcopy

#basic set up for pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# this is for running python main.py
path = os.path.dirname(os.path.abspath(__file__)) + '/'

# this is for running the executable file
# path = os.path.dirname(os.path.realpath(sys.executable)) + '/'

new_game = False
god_mod = True
chapter_ranges =[(0, 8), (9, 19), (20, 28), (29, 38)] # (Start Stage, End Stage) for Ch 1, 2, 3, 4
current_chapter = 0

save = {
    'unlock': [True] + [False]*38,
    'star': [0]*39,
    'current_stage': 0,
    'achievement': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
    'obtain': [False, False, False, False, False, False, False],  # C_weapon, C_equiptment, A_weapon, A_equiptment, SS_weapon, SS_equiptment, ex_weapon
    'equipt': [7, 8],  # weapon, equiptment. 7, 8 mean empty. number follow 'obtain' index
    'obtain_w_n': 0,
    'obtain_e_n': 0,
    'last_play': [0, 0], # stage_number, continus_times
    'sound': 100,
    'music': 100,
    'full_screen': False,
    'hard': False,
    'chosen_path': 34,
}

WIDTH  = int(pygame.display.Info().current_w * 0.65)
# WIDTH  = 500
HEIGHT = int(WIDTH/1440*960)

def transform_scale(arr):
    return [int(n*WIDTH/1440) for n in arr]

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
            if len(save['unlock']) < 39:
                save['unlock'].extend([False] * (39 - len(save['unlock'])))
                save['star'].extend([0] * (39 - len(save['star'])))
            if 'chosen_path' not in save:
                save['chosen_path'] = 34
            if 'hard' not in save:
                save['hard'] = False
            if 'equipt' in save:
                if save['equipt'][0] not in [0, 2, 4, 6, 7]:
                    save['equipt'][0] = 7  # 7 代表未裝備武器
                if save['equipt'][1] not in [1, 3, 5, 6, 8]:
                    save['equipt'][1] = 8  # 8 代表未裝備防具
            write()
            print("Loaded data:", save)
    except:
        print("File not found. Creating a new one.")
        with open('udata.sf', 'w') as store_file:
            json.dump(deepcopy(save), store_file)

def write():
    with open('udata.sf', 'w') as store_data:
        json.dump(save, store_data)

STAGE_TITLES = [
    "第一章 - 初始之森", "第一章 - 五十音(1)", "第一章 - 五十音(2)", "第一章 - 哥布林來襲", "第一章 - 幻影虎", 
    "第一章 - 五十音(3)", "第一章 - 五十音(4)", "第一章 - 全力防禦", "第一章 - 幻影虎(終)",
    "第二章 - 漢字初識", "第二章 - 血脈覺醒", "第二章 - 基礎漢字", "第二章 - 迷惘", "第二章 - 詞彙", 
    "第二章 - 瘴氣森林", "第二章 - 形容詞", "第二章 - 震動", "第二章 - 清除小怪", "第二章 - 危機", "第二章 - 天魔降臨",
    "第三章 - 句子結構", "第三章 - 助詞用法", "第三章 - 主謂賓", "第三章 - 擴充句型", "第三章 - 動詞辞書形", 
    "第三章 - 動詞て形", "第三章 - 動詞ない形", "第三章 - 動詞た形", "第三章 - 魔龍降臨",
    "終章 - 忘我之路", "終章 - 南方大將", "終章 - 西方大將", "終章 - 北方大將", "終章 - 魔王寶座",
    "決戰 - 勇者之路", "決戰 - 南方大將", "決戰 - 西方大將", "決戰 - 北方大將", "決戰1 - 獄煌聖所"
]

def draw_stage_selection(n):



    match n:
        case 0:
            bg = 10
            center = 17
            title = 39
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
            title = 40
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 17
                else:
                    next = 18
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
                center = 17
            else:
                center = 18
            title = 41
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 17
                else:
                    next = 18
            else:
                next = None
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        
        case 3:
            bg = 10
            if save["unlock"][n]:
                center = 17
            else:
                center = 18
            title = 42
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 17
                else:
                    next = 18
            else:
                next = None
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        case 4:
            bg = 10
            if save["unlock"][n]:
                center = 17
            else:
                center = 18
            title = 43
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 17
                else:
                    next = 18
            else:
                next = None
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        case 5:
            #require changing
            bg = 10
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 17
            else:
                center = 18
            # the title text, but in image format, Jeff can help gen
            title = 44
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 17
                else:
                    next = 18
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        case 6:
            bg = 10
            if save["unlock"][n]:
                center = 17
            else:
                center = 18
            title = 45
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 17
                else:
                    next = 18
            else:
                next = None
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        case 7:
            #require changing
            bg = 10
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 17
            else:
                center = 18
            # the title text, but in image format, Jeff can help gen
            title = 46
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 17
                else:
                    next = 18
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        case 8:
            #require changing
            bg = 10
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 17
            else:
                center = 18
            # the title text, but in image format, Jeff can help gen
            title = 47
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = None
                else:
                    next = None
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        case 9:
            #require changing
            bg = 88
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 20
            else:
                center = 19
            # the title text, but in image format, Jeff can help gen
            title = 48
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
                prev = None
            else:
                prev = None
        case 10:
            #require changing
            bg = 88
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 20
            else:
                center = 19
            # the title text, but in image format, Jeff can help gen
            title = 49
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
                prev = 20
            else:
                prev = 19
        case 11:
            #require changing
            bg = 88
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 20
            else:
                center = 19
            # the title text, but in image format, Jeff can help gen
            title = 50
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
                prev = 20
            else:
                prev = 19
        case 12:
            #require changing
            bg = 88
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 20
            else:
                center = 19
            # the title text, but in image format, Jeff can help gen
            title = 51
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
                prev = 20
            else:
                prev = 19
        case 13:
            #require changing
            bg = 88
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 20
            else:
                center = 19
            # the title text, but in image format, Jeff can help gen
            title = 52
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
                prev = 20
            else:
                prev = 19
        case 14:
            #require changing
            bg = 88
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 20
            else:
                center = 19
            # the title text, but in image format, Jeff can help gen
            title = 53
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
                prev = 20
            else:
                prev = 19
        case 15:
            #require changing
            bg = 88
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 20
            else:
                center = 19
            # the title text, but in image format, Jeff can help gen
            title = 54
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
                prev = 20
            else:
                prev = 19
        case 16:
            #require changing
            bg = 88
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 20
            else:
                center = 19
            # the title text, but in image format, Jeff can help gen
            title = 55
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
                prev = 20
            else:
                prev = 19
        case 17:
            #require changing
            bg = 88
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 20
            else:
                center = 19
            # the title text, but in image format, Jeff can help gen
            title = 56
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
                prev = 20
            else:
                prev = 19
        case 18:
            #require changing
            bg = 88
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 20
            else:
                center = 19
            # the title text, but in image format, Jeff can help gen
            title = 57
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
                prev = 20
            else:
                prev = 19
        case 19:
            #require changing
            bg = 88
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 20
            else:
                center = 19
            # the title text, but in image format, Jeff can help gen
            title = 58
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = None
                else:
                    next = None
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 20
            else:
                prev = 19
        case 20:
            #require changing
            bg = 87
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 17
            else:
                center = 18
            # the title text, but in image format, Jeff can help gen
            title = 59
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 17
                else:
                    next = 18
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = None
            else:
                prev = None
        case 21:
            #require changing
            bg = 87
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 17
            else:
                center = 18
            # the title text, but in image format, Jeff can help gen
            title = 60
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 17
                else:
                    next = 18
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        case 22:
            #require changing
            bg = 87
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 17
            else:
                center = 18
            # the title text, but in image format, Jeff can help gen
            title = 61
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 17
                else:
                    next = 18
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        case 23:
            #require changing
            bg = 87
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 17
            else:
                center = 18
            # the title text, but in image format, Jeff can help gen
            title = 62
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 17
                else:
                    next = 18
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        case 24:
            #require changing
            bg = 87
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 17
            else:
                center = 18
            # the title text, but in image format, Jeff can help gen
            title = 63
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 17
                else:
                    next = 18
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        case 25:
            #require changing
            bg = 87
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 17
            else:
                center = 18
            # the title text, but in image format, Jeff can help gen
            title = 64
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 17
                else:
                    next = 18
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        case 26:
            #require changing
            bg = 87
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 17
            else:
                center = 18
            # the title text, but in image format, Jeff can help gen
            title = 65
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 17
                else:
                    next = 18
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        case 27:
            #require changing
            bg = 87
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 17
            else:
                center = 18
            # the title text, but in image format, Jeff can help gen
            title = 66
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 17
                else:
                    next = 18
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        case 28:
            #require changing
            bg = 87
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 17
            else:
                center = 18
            # the title text, but in image format, Jeff can help gen
            title = 67
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = None
                else:
                    next = None
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 17
            else:
                prev = 18
        case 29:
            #require changing
            bg = 25
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 27
            else:
                center = 26
            # the title text, but in image format, Jeff can help gen
            title = 68
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 27
                else:
                    next = 26
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = None
            else:
                prev = None
        case 30:
            #require changing
            bg = 25
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 27
            else:
                center = 26
            # the title text, but in image format, Jeff can help gen
            title = 69
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 27
                else:
                    next = 26
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 27
            else:
                prev = 26
        case 31:
            #require changing
            bg = 25
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 27
            else:
                center = 26
            # the title text, but in image format, Jeff can help gen
            title = 70
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 27
                else:
                    next = 26
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 27
            else:
                prev = 26
        case 32:
            #require changing
            bg = 25
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 27
            else:
                center = 26
            # the title text, but in image format, Jeff can help gen
            title = 71
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 27
                else:
                    next = 26
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 27
            else:
                prev = 26
        case 33:
            #require changing
            bg = 25
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 27
            else:
                center = 26
            # the title text, but in image format, Jeff can help gen
            title = 72
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 27
                else:
                    next = 26
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 27
            else:
                prev = 26
        case 34:
           #require changing
            bg = 25
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 27
            else:
                center = 26
            # the title text, but in image format, Jeff can help gen
            title = 73
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 27
                else:
                    next = 26
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = None
            else:
                prev = None
        case 35:
            #require changing
            bg = 25
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 27
            else:
                center = 26
            # the title text, but in image format, Jeff can help gen
            title = 74
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 27
                else:
                    next = 26
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 27
            else:
                prev = 26
        case 36:
            #require changing
            bg = 25
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 27
            else:
                center = 26
            # the title text, but in image format, Jeff can help gen
            title = 75
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 27
                else:
                    next = 26
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 27
            else:
                prev = 26
        case 37:
            #require changing
            bg = 25
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 27
            else:
                center = 26
            # the title text, but in image format, Jeff can help gen
            title = 76
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = 27
                else:
                    next = 26
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 27
            else:
                prev = 26
        case 38:
            #require changing
            bg = 25
            # image at center, if havent unlock then will show the gray version
            if save["unlock"][n]:
                center = 27
            else:
                center = 26
            # the title text, but in image format, Jeff can help gen
            title = 77
            #image of next stage
            if n+1 < len(save["unlock"]):
                if save["unlock"][n+1]:
                    next = None
                else:
                    next = None
            else:
                next = None
            # image of previos stage
            if save["unlock"][n-1]:
                prev = 27
            else:
                prev = 26
        

    screen.blit(images[bg], transform_scale([0, 0]))
    screen.blit(images[center], transform_scale([297, 198]))

    r = images[title].get_rect()
    r.center = screen.get_rect().center
    r.y = HEIGHT*0.08
    screen.blit(images[title], r)
    if prev is not None:
        screen.blit(images[prev], transform_scale([-600, 198]))
        
    # Draw next stage image on the right (if it exists)
    if next is not None:
        screen.blit(images[next], transform_scale([1194, 198]))

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
        case 5:
            screen.blit(images[3], (0, 0))
        case 6:
            screen.blit(images[3], (0, 0))
        case 7:
            screen.blit(images[3], (0, 0))
        case 8:
            screen.blit(images[3], (0, 0))
        case 9:
            screen.blit(images[3], (0, 0))
        case 10:
            screen.blit(images[3], (0, 0))
        case 11:
            screen.blit(images[3], (0, 0))
        case 12:
            screen.blit(images[3], (0, 0))
        case 13:
            screen.blit(images[3], (0, 0))
        case 14:
            screen.blit(images[3], (0, 0))
        case 15:
            screen.blit(images[3], (0, 0))
        case 16:
            screen.blit(images[3], (0, 0))
        case 17:
            screen.blit(images[3], (0, 0))
        case 18:
            screen.blit(images[3], (0, 0))
        case 19:
            screen.blit(images[3], (0, 0))
        case 20:
            screen.blit(images[3], (0, 0))
        case 21:
            screen.blit(images[3], (0, 0))
        case 22:
            screen.blit(images[3], (0, 0))
        case 23:
            screen.blit(images[3], (0, 0))
        case 24:
            screen.blit(images[3], (0, 0))
        case 25:
            screen.blit(images[3], (0, 0))
        case 26:
            screen.blit(images[3], (0, 0))
        case 27:
            screen.blit(images[3], (0, 0))
        case 28:
            screen.blit(images[3], (0, 0))
        case 29:
            screen.blit(images[3], (0, 0))
        case 30:
            screen.blit(images[3], (0, 0))
        case 31:
            screen.blit(images[3], (0, 0))
        case 32:
            screen.blit(images[3], (0, 0))
        case 33:
            screen.blit(images[3], (0, 0))
        case 34:
            screen.blit(images[3], (0, 0))
        case 35:
            screen.blit(images[3], (0, 0))
        case 36:
            screen.blit(images[3], (0, 0))
        case 37:
            screen.blit(images[3], (0, 0))  
        case 38:
            screen.blit(images[3], (0, 0))             

def end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage):
    if(sum(save["star"]) >= int(len(battle_detail)*3/2) and not(save["achievement"][4])):
        save["achievement"][4] = True
        achievement_stack.append([4, fps])
    if(sum(save["star"]) >= int(len(battle_detail)*3) and not(save["achievement"][5])):
        save["achievement"][5] = True
        achievement_stack.append([5, fps])

    if (recover_times > 5 and not(save["achievement"][0])):
        save["achievement"][0] = True
        achievement_stack.append([0, fps])
    if (recover_times > 15 and not(save["achievement"][1])):
        save["achievement"][1] = True
        achievement_stack.append([1, fps])
    if (recover_times > 30 and not(save["achievement"][2])):
        save["achievement"][2] = True
        achievement_stack.append([2, fps])
    if (damage_taken_times == 0 and not(save["achievement"][6])):
        save["achievement"][6] = True
        achievement_stack.append([6, fps])
    if (0 < player_hp <= 100*0.1 and not(save["achievement"][7])):
        save["achievement"][7] = True
        achievement_stack.append([7, fps])
    if (idle_times >= fps*60*15 and not(save["achievement"][21])):
        save["achievement"][21] = True
        achievement_stack.append([21, fps])
    if(attack_times == 0 and not(save["achievement"][20])):
        save["achievement"][20] = True
        achievement_stack.append([20, fps])

    if(player_hp > 0):
        if(stage == save['last_play'][0]):
            save['last_play'][1] += 1
            if(save['last_play'][1] >= 5 and not(save["achievement"][9])):
                save["achievement"][9] = True
                achievement_stack.append([9, fps])
        else:
            save['last_play'] = [stage, 1]
    else:
        save['last_play'] = [0, 0]

    if(stage == 8 and not(save["achievement"][10])):
        save["achievement"][10] = True
        achievement_stack.append([10, fps])
    elif(stage == 23 and not(save["achievement"][11])):
        save["achievement"][11] = True
        achievement_stack.append([11, fps])
    elif(stage == 19 and not(save["achievement"][12])):
        save["achievement"][12] = True
        achievement_stack.append([12, fps])
    elif(stage == 28 and not(save["achievement"][13])):
        save["achievement"][13] = True
        achievement_stack.append([13, fps])
    elif(stage == 33 and not(save["achievement"][23])):
        save["achievement"][23] = True
        achievement_stack.append([23, fps])
    elif(stage == 38 and not(save["achievement"][24])):
        save["achievement"][24] = True
        achievement_stack.append([24, fps])
    elif(stage == 33 and not(save["achievement"][27]) and save['equipt'][0] == 7 and save['equipt'][1] == 8): # here, no equiptment
        save["achievement"][27] = True
        achievement_stack.append([27])
    elif(stage == 38 and not(save["achievement"][27]) and save['equipt'][0] == 7 and save['equipt'][1] == 8): # here, no equiptment
        save["achievement"][27] = True
        achievement_stack.append([27, fps])
    elif(stage == 33 and not(save["achievement"][26]) and save['hard']): # here, 2nd round
        save["achievement"][26] = True
        achievement_stack.append([26])
    elif(stage == 38 and not(save["achievement"][26]) and save['hard']): # here, 2nd round
        save["achievement"][26] = True
        achievement_stack.append([26])

    elif(stage == 8 and not(save["achievement"][14])):
        save["achievement"][14] = True
        achievement_stack.append([14, fps])
        save["obtain"][0] = True
        save["obtain_w_n"] += 1
    elif(stage == 5 and not(save["achievement"][15])):
        save["achievement"][15] = True
        achievement_stack.append([15, fps])
        save["obtain"][1] = True
        save["obtain_e_n"] += 1
    elif(stage == 19 and not(save["achievement"][16])):
        save["achievement"][16] = True
        achievement_stack.append([16, fps])
        save["obtain"][2] = True
        save["obtain_w_n"] += 1
    elif(stage == 19 and not(save["achievement"][17])):
        save["achievement"][17] = True
        achievement_stack.append([17, fps])
        save["obtain"][3] = True
        save["obtain_e_n"] += 1
    elif(stage == 34 and not(save["achievement"][18])):
        save["achievement"][18] = True
        achievement_stack.append([18, fps])
        save["obtain"][4] = True
        save["obtain_w_n"] += 1
    elif(stage == 28 and not(save["achievement"][19])):
        save["achievement"][19] = True
        achievement_stack.append([19, fps])
        save["obtain"][5] = True
        save["obtain_e_n"] += 1
    elif(stage == 28 and not(save["achievement"][22])):
        save["achievement"][22] = True
        achievement_stack.append([22, fps])
        save["obtain"][6] = True
        save["obtain_w_n"] += 1
        save["obtain_e_n"] += 1
    
    if(attack_times == 1 and click_times == 0 and not(save["achievement"][28])):
        save["achievement"][28] = True
        achievement_stack.append([28, fps])

    if (not(save["achievement"][29])):
        if(sum(save["achievement"]) == 29):
            save["achievement"][29] = True
            achievement_stack.append([29, fps])
    write()


def draw_achievemet_stack():
    if(achievement_stack[0][1] > 0):
        pygame.draw.rect(screen, [47, 47, 47], transform_scale([1040, 860, 400, 100]))
        pygame.draw.rect(screen, [0, 0, 0], transform_scale([1040, 860, 400, 100]), transform_scale([4])[0])
        pygame.draw.rect(screen, [178, 250, 178], transform_scale([1050, 870, 80, 80]))
        text_sp(screen, achievement_data["icon"][achievement_stack[0][0]][0], achievement_data["icon"][achievement_stack[0][0]][1], 4*18, transform_scale([1090, 910]), 255, "center")
        text(screen, achievement_data["unlock_title"][achievement_stack[0][0]], [200, 200, 200], 4*8, transform_scale([1140, 900]), "left")

        achievement_stack[0][1] -= 1
    elif(achievement_stack[0][1] < -12):
        achievement_stack.pop(0)
    else:
        achievement_stack[0][1] -= 1
        

# os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((pygame.display.get_desktop_sizes()[0][0]-WIDTH)/2, 20)
os.environ['SDL_VIDEO_CENTERED'] = '1'


load()

if new_game:
    save = {
        'unlock': [True] + [False]*38,
        'star': [0]*39,
        'current_stage': 0,
        'achievement': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, ],
        'obtain': [False, False, False, False, False, False, False],  # C_weapon, C_equiptment, A_weapon, A_equiptment, SS_weapon, SS_equiptment, ex_weapon
        'equipt': [7, 8],  # weapon, equiptment. 7, 8 mean empty. number follow 'obtain' index
        'obtain_w_n': 0,
        'obtain_e_n': 0,
        'last_play': [0, 0], # stage_number, continus_times
        'sound': 100,
        'music': 100,
        'full_screen': False,
        'hard': False,
        'chosen_path': 34,
    }
if god_mod:
    save = {
        'unlock': [True]*39,
        'star': [0]*39,
        'current_stage': 0,
        # 'achievement': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, ],
        'achievement': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, ],
        'obtain': [True, True, True, True, True, True, True],  # C_weapon, C_equiptment, A_weapon, A_equiptment, SS_weapon, SS_equiptment, ex_weapon
        'equipt': [7, 8],  # weapon, equiptment. 7, 8 mean empty. number follow 'obtain' index
        'obtain_w_n': 4,
        'obtain_e_n': 4,
        'last_play': [0, 0], # stage_number, continus_times
        'sound': 100,
        'music': 100,
        'full_screen': False,
        'hard': False,
        'chosen_path': 34,
    }
# question bank: verb form convertion
# size: 27
# choose_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# not_chosen_list = []


if save["full_screen"]:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Learn Japanese!")
clock = pygame.time.Clock()
fps = 60



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
     

achievement_data = {
    'icon':[
        ["回", [255, 255, 255]], 
        ["回", [128, 128, 128]], 
        ["回", [0, 0, 0]], 
        ["星", [255, 255, 255]], 
        ["星", [128, 128, 128]], 
        ["星", [0, 0, 0]], 
        ["閃", [252, 186, 3]], 
        ["根", [69, 133, 0]], 
        ["超", [224, 49, 0]], 
        ["連", [0, 141, 242]], 
        ["音", [226, 242, 0]], 
        ["順", [27, 54, 97]], 
        ["漢", [168, 79, 0]], 
        ["換", [227, 176, 36]], 
        ["武", [255, 255, 255]], 
        ["防", [255, 255, 255]], 
        ["武", [128, 128, 128]], 
        ["防", [128, 128, 128]], 
        ["武", [0, 0, 0]], 
        ["防", [0, 0, 0]], 
        ["點", [156, 156, 156]], 
        ["石", [92, 92, 92]], 
        ["魔", [108, 0, 128]], 
        ["終", [255, 201, 254]], 
        ["終", [255, 251, 201]], 
        ["迴", [0, 224, 198]], 
        ["難", [117, 10, 0]], 
        ["裸", [255, 255, 255]], 
        ["一", [255, 21, 0]], 
        ["全", [255, 227, 46]], 
    ],
    'hidden_title': [
        "小回復術士", 
        "普通回復術士", 
        "大回復術士", 
        "滿分", 
        "半天星", 
        "滿天星", 
        "無損", 
        "根性", 
        "超越", 
        "努力不懈", 
        "五十音", 
        "次序很重要", 
        "熟悉的字(?", 
        "英雄級冒險者", 
        "C級武器", 
        "C級防具", 
        "A級武器", 
        "A級防具", 
        "SS級武器", 
        "SS級防具", 
        "一拳不行就多一拳", 
        "等到天荒地老", 
        "???", 
        "????", 
        "????", 
        "再度轉生", 
        "迎難而上", 
        "史上最強豆腐", 
        "一拳超人", 
        "勇者", 
    ],
    'unlock_title': [
        "小回復術士", 
        "普通回復術士", 
        "大回復術士", 
        "滿分", 
        "半天星", 
        "滿天星", 
        "無損", 
        "根性", 
        "超越", 
        "努力不懈", 
        "五十音", 
        "次序很重要", 
        "熟悉的字(?", 
        "英雄級冒險者", 
        "C級武器", 
        "C級防具", 
        "A級武器", 
        "A級防具", 
        "SS級武器", 
        "SS級防具", 
        "一拳不行就多一拳", 
        "等到天荒地老", 
        "對不起", 
        "犧牲小我", 
        "守護一切", 
        "再度轉生", 
        "迎難而上", 
        "史上最強豆腐", 
        "一拳超人", 
        "勇者", 
    ],
    'hidden_description': [
        "在一個關卡來使用\n回復魔法的次數達5次", 
        "在一個關卡來使用\n回復魔法的次數達15次", 
        "在一個關卡來使用\n回復魔法的次數達30次", 
        "在一個關卡中收集到\n3顆星星", 
        "收集到所有星星\n的一半", 
        "收集到所有星星", 
        "以無被攻擊過\n的狀態下\n通過其中一關卡", 
        "已剩餘一成血\n以下的狀態\n下通過其中一關卡", 
        "在輸入類關卡中\n輸入的字數超出\n框架範圍", 
        "連續挑戰同一關卡\n並獲勝5次", 
        "已完成全部有關\n五十音的關卡", 
        "已完成有關\n句子順序的關卡", 
        "已完成有關\n漢字的關卡", 
        "已完成有關\n動詞轉換的關卡", 
        "已獲得???", 
        "已獲得??????", 
        "已獲得???", 
        "已獲得???", 
        "已獲得????", 
        "已獲得????", 
        "只用??點擊\n殺死魔物", 
        "在其中一關卡內\n維持什麼都不做\n超過15分鐘", 
        "殺死??", 
        "已達成\n「????」\n結局", 
        "已達成\n「????」\n結局", 
        "開啟二周目", 
        "通關二周目", 
        "不穿任何裝備\n通關最終關卡", 
        "只用一擊擊敗魔物", 
        "已獲得所有成就", 
    ],
    'unlock_description': [
        "在一個關卡來使用\n回復魔法的次數達5次",        # recover_times done  0
        "在一個關卡來使用\n回復魔法的次數達15次",       # recover_times done
        "在一個關卡來使用\n回復魔法的次數達30次",       # recover_times done
        "在一個關卡中收集到\n3顆星星",                 # done
        "收集到所有星星\n的一半",                      # ready then done
        "收集到所有星星",                             # ready then done 5
        "以無被攻擊過\n的狀態下\n通過其中一關卡",       # damage_taken_times done
        "已剩餘一成血\n以下的狀態\n下通過其中一關卡",   # done
        "在輸入類關卡中\n輸入的字數超出\n框架範圍",     # done
        "連續挑戰同一關卡\n並獲勝5次",                  # done
        "已完成全部有關\n五十音的關卡",                 # done 10
        "已完成有關\n句子順序的關卡",                   # done
        "已完成有關\n漢字的關卡",                       # done
        "已完成有關\n動詞轉換的關卡",                   # done
        "已獲得名匠靈珠",                               # done 14
        "已獲得皇家守衛套裝",                           # done 15
        "已獲得天魔杖",                                 # done
        "已獲得天神甲",                                 # done
        "已獲得言靈天杖",                               # done
        "已獲得不滅龍鱗",                               # done 19
        "只用滑鼠點擊\n殺死魔物",                       # done 20
        "在其中一關卡內\n維持什麼都不做\n超過15分鐘",    # idle_times done
        "殺死莉子",                                     # done 22
        "已達成\n「犧牲小我」\n結局",                   # done
        "已達成\n「守護一切」\n結局",                   # done
        "開啟二周目",                                  # done
        "通關二周目",                                  # done 
        "不穿任何裝備\n通關最終關卡",                   #done 
        "只用一擊擊敗魔物", 
        "已獲得所有成就", 
    ],
}



time = 0                                
effect_time = 0                        
win_lose_effect_timer = 0    
changing = None

images = [
    pygame.transform.scale(pygame.image.load(path+"media/dungeon_crystal_1.png"), [WIDTH, HEIGHT]),                    # 0
    pygame.transform.scale(pygame.image.load(path+"media/title_text.png"), transform_scale([816, 144])),               # 1
    pygame.transform.scale(pygame.image.load(path+"media/press_to_start.png"), transform_scale([269, 36])),            # 2
    pygame.transform.scale(pygame.image.load(path+"media/forest_1.png"), [WIDTH, HEIGHT]),                             # 3
    pygame.transform.scale(pygame.image.load(path+"media/main_char.png"), transform_scale([640, 768])),                # 4
    pygame.transform.scale(pygame.image.load(path+"media/teacher_no_glasses.png"), transform_scale([517, 680])),       # 5
    pygame.transform.scale(pygame.image.load(path+"media/skip.png"), transform_scale([310, 80])),                      # 6
    pygame.transform.scale(pygame.image.load(path+"media/main_char_gray.png"), transform_scale([640, 768])),           # 7
    pygame.transform.scale(pygame.image.load(path+"media/teacher_no_glasses_gray.png"), transform_scale([517, 680])),  # 8
    pygame.transform.scale(pygame.image.load(path+"media/purple_slime_1.png"),transform_scale([532, 572])),            # 9
    pygame.transform.scale(pygame.image.load(path+"media/forest_river_sky.png"),transform_scale([1440, 1080])),        #10
    pygame.transform.scale(pygame.image.load(path+"media/stage_arrow.png"),transform_scale([75, 110])),                #11
    pygame.transform.scale(pygame.image.load(path+"media/stage1_title1.png"),transform_scale([200, 60])),              #12
    pygame.transform.scale(pygame.image.load(path+"media/star0.png"),transform_scale([360, 100])),                     #13
    pygame.transform.scale(pygame.image.load(path+"media/star1.png"),transform_scale([360, 100])),                     #14
    pygame.transform.scale(pygame.image.load(path+"media/star2.png"),transform_scale([360, 100])),                     #15
    pygame.transform.scale(pygame.image.load(path+"media/star3.png"),transform_scale([360, 100])),                     #16
    pygame.transform.scale(pygame.image.load(path+"media/stage_type_1_img_light.png"),transform_scale([847, 635])),    #17
    pygame.transform.scale(pygame.image.load(path+"media/stage_type_1_img_dark.png"),transform_scale([847, 635])),     #18
    pygame.transform.scale(pygame.image.load(path+"media/stage_type_2_img_dark.png"),transform_scale([847, 635])),     #19
    pygame.transform.scale(pygame.image.load(path+"media/stage_type_2_img_light.png"),transform_scale([847, 635])),    #20
    pygame.transform.scale(pygame.image.load(path+"media/stage2_title1.png"),transform_scale([185, 60])),              #21
    pygame.transform.scale(pygame.image.load(path+"media/continue.png"),transform_scale([520, 110])),                  #22
    pygame.transform.scale(pygame.image.load(path+"media/stage3_title1.png"), transform_scale([186, 60])),             #23
    pygame.transform.scale(pygame.image.load(path+"media/stage4_title1.png"), transform_scale([187, 60])),             #24
    pygame.transform.scale(pygame.image.load(path+"media/hell_bg.png"), [WIDTH, HEIGHT]),                              #25
    pygame.transform.scale(pygame.image.load(path+"media/hell_bg_dark.png"),transform_scale([847, 635])),              #26
    pygame.transform.scale(pygame.image.load(path+"media/hell_bg_light.png"),transform_scale([847, 635])),             #27
    pygame.transform.scale(pygame.image.load(path+"media/finalstage1_title.png"),transform_scale([299, 60])),          #28
    pygame.transform.scale(pygame.image.load(path+"media/demon_1.png"), transform_scale([685, 400])),                  #29
    pygame.transform.scale(pygame.image.load(path+"media/high_demon_1.png"), transform_scale([187, 60])),  # unused
    pygame.transform.scale(pygame.image.load(path+"media/world_map.png"), transform_scale([WIDTH, HEIGHT])),           #31
    pygame.transform.scale(pygame.image.load(path+"media/armor1.png"), transform_scale([60, 60])),                     #32
    pygame.transform.scale(pygame.image.load(path+"media/armor2.png"), transform_scale([60, 60])),                     #33
    pygame.transform.scale(pygame.image.load(path+"media/armor3.png"), transform_scale([60, 60])),                     #34
    pygame.transform.scale(pygame.image.load(path+"media/weapon1.png"), transform_scale([60, 60])),                    #35
    pygame.transform.scale(pygame.image.load(path+"media/weapon2.png"), transform_scale([60, 60])),                    #36
    pygame.transform.scale(pygame.image.load(path+"media/weapon3.png"), transform_scale([60, 60])),                    #37
    pygame.transform.scale(pygame.image.load(path+"media/sp_armor_weapon.png"), transform_scale([60, 60])),            #38
    pygame.transform.scale(pygame.image.load(path+"media/stage0_title.png"), transform_scale([220, 60])),              #39
    pygame.transform.scale(pygame.image.load(path+"media/stage1_title.png"), transform_scale([220, 60])),              #40
    pygame.transform.scale(pygame.image.load(path+"media/stage2_title.png"), transform_scale([220, 60])),              #41
    pygame.transform.scale(pygame.image.load(path+"media/stage3_title.png"), transform_scale([220, 60])),              #42
    pygame.transform.scale(pygame.image.load(path+"media/stage4_title.png"), transform_scale([220, 60])),              #43
    pygame.transform.scale(pygame.image.load(path+"media/stage5_title.png"), transform_scale([220, 60])),              #44
    pygame.transform.scale(pygame.image.load(path+"media/stage6_title.png"), transform_scale([220, 60])),              #45
    pygame.transform.scale(pygame.image.load(path+"media/stage7_title.png"), transform_scale([220, 60])),              #46
    pygame.transform.scale(pygame.image.load(path+"media/stage8_title.png"), transform_scale([220, 60])),              #47
    pygame.transform.scale(pygame.image.load(path+"media/stage9_title.png"), transform_scale([220, 60])),              #48
    pygame.transform.scale(pygame.image.load(path+"media/stage10_title.png"), transform_scale([220, 60])),             #49
    pygame.transform.scale(pygame.image.load(path+"media/stage11_title.png"), transform_scale([220, 60])),             #50
    pygame.transform.scale(pygame.image.load(path+"media/stage12_title.png"), transform_scale([220, 60])),             #51
    pygame.transform.scale(pygame.image.load(path+"media/stage13_title.png"), transform_scale([220, 60])),             #52
    pygame.transform.scale(pygame.image.load(path+"media/stage14_title.png"), transform_scale([220, 60])),             #53
    pygame.transform.scale(pygame.image.load(path+"media/stage15_title.png"), transform_scale([220, 60])),             #54
    pygame.transform.scale(pygame.image.load(path+"media/stage16_title.png"), transform_scale([220, 60])),             #55
    pygame.transform.scale(pygame.image.load(path+"media/stage17_title.png"), transform_scale([220, 60])),             #56
    pygame.transform.scale(pygame.image.load(path+"media/stage18_title.png"), transform_scale([220, 60])),             #57
    pygame.transform.scale(pygame.image.load(path+"media/stage19_title.png"), transform_scale([220, 60])),             #58
    pygame.transform.scale(pygame.image.load(path+"media/stage20_title.png"), transform_scale([400, 60])),             #59
    pygame.transform.scale(pygame.image.load(path+"media/stage21_title.png"), transform_scale([400, 60])),             #60
    pygame.transform.scale(pygame.image.load(path+"media/stage22_title.png"), transform_scale([400, 60])),             #61
    pygame.transform.scale(pygame.image.load(path+"media/stage23_title.png"), transform_scale([400, 60])),             #62
    pygame.transform.scale(pygame.image.load(path+"media/stage24_title.png"), transform_scale([220, 60])),             #63
    pygame.transform.scale(pygame.image.load(path+"media/stage25_title.png"), transform_scale([220, 60])),             #64
    pygame.transform.scale(pygame.image.load(path+"media/stage26_title.png"), transform_scale([220, 60])),             #65
    pygame.transform.scale(pygame.image.load(path+"media/stage27_title.png"), transform_scale([220, 60])),             #66
    pygame.transform.scale(pygame.image.load(path+"media/stage28_title.png"), transform_scale([220, 60])),             #67
    pygame.transform.scale(pygame.image.load(path+"media/stage29_title.png"), transform_scale([220, 60])),             #68
    pygame.transform.scale(pygame.image.load(path+"media/stage30_title.png"), transform_scale([220, 60])),             #69
    pygame.transform.scale(pygame.image.load(path+"media/stage31_title.png"), transform_scale([220, 60])),             #70
    pygame.transform.scale(pygame.image.load(path+"media/stage32_title.png"), transform_scale([220, 60])),             #71
    pygame.transform.scale(pygame.image.load(path+"media/stage33_title.png"), transform_scale([220, 60])),             #72
    pygame.transform.scale(pygame.image.load(path+"media/stage34_title.png"), transform_scale([220, 60])),             #73
    pygame.transform.scale(pygame.image.load(path+"media/stage35_title.png"), transform_scale([220, 60])),             #74
    pygame.transform.scale(pygame.image.load(path+"media/stage36_title.png"), transform_scale([220, 60])),             #75
    pygame.transform.scale(pygame.image.load(path+"media/stage37_title.png"), transform_scale([220, 60])),             #76
    pygame.transform.scale(pygame.image.load(path+"media/stage38_title.png"), transform_scale([220, 60])),             #77
    pygame.transform.scale(pygame.image.load(path+"media/goblin_king.png"), transform_scale([532, 572])),              #78
    pygame.transform.scale(pygame.image.load(path+"media/goblin_warrior.png"), transform_scale([532, 572])),           #79
    pygame.transform.scale(pygame.image.load(path+"media/tenma.png"), transform_scale([532, 572])),                    #80
    pygame.transform.scale(pygame.image.load(path+"media/dragon.png"), transform_scale([532, 572])),                   #81
    pygame.transform.scale(pygame.image.load(path+"media/demon_king.png"), transform_scale([532, 572])),               #82
    pygame.transform.scale(pygame.image.load(path+"media/demon_general1.png"), transform_scale([532, 572])),           #83
    pygame.transform.scale(pygame.image.load(path+"media/demon_general2.png"), transform_scale([532, 572])),           #84
    pygame.transform.scale(pygame.image.load(path+"media/demon_general3.png"), transform_scale([532, 572])),           #85
    pygame.transform.scale(pygame.image.load(path+"media/demon_general4.png"), transform_scale([532, 572])),           #86
    pygame.transform.scale(pygame.image.load(path+"media/forest_night.png"), transform_scale([1440, 1080])),           #87
    pygame.transform.scale(pygame.image.load(path+"media/forest_village.png"), transform_scale([1440, 1080])),         #88

]                                                              

# 基礎言靈魔法表示: <あ>
dialog = [
    #stage 0
    [
        (2, "？？？：\nおいおい！起[お]きろ！"),
        (1, "？？？：\n什麼？我在哪裡？那個女孩在說什麼？"),
        (2, "？？？：\n終於醒了。這裡是春日森林，我在旁邊路過就看到你\n躺在這裡。"),
        (2, "莉子：\n我叫莉子[りこ]，你還記得你的名字嗎？\n（幸好我在學校學過中文..."),
        (1, "赤真：\n我好像叫赤真。春日森林...是在日本嗎？"),
        (2, "莉子：\n日本？這裡是東瀛喔！\n我從未聽說過你所說的日本呢。（難道他失憶了？)"),
        (1, "赤真：\n欸欸欸？！難道我像漫畫中一樣穿越到異世界了嗎？？"),
        (2, "莉子：\n什麼是漫畫？異世界？"),
        (1, "赤真：\n沒什麼！（看來是真的了，\n我的宅男之夢終於成真了！！)"),
        (2, "莉子：\n。。。"),
        (1, "赤真：\n請問你知道冒險者、魔物、魔法嗎？（期待)"),
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
        (2, "莉子：\n嘩，真厲害！只教了你一次就發動成功了！\n本小姐教得真好！（嘿嘿！成功得到一個免費打手～)"),
        (2, "莉子：\n看那邊！那裡有隻史萊姆，立刻實戰一下吧！"),
        (1, "赤真：\n等...等一下！能再說多次那5個音嗎？"),
        (2, "莉子：\n真拿你沒辦法～ 聽好了哦！\n「あ」a、「い」i、「う」u、「え」e、「お」o"),
        (2, "莉子：\n準備好了嗎？"),
        (1, "赤真：\n準備好了！來吧！")
    ],
    #stage 1
    [
        (2, '莉子：\n不錯不錯！你成為一個合格的冒險者了！'),
        (1, '赤真：\n呼～（好險)'),
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
        (1, '赤真：\n好複雜...'),
        (2, '莉子：\n不過也不用一次過全部記得，我們慢慢來吧！'),
        (1, '赤真：\n謝謝你，莉子小姐。'),
        (2, '莉子：\n嘿嘿～呀！差點忘了！'),
        (1, '赤真：\n怎麼了？'),
        (2, '莉子：\n差點忘記教你言靈魔法的回復術。'),
        (2, '莉子：\n我先示範一次，之後你應該就能學會了。何況本小姐\n教得這麼好，對吧？'),
        (1, '赤真：\n點頭(滴汗...)'),
        (2.1, '莉子：\n<か>！'),
        (1, '赤真：\n身上的疼痛疲勞都消失了！'),
        (2, '莉子：\n正好，前面有另一隻史萊姆，用新學的10個音試試吧！'),
        (1, '赤真：\n好，來吧！')
    ],
    #stage 2
    [
        (2, '莉子：\n最近魔物出現的頻率很不正常，\n連低階區域都出現了高階怪！'),
        (1, '赤真：\n難怪工會發布了緊急調查任務...'),
        (2, '莉子：\n沒錯！而且工會還派了C級冒險者陪同我們一起去呢。'),
        (2, '莉子：\n在出發前，我們來學『さ』行跟它的濁音『ざ』行吧！\n「さ」sa、「し」shi、「す」su、「せ」se、「そ」so'),
        (2, '莉子：\n「ざ」za、「じ」ji、「ず」zu、「ぜ」ze、「ぞ」zo'),
        (1, '赤真：\n好！有C級前輩在，我們剛好可以安心練習新魔法！'),
        (2, '莉子：\n很好，那邊出現了幾隻魔物，拿它們練練手吧！')
    ],
    #stage 3
    [
        (1, '赤真：\n等一下... 前方那股令人窒息的壓迫感是什麼？'),
        (2, '莉子：\n糟了！那是森林深處的精英怪... 哥布林王！\n為什麼這種級別的魔物會出現在外圍？！'),
        (0, '系統：\n【警告】C級冒險者前輩被哥布林王\n一擊擊飛！生死未卜！'),
        (1, '赤真：\n不會吧... 連C級前輩都被瞬間秒殺了？！\n那我們還等什麼，快逃啊！'),
        (2, '莉子：\n來不及了，哥布林王發現我們了！\n小心，牠手下的哥布林戰士朝你衝過去了！'),
        (1, '赤真：\n哇啊啊！衝著我來了！我該怎麼辦？！'),
        (2, '莉子：\n快反擊！現在教你『た』行跟它的濁音『だ』行\n可以用來施展防禦打擊！'),
        (2, '莉子：\n「た」ta、「ち」chi、「つ」tsu、「て」te、「と」to\n '),
        (2, '莉子：\n「だ」da、「ぢ」ji、「づ」zu、「で」de、「ど」do'),
        (1, '赤真：\n哪有人刀都架在脖子上了還在教書的啦！\n不管了，拼了！！')
    ],
    #stage 4
    [
        (0, '系統：\n【警告】精英怪『哥布林王』已鎖定目標！'),
        (1, '赤真：\n呼... 呼... 終於解決掉那隻哥布林戰士了。\n等等，哥布林王親自舉起武器走過來了！'),
        (2, '莉子：\n我們絕對打不贏牠的！現在唯一的目標就是逃回城裡！\n快跟我撤退！'),
        (1, '赤真：\n那就快跑啊！可是牠的速度好快，馬上就要追上來了！'),
        (2, '莉子：\n牠為什麼只盯著我們？！快，用『な』行魔法牽制牠！\n「な」na、「に」ni、「ぬ」nu、「ね」ne、「の」no！'),
        (1, '赤真：\n這種時候就別上課了啊啊啊！快逃啊！！'),
        (2, '莉子：\n邊逃跑邊詠唱！還有『ま』行，能製造迷霧掩護我們！\n'),
        (2, '莉子：\n「ま」ma、「み」mi、「む」mu、「め」me、「も」mo！'),
        (1, '赤真：\n等等，「ぬ」跟「め」長得也太像了吧！\n妳是想害死我嗎？！'),
        (2, '莉子：\n別管那麼多了！大聲詠唱然後拼命跑！\n'),
        (2, '莉子：\n千萬別回頭！撤回城裡！'),
        (1, '赤真：\n啊啊啊啊！撤退！撤退！言靈魔法，發動！')
    ],
    #stage 5
    [
        (1, '赤真：\n呼... 呼... 終於逃回城了，好險。'),
        (2, '莉子：\n工會知道哥布林王出現後，已經準備全面進攻了！\n國王陛下甚至賜予了我們『皇家守衛套裝』！'),
        (1, '赤真：\n有了這套護甲裝備，我們的防禦力大增了！'),
        (2, '莉子：\n趁現在，快把『は』行、濁音\n『ば』和半濁音『ぱ』行學起來！'),
        (2, '莉子：\n「は」ha、「ひ」hi、「ふ」fu、「へ」he、「ほ」ho'),
        (2, '莉子：\n「ば」ba、「び」bi、「ぶ」bu、「べ」be、「ぼ」bo'),
        (2, '莉子：\n「ぱ」pa、「ぴ」pi、「ぷ」pu、「ぺ」pe、「ぽ」po'),
        (1, '赤真：\n我記住了！這次我們絕對不能再逃跑！')
    ],
    #stage 6
    [
        (2, '莉子：\n全面進攻馬上就要開始了！\n 我把剩下的基本音全部教給你！'),
        (2, '莉子：\n『や』行、『ら』行、『わ』、『を』和『ん』！'),
        (2, '莉子：\n「や」ya、「ゆ」yu、「よ」yo \n「ら」ra、「り」ri、「る」ru、「れ」re、「ろ」ro'),
        (2, '莉子：\n最後是「わ」wa、「を」wo、「ん」n！'),
        (1, '赤真：\n好！我已經把五十音全都學會了，魔力感覺源源不絕！'),
        (2, '莉子：\n準備出發，我們去討伐那隻哥布林王！')
    ],
    #stage 7
    [
        (0, '系統：\n【決戰】遭遇 哥布林王！'),
        (1, '赤真：\n又是你這隻怪物！這次我們可不會再退縮了！'),
        (2, '莉子：\n赤真，用你學會的五十音魔法，給牠們致命一擊！'),
        (1, '赤真：\n看我的！言靈魔法全開！！')
    ],
    #stage 8
    [
        (1, '赤真：\n我們贏了！終於打敗哥布林王了！'),
        (2, '莉子：\n太棒了！我們還用哥布林王的素材，\n請城內工匠打造了武器『名匠靈珠』！'),
        (1, '赤真：\n裝備大升級！有了它，接下來的冒險就更有把握了。'),
        (2, '莉子：\n為了發揮新武器的威力，我現在把最後的發音規則\n「拗音」教給你！'),
        (2, '莉子：\n「きゃ」kya、「きゅ」kyu、「きょ」kyo\n「しゃ」sha、「しゅ」shu、「しょ」sho\n「ちゃ」cha、「ちゅ」chu、「ちょ」cho\n「にゃ」nya、「にゅ」nyu、「にょ」nyo\n「ひゃ」hya、「ひゅ」hyu、「ひょ」hyo\n「みゃ」mya、「みゅ」myu、「みょ」myo\n「りゃ」rya、「りゅ」ryu、「りょ」ryo！'),
        (1, '赤真：\n原來是把字拼在一起發音啊！\n我準備好迎接第二章的挑戰了！')
    ],
    #stage 9
    [
        (2, '莉子：\n工會發現哥布林王只是魔族派來的探子，\n經過一段冷靜期，魔族開始派更強大的魔物試探了。'),
        (2, '莉子：\n從今天開始，我們要學習漢字（Kanji），\n這是更高階的魔法！'),
        (1, '赤真：\n莉子，你臉色不太好，沒事吧？'),
        (2, '莉子：\n不知道為什麼，我的記憶中開始出現\n精靈族言靈魔法的傳承...\n (但我明明是人類啊...)'),
    ],
    #stage 10
    [
        (2, '莉子：\n嗚... 頭好痛！'),
        (1, '赤真：\n莉子！你怎麼了？！'),
        (2, '莉子：\n我體內的血脈好像發生了衝突，\n施展新覺醒的魔法就會劇痛...'),
        (1, '赤真：\n既然如此，你別勉強了！\n接下來的漢字魔法全部交給我來施展！')
    ],
    #stage 11
    [
         (2, '莉子：\n謝謝你，赤真。我們繼續練習漢字的讀音辨識吧。'),
        (1, '赤真：\n你好好休息，看我把這些魔物全部清掉！')
    ],
    #stage 12
    [
        (1, '赤真：\n魔族的入侵越來越頻繁了，這樣下去不是辦法。'),
        (2, '莉子：\n嗯，我的傳承記憶也越來越清晰... \n我隱約對自己的身分產生懷疑了。'),
        (1, '赤真：\n等這波魔物清理完，我們分開調查一下吧，或許能找到線索。')
    ],
    #stage 13
    [
        (1, '赤真：\n漢字的數量真多，但我能感覺到法術的威力正在倍增。'),
        (2, '莉子：\n加油，只要把這些字詞深深印在腦海裡，\n詠唱速度就會變快！')
    ],
    #stage 14
    [
        (1, '赤真：\n這附近的瘴氣越來越重了。'),
        (2, '莉子：\n大家都要小心，魔族的前鋒部隊隨時會出現。')
     ],
    #stage 15
    [
        (1, '赤真：\n漢字魔法不僅能攻擊，還能用來防禦和干擾，\n真是博大精深。'),
        (2, '莉子：\n沒錯，所以你要完全掌握它們！')
    ],
    #stage 16
    [
         (2, '莉子：\n赤真，你有沒有覺得地面的震動越來越明顯了？'),
        (1, '赤真：\n看來有什麼大傢伙要來了，\n我先用漢字魔法把周圍的小怪清空！')
    ],
    #stage 17
    [
        (1, '赤真：\n呼... 終於清得差不多了。'), #add more dialogue here
        (2, '莉子：\n別鬆懈！真正的考驗才剛要開始。')
    ],
    #stage 18
    [
        (1, '赤真：\n莉子，小心！前面那個傢伙的氣息跟之前的魔物完全不同！'),
        (2, '莉子：\n那是中級Boss... 我們必須全力以赴！')
    ],
    #stage 19
    [
        (0, '系統：\n【警告】中級Boss『天魔』降臨！攻擊力極高！'),
        (1, '赤真：\n可惡！天魔的血量明明已經見底了，怎麼還不倒下！\n（天魔 HP 下限被鎖定在 1）'),
        (2, '莉子：\n赤真，退後！讓我來！\n啊啊啊啊——（忍痛詠唱最強咒文）『天神之力』！'),
        (3, '高空出現一個巨大的魔法陣，一道強光彈出，/n'),
        (2, '瞬間擊殺了天魔。\n莉子召喚出護甲『天神甲』，天魔掉落武器『天魔杖』。'),
        (2, '莉子：\n赤真，傳承記憶讓我明白了我的身世... \n我的血脈能衍生出另一個作用。'),
        (2, '莉子：\n我可以成為別人的武器，但代價是...失去生命。'),
        (1, '赤真：\n開什麼玩笑！我絕對不允許這種事發生！！')
     ],
    #stage 20
    [
        (1, '赤真：\n（我必須變得更強，強到不需要莉子犧牲！）'),
        (2, '莉子：\n赤真... 接下來我們要學習基礎的句子結構\n（Sentence Structure）。\n把單字拖曳到正確的位置組成完整的句子。'),
        (1, '赤真：\n交給我吧，不管多複雜的文法我都能學會！')
    ],
    #stage 21
    [
        (2, '莉子：\n注意東瀛語的助詞「は」、「を」、「に」的用法喔！'),
        (1, '赤真：\n主詞、受詞和動詞的順序跟中文不一樣，但我已經抓到訣竅了。')
    ],
    #stage 22
    [
        (1, '赤真：\n有了完整的句子，言靈魔法的範圍和精準度都提升了！'),
        (2, '莉子：\n這就是語言的力量，繼續保持這個氣勢！')
    ],
    #stage 23
    [
        (2, '莉子：\n這是最後一組基礎句型訓練了，把它們完美組合起來吧！'),
        (1, '赤真：\n沒問題，這些魔物根本撐不住我的一句完整詠唱！')
    ],
    #stage 24
    [
        (2, '莉子：\n句子結構掌握後，最核心的就是動詞變化（Verb form）了！\n先從『ます形』變換成『辞書形』開始吧！'),
        (1, '赤真：\n動詞變化？聽起來能讓魔法產生不同的型態變化！')
    ],
    #stage 25
    [
        (2, '莉子：\n接下來是『て形』和『た形』，這在連續施法時非常重要！'),
        (1, '赤真：\n變化規則有點多，但我會在實戰中記住它們的！')
    ],
    #stage 26
    [
        (2, '莉子：\n別忘了『ない形』，這是否定型態，能用來消除敵人的增益狀態！'),
        (1, '赤真：\n這招實用！看我把它們的護盾全部消除！')
    ],
    #stage 27
    [
        (2, '莉子：\n你已經學會了所有的動詞變化，你現在是一名非常出色的言靈使了！'),
        (1, '赤真：\n這都多虧了你的教導，莉子。我們一定能一起活著終結這場戰爭。')
    ],
    #stage 28
    [
        (3, '天空突然一暗，四周空氣瞬間凝結，一頭毀天滅地的魔龍出現。'),
        (1, '赤真：\n好可怕的壓迫感... 這絕不是我們能抗衡的等級！牠發現我們了！'),
        (2, '莉子：\n赤真！在生死存亡之際，你必須作出抉擇！\n殺了我！你就能得到『混血靈心』，往後的攻擊力會翻倍！'),
        (1, '赤真：\n我說過，我絕對不會犧牲你！！'),
        (2, '莉子：\n不這樣做，我們都會被魔龍殺死！求求你，動手吧！'),
        (3, '系統：\n【命運的分歧點】\n接下來的戰鬥表現/選擇將決定莉子的生死，並導向完全不同的結局。')
    ],
     #stage 29
    [
        (1, '赤真：\n......莉子。'),
        (3, '為了生存，赤真被迫殺死了莉子，獲得了『混血靈心』。\n他強勢討伐了魔龍，獨自一人殺入魔族領地。'),
        (0, '東方大將：\n愚蠢的人類，竟敢單槍匹馬闖入這裡！'),
        (1, '赤真：\n...擋路者，死。力量源源不絕湧上來，但心裡卻空無一物。')
    ],
    #stage 30
    [
        (0, '南方大將：\n東方大將居然敗給了你這滿身煞氣的小子！'),
        (1, '赤真：\n太弱了。下一個。')
    ],
    #stage 31
    [
        (0, '西方大將：\n你的魔法充滿了絕望與悲憤，你到底經歷了什麼？'),
        (1, '赤真：\n閉嘴！言靈·滅！')
    ],
    #stage 32
    [
        (0, '北方大將：\n魔王大人就在前方，我絕不會讓你過去！'),
        (1, '赤真：\n連同這個世界，一起毀滅吧。')    ],
    #stage 33
    [
        (0, '魔王：\n沒想到你能走到這裡。你的眼神...比我們魔族還要冰冷。'),
        (1, '赤真：\n...廢話少說，去死吧。'),
        (3, '一番苦戰後，赤真將魔王擊敗。但他獨自一人，無人可分享勝利的喜悅。'),
        (1, '赤真：\n回想殺死莉子的那一刻... 我真是悔不當初。'),
        (3, '【結局：忘我】\n主角憎恨這個殘酷的世界，最終取代了王座成為新的魔王，\n在萬年後被新出現的勇者討伐而死。')
    ], 
    #stage 34 (choice B)
    [
        (1, '赤真：\n哈啊... 哈啊... 我們做到了！沒有犧牲你，我們也打倒魔龍了！'),
        (2, '莉子：\n太好了！而且我們還獲得了極品素材『不滅龍鱗』！'),
        (3, '此時，一名老者急速趕來，他正是因為發明言靈魔法而被天神抹除存在的\n傳說中的『言靈大法師』。'),
        (0, '言靈大法師：\n你寧死不屈守護同伴的行為打動了我。通過我的考驗，\n這把專屬武器『言靈天杖』就傳授給你！'),
        (1, '赤真：\n好強大的力量！莉子，我們殺入魔族領地，去擊敗東方大將吧！')
    ],
    #stage 35
    [
        (0, '南方大將：\n東方大將居然敗了！你們這對人類與精靈的組合不簡單！'),
        (2, '莉子：\n赤真，用我們新學會的動詞變化配合言靈天杖的威力！'),
        (1, '赤真：\n看我的！')
    ],
    #stage 36
    [
        (0, '西方大將：\n別太得意忘形了，人類！'),
        (1, '赤真：\n只要有莉子在我身邊，我的言靈就不會迷惘！')
    ],
    #stage 37
    [
        (0, '北方大將：\n魔王大人的王座就在前方，我會誓死守衛！'),
        (2, '莉子：\n赤真，這是最後的將領了，突破他！')
    ],
    #stage 38
    [
        (0, '魔王：\n勇者啊，你們以為憑藉那點力量就能阻止我嗎？'),
        (1, '赤真：\n我們一路走來，克服了無數難關，絕不是為了屈服於你！'),
        (2, '莉子：\n赤真，我們一起上！用你最強的言靈魔法！'),
        (1, '赤真：\n為了守護莉子，守護這個世界！接招吧，魔王！！'),
        (3, '【結局：勇者】\n赤真擊殺魔王凱旋而歸，成為世間傳頌的勇者。\n其後與女主角莉子共度餘生，直至二人壽終正寢。')
    ]

]


# 0: both gray; 1: left talking; 2: right talking; 3: both talking
story_num = 0
stage = 0
dialog_num = 0

#sound effect
SFX_FILES = {
    "click": "media/sfx_click.wav",
    "attack": "media/sfx_attack.wav",       # When player attacks
    "heal": "media/sfx_heal.wav",           # When player uses recover
    "damage": "media/sfx_hurt.wav",       # When enemy attacks player
    "error": "media/sfx_error.wav",         # Wrong answer buzzer
    "win": "media/sfx_win.wav",             # Stage clear
    "lose": "media/sfx_lose.wav"            # Player dies
}
# 2. Dictionary to hold the loaded sound objects
loaded_sfx = {}

# 3. Pre-load all sound effects safely
for name, filename in SFX_FILES.items():
    try:
        filepath = path + filename
        if os.path.exists(filepath):
            loaded_sfx[name] = pygame.mixer.Sound(filepath)
        else:
            loaded_sfx[name] = None
            print(f"Warning: SFX missing -> {filepath}")
    except Exception as e:
        loaded_sfx[name] = None
        print(f"Error loading {name} sound: {e}")

# 4. The main function to play a sound effect
def play_sfx(name):
    sound = loaded_sfx.get(name)
    if sound:
        # Get volume from options (0 to 100), convert to Pygame format (0.0 to 1.0)
        volume = save.get('sound', 100) / 100.0
        sound.set_volume(volume)
        sound.play()
def play_bgm(filename):
    try:
        filepath = path + "media/" + filename
        if os.path.exists(filepath):
            pygame.mixer.music.load(filepath)
            volume = save.get('music', 100) / 100.0
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1) # -1 means loop forever
        else:
            print(f"Warning: BGM missing -> {filepath}")
    except Exception as e:
        print(f"Error playing BGM: {e}")

# 6. Function to instantly update BGM volume when dragging the option slider
def update_bgm_volume():
    volume = save.get('music', 100) / 100.0
    pygame.mixer.music.set_volume(volume)

#this part is for drag type
draggable_rects = []
draggable_rects_initial_pos = []
dragged_item_index = -1
is_dragging = False
drag_offset_x = 0
drag_offset_y = 0
drop_target_rect = pygame.Rect(0,0,0,0) # Initialize with a dummy rect
parts = []
hover_insertion_index = -1
block_offsets = {}

scale = [2, 80, 4, 50, 8, 20, 10, 1, 100] # player_hp -= round(battle_detail[stage]["enemy_attack"] * scale[save["equipt"][1]]/10) | enemy_hp -= 20*scale[save["equipt"][0]]

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
        "enemy_hp": 100 * (1.5 if save['hard'] else 1),
        "enemy_attack": 20 * (1.5 if save['hard'] else 1),
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
        "enemy_hp": 200 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "以滑, 鼠點擊正確的選項",
    },
    # 2
    {
        "question_type": "MC",
        "question":["さ","し","す","せ","そ", "ざ","じ","ず","ぜ","ぞ"],
        "answer": {
            "さ": ("sa", ["sa", "za", "chi", "ki"]),
            "し": ("shi", ["shi", "ji", "chi", "tsu"]),
            "す": ("su", ["su", "zu", "tsu", "ku"]),
            "せ": ("se",["se", "ze", "te", "ne"]),
            "そ": ("so",["so", "zo", "to", "ko"]),
            "ざ": ("za",["za", "sa", "da", "ga"]),
            "じ": ("ji", ["ji", "shi", "gi", "zi"]),
            "ず": ("zu", ["zu", "su", "dzu", "gu"]),
            "ぜ": ("ze", ["ze", "se", "de", "ge"]),
            "ぞ": ("zo", ["zo", "so", "do", "go"])
        },
        "word_size": 64,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "や" ,
        "target": [10, 14],
        "enemy_hp": 200 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 3
    {
        "question_type": "MC",
        "question":["た","ち","つ","て","と", "だ","ぢ","づ","で","ど"],
        "answer": {
            "た": ("ta",["ta", "da", "ka", "na"]),
            "ち": ("chi", ["chi", "shi", "ti", "ji"]),
            "つ": ("tsu", ["tsu", "su", "tu", "du"]),
            "て": ("te", ["te", "de", "se", "he"]),
            "と": ("to", ["to", "do", "ko", "so"]),
            "だ": ("da",["da", "ta", "ba", "ga"]),
            "ぢ": ("di",["di", "ji", "chi", "zi"]),
            "づ": ("du",["du", "zu", "tsu", "dzu"]),
            "で": ("de", ["de", "te", "ge", "be"]),
            "ど": ("do", ["do", "to", "go", "bo"])
        },
        "word_size": 64,
        "order":[],
        "enemy_surf": 79,
        "enemy_attack_word": "爪", 
        "target":[10, 14],
        "enemy_hp": 220 * (1.5 if save['hard'] else 1),
        "enemy_attack": 40 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 4
    {
        "question_type": "MC",
        "question":["な","に","ぬ","ね","の", "ま","み","む","め","も"],
        "answer": {
            "な": ("na",["na", "ma", "ta", "ha"]),
            "に": ("ni",["ni", "mi", "ri", "chi"]),
            "ぬ": ("nu", ["nu", "mu", "me", "ne"]),  # Tests visual similarity with me/ne
            "ね": ("ne",["ne", "re", "wa", "nu"]),  # Tests visual similarity with re/wa
            "の": ("no",["no", "mo", "so", "ro"]),
            "ま": ("ma",["ma", "na", "ha", "ho"]),  # Tests visual similarity with ha/ho
            "み": ("mi",["mi", "ni", "ri", "hi"]),
            "む": ("mu",["mu", "su", "nu", "fu"]),  # Tests visual similarity with su
            "め": ("me",["me", "nu", "ne", "no"]),  # Tests visual similarity with nu/ne
            "も": ("mo",["mo", "ma", "to", "yo"])
        },
        "word_size": 64,
        "order":[],
        "enemy_surf": 78, 
        "enemy_attack_word": "吼", 
        "target":[10, 14],
        "enemy_hp": 240 * (1.5 if save['hard'] else 1),
        "enemy_attack": 50 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 5
    {
        "question_type": "MC",
        "question":["は","ひ","ふ","へ","ほ", "ば","び","ぶ","べ","ぼ", "ぱ","ぴ","ぷ","ぺ","ぽ"],
        "answer": {
            "は": ("ha",["ha", "ba", "pa", "ho"]), # Tests visual similarity with ho
            "ひ": ("hi", ["hi", "bi", "pi", "ni"]),
            "ふ": ("fu",["fu", "bu", "pu", "nu"]),
            "へ": ("he",["he", "be", "pe", "te"]),
            "ほ": ("ho",["ho", "bo", "po", "ha"]), # Tests visual similarity with ha
            "ば": ("ba",["ba", "ha", "pa", "da"]),
            "び": ("bi", ["bi", "hi", "pi", "ji"]),
            "ぶ": ("bu", ["bu", "fu", "pu", "zu"]),
            "べ": ("be", ["be", "he", "pe", "de"]),
            "ぼ": ("bo",["bo", "ho", "po", "do"]),
            "ぱ": ("pa",["pa", "ha", "ba", "ya"]),
            "ぴ": ("pi",["pi", "hi", "bi", "ri"]),
            "ぷ": ("pu", ["pu", "fu", "bu", "mu"]),
            "ぺ": ("pe", ["pe", "he", "be", "re"]),
            "ぽ": ("po", ["po", "ho", "bo", "so"])
        },
        "word_size": 64,
        "order":[],
        "enemy_surf": 9, 
        "enemy_attack_word": "擊",
        "target": [15, 18],
        "enemy_hp": 260 * (1.5 if save['hard'] else 1),
        "enemy_attack": 60 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 6
    {
        "question_type": "MC",
        "question":["や","ゆ","よ", "ら","り","る","れ","ろ", "わ","を","ん"],
        "answer": {
            "や": ("ya", ["ya", "ka", "yo", "wa"]),
            "ゆ": ("yu", ["yu", "yo", "nu", "me"]),
            "よ": ("よ",["yo", "ma", "ha", "ro"]),
            "ら": ("ra",["ra", "chi", "u", "ro"]),  # Tests similarity with chi (ち) and u (う)
            "り": ("ri", ["ri", "i", "ni", "re"]),   # Tests similarity with i (い)
            "る": ("ru", ["ru", "ro", "su", "tsu"]), # Tests similarity with ro (ろ)
            "れ": ("re", ["re", "ne", "wa", "nu"]),  # Tests similarity with ne (ね) and wa (わ)
            "ろ": ("ro",["ro", "ru", "so", "tsu"]), # Tests similarity with ru (る)
            "わ": ("wa", ["wa", "re", "ne", "wo"]),  # Tests similarity with re (れ) and ne (ね)
            "を": ("wo",["wo", "o", "wa", "n"]),    # Tests phonetic similarity with o (お)
            "ん": ("n",["n", "m", "h", "so"])
        },
        "word_size": 64,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "突", 
        "target": [11, 15], # Adjusted for 11 questions
        "enemy_hp": 280 * (1.5 if save['hard'] else 1),
        "enemy_attack": 70 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 7
    {
        "question_type": "MC",
        "question":[
            "あ","い","う","え","お", "か","き","く","け","こ", "が","ぎ","ぐ","げ","ご",
            "さ","し","す","せ","そ", "ざ","じ","ず","ぜ","ぞ", "た","ち","つ","て","と",
            "だ","ぢ","づ","で","ど", "な","に","ぬ","ね","の", "ま","み","む","め","も",
            "は","ひ","ふ","へ","ほ", "ば","び","ぶ","べ","ぼ", "ぱ","ぴ","ぷ","ぺ","ぽ",
            "や","ゆ","よ", "ら","り","る","れ","ろ", "わ","を","ん"
        ],
        "answer": {
            "あ": ("a",["a", "i", "u", "e"]),
            "い": ("i",["i", "u", "e", "o"]),
            "う": ("u",["u", "e", "o", "a"]),
            "え": ("e", ["e", "o", "a", "i"]),
            "お": ("o", ["o", "a", "i", "u"]),
            "か": ("ka", ["ka", "ga", "ha", "wa"]),
            "き": ("ki",["ki", "sa", "chi", "gi"]),
            "く": ("ku",["ka", "ga", "ku", "su"]),
            "け": ("ke",["ke", "ka", "ki", "gi"]),
            "こ": ("ko", ["ko", "go", "wo", "ka"]),
            "が": ("ga", ["ga", "ka", "na", "ra"]),
            "ぎ": ("gi", ["gi", "ki", "shi", "bi"]),
            "ぐ": ("gu",["gu", "ku", "su", "bu"]),
            "げ": ("ge",["ge", "ke", "ko", "go"]),
            "ご": ("go",["go", "ko", "so", "ga"]),
            "さ": ("sa", ["sa", "za", "chi", "ki"]),
            "し": ("shi", ["shi", "ji", "chi", "tsu"]),
            "す": ("su", ["su", "zu", "tsu", "ku"]),
            "せ": ("se",["se", "ze", "te", "ne"]),
            "そ": ("so",["so", "zo", "to", "ko"]),
            "ざ": ("za",["za", "sa", "da", "ga"]),
            "じ": ("ji", ["ji", "shi", "gi", "zi"]),
            "ず": ("zu", ["zu", "su", "dzu", "gu"]),
            "ぜ": ("ze", ["ze", "se", "de", "ge"]),
            "ぞ": ("zo", ["zo", "so", "do", "go"]),
            "た": ("ta",["ta", "da", "ka", "na"]),
            "ち": ("chi",["chi", "shi", "ti", "ji"]),
            "つ": ("tsu",["tsu", "su", "tu", "du"]),
            "て": ("te", ["te", "de", "se", "he"]),
            "と": ("to", ["to", "do", "ko", "so"]),
            "だ": ("da", ["da", "ta", "ba", "ga"]),
            "ぢ": ("di",["di", "ji", "chi", "zi"]),
            "づ": ("du",["du", "zu", "tsu", "dzu"]),
            "で": ("de",["de", "te", "ge", "be"]),
            "ど": ("do", ["do", "to", "go", "bo"]),
            "な": ("na", ["na", "ma", "ta", "ha"]),
            "に": ("ni", ["ni", "mi", "ri", "chi"]),
            "ぬ": ("nu", ["nu", "mu", "me", "ne"]),
            "ね": ("ne",["ne", "re", "wa", "nu"]),
            "の": ("no",["no", "mo", "so", "ro"]),
            "ま": ("ma", ["ma", "na", "ha", "ho"]),
            "み": ("mi", ["mi", "ni", "ri", "hi"]),
            "む": ("mu", ["mu", "su", "nu", "fu"]),
            "め": ("me", ["me", "nu", "ne", "no"]),
            "も": ("mo",["mo", "ma", "to", "yo"]),
            "は": ("ha",["ha", "ba", "pa", "ho"]),
            "ひ": ("hi", ["hi", "bi", "pi", "ni"]),
            "ふ": ("fu", ["fu", "bu", "pu", "nu"]),
            "へ": ("he", ["he", "be", "pe", "te"]),
            "ほ": ("ho", ["ho", "bo", "po", "ha"]),
            "ば": ("ba",["ba", "ha", "pa", "da"]),
            "び": ("bi",["bi", "hi", "pi", "ji"]),
            "ぶ": ("bu", ["bu", "fu", "pu", "zu"]),
            "べ": ("be", ["be", "he", "pe", "de"]),
            "ぼ": ("bo", ["bo", "ho", "po", "do"]),
            "ぱ": ("pa", ["pa", "ha", "ba", "ya"]),
            "ぴ": ("pi",["pi", "hi", "bi", "ri"]),
            "ぷ": ("pu",["pu", "fu", "bu", "mu"]),
            "ぺ": ("pe", ["pe", "he", "be", "re"]),
            "ぽ": ("po", ["po", "ho", "bo", "so"]),
            "や": ("ya", ["ya", "ka", "yo", "wa"]),
            "ゆ": ("yu", ["yu", "yo", "nu", "me"]),
            "よ": ("yo",["yo", "ma", "ha", "ro"]),
            "ら": ("ra",["ra", "chi", "u", "ro"]),
            "り": ("ri", ["ri", "i", "ni", "re"]),
            "る": ("ru", ["ru", "ro", "su", "tsu"]),
            "れ": ("re", ["re", "ne", "wa", "nu"]),
            "ろ": ("ro", ["ro", "ru", "so", "tsu"]),
            "わ": ("wa",["wa", "re", "ne", "wo"]),
            "を": ("wo",["wo", "o", "wa", "n"]),
            "ん": ("n",["n", "m", "h", "so"])
        },
        "word_size": 64,
        "order":[],
        "enemy_surf": 78, 
        "enemy_attack_word": "滅", 
        "target": [20, 25], 
        "enemy_hp": 400 * (1.5 if save['hard'] else 1),
        "enemy_attack": 80 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 8
    {
        "question_type": "MC",
        "question":[
            "きゃ","きゅ","きょ", "しゃ","しゅ","しょ", "ちゃ","ちゅ","ちょ", 
            "にゃ","にゅ","にょ", "ひゃ","ひゅ","ひょ", "みゃ","みゅ","みょ", "りゃ","りゅ","りょ"
        ],
        "answer": {
            "きゃ": ("kya", ["kya", "kiya", "kuyo", "gya"]),
            "きゅ": ("kyu", ["kyu", "kiyu", "kya", "gyu"]),
            "きょ": ("kyo", ["kyo", "kiyo", "kyu", "gyo"]),
            "しゃ": ("sha", ["sha", "shiya", "shu", "ja"]),
            "しゅ": ("shu", ["shu", "shiyu", "sho", "ju"]),
            "しょ": ("sho", ["sho", "shiyo", "sha", "jo"]),
            "ちゃ": ("cha",["cha", "chiya", "chu", "sha"]),
            "ちゅ": ("chu",["chu", "chiyu", "cho", "shu"]),
            "ちょ": ("cho",["cho", "chiyo", "cha", "sho"]),
            "にゃ": ("nya",["nya", "niya", "nyu", "mya"]),
            "にゅ": ("nyu",["nyu", "niyu", "nyo", "myu"]),
            "にょ": ("nyo",["nyo", "niyo", "nya", "myo"]),
            "ひゃ": ("hya",["hya", "hiya", "hyu", "pya"]),
            "ひゅ": ("hyu",["hyu", "hiyu", "hyo", "pyu"]),
            "ひょ": ("hyo",["hyo", "hiyo", "hya", "pyo"]),
            "みゃ": ("mya",["mya", "miya", "myu", "nya"]),
            "みゅ": ("myu",["myu", "miyu", "myo", "nyu"]),
            "みょ": ("myo", ["myo", "miyo", "mya", "nyo"]),
            "りゃ": ("rya", ["rya", "riya", "ryu", "mya"]),
            "りゅ": ("ryu", ["ryu", "riyu", "ryo", "myu"]),
            "りょ": ("ryo", ["ryo", "riyo", "rya", "myo"])
        },
        "word_size": 64,
        "order":[],
        "enemy_surf": 78,
        "enemy_attack_word": "咬", 
        "target":[12, 16],
        "enemy_hp": 240 * (1.5 if save['hard'] else 1),
        "enemy_attack": 50 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 9 (Kanji - Numbers)
    {
        "question_type": "MC",
        "question":[
            "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "百", "千", "万", "億", "兆", "零",
            "いち", "に", "さん", "よん", "ご", "ろく", "なな", "はち", "きゅう", "じゅう", "ひゃく", "せん", "まん", "おく", "ちょう", "れい"
        ],
        "answer": {
            "一": ("いち", ["いち", "に", "さん", "し"]),
            "二": ("に", ["に", "いち", "さん", "よん"]),
            "三": ("さん", ["さん", "に", "し", "ご"]),
            "四": ("よん", ["よん", "さん", "ご", "ろく"]),
            "五": ("ご", ["ご", "よん", "ろく", "なな"]),
            "六": ("ろく",["ろく", "ご", "なな", "はち"]),
            "七": ("なな",["なな", "ろく", "はち", "きゅう"]),
            "八": ("はち", ["はち", "なな", "きゅう", "じゅう"]),
            "九": ("きゅう", ["きゅう", "はち", "じゅう", "いち"]),
            "十": ("じゅう", ["じゅう", "きゅう", "いち", "に"]),
            "百": ("ひゃく", ["ひゃく", "せん", "まん", "れい"]),
            "千": ("せん", ["せん", "ひゃく", "まん", "ちょう"]),
            "万": ("まん", ["まん", "せん", "ひゃく", "おく"]),
            "億": ("おく", ["おく", "まん", "ちょう", "せん"]),
            "兆": ("ちょう", ["ちょう", "おく", "まん", "ひゃく"]),
            "零": ("れい/ぜろ", ["れい/ぜろ", "いち", "ひゃく", "さん"]),
            "いち": ("一", ["一", "二", "三", "四"]),
            "に": ("二", ["二", "一", "三", "四"]),
            "さん": ("三", ["三", "二", "四", "五"]),
            "よん": ("四", ["四", "三", "五", "六"]),
            "ご": ("五", ["五", "四", "六", "七"]),
            "ろく": ("六", ["六", "五", "七", "八"]),
            "なな": ("七", ["七", "六", "八", "九"]),
            "はち": ("八", ["八", "七", "九", "十"]),
            "きゅう": ("九", ["九", "八", "十", "一"]),
            "じゅう": ("十", ["十", "九", "一", "二"]),
            "ひゃく": ("百", ["百", "千", "万", "零"]),
            "せん": ("千", ["千", "百", "万", "兆"]),
            "まん": ("万", ["万", "千", "百", "億"]),
            "おく": ("億", ["億", "万", "兆", "千"]),
            "ちょう": ("兆", ["兆", "億", "万", "百"]),
            "れい/ぜろ": ("零", ["零", "一", "百", "万"])
        },
        "word_size": 48,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "算",
        "target": [10, 12],
        "enemy_hp": 200 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊漢字正確的平假名讀音",
    },
    # 10 (Kanji - Elements)
    {
        "question_type": "MC",
        "question":[
            "日", "月", "火", "水", "木", "金", "土", "光", "闇", "風", "雷", "氷", "星", "雲", "雪",
            "ひ/にち", "つき", "ひ/か", "みず", "き", "きん", "つち", "ひかり", "やみ", "かぜ", "かみなり", "こおり", "ほし", "くも", "ゆき"
        ],
        "answer": {
            "日": ("ひ/にち",["ひ/にち", "つき", "みず", "き"]),
            "月": ("つき",["つき", "ひ/にち", "つち", "きん"]),
            "火": ("ひ/か",["ひ/か", "みず", "つち", "き"]),
            "水": ("みず",["みず", "つき", "つち", "ひ/か"]),
            "木": ("き",["き", "きん", "ひ/にち", "みず"]),
            "金": ("きん",["きん", "ぎん", "き", "つち"]),
            "土": ("つち",["つち", "みず", "つき", "ひ/にち"]),
            "光": ("ひかり", ["ひかり", "やみ", "かぜ", "ほし"]),
            "闇": ("やみ", ["やみ", "ひかり", "かげ", "ゆき"]),
            "風": ("かぜ", ["かぜ", "くも", "あめ", "ゆき"]),
            "雷": ("かみなり", ["かみなり", "あめ", "ゆき", "かぜ"]),
            "氷": ("こおり", ["こおり", "みず", "ゆき", "ほし"]),
            "星": ("ほし", ["ほし", "つき", "ひかり", "くも"]),
            "雲": ("くも", ["くも", "あめ", "かぜ", "ゆき"]),
            "雪": ("ゆき", ["ゆき", "こおり", "あめ", "くも"]),
            "ひ/にち": ("日", ["日", "月", "水", "木"]),
            "つき": ("月", ["月", "日", "土", "金"]),
            "ひ/か": ("火", ["火", "水", "土", "木"]),
            "みず": ("水", ["水", "月", "土", "火"]),
            "き": ("木", ["木", "金", "日", "水"]),
            "きん": ("金", ["金", "銀", "木", "土"]),
            "つち": ("土", ["土", "水", "月", "日"]),
            "ひかり": ("光", ["光", "闇", "風", "星"]),
            "やみ": ("闇", ["闇", "光", "影", "雪"]),
            "かぜ": ("風", ["風", "雲", "雨", "雪"]),
            "かみなり": ("雷", ["雷", "雨", "雪", "風"]),
            "こおり": ("氷", ["氷", "水", "雪", "星"]),
            "ほし": ("星", ["星", "月", "光", "雲"]),
            "くも": ("雲", ["雲", "雨", "風", "雪"]),
            "ゆき": ("雪", ["雪", "氷", "雨", "雲"])
        },
        "word_size": 40,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "素",
        "target": [6, 7],
        "enemy_hp": 140 * (1.5 if save['hard'] else 1),
        "enemy_attack": 20 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊漢字正確的平假名讀音",
    },
    # 11 (kanji - Animals & Objects)
    {
        "question_type": "Drag",
        "questions": [
            { "sentence": "猫_", "answer": "ねこ", "options": ["ねこ", "いぬ", "とり", "さかな"] },
            { "sentence": "犬_", "answer": "いぬ", "options": ["いぬ", "ねこ", "うさぎ", "へび"] },
            { "sentence": "本_", "answer": "ほん", "options": ["ほん", "えんぴつ", "かばん", "とけい"] },
            { "sentence": "車_", "answer": "くるま", "options": ["くるま", "でんしゃ", "ふね", "ひこうき"] },
            { "sentence": "鳥_", "answer": "とり", "options": ["とり", "さかな", "ねこ", "いぬ"] },
            { "sentence": "魚_", "answer": "さかな", "options": ["さかな", "とり", "うさぎ", "へび"] },
            { "sentence": "鉛筆_", "answer": "えんぴつ", "options": ["えんぴつ", "ほん", "かさ", "くつ"] },
            { "sentence": "鞄_", "answer": "かばん", "options": ["かばん", "とけい", "ほん", "えんぴつ"] },
            { "sentence": "時計_", "answer": "とけい", "options": ["とけい", "かばん", "かさ", "くつ"] },
            { "sentence": "肉_", "answer": "にく", "options": ["にく", "さかな", "やさい", "ごはん"] },
            { "sentence": "傘_", "answer": "かさ", "options": ["かさ", "くつ", "かばん", "とけい"] },
            { "sentence": "靴_", "answer": "くつ", "options": ["くつ", "かさ", "ほん", "えんぴつ"] },
            { "sentence": "桜_", "answer": "さくら", "options": ["さくら", "はな", "き", "はし"] },
            { "sentence": "橋_", "answer": "はし", "options": ["はし", "みち", "さくら", "き"] },
            { "sentence": "薬_", "answer": "くすり", "options": ["くすり", "みず", "おちゃ", "にく"] },
            { "sentence": "ねこ_", "answer": "猫", "options": ["猫", "犬", "鳥", "魚"] },
            { "sentence": "いぬ_", "answer": "犬", "options": ["犬", "猫", "兎", "蛇"] },
            { "sentence": "ほん_", "answer": "本", "options": ["本", "鉛筆", "鞄", "時計"] },
            { "sentence": "くるま_", "answer": "車", "options": ["車", "電車", "船", "飛行機"] },
            { "sentence": "とり_", "answer": "鳥", "options": ["鳥", "魚", "猫", "犬"] },
            { "sentence": "さかな_", "answer": "魚", "options": ["魚", "鳥", "兎", "蛇"] },
            { "sentence": "えんぴつ_", "answer": "鉛筆", "options": ["鉛筆", "本", "傘", "靴"] },
            { "sentence": "かばん_", "answer": "鞄", "options": ["鞄", "時計", "本", "鉛筆"] },
            { "sentence": "とけい_", "answer": "時計", "options": ["時計", "鞄", "傘", "靴"] },
            { "sentence": "にく_", "answer": "肉", "options": ["肉", "魚", "野菜", "ご飯"] },
            { "sentence": "かさ_", "answer": "傘", "options": ["傘", "靴", "鞄", "時計"] },
            { "sentence": "くつ_", "answer": "靴", "options": ["靴", "傘", "本", "鉛筆"] },
            { "sentence": "さくら_", "answer": "桜", "options": ["桜", "花", "木", "橋"] },
            { "sentence": "はし_", "answer": "橋", "options": ["橋", "道", "桜", "木"] },
            { "sentence": "くすり_", "answer": "薬", "options": ["薬", "水", "お茶", "肉"] }
        ],
        "order": [],
        "enemy_surf": 9,
        "enemy_attack_word": "物",
        "target": [7, 9],
        "enemy_hp": 140 * (1.5 if save['hard'] else 1),
        "enemy_attack": 20 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠拖拉正確的選項至空格內",
    },
    # 12 (kanji - Nature)
    {
        "question_type": "MC",
        "question":[
            "山", "川", "空", "天", "雨", "石", "花", "森", "海", "陸", "谷", "草", "葉", "根", "泥",
            "やま", "かわ", "そら", "てん", "あめ", "いし", "はな", "もり", "うみ", "りく", "たに", "くさ", "は", "ね", "どろ"
        ],
        "answer": {
            "山": ("やま", ["やま", "かわ", "そら", "てん"]),
            "川": ("かわ", ["かわ", "やま", "うみ", "あめ"]),
            "空": ("そら", ["そら", "てん", "あめ", "いし"]),
            "天": ("てん", ["てん", "そら", "やま", "もり"]),
            "雨": ("あめ", ["あめ", "かわ", "はな", "そら"]),
            "石": ("いし", ["いし", "やま", "はな", "もり"]),
            "花": ("はな", ["はな", "あめ", "そら", "いし"]),
            "森": ("もり", ["もり", "やま", "かわ", "てん"]),
            "海": ("うみ", ["うみ", "かわ", "やま", "みず"]),
            "陸": ("りく", ["りく", "うみ", "そら", "もり"]),
            "谷": ("たに", ["たに", "やま", "かわ", "もり"]),
            "草": ("くさ", ["くさ", "はな", "き", "は"]),
            "葉": ("は", ["は", "き", "くさ", "はな"]),
            "根": ("ね", ["ね", "は", "き", "くさ"]),
            "泥": ("どろ", ["どろ", "いし", "つち", "すな"]),
            "やま": ("山", ["山", "川", "空", "天"]),
            "かわ": ("川", ["川", "山", "海", "雨"]),
            "そら": ("空", ["空", "天", "雨", "石"]),
            "てん": ("天", ["天", "空", "山", "森"]),
            "あめ": ("雨", ["雨", "川", "花", "空"]),
            "いし": ("石", ["石", "山", "花", "森"]),
            "はな": ("花", ["花", "雨", "空", "石"]),
            "もり": ("森", ["森", "山", "川", "天"]),
            "うみ": ("海", ["海", "川", "山", "水"]),
            "りく": ("陸", ["陸", "海", "空", "森"]),
            "たに": ("谷", ["谷", "山", "川", "森"]),
            "くさ": ("草", ["草", "花", "木", "葉"]),
            "は": ("葉", ["葉", "木", "草", "花"]),
            "ね": ("根", ["根", "葉", "木", "草"]),
            "どろ": ("泥", ["泥", "石", "土", "砂"])
        },
        "word_size": 48,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "震",
        "target": [9, 12],
        "enemy_hp": 180 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊漢字正確的平假名讀音",
    },
    # 13 (kanji - Directions)
    {
        "question_type": "Drag",
        "questions":[
            { "sentence": "上_", "answer": "うえ", "options": ["うえ", "した", "ひだり", "みぎ"] },
            { "sentence": "下_", "answer": "した", "options": ["した", "うえ", "まえ", "うしろ"] },
            { "sentence": "左_", "answer": "ひだり", "options":["ひだり", "みぎ", "なか", "そと"] },
            { "sentence": "右_", "answer": "みぎ", "options": ["みぎ", "ひだり", "まえ", "なか"] },
            { "sentence": "中_", "answer": "なか", "options": ["なか", "そと", "うえ", "した"] },
            { "sentence": "外_", "answer": "そと", "options":["そと", "なか", "ひだり", "みぎ"] },
            { "sentence": "前_", "answer": "まえ", "options":["まえ", "うしろ", "うえ", "そと"] },
            { "sentence": "後_", "answer": "うしろ", "options": ["うしろ", "まえ", "した", "なか"] },
            { "sentence": "隣_", "answer": "となり", "options": ["となり", "ちかく", "とおく", "なか"] },
            { "sentence": "近く_", "answer": "ちかく", "options": ["ちかく", "となり", "とおく", "そと"] },
            { "sentence": "遠く_", "answer": "とおく", "options": ["とおく", "ちかく", "となり", "まえ"] },
            { "sentence": "北_", "answer": "きた", "options": ["きた", "みなみ", "ひがし", "にし"] },
            { "sentence": "南_", "answer": "みなみ", "options": ["みなみ", "きた", "ひがし", "にし"] },
            { "sentence": "東_", "answer": "ひがし", "options": ["ひがし", "にし", "みなみ", "きた"] },
            { "sentence": "西_", "answer": "にし", "options": ["にし", "ひがし", "きた", "みなみ"] },
            { "sentence": "うえ_", "answer": "上", "options": ["上", "下", "左", "右"] },
            { "sentence": "した_", "answer": "下", "options": ["下", "上", "前", "後"] },
            { "sentence": "ひだり_", "answer": "左", "options":["左", "右", "中", "外"] },
            { "sentence": "みぎ_", "answer": "右", "options": ["右", "左", "前", "中"] },
            { "sentence": "なか_", "answer": "中", "options": ["中", "外", "上", "下"] },
            { "sentence": "そと_", "answer": "外", "options":["外", "中", "左", "右"] },
            { "sentence": "まえ_", "answer": "前", "options":["前", "後", "上", "外"] },
            { "sentence": "うしろ_", "answer": "後", "options": ["後", "前", "下", "中"] },
            { "sentence": "となり_", "answer": "隣", "options": ["隣", "近く", "遠く", "中"] },
            { "sentence": "ちかく_", "answer": "近く", "options": ["近く", "隣", "遠く", "外"] },
            { "sentence": "とおく_", "answer": "遠く", "options": ["遠く", "近く", "隣", "前"] },
            { "sentence": "きた_", "answer": "北", "options": ["北", "南", "東", "西"] },
            { "sentence": "みなみ_", "answer": "南", "options": ["南", "北", "東", "西"] },
            { "sentence": "ひがし_", "answer": "東", "options": ["東", "西", "南", "北"] },
            { "sentence": "にし_", "answer": "西", "options": ["西", "東", "北", "南"] }
        ],
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "轉",
        "target": [9, 12],
        "enemy_hp": 180 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "將正確的方向漢字拖拉至對應的中文意思旁",
    },
    # 14 (MC - Body & People)
    {
        "question_type": "MC",
         "question":[
            "人", "目", "口", "耳", "手", "足", "体", "男", "女", "頭", "髪", "鼻", "歯", "指", "首", "肩",
            "ひと", "め", "くち", "みみ", "て", "あし", "からだ", "おとこ", "おんな", "あたま", "かみ", "はな", "は", "ゆび", "くび", "かた"
        ],
        "answer": {
            "人": ("ひと", ["ひと", "おとこ", "おんな", "め"]),
            "目": ("め", ["め", "みみ", "くち", "て"]),
            "口": ("くち", ["くち", "め", "みみ", "あし"]),
            "耳": ("みみ", ["みみ", "め", "くち", "からだ"]),
            "手": ("て", ["て", "あし", "め", "ひと"]),
            "足": ("あし", ["あし", "て", "みみ", "おとこ"]),
            "体": ("からだ", ["からだ", "ひと", "おんな", "くち"]),
            "男": ("おとこ", ["おとこ", "おんな", "ひと", "からだ"]),
            "女": ("おんな", ["おんな", "おとこ", "ひと", "て"]),
            "頭": ("あたま", ["あたま", "かみ", "かた", "くび"]),
            "髪": ("かみ", ["かみ", "あたま", "みみ", "め"]),
            "鼻": ("はな", ["はな", "くち", "め", "みみ"]),
            "歯": ("は", ["は", "くち", "はな", "あたま"]),
            "指": ("ゆび", ["ゆび", "て", "あし", "かた"]),
            "首": ("くび", ["くび", "かた", "あたま", "ゆび"]),
            "肩": ("かた", ["かた", "くび", "て", "あし"]),
            "ひと": ("人", ["人", "男", "女", "目"]),
            "め": ("目", ["目", "耳", "口", "手"]),
            "くち": ("口", ["口", "目", "耳", "足"]),
            "みみ": ("耳", ["耳", "目", "口", "体"]),
            "て": ("手", ["手", "足", "目", "人"]),
            "あし": ("足", ["足", "手", "耳", "男"]),
            "からだ": ("体", ["体", "人", "女", "口"]),
            "おとこ": ("男", ["男", "女", "人", "体"]),
            "おんな": ("女", ["女", "男", "人", "手"]),
            "あたま": ("頭", ["頭", "髪", "肩", "首"]),
            "かみ": ("髪", ["髪", "頭", "耳", "目"]),
            "はな": ("鼻", ["鼻", "口", "目", "耳"]),
            "は": ("歯", ["歯", "口", "鼻", "頭"]),
            "ゆび": ("指", ["指", "手", "足", "肩"]),
            "くび": ("首", ["首", "肩", "頭", "指"]),
            "かた": ("肩", ["肩", "首", "手", "足"])
        },
        "word_size": 48,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "抓",
        "target": [10, 13],
        "enemy_hp": 200 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊漢字正確的平假名讀音",
    },
    # 15 (Drag - Time & Periods)
    {
        "question_type": "Drag",
         "questions":[
            { "sentence": "今_", "answer": "いま", "options": ["いま", "じ", "ふん", "はん"] },
            { "sentence": "時_", "answer": "じ", "options":["じ", "いま", "ねん", "あさ"] },
            { "sentence": "分_", "answer": "ふん", "options":["ふん", "はん", "じ", "ひる"] },
            { "sentence": "半_", "answer": "はん", "options": ["はん", "ふん", "いま", "よる"] },
            { "sentence": "年_", "answer": "ねん", "options":["ねん", "じ", "はん", "あさ"] },
            { "sentence": "朝_", "answer": "あさ", "options":["あさ", "ひる", "よる", "いま"] },
            { "sentence": "昼_", "answer": "ひる", "options": ["ひる", "あさ", "よる", "じ"] },
            { "sentence": "夜_", "answer": "よる", "options": ["よる", "ひる", "あさ", "ねん"] },
            { "sentence": "今日_", "answer": "きょう", "options": ["きょう", "あした", "きのう", "まいにち"] },
            { "sentence": "明日_", "answer": "あした", "options": ["あした", "きのう", "きょう", "しゅう"] },
            { "sentence": "昨日_", "answer": "きのう", "options": ["きのう", "あした", "きょう", "しゅう"] },
            { "sentence": "毎日_", "answer": "まいにち", "options": ["まいにち", "きょう", "あした", "きのう"] },
            { "sentence": "週_", "answer": "しゅう", "options": ["しゅう", "ねん", "げつ", "にち"] },
            { "sentence": "夕方_", "answer": "ゆうがた", "options": ["ゆうがた", "あさ", "ひる", "よる"] },
            { "sentence": "季節_", "answer": "きせつ", "options": ["きせつ", "ねん", "しゅう", "ゆうがた"] },
            { "sentence": "いま_", "answer": "今", "options": ["今", "時", "分", "半"] },
            { "sentence": "じ_", "answer": "時", "options":["時", "今", "年", "朝"] },
            { "sentence": "ふん_", "answer": "分", "options":["分", "半", "時", "昼"] },
            { "sentence": "はん_", "answer": "半", "options": ["半", "分", "今", "夜"] },
            { "sentence": "ねん_", "answer": "年", "options":["年", "時", "半", "朝"] },
            { "sentence": "あさ_", "answer": "朝", "options":["朝", "昼", "夜", "今"] },
            { "sentence": "ひる_", "answer": "昼", "options": ["昼", "朝", "夜", "時"] },
            { "sentence": "よる_", "answer": "夜", "options": ["夜", "昼", "朝", "年"] },
            { "sentence": "きょう_", "answer": "今日", "options": ["今日", "明日", "昨日", "毎日"] },
            { "sentence": "あした_", "answer": "明日", "options": ["明日", "昨日", "今日", "週"] },
            { "sentence": "きのう_", "answer": "昨日", "options": ["昨日", "明日", "今日", "週"] },
            { "sentence": "まいにち_", "answer": "毎日", "options": ["毎日", "今日", "明日", "昨日"] },
            { "sentence": "しゅう_", "answer": "週", "options": ["週", "年", "月", "日"] },
            { "sentence": "ゆうがた_", "answer": "夕方", "options": ["夕方", "朝", "昼", "夜"] },
            { "sentence": "きせつ_", "answer": "季節", "options": ["季節", "年", "週", "夕方"] }
        ],
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "遲",
        "target": [10, 13],
        "enemy_hp": 200 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "將正確的時間漢字拖拉至對應的中文意思旁",
    },
    # 16 (MC - Adjectives)
    {
        "question_type": "MC",
        "question":[
            "大きい", "小さい", "高い", "低い", "新しい", "古い", "多い", "少ない", "暑い", "寒い", "熱い", "冷たい", "良い", "悪い", "長い", "短い",
            "おおきい", "ちいさい", "たかい", "ひくい", "あたらしい", "ふるい", "おおい", "すくない", "あつい(氣候)", "さむい", "あつい(溫度)", "つめたい", "よい", "わるい", "ながい", "みじかい"
        ],
        "answer": {
            "大きい": ("おおきい",["おおきい", "ちいさい", "たかい", "ひくい"]),
            "小さい": ("ちいさい", ["ちいさい", "おおきい", "あたらしい", "ふるい"]),
            "高い": ("たかい", ["たかい", "ひくい", "おおきい", "おおい"]),
            "低い": ("ひくい", ["ひくい", "たかい", "ちいさい", "すくない"]),
            "新しい": ("あたらしい", ["あたらしい", "ふるい", "おおきい", "おおい"]),
            "古い": ("ふるい",["ふるい", "あたらしい", "ちいさい", "ひくい"]),
            "多い": ("おおい",["おおい", "すくない", "たかい", "あたらしい"]),
            "少ない": ("すくない",["すくない", "おおい", "ひくい", "ふるい"]),
            "暑い": ("あつい", ["あつい", "さむい", "あたたかい", "すずしい"]),
            "寒い": ("さむい", ["さむい", "あつい", "つめたい", "ながい"]),
            "熱い": ("あつい", ["あつい", "つめたい", "さむい", "わるい"]),
            "冷たい": ("つめたい", ["つめたい", "あつい", "さむい", "よい"]),
            "良い": ("よい", ["よい", "わるい", "ながい", "みじかい"]),
            "悪い": ("わるい", ["わるい", "よい", "たかい", "ひくい"]),
            "長い": ("ながい", ["ながい", "みじかい", "おおきい", "ちいさい"]),
            "短い": ("みじかい", ["みじかい", "ながい", "おおい", "すくない"]),
            "おおきい": ("大きい",["大きい", "小さい", "高い", "低い"]),
            "ちいさい": ("小さい", ["小さい", "大きい", "新しい", "古い"]),
            "たかい": ("高い", ["高い", "低い", "大きい", "多い"]),
            "ひくい": ("低い", ["低い", "高い", "小さい", "少ない"]),
            "あたらしい": ("新しい", ["新しい", "古い", "大きい", "多い"]),
            "ふるい": ("古い",["古い", "新しい", "小さい", "低い"]),
            "おおい": ("多い",["多い", "少ない", "高い", "新しい"]),
            "すくない": ("少ない",["少ない", "多い", "低い", "古い"]),
            "あつい(氣候)": ("暑い", ["暑い", "寒い", "温かい", "涼しい"]),
            "さむい": ("寒い", ["寒い", "暑い", "冷たい", "長い"]),
            "あつい(溫度)": ("熱い", ["熱い", "冷たい", "寒い", "悪い"]),
            "つめたい": ("冷たい", ["冷たい", "熱い", "寒い", "良い"]),
            "よい": ("良い", ["良い", "悪い", "長い", "短い"]),
            "わるい": ("悪い", ["悪い", "良い", "高い", "低い"]),
            "ながい": ("長い", ["長い", "短い", "大きい", "小さい"]),
            "みじかい": ("短い", ["短い", "長い", "多い", "少ない"])
        },
        "word_size": 40,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "幻",
        "target": [11, 14],
        "enemy_hp": 220 * (1.5 if save['hard'] else 1),
        "enemy_attack": 40 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊形容詞正確的平假名讀音",
    },
    # 17 (kanji to hiragana 1 )
    {
        "question_type": "MC",
        "question": [
            "行きます", "来ます", "帰ります", "出掛けます", "食べます", "飲みます", "見ます", "読みます", "書きます", "聞きます", "買います", "起きます", "寝ます", "走ります", "泳ぎます",
            "いきます", "きます", "かえります", "でかけます", "たべます", "のみます", "みます", "よみます", "かきます", "ききます", "かいます", "おきます", "ねます", "はしります", "およぎます"
        ],
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
            "聞きます": ("ききます", ["ききます", "みにます", "こくます", "きます"]),
            "買います": ("かいます", ["かいます", "かきます", "ききます", "します"]),
            "起きます": ("おきます", ["おきます", "ねます", "みます", "いきます"]),
            "寝ます": ("ねます", ["ねます", "おきます", "のみます", "でます"]),
            "走ります": ("はしります", ["はしります", "あるきます", "かえります", "とまります"]),
            "泳ぎます": ("およぎます", ["およぎます", "やすみます", "あそびます", "よみます"]),
            "いきます": ("行きます", ["行きます", "来ます", "見ます", "聞きます"]),
            "きます": ("来ます", ["来ます", "行きます", "居ます", "着ます"]),
            "かえります": ("帰ります", ["帰ります", "代わります", "戻ります", "出掛ります"]),
            "でかけます": ("出掛けます", ["出掛けます", "手掛けます", "出負けます", "怪我けます"]),
            "たべます": ("食べます", ["食べます", "喋ります", "並べます", "比べます"]),
            "のみます": ("飲みます", ["飲みます", "乗みます", "読みます", "包みます"]),
            "みます": ("見ます", ["見ます", "魅ます", "建ます", "店ます"]),
            "よみます": ("読みます", ["読みます", "呼びます", "飲みます", "休みます"]),
            "かきます": ("書きます", ["書きます", "描きます", "欠きます", "買います"]),
            "ききます": ("聞きます", ["聞きます", "効きます", "来きます", "着きます"]),
            "かいます": ("買います", ["買います", "飼います", "書きます", "会います"]),
            "おきます": ("起きます", ["起きます", "置きます", "寝ます", "行きます"]),
            "ねます": ("寝ます", ["寝ます", "起きます", "飲みます", "出ます"]),
            "はしります": ("走ります", ["走ります", "歩きます", "帰ります", "止まります"]),
            "およぎます": ("泳ぎます", ["泳ぎます", "休みます", "遊びます", "読みます"])
        },
        "word_size": 36,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "む" ,
        "target": [5, 7],
        "enemy_hp": 100 * (1.5 if save['hard'] else 1),
        "enemy_attack": 20 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 18 (kanji - Days of the week)
    {
        "question_type": "Drag",
       "questions":[
            { "sentence": "月曜日_", "answer": "げつようび", "options":["げつようび", "かようび", "すいようび", "にちようび"] },
            { "sentence": "火曜日_", "answer": "かようび", "options":["かようび", "もくようび", "きんようび", "どようび"] },
            { "sentence": "水曜日_", "answer": "すいようび", "options":["すいようび", "かようび", "もくようび", "げつようび"] },
            { "sentence": "木曜日_", "answer": "もくようび", "options": ["もくようび", "すいようび", "きんようび", "どようび"] },
            { "sentence": "金曜日_", "answer": "きんようび", "options":["きんようび", "げつようび", "かようび", "にちようび"] },
            { "sentence": "土曜日_", "answer": "どようび", "options": ["どようび", "にちようび", "すいようび", "もくようび"] },
            { "sentence": "日曜日_", "answer": "にちようび", "options":["にちようび", "げつようび", "きんようび", "どようび"] },
            { "sentence": "週末_", "answer": "しゅうまつ", "options":["しゅうまつ", "へいじつ", "しゅくじつ", "らいしゅう"] },
            { "sentence": "祝日_", "answer": "しゅくじつ", "options":["しゅくじつ", "しゅうまつ", "へいじつ", "きょねん"] },
            { "sentence": "平日_", "answer": "へいじつ", "options":["へいじつ", "しゅうまつ", "しゅくじつ", "らいしゅう"] },
            { "sentence": "先週_", "answer": "せんしゅう", "options":["せんしゅう", "こんしゅう", "らいしゅう", "きょねん"] },
            { "sentence": "今週_", "answer": "こんしゅう", "options":["こんしゅう", "せんしゅう", "らいしゅう", "らいねん"] },
            { "sentence": "来週_", "answer": "らいしゅう", "options":["らいしゅう", "こんしゅう", "せんしゅう", "らいねん"] },
            { "sentence": "去年_", "answer": "きょねん", "options":["きょねん", "らいねん", "せんしゅう", "しゅうまつ"] },
            { "sentence": "来年_", "answer": "らいねん", "options":["らいねん", "きょねん", "らいしゅう", "へいじつ"] },
            { "sentence": "げつようび_", "answer": "月曜日", "options":["月曜日", "火曜日", "水曜日", "日曜日"] },
            { "sentence": "かようび_", "answer": "火曜日", "options":["火曜日", "木曜日", "金曜日", "土曜日"] },
            { "sentence": "すいようび_", "answer": "水曜日", "options":["水曜日", "火曜日", "木曜日", "月曜日"] },
            { "sentence": "もくようび_", "answer": "木曜日", "options": ["木曜日", "水曜日", "金曜日", "土曜日"] },
            { "sentence": "きんようび_", "answer": "金曜日", "options":["金曜日", "月曜日", "火曜日", "日曜日"] },
            { "sentence": "どようび_", "answer": "土曜日", "options": ["土曜日", "日曜日", "水曜日", "木曜日"] },
            { "sentence": "にちようび_", "answer": "日曜日", "options":["日曜日", "月曜日", "金曜日", "土曜日"] },
            { "sentence": "しゅうまつ_", "answer": "週末", "options":["週末", "平日", "祝日", "来週"] },
            { "sentence": "しゅくじつ_", "answer": "祝日", "options":["祝日", "週末", "平日", "去年"] },
            { "sentence": "へいじつ_", "answer": "平日", "options":["平日", "週末", "祝日", "来週"] },
            { "sentence": "せんしゅう_", "answer": "先週", "options":["先週", "今週", "来週", "去年"] },
            { "sentence": "こんしゅう_", "answer": "今週", "options":["今週", "先週", "来週", "来年"] },
            { "sentence": "らいしゅう_", "answer": "来週", "options":["来週", "今週", "先週", "来年"] },
            { "sentence": "きょねん_", "answer": "去年", "options":["去年", "来年", "先週", "週末"] },
            { "sentence": "らいねん_", "answer": "来年", "options":["来年", "去年", "来週", "平日"] }
        ],
        "order":[],
        "enemy_surf": 29, 
        "enemy_attack_word": "壓",
        "target":[6, 7],
        "enemy_hp": 140 * (1.5 if save['hard'] else 1),
        "enemy_attack": 20 * (1.5 if save['hard'] else 1),
        "discription": "將正確的星期拖拉至對應的中文意思旁",
    },
    # 19 (MC - Mid Boss "Tenma" - Grand Kanji Exam)
    {
        "question_type": "MC",
        "question":[
            "百", "千", "水", "木", "山", "空", "前", "人", "目", "時", 
            "大きい", "新しい", "行く", "読む", "話す", "月曜日", "日曜日",
            "ひゃく", "せん", "みず", "き", "やま", "そら", "まえ", "ひと", "め", "とき/じ",
            "おおきい", "あたらしい", "いく", "よむ", "はなす", "げつようび", "にちようび"
        ],
        "answer": {
            # Kanji -> Hiragana
            "百": ("ひゃく", ["ひゃく", "せん", "まん", "ひやく"]),
            "千": ("せん", ["せん", "ひゃく", "まん", "ぜん"]),
            "水": ("みず", ["みず", "つき", "つち", "ひ/か"]),
            "木": ("き", ["き", "きん", "ひ/にち", "みず"]),
            "山": ("やま", ["やま", "かわ", "そら", "てん"]),
            "空": ("そら", ["そら", "てん", "あめ", "いし"]),
            "前": ("まえ", ["まえ", "うしろ", "うえ", "なか"]),
            "人": ("ひと",["ひと", "おとこ", "おんな", "め"]),
            "目": ("め",["め", "みみ", "くち", "て"]),
            "時": ("とき/じ",["とき/じ", "いま", "ねん", "あさ"]),
            "大きい": ("おおきい", ["おおきい", "ちいさい", "たかい", "ひくい"]),
            "新しい": ("あたらしい", ["あたらしい", "ふるい", "おおきい", "おおい"]),
            "行く": ("いく", ["いく", "くる", "みる", "きく"]),
            "読む": ("よむ", ["よむ", "かく", "いう", "はなす"]),
            "話す": ("はなす", ["はなす", "いう", "よむ", "やすむ"]),
            "月曜日": ("げつようび",["げつようび", "かようび", "すいようび", "にちようび"]),
            "日曜日": ("にちようび",["にちようび", "げつようび", "きんようび", "どようび"]),

            # Hiragana -> Kanji
            "ひゃく": ("百", ["百", "千", "万", "白"]),
            "せん": ("千", ["千", "百", "万", "前"]),
            "みず": ("水", ["水", "木", "月", "火"]),
            "き": ("木", ["木", "金", "日", "水"]),
            "やま": ("山", ["山", "川", "空", "天"]),
            "そら": ("空", ["空", "天", "雨", "石"]),
            "まえ": ("前", ["前", "後", "上", "中"]),
            "ひと": ("人", ["人", "男", "女", "目"]),
            "め": ("目", ["目", "耳", "口", "手"]),
            "とき/じ": ("時", ["時", "今", "年", "朝"]),
            "おおきい": ("大きい", ["大きい", "小さい", "高い", "低い"]),
            "あたらしい": ("新しい", ["新しい", "古い", "大きい", "多い"]),
            "いく": ("行く", ["行く", "来る", "見る", "聞く"]),
            "よむ": ("読む", ["読む", "書く", "言う", "話す"]),
            "はなす": ("話す", ["話す", "言う", "読む", "休む"]),
            "げつようび": ("月曜日", ["月曜日", "火曜日", "水曜日", "日曜日"]),
            "にちようび": ("日曜日", ["日曜日", "月曜日", "金曜日", "土曜日"])
        },
        "word_size": 36,
        "order":[],
        "enemy_surf": 80,  # Mid Boss (Tenma)
        "enemy_attack_word": "死",
        "target": [20, 25],
        "enemy_hp": 400 * (1.5 if save['hard'] else 1),   # Requires 20 hits to defeat!
        "enemy_attack": 50 * (1.5 if save['hard'] else 1),
        "discription": "中級Boss『天魔』降臨！點擊漢字正確的讀音！",
    },
    # 20 (Sentence Order - Basic A is B)
    {
        "question_type": "Sentence_Order",
        "questions":[
            { 
                "meaning": "我是赤真 (I am Akamasa)", 
                "answer_order": ["わたし", "は", "あかまさ", "です"], 
                "options": ["です", "わたし", "は", "あかまさ", "が", "を"] 
            },
            { 
                "meaning": "這是蘋果 (This is an apple)", 
                "answer_order": ["これ", "は", "りんご", "です"], 
                "options":["りんご", "これ", "は", "です", "それ", "に"] 
            },
            { 
                "meaning": "莉子是精靈 (Riko is an elf)", 
                "answer_order": ["りこ", "は", "エルフ", "です"], 
                "options": ["りこ", "エルフ", "は", "です", "を", "の"] 
            },
            { 
                "meaning": "那是一本書 (That is a book)", 
                "answer_order": ["それ", "は", "ほん", "です"], 
                "options":["ほん", "それ", "は", "です", "あれ", "が"] 
            },
            { 
                "meaning": "明天是星期一 (Tomorrow is Monday)", 
                "answer_order":["あした", "は", "げつようび", "です"], 
                "options":["あした", "は", "げつようび", "です", "きょう", "に"] 
            },
            { 
                "meaning": "我是學生 (I am a student)", 
                "answer_order": ["わたし", "は", "がくせい", "です"], 
                "options": ["わたし", "は", "がくせい", "です", "が", "を"] 
            },
            { 
                "meaning": "那個人是老師 (That person is a teacher)", 
                "answer_order": ["あのひと", "は", "せんせい", "です"], 
                "options": ["あのひと", "は", "せんせい", "です", "この", "に"] 
            },
            { 
                "meaning": "這裡是學校 (Here is a school)", 
                "answer_order": ["ここ", "は", "がっこう", "です"], 
                "options": ["ここ", "は", "がっこう", "です", "そこ", "へ"] 
            },
            { 
                "meaning": "今天是星期天 (Today is Sunday)", 
                "answer_order": ["きょう", "は", "にちようび", "です"], 
                "options": ["きょう", "は", "にちようび", "です", "あした", "が"] 
            },
            { 
                "meaning": "這是水 (This is water)", 
                "answer_order": ["これ", "は", "みず", "です"], 
                "options": ["これ", "は", "みず", "です", "それ", "を"] 
            },
            { 
                "meaning": "那是狗 (That is a dog)", 
                "answer_order": ["それ", "は", "いぬ", "です"], 
                "options": ["それ", "は", "いぬ", "です", "あれ", "ねこ"] 
            },
            { 
                "meaning": "這是我的書 (This is my book)", 
                "answer_order": ["これ", "は", "わたし", "の", "ほん", "です"], 
                "options": ["これ", "は", "わたし", "の", "ほん", "です", "が", "を"] 
            },
            { 
                "meaning": "莉子是女孩子 (Riko is a girl)", 
                "answer_order": ["りこ", "は", "おんなのこ", "です"], 
                "options": ["りこ", "は", "おんなのこ", "です", "おとこのこ", "に"] 
            },
            { 
                "meaning": "赤真是男人 (Akamasa is a man)", 
                "answer_order": ["あかまさ", "は", "おとこ", "です"], 
                "options": ["あかまさ", "は", "おとこ", "です", "おんな", "を"] 
            },
            { 
                "meaning": "那個是山 (That over there is a mountain)", 
                "answer_order": ["あれ", "は", "やま", "です"], 
                "options": ["あれ", "は", "やま", "です", "これ", "かわ"] 
            },
            { 
                "meaning": "這裡是森林 (Here is a forest)", 
                "answer_order": ["ここ", "は", "もり", "です"], 
                "options": ["ここ", "は", "もり", "です", "そこ", "に"] 
            }
        ],
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "基",
        "target": [5, 6],
        "enemy_hp": 100 * (1.5 if save['hard'] else 1), # 5 hits to defeat
        "enemy_attack": 20 * (1.5 if save['hard'] else 1),
        "discription": "將單字拖入上方橫線組成正確句子，完成後按「詠唱」",
    },
    # 21 (Sentence Order - Particles を, に, へ)
    {
        "question_type": "Sentence_Order",
        "questions":[
            { "meaning": "吃蘋果 (Eat an apple)", "answer_order": ["りんご", "を", "たべます"], "options":["りんご", "を", "たべます", "は", "のみます", "が"] },
            { "meaning": "喝水 (Drink water)", "answer_order":["みず", "を", "のみます"], "options":["みず", "を", "のみます", "に", "たべます", "へ"] },
            { "meaning": "去學校 (Go to school)", "answer_order":["がっこう", "に", "いきます"], "options":["がっこう", "に", "いきます", "を", "きます", "で"] },
            { "meaning": "讀書 (Read a book)", "answer_order": ["ほん", "を", "よみます"], "options": ["ほん", "を", "よみます", "が", "かきます", "に"] },
            { "meaning": "回家 (Return home)", "answer_order": ["うち", "に", "かえります"], "options":["うち", "に", "かえります", "を", "でます", "は"] },
            { "meaning": "買肉 (Buy meat)", "answer_order":["にく", "を", "かいます"], "options":["にく", "を", "かいます", "は", "に", "が"] },
            { "meaning": "看電視 (Watch TV)", "answer_order":["テレビ", "を", "みます"], "options":["テレビ", "を", "みます", "に", "へ", "が"] },
            { "meaning": "聽收音機 (Listen to the radio)", "answer_order":["ラジオ", "を", "ききます"], "options":["ラジオ", "を", "ききます", "で", "に", "は"] },
            { "meaning": "買鞋子 (Buy shoes)", "answer_order":["くつ", "を", "かいます"], "options":["くつ", "を", "かいます", "へ", "に", "が"] },
            { "meaning": "去醫院 (Go to the hospital)", "answer_order":["びょういん", "へ", "いきます"], "options":["びょういん", "へ", "いきます", "を", "で", "は"] },
            { "meaning": "喝茶 (Drink tea)", "answer_order":["おちゃ", "を", "のみます"], "options":["おちゃ", "を", "のみます", "に", "が", "へ"] },
            { "meaning": "寫名字 (Write a name)", "answer_order":["なまえ", "を", "かきます"], "options":["なまえ", "を", "かきます", "に", "で", "は"] },
            { "meaning": "見朋友 (Meet a friend)", "answer_order":["ともだち", "に", "あいます"], "options":["ともだち", "に", "あいます", "を", "で", "へ"] },
            { "meaning": "買花 (Buy flowers)", "answer_order":["はな", "を", "かいます"], "options":["はな", "を", "かいます", "に", "が", "へ"] },
            { "meaning": "來到城鎮 (Come to the town)", "answer_order":["まち", "に", "きます"], "options":["まち", "に", "きます", "を", "は", "で"] },
            { "meaning": "乘車 (Ride a car)", "answer_order":["くるま", "に", "のります"], "options":["くるま", "に", "のります", "を", "へ", "が"] },
            { "meaning": "吃魚 (Eat fish)", "answer_order":["さかな", "を", "たべます"], "options":["さかな", "を", "たべます", "に", "で", "は"] },
            { "meaning": "讀報紙 (Read a newspaper)", "answer_order":["しんぶん", "を", "よみます"], "options":["しんぶん", "を", "よみます", "に", "へ", "が"] }
        ],
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "助", # Represents "Particles"
        "target": [6, 7],
        "enemy_hp": 120 * (1.5 if save['hard'] else 1), # 6 hits to defeat
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "將單字拖入上方橫線組成正確句子，完成後按「詠唱」",
    },
    # 22 (Sentence Order - Subject + Object + Verb)
    {
        "question_type": "Sentence_Order",
        "questions":[
            { "meaning": "我吃肉 (I eat meat)", "answer_order":["わたし", "は", "にく", "を", "たべます"], "options":["わたし", "は", "にく", "を", "たべます", "が", "に"] },
            { "meaning": "莉子喝水 (Riko drinks water)", "answer_order": ["りこ", "は", "みず", "を", "のみます"], "options":["りこ", "は", "みず", "を", "のみます", "へ", "で"] },
            { "meaning": "我去學校 (I go to school)", "answer_order":["わたし", "は", "がっこう", "に", "いきます"], "options":["わたし", "は", "がっこう", "に", "いきます", "を", "で"] },
            { "meaning": "老師看書 (The teacher reads a book)", "answer_order":["せんせい", "は", "ほん", "を", "よみます"], "options":["せんせい", "は", "ほん", "を", "よみます", "が", "に"] },
            { "meaning": "赤真買蘋果 (Akamasa buys an apple)", "answer_order": ["あかまさ", "は", "りんご", "を", "かいます"], "options":["あかまさ", "は", "りんご", "を", "かいます", "の", "へ"] },
            { "meaning": "學生寫字 (The student writes characters)", "answer_order":["がくせい", "は", "じ", "を", "かきます"], "options":["がくせい", "は", "じ", "を", "かきます", "に", "の"] },
            { "meaning": "貓看鳥 (The cat looks at the bird)", "answer_order":["ねこ", "は", "とり", "を", "みます"], "options":["ねこ", "は", "とり", "を", "みます", "が", "へ"] },
            { "meaning": "我寫信 (I write a letter)", "answer_order":["わたし", "は", "てがみ", "を", "かきます"], "options":["わたし", "は", "てがみ", "を", "かきます", "に", "で"] },
            { "meaning": "他買車 (He buys a car)", "answer_order":["かれ", "は", "くるま", "を", "かいます"], "options":["かれ", "は", "くるま", "を", "かいます", "が", "へ"] },
            { "meaning": "她看花 (She looks at the flower)", "answer_order":["かのじょ", "は", "はな", "を", "みます"], "options":["かのじょ", "は", "はな", "を", "みます", "に", "の"] },
            { "meaning": "男孩吃麵包 (The boy eats bread)", "answer_order":["おとこのこ", "は", "パン", "を", "たべます"], "options":["おとこのこ", "は", "パン", "を", "たべます", "で", "が"] },
            { "meaning": "女孩喝茶 (The girl drinks tea)", "answer_order":["おんなのこ", "は", "おちゃ", "を", "のみます"], "options":["おんなのこ", "は", "おちゃ", "を", "のみます", "に", "へ"] },
            { "meaning": "我聽音樂 (I listen to music)", "answer_order":["わたし", "は", "おんがく", "を", "ききます"], "options":["わたし", "は", "おんがく", "を", "ききます", "が", "の"] },
            { "meaning": "老師說英語 (The teacher speaks English)", "answer_order":["せんせい", "は", "えいご", "を", "はなします"], "options":["せんせい", "は", "えいご", "を", "はなします", "に", "で"] },
            { "meaning": "莉子使用魔法 (Riko uses magic)", "answer_order":["りこ", "は", "まほう", "を", "つかいます"], "options":["りこ", "は", "まほう", "を", "つかいます", "が", "へ"] },
            { "meaning": "赤真喝藥 (Akamasa drinks medicine)", "answer_order":["あかまさ", "は", "くすり", "を", "のみます"], "options":["あかまさ", "は", "くすり", "を", "のみます", "で", "に"] },
            { "meaning": "我看報紙 (I read the newspaper)", "answer_order":["わたし", "は", "しんぶん", "を", "よみます"], "options":["わたし", "は", "しんぶん", "を", "よみます", "の", "へ"] }
        ],
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "連",
        "target": [7, 8],
        "enemy_hp": 140 * (1.5 if save['hard'] else 1), # 7 hits to defeat\
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "將單字拖入上方橫線組成正確句子，完成後按「詠唱」",
    },
    # 23 (Sentence Order - Expansion with Time & Location)
    {
        "question_type": "Sentence_Order",
        "questions":[
            { "meaning": "今天我在家 (I am at home today)", "answer_order": ["きょう", "わたし", "は", "うち", "に", "います"], "options":["きょう", "わたし", "は", "うち", "に", "います", "を", "へ"] },
            { "meaning": "昨天吃了蘋果 (Ate an apple yesterday)", "answer_order":["きのう", "りんご", "を", "たべました"], "options":["きのう", "りんご", "を", "たべました", "たべます", "に", "は"] },
            { "meaning": "在學校讀書 (Study at school)", "answer_order":["がっこう", "で", "ほん", "を", "よみます"], "options":["がっこう", "で", "ほん", "を", "よみます", "に", "が"] },
            { "meaning": "明天去森林 (Go to the forest tomorrow)", "answer_order": ["あした", "もり", "へ", "いきます"], "options": ["あした", "もり", "へ", "いきます", "で", "を", "きのう"] },
            { "meaning": "在餐廳吃肉 (Eat meat at the restaurant)", "answer_order":["レストラン", "で", "にく", "を", "たべます"], "options":["レストラン", "で", "にく", "を", "たべます", "に", "は"] },
            { "meaning": "每天早上喝水 (Drink water every morning)", "answer_order":["まいあさ", "みず", "を", "のみます"], "options":["まいあさ", "みず", "を", "のみます", "は", "で", "の"] },
            { "meaning": "昨天莉子買了書 (Riko bought a book yesterday)", "answer_order": ["きのう", "りこ", "は", "ほん", "を", "かいました"], "options":["きのう", "りこ", "は", "ほん", "を", "かいました", "かいます", "で"] },
            { "meaning": "在房間寫字 (Write characters in the room)", "answer_order":["へや", "で", "じ", "を", "かきます"], "options":["へや", "で", "じ", "を", "かきます", "に", "へ"] },
            { "meaning": "今天在公園玩 (Play in the park today)", "answer_order":["きょう", "こうえん", "で", "あそびます"], "options":["きょう", "こうえん", "で", "あそびます", "に", "を"] },
            { "meaning": "下週去東京 (Go to Tokyo next week)", "answer_order":["らいしゅう", "とうきょう", "へ", "いきます"], "options":["らいしゅう", "とうきょう", "へ", "いきます", "で", "を"] },
            { "meaning": "每天在圖書館學習 (Study at the library everyday)", "answer_order":["まいにち", "としょかん", "で", "べんきょうします"], "options":["まいにち", "としょかん", "で", "べんきょうします", "に", "は"] },
            { "meaning": "昨天在海裡游泳 (Swam in the sea yesterday)", "answer_order":["きのう", "うみ", "で", "およぎました"], "options":["きのう", "うみ", "で", "およぎました", "に", "およぎます"] },
            { "meaning": "明天在電影院看電影 (Watch a movie at the cinema tomorrow)", "answer_order":["あした", "えいがかん", "で", "えいが", "を", "みます"], "options":["あした", "えいがかん", "で", "えいが", "を", "みます", "に"] },
            { "meaning": "今晚在家看電視 (Watch TV at home tonight)", "answer_order":["こんや", "うち", "で", "テレビ", "を", "みます"], "options":["こんや", "うち", "で", "テレビ", "を", "みます", "へ"] },
            { "meaning": "去年我去了日本 (I went to Japan last year)", "answer_order":["きょねん", "わたし", "は", "にほん", "へ", "いきました"], "options":["きょねん", "わたし", "は", "にほん", "へ", "いきました", "で"] },
            { "meaning": "每晚我聽音樂 (I listen to music every night)", "answer_order":["まいばん", "わたし", "は", "おんがく", "を", "ききます"], "options":["まいばん", "わたし", "は", "おんがく", "を", "ききます", "で", "に"] },
            { "meaning": "早上在咖啡廳喝咖啡 (Drink coffee at a cafe in the morning)", "answer_order":["あさ", "カフェ", "で", "コーヒー", "を", "のみます"], "options":["あさ", "カフェ", "で", "コーヒー", "を", "のみます", "に", "が"] }
        ],
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "完",
        "target": [8, 9],
        "enemy_hp": 160 * (1.5 if save['hard'] else 1), # 8 hits to defeat
        "enemy_attack": 40 * (1.5 if save['hard'] else 1),
        "discription": "將單字拖入上方橫線組成正確句子，完成後按「詠唱」",
    },

    #24 (masu to ru)
    {
        "question_type": "input",
        "question": "verb_masu",
        "answer": "verb_ru",
        "enemy_surf": 29,
        "counter": 0,
        "enemy_attack_word": "打",
        "target": [7, 10],
        "enemy_hp": 140 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\nます形 → 辞書形",
    },
    # 25 (Input - Ru to Te Form)
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_te",
        "enemy_surf": 9,
        "counter": 0,
        "enemy_attack_word": "連",
        "target": [9, 11], # 9 hits for 3 stars
        "enemy_hp": 180 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → て形",
    },
    # 26 (Input - Ru to Nai Form)
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_nai",
        "enemy_surf": 9,
        "counter": 0,
        "enemy_attack_word": "無",
        "target":[10, 12], # 10 hits for 3 stars
        "enemy_hp": 200 * (1.5 if save['hard'] else 1),
        "enemy_attack": 40 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → ない形 (否定)",
    },
    # 27 (Input - Ru to Ta Form)
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_ta",
        "enemy_surf": 9,
        "counter": 0,
        "enemy_attack_word": "極",
        "target": [11, 13], # 11 hits for 3 stars
        "enemy_hp": 220 * (1.5 if save['hard'] else 1),
        "enemy_attack": 40 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → た形 (過去式)",
    },
    # 28 (Input - Ru to Kanou Form / Boss Fight)
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_kanou",
        "enemy_surf": 81,  # Demon Dragon Boss Sprite
        "counter": 0,
        "enemy_attack_word": "滅",
        "target": [20, 25], # 20 hits required! A true test of endurance.
        "enemy_hp": 400 * (1.5 if save['hard'] else 1),
        "enemy_attack": 50 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "【魔龍降臨】以鍵盤輸入羅馬拼音後，按Enter\n辞書形 → 可能形 (能/可以)",
    },
    # 29 chapter 4 Bad Ending (Stage 29)
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_ro",
        "enemy_surf": 83,
        "counter": 0,
        "enemy_attack_word": "殺",
        "target": [8, 10],
        "enemy_hp": 260 * (1.5 if save['hard'] else 1),
        "enemy_attack": 50 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → 命令形 (強制...)",
    },
    #30
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_na",
        "enemy_surf": 84,
        "counter": 0,
        "enemy_attack_word": "怨",
        "target": [10, 12],
        "enemy_hp": 280 * (1.5 if save['hard'] else 1),
        "enemy_attack": 60 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → 禁止形 (不准...)",
    },
    #31
    {
        "question_type": "Sentence_Order",
        "questions":[
            { "meaning": "我殺了莉子 (I killed Riko)", "answer_order":["わたし", "は", "りこ", "を", "ころしました"], "options":["わたし", "は", "りこ", "を", "ころしました", "が", "に"] },
            { "meaning": "甚麼都沒有 (There is nothing)", "answer_order": ["なにも", "ありません"], "options":["なにも", "ありません", "あります", "は", "が"] },
            { "meaning": "世界將會毀滅 (The world will be destroyed)", "answer_order": ["せかい", "は", "ほろびます"], "options": ["せかい", "は", "ほろびます", "を", "に"] },
            { "meaning": "不要死 (Don't die)", "answer_order":["しなないで", "ください"], "options":["しなないで", "ください", "しにます", "は", "で"] },
            { "meaning": "我是魔王 (I am the Demon King)", "answer_order": ["わたし", "は", "まおう", "です"], "options":["わたし", "は", "まおう", "です", "が", "を"] },
            { "meaning": "已經太遲了 (It is already too late)", "answer_order": ["もう", "おそい", "です"], "options": ["もう", "おそい", "です", "はやい", "は", "が"] },
            { "meaning": "心裡很痛 (My heart hurts)", "answer_order": ["こころ", "が", "いたい", "です"], "options": ["こころ", "が", "いたい", "です", "を", "は"] },
            { "meaning": "人類很愚蠢 (Humans are foolish)", "answer_order": ["にんげん", "は", "おろか", "です"], "options": ["にんげん", "は", "おろか", "です", "を", "に", "かしこい"] },
            { "meaning": "我不會原諒你 (I won't forgive you)", "answer_order": ["あなた", "を", "ゆるしません"], "options": ["あなた", "を", "ゆるしません", "ゆるします", "が", "に"] },
            { "meaning": "全部破壞吧 (Destroy everything)", "answer_order": ["すべて", "を", "こわします"], "options": ["すべて", "を", "こわします", "に", "は", "つくります"] },
            { "meaning": "沒人能救我 (No one can save me)", "answer_order": ["だれも", "わたし", "を", "たすけません"], "options": ["だれも", "わたし", "を", "たすけません", "が", "に", "たすけます"] },
            { "meaning": "這是絕望 (This is despair)", "answer_order": ["これ", "は", "ぜつぼう", "です"], "options": ["これ", "は", "ぜつぼう", "です", "きぼう", "が", "を"] },
            { "meaning": "血流不止 (The blood won't stop flowing)", "answer_order": ["ち", "が", "とまりません"], "options": ["ち", "が", "とまりません", "を", "は", "とまります"] },
            { "meaning": "聽不見聲音 (I can't hear any sound)", "answer_order": ["おと", "が", "きこえません"], "options": ["おと", "が", "きこえません", "を", "は", "きこえます"] },
            { "meaning": "我獨自一人 (I am all alone)", "answer_order": ["わたし", "は", "ひとりぼっち", "です"], "options": ["わたし", "は", "ひとりぼっち", "です", "ふたり", "を", "が"] },
            { "meaning": "為什麼會變成這樣？ (Why did it turn out like this?)", "answer_order": ["なぜ", "こう", "なりました", "か"], "options": ["なぜ", "こう", "なりました", "か", "は", "を", "なります"] },
            { "meaning": "結束了 (It's over)", "answer_order": ["おわり", "です"], "options": ["おわり", "です", "はじまり", "は", "が"] }
        ],
        "order":[],
        "enemy_surf": 85,
        "enemy_attack_word": "恨",
        "target": [4, 5],
        "enemy_hp": 300 * (1.5 if save['hard'] else 1),
        "enemy_attack": 70 * (1.5 if save['hard'] else 1),
        "discription": "將單字拖入上方橫線組成正確句子，完成後按「詠唱」",
    },
    #32
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_ba",
        "enemy_surf": 86,
        "counter": 0,
        "enemy_attack_word": "悔",
        "target":[12, 14],
        "enemy_hp": 320 * (1.5 if save['hard'] else 1),
        "enemy_attack": 75 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → 條件形 (ば形)",
    },
    #33
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_saseru_rareru",
        "enemy_surf": 82,
        "counter": 0,
        "enemy_attack_word": "終",
        "target": [20, 25],
        "enemy_hp": 500 * (1.5 if save['hard'] else 1),
        "enemy_attack": 80 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "【魔王降臨】以鍵盤輸入羅馬拼音後，按Enter\n辞書形 → 使役被動形 (被迫...)",
    },
    # 34 chapter 4 True Ending (Stage 34)
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_ikou",
        "enemy_surf": 83,
        "counter": 0,
        "enemy_attack_word": "炎",
        "target": [8, 10],
        "enemy_hp": 260 * (1.5 if save['hard'] else 1),
        "enemy_attack": 50 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → 意向形 (一起...吧！)",
    },
    #35
    {
        "question_type": "Sentence_Order",
         "questions":[
            { "meaning": " (Read a book in the forest today)", "answer_order":["きょう", "もり", "で", "ほん", "を", "よみます"], "options":["きょう", "もり", "で", "ほん", "を", "よみます", "に", "が"] },
            { "meaning": "每天早上吃蘋果 (Eat apples every morning)", "answer_order":["まいあさ", "りんご", "を", "たべます"], "options":["まいあさ", "りんご", "を", "たべます", "に", "は"] },
            { "meaning": "我不吃肉 (I do not eat meat)", "answer_order": ["わたし", "は", "にく", "を", "たべません"], "options":["わたし", "は", "にく", "を", "たべません", "たべます", "が"] },
            { "meaning": "明天去學校 (Go to school tomorrow)", "answer_order": ["あした", "がっこう", "に", "いきます"], "options":["あした", "がっこう", "に", "いきます", "で", "を"] },
            { "meaning": "和莉子一起戰鬥 (Fight together with Riko)", "answer_order": ["りこ", "と", "いっしょに", "たたかいます"], "options": ["りこ", "と", "いっしょに", "たたかいます", "が", "を", "にげます"] },
            { "meaning": "我們不會輸 (We will not lose)", "answer_order": ["わたしたち", "は", "まけません"], "options": ["わたしたち", "は", "まけません", "を", "に", "かちます"] },
            { "meaning": "相信朋友 (Believe in friends)", "answer_order": ["ともだち", "を", "しんじます"], "options": ["ともだち", "を", "しんじます", "に", "は", "うたがいます"] },
            { "meaning": "守護這個世界 (Protect this world)", "answer_order": ["この", "せかい", "を", "まもります"], "options": ["この", "せかい", "を", "まもります", "あの", "に", "こわします"] },
            { "meaning": "用魔法打倒敵人 (Defeat the enemy with magic)", "answer_order": ["まほう", "で", "てき", "を", "たおします"], "options": ["まほう", "で", "てき", "を", "たおします", "に", "は", "が"] },
            { "meaning": "尋找新的武器 (Search for a new weapon)", "answer_order": ["あたらしい", "ぶき", "を", "さがします"], "options": ["あたらしい", "ぶき", "を", "さがします", "ふるい", "に", "が"] },
            { "meaning": "絕對不放棄 (Absolutely will not give up)", "answer_order": ["ぜったいに", "あきらめません"], "options": ["ぜったいに", "あきらめません", "あきらめます", "を", "に"] },
            { "meaning": "明天向城堡出發 (Depart for the castle tomorrow)", "answer_order": ["あした", "しろ", "へ", "しゅっぱつします"], "options": ["あした", "しろ", "へ", "しゅっぱつします", "きのう", "を", "で"] },
            { "meaning": "我們是冒險者 (We are adventurers)", "answer_order": ["わたしたち", "は", "ぼうけんしゃ", "です"], "options": ["わたしたち", "は", "ぼうけんしゃ", "です", "を", "が", "に"] },
            { "meaning": "買強力的裝備 (Buy powerful equipment)", "answer_order": ["つよい", "そうび", "を", "かいます"], "options": ["つよい", "そうび", "を", "かいます", "よわい", "に", "で"] },
            { "meaning": "喝回復藥水 (Drink a healing potion)", "answer_order": ["かいふくやく", "を", "のみます"], "options": ["かいふくやく", "を", "のみます", "たべます", "に", "が"] },
            { "meaning": "拯救大家 (Save everyone)", "answer_order": ["みんな", "を", "たすけます"], "options": ["みんな", "を", "たすけます", "が", "に", "ころします"] }
        ],
        "order":[],
        "enemy_surf": 84,
        "enemy_attack_word": "風",
        "target": [4, 5],
        "enemy_hp": 300 * (1.5 if save['hard'] else 1),
        "enemy_attack": 60 * (1.5 if save['hard'] else 1),
        "discription": "將單字拖入上方橫線組成正確句子，完成後按「詠唱」",
    },
    #36
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_kanou",
        "enemy_surf": 85,
        "counter": 0,
        "enemy_attack_word": "冰",
        "target":[10, 12],
        "enemy_hp": 320 * (1.5 if save['hard'] else 1),
        "enemy_attack": 65 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → 可能形 (能/可以)",
    },
    #37
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_te",
        "enemy_surf": 86,
        "counter": 0,
        "enemy_attack_word": "壁",
        "target": [12, 14],
        "enemy_hp": 340 * (1.5 if save['hard'] else 1),
        "enemy_attack": 70 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → て形 (連續行動)",
    },
    #38
    {
        "question_type": "Sentence_Order",
         "questions":[
            { "meaning": "這是最後的戰鬥 (This is the final battle)", "answer_order": ["これ", "が", "さいご", "の", "たたかい", "です"], "options": ["これ", "が", "さいご", "の", "たたかい", "です", "は", "を", "さいしょ"] },
            { "meaning": "發動最強的魔法 (Activate the strongest magic)", "answer_order": ["さいきょう", "の", "まほう", "を", "はつどうします"], "options": ["さいきょう", "の", "まほう", "を", "はつどうします", "が", "に", "さいじゃく"] },
            { "meaning": "我一定會打倒魔王 (I will definitely defeat the Demon King)", "answer_order": ["わたし", "は", "かならず", "まおう", "を", "たおします"], "options": ["わたし", "は", "かならず", "まおう", "を", "たおします", "が", "に", "まけます"] },
            { "meaning": "和大家一起回家 (Return home together with everyone)", "answer_order": ["みんな", "と", "いっしょに", "かえります"], "options": ["みんな", "と", "いっしょに", "かえります", "を", "が", "いきます"] },
            { "meaning": "你的野心到此為止了 (Your ambition ends here)", "answer_order": ["おまえ", "の", "やぼう", "は", "ここ", "まで", "です"], "options": ["おまえ", "の", "やぼう", "は", "ここ", "まで", "です", "が", "を", "そこ"] },
            { "meaning": "我們的羈絆是無限的 (Our bond is infinite)", "answer_order": ["わたしたち", "の", "きずな", "は", "むげん", "です"], "options": ["わたしたち", "の", "きずな", "は", "むげん", "です", "が", "を", "ゆうげん"] },
            { "meaning": "迎接光明的未來 (Welcome a bright future)", "answer_order": ["あかるい", "みらい", "を", "むかえます"], "options": ["あかるい", "みらい", "を", "むかえます", "くらい", "に", "が"] },
            { "meaning": "舉起傳說的劍 (Raise the legendary sword)", "answer_order": ["でんせつ", "の", "つるぎ", "を", "かかげます"], "options": ["でんせつ", "の", "つるぎ", "を", "かかげます", "が", "に", "おとします"] },
            { "meaning": "勇者不畏懼黑暗 (A hero does not fear the dark)", "answer_order": ["ゆうしゃ", "は", "やみ", "を", "おそれません"], "options": ["ゆうしゃ", "は", "やみ", "を", "おそれません", "が", "に", "ひかり"] },
            { "meaning": "奇蹟一定會發生 (A miracle will definitely happen)", "answer_order": ["きせき", "は", "かならず", "おきます"], "options": ["きせき", "は", "かならず", "おきます", "を", "に", "おきません"] },
            { "meaning": "為了和平而戰 (Fight for peace)", "answer_order": ["へいわ", "の", "ために", "たたかいます"], "options": ["へいわ", "の", "ために", "たたかいます", "が", "を", "にげます"] },
            { "meaning": "把力量借給我 (Lend me your power)", "answer_order": ["わたし", "に", "ちから", "を", "かして", "ください"], "options": ["わたし", "に", "ちから", "を", "かして", "ください", "が", "で", "かえして"] },
            { "meaning": "突破極限 (Break through the limits)", "answer_order": ["げんかい", "を", "とっぱします"], "options": ["げんかい", "を", "とっぱします", "が", "に", "あきらめます"] },
            { "meaning": "絕對不會逃跑 (Absolutely will not run away)", "answer_order": ["ぜったいに", "にげません"], "options": ["ぜったいに", "にげません", "にげます", "を", "に"] },
            { "meaning": "使出全部的力量 (Put forth all power)", "answer_order": ["すべて", "の", "ちから", "を", "だします"], "options": ["すべて", "の", "ちから", "を", "だします", "が", "に", "かくします"] },
            { "meaning": "創造新的傳說 (Create a new legend)", "answer_order": ["あたらしい", "でんせつ", "を", "つくります"], "options": ["あたらしい", "でんせつ", "を", "つくります", "ふるい", "が", "に"] },
            { "meaning": "我感謝莉子 (I thank Riko)", "answer_order": ["わたし", "は", "りこ", "に", "かんしゃします"], "options": ["わたし", "は", "りこ", "に", "かんしゃします", "を", "で", "あやまります"] }
        ],
        "order":[],
        "enemy_surf": 82,
        "enemy_attack_word": "滅",
        "target": [5, 6],
        "enemy_hp": 800 * (1.5 if save['hard'] else 1), # Demon King has very high HP!
        "enemy_attack": 80 * (1.5 if save['hard'] else 1),
        "discription": "【魔王降臨】將單字拖入橫線組成句子，發動最終詠唱！",
    }
    
    

]

def reload_battle_detail():
    battle_detail = [
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
        "enemy_hp": 100 * (1.5 if save['hard'] else 1),
        "enemy_attack": 20 * (1.5 if save['hard'] else 1),
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
        "enemy_hp": 200 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "以滑, 鼠點擊正確的選項",
    },
    # 2
    {
        "question_type": "MC",
        "question":["さ","し","す","せ","そ", "ざ","じ","ず","ぜ","ぞ"],
        "answer": {
            "さ": ("sa", ["sa", "za", "chi", "ki"]),
            "し": ("shi", ["shi", "ji", "chi", "tsu"]),
            "す": ("su", ["su", "zu", "tsu", "ku"]),
            "せ": ("se",["se", "ze", "te", "ne"]),
            "そ": ("so",["so", "zo", "to", "ko"]),
            "ざ": ("za",["za", "sa", "da", "ga"]),
            "じ": ("ji", ["ji", "shi", "gi", "zi"]),
            "ず": ("zu", ["zu", "su", "dzu", "gu"]),
            "ぜ": ("ze", ["ze", "se", "de", "ge"]),
            "ぞ": ("zo", ["zo", "so", "do", "go"])
        },
        "word_size": 64,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "や" ,
        "target": [10, 14],
        "enemy_hp": 200 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 3
    {
        "question_type": "MC",
        "question":["た","ち","つ","て","と", "だ","ぢ","づ","で","ど"],
        "answer": {
            "た": ("ta",["ta", "da", "ka", "na"]),
            "ち": ("chi", ["chi", "shi", "ti", "ji"]),
            "つ": ("tsu", ["tsu", "su", "tu", "du"]),
            "て": ("te", ["te", "de", "se", "he"]),
            "と": ("to", ["to", "do", "ko", "so"]),
            "だ": ("da",["da", "ta", "ba", "ga"]),
            "ぢ": ("di",["di", "ji", "chi", "zi"]),
            "づ": ("du",["du", "zu", "tsu", "dzu"]),
            "で": ("de", ["de", "te", "ge", "be"]),
            "ど": ("do", ["do", "to", "go", "bo"])
        },
        "word_size": 64,
        "order":[],
        "enemy_surf": 79,
        "enemy_attack_word": "爪", 
        "target":[10, 14],
        "enemy_hp": 220 * (1.5 if save['hard'] else 1),
        "enemy_attack": 40 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 4
    {
        "question_type": "MC",
        "question":["な","に","ぬ","ね","の", "ま","み","む","め","も"],
        "answer": {
            "な": ("na",["na", "ma", "ta", "ha"]),
            "に": ("ni",["ni", "mi", "ri", "chi"]),
            "ぬ": ("nu", ["nu", "mu", "me", "ne"]),  # Tests visual similarity with me/ne
            "ね": ("ne",["ne", "re", "wa", "nu"]),  # Tests visual similarity with re/wa
            "の": ("no",["no", "mo", "so", "ro"]),
            "ま": ("ma",["ma", "na", "ha", "ho"]),  # Tests visual similarity with ha/ho
            "み": ("mi",["mi", "ni", "ri", "hi"]),
            "む": ("mu",["mu", "su", "nu", "fu"]),  # Tests visual similarity with su
            "め": ("me",["me", "nu", "ne", "no"]),  # Tests visual similarity with nu/ne
            "も": ("mo",["mo", "ma", "to", "yo"])
        },
        "word_size": 64,
        "order":[],
        "enemy_surf": 78, 
        "enemy_attack_word": "吼", 
        "target":[10, 14],
        "enemy_hp": 240 * (1.5 if save['hard'] else 1),
        "enemy_attack": 50 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 5
    {
        "question_type": "MC",
        "question":["は","ひ","ふ","へ","ほ", "ば","び","ぶ","べ","ぼ", "ぱ","ぴ","ぷ","ぺ","ぽ"],
        "answer": {
            "は": ("ha",["ha", "ba", "pa", "ho"]), # Tests visual similarity with ho
            "ひ": ("hi", ["hi", "bi", "pi", "ni"]),
            "ふ": ("fu",["fu", "bu", "pu", "nu"]),
            "へ": ("he",["he", "be", "pe", "te"]),
            "ほ": ("ho",["ho", "bo", "po", "ha"]), # Tests visual similarity with ha
            "ば": ("ba",["ba", "ha", "pa", "da"]),
            "び": ("bi", ["bi", "hi", "pi", "ji"]),
            "ぶ": ("bu", ["bu", "fu", "pu", "zu"]),
            "べ": ("be", ["be", "he", "pe", "de"]),
            "ぼ": ("bo",["bo", "ho", "po", "do"]),
            "ぱ": ("pa",["pa", "ha", "ba", "ya"]),
            "ぴ": ("pi",["pi", "hi", "bi", "ri"]),
            "ぷ": ("pu", ["pu", "fu", "bu", "mu"]),
            "ぺ": ("pe", ["pe", "he", "be", "re"]),
            "ぽ": ("po", ["po", "ho", "bo", "so"])
        },
        "word_size": 64,
        "order":[],
        "enemy_surf": 9, 
        "enemy_attack_word": "擊",
        "target": [15, 18],
        "enemy_hp": 260 * (1.5 if save['hard'] else 1),
        "enemy_attack": 60 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 6
    {
        "question_type": "MC",
        "question":["や","ゆ","よ", "ら","り","る","れ","ろ", "わ","を","ん"],
        "answer": {
            "や": ("ya", ["ya", "ka", "yo", "wa"]),
            "ゆ": ("yu", ["yu", "yo", "nu", "me"]),
            "よ": ("よ",["yo", "ma", "ha", "ro"]),
            "ら": ("ra",["ra", "chi", "u", "ro"]),  # Tests similarity with chi (ち) and u (う)
            "り": ("ri", ["ri", "i", "ni", "re"]),   # Tests similarity with i (い)
            "る": ("ru", ["ru", "ro", "su", "tsu"]), # Tests similarity with ro (ろ)
            "れ": ("re", ["re", "ne", "wa", "nu"]),  # Tests similarity with ne (ね) and wa (わ)
            "ろ": ("ro",["ro", "ru", "so", "tsu"]), # Tests similarity with ru (る)
            "わ": ("wa", ["wa", "re", "ne", "wo"]),  # Tests similarity with re (れ) and ne (ね)
            "を": ("wo",["wo", "o", "wa", "n"]),    # Tests phonetic similarity with o (お)
            "ん": ("n",["n", "m", "h", "so"])
        },
        "word_size": 64,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "突", 
        "target": [11, 15], # Adjusted for 11 questions
        "enemy_hp": 280 * (1.5 if save['hard'] else 1),
        "enemy_attack": 70 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 7
    {
        "question_type": "MC",
        "question":[
            "あ","い","う","え","お", "か","き","く","け","こ", "が","ぎ","ぐ","げ","ご",
            "さ","し","す","せ","そ", "ざ","じ","ず","ぜ","ぞ", "た","ち","つ","て","と",
            "だ","ぢ","づ","で","ど", "な","に","ぬ","ね","の", "ま","み","む","め","も",
            "は","ひ","ふ","へ","ほ", "ば","び","ぶ","べ","ぼ", "ぱ","ぴ","ぷ","ぺ","ぽ",
            "や","ゆ","よ", "ら","り","る","れ","ろ", "わ","を","ん"
        ],
        "answer": {
            "あ": ("a",["a", "i", "u", "e"]),
            "い": ("i",["i", "u", "e", "o"]),
            "う": ("u",["u", "e", "o", "a"]),
            "え": ("e", ["e", "o", "a", "i"]),
            "お": ("o", ["o", "a", "i", "u"]),
            "か": ("ka", ["ka", "ga", "ha", "wa"]),
            "き": ("ki",["ki", "sa", "chi", "gi"]),
            "く": ("ku",["ka", "ga", "ku", "su"]),
            "け": ("ke",["ke", "ka", "ki", "gi"]),
            "こ": ("ko", ["ko", "go", "wo", "ka"]),
            "が": ("ga", ["ga", "ka", "na", "ra"]),
            "ぎ": ("gi", ["gi", "ki", "shi", "bi"]),
            "ぐ": ("gu",["gu", "ku", "su", "bu"]),
            "げ": ("ge",["ge", "ke", "ko", "go"]),
            "ご": ("go",["go", "ko", "so", "ga"]),
            "さ": ("sa", ["sa", "za", "chi", "ki"]),
            "し": ("shi", ["shi", "ji", "chi", "tsu"]),
            "す": ("su", ["su", "zu", "tsu", "ku"]),
            "せ": ("se",["se", "ze", "te", "ne"]),
            "そ": ("so",["so", "zo", "to", "ko"]),
            "ざ": ("za",["za", "sa", "da", "ga"]),
            "じ": ("ji", ["ji", "shi", "gi", "zi"]),
            "ず": ("zu", ["zu", "su", "dzu", "gu"]),
            "ぜ": ("ze", ["ze", "se", "de", "ge"]),
            "ぞ": ("zo", ["zo", "so", "do", "go"]),
            "た": ("ta",["ta", "da", "ka", "na"]),
            "ち": ("chi",["chi", "shi", "ti", "ji"]),
            "つ": ("tsu",["tsu", "su", "tu", "du"]),
            "て": ("te", ["te", "de", "se", "he"]),
            "と": ("to", ["to", "do", "ko", "so"]),
            "だ": ("da", ["da", "ta", "ba", "ga"]),
            "ぢ": ("di",["di", "ji", "chi", "zi"]),
            "づ": ("du",["du", "zu", "tsu", "dzu"]),
            "で": ("de",["de", "te", "ge", "be"]),
            "ど": ("do", ["do", "to", "go", "bo"]),
            "な": ("na", ["na", "ma", "ta", "ha"]),
            "に": ("ni", ["ni", "mi", "ri", "chi"]),
            "ぬ": ("nu", ["nu", "mu", "me", "ne"]),
            "ね": ("ne",["ne", "re", "wa", "nu"]),
            "の": ("no",["no", "mo", "so", "ro"]),
            "ま": ("ma", ["ma", "na", "ha", "ho"]),
            "み": ("mi", ["mi", "ni", "ri", "hi"]),
            "む": ("mu", ["mu", "su", "nu", "fu"]),
            "め": ("me", ["me", "nu", "ne", "no"]),
            "も": ("mo",["mo", "ma", "to", "yo"]),
            "は": ("ha",["ha", "ba", "pa", "ho"]),
            "ひ": ("hi", ["hi", "bi", "pi", "ni"]),
            "ふ": ("fu", ["fu", "bu", "pu", "nu"]),
            "へ": ("he", ["he", "be", "pe", "te"]),
            "ほ": ("ho", ["ho", "bo", "po", "ha"]),
            "ば": ("ba",["ba", "ha", "pa", "da"]),
            "び": ("bi",["bi", "hi", "pi", "ji"]),
            "ぶ": ("bu", ["bu", "fu", "pu", "zu"]),
            "べ": ("be", ["be", "he", "pe", "de"]),
            "ぼ": ("bo", ["bo", "ho", "po", "do"]),
            "ぱ": ("pa", ["pa", "ha", "ba", "ya"]),
            "ぴ": ("pi",["pi", "hi", "bi", "ri"]),
            "ぷ": ("pu",["pu", "fu", "bu", "mu"]),
            "ぺ": ("pe", ["pe", "he", "be", "re"]),
            "ぽ": ("po", ["po", "ho", "bo", "so"]),
            "や": ("ya", ["ya", "ka", "yo", "wa"]),
            "ゆ": ("yu", ["yu", "yo", "nu", "me"]),
            "よ": ("yo",["yo", "ma", "ha", "ro"]),
            "ら": ("ra",["ra", "chi", "u", "ro"]),
            "り": ("ri", ["ri", "i", "ni", "re"]),
            "る": ("ru", ["ru", "ro", "su", "tsu"]),
            "れ": ("re", ["re", "ne", "wa", "nu"]),
            "ろ": ("ro", ["ro", "ru", "so", "tsu"]),
            "わ": ("wa",["wa", "re", "ne", "wo"]),
            "を": ("wo",["wo", "o", "wa", "n"]),
            "ん": ("n",["n", "m", "h", "so"])
        },
        "word_size": 64,
        "order":[],
        "enemy_surf": 29, 
        "enemy_attack_word": "滅", 
        "target": [20, 25], 
        "enemy_hp": 400 * (1.5 if save['hard'] else 1),
        "enemy_attack": 80 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 8
    {
        "question_type": "MC",
        "question":[
            "きゃ","きゅ","きょ", "しゃ","しゅ","しょ", "ちゃ","ちゅ","ちょ", 
            "にゃ","にゅ","にょ", "ひゃ","ひゅ","ひょ", "みゃ","みゅ","みょ", "りゃ","りゅ","りょ"
        ],
        "answer": {
            "きゃ": ("kya", ["kya", "kiya", "kuyo", "gya"]),
            "きゅ": ("kyu", ["kyu", "kiyu", "kya", "gyu"]),
            "きょ": ("kyo", ["kyo", "kiyo", "kyu", "gyo"]),
            "しゃ": ("sha", ["sha", "shiya", "shu", "ja"]),
            "しゅ": ("shu", ["shu", "shiyu", "sho", "ju"]),
            "しょ": ("sho", ["sho", "shiyo", "sha", "jo"]),
            "ちゃ": ("cha",["cha", "chiya", "chu", "sha"]),
            "ちゅ": ("chu",["chu", "chiyu", "cho", "shu"]),
            "ちょ": ("cho",["cho", "chiyo", "cha", "sho"]),
            "にゃ": ("nya",["nya", "niya", "nyu", "mya"]),
            "にゅ": ("nyu",["nyu", "niyu", "nyo", "myu"]),
            "にょ": ("nyo",["nyo", "niyo", "nya", "myo"]),
            "ひゃ": ("hya",["hya", "hiya", "hyu", "pya"]),
            "ひゅ": ("hyu",["hyu", "hiyu", "hyo", "pyu"]),
            "ひょ": ("hyo",["hyo", "hiyo", "hya", "pyo"]),
            "みゃ": ("mya",["mya", "miya", "myu", "nya"]),
            "みゅ": ("myu",["myu", "miyu", "myo", "nyu"]),
            "みょ": ("myo", ["myo", "miyo", "mya", "nyo"]),
            "りゃ": ("rya", ["rya", "riya", "ryu", "mya"]),
            "りゅ": ("ryu", ["ryu", "riyu", "ryo", "myu"]),
            "りょ": ("ryo", ["ryo", "riyo", "rya", "myo"])
        },
        "word_size": 64,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "咬", 
        "target":[12, 16],
        "enemy_hp": 240 * (1.5 if save['hard'] else 1),
        "enemy_attack": 50 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 9 (Kanji - Numbers)
    {
        "question_type": "MC",
        "question":[
            "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "百", "千", "万", "億", "兆", "零",
            "いち", "に", "さん", "よん", "ご", "ろく", "なな", "はち", "きゅう", "じゅう", "ひゃく", "せん", "まん", "おく", "ちょう", "れい"
        ],
        "answer": {
            "一": ("いち", ["いち", "に", "さん", "し"]),
            "二": ("に", ["に", "いち", "さん", "よん"]),
            "三": ("さん", ["さん", "に", "し", "ご"]),
            "四": ("よん", ["よん", "さん", "ご", "ろく"]),
            "五": ("ご", ["ご", "よん", "ろく", "なな"]),
            "六": ("ろく",["ろく", "ご", "なな", "はち"]),
            "七": ("なな",["なな", "ろく", "はち", "きゅう"]),
            "八": ("はち", ["はち", "なな", "きゅう", "じゅう"]),
            "九": ("きゅう", ["きゅう", "はち", "じゅう", "いち"]),
            "十": ("じゅう", ["じゅう", "きゅう", "いち", "に"]),
            "百": ("ひゃく", ["ひゃく", "せん", "まん", "れい"]),
            "千": ("せん", ["せん", "ひゃく", "まん", "ちょう"]),
            "万": ("まん", ["まん", "せん", "ひゃく", "おく"]),
            "億": ("おく", ["おく", "まん", "ちょう", "せん"]),
            "兆": ("ちょう", ["ちょう", "おく", "まん", "ひゃく"]),
            "零": ("れい/ぜろ", ["れい/ぜろ", "いち", "ひゃく", "さん"]),
            "いち": ("一", ["一", "二", "三", "四"]),
            "に": ("二", ["二", "一", "三", "四"]),
            "さん": ("三", ["三", "二", "四", "五"]),
            "よん": ("四", ["四", "三", "五", "六"]),
            "ご": ("五", ["五", "四", "六", "七"]),
            "ろく": ("六", ["六", "五", "七", "八"]),
            "なな": ("七", ["七", "六", "八", "九"]),
            "はち": ("八", ["八", "七", "九", "十"]),
            "きゅう": ("九", ["九", "八", "十", "一"]),
            "じゅう": ("十", ["十", "九", "一", "二"]),
            "ひゃく": ("百", ["百", "千", "万", "零"]),
            "せん": ("千", ["千", "百", "万", "兆"]),
            "まん": ("万", ["万", "千", "百", "億"]),
            "おく": ("億", ["億", "万", "兆", "千"]),
            "ちょう": ("兆", ["兆", "億", "万", "百"]),
            "れい/ぜろ": ("零", ["零", "一", "百", "万"])
        },
        "word_size": 48,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "算",
        "target": [10, 12],
        "enemy_hp": 200 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊漢字正確的平假名讀音",
    },
    # 10 (Kanji - Elements)
    {
        "question_type": "MC",
        "question":[
            "日", "月", "火", "水", "木", "金", "土", "光", "闇", "風", "雷", "氷", "星", "雲", "雪",
            "ひ/にち", "つき", "ひ/か", "みず", "き", "きん", "つち", "ひかり", "やみ", "かぜ", "かみなり", "こおり", "ほし", "くも", "ゆき"
        ],
        "answer": {
            "日": ("ひ/にち",["ひ/にち", "つき", "みず", "き"]),
            "月": ("つき",["つき", "ひ/にち", "つち", "きん"]),
            "火": ("ひ/か",["ひ/か", "みず", "つち", "き"]),
            "水": ("みず",["みず", "つき", "つち", "ひ/か"]),
            "木": ("き",["き", "きん", "ひ/にち", "みず"]),
            "金": ("きん",["きん", "ぎん", "き", "つち"]),
            "土": ("つち",["つち", "みず", "つき", "ひ/にち"]),
            "光": ("ひかり", ["ひかり", "やみ", "かぜ", "ほし"]),
            "闇": ("やみ", ["やみ", "ひかり", "かげ", "ゆき"]),
            "風": ("かぜ", ["かぜ", "くも", "あめ", "ゆき"]),
            "雷": ("かみなり", ["かみなり", "あめ", "ゆき", "かぜ"]),
            "氷": ("こおり", ["こおり", "みず", "ゆき", "ほし"]),
            "星": ("ほし", ["ほし", "つき", "ひかり", "くも"]),
            "雲": ("くも", ["くも", "あめ", "かぜ", "ゆき"]),
            "雪": ("ゆき", ["ゆき", "こおり", "あめ", "くも"]),
            "ひ/にち": ("日", ["日", "月", "水", "木"]),
            "つき": ("月", ["月", "日", "土", "金"]),
            "ひ/か": ("火", ["火", "水", "土", "木"]),
            "みず": ("水", ["水", "月", "土", "火"]),
            "き": ("木", ["木", "金", "日", "水"]),
            "きん": ("金", ["金", "銀", "木", "土"]),
            "つち": ("土", ["土", "水", "月", "日"]),
            "ひかり": ("光", ["光", "闇", "風", "星"]),
            "やみ": ("闇", ["闇", "光", "影", "雪"]),
            "かぜ": ("風", ["風", "雲", "雨", "雪"]),
            "かみなり": ("雷", ["雷", "雨", "雪", "風"]),
            "こおり": ("氷", ["氷", "水", "雪", "星"]),
            "ほし": ("星", ["星", "月", "光", "雲"]),
            "くも": ("雲", ["雲", "雨", "風", "雪"]),
            "ゆき": ("雪", ["雪", "氷", "雨", "雲"])
        },
        "word_size": 40,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "素",
        "target": [6, 7],
        "enemy_hp": 140 * (1.5 if save['hard'] else 1),
        "enemy_attack": 20 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊漢字正確的平假名讀音",
    },
    # 11 (kanji - Animals & Objects)
    {
        "question_type": "Drag",
        "questions": [
            { "sentence": "猫_", "answer": "ねこ", "options": ["ねこ", "いぬ", "とり", "さかな"] },
            { "sentence": "犬_", "answer": "いぬ", "options": ["いぬ", "ねこ", "うさぎ", "へび"] },
            { "sentence": "本_", "answer": "ほん", "options": ["ほん", "えんぴつ", "かばん", "とけい"] },
            { "sentence": "車_", "answer": "くるま", "options": ["くるま", "でんしゃ", "ふね", "ひこうき"] },
            { "sentence": "鳥_", "answer": "とり", "options": ["とり", "さかな", "ねこ", "いぬ"] },
            { "sentence": "魚_", "answer": "さかな", "options": ["さかな", "とり", "うさぎ", "へび"] },
            { "sentence": "鉛筆_", "answer": "えんぴつ", "options": ["えんぴつ", "ほん", "かさ", "くつ"] },
            { "sentence": "鞄_", "answer": "かばん", "options": ["かばん", "とけい", "ほん", "えんぴつ"] },
            { "sentence": "時計_", "answer": "とけい", "options": ["とけい", "かばん", "かさ", "くつ"] },
            { "sentence": "肉_", "answer": "にく", "options": ["にく", "さかな", "やさい", "ごはん"] },
            { "sentence": "傘_", "answer": "かさ", "options": ["かさ", "くつ", "かばん", "とけい"] },
            { "sentence": "靴_", "answer": "くつ", "options": ["くつ", "かさ", "ほん", "えんぴつ"] },
            { "sentence": "桜_", "answer": "さくら", "options": ["さくら", "はな", "き", "はし"] },
            { "sentence": "橋_", "answer": "はし", "options": ["はし", "みち", "さくら", "き"] },
            { "sentence": "薬_", "answer": "くすり", "options": ["くすり", "みず", "おちゃ", "にく"] },
            { "sentence": "ねこ_", "answer": "猫", "options": ["猫", "犬", "鳥", "魚"] },
            { "sentence": "いぬ_", "answer": "犬", "options": ["犬", "猫", "兎", "蛇"] },
            { "sentence": "ほん_", "answer": "本", "options": ["本", "鉛筆", "鞄", "時計"] },
            { "sentence": "くるま_", "answer": "車", "options": ["車", "電車", "船", "飛行機"] },
            { "sentence": "とり_", "answer": "鳥", "options": ["鳥", "魚", "猫", "犬"] },
            { "sentence": "さかな_", "answer": "魚", "options": ["魚", "鳥", "兎", "蛇"] },
            { "sentence": "えんぴつ_", "answer": "鉛筆", "options": ["鉛筆", "本", "傘", "靴"] },
            { "sentence": "かばん_", "answer": "鞄", "options": ["鞄", "時計", "本", "鉛筆"] },
            { "sentence": "とけい_", "answer": "時計", "options": ["時計", "鞄", "傘", "靴"] },
            { "sentence": "にく_", "answer": "肉", "options": ["肉", "魚", "野菜", "ご飯"] },
            { "sentence": "かさ_", "answer": "傘", "options": ["傘", "靴", "鞄", "時計"] },
            { "sentence": "くつ_", "answer": "靴", "options": ["靴", "傘", "本", "鉛筆"] },
            { "sentence": "さくら_", "answer": "桜", "options": ["桜", "花", "木", "橋"] },
            { "sentence": "はし_", "answer": "橋", "options": ["橋", "道", "桜", "木"] },
            { "sentence": "くすり_", "answer": "薬", "options": ["薬", "水", "お茶", "肉"] }
        ],
        "order": [],
        "enemy_surf": 9,
        "enemy_attack_word": "物",
        "target": [7, 9],
        "enemy_hp": 140 * (1.5 if save['hard'] else 1),
        "enemy_attack": 20 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠拖拉正確的選項至空格內",
    },
    # 12 (kanji - Nature)
    {
        "question_type": "MC",
        "question":[
            "山", "川", "空", "天", "雨", "石", "花", "森", "海", "陸", "谷", "草", "葉", "根", "泥",
            "やま", "かわ", "そら", "てん", "あめ", "いし", "はな", "もり", "うみ", "りく", "たに", "くさ", "は", "ね", "どろ"
        ],
        "answer": {
            "山": ("やま", ["やま", "かわ", "そら", "てん"]),
            "川": ("かわ", ["かわ", "やま", "うみ", "あめ"]),
            "空": ("そら", ["そら", "てん", "あめ", "いし"]),
            "天": ("てん", ["てん", "そら", "やま", "もり"]),
            "雨": ("あめ", ["あめ", "かわ", "はな", "そら"]),
            "石": ("いし", ["いし", "やま", "はな", "もり"]),
            "花": ("はな", ["はな", "あめ", "そら", "いし"]),
            "森": ("もり", ["もり", "やま", "かわ", "てん"]),
            "海": ("うみ", ["うみ", "かわ", "やま", "みず"]),
            "陸": ("りく", ["りく", "うみ", "そら", "もり"]),
            "谷": ("たに", ["たに", "やま", "かわ", "もり"]),
            "草": ("くさ", ["くさ", "はな", "き", "は"]),
            "葉": ("は", ["は", "き", "くさ", "はな"]),
            "根": ("ね", ["ね", "は", "き", "くさ"]),
            "泥": ("どろ", ["どろ", "いし", "つち", "すな"]),
            "やま": ("山", ["山", "川", "空", "天"]),
            "かわ": ("川", ["川", "山", "海", "雨"]),
            "そら": ("空", ["空", "天", "雨", "石"]),
            "てん": ("天", ["天", "空", "山", "森"]),
            "あめ": ("雨", ["雨", "川", "花", "空"]),
            "いし": ("石", ["石", "山", "花", "森"]),
            "はな": ("花", ["花", "雨", "空", "石"]),
            "もり": ("森", ["森", "山", "川", "天"]),
            "うみ": ("海", ["海", "川", "山", "水"]),
            "りく": ("陸", ["陸", "海", "空", "森"]),
            "たに": ("谷", ["谷", "山", "川", "森"]),
            "くさ": ("草", ["草", "花", "木", "葉"]),
            "は": ("葉", ["葉", "木", "草", "花"]),
            "ね": ("根", ["根", "葉", "木", "草"]),
            "どろ": ("泥", ["泥", "石", "土", "砂"])
        },
        "word_size": 48,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "震",
        "target": [9, 12],
        "enemy_hp": 180 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊漢字正確的平假名讀音",
    },
    # 13 (kanji - Directions)
    {
        "question_type": "Drag",
        "questions":[
            { "sentence": "上_", "answer": "うえ", "options": ["うえ", "した", "ひだり", "みぎ"] },
            { "sentence": "下_", "answer": "した", "options": ["した", "うえ", "まえ", "うしろ"] },
            { "sentence": "左_", "answer": "ひだり", "options":["ひだり", "みぎ", "なか", "そと"] },
            { "sentence": "右_", "answer": "みぎ", "options": ["みぎ", "ひだり", "まえ", "なか"] },
            { "sentence": "中_", "answer": "なか", "options": ["なか", "そと", "うえ", "した"] },
            { "sentence": "外_", "answer": "そと", "options":["そと", "なか", "ひだり", "みぎ"] },
            { "sentence": "前_", "answer": "まえ", "options":["まえ", "うしろ", "うえ", "そと"] },
            { "sentence": "後_", "answer": "うしろ", "options": ["うしろ", "まえ", "した", "なか"] },
            { "sentence": "隣_", "answer": "となり", "options": ["となり", "ちかく", "とおく", "なか"] },
            { "sentence": "近く_", "answer": "ちかく", "options": ["ちかく", "となり", "とおく", "そと"] },
            { "sentence": "遠く_", "answer": "とおく", "options": ["とおく", "ちかく", "となり", "まえ"] },
            { "sentence": "北_", "answer": "きた", "options": ["きた", "みなみ", "ひがし", "にし"] },
            { "sentence": "南_", "answer": "みなみ", "options": ["みなみ", "きた", "ひがし", "にし"] },
            { "sentence": "東_", "answer": "ひがし", "options": ["ひがし", "にし", "みなみ", "きた"] },
            { "sentence": "西_", "answer": "にし", "options": ["にし", "ひがし", "きた", "みなみ"] },
            { "sentence": "うえ_", "answer": "上", "options": ["上", "下", "左", "右"] },
            { "sentence": "した_", "answer": "下", "options": ["下", "上", "前", "後"] },
            { "sentence": "ひだり_", "answer": "左", "options":["左", "右", "中", "外"] },
            { "sentence": "みぎ_", "answer": "右", "options": ["右", "左", "前", "中"] },
            { "sentence": "なか_", "answer": "中", "options": ["中", "外", "上", "下"] },
            { "sentence": "そと_", "answer": "外", "options":["外", "中", "左", "右"] },
            { "sentence": "まえ_", "answer": "前", "options":["前", "後", "上", "外"] },
            { "sentence": "うしろ_", "answer": "後", "options": ["後", "前", "下", "中"] },
            { "sentence": "となり_", "answer": "隣", "options": ["隣", "近く", "遠く", "中"] },
            { "sentence": "ちかく_", "answer": "近く", "options": ["近く", "隣", "遠く", "外"] },
            { "sentence": "とおく_", "answer": "遠く", "options": ["遠く", "近く", "隣", "前"] },
            { "sentence": "きた_", "answer": "北", "options": ["北", "南", "東", "西"] },
            { "sentence": "みなみ_", "answer": "南", "options": ["南", "北", "東", "西"] },
            { "sentence": "ひがし_", "answer": "東", "options": ["東", "西", "南", "北"] },
            { "sentence": "にし_", "answer": "西", "options": ["西", "東", "北", "南"] }
        ],
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "轉",
        "target": [9, 12],
        "enemy_hp": 180 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "將正確的方向漢字拖拉至對應的中文意思旁",
    },
    # 14 (MC - Body & People)
    {
        "question_type": "MC",
         "question":[
            "人", "目", "口", "耳", "手", "足", "体", "男", "女", "頭", "髪", "鼻", "歯", "指", "首", "肩",
            "ひと", "め", "くち", "みみ", "て", "あし", "からだ", "おとこ", "おんな", "あたま", "かみ", "はな", "は", "ゆび", "くび", "かた"
        ],
        "answer": {
            "人": ("ひと", ["ひと", "おとこ", "おんな", "め"]),
            "目": ("め", ["め", "みみ", "くち", "て"]),
            "口": ("くち", ["くち", "め", "みみ", "あし"]),
            "耳": ("みみ", ["みみ", "め", "くち", "からだ"]),
            "手": ("て", ["て", "あし", "め", "ひと"]),
            "足": ("あし", ["あし", "て", "みみ", "おとこ"]),
            "体": ("からだ", ["からだ", "ひと", "おんな", "くち"]),
            "男": ("おとこ", ["おとこ", "おんな", "ひと", "からだ"]),
            "女": ("おんな", ["おんな", "おとこ", "ひと", "て"]),
            "頭": ("あたま", ["あたま", "かみ", "かた", "くび"]),
            "髪": ("かみ", ["かみ", "あたま", "みみ", "め"]),
            "鼻": ("はな", ["はな", "くち", "め", "みみ"]),
            "歯": ("は", ["は", "くち", "はな", "あたま"]),
            "指": ("ゆび", ["ゆび", "て", "あし", "かた"]),
            "首": ("くび", ["くび", "かた", "あたま", "ゆび"]),
            "肩": ("かた", ["かた", "くび", "て", "あし"]),
            "ひと": ("人", ["人", "男", "女", "目"]),
            "め": ("目", ["目", "耳", "口", "手"]),
            "くち": ("口", ["口", "目", "耳", "足"]),
            "みみ": ("耳", ["耳", "目", "口", "体"]),
            "て": ("手", ["手", "足", "目", "人"]),
            "あし": ("足", ["足", "手", "耳", "男"]),
            "からだ": ("体", ["体", "人", "女", "口"]),
            "おとこ": ("男", ["男", "女", "人", "体"]),
            "おんな": ("女", ["女", "男", "人", "手"]),
            "あたま": ("頭", ["頭", "髪", "肩", "首"]),
            "かみ": ("髪", ["髪", "頭", "耳", "目"]),
            "はな": ("鼻", ["鼻", "口", "目", "耳"]),
            "は": ("歯", ["歯", "口", "鼻", "頭"]),
            "ゆび": ("指", ["指", "手", "足", "肩"]),
            "くび": ("首", ["首", "肩", "頭", "指"]),
            "かた": ("肩", ["肩", "首", "手", "足"])
        },
        "word_size": 48,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "抓",
        "target": [10, 13],
        "enemy_hp": 200 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊漢字正確的平假名讀音",
    },
    # 15 (Drag - Time & Periods)
    {
        "question_type": "Drag",
         "questions":[
            { "sentence": "今_", "answer": "いま", "options": ["いま", "じ", "ふん", "はん"] },
            { "sentence": "時_", "answer": "じ", "options":["じ", "いま", "ねん", "あさ"] },
            { "sentence": "分_", "answer": "ふん", "options":["ふん", "はん", "じ", "ひる"] },
            { "sentence": "半_", "answer": "はん", "options": ["はん", "ふん", "いま", "よる"] },
            { "sentence": "年_", "answer": "ねん", "options":["ねん", "じ", "はん", "あさ"] },
            { "sentence": "朝_", "answer": "あさ", "options":["あさ", "ひる", "よる", "いま"] },
            { "sentence": "昼_", "answer": "ひる", "options": ["ひる", "あさ", "よる", "じ"] },
            { "sentence": "夜_", "answer": "よる", "options": ["よる", "ひる", "あさ", "ねん"] },
            { "sentence": "今日_", "answer": "きょう", "options": ["きょう", "あした", "きのう", "まいにち"] },
            { "sentence": "明日_", "answer": "あした", "options": ["あした", "きのう", "きょう", "しゅう"] },
            { "sentence": "昨日_", "answer": "きのう", "options": ["きのう", "あした", "きょう", "しゅう"] },
            { "sentence": "毎日_", "answer": "まいにち", "options": ["まいにち", "きょう", "あした", "きのう"] },
            { "sentence": "週_", "answer": "しゅう", "options": ["しゅう", "ねん", "げつ", "にち"] },
            { "sentence": "夕方_", "answer": "ゆうがた", "options": ["ゆうがた", "あさ", "ひる", "よる"] },
            { "sentence": "季節_", "answer": "きせつ", "options": ["きせつ", "ねん", "しゅう", "ゆうがた"] },
            { "sentence": "いま_", "answer": "今", "options": ["今", "時", "分", "半"] },
            { "sentence": "じ_", "answer": "時", "options":["時", "今", "年", "朝"] },
            { "sentence": "ふん_", "answer": "分", "options":["分", "半", "時", "昼"] },
            { "sentence": "はん_", "answer": "半", "options": ["半", "分", "今", "夜"] },
            { "sentence": "ねん_", "answer": "年", "options":["年", "時", "半", "朝"] },
            { "sentence": "あさ_", "answer": "朝", "options":["朝", "昼", "夜", "今"] },
            { "sentence": "ひる_", "answer": "昼", "options": ["昼", "朝", "夜", "時"] },
            { "sentence": "よる_", "answer": "夜", "options": ["夜", "昼", "朝", "年"] },
            { "sentence": "きょう_", "answer": "今日", "options": ["今日", "明日", "昨日", "毎日"] },
            { "sentence": "あした_", "answer": "明日", "options": ["明日", "昨日", "今日", "週"] },
            { "sentence": "きのう_", "answer": "昨日", "options": ["昨日", "明日", "今日", "週"] },
            { "sentence": "まいにち_", "answer": "毎日", "options": ["毎日", "今日", "明日", "昨日"] },
            { "sentence": "しゅう_", "answer": "週", "options": ["週", "年", "月", "日"] },
            { "sentence": "ゆうがた_", "answer": "夕方", "options": ["夕方", "朝", "昼", "夜"] },
            { "sentence": "きせつ_", "answer": "季節", "options": ["季節", "年", "週", "夕方"] }
        ],
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "遲",
        "target": [10, 13],
        "enemy_hp": 200 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "將正確的時間漢字拖拉至對應的中文意思旁",
    },
    # 16 (MC - Adjectives)
    {
        "question_type": "MC",
        "question":[
            "大きい", "小さい", "高い", "低い", "新しい", "古い", "多い", "少ない", "暑い", "寒い", "熱い", "冷たい", "良い", "悪い", "長い", "短い",
            "おおきい", "ちいさい", "たかい", "ひくい", "あたらしい", "ふるい", "おおい", "すくない", "あつい(氣候)", "さむい", "あつい(溫度)", "つめたい", "よい", "わるい", "ながい", "みじかい"
        ],
        "answer": {
            "大きい": ("おおきい",["おおきい", "ちいさい", "たかい", "ひくい"]),
            "小さい": ("ちいさい", ["ちいさい", "おおきい", "あたらしい", "ふるい"]),
            "高い": ("たかい", ["たかい", "ひくい", "おおきい", "おおい"]),
            "低い": ("ひくい", ["ひくい", "たかい", "ちいさい", "すくない"]),
            "新しい": ("あたらしい", ["あたらしい", "ふるい", "おおきい", "おおい"]),
            "古い": ("ふるい",["ふるい", "あたらしい", "ちいさい", "ひくい"]),
            "多い": ("おおい",["おおい", "すくない", "たかい", "あたらしい"]),
            "少ない": ("すくない",["すくない", "おおい", "ひくい", "ふるい"]),
            "暑い": ("あつい", ["あつい", "さむい", "あたたかい", "すずしい"]),
            "寒い": ("さむい", ["さむい", "あつい", "つめたい", "ながい"]),
            "熱い": ("あつい", ["あつい", "つめたい", "さむい", "わるい"]),
            "冷たい": ("つめたい", ["つめたい", "あつい", "さむい", "よい"]),
            "良い": ("よい", ["よい", "わるい", "ながい", "みじかい"]),
            "悪い": ("わるい", ["わるい", "よい", "たかい", "ひくい"]),
            "長い": ("ながい", ["ながい", "みじかい", "おおきい", "ちいさい"]),
            "短い": ("みじかい", ["みじかい", "ながい", "おおい", "すくない"]),
            "おおきい": ("大きい",["大きい", "小さい", "高い", "低い"]),
            "ちいさい": ("小さい", ["小さい", "大きい", "新しい", "古い"]),
            "たかい": ("高い", ["高い", "低い", "大きい", "多い"]),
            "ひくい": ("低い", ["低い", "高い", "小さい", "少ない"]),
            "あたらしい": ("新しい", ["新しい", "古い", "大きい", "多い"]),
            "ふるい": ("古い",["古い", "新しい", "小さい", "低い"]),
            "おおい": ("多い",["多い", "少ない", "高い", "新しい"]),
            "すくない": ("少ない",["少ない", "多い", "低い", "古い"]),
            "あつい(氣候)": ("暑い", ["暑い", "寒い", "温かい", "涼しい"]),
            "さむい": ("寒い", ["寒い", "暑い", "冷たい", "長い"]),
            "あつい(溫度)": ("熱い", ["熱い", "冷たい", "寒い", "悪い"]),
            "つめたい": ("冷たい", ["冷たい", "熱い", "寒い", "良い"]),
            "よい": ("良い", ["良い", "悪い", "長い", "短い"]),
            "わるい": ("悪い", ["悪い", "良い", "高い", "低い"]),
            "ながい": ("長い", ["長い", "短い", "大きい", "小さい"]),
            "みじかい": ("短い", ["短い", "長い", "多い", "少ない"])
        },
        "word_size": 40,
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "幻",
        "target": [11, 14],
        "enemy_hp": 220 * (1.5 if save['hard'] else 1),
        "enemy_attack": 40 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊形容詞正確的平假名讀音",
    },
    # 17 (kanji to hiragana 1 )
    {
        "question_type": "MC",
        "question": [
            "行きます", "来ます", "帰ります", "出掛けます", "食べます", "飲みます", "見ます", "読みます", "書きます", "聞きます", "買います", "起きます", "寝ます", "走ります", "泳ぎます",
            "いきます", "きます", "かえります", "でかけます", "たべます", "のみます", "みます", "よみます", "かきます", "ききます", "かいます", "おきます", "ねます", "はしります", "およぎます"
        ],
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
            "聞きます": ("ききます", ["ききます", "みにます", "こくます", "きます"]),
            "買います": ("かいます", ["かいます", "かきます", "ききます", "します"]),
            "起きます": ("おきます", ["おきます", "ねます", "みます", "いきます"]),
            "寝ます": ("ねます", ["ねます", "おきます", "のみます", "でます"]),
            "走ります": ("はしります", ["はしります", "あるきます", "かえります", "とまります"]),
            "泳ぎます": ("およぎます", ["およぎます", "やすみます", "あそびます", "よみます"]),
            "いきます": ("行きます", ["行きます", "来ます", "見ます", "聞きます"]),
            "きます": ("来ます", ["来ます", "行きます", "居ます", "着ます"]),
            "かえります": ("帰ります", ["帰ります", "代わります", "戻ります", "出掛ります"]),
            "でかけます": ("出掛けます", ["出掛けます", "手掛けます", "出負けます", "怪我けます"]),
            "たべます": ("食べます", ["食べます", "喋ります", "並べます", "比べます"]),
            "のみます": ("飲みます", ["飲みます", "乗みます", "読みます", "包みます"]),
            "みます": ("見ます", ["見ます", "魅ます", "建ます", "店ます"]),
            "よみます": ("読みます", ["読みます", "呼びます", "飲みます", "休みます"]),
            "かきます": ("書きます", ["書きます", "描きます", "欠きます", "買います"]),
            "ききます": ("聞きます", ["聞きます", "効きます", "来きます", "着きます"]),
            "かいます": ("買います", ["買います", "飼います", "書きます", "会います"]),
            "おきます": ("起きます", ["起きます", "置きます", "寝ます", "行きます"]),
            "ねます": ("寝ます", ["寝ます", "起きます", "飲みます", "出ます"]),
            "はしります": ("走ります", ["走ります", "歩きます", "帰ります", "止まります"]),
            "およぎます": ("泳ぎます", ["泳ぎます", "休みます", "遊びます", "読みます"])
        },
        "word_size": 36,
        "order": [],
        "enemy_surf": 9,
        "enemy_attack_word": "む" ,
        "target": [5, 7],
        "enemy_hp": 100 * (1.5 if save['hard'] else 1),
        "enemy_attack": 20 * (1.5 if save['hard'] else 1),
        "discription": "以滑鼠點擊正確的選項",
    },
    # 18 (kanji - Days of the week)
    {
        "question_type": "Drag",
       "questions":[
            { "sentence": "月曜日_", "answer": "げつようび", "options":["げつようび", "かようび", "すいようび", "にちようび"] },
            { "sentence": "火曜日_", "answer": "かようび", "options":["かようび", "もくようび", "きんようび", "どようび"] },
            { "sentence": "水曜日_", "answer": "すいようび", "options":["すいようび", "かようび", "もくようび", "げつようび"] },
            { "sentence": "木曜日_", "answer": "もくようび", "options": ["もくようび", "すいようび", "きんようび", "どようび"] },
            { "sentence": "金曜日_", "answer": "きんようび", "options":["きんようび", "げつようび", "かようび", "にちようび"] },
            { "sentence": "土曜日_", "answer": "どようび", "options": ["どようび", "にちようび", "すいようび", "もくようび"] },
            { "sentence": "日曜日_", "answer": "にちようび", "options":["にちようび", "げつようび", "きんようび", "どようび"] },
            { "sentence": "週末_", "answer": "しゅうまつ", "options":["しゅうまつ", "へいじつ", "しゅくじつ", "らいしゅう"] },
            { "sentence": "祝日_", "answer": "しゅくじつ", "options":["しゅくじつ", "しゅうまつ", "へいじつ", "きょねん"] },
            { "sentence": "平日_", "answer": "へいじつ", "options":["へいじつ", "しゅうまつ", "しゅくじつ", "らいしゅう"] },
            { "sentence": "先週_", "answer": "せんしゅう", "options":["せんしゅう", "こんしゅう", "らいしゅう", "きょねん"] },
            { "sentence": "今週_", "answer": "こんしゅう", "options":["こんしゅう", "せんしゅう", "らいしゅう", "らいねん"] },
            { "sentence": "来週_", "answer": "らいしゅう", "options":["らいしゅう", "こんしゅう", "せんしゅう", "らいねん"] },
            { "sentence": "去年_", "answer": "きょねん", "options":["きょねん", "らいねん", "せんしゅう", "しゅうまつ"] },
            { "sentence": "来年_", "answer": "らいねん", "options":["らいねん", "きょねん", "らいしゅう", "へいじつ"] },
            { "sentence": "げつようび_", "answer": "月曜日", "options":["月曜日", "火曜日", "水曜日", "日曜日"] },
            { "sentence": "かようび_", "answer": "火曜日", "options":["火曜日", "木曜日", "金曜日", "土曜日"] },
            { "sentence": "すいようび_", "answer": "水曜日", "options":["水曜日", "火曜日", "木曜日", "月曜日"] },
            { "sentence": "もくようび_", "answer": "木曜日", "options": ["木曜日", "水曜日", "金曜日", "土曜日"] },
            { "sentence": "きんようび_", "answer": "金曜日", "options":["金曜日", "月曜日", "火曜日", "日曜日"] },
            { "sentence": "どようび_", "answer": "土曜日", "options": ["土曜日", "日曜日", "水曜日", "木曜日"] },
            { "sentence": "にちようび_", "answer": "日曜日", "options":["日曜日", "月曜日", "金曜日", "土曜日"] },
            { "sentence": "しゅうまつ_", "answer": "週末", "options":["週末", "平日", "祝日", "来週"] },
            { "sentence": "しゅくじつ_", "answer": "祝日", "options":["祝日", "週末", "平日", "去年"] },
            { "sentence": "へいじつ_", "answer": "平日", "options":["平日", "週末", "祝日", "来週"] },
            { "sentence": "せんしゅう_", "answer": "先週", "options":["先週", "今週", "来週", "去年"] },
            { "sentence": "こんしゅう_", "answer": "今週", "options":["今週", "先週", "来週", "来年"] },
            { "sentence": "らいしゅう_", "answer": "来週", "options":["来週", "今週", "先週", "来年"] },
            { "sentence": "きょねん_", "answer": "去年", "options":["去年", "来年", "先週", "週末"] },
            { "sentence": "らいねん_", "answer": "来年", "options":["来年", "去年", "来週", "平日"] }
        ],
        "order":[],
        "enemy_surf": 29, 
        "enemy_attack_word": "壓",
        "target":[6, 7],
        "enemy_hp": 140 * (1.5 if save['hard'] else 1),
        "enemy_attack": 20 * (1.5 if save['hard'] else 1),
        "discription": "將正確的星期拖拉至對應的中文意思旁",
    },
    # 19 (MC - Mid Boss "Tenma" - Grand Kanji Exam)
    {
        "question_type": "MC",
        "question":[
            "百", "千", "水", "木", "山", "空", "前", "人", "目", "時", 
            "大きい", "新しい", "行く", "読む", "話す", "月曜日", "日曜日",
            "ひゃく", "せん", "みず", "き", "やま", "そら", "まえ", "ひと", "め", "とき/じ",
            "おおきい", "あたらしい", "いく", "よむ", "はなす", "げつようび", "にちようび"
        ],
        "answer": {
            # Kanji -> Hiragana
            "百": ("ひゃく", ["ひゃく", "せん", "まん", "ひやく"]),
            "千": ("せん", ["せん", "ひゃく", "まん", "ぜん"]),
            "水": ("みず", ["みず", "つき", "つち", "ひ/か"]),
            "木": ("き", ["き", "きん", "ひ/にち", "みず"]),
            "山": ("やま", ["やま", "かわ", "そら", "てん"]),
            "空": ("そら", ["そら", "てん", "あめ", "いし"]),
            "前": ("まえ", ["まえ", "うしろ", "うえ", "なか"]),
            "人": ("ひと",["ひと", "おとこ", "おんな", "め"]),
            "目": ("め",["め", "みみ", "くち", "て"]),
            "時": ("とき/じ",["とき/じ", "いま", "ねん", "あさ"]),
            "大きい": ("おおきい", ["おおきい", "ちいさい", "たかい", "ひくい"]),
            "新しい": ("あたらしい", ["あたらしい", "ふるい", "おおきい", "おおい"]),
            "行く": ("いく", ["いく", "くる", "みる", "きく"]),
            "読む": ("よむ", ["よむ", "かく", "いう", "はなす"]),
            "話す": ("はなす", ["はなす", "いう", "よむ", "やすむ"]),
            "月曜日": ("げつようび",["げつようび", "かようび", "すいようび", "にちようび"]),
            "日曜日": ("にちようび",["にちようび", "げつようび", "きんようび", "どようび"]),

            # Hiragana -> Kanji
            "ひゃく": ("百", ["百", "千", "万", "白"]),
            "せん": ("千", ["千", "百", "万", "前"]),
            "みず": ("水", ["水", "木", "月", "火"]),
            "き": ("木", ["木", "金", "日", "水"]),
            "やま": ("山", ["山", "川", "空", "天"]),
            "そら": ("空", ["空", "天", "雨", "石"]),
            "まえ": ("前", ["前", "後", "上", "中"]),
            "ひと": ("人", ["人", "男", "女", "目"]),
            "め": ("目", ["目", "耳", "口", "手"]),
            "とき/じ": ("時", ["時", "今", "年", "朝"]),
            "おおきい": ("大きい", ["大きい", "小さい", "高い", "低い"]),
            "あたらしい": ("新しい", ["新しい", "古い", "大きい", "多い"]),
            "いく": ("行く", ["行く", "来る", "見る", "聞く"]),
            "よむ": ("読む", ["読む", "書く", "言う", "話す"]),
            "はなす": ("話す", ["話す", "言う", "読む", "休む"]),
            "げつようび": ("月曜日", ["月曜日", "火曜日", "水曜日", "日曜日"]),
            "にちようび": ("日曜日", ["日曜日", "月曜日", "金曜日", "土曜日"])
        },
        "word_size": 36,
        "order":[],
        "enemy_surf": 80,  # Mid Boss (Tenma)
        "enemy_attack_word": "死",
        "target": [20, 25],
        "enemy_hp": 400 * (1.5 if save['hard'] else 1),   # Requires 20 hits to defeat!
        "enemy_attack": 50 * (1.5 if save['hard'] else 1),
        "discription": "中級Boss『天魔』降臨！點擊漢字正確的讀音！",
    },
    # 20 (Sentence Order - Basic A is B)
    {
        "question_type": "Sentence_Order",
        "questions":[
            { 
                "meaning": "我是赤真 (I am Akamasa)", 
                "answer_order": ["わたし", "は", "あかまさ", "です"], 
                "options": ["です", "わたし", "は", "あかまさ", "が", "を"] 
            },
            { 
                "meaning": "這是蘋果 (This is an apple)", 
                "answer_order": ["これ", "は", "りんご", "です"], 
                "options":["りんご", "これ", "は", "です", "それ", "に"] 
            },
            { 
                "meaning": "莉子是精靈 (Riko is an elf)", 
                "answer_order": ["りこ", "は", "エルフ", "です"], 
                "options": ["りこ", "エルフ", "は", "です", "を", "の"] 
            },
            { 
                "meaning": "那是一本書 (That is a book)", 
                "answer_order": ["それ", "は", "ほん", "です"], 
                "options":["ほん", "それ", "は", "です", "あれ", "が"] 
            },
            { 
                "meaning": "明天是星期一 (Tomorrow is Monday)", 
                "answer_order":["あした", "は", "げつようび", "です"], 
                "options":["あした", "は", "げつようび", "です", "きょう", "に"] 
            },
            { 
                "meaning": "我是學生 (I am a student)", 
                "answer_order": ["わたし", "は", "がくせい", "です"], 
                "options": ["わたし", "は", "がくせい", "です", "が", "を"] 
            },
            { 
                "meaning": "那個人是老師 (That person is a teacher)", 
                "answer_order": ["あのひと", "は", "せんせい", "です"], 
                "options": ["あのひと", "は", "せんせい", "です", "この", "に"] 
            },
            { 
                "meaning": "這裡是學校 (Here is a school)", 
                "answer_order": ["ここ", "は", "がっこう", "です"], 
                "options": ["ここ", "は", "がっこう", "です", "そこ", "へ"] 
            },
            { 
                "meaning": "今天是星期天 (Today is Sunday)", 
                "answer_order": ["きょう", "は", "にちようび", "です"], 
                "options": ["きょう", "は", "にちようび", "です", "あした", "が"] 
            },
            { 
                "meaning": "這是水 (This is water)", 
                "answer_order": ["これ", "は", "みず", "です"], 
                "options": ["これ", "は", "みず", "です", "それ", "を"] 
            },
            { 
                "meaning": "那是狗 (That is a dog)", 
                "answer_order": ["それ", "は", "いぬ", "です"], 
                "options": ["それ", "は", "いぬ", "です", "あれ", "ねこ"] 
            },
            { 
                "meaning": "這是我的書 (This is my book)", 
                "answer_order": ["これ", "は", "わたし", "の", "ほん", "です"], 
                "options": ["これ", "は", "わたし", "の", "ほん", "です", "が", "を"] 
            },
            { 
                "meaning": "莉子是女孩子 (Riko is a girl)", 
                "answer_order": ["りこ", "は", "おんなのこ", "です"], 
                "options": ["りこ", "は", "おんなのこ", "です", "おとこのこ", "に"] 
            },
            { 
                "meaning": "赤真是男人 (Akamasa is a man)", 
                "answer_order": ["あかまさ", "は", "おとこ", "です"], 
                "options": ["あかまさ", "は", "おとこ", "です", "おんな", "を"] 
            },
            { 
                "meaning": "那個是山 (That over there is a mountain)", 
                "answer_order": ["あれ", "は", "やま", "です"], 
                "options": ["あれ", "は", "やま", "です", "これ", "かわ"] 
            },
            { 
                "meaning": "這裡是森林 (Here is a forest)", 
                "answer_order": ["ここ", "は", "もり", "です"], 
                "options": ["ここ", "は", "もり", "です", "そこ", "に"] 
            }
        ],
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "基",
        "target": [5, 6],
        "enemy_hp": 100 * (1.5 if save['hard'] else 1), # 5 hits to defeat
        "enemy_attack": 20 * (1.5 if save['hard'] else 1),
        "discription": "將單字拖入上方橫線組成正確句子，完成後按「詠唱」",
    },
    # 21 (Sentence Order - Particles を, に, へ)
    {
        "question_type": "Sentence_Order",
        "questions":[
            { "meaning": "吃蘋果 (Eat an apple)", "answer_order": ["りんご", "を", "たべます"], "options":["りんご", "を", "たべます", "は", "のみます", "が"] },
            { "meaning": "喝水 (Drink water)", "answer_order":["みず", "を", "のみます"], "options":["みず", "を", "のみます", "に", "たべます", "へ"] },
            { "meaning": "去學校 (Go to school)", "answer_order":["がっこう", "に", "いきます"], "options":["がっこう", "に", "いきます", "を", "きます", "で"] },
            { "meaning": "讀書 (Read a book)", "answer_order": ["ほん", "を", "よみます"], "options": ["ほん", "を", "よみます", "が", "かきます", "に"] },
            { "meaning": "回家 (Return home)", "answer_order": ["うち", "に", "かえります"], "options":["うち", "に", "かえります", "を", "でます", "は"] },
            { "meaning": "買肉 (Buy meat)", "answer_order":["にく", "を", "かいます"], "options":["にく", "を", "かいます", "は", "に", "が"] },
            { "meaning": "看電視 (Watch TV)", "answer_order":["テレビ", "を", "みます"], "options":["テレビ", "を", "みます", "に", "へ", "が"] },
            { "meaning": "聽收音機 (Listen to the radio)", "answer_order":["ラジオ", "を", "ききます"], "options":["ラジオ", "を", "ききます", "で", "に", "は"] },
            { "meaning": "買鞋子 (Buy shoes)", "answer_order":["くつ", "を", "かいます"], "options":["くつ", "を", "かいます", "へ", "に", "が"] },
            { "meaning": "去醫院 (Go to the hospital)", "answer_order":["びょういん", "へ", "いきます"], "options":["びょういん", "へ", "いきます", "を", "で", "は"] },
            { "meaning": "喝茶 (Drink tea)", "answer_order":["おちゃ", "を", "のみます"], "options":["おちゃ", "を", "のみます", "に", "が", "へ"] },
            { "meaning": "寫名字 (Write a name)", "answer_order":["なまえ", "を", "かきます"], "options":["なまえ", "を", "かきます", "に", "で", "は"] },
            { "meaning": "見朋友 (Meet a friend)", "answer_order":["ともだち", "に", "あいます"], "options":["ともだち", "に", "あいます", "を", "で", "へ"] },
            { "meaning": "買花 (Buy flowers)", "answer_order":["はな", "を", "かいます"], "options":["はな", "を", "かいます", "に", "が", "へ"] },
            { "meaning": "來到城鎮 (Come to the town)", "answer_order":["まち", "に", "きます"], "options":["まち", "に", "きます", "を", "は", "で"] },
            { "meaning": "乘車 (Ride a car)", "answer_order":["くるま", "に", "のります"], "options":["くるま", "に", "のります", "を", "へ", "が"] },
            { "meaning": "吃魚 (Eat fish)", "answer_order":["さかな", "を", "たべます"], "options":["さかな", "を", "たべます", "に", "で", "は"] },
            { "meaning": "讀報紙 (Read a newspaper)", "answer_order":["しんぶん", "を", "よみます"], "options":["しんぶん", "を", "よみます", "に", "へ", "が"] }
        ],
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "助", # Represents "Particles"
        "target": [6, 7],
        "enemy_hp": 120 * (1.5 if save['hard'] else 1), # 6 hits to defeat
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "將單字拖入上方橫線組成正確句子，完成後按「詠唱」",
    },
    # 22 (Sentence Order - Subject + Object + Verb)
    {
        "question_type": "Sentence_Order",
        "questions":[
            { "meaning": "我吃肉 (I eat meat)", "answer_order":["わたし", "は", "にく", "を", "たべます"], "options":["わたし", "は", "にく", "を", "たべます", "が", "に"] },
            { "meaning": "莉子喝水 (Riko drinks water)", "answer_order": ["りこ", "は", "みず", "を", "のみます"], "options":["りこ", "は", "みず", "を", "のみます", "へ", "で"] },
            { "meaning": "我去學校 (I go to school)", "answer_order":["わたし", "は", "がっこう", "に", "いきます"], "options":["わたし", "は", "がっこう", "に", "いきます", "を", "で"] },
            { "meaning": "老師看書 (The teacher reads a book)", "answer_order":["せんせい", "は", "ほん", "を", "よみます"], "options":["せんせい", "は", "ほん", "を", "よみます", "が", "に"] },
            { "meaning": "赤真買蘋果 (Akamasa buys an apple)", "answer_order": ["あかまさ", "は", "りんご", "を", "かいます"], "options":["あかまさ", "は", "りんご", "を", "かいます", "の", "へ"] },
            { "meaning": "學生寫字 (The student writes characters)", "answer_order":["がくせい", "は", "じ", "を", "かきます"], "options":["がくせい", "は", "じ", "を", "かきます", "に", "の"] },
            { "meaning": "貓看鳥 (The cat looks at the bird)", "answer_order":["ねこ", "は", "とり", "を", "みます"], "options":["ねこ", "は", "とり", "を", "みます", "が", "へ"] },
            { "meaning": "我寫信 (I write a letter)", "answer_order":["わたし", "は", "てがみ", "を", "かきます"], "options":["わたし", "は", "てがみ", "を", "かきます", "に", "で"] },
            { "meaning": "他買車 (He buys a car)", "answer_order":["かれ", "は", "くるま", "を", "かいます"], "options":["かれ", "は", "くるま", "を", "かいます", "が", "へ"] },
            { "meaning": "她看花 (She looks at the flower)", "answer_order":["かのじょ", "は", "はな", "を", "みます"], "options":["かのじょ", "は", "はな", "を", "みます", "に", "の"] },
            { "meaning": "男孩吃麵包 (The boy eats bread)", "answer_order":["おとこのこ", "は", "パン", "を", "たべます"], "options":["おとこのこ", "は", "パン", "を", "たべます", "で", "が"] },
            { "meaning": "女孩喝茶 (The girl drinks tea)", "answer_order":["おんなのこ", "は", "おちゃ", "を", "のみます"], "options":["おんなのこ", "は", "おちゃ", "を", "のみます", "に", "へ"] },
            { "meaning": "我聽音樂 (I listen to music)", "answer_order":["わたし", "は", "おんがく", "を", "ききます"], "options":["わたし", "は", "おんがく", "を", "ききます", "が", "の"] },
            { "meaning": "老師說英語 (The teacher speaks English)", "answer_order":["せんせい", "は", "えいご", "を", "はなします"], "options":["せんせい", "は", "えいご", "を", "はなします", "に", "で"] },
            { "meaning": "莉子使用魔法 (Riko uses magic)", "answer_order":["りこ", "は", "まほう", "を", "つかいます"], "options":["りこ", "は", "まほう", "を", "つかいます", "が", "へ"] },
            { "meaning": "赤真喝藥 (Akamasa drinks medicine)", "answer_order":["あかまさ", "は", "くすり", "を", "のみます"], "options":["あかまさ", "は", "くすり", "を", "のみます", "で", "に"] },
            { "meaning": "我看報紙 (I read the newspaper)", "answer_order":["わたし", "は", "しんぶん", "を", "よみます"], "options":["わたし", "は", "しんぶん", "を", "よみます", "の", "へ"] }
        ],
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "連",
        "target": [7, 8],
        "enemy_hp": 140 * (1.5 if save['hard'] else 1), # 7 hits to defeat\
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "discription": "將單字拖入上方橫線組成正確句子，完成後按「詠唱」",
    },
    # 23 (Sentence Order - Expansion with Time & Location)
    {
        "question_type": "Sentence_Order",
        "questions":[
            { "meaning": "今天我在家 (I am at home today)", "answer_order": ["きょう", "わたし", "は", "うち", "に", "います"], "options":["きょう", "わたし", "は", "うち", "に", "います", "を", "へ"] },
            { "meaning": "昨天吃了蘋果 (Ate an apple yesterday)", "answer_order":["きのう", "りんご", "を", "たべました"], "options":["きのう", "りんご", "を", "たべました", "たべます", "に", "は"] },
            { "meaning": "在學校讀書 (Study at school)", "answer_order":["がっこう", "で", "ほん", "を", "よみます"], "options":["がっこう", "で", "ほん", "を", "よみます", "に", "が"] },
            { "meaning": "明天去森林 (Go to the forest tomorrow)", "answer_order": ["あした", "もり", "へ", "いきます"], "options": ["あした", "もり", "へ", "いきます", "で", "を", "きのう"] },
            { "meaning": "在餐廳吃肉 (Eat meat at the restaurant)", "answer_order":["レストラン", "で", "にく", "を", "たべます"], "options":["レストラン", "で", "にく", "を", "たべます", "に", "は"] },
            { "meaning": "每天早上喝水 (Drink water every morning)", "answer_order":["まいあさ", "みず", "を", "のみます"], "options":["まいあさ", "みず", "を", "のみます", "は", "で", "の"] },
            { "meaning": "昨天莉子買了書 (Riko bought a book yesterday)", "answer_order": ["きのう", "りこ", "は", "ほん", "を", "かいました"], "options":["きのう", "りこ", "は", "ほん", "を", "かいました", "かいます", "で"] },
            { "meaning": "在房間寫字 (Write characters in the room)", "answer_order":["へや", "で", "じ", "を", "かきます"], "options":["へや", "で", "じ", "を", "かきます", "に", "へ"] },
            { "meaning": "今天在公園玩 (Play in the park today)", "answer_order":["きょう", "こうえん", "で", "あそびます"], "options":["きょう", "こうえん", "で", "あそびます", "に", "を"] },
            { "meaning": "下週去東京 (Go to Tokyo next week)", "answer_order":["らいしゅう", "とうきょう", "へ", "いきます"], "options":["らいしゅう", "とうきょう", "へ", "いきます", "で", "を"] },
            { "meaning": "每天在圖書館學習 (Study at the library everyday)", "answer_order":["まいにち", "としょかん", "で", "べんきょうします"], "options":["まいにち", "としょかん", "で", "べんきょうします", "に", "は"] },
            { "meaning": "昨天在海裡游泳 (Swam in the sea yesterday)", "answer_order":["きのう", "うみ", "で", "およぎました"], "options":["きのう", "うみ", "で", "およぎました", "に", "およぎます"] },
            { "meaning": "明天在電影院看電影 (Watch a movie at the cinema tomorrow)", "answer_order":["あした", "えいがかん", "で", "えいが", "を", "みます"], "options":["あした", "えいがかん", "で", "えいが", "を", "みます", "に"] },
            { "meaning": "今晚在家看電視 (Watch TV at home tonight)", "answer_order":["こんや", "うち", "で", "テレビ", "を", "みます"], "options":["こんや", "うち", "で", "テレビ", "を", "みます", "へ"] },
            { "meaning": "去年我去了日本 (I went to Japan last year)", "answer_order":["きょねん", "わたし", "は", "にほん", "へ", "いきました"], "options":["きょねん", "わたし", "は", "にほん", "へ", "いきました", "で"] },
            { "meaning": "每晚我聽音樂 (I listen to music every night)", "answer_order":["まいばん", "わたし", "は", "おんがく", "を", "ききます"], "options":["まいばん", "わたし", "は", "おんがく", "を", "ききます", "で", "に"] },
            { "meaning": "早上在咖啡廳喝咖啡 (Drink coffee at a cafe in the morning)", "answer_order":["あさ", "カフェ", "で", "コーヒー", "を", "のみます"], "options":["あさ", "カフェ", "で", "コーヒー", "を", "のみます", "に", "が"] }
        ],
        "order":[],
        "enemy_surf": 9,
        "enemy_attack_word": "完",
        "target": [8, 9],
        "enemy_hp": 160 * (1.5 if save['hard'] else 1), # 8 hits to defeat
        "enemy_attack": 40 * (1.5 if save['hard'] else 1),
        "discription": "將單字拖入上方橫線組成正確句子，完成後按「詠唱」",
    },

    #24 (masu to ru)
    {
        "question_type": "input",
        "question": "verb_masu",
        "answer": "verb_ru",
        "enemy_surf": 29,
        "counter": 0,
        "enemy_attack_word": "打",
        "target": [7, 10],
        "enemy_hp": 140 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\nます形 → 辞書形",
    },
    # 25 (Input - Ru to Te Form)
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_te",
        "enemy_surf": 9,
        "counter": 0,
        "enemy_attack_word": "連",
        "target": [9, 11], # 9 hits for 3 stars
        "enemy_hp": 180 * (1.5 if save['hard'] else 1),
        "enemy_attack": 30 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → て形",
    },
    # 26 (Input - Ru to Nai Form)
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_nai",
        "enemy_surf": 9,
        "counter": 0,
        "enemy_attack_word": "無",
        "target":[10, 12], # 10 hits for 3 stars
        "enemy_hp": 200 * (1.5 if save['hard'] else 1),
        "enemy_attack": 40 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → ない形 (否定)",
    },
    # 27 (Input - Ru to Ta Form)
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_ta",
        "enemy_surf": 9,
        "counter": 0,
        "enemy_attack_word": "極",
        "target": [11, 13], # 11 hits for 3 stars
        "enemy_hp": 220 * (1.5 if save['hard'] else 1),
        "enemy_attack": 40 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → た形 (過去式)",
    },
    # 28 (Input - Ru to Kanou Form / Boss Fight)
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_kanou",
        "enemy_surf": 81,  # Demon Dragon Boss Sprite
        "counter": 0,
        "enemy_attack_word": "滅",
        "target": [20, 25], # 20 hits required! A true test of endurance.
        "enemy_hp": 400 * (1.5 if save['hard'] else 1),
        "enemy_attack": 50 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "【魔龍降臨】以鍵盤輸入羅馬拼音後，按Enter\n辞書形 → 可能形 (能/可以)",
    },
    # 29 chapter 4 Bad Ending (Stage 29)
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_ro",
        "enemy_surf": 83,
        "counter": 0,
        "enemy_attack_word": "殺",
        "target": [8, 10],
        "enemy_hp": 260 * (1.5 if save['hard'] else 1),
        "enemy_attack": 50 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → 命令形 (強制...)",
    },
    #30
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_na",
        "enemy_surf": 84,
        "counter": 0,
        "enemy_attack_word": "怨",
        "target": [10, 12],
        "enemy_hp": 280 * (1.5 if save['hard'] else 1),
        "enemy_attack": 60 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → 禁止形 (不准...)",
    },
    #31
    {
        "question_type": "Sentence_Order",
        "questions":[
            { "meaning": "我殺了莉子 (I killed Riko)", "answer_order":["わたし", "は", "りこ", "を", "ころしました"], "options":["わたし", "は", "りこ", "を", "ころしました", "が", "に"] },
            { "meaning": "甚麼都沒有 (There is nothing)", "answer_order": ["なにも", "ありません"], "options":["なにも", "ありません", "あります", "は", "が"] },
            { "meaning": "世界將會毀滅 (The world will be destroyed)", "answer_order": ["せかい", "は", "ほろびます"], "options": ["せかい", "は", "ほろびます", "を", "に"] },
            { "meaning": "不要死 (Don't die)", "answer_order":["しなないで", "ください"], "options":["しなないで", "ください", "しにます", "は", "で"] },
            { "meaning": "我是魔王 (I am the Demon King)", "answer_order": ["わたし", "は", "まおう", "です"], "options":["わたし", "は", "まおう", "です", "が", "を"] },
            { "meaning": "已經太遲了 (It is already too late)", "answer_order": ["もう", "おそい", "です"], "options": ["もう", "おそい", "です", "はやい", "は", "が"] },
            { "meaning": "心裡很痛 (My heart hurts)", "answer_order": ["こころ", "が", "いたい", "です"], "options": ["こころ", "が", "いたい", "です", "を", "は"] },
            { "meaning": "人類很愚蠢 (Humans are foolish)", "answer_order": ["にんげん", "は", "おろか", "です"], "options": ["にんげん", "は", "おろか", "です", "を", "に", "かしこい"] },
            { "meaning": "我不會原諒你 (I won't forgive you)", "answer_order": ["あなた", "を", "ゆるしません"], "options": ["あなた", "を", "ゆるしません", "ゆるします", "が", "に"] },
            { "meaning": "全部破壞吧 (Destroy everything)", "answer_order": ["すべて", "を", "こわします"], "options": ["すべて", "を", "こわします", "に", "は", "つくります"] },
            { "meaning": "沒人能救我 (No one can save me)", "answer_order": ["だれも", "わたし", "を", "たすけません"], "options": ["だれも", "わたし", "を", "たすけません", "が", "に", "たすけます"] },
            { "meaning": "這是絕望 (This is despair)", "answer_order": ["これ", "は", "ぜつぼう", "です"], "options": ["これ", "は", "ぜつぼう", "です", "きぼう", "が", "を"] },
            { "meaning": "血流不止 (The blood won't stop flowing)", "answer_order": ["ち", "が", "とまりません"], "options": ["ち", "が", "とまりません", "を", "は", "とまります"] },
            { "meaning": "聽不見聲音 (I can't hear any sound)", "answer_order": ["おと", "が", "きこえません"], "options": ["おと", "が", "きこえません", "を", "は", "きこえます"] },
            { "meaning": "我獨自一人 (I am all alone)", "answer_order": ["わたし", "は", "ひとりぼっち", "です"], "options": ["わたし", "は", "ひとりぼっち", "です", "ふたり", "を", "が"] },
            { "meaning": "為什麼會變成這樣？ (Why did it turn out like this?)", "answer_order": ["なぜ", "こう", "なりました", "か"], "options": ["なぜ", "こう", "なりました", "か", "は", "を", "なります"] },
            { "meaning": "結束了 (It's over)", "answer_order": ["おわり", "です"], "options": ["おわり", "です", "はじまり", "は", "が"] }
        ],
        "order":[],
        "enemy_surf": 85,
        "enemy_attack_word": "恨",
        "target": [4, 5],
        "enemy_hp": 300 * (1.5 if save['hard'] else 1),
        "enemy_attack": 70 * (1.5 if save['hard'] else 1),
        "discription": "將單字拖入上方橫線組成正確句子，完成後按「詠唱」",
    },
    #32
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_ba",
        "enemy_surf": 86,
        "counter": 0,
        "enemy_attack_word": "悔",
        "target":[12, 14],
        "enemy_hp": 320 * (1.5 if save['hard'] else 1),
        "enemy_attack": 75 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → 條件形 (ば形)",
    },
    #33
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_saseru_rareru",
        "enemy_surf": 82,
        "counter": 0,
        "enemy_attack_word": "終",
        "target": [20, 25],
        "enemy_hp": 500 * (1.5 if save['hard'] else 1),
        "enemy_attack": 80 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "【魔王降臨】以鍵盤輸入羅馬拼音後，按Enter\n辞書形 → 使役被動形 (被迫...)",
    },
    # 34 chapter 4 True Ending (Stage 34)
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_ikou",
        "enemy_surf": 83,
        "counter": 0,
        "enemy_attack_word": "炎",
        "target": [8, 10],
        "enemy_hp": 260 * (1.5 if save['hard'] else 1),
        "enemy_attack": 50 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → 意向形 (一起...吧！)",
    },
    #35
    {
        "question_type": "Sentence_Order",
         "questions":[
            { "meaning": " (Read a book in the forest today)", "answer_order":["きょう", "もり", "で", "ほん", "を", "よみます"], "options":["きょう", "もり", "で", "ほん", "を", "よみます", "に", "が"] },
            { "meaning": "每天早上吃蘋果 (Eat apples every morning)", "answer_order":["まいあさ", "りんご", "を", "たべます"], "options":["まいあさ", "りんご", "を", "たべます", "に", "は"] },
            { "meaning": "我不吃肉 (I do not eat meat)", "answer_order": ["わたし", "は", "にく", "を", "たべません"], "options":["わたし", "は", "にく", "を", "たべません", "たべます", "が"] },
            { "meaning": "明天去學校 (Go to school tomorrow)", "answer_order": ["あした", "がっこう", "に", "いきます"], "options":["あした", "がっこう", "に", "いきます", "で", "を"] },
            { "meaning": "和莉子一起戰鬥 (Fight together with Riko)", "answer_order": ["りこ", "と", "いっしょに", "たたかいます"], "options": ["りこ", "と", "いっしょに", "たたかいます", "が", "を", "にげます"] },
            { "meaning": "我們不會輸 (We will not lose)", "answer_order": ["わたしたち", "は", "まけません"], "options": ["わたしたち", "は", "まけません", "を", "に", "かちます"] },
            { "meaning": "相信朋友 (Believe in friends)", "answer_order": ["ともだち", "を", "しんじます"], "options": ["ともだち", "を", "しんじます", "に", "は", "うたがいます"] },
            { "meaning": "守護這個世界 (Protect this world)", "answer_order": ["この", "せかい", "を", "まもります"], "options": ["この", "せかい", "を", "まもります", "あの", "に", "こわします"] },
            { "meaning": "用魔法打倒敵人 (Defeat the enemy with magic)", "answer_order": ["まほう", "で", "てき", "を", "たおします"], "options": ["まほう", "で", "てき", "を", "たおします", "に", "は", "が"] },
            { "meaning": "尋找新的武器 (Search for a new weapon)", "answer_order": ["あたらしい", "ぶき", "を", "さがします"], "options": ["あたらしい", "ぶき", "を", "さがします", "ふるい", "に", "が"] },
            { "meaning": "絕對不放棄 (Absolutely will not give up)", "answer_order": ["ぜったいに", "あきらめません"], "options": ["ぜったいに", "あきらめません", "あきらめます", "を", "に"] },
            { "meaning": "明天向城堡出發 (Depart for the castle tomorrow)", "answer_order": ["あした", "しろ", "へ", "しゅっぱつします"], "options": ["あした", "しろ", "へ", "しゅっぱつします", "きのう", "を", "で"] },
            { "meaning": "我們是冒險者 (We are adventurers)", "answer_order": ["わたしたち", "は", "ぼうけんしゃ", "です"], "options": ["わたしたち", "は", "ぼうけんしゃ", "です", "を", "が", "に"] },
            { "meaning": "買強力的裝備 (Buy powerful equipment)", "answer_order": ["つよい", "そうび", "を", "かいます"], "options": ["つよい", "そうび", "を", "かいます", "よわい", "に", "で"] },
            { "meaning": "喝回復藥水 (Drink a healing potion)", "answer_order": ["かいふくやく", "を", "のみます"], "options": ["かいふくやく", "を", "のみます", "たべます", "に", "が"] },
            { "meaning": "拯救大家 (Save everyone)", "answer_order": ["みんな", "を", "たすけます"], "options": ["みんな", "を", "たすけます", "が", "に", "ころします"] }
        ],
        "order":[],
        "enemy_surf": 84,
        "enemy_attack_word": "風",
        "target": [4, 5],
        "enemy_hp": 300 * (1.5 if save['hard'] else 1),
        "enemy_attack": 60 * (1.5 if save['hard'] else 1),
        "discription": "將單字拖入上方橫線組成正確句子，完成後按「詠唱」",
    },
    #36
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_kanou",
        "enemy_surf": 85,
        "counter": 0,
        "enemy_attack_word": "冰",
        "target":[10, 12],
        "enemy_hp": 320 * (1.5 if save['hard'] else 1),
        "enemy_attack": 65 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → 可能形 (能/可以)",
    },
    #37
    {
        "question_type": "input",
        "question": "verb_ru",
        "answer": "verb_te",
        "enemy_surf": 86,
        "counter": 0,
        "enemy_attack_word": "壁",
        "target": [12, 14],
        "enemy_hp": 340 * (1.5 if save['hard'] else 1),
        "enemy_attack": 70 * (1.5 if save['hard'] else 1),
        "curr_qs": None,
        "discription": "以鍵盤輸入答案的羅馬拼音後，按Enter\n辞書形 → て形 (連續行動)",
    },
    #38
    {
        "question_type": "Sentence_Order",
         "questions":[
            { "meaning": "這是最後的戰鬥 (This is the final battle)", "answer_order": ["これ", "が", "さいご", "の", "たたかい", "です"], "options": ["これ", "が", "さいご", "の", "たたかい", "です", "は", "を", "さいしょ"] },
            { "meaning": "發動最強的魔法 (Activate the strongest magic)", "answer_order": ["さいきょう", "の", "まほう", "を", "はつどうします"], "options": ["さいきょう", "の", "まほう", "を", "はつどうします", "が", "に", "さいじゃく"] },
            { "meaning": "我一定會打倒魔王 (I will definitely defeat the Demon King)", "answer_order": ["わたし", "は", "かならず", "まおう", "を", "たおします"], "options": ["わたし", "は", "かならず", "まおう", "を", "たおします", "が", "に", "まけます"] },
            { "meaning": "和大家一起回家 (Return home together with everyone)", "answer_order": ["みんな", "と", "いっしょに", "かえります"], "options": ["みんな", "と", "いっしょに", "かえります", "を", "が", "いきます"] },
            { "meaning": "你的野心到此為止了 (Your ambition ends here)", "answer_order": ["おまえ", "の", "やぼう", "は", "ここ", "まで", "です"], "options": ["おまえ", "の", "やぼう", "は", "ここ", "まで", "です", "が", "を", "そこ"] },
            { "meaning": "我們的羈絆是無限的 (Our bond is infinite)", "answer_order": ["わたしたち", "の", "きずな", "は", "むげん", "です"], "options": ["わたしたち", "の", "きずな", "は", "むげん", "です", "が", "を", "ゆうげん"] },
            { "meaning": "迎接光明的未來 (Welcome a bright future)", "answer_order": ["あかるい", "みらい", "を", "むかえます"], "options": ["あかるい", "みらい", "を", "むかえます", "くらい", "に", "が"] },
            { "meaning": "舉起傳說的劍 (Raise the legendary sword)", "answer_order": ["でんせつ", "の", "つるぎ", "を", "かかげます"], "options": ["でんせつ", "の", "つるぎ", "を", "かかげます", "が", "に", "おとします"] },
            { "meaning": "勇者不畏懼黑暗 (A hero does not fear the dark)", "answer_order": ["ゆうしゃ", "は", "やみ", "を", "おそれません"], "options": ["ゆうしゃ", "は", "やみ", "を", "おそれません", "が", "に", "ひかり"] },
            { "meaning": "奇蹟一定會發生 (A miracle will definitely happen)", "answer_order": ["きせき", "は", "かならず", "おきます"], "options": ["きせき", "は", "かならず", "おきます", "を", "に", "おきません"] },
            { "meaning": "為了和平而戰 (Fight for peace)", "answer_order": ["へいわ", "の", "ために", "たたかいます"], "options": ["へいわ", "の", "ために", "たたかいます", "が", "を", "にげます"] },
            { "meaning": "把力量借給我 (Lend me your power)", "answer_order": ["わたし", "に", "ちから", "を", "かして", "ください"], "options": ["わたし", "に", "ちから", "を", "かして", "ください", "が", "で", "かえして"] },
            { "meaning": "突破極限 (Break through the limits)", "answer_order": ["げんかい", "を", "とっぱします"], "options": ["げんかい", "を", "とっぱします", "が", "に", "あきらめます"] },
            { "meaning": "絕對不會逃跑 (Absolutely will not run away)", "answer_order": ["ぜったいに", "にげません"], "options": ["ぜったいに", "にげません", "にげます", "を", "に"] },
            { "meaning": "使出全部的力量 (Put forth all power)", "answer_order": ["すべて", "の", "ちから", "を", "だします"], "options": ["すべて", "の", "ちから", "を", "だします", "が", "に", "かくします"] },
            { "meaning": "創造新的傳說 (Create a new legend)", "answer_order": ["あたらしい", "でんせつ", "を", "つくります"], "options": ["あたらしい", "でんせつ", "を", "つくります", "ふるい", "が", "に"] },
            { "meaning": "我感謝莉子 (I thank Riko)", "answer_order": ["わたし", "は", "りこ", "に", "かんしゃします"], "options": ["わたし", "は", "りこ", "に", "かんしゃします", "を", "で", "あやまります"] }
        ],
        "order":[],
        "enemy_surf": 82,
        "enemy_attack_word": "滅",
        "target": [5, 6],
        "enemy_hp": 800 * (1.5 if save['hard'] else 1), # Demon King has very high HP!
        "enemy_attack": 80 * (1.5 if save['hard'] else 1),
        "discription": "【魔王降臨】將單字拖入橫線組成句子，發動最終詠唱！",
    }
    ]
    return battle_detail



battle_detail_backup = deepcopy(battle_detail)

player_hp = 100
enemy_hp = 100
question_num = 0

# achievement related data
idle_times = 0
recover_times = 0
damage_taken_times = 0
attack_times = 0
click_times = 0

achievement_stack = []
    

s = pygame.Surface((WIDTH,HEIGHT))
s.fill((0,0,0))
br = transform_scale([4])[0]

print(br)
# main game loop
while running: 
    if game_state == "menu":

        # BG image
        screen.blit(images[25 if save["star"][-1]>0 or save['hard'] else 0], (0, 0))

        # Title text
        r = images[1].get_rect()
        r.center = screen.get_rect().center
        screen.blit(images[1], r)

        if save["star"][-1] > 0:
            pygame.draw.rect(screen, [186, 148, 45], transform_scale([570, 550, 300, 50]), border_radius=br)
            pygame.draw.rect(screen, [0, 0, 0], transform_scale([570, 550, 300, 50]), br, br)
            text(screen, "輪迴", [0, 0, 0], 30, transform_scale([570+150, 550+25]), "center")

        pygame.draw.rect(screen, [186, 148, 45], transform_scale([570, 620, 300, 50]), border_radius=br)
        pygame.draw.rect(screen, [0, 0, 0], transform_scale([570, 620, 300, 50]), br, br)
        text(screen, "繼續" if save["unlock"][1] or save['hard'] else "新遊戲", [0, 0, 0], 30, transform_scale([570+150, 620+25]), "center")

        pygame.draw.rect(screen, [186, 148, 45], transform_scale([570, 690, 300, 50]), border_radius=br)
        pygame.draw.rect(screen, [0, 0, 0], transform_scale([570, 690, 300, 50]), br, br)
        text(screen, "設定", [0, 0, 0], 30, transform_scale([570+150, 690+25]), "center")

        pygame.draw.rect(screen, [186, 148, 45], transform_scale([570, 760, 300, 50]), border_radius=br)
        pygame.draw.rect(screen, [0, 0, 0], transform_scale([570, 760, 300, 50]), br, br)
        text(screen, "成就", [0, 0, 0], 30, transform_scale([570+150, 760+25]), "center")

        pygame.draw.rect(screen, [186, 148, 45], transform_scale([570, 830, 300, 50]), border_radius=br)
        pygame.draw.rect(screen, [0, 0, 0], transform_scale([570, 830, 300, 50]), br, br)
        text(screen, "退出", [0, 0, 0], 30, transform_scale([570+150, 830+25]), "center")

        
        if(time != 0):
            time += 1
            s.set_alpha(int(time/fps/1*255))
            screen.blit(s, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if click_check(pygame.mouse.get_pos(), transform_scale([570, 550, 300, 50])) and save["star"][-1] > 0:  # new round
                        if (time == 0):
                            play_sfx("click")
                            time += 1
                            menu_action = "start"
                            save.update({
                                'unlock': [True] + [False]*38,
                                'star': [0]*39,
                                'current_stage': 0,
                                'equipt': [7, 8],  # weapon, equiptment. 7, 8 mean empty. number follow 'obtain' index
                                'obtain_w_n': 2,
                                'obtain_e_n': 2,
                                'last_play': [0, 0], # stage_number, continus_times
                                'hard': True,
                                'chosen_path': 34,
                            })
                            save["obtain"][4] = False
                            save["obtain"][5] = False
                            save["obtain"][6] = False
                            battle_detail = reload_battle_detail()
                            if not(save["achievement"][25]):
                                save["achievement"][25] = True
                                achievement_stack.append([25, fps])
                            if (not(save["achievement"][29])):
                                if(sum(save["achievement"]) == 29):
                                    save["achievement"][29] = True
                                    achievement_stack.append([29, fps])
                    if click_check(pygame.mouse.get_pos(), transform_scale([570, 620, 300, 50])):  #start
                        if (time == 0):
                            play_sfx("click")
                            time += 1
                            menu_action = "start"
                    if click_check(pygame.mouse.get_pos(), transform_scale([570, 690, 300, 50])):  #option
                        if (time == 0):
                            play_sfx("click")
                            play_sfx("click")
                            time += 1
                            menu_action = "option"
                    if click_check(pygame.mouse.get_pos(), transform_scale([570, 760, 300, 50])):  #option
                        if (time == 0):
                            play_sfx("click")
                            time += 1
                            menu_action = "achievement"
                    if click_check(pygame.mouse.get_pos(), transform_scale([570, 830, 300, 50])):  #exit
                        if (time == 0):
                            time += 1
                            menu_action = "exit"
                            

        # enter game
        if(time > fps*1):
            if(menu_action == "start"):
                if save["unlock"][1]:
                    game_state = "select_world"
                    selecting_weapon = False
                    selecting_equiptment = False
                    time=0
                else:
                    game_state = "story"
                    story_num = 0
                    dialog_num = 0
                    time = 0
            elif(menu_action == "exit"):
                running = False
            else:
                game_state = menu_action
                time=0
        if(len(achievement_stack)>0):
            draw_achievemet_stack()
                    
    if game_state == "story":
        # end story
        if dialog_num == len(dialog[story_num]):
            battle_detail = deepcopy(battle_detail_backup)
            time = 0
            idle_times = 0
            recover_times = 0
            damage_taken_times = 0
            attack_times = 0
            click_times = 0
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
            
            elif battle_detail[stage]["question_type"] == "Sentence_Order":
                battle_detail[stage]["order"] = list(range(len(battle_detail[stage]["questions"])))
                random.shuffle(battle_detail[stage]["order"])
                
                # Initialize variables specific to this mode
                draggable_rects.clear() 
                draggable_rects_initial_pos.clear()
                current_sentence_indices = [] # Important for the new logic
                
                is_dragging = False
                dragged_item_index = -1
                action = None 
                question_num = 0
                correct = None
            for event in pygame.event.get():
                # allow close game
                if event.type == pygame.QUIT:
                    running = False
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

            # back button
            pygame.draw.rect(screen, [186, 148, 45], transform_scale([40, 40, 80, 80]), border_radius=br)
            pygame.draw.rect(screen, [0, 0, 0], transform_scale([40, 40, 80, 80]), br, br)
            text(screen, "返回", [0, 0, 0], 25, transform_scale([80, 80]), "center")

            if stage == 28 and dialog_num == len(dialog[28]) - 1:
                choice_1_rect = pygame.Rect(transform_scale([220, 450, 400, 100]))
                choice_2_rect = pygame.Rect(transform_scale([820, 450, 400, 100]))
                
                pygame.draw.rect(screen, [150, 50, 50], choice_1_rect, border_radius=10)
                pygame.draw.rect(screen,[0, 0, 0], choice_1_rect, 3, 10)
                text(screen, "殺死莉子獲得力量",[255, 255, 255], 36, choice_1_rect.center, "center")
                
                pygame.draw.rect(screen, [50, 150, 50], choice_2_rect, border_radius=10)
                pygame.draw.rect(screen,[0, 0, 0], choice_2_rect, 3, 10)
                text(screen, "憑自己的力量迎戰", [255, 255, 255], 36, choice_2_rect.center, "center")

            #  effect
            if (dialog[story_num][dialog_num][0] == 1.1):
                if(effect_time > 0 and effect_time < fps*2):
                    effect_time += 1
                    text_sp(screen, "あ", (120, 0, 0), 200, [WIDTH/2, HEIGHT/2], int((fps*2-effect_time)/(fps*2)*255), "center")
                elif(effect_time >= fps*2):
                    effect_time = 0
            elif (dialog[story_num][dialog_num][0] == 2.1):
                if(effect_time > 0 and effect_time < fps*2):
                    effect_time += 1
                    text_sp(screen, "か", (120, 255, 120), 200, transform_scale([220, 520]), int((fps*2-effect_time)/(fps*2)*255), "center")
                elif(effect_time >= fps*2):
                    effect_time = 0
            elif (effect_time != 0):
                effect_time = 0

            if(time != 0):
                time += 1
                s.set_alpha(int(time/fps/1*255))
                screen.blit(s, (0,0))
            


            
            for event in pygame.event.get():
                # allow close game
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        
                        # Process choices if on Stage 28 choice screen
                        if stage == 28 and dialog_num == len(dialog[28]) - 1:
                            choice_1_rect = pygame.Rect(transform_scale([220, 450, 400, 100]))
                            choice_2_rect = pygame.Rect(transform_scale([820, 450, 400, 100]))
                            if click_check(pos, choice_1_rect):
                                play_sfx("click")
                                save["chosen_path"] = 29
                                write()
                                dialog_num += 1
                            elif click_check(pos, choice_2_rect):
                                play_sfx("click")
                                save["chosen_path"] = 34
                                write()
                                dialog_num += 1
                            elif click_check(pos, transform_scale([40, 40, 80, 80])):
                                if time == 0:
                                    play_sfx("click")
                                    time += 1
                                    menu_action = "back"
                        else:
                            if click_check(pygame.mouse.get_pos(), transform_scale([1111, 35, 310, 80])):
                                # skip button
                                if stage == 28:
                                    dialog_num = len(dialog[story_num]) - 1 # Stop at choice
                                else:
                                    dialog_num = len(dialog[story_num])
                            elif click_check(pygame.mouse.get_pos(), transform_scale([40, 40, 80, 80])):
                                if(time == 0):
                                    time += 1
                                    menu_action = "back"
                            else:
                                # next sentence
                                dialog_num += 1
                                if dialog_num != len(dialog[story_num]):
                                    # effect list
                                    if dialog[story_num][dialog_num][0] == 1.1 or dialog[story_num][dialog_num][0] == 2.1:
                                        effect_time = 1
                                        menu_action = "none"
            # enter game
            if(time > fps*1 and menu_action == "back"):
                game_state = "menu"
                time=0

        if(len(achievement_stack)>0):
            draw_achievemet_stack()

    if game_state == "playing":
        if battle_detail[stage]["question_type"] == "MC":
            # BG image
            draw_story_bg(stage)

            # right character
            screen.blit(pygame.transform.flip(images[4], flip_x=True, flip_y=False), transform_scale([959, 263]))
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([1130, 0, 310, 80]))
            text(screen, "HP", (0, 0, 0), 24, transform_scale([1158, 22]))
            pygame.draw.rect(screen, (0, 0, 0), transform_scale([1209, 34, 204, 13]))
            pygame.draw.rect(screen, (255, 0, 0), transform_scale([1209, 34, player_hp/100*204, 13]))
            

            # left enemy
            enemy = screen.blit(pygame.transform.flip(images[battle_detail[stage]["enemy_surf"]], flip_x=True, flip_y=False), transform_scale([-51, 100]))
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([0, 0, 310, 80]))
            text(screen, "HP", (0, 0, 0), 24, transform_scale([28, 22]))
            pygame.draw.rect(screen, (0, 0, 0), transform_scale([79, 34, 204, 13]))
            pygame.draw.rect(screen, (255, 0, 0), transform_scale([79, 34, enemy_hp/battle_detail[stage]["enemy_hp"]*204, 13]))

            # discription
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([320, 0, 800, 80]))
            if(action == None):
                text(screen, "選擇行動", (20, 20, 20), transform_scale([35])[0], transform_scale([720, 48]), "center")
            else:
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

            idle_times += 1



            for event in pygame.event.get():
                # allow close game
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        if action == "attack" or action == "recover":
                            if time == 0:
                                if click_check(pos, transform_scale(list(enemy))):
                                    click_times += 1
                                    enemy_hp = max(0, enemy_hp-1)
                                    if enemy_hp <= 0:
                                        play_sfx("win")
                                        time = -1*fps
                                        if (len(battle_detail[stage]["order"]) <= battle_detail[stage]["target"][0]):
                                            save["star"][stage] = 3
                                            if(not(save["achievement"][3])):
                                                save["achievement"][3] = True
                                                achievement_stack.append([3, fps])
                                        elif (len(battle_detail[stage]["order"]) <= battle_detail[stage]["target"][1]):
                                            if save["star"][stage] < 2:
                                                save["star"][stage] = 2
                                        else:
                                            if save["star"][stage] < 1:
                                                save["star"][stage] = 1
                                        if save["current_stage"] == 28:
                                            save["unlock"][save.get("chosen_path", 34)] = True
                                        elif len(save["unlock"])>save["current_stage"]+1:
                                            save["unlock"][save["current_stage"]+1]=True
                                        end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage)
                                        write()
                                        game_state = "win"
                                if click_check(pos, transform_scale([407, 729, 194, 94])):
                                    time = 1
                                    idle_times = 0
                                    if battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][0] == battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][0]:
                                        correct = True
                                    else:
                                        correct = False
                                elif click_check(pos, transform_scale([840, 729, 194, 94])):
                                    time = 1
                                    idle_times = 0
                                    if battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][1] == battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][0]:
                                        correct = True
                                    else:
                                        correct = False
                                elif click_check(pos, transform_scale([407, 842, 194, 94])):
                                    time = 1
                                    idle_times = 0
                                    if battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][2] == battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][0]:
                                        correct = True
                                    else:
                                        correct = False
                                elif click_check(pos, transform_scale([840, 842, 194, 94])):
                                    time = 1
                                    idle_times = 0
                                    if battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][3] == battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][0]:
                                        correct = True
                                    else:
                                        correct = False
                        else:
                            if click_check(pos, transform_scale([407, 729, 194, 207])):
                                idle_times = 0
                                action = "attack"
                            elif click_check(pos, transform_scale([840, 729, 194, 207])):
                                idle_times = 0
                                recover_times += 1
                                action = "recover"

            if correct == True:
                if action == "attack":
                    if time == 1: play_sfx("attack")
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]][0], (120, 0, 0), 200, transform_scale([220, 330]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    if time == 0:
                        attack_times += 1
                        enemy_hp -= 20*scale[save["equipt"][0]] if not(god_mod) else 9999
                        correct = None
                        if stage == 0:
                            action = "attack"
                        else:
                            action = None
                        question_num += 1
                        if enemy_hp <= 0:
                            play_sfx("win")
                            time = -1*fps
                            if (len(battle_detail[stage]["order"]) <= battle_detail[stage]["target"][0]):
                                save["star"][stage] = 3
                                if(not(save["achievement"][3])):
                                    save["achievement"][3] = True
                                    achievement_stack.append([3, fps])
                            elif (len(battle_detail[stage]["order"]) <= battle_detail[stage]["target"][1]):
                                if save["star"][stage] < 2:
                                    save["star"][stage] = 2
                            else:
                                if save["star"][stage] < 1:
                                    save["star"][stage] = 1
                            if save["current_stage"] == 28:
                                save["unlock"][save.get("chosen_path", 34)] = True
                            elif len(save["unlock"])>save["current_stage"]+1:
                                save["unlock"][save["current_stage"]+1]=True
                            end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage)
                            write()
                            game_state = "win"
                        else:
                            temp = random.randint(0, len(battle_detail[stage]["question"])-1)
                            while temp == battle_detail[stage]["order"][-1]:
                                temp = random.randint(0, len(battle_detail[stage]["question"])-1)
                            battle_detail[stage]["order"].append(temp)
                            random.shuffle(battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1])
                elif action == "recover":
                    if time == 1: play_sfx("heal")
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
                    if time == 1:                     # <--- ADD THESE 3 LINES
                        #play_sfx("error")             # <---
                        play_sfx("damage") 
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, battle_detail[stage]["enemy_attack_word"], (120, 0, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    if time == 0:
                        attack_times += 1
                        player_hp -= round(battle_detail[stage]["enemy_attack"] * scale[save["equipt"][1]]/100)
                        damage_taken_times += 1
                        correct = None
                        if stage == 0:
                            action = "attack"
                        else:
                            action = None
                        question_num += 1
                        if player_hp <= 0:
                            play_sfx("lose")
                            time = -1*fps
                            end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage)
                            game_state = "lose"
                        else:
                            temp = random.randint(0, len(battle_detail[stage]["question"])-1)
                            while temp == battle_detail[stage]["order"][-1]:
                                temp = random.randint(0, len(battle_detail[stage]["question"])-1)
                            battle_detail[stage]["order"].append(temp)
                            random.shuffle(battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1])
                elif action == "recover":
                    if time == 1:                     # <--- ADD THESE 3 LINES
                        #play_sfx("error")             # <---
                        play_sfx("damage") 
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]][0], (120, 255, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                        text_sp(screen, "╳", (100, 0, 0), transform_scale([250])[0], transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    if time == 0:
                        player_hp -= 10
                        damage_taken_times += 1
                        correct = None
                        action = None
                        question_num += 1
                        if player_hp <= 0:
                            play_sfx("lose")
                            time = -1*fps
                            end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage)
                            game_state = "lose"
                        else:
                            temp = random.randint(0, len(battle_detail[stage]["question"])-1)
                            while temp == battle_detail[stage]["order"][-1]:
                                temp = random.randint(0, len(battle_detail[stage]["question"])-1)
                            battle_detail[stage]["order"].append(temp)
                            random.shuffle(battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1])

        elif battle_detail[stage]["question_type"] == "Drag":
            # BG image
            draw_story_bg(stage)

            # right character
            screen.blit(pygame.transform.flip(images[4], flip_x=True, flip_y=False), transform_scale([959, 263]))
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([1130, 0, 310, 80]))
            text(screen, "HP", (0, 0, 0), 24, transform_scale([1158, 22]))
            pygame.draw.rect(screen, (0, 0, 0), transform_scale([1209, 34, 204, 13]))
            pygame.draw.rect(screen, (255, 0, 0), transform_scale([1209, 34, player_hp/100*204, 13]))


            # left enemy
            enemy = screen.blit(pygame.transform.flip(images[battle_detail[stage]["enemy_surf"]], flip_x=True, flip_y=False), transform_scale([-51, 100]))
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([0, 0, 310, 80]))
            text(screen, "HP", (0, 0, 0), 24, transform_scale([28, 22]))
            pygame.draw.rect(screen, (0, 0, 0), transform_scale([79, 34, 204, 13]))
            pygame.draw.rect(screen, (255, 0, 0), transform_scale([79, 34, enemy_hp/battle_detail[stage]["enemy_hp"]*204, 13]))

            # discription
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([320, 0, 800, 80]))
            if(action == None):
                text(screen, "選擇行動", (20, 20, 20), transform_scale([35])[0], transform_scale([720, 48]), "center")
            else:
                text(screen, battle_detail[stage]["discription"], (20, 20, 20), transform_scale([35])[0], transform_scale([720, 48]), "center")

            if(len(achievement_stack)>0):
                draw_achievemet_stack()

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
                    random.shuffle(current_q["options"])
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
                    if click_check(pos, transform_scale(list(enemy))):
                        click_times += 1
                        enemy_hp = max(0, enemy_hp-1)
                        if enemy_hp <= 0:
                            play_sfx("win")
                            time = -1*fps
                            if (len(battle_detail[stage]["order"]) <= battle_detail[stage]["target"][0]):
                                save["star"][stage] = 3
                                if(not(save["achievement"][3])):
                                    save["achievement"][3] = True
                                    achievement_stack.append([3, fps])
                            elif (len(battle_detail[stage]["order"]) <= battle_detail[stage]["target"][1]):
                                if save["star"][stage] < 2:
                                    save["star"][stage] = 2
                            else:
                                if save["star"][stage] < 1:
                                    save["star"][stage] = 1
                            if save["current_stage"] == 28:
                                save["unlock"][save.get("chosen_path", 34)] = True
                            elif len(save["unlock"])>save["current_stage"]+1:
                                save["unlock"][save["current_stage"]+1]=True
                            end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage)
                            write()
                            game_state = "win"
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
                    if time == 1: play_sfx("attack")
                    if(time > 0 and time < fps*1):
                        time += 1
                        q_text = current_q["answer"]
                        text_sp(screen, q_text, (120, 0, 0), 200, transform_scale([220, 330]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1): 
                        time = 0
                    
                    if time == 0:
                        attack_times += 1
                        enemy_hp -= 20*scale[save["equipt"][0]] if not(god_mod) else 9999

                elif action == "recover":
                    if time == 1: play_sfx("heal")
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
                        play_sfx("win")
                        time = -1*fps 
                        if (question_num <= battle_detail[stage]["target"][0]):
                            save["star"][stage] = 3
                            if(not(save["achievement"][3])):
                                save["achievement"][3] = True
                                achievement_stack.append([3, fps])
                        elif (question_num <= battle_detail[stage]["target"][1]):
                            save["star"][stage] = max(save["star"][stage], 2)
                        else:
                            save["star"][stage] = max(save["star"][stage], 1)
                        
                        if save["current_stage"] == 28:
                            save["unlock"][save.get("chosen_path", 34)] = True
                        elif len(save["unlock"])>save["current_stage"]+1:
                            save["unlock"][save["current_stage"]+1]=True
                        write()
                        end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage)
                        game_state = "win"
                    else: 
                        draggable_rects.clear() 
                        draggable_rects_initial_pos.clear()
                        if question_num >= len(battle_detail[stage]["order"]):
                            random.shuffle(battle_detail[stage]["order"])
                            question_num = 0

            elif correct == False:
                if action == "attack":
                    if time == 1:                     
                        #play_sfx("error")             
                        play_sfx("damage")
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, battle_detail[stage]["enemy_attack_word"], (120, 0, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    
                    if time == 0:
                        attack_times += 1
                        player_hp -= round(battle_detail[stage]["enemy_attack"] * scale[save["equipt"][1]]/100)
                        correct = None
                        question_num += 1
                        action = None
                        
                        if player_hp <= 0:
                            play_sfx("lose")
                            time = -1*fps
                            end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage)
                            game_state = "lose"
                        else: 
                            draggable_rects.clear()
                            draggable_rects_initial_pos.clear()
                            if question_num >= len(battle_detail[stage]["order"]):
                                random.shuffle(battle_detail[stage]["order"])
                                question_num = 0
                elif action == "recover":
                    if time == 1:                     
                        #play_sfx("error")             
                        play_sfx("damage")
                    if(time > 0 and time < fps*1):
                        time += 1
                        q_text = current_q["answer"]
                        text_sp(screen, q_text, (120, 255, 120), transform_scale([200])[0], transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                        text_sp(screen, "╳", (100, 0, 0), transform_scale([250])[0], transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0

                    if time == 0:
                        player_hp -= 10
                        correct = None
                        question_num += 1
                        action = None
                        
                        if player_hp <= 0:
                            play_sfx("lose")
                            time = -1*fps
                            end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage)
                            game_state = "lose"
                        else: 
                            draggable_rects.clear()
                            draggable_rects_initial_pos.clear()
                            if question_num >= len(battle_detail[stage]["order"]):
                                random.shuffle(battle_detail[stage]["order"])
                                question_num = 0
        # ... after the elif battle_detail[stage]["question_type"] == "input": block ...
        
        elif battle_detail[stage]["question_type"] == "Sentence_Order":
            # BG image
            draw_story_bg(stage)

            # right character
            screen.blit(pygame.transform.flip(images[4], flip_x=True, flip_y=False), transform_scale([959, 263]))
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([1130, 0, 310, 80]))
            text(screen, "HP", (0, 0, 0), 24, transform_scale([1158, 22]))
            pygame.draw.rect(screen, (0, 0, 0), transform_scale([1209, 34, 204, 13]))
            pygame.draw.rect(screen, (255, 0, 0), transform_scale([1209, 34, player_hp/100*204, 13]))

            # left enemy
            enemy = screen.blit(pygame.transform.flip(images[battle_detail[stage]["enemy_surf"]], flip_x=True, flip_y=False), transform_scale([-51, 100]))
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([0, 0, 310, 80]))
            text(screen, "HP", (0, 0, 0), 24, transform_scale([28, 22]))
            pygame.draw.rect(screen, (0, 0, 0), transform_scale([79, 34, 204, 13]))
            pygame.draw.rect(screen, (255, 0, 0), transform_scale([79, 34, enemy_hp/battle_detail[stage]["enemy_hp"]*204, 13]))

            # Description
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([320, 0, 800, 80]))
            if (action == None):
                text(screen, "選擇行動", (20, 20, 20), transform_scale([35])[0], transform_scale([720, 48]), "center")
            else:
                text(screen, battle_detail[stage]["discription"], (20, 20, 20), transform_scale([35])[0], transform_scale([720, 48]), "center")

            # Main Action Selection (Attack/Recover)
            if action is None:
                #draggable_rects.clear() 
                #draggable_rects_initial_pos.clear()
                pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([324, 552, 791, 408]))
                pygame.draw.rect(screen, pygame.Color("#ececec"), transform_scale([407, 729, 194, 207]))
                pygame.draw.rect(screen, pygame.Color("#ececec"), transform_scale([840, 729, 194, 207]))
                text(screen, "攻擊", (0, 0, 0), 64, transform_scale([504, 813]), "center")
                text(screen, "回復", (0, 0, 0), 64, transform_scale([937, 813]), "center")
        
            
            
            # The Puzzle Logic
            else:
                q_index = battle_detail[stage]["order"][question_num]
                current_q = battle_detail[stage]["questions"][q_index]
                
                # Setup Rects for the first time for this question
                if not draggable_rects:
                    current_sentence_indices =[] # Reset user answer
                    random.shuffle(current_q["options"])
                    options = current_q["options"]
                    
                    # 1. DYNAMICALLY size rects based on text length!
                    try: 
                        temp_font = pygame.font.Font('media/LXGWMarkerGothic-Regular.ttf', transform_scale([32])[0])
                    except: 
                        temp_font = pygame.font.Font(pygame.font.get_default_font(), transform_scale([32])[0])
                        
                    opt_h = transform_scale([70])[0]
                    for opt_text in options:
                        text_w = temp_font.size(opt_text)[0]
                        # Min width 120, otherwise expand to fit text + 40px padding
                        opt_w = max(transform_scale([120])[0], text_w + transform_scale([40])[0])
                        draggable_rects.append(pygame.Rect(0, 0, opt_w, opt_h))

                # Draw Question Meaning (The Prompt)
                pygame.draw.rect(screen, pygame.Color("#f0f0f0"), transform_scale([200, 200, 1040, 80]), border_radius=10)
                text(screen, current_q["meaning"], (0,0,0), 40, transform_scale([720, 240]), "center")

                # Define Zones
                answer_y = transform_scale([400])[0]
                bank_y = transform_scale([600])[0]
                zone_answer = pygame.Rect(transform_scale([80, 350, 1280, 170])) # <--- Widened drop zone
                gap = transform_scale([20])[0]
                
                hover_insertion_index = -1
                if is_dragging and dragged_item_index != -1:
                    dragged_rect = draggable_rects[dragged_item_index]
                    if zone_answer.colliderect(dragged_rect):
                        hover_insertion_index = len(current_sentence_indices)
                        for idx, opt_idx in enumerate(current_sentence_indices):
                            if dragged_rect.centerx < draggable_rects[opt_idx].centerx:
                                hover_insertion_index = idx
                                break

                # Drawing Answer Line
                pygame.draw.line(screen, (0,0,0), transform_scale([100, 500]), transform_scale([1340, 500]), 3)

                # --- 2. DRAW BLOCKS WITH SPREADING ANIMATION (Dynamic Width) ---
                ans_x = transform_scale([100])[0]
                
                for idx_in_list, opt_idx in enumerate(current_sentence_indices):
                    r = draggable_rects[opt_idx]
                    
                    # If the dragged item is hovering here, leave a space for it!
                    if hover_insertion_index == idx_in_list and is_dragging and dragged_item_index != -1:
                        ans_x += draggable_rects[dragged_item_index].width + gap
                        
                    if not (is_dragging and dragged_item_index == opt_idx):
                        r.x += (ans_x - r.x) * 0.2 
                        r.y += (answer_y - r.y) * 0.2
                        
                    # Add this block's width to the running total
                    ans_x += r.width + gap

                    # --- FIX: ACTUALLY DRAW THE SELECTED BLOCKS ---
                    if not (is_dragging and dragged_item_index == opt_idx):
                        pygame.draw.rect(screen, pygame.Color("#aaddff"), r, border_radius=8)
                        pygame.draw.rect(screen, (0,0,0), r, 2, 8)
                        text(screen, current_q["options"][opt_idx], (0,0,0), 32, r.center, "center")

                # --- 3. DRAW WORD BANK (Dynamic Width & Auto Wrapping) ---
                bank_x = transform_scale([100])[0]
                bank_y_start = transform_scale([580])[0]
                current_row = 0
                
                for i in range(len(current_q["options"])):
                    if i not in current_sentence_indices:
                        r = draggable_rects[i]
                        
                        # Wrap to next line if this block exceeds screen width
                        if bank_x + r.width > transform_scale([1340])[0]:
                            bank_x = transform_scale([100])[0]
                            current_row += 1
                            
                        if not (is_dragging and dragged_item_index == i):
                            target_y = bank_y_start + current_row * transform_scale([90])[0]
                            r.x += (bank_x - r.x) * 0.2
                            r.y += (target_y - r.y) * 0.2
                            
                            # --- ACTUALLY DRAW THE UNSELECTED BLOCKS ---
                            pygame.draw.rect(screen, pygame.Color("#ececec"), r, border_radius=8)
                            pygame.draw.rect(screen, (0,0,0), r, 2, 8)
                            text(screen, current_q["options"][i], (0,0,0), 32, r.center, "center")
                        
                        # Accumulate width for the next block
                        bank_x += r.width + gap
                        
                # Dragged Item on top
                if is_dragging and dragged_item_index != -1:
                    r = draggable_rects[dragged_item_index]
                    pygame.draw.rect(screen, pygame.Color("#ffd700"), r, border_radius=8)
                    pygame.draw.rect(screen, (0,0,0), r, 2, 8)
                    text(screen, current_q["options"][dragged_item_index], (0,0,0), 32, r.center, "center")

                # Submit Button (Cast Spell)

                # Submit Button (Cast Spell)
                # ... (Leave your submit and reset button codes exactly as they are down here!) ...

                # Submit Button (Cast Spell)
                submit_rect = pygame.Rect(transform_scale([750, 800, 200, 80]))
                pygame.draw.rect(screen,[186, 148, 45], submit_rect, border_radius=10)
                pygame.draw.rect(screen, [0, 0, 0], submit_rect, 3, 10)
                text(screen, "詠唱", [0, 0, 0], 40, submit_rect.center, "center")

                # Reset Button (Clear Sentence)
                reset_rect = pygame.Rect(transform_scale([490, 800, 200, 80]))
                pygame.draw.rect(screen, [200, 80, 80], reset_rect, border_radius=10) # Reddish color for reset
                pygame.draw.rect(screen, [0, 0, 0], reset_rect, 3, 10)
                text(screen, "重置", [255, 255, 255], 40, reset_rect.center, "center")

                # Determine Positions and Draw Blocks
                # We arrange blocks based on whether they are in 'current_sentence_indices' or not
                if(len(achievement_stack)>0):
                    draw_achievemet_stack()

            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if time == 0:
                    if click_check(pos, transform_scale(list(enemy))):
                        click_times += 1
                        enemy_hp = max(0, enemy_hp-1)
                        if enemy_hp <= 0:
                            play_sfx("win")
                            time = -1*fps
                            if (len(battle_detail[stage]["order"]) <= battle_detail[stage]["target"][0]):
                                save["star"][stage] = 3
                                if(not(save["achievement"][3])):
                                    save["achievement"][3] = True
                                    achievement_stack.append([3, fps])
                            elif (len(battle_detail[stage]["order"]) <= battle_detail[stage]["target"][1]):
                                if save["star"][stage] < 2:
                                    save["star"][stage] = 2
                            else:
                                if save["star"][stage] < 1:
                                    save["star"][stage] = 1
                            if save["current_stage"] == 28:
                                save["unlock"][save.get("chosen_path", 34)] = True
                            elif len(save["unlock"])>save["current_stage"]+1:
                                save["unlock"][save["current_stage"]+1]=True
                            end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage)
                            write()
                            game_state = "win"
                    if action is None:
                        # Select Attack/Recover
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if click_check(pos, transform_scale([407, 729, 194, 207])):
                                action = "attack"
                            elif click_check(pos, transform_scale([840, 729, 194, 207])):
                                action = "recover"
                    else:
                        # Drag Logic
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            # 1. Check Submit Button
                            if submit_rect.collidepoint(event.pos):
                                time = 1 # Start validation
                                # Construct user sentence from indices
                                user_sentence =[current_q["options"][i] for i in current_sentence_indices]
                                if user_sentence == current_q["answer_order"]:
                                    correct = True
                                else:
                                    correct = False
                            
                            # 2. Check Reset Button
                            elif reset_rect.collidepoint(event.pos):
                                # play_sfx("click")  # Uncomment this if you added the sound manager!
                                current_sentence_indices.clear() # This empties the answer line instantly!
                            
                            # 3. Check Words
                            elif not is_dragging:
                                for i, rect in enumerate(draggable_rects):
                                    if rect.collidepoint(event.pos):
                                        is_dragging = True
                                        dragged_item_index = i
                                        drag_offset_x = event.pos[0] - rect.x
                                        drag_offset_y = event.pos[1] - rect.y
                                        # Temporarily remove from logic lists so it floats freely
                                        if i in current_sentence_indices:
                                            current_sentence_indices.remove(i)
                                        break
                        
                        elif event.type == pygame.MOUSEMOTION and is_dragging:
                            #if dragged_item_index != -1:
                            draggable_rects[dragged_item_index].x = event.pos[0] - drag_offset_x
                            draggable_rects[dragged_item_index].y = event.pos[1] - drag_offset_y
                        
                        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and is_dragging:
                            if zone_answer.colliderect(draggable_rects[dragged_item_index]):
                                if hover_insertion_index != -1:
                                    current_sentence_indices.insert(hover_insertion_index, dragged_item_index)
                                else:
                                    current_sentence_indices.append(dragged_item_index)
                            else:
                                pass 
                            
                            
                            is_dragging = False
                            dragged_item_index = -1

            # --- Validation & Transition Logic (Reuse logic from other modes) ---
            if correct == True:
                if action == "attack":
                    if time == 1: play_sfx("attack")
                    if(time > 0 and time < fps*1):
                        time += 1
                        # Show Full Correct Sentence
                        ans_str = "".join(current_q["answer_order"])
                        text_sp(screen, ans_str, (120, 0, 0), 64, transform_scale([WIDTH/2, 330]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1): 
                        time = 0
                    
                    if time == 0:
                        attack_times += 1
                        enemy_hp -= 20*scale[save["equipt"][0]] if not(god_mod) else 9999
                        correct = None 
                        question_num += 1
                        action = None
                        draggable_rects.clear() # Reset for next question

                        # Win Check
                        if enemy_hp <= 0:
                            play_sfx("win")
                            time = -1*fps 
                            if (question_num <= battle_detail[stage]["target"][0]):
                                save["star"][stage] = 3
                                if(not(save["achievement"][3])):
                                    save["achievement"][3] = True
                                    achievement_stack.append([3, fps])
                            elif (question_num <= battle_detail[stage]["target"][1]):
                                save["star"][stage] = max(save["star"][stage], 2)
                            else:
                                save["star"][stage] = max(save["star"][stage], 1)
                            
                            if save["current_stage"] == 28:
                                save["unlock"][save.get("chosen_path", 34)] = True
                            elif len(save["unlock"])>save["current_stage"]+1:
                                save["unlock"][save["current_stage"]+1]=True
                            write()
                            end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage)
                            game_state = "win"
                        elif question_num >= len(battle_detail[stage]["order"]):
                            random.shuffle(battle_detail[stage]["order"])
                            question_num = 0

                elif action == "recover":
                    if time == 1: play_sfx("heal")
                    # Identical Recover logic to Drag mode
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, "回復成功", (120, 255, 120), 100, transform_scale([WIDTH/2, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1): time = 0
                    if time == 0:
                        player_hp = min(player_hp+20, 100)
                        correct = None
                        question_num += 1
                        action = None
                        draggable_rects.clear()
                        if question_num >= len(battle_detail[stage]["order"]):
                            random.shuffle(battle_detail[stage]["order"])
                            question_num = 0

            elif correct == False:
                if action == "attack":
                    if time == 1:                     # <--- ADD THESE 3 LINES
                        play_sfx("error")             # <---
                        play_sfx("damage")
                # Wrong Answer Logic
                if(time > 0 and time < fps*1):
                    time += 1
                    text_sp(screen, "X", (150, 0, 0), 200, transform_scale([WIDTH/2, 520]), int((fps*1-time)/(fps*1)*255), "center")
                elif(time >= fps*1):
                    time = 0
                
                if time == 0:
                    if action == "attack": 
                        attack_times += 1
                        player_hp -= round(battle_detail[stage]["enemy_attack"] * scale[save["equipt"][1]]/100)
                    elif action == "recover": 
                        player_hp -= 10
                    
                    correct = None
                    question_num += 1
                    action = None
                    draggable_rects.clear()

                    if player_hp <= 0:
                        play_sfx("lose")
                        time = -1*fps
                        end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage)
                        game_state = "lose"
                    elif question_num >= len(battle_detail[stage]["order"]):
                        random.shuffle(battle_detail[stage]["order"])
                        question_num = 0

        elif battle_detail[stage]["question_type"] == "input":
            # BG image
            draw_story_bg(stage)

            # right character
            screen.blit(pygame.transform.flip(images[4], flip_x=True, flip_y=False), transform_scale([959, 263]))
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([1130, 0, 310, 80]))
            text(screen, "HP", (0, 0, 0), 24, transform_scale([1158, 22]))
            pygame.draw.rect(screen, (0, 0, 0), transform_scale([1209, 34, 204, 13]))
            pygame.draw.rect(screen, (255, 0, 0), transform_scale([1209, 34, player_hp/100*204, 13]))

            # left enemy
            enemy = screen.blit(pygame.transform.flip(images[battle_detail[stage]["enemy_surf"]], flip_x=True, flip_y=False), transform_scale([-51, 100]))
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([0, 0, 310, 80]))
            text(screen, "HP", (0, 0, 0), 24, transform_scale([28, 22]))
            pygame.draw.rect(screen, (0, 0, 0), transform_scale([79, 34, 204, 13]))
            pygame.draw.rect(screen, (255, 0, 0), transform_scale([79, 34, enemy_hp/battle_detail[stage]["enemy_hp"]*204, 13]))

            # discription
            pygame.draw.rect(screen, pygame.Color("#d9d9d9"), transform_scale([320, 0, 800, 80]))
            if(action == None):
                text(screen, "選擇行動", (20, 20, 20), transform_scale([35])[0], transform_scale([720, 48]), "center")
            else:
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

            if(len(achievement_stack)>0):
                draw_achievemet_stack()
            
            
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
                    if click_check(pos, transform_scale(list(enemy))):
                        click_times += 1
                        enemy_hp = max(0, enemy_hp-1)
                        if enemy_hp <= 0:
                            play_sfx("win")
                            time = -1*fps
                            if (len(battle_detail[stage]["order"]) <= battle_detail[stage]["target"][0]):
                                save["star"][stage] = 3
                                if(not(save["achievement"][3])):
                                    save["achievement"][3] = True
                                    achievement_stack.append([3, fps])
                            elif (len(battle_detail[stage]["order"]) <= battle_detail[stage]["target"][1]):
                                if save["star"][stage] < 2:
                                    save["star"][stage] = 2
                            else:
                                if save["star"][stage] < 1:
                                    save["star"][stage] = 1
                            if save["current_stage"] == 28:
                                save["unlock"][save.get("chosen_path", 34)] = True
                            elif len(save["unlock"])>save["current_stage"]+1:
                                save["unlock"][save["current_stage"]+1]=True
                            end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage)
                            write()
                            game_state = "win"
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
                                if not(save["achievement"][8]):
                                    try:
                                        my_font = pygame.font.Font('media/LXGWMarkerGothic-Regular.ttf', transform_scale([64])[0])
                                    except Exception:
                                        my_font = pygame.font.Font(pygame.font.get_default_font(), transform_scale([64])[0])
                                    if(my_font.size(outputArr)[0]>660):
                                        save["achievement"][8] = True
                                        achievement_stack.append([8, fps])
                                    if (not(save["achievement"][29])):
                                        if(sum(save["achievement"]) == 29):
                                            save["achievement"][29] = True
                                            achievement_stack.append([29, fps])
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
                    if time == 1: play_sfx("attack")
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, verb[battle_detail[stage]["question"]][battle_detail[stage]["curr_qs"]][0], (120, 0, 0), 200, transform_scale([220, 330]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    if time == 0:
                        attack_times += 1
                        enemy_hp -= 20*scale[save["equipt"][0]] if not(god_mod) else 9999
                        correct = None
                        action = None
                        if enemy_hp <= 0:
                            play_sfx("win")
                            time = -1*fps
                            if (battle_detail[stage]["counter"] <= battle_detail[stage]["target"][0]):
                                save["star"][stage] = 3
                                if(not(save["achievement"][3])):
                                    save["achievement"][3] = True
                                    achievement_stack.append([3, fps])
                            elif (battle_detail[stage]["counter"] <= battle_detail[stage]["target"][1]):
                                if save["star"][stage] < 2:
                                    save["star"][stage] = 2
                            else:
                                if save["star"][stage] < 1:
                                    save["star"][stage] = 1
                            if save["current_stage"] == 28:
                                save["unlock"][save.get("chosen_path", 34)] = True
                            elif len(save["unlock"])>save["current_stage"]+1:
                                save["unlock"][save["current_stage"]+1]=True
                            write()
                            end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage)
                            game_state = "win"
                        else:
                            temp = random.randint(0, len(verb[battle_detail[stage]["question"]])-1)
                            while temp == battle_detail[stage]["curr_qs"]:
                                temp = random.randint(0, len(verb[battle_detail[stage]["question"]])-1)
                            battle_detail[stage]["curr_qs"] = temp
                        inputArr = ""
                        outputArr = ""
                elif action == "recover":
                    if time == 1: play_sfx("heal")
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
                    if time == 1:                     # <--- ADD THESE 3 LINES
                        #play_sfx("error")             # <---
                        play_sfx("damage")
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, battle_detail[stage]["enemy_attack_word"], (120, 0, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    if time == 0:
                        attack_times += 1
                        player_hp -= round(battle_detail[stage]["enemy_attack"] * scale[save["equipt"][1]]/100)
                        correct = None
                        if stage == 0:
                            action = "attack"
                        else:
                            action = None
                        if player_hp <= 0:
                            play_sfx("lose")
                            time = -1*fps
                            end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage)
                            game_state = "lose"
                        else:
                            temp = random.randint(0, len(verb[battle_detail[stage]["question"]])-1)
                            while temp == battle_detail[stage]["curr_qs"]:
                                temp = random.randint(0, len(verb[battle_detail[stage]["question"]])-1)
                            battle_detail[stage]["curr_qs"] = temp
                        inputArr = ""
                        outputArr = ""
                elif action == "recover":
                    if time == 1:                     # <--- ADD THESE 3 LINES
                        #play_sfx("error")             # <---
                        play_sfx("damage")
                    if(time > 0 and time < fps*1):
                        time += 1
                        text_sp(screen, verb[battle_detail[stage]["question"]][battle_detail[stage]["curr_qs"]][0], (120, 255, 120), 200, transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                        text_sp(screen, "╳", (100, 0, 0), transform_scale([250])[0], transform_scale([1310, 520]), int((fps*1-time)/(fps*1)*255), "center")
                    elif(time >= fps*1):
                        time = 0
                    if time == 0:
                        player_hp -= 10
                        correct = None
                        action = None
                        if player_hp <= 0:
                            time = -1*fps
                            end_stage_achievement_check(recover_times, damage_taken_times, attack_times, click_times, player_hp, idle_times, stage)
                            game_state = "lose"
                        else:
                            temp = random.randint(0, len(verb[battle_detail[stage]["question"]])-1)
                            while temp == battle_detail[stage]["curr_qs"]:
                                temp = random.randint(0, len(verb[battle_detail[stage]["question"]])-1)
                            battle_detail[stage]["curr_qs"] = temp
                        inputArr = ""
                        outputArr = ""
        if(len(achievement_stack)>0):
            draw_achievemet_stack()
    
    if game_state == "select_world":
        screen.blit(pygame.transform.scale(images[31], (WIDTH, HEIGHT)), (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        text(screen, "選擇章節", [255, 255, 255], 40, transform_scale([WIDTH/2, 50]), "center")
        
        w1_rect = transform_scale([900, 240, 380, 70]) # Forest
        w2_rect = transform_scale([80, 240, 380, 70]) # Kingdom
        w3_rect = transform_scale([80, 650, 500, 70]) # Road
        w4_rect = transform_scale([850, 630, 420, 70]) # Demon Castle

        chapters = [
            (w1_rect, True, "第一章: 五十音"),
            (w2_rect, save['unlock'][9], "第二章: 漢字魔法"),
            (w3_rect, save['unlock'][20], "第三章: 文法與動詞變化"),
            (w4_rect, (save['unlock'][29] or save['unlock'][34]), "最終章: 命運的對決")
        ]
        
        for rect, is_unlocked, title in chapters:
            is_hover = click_check(mouse_pos, rect)
            
            if is_unlocked:
                if is_hover:
                    # GLOW EFFECT: Draw a bright white/yellow blurred-look border first
                    glow_rect = [rect[0]-5, rect[1]-5, rect[2]+10, rect[3]+10]
                    pygame.draw.rect(screen, [255, 255, 200], glow_rect, border_radius=15)
                    button_color = [255, 215, 0] # Bright Gold
                else:
                    button_color = [186, 148, 45] # Normal Gold
            else:
                button_color = [100, 100, 100] # Gray (Locked)

            pygame.draw.rect(screen, button_color, rect, border_radius=10)
            pygame.draw.rect(screen, [0, 0, 0], rect, 3, 10) # Black outline
            # Draw text
            text_color = [0, 0, 0] if is_unlocked else [50, 50, 50]
            text(screen, title, text_color, 28, (rect[0] + rect[2]/2, rect[1] + rect[3]/2), "center")

        back_rect = transform_scale([40, 40, 100, 50])
        back_hover = click_check(mouse_pos, back_rect)
        back_color = [255, 255, 255] if back_hover else [186, 148, 45]
        pygame.draw.rect(screen, back_color, back_rect, border_radius=br)
        pygame.draw.rect(screen, [0, 0, 0], back_rect, br, br)
        text(screen, "返回", [0, 0, 0], 25, transform_scale([90, 65]), "center")


        if(save["obtain"][0]):
            pygame.draw.rect(screen, [153, 116, 41], transform_scale([620, 860, 80, 80]), border_radius=br)
            pygame.draw.rect(screen, [69, 46, 0], transform_scale([620, 860, 80, 80]), br, br)
            if save["equipt"][0] != 7:
                screen.blit(images[int(save["equipt"][0]/2)+35], transform_scale([630, 870]))
        
        if(selecting_weapon):
            pygame.draw.rect(screen, [153, 116, 41], transform_scale([620, 860-80*save["obtain_w_n"], 80, 80*save["obtain_w_n"]]), border_radius=br)
            pygame.draw.rect(screen, [69, 46, 0], transform_scale([620, 860-80*save["obtain_w_n"], 80, 80*save["obtain_w_n"]]), br, br)
            if(save["obtain"][0]):
                screen.blit(images[35], transform_scale([630, 870-80]))
            if(save["obtain"][2]):
                screen.blit(images[36], transform_scale([630, 870-160]))
            if(save["obtain"][4]):
                screen.blit(images[37], transform_scale([630, 870-240]))
            if (save["obtain"][6]):
                screen.blit(images[38], transform_scale([630, 870-80*save["obtain_w_n"]]))

            

        if(save["obtain"][1]):
            pygame.draw.rect(screen, [153, 116, 41], transform_scale([740, 860, 80, 80]), border_radius=br)
            pygame.draw.rect(screen, [69, 46, 0], transform_scale([740, 860, 80, 80]), br, br)
            if save["equipt"][1] == 6:
                screen.blit(images[38], transform_scale([750, 870]))
            elif save["equipt"][1] != 8:
                screen.blit(images[int(save["equipt"][1]/2)+32], transform_scale([750, 870]))

        if(selecting_equiptment):
            pygame.draw.rect(screen, [153, 116, 41], transform_scale([740, 860-80*save["obtain_e_n"], 80, 80*save["obtain_e_n"]]), border_radius=br)
            pygame.draw.rect(screen, [69, 46, 0], transform_scale([740, 860-80*save["obtain_e_n"], 80, 80*save["obtain_e_n"]]), br, br)
            if(save["obtain"][1]):
                screen.blit(images[32], transform_scale([750, 870-80]))
            if(save["obtain"][3]):
                screen.blit(images[33], transform_scale([750, 870-160]))
            if(save["obtain"][5]):
                screen.blit(images[34], transform_scale([750, 870-240]))
            if (save["obtain"][6]):
                screen.blit(images[38], transform_scale([750, 870-80*save["obtain_e_n"]]))


        if(time != 0):
            time += 1
            s.set_alpha(int(time/fps/1*255))
            screen.blit(s, (0,0))

        if(len(achievement_stack)>0):
            draw_achievemet_stack()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()

                    if click_check(pos, transform_scale([620, 860, 80, 80])) and time == 0:
                        play_sfx("click")
                        if selecting_weapon:
                            if save["equipt"][0] == 6:
                                save["equipt"][1] = 8
                            save["equipt"][0] = 7
                        selecting_weapon = not(selecting_weapon)
                        selecting_equiptment = False
                    elif click_check(pos, transform_scale([740, 860, 80, 80])) and time == 0:
                        play_sfx("click")
                        if selecting_equiptment:
                            if save["equipt"][1] == 6:
                                save['equipt'][0] = 7
                            save["equipt"][1] = 8
                        selecting_equiptment = not(selecting_equiptment)
                        selecting_weapon = False
                    elif click_check(pos, transform_scale([620, 860-80, 80, 80])) and time == 0 and save["obtain"][0] and selecting_weapon:
                        play_sfx("click")
                        if save["equipt"][1] == 6:
                            save["equipt"][1] = 8
                        save["equipt"][0] = 0
                        selecting_weapon = not(selecting_weapon)
                    elif click_check(pos, transform_scale([620, 860-160, 80, 80])) and time == 0 and save["obtain"][2] and selecting_weapon:
                        play_sfx("click")
                        if save["equipt"][1] == 6:
                            save["equipt"][1] = 8
                        save["equipt"][0] = 2
                        selecting_weapon = not(selecting_weapon)
                    elif click_check(pos, transform_scale([620, 860-240, 80, 80])) and time == 0 and save["obtain"][4] and selecting_weapon:
                        play_sfx("click")
                        if save["equipt"][1] == 6:
                            save["equipt"][1] = 8
                        save["equipt"][0] = 4
                        selecting_weapon = not(selecting_weapon)
                    elif click_check(pos, transform_scale([740, 860-80, 80, 80])) and time == 0 and save["obtain"][1] and selecting_equiptment:
                        play_sfx("click")
                        if save["equipt"][0] == 6:
                            save["equipt"][0] = 7
                        save["equipt"][1] = 1
                        selecting_equiptment = not(selecting_equiptment)
                    elif click_check(pos, transform_scale([740, 860-160, 80, 80])) and time == 0 and save["obtain"][3] and selecting_equiptment:
                        play_sfx("click")
                        if save["equipt"][0] == 6:
                            save["equipt"][0] = 7
                        save["equipt"][1] = 3
                        selecting_equiptment = not(selecting_equiptment)
                    elif click_check(pos, transform_scale([740, 860-240, 80, 80])) and time == 0 and save["obtain"][5] and selecting_equiptment:
                        play_sfx("click")
                        if save["equipt"][0] == 6:
                            save["equipt"][0] = 7
                        save["equipt"][1] = 5
                        selecting_equiptment = not(selecting_equiptment)
                    elif click_check(pos, transform_scale([620, 860-80*save["obtain_w_n"], 80, 80])) and time == 0 and save["obtain"][6] and selecting_weapon:
                        play_sfx("click")
                        save["equipt"][0] = 6
                        save["equipt"][1] = 6
                        selecting_weapon = not(selecting_weapon)
                    elif click_check(pos, transform_scale([740, 860-80*save["obtain_e_n"], 80, 80])) and time == 0 and save["obtain"][6] and selecting_equiptment:
                        play_sfx("click")
                        save["equipt"][0] = 6
                        save["equipt"][1] = 6
                        selecting_equiptment = not(selecting_equiptment)
                    elif click_check(pos, w1_rect) and time == 0:
                        play_sfx("click")
                        time += 1; menu_action = "w1"
                    elif click_check(pos, w2_rect) and save['unlock'][9] and time == 0:
                        play_sfx("click")
                        time += 1; menu_action = "w2"
                    elif click_check(pos, w3_rect) and save['unlock'][20] and time == 0:
                        play_sfx("click")
                        time += 1; menu_action = "w3"
                    elif click_check(pos, w4_rect) and (save['unlock'][29] or save['unlock'][34]) and time == 0:
                        play_sfx("click")
                        time += 1; menu_action = "w4"
                    elif click_check(pos, transform_scale([40, 40, 80, 80])) and time == 0:
                        play_sfx("click")
                        time += 1; menu_action = "back"
                    else:
                        selecting_weapon = False
                        selecting_equiptment = False

        if(time > fps):
            if menu_action == "w1":
                current_chapter = 0
                save['current_stage'] = chapter_ranges[0][0]
                game_state = "select_stage"
            elif menu_action == "w2":
                current_chapter = 1
                save['current_stage'] = chapter_ranges[1][0]
                game_state = "select_stage"
            elif menu_action == "w3":
                current_chapter = 2
                save['current_stage'] = chapter_ranges[2][0]
                game_state = "select_stage"
            elif menu_action == "w4":
                current_chapter = 3
                # Dynamic branching validation
                if save.get('chosen_path', 34) == 29:
                    chapter_ranges[3] = (29, 33)
                    save['current_stage'] = 29
                else:
                    chapter_ranges[3] = (34, 38)
                    save['current_stage'] = 34
                game_state = "select_stage"
            elif menu_action == "back":
                game_state = "menu"
            time = 0


    # stage select
    if game_state == "select_stage":
        

        # bg image, text, center image, nearby image
        draw_stage_selection(save['current_stage'])
        
        min_stage, max_stage = chapter_ranges[current_chapter]

        # left right arrow
        #if (save['current_stage'] != 0):
            #screen.blit(images[11], transform_scale([162, 424]))
        #if (save['current_stage']+1 != len(save["star"])):
            #screen.blit(pygame.transform.flip(images[11], flip_x=True, flip_y=False), transform_scale([1186, 424]))
        if (save['current_stage'] > min_stage):
            screen.blit(images[11], transform_scale([162, 424]))
        if (save['current_stage'] < max_stage and save['current_stage'] + 1 < len(save["unlock"])):
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

        # back button
        pygame.draw.rect(screen, [186, 148, 45], transform_scale([40, 40, 80, 80]), border_radius=br)
        pygame.draw.rect(screen, [0, 0, 0], transform_scale([40, 40, 80, 80]), br, br)
        text(screen, "返回", [0, 0, 0], 20, transform_scale([80, 80]), "center")


        if(time != 0):
            time += 1
            s.set_alpha(int(time/fps/1*255))
            screen.blit(s, (0,0))

        if(len(achievement_stack)>0):
            draw_achievemet_stack()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if click_check(pygame.mouse.get_pos(), transform_scale([1186, 424, 75, 110])):
                        #if (save['current_stage']+1 < len(save["star"])):
                        if (save['current_stage'] < max_stage and save['current_stage']+1 < len(save["star"])):
                            play_sfx("click")
                            save['current_stage'] += 1
                            write()
                    if click_check(pygame.mouse.get_pos(), transform_scale([162, 424, 75, 110])):
                        if (save['current_stage'] > min_stage):
                            play_sfx("click")
                            save['current_stage'] -= 1
                            write()
                    if click_check(pygame.mouse.get_pos(), transform_scale([297, 198, 847, 635])):
                        if (save['unlock'][save["current_stage"]]):
                            if (time == 0):
                                play_sfx("click")
                                time += 1
                                menu_action = "enter"
                    if click_check(pygame.mouse.get_pos(), transform_scale([40, 40, 80, 80])):
                        if(time == 0):
                            play_sfx("click")
                            time += 1
                            menu_action = "back"
        # enter story
        if(time > fps):
            if(menu_action =="enter"):
                game_state = "story"
                story_num = save["current_stage"]
                stage = save["current_stage"]
                dialog_num = 0
                time = 0
            elif(menu_action == "back"):
                game_state = "select_world"
                selecting_weapon = False
                selecting_equiptment = False
                story_num = save["current_stage"]
                stage = save["current_stage"]
                dialog_num = 0
                time = 0

    # this is game state of winning the game
    if game_state == "win" or game_state == "lose":
        # BG image
        draw_story_bg(stage)

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

        if(len(achievement_stack)>0):
            draw_achievemet_stack()

        # enter story
        if(time > fps*1):
            game_state = "select_stage"
            time = 0

    # control the setting of game sound, game voice, full screen
    if game_state == "option":
        # BG image
        screen.blit(images[0], (0, 0))

        # back button
        pygame.draw.rect(screen, [186, 148, 45], transform_scale([40, 40, 80, 80]), border_radius=br)
        pygame.draw.rect(screen, [0, 0, 0], transform_scale([40, 40, 80, 80]), br, br)
        text(screen, "返回", [0, 0, 0], 25, transform_scale([80, 80]), "center")
        


        pygame.draw.rect(screen, [220, 220, 220], transform_scale([80, 140, 1280, 680]), border_radius=br)
        text(screen, "設定", [0, 0, 0], 3*25, transform_scale([720, 190]), "center")
        text(screen, "    音樂:", [0, 0, 0], 3*20, transform_scale([100, 160+100]), "left")
        text(screen, "    音效:", [0, 0, 0], 3*20, transform_scale([100, 160+100+3*22]), "left")
        text(screen, "全螢幕:", [0, 0, 0], 3*20, transform_scale([100, 160+100+3*44]), "left")


        # adjust bar for music
        pygame.draw.rect(screen, [128, 128, 128], transform_scale([320, 170+100, 800*save['music']/100, 3*20]), border_radius=br)
        pygame.draw.rect(screen, [200, 200, 200], transform_scale([320+800*save['music']/100, 170+100, 800-800*save['music']/100, 3*20]), border_radius=br)
        pygame.draw.rect(screen, [0, 0, 0], transform_scale([320, 170+100, 800, 3*20]), br, br)
        pygame.draw.rect(screen, [255, 255, 255], transform_scale([380+680*save['music']/100-60, 170+100, 120, 3*20]), border_radius=br)
        pygame.draw.rect(screen, [0, 0, 0], transform_scale([380+680*save['music']/100-60, 170+100, 120, 3*20]), br, br)
        text(screen, str(save['music']), [0, 0, 0], 3*20, transform_scale([1220, 160+100]), "left")

        # adjust bar for sound
        pygame.draw.rect(screen, [128, 128, 128], transform_scale([320, 170+100+3*22, 800*save['sound']/100, 3*20]), border_radius=br)
        pygame.draw.rect(screen, [200, 200, 200], transform_scale([320+800*save['sound']/100, 170+100+3*22, 800-800*save['sound']/100, 3*20]), border_radius=br)
        pygame.draw.rect(screen, [0, 0, 0], transform_scale([320, 170+100+3*22, 800, 3*20]), br, br)
        pygame.draw.rect(screen, [255, 255, 255], transform_scale([380+680*save['sound']/100-60, 170+100+3*22, 120, 3*20]), border_radius=br)
        pygame.draw.rect(screen, [0, 0, 0], transform_scale([380+680*save['sound']/100-60, 170+100+3*22, 120, 3*20]), br, br)
        text(screen, str(save['sound']), [0, 0, 0], 3*20, transform_scale([1220, 160+100+3*22]), "left")

        # check box for full screen
        pygame.draw.rect(screen, [128, 128, 128], transform_scale([320, 170+100+3*44, 3*20, 3*20]), border_radius=br)
        pygame.draw.rect(screen, [200, 200, 200], transform_scale([320, 170+100+3*44, 3*20, 3*20]), br, br)
        text(screen, "X" if save["full_screen"] else "", [0, 0, 0], 3*15, transform_scale([320+3*10, 170+100+3*44+3*10]), "center")
        

        if(time != 0):
            time += 1
            s.set_alpha(int(time/fps/1*255))
            screen.blit(s, (0,0))

        if(len(achievement_stack)>0):
            draw_achievemet_stack()
        
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if click_check(pygame.mouse.get_pos(), transform_scale([40, 40, 80, 80])):
                        if(time == 0):
                            time += 1
                    if click_check(pos, transform_scale([380+680*save['music']/100-60, 170+100, 120, 3*20])):
                        changing = 'music'
                    if click_check(pos, transform_scale([380+680*save['sound']/100-60, 170+100+3*22, 120, 3*20])):
                        changing = 'sound'
                    if click_check(pos, transform_scale([320, 170+100+3*44, 3*20, 3*20])):
                        save["full_screen"] = not(save["full_screen"])
                        # WIDTH, WIDTH_switch, HEIGHT, HEIGHT_switch = WIDTH_switch, WIDTH, HEIGHT_switch, HEIGHT
                        if save["full_screen"]:
                            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                        else:
                            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    changing=None
                    write()


        if(changing == 'music'):
            a, b, r = transform_scale([380, 380+680, 680])
            save["music"] = min(max(0, int((pos[0]-a)/r*100)), 100)
        elif(changing == 'sound'):
            a, b, r = transform_scale([380, 380+680, 680])
            save["sound"] = min(max(0, int((pos[0]-a)/r*100)), 100)

        
        #  back
        if(time > fps*1):
            game_state = "menu"
            time=0

    {
#  小回復術士 
# 在一個關卡來使用回復魔法的次數達5次
#  普通回復術士 
# 在一個關卡來使用回復魔法的次數達15次
#  大回復術士 
# 在一個關卡來使用回復魔法的次數達30次
#  滿分 
# 在一個關卡中收集到3顆星星
#  半天星 
# 收集到所有星星的一半
#  滿天星 
# 收集到所有星星
#  無損 
# 以無被攻擊過的狀態下通過其中一關卡
#  根性 
# 已剩餘一成血以下的狀態下通過其中一關卡
#  超越 
# 在輸入類關卡中輸入的字數超出框架範圍
#  努力不懈 
# 連續挑戰同一關卡並獲勝5次
#  五十音 
# 已完成全部有關五十音的關卡
#  次序很重要 
# 已完成有關句子順序的關卡
#  熟悉的字(? 
# 已完成有關漢字的關卡
#  英雄級冒險者 
# 已完成有關動詞轉換的關卡
#  C級武器 
# 已獲得名匠靈珠
#  C級防具
# 已獲得皇家守衛套裝
#  A級武器 
# 已獲得天魔杖
#  A級防具
# 已獲得天神甲
#  SS級武器 
# 已獲得言靈天杖
#  SS級防具
# 已獲得不滅龍鱗
#  一拳不行就多一拳 
# 只用滑鼠點擊殺死魔物
#  等到天荒地老 
# 在其中一關卡內維持什麼都不做超過15分鐘
#  對不起 
# 殺死莉子
#  犧牲小我 
# 已達成「犧牲小我」結局
#  守護一切 
# 已達成「守護一切」結局
#  再度轉生 
# 開啟二周目
#  迎難而上 
# 通關二周目
#  史上最強豆腐 
# 不穿任何裝備通關最終關卡
#  一拳超人 
# 只用一擊擊敗魔物
#  勇者 
# 已獲得所有成就
    }

    # 30 achievements
    if game_state == "achievement":
        # BG image
        screen.blit(images[0], (0, 0))

        # back button
        pygame.draw.rect(screen, [186, 148, 45], transform_scale([40, 40, 80, 80]), border_radius=br)
        pygame.draw.rect(screen, [0, 0, 0], transform_scale([40, 40, 80, 80]), br, br)
        text(screen, "返回", [0, 0, 0], 20, transform_scale([80, 80]), "center")

        pygame.draw.rect(screen, [128, 128, 128], transform_scale([880, 140, 480, 680]), border_radius=br)
        pygame.draw.rect(screen, [0, 0, 0], transform_scale([880, 140, 480, 680]), br, br)

        pos = pygame.mouse.get_pos()
        tar = transform_scale([40, 180, 120, 120])
        for i in range(5):
            for j in range(6):
                if (int((pos[0]-tar[0])/tar[2])==j and int((pos[1]-tar[1])/tar[3])==i and pos[0]-tar[0]>0 and pos[1]-tar[1]>0):
                    if(save["achievement"][i*6+j]):
                        text(screen, achievement_data["unlock_title"][i*6+j], [0, 0, 0], 3*18, transform_scale([1120, 200]), "center")
                        text(screen, achievement_data["unlock_description"][i*6+j], [0, 0, 0], 3*15, transform_scale([1120, 480]), "center")
                        pygame.draw.rect(screen, [178, 250, 178], transform_scale([40+120*j, 180+120*i, 120, 120]), border_radius=br)
                        pygame.draw.rect(screen, [0, 0, 0], transform_scale([40+120*j, 180+120*i, 120, 120]), br, br)
                    else:
                        text(screen, achievement_data["hidden_title"][i*6+j], [0, 0, 0], 3*18, transform_scale([1120, 200]), "center")
                        text(screen, achievement_data["hidden_description"][i*6+j], [0, 0, 0], 3*15, transform_scale([1120, 480]), "center")
                        pygame.draw.rect(screen, [250, 178, 178], transform_scale([40+120*j, 180+120*i, 120, 120]), border_radius=br)
                        pygame.draw.rect(screen, [0, 0, 0], transform_scale([40+120*j, 180+120*i, 120, 120]), br, br)
                        

                else:
                    if(save["achievement"][i*6+j]):
                        pygame.draw.rect(screen, [128, 200, 128], transform_scale([40+120*j, 180+120*i, 120, 120]), border_radius=br)
                        pygame.draw.rect(screen, [0, 0, 0], transform_scale([40+120*j, 180+120*i, 120, 120]), br, br)
                    else:
                        pygame.draw.rect(screen, [200, 128, 128], transform_scale([40+120*j, 180+120*i, 120, 120]), border_radius=br)
                        pygame.draw.rect(screen, [0, 0, 0], transform_scale([40+120*j, 180+120*i, 120, 120]), br, br)

                text_sp(screen, achievement_data["icon"][i*6+j][0], achievement_data["icon"][i*6+j][1], 3*18, transform_scale([100+120*j, 240+120*i]), 255, "center")
        
        


        if(time != 0):
            time += 1
            s.set_alpha(int(time/fps*255))
            screen.blit(s, (0,0))

        if(len(achievement_stack)>0):
            draw_achievemet_stack()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if click_check(pygame.mouse.get_pos(), transform_scale([40, 40, 80, 80])):
                        if(time == 0):
                            time += 1
        
        #  back
        if(time > fps):
            game_state = "menu"
            time=0
                        

    clock.tick(fps)
    pygame.display.update()
