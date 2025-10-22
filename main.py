import pygame, random, os

# draw text on screen
def text(screen, text, color, size, pos, align="left"):
    text = text.encode("utf-8").decode("utf-8")
    try:
        my_font = pygame.font.Font('media/LXGWMarkerGothic-Regular.ttf', size)
    except Exception:
        my_font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = my_font.render(text, True, color)
    if align == "left":
        screen.blit(text_surface, pos)
    elif align == "center" or align == "centre":
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)

def text_sp(screen, text, color, size, pos, alpla, align="left"):
    text = text.encode("utf-8").decode("utf-8")
    try:
        my_font = pygame.font.Font('media/YujiSyuku-Regular.ttf', size)
    except Exception:
        my_font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = my_font.render(text, True, color)
    text_surface.set_alpha(alpla)
    if align == "left":
        screen.blit(text_surface, pos)
    elif align == "center" or align == "centre":
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)

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


def main():
    #basic set up for pygame
    pygame.init()
    pygame.font.init()
    WIDTH, HEIGHT = 1440, 960
    
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((pygame.display.get_desktop_sizes()[0][0]-WIDTH)/2, 20)
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("learn Japanese!")
    clock = pygame.time.Clock()
    fps = 60

    # question bank: verb form convertion
    # size: 27
    choose_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    not_chosen_list = []

    verb_ru = ["いる", "行く", "来る", "帰る", "出掛ける", "する", "食べる", "飲む", "見る", "読む", "書く", "聞く", "買う", "起きる", "寝る", "乗る", "売る", "降(お)りる", "迎える", "会う", "働く", "休む", "入る", "出る", "着る", "履く", "脱ぐ", "座る", "渡る", "通る", "置く", "使う", "刺す", "押す", "話す", "言う", "替える", "走る", "戻る", "泊まる", "止める", "教える", "習う", "泳ぐ", "弾く", "開ける", "閉める", "付ける", "消す", "洗う", "入れる", "取る", "打つ", "作る", "焼く", "歩く", "曲がる"]
    verb_ru_hira = ["いる", "いく", "くる", "かえる", "でかける", "する", "たべる", "のむ", "みる", "よむ", "かく", "きく", "かう", "おきる", "ねる", "のる", "うる", "おりる", "むかえる", "あう", "はたらく", "やすむ", "はいる", "でる", "きる", "はく", "ぬぐ", "すわる", "わたる", "とおる", "おく", "つかう", "さす", "おす", "はなす", "いう", "かえる", "はしる", "もどる", "とまる", "やむ", "おしえる", "ならう", "およぐ", "ひく", "あける", "しめる", "つける", "けす", "あらう", "いれる", "とる", "うつ", "つくる", "やく", "あるく", "まがる"]

    verb_masu = ["います", "行きます", "来ます", "帰ります", "出掛けます", "します", "食べます", "飲みます", "見ます", "読みます", "書きます", "聞きます", "買います", "起きます", "寝ます", "乗ります", "売ります", "降(お)ります", "迎えます", "会います", "働きます", "休みます", "入ります", "出ます", "着ます", "穿きます", "脱ぎます", "座ります", "渡ります", "通ります", "置きます", "使います", "挿します", "押します", "話します", "言います", "替えます", "走ります", "戻ります", "泊まります", "止めます", "教えます", "習います", "泳ぎます", "弾きます", "開けます", "閉めます", "つけます", "消します", "洗います", "入れます", "取ります", "打ちます", "作ります", "焼きます", "歩きます", "曲がります"]
    verb_masu_hira = ["います", "いきます", "きます", "かえります", "でかけます", "します", "たべます", "のみます", "みます", "よみます", "かきます", "ききます", "かいます", "おきます", "ねます", "のります", "うります", "おります", "むかえます", "あいます", "はたらきます", "やすみます", "はいります", "でます", "きます", "はきます", "ぬぎます", "すわります", "わたります", "とおります", "おきます", "つかいます", "さしいます", "おします", "はなします", "いいます", "かえます", "はしります", "もどります", "とまります", "やめます", "おしえます", "なります", "およぎます", "ひきます", "あけます", "しめます", "つけます", "けします", "あらいます", "いれます", "とります", "うちます", "つくります", "やきます", "あるきます", "まがります"]

    verb_te = ["いって", "行って", "来て", "帰って", "出掛けて", "して", "食べて", "飲んで", "見て", "読んで", "書いて", "聞いて", "買って", "起きて", "寝て", "乗って", "売って", "降(お)りて", "迎えて", "会って", "働いて", "休んで", "入って", "出て", "着て", "履いて", "脱いで", "座って", "渡って", "通って", "置いて", "使って", "刺して", "押して", "話して", "言って", "替えて", "走って", "戻って", "泊まって", "止めて", "教えて", "習って", "泳いで", "弾いて", "開けて", "閉めて", "付けて", "消して", "洗って", "入れて", "取って", "打って", "作って", "焼いて", "歩いて", "曲がって"]
    verb_te_hira = ["いって", "いって", "きて", "かえって", "でかけて", "して", "たべて", "のんで", "みて", "よんで", "かいて", "きいて", "かって", "おきて", "ねて", "のって", "うって", "おりて", "むかえて", "あって", "はたらいて", "やすんで", "はいって", "でて", "きて", "はいて", "ぬいで", "すわって", "わたって", "とおって", "おいて", "つかって", "さして", "おして", "はなして", "いって", "かえて", "はしって", "もどって", "とまって", "やめて", "おしえて", "ならって", "およいで", "ひいて", "あけて", "しめて", "つけて", "けして", "あらって", "いれて", "とって", "うって", "つくって", "やいて", "あるいて", "まがって"]

    verb_ta = ["いた", "行った", "来た", "帰った", "出掛けた", "した", "食べた", "飲んだ", "見た", "読んだ", "書いた", "聞いた", "買った", "起きた", "寝た", "乗った", "売った", "降(お)りた", "迎えた", "会った", "働いた", "休んだ", "入った", "出た", "着た", "履いた", "脱いだ", "座った", "渡った", "通った", "置いた", "使った", "刺した", "押した", "話した", "言った", "替えた", "走った", "戻った", "泊まった", "止めた", "教えた", "習った", "泳いだ", "弾いた", "開けた", "閉めた", "付けた", "消した", "洗った", "入れた", "取った", "打った", "作った", "焼いた", "歩いた", "曲がった"]
    verb_ta_hira = ["いた", "いった", "きた", "かえった", "でかけた", "した", "たべた", "のんだ", "みた", "よんだ", "かいた", "きいた", "かった", "おきた", "ねた", "のった", "うった", "おりた", "むかえた", "あった", "はたらいた", "やすんだ", "はいった", "でた", "きた", "はいた", "ぬいだ", "すわった", "わたった", "とおった", "おいた", "つかった", "さした", "おした", "はなした", "いった", "かえた", "はしった", "もどった", "とまった", "やんだ", "おしえた", "ならった", "およいだ", "ひいた", "あけた", "しめた", "つけた", "けした", "あらった", "いれた", "とった", "うった", "つくった", "やいた", "あるいた", "まがった"]

    verb_nai = ["いない", "行かない", "来ない", "帰らない", "出掛けない", "しない", "食べない", "飲まない", "見ない", "読まない", "書かない", "聞かない", "買わない", "起きない", "寝ない", "乗らない", "売らない", "降(お)りない", "迎えない", "会わない", "働かない", "休まない", "入らない", "出ない", "着ない", "履かない", "脱がない", "座らない", "渡らない", "通らない", "置かない", "使わない", "刺さない", "押さない", "話さない", "言わない", "替えない", "走らない", "戻らない", "泊まらない", "止めない", "教えない", "習わない", "泳がない", "弾かない", "開けない", "閉めない", "付けない", "消さない", "洗わない", "入れない", "取らない", "打たない", "作らない", "焼かない", "歩かない", "曲がらない"]
    verb_nai_hira = ["いない", "いかない", "こない", "かえらない", "でかけない", "しない", "たべない", "のまない", "みない", "よまない", "かかない", "きかない", "かわない", "おきない", "ねない", "のらない", "うらない", "おりない", "むかえない", "あわない", "はたらかない", "やすまない", "はいらない", "でない", "こない", "きない", "はかない", "ぬがない", "すわらない", "わたらない", "とおらない", "おかない", "つかわない", "ささない", "おさない", "はなさない", "いわない", "かえない", "はしらない", "もどらない", "とまらない", "やめない", "おしえない", "ならわない", "およがない", "ひかない", "あけない", "しめない", "つけない", "けさない", "あらわない", "いれない", "とらない", "うたない", "つくらない", "やかない", "あるかない", "まがらない"]

    verb_ikou = ["いよう", "行こう", "来よう", "帰ろう", "出掛けよう", "しよう", "食べよう", "飲もう", "見よう", "読もう", "書こう", "聞こう", "買おう", "起きよう", "寝よう", "乗ろう", "売ろう", "降(お)りよう", "迎えよう", "会おう", "働こう", "休もう", "入ろう", "出よう", "着よう", "履こう", "脱ごう", "座ろう", "渡ろう", "通ろう", "置こう", "使おう", "刺そう", "押そう", "話そう", "言おう", "替えよう", "走ろう", "戻ろう", "泊まろう", "止めよう", "教えよう", "習おう", "泳ごう", "弾こう", "開けよう", "閉めよう", "付けよう", "消そう", "洗おう", "入れよう", "取ろう", "打とう", "作ろう", "焼こう", "歩こう", "曲がろう"]
    verb_ikou_hira = ["いよう", "いこう", "こよう", "かえろう", "でかけよう", "しよう", "たべよう", "のもう", "みよう", "よもう", "かこう", "きこう", "かおう", "おきよう", "ねよう", "のろう", "うろう", "おりよう", "むかえよう", "あおう", "はたらこう", "やすもう", "はいろう", "でよう", "きよう", "きよう", "はこう", "ぬごう", "すわろう", "わたろう", "とおろう", "おこう", "つかおう", "さそう", "おそう", "はなそう", "いおう", "かえよう", "はしろう", "もどろう", "とまろう", "やめよう", "おしえよう", "ならおう", "およごう", "ひこう", "あけよう", "しめよう", "つけよう", "けそう", "あらおう", "いれよう", "とろう", "うとう", "つくろう", "やこう", "あるこう", "まがろう"]

    verb_kanou = ["いられる", "行ける", "来られる", "帰れる", "出掛けられる", "できる", "食べられる", "飲める", "見られる", "読める", "書ける", "聞ける", "買える", "起きられる", "寝られる", "乗れる", "売れる", "降(お)りられる", "迎えられる", "会える", "働ける", "休める", "入れる", "出られる", "着られる", "履ける", "脱げる", "座れる", "渡れる", "通れる", "置ける", "使える", "刺せる", "押せる", "話せる", "言える", "替えられる", "走れる", "戻れる", "泊まれる", "止められる", "教えられる", "習える", "泳げる", "弾ける", "開けられる", "閉められる", "付けられる", "消せる", "洗える", "入れられる", "取れる", "打てる", "作れる", "焼ける", "歩ける", "曲がれる"]
    verb_kanou_hira = ["いられる", "いける", "こられる", "かえれる", "でかけられる", "できる", "たべられる", "のめる", "みられる", "よめる", "かける", "きける", "かえる", "おきられる", "ねられる", "のれる", "うれる", "おりられる", "むかえられる", "あえる", "はたらける", "やすめる", "はいれる", "でられる", "きられる", "きれる", "はける", "ぬげる", "すわれる", "わたれる", "とおれる", "おける", "つかえる", "させる", "おせる", "はなせる", "いえる", "かえられる", "はしれる", "もどれる", "とまれる", "やめられる", "おしえられる", "ならえる", "およげる", "ひける", "あけられる", "しめられる", "つけられる", "けせる", "あらえる", "いれられる", "とれる", "うてる", "つくれる", "やける", "あるける", "まがれる"]

    verb_ba = ["いれば", "行けば", "来れば", "帰れば", "出掛ければ", "すれば", "食べれば", "飲めば", "見れば", "読めば", "書けば", "聞けば", "買えば", "起きれば", "寝れば", "乗れば", "売れば", "降(お)りれば", "迎えれば", "会えば", "働けば", "休めば", "入れば", "出れば", "着れば", "履けば", "脱げば", "座れば", "渡れば", "通れば", "置けば", "使えば", "刺せば", "押せば", "話せば", "言えば", "替えれば", "走れば", "戻れば", "泊まれば", "止められれば", "教えれば", "習えば", "泳げば", "弾けば", "開ければ", "閉めれば", "付ければ", "消せば", "洗えば", "入れれば", "取れば", "打てば", "作れば", "焼けば", "歩けば", "曲がれば"]
    verb_ba_hira = ["いれば", "いけば", "これば", "かえれば", "でかければ", "すれば", "たべれば", "のめば", "みれば", "よめば", "かけば", "きけば", "かえば", "おきれば", "ねれば", "のれば", "うれば", "おりれば", "むかえれば", "あえば", "はたらけば", "やすめば", "はいれば", "でれば", "きれば", "きれば", "はけば", "ぬげば", "すわれば", "わたれば", "とおれば", "おけば", "つかえば", "させば", "おせば", "はなせば", "いえば", "かえれば", "はしれば", "もどれば", "とまれば", "やめれば", "おしえれば", "ならえば", "およげば", "ひけば", "あければ", "しめれば", "つければ", "けせば", "あらえば", "いれれば", "とれば", "うてば", "つくれば", "やけば", "あるけば", "まがれば"]

    verb_ro = ["いろ", "行け", "来い", "帰れ", "出掛けろ", "しろ", "食べろ", "飲め", "見ろ", "読め", "書け", "聞け", "買え", "起きろ", "寝ろ", "乗れ", "売れ", "降(お)りろ", "迎えろ", "会え", "働け", "休め", "入れ", "出ろ", "着ろ", "履け", "脱げ", "座れ", "渡れ", "通れ", "置け", "使え", "刺せ", "押せ", "話せ", "言え", "替えろ", "走れ", "戻れ", "泊まれ", "止められろ", "教えろ", "習え", "泳げ", "弾け", "開けろ", "閉めろ", "付けろ", "消せ", "洗え", "入れろ", "取れ", "打て", "作れ", "焼けろ", "歩け", "曲がれ"]
    verb_ro_hira = ["いろ", "いけ", "こい", "かえれ", "でかけろ", "しろ", "たべろ", "のめ", "みろ", "よめ", "かけ", "きけ", "かえ", "おきろ", "ねろ", "のれ", "うれ", "おりろ", "むかえろ", "あえ", "はたらけ", "やすめ", "はいれ", "でろ", "きろ", "きれ", "はけ", "ぬげ", "すわれ", "わたれ", "とおれ", "おけ", "つかえ", "させ", "おせ", "はなせ", "いえ", "かえろ", "はしれ", "もどれ", "とまれ", "やめろ", "おしえろ", "ならえ", "およげ", "ひけ", "あけろ", "しめろ", "つけろ", "けせ", "あらえ", "いれろ", "とれ", "うて", "つくれ", "やけろ", "あるけ", "まがれ"]

    verb_na = ["いるな", "行くな", "来るな", "帰るな", "出掛けるな", "するな", "食べるな", "飲むな", "見るな", "読むな", "書くな", "聞くな", "買うな", "起きるな", "寝るな", "乗るな", "売るな", "降(お)りるな", "迎えるな", "会うな", "働くな", "休むな", "入るな", "出るな", "着るな", "履くな", "脱ぐな", "座るな", "渡るな", "通るな", "置くな", "使うな", "刺すな", "押すな", "話すな", "言うな", "替えるな", "走るな", "戻るな", "泊まるな", "止められるな", "教えるな", "習うな", "泳ぐな", "弾くな", "開けるな", "閉めるな", "付けるな", "消すな", "洗うな", "入れるな", "取るな", "打つな", "作るな", "焼けるな", "歩くな", "曲がるな"]
    verb_na_hira = ["いるな", "いくな", "くるな", "かえるな", "でかけるな", "するな", "たべるな", "のむな", "みるな", "よむな", "かくな", "きくな", "かうな", "おきるな", "ねるな", "のるな", "うるな", "おりるな", "むかえるな", "あうな", "はたらくな", "やすむな", "はいるな", "でるな", "きるな", "きるな", "はくな", "ぬぐな", "すわるな", "わたるな", "とおるな", "おくな", "つかうな", "させな", "おすな", "はなすな", "いうな", "かえるな", "はしるな", "もどるな", "とまるな", "やめるな", "おしえるな", "ならうな", "およぐな", "ひくな", "あけるな", "しめるな", "つけるな", "けすな", "あらうな", "いれるな", "とるな", "うつな", "つくるな", "やけるな", "あるくな", "まがるな"]

    verb_rareru = ["いられる", "行かれる", "来られる", "帰られる", "出掛けられる", "される", "食べられる", "飲まれる", "見られる", "読まれる", "書かれる", "聞かれる", "買われる", "起きられる", "寝られる", "乗られる", "売られる", "降(お)りられる", "迎えられる", "会われる", "働かれる", "休まれる", "入られる", "出られる", "着られる", "履かれる", "脱がれる", "座られる", "渡られる", "通られる", "置かれる", "使われる", "刺される", "押される", "話される", "言われる", "替えられる", "走られる", "戻られる", "泊まられる", "止められる", "教えられる", "習われる", "泳がれる", "弾かれる", "開けられる", "閉められる", "付けられる", "消される", "洗われる", "入れられる", "取られる", "打たれる", "作られる", "焼かれる", "歩かれる", "曲げられる"]
    verb_rareru_hira = ["いられる", "いかれる", "こられる", "かえられる", "でかけられる", "される", "たべられる", "のまれる", "みられる", "よまれる", "かかれる", "きかれる", "かわれる", "おきられる", "ねられる", "のられる", "うられる", "おりられる", "むかえられる", "あわれる", "はたらかれる", "やすまれる", "はいられる", "でられる", "きられる", "きられる", "はかれる", "ぬがれる", "すわられる", "わたられる", "とおられる", "おかれる", "つかわれる", "される", "おされる", "はなされる", "いわれる", "かえられる", "はされる", "もどられる", "とまられる", "やめられる", "おしえられる", "ならわれる", "およがれる", "ひかれる", "あけられる", "しめられる", "つけられる", "keされる", "あられる", "いれられる", "とられる", "うたれる", "つくられる", "やかれる", "あるかれる", "まげられる"]

    verb_saseru = ["いらせる", "行かせる", "来させる", "帰らせる", "出掛けさせる", "させる", "食べさせる", "飲ませる", "見させる", "読ませる", "書かせる", "聞かせる", "買わせる", "起きさせる", "寝させる", "乗らせる", "売らせる", "降(お)りさせる", "迎えさせる", "会わせる", "働かせる", "休ませる", "入らせる", "出させる", "着させる", "履かせる", "脱がせる", "座らせる", "渡らせる", "通らせる", "置かせる", "使わせる", "刺させる", "押させる", "話させる", "言わせる", "替えさせる", "走らせる", "戻らせる", "泊まらせる", "止めさせる", "教えさせる", "習わせる", "泳がせる", "弾かせる", "開けさせる", "閉めさせる", "付けさせる", "消させる", "洗わせる", "入れさせる", "取らせる", "打たせる", "作らせる", "焼かせる", "歩かせる", "曲げさせる"]
    verb_saseru_hira = ["いらせる", "いかせる", "こさせる", "かえらせる", "でかけさせる", "させる", "たべさせる", "のませる", "みさせる", "よませる", "かかせる", "きかせる", "かわせる", "おきさせる", "ねさせる", "のらせる", "うらせる", "おりさせる", "むかえさせる", "あわせる", "はたらかせる", "やすませる", "はいらせる", "ださせる", "きさせる", "きさせる", "はかせる", "ぬがせる", "すわらせる", "わたらせる", "とおらせる", "おかせる", "つかわせる", "させる", "おさせる", "はなさせる", "いわせる", "かえさせる", "はさせる", "もどらせる", "とまらせる", "やめさせる", "おしえさせる", "ならわせる", "およがせる", "ひかせる", "あけさせる", "しめさせる", "つけさせる", "keさせる", "あらわせる", "いれさせる", "とらせる", "うたせる", "つくらせる", "やかせる", "あるかせる", "まげさせる"]

    verb_saseru_rareru = ["いらせられる", "行かせられる", "来させられる", "帰らせられる", "出掛けさせられる", "させられる", "食べさせられる", "飲ませられる", "見させられる", "読ませられる", "書かせられる", "聞かせられる", "買わせられる", "起きさせられる", "寝させられる", "乗らせられる", "売らせられる", "降(お)りさせられる", "迎えさせられる", "会わせられる", "働かせられる", "休ませられる", "入らせられる", "出させられる", "着させられる", "履かせられる", "脱がせられる", "座らせられる", "渡らせられる", "通らせられる", "置かせられる", "使わせられる", "刺させられる", "押させられる", "話させられる", "言わせられる", "替えさせられる", "走らせられる", "戻らせられる", "泊まらせられる", "止めさせられる", "教えさせられる", "習わせられる", "泳がせられる", "弾かせられる", "開けさせられる", "閉めさせられる", "付けさせられる", "消させられる", "洗わせられる", "入れさせられる", "取らせられる", "打たせられる", "作らせられる", "焼かせられる", "歩かせられる", "曲げさせられる"]
    verb_saseru_rareru_hira = ["いらせられる", "いかせられる", "こさせられる", "かえらせられる", "でかけさせられる", "させられる", "たべさせられる", "のませられる", "みさせられる", "よませられる", "かかせられる", "きかせられる", "かわせられる", "おきさせられる", "ねさせられる", "のらせられる", "うらせられる", "おりさせられる", "むかえさせられる", "あわせられる", "はたらかせられる", "やすませられる", "はいらせられる", "ださせられる", "きさせられる", "きさせられる", "はかせられる", "ぬがせられる", "すわらせられる", "わたらせられる", "とおらせられる", "おかせられる", "つかわせられる", "させられる", "おさせられる", "はなさせられる", "いわせられる", "かえさせられる", "はさせられる", "もどらせられる", "とまらせられる", "やめさせられる", "おしえさせられる", "ならわせられる", "およがせられる", "ひかせられる", "あけさせられる", "しめさせられる", "つけさせられる", "keさせられる", "あらわせられる", "いれさせられる", "とらせられる", "うたせられる", "つくらせられる", "やかせられる", "あるかせられる", "まげさせられる"]

    # basic initialize of variables for the game loop
    game_state = "menu"
    running = True
    inputArr = ""
    outputArr = ""
    no_of_qs = 3
    no_of_heart = 3
    heart = pygame.image.load("media/heart.png").convert_alpha()
    heart = pygame.transform.scale(heart, [32, 32])

    kara = "masu"
    made = "masu"
    verb = ""
    pause = False
    temptime = pygame.time.get_ticks()
    score = 0
    prevScore = 0
    time = 0
    images = [
        pygame.transform.scale(pygame.image.load("media/dungeon_crystal_1.png"), [WIDTH, HEIGHT]),  # 0
        pygame.transform.scale(pygame.image.load("media/title_text.png"), [816, 144]),              # 1
        pygame.transform.scale(pygame.image.load("media/press_to_start.png"), [269, 36]),           # 2
        pygame.transform.scale(pygame.image.load("media/forest_1.png"), [WIDTH, HEIGHT]),           # 3
        pygame.transform.scale(pygame.image.load("media/main_char.png"), [640, 768]),               # 4
        pygame.transform.scale(pygame.image.load("media/teacher_no_glasses.png"), [517, 680]),      # 5
        pygame.transform.scale(pygame.image.load("media/skip.png"), [310, 80]),                     # 6
        pygame.transform.scale(pygame.image.load("media/main_char_gray.png"), [640, 768]),          # 7
        pygame.transform.scale(pygame.image.load("media/teacher_no_glasses_gray.png"), [517, 680]), # 8
        pygame.transform.scale(pygame.image.load("media/purple_slime_1.png"), [532, 572]),          # 9
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
            (2, "莉子：\n不管了，讓我先開始教你吧！"),
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
    ]
    # 0: both gray; 1: left talking; 2: right talking; 3: both talking
    story_num = 0
    dialog_num = 0
    

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
            "num_of_qs": 10,
            "order": [],
            "enemy_surf": pygame.transform.flip(images[9], flip_x=True, flip_y=False)
            
        }
    ]
    player_hp = 100
    enemy_hp = 100
    stage = 0
    question_num = 0
    
    def battle_hp_init():
        player_hp = 100
        enemy_hp = 100
        battle_detail[stage]["order"] = [random.randint(0, len(battle_detail[stage]["question"])-1) for _ in range(battle_detail[stage]["num_of_qs"])]
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

            # play button
            screen.blit(images[2], (586, 787))
            
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

            if(time > fps*2):
                game_state = "story"
                story_num = 0
                dialog_num = 0
                time = 0
                
            
        if game_state == "story":
            if dialog_num == len(dialog[story_num]):
                time = 0

                # inputing = False
                # qs_answered = 0
                # score = 0
                # inputArr = ""
                # outputArr = ""
                # game_state = "select_kara"
                # no_of_heart = 3

                game_state = "playing"
                battle_hp_init()
                stage = 0
                random.shuffle(battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1])
            else:
                # BG image
                screen.blit(images[3], (0, 0))

                # left character
                talking = int(dialog[story_num][dialog_num][0])
                if talking == 1 or talking == 0:
                    screen.blit(images[4], (-139, 218))
                else:
                    screen.blit(images[7], (-139, 218))

                # right character
                if talking == 2 or talking == 0:
                    screen.blit(images[5], (1013, 280))
                else:
                    screen.blit(images[8], (1013, 280))

                # skip button
                screen.blit(images[6], (1111, 35))

                # dialog box
                pygame.draw.rect(screen, pygame.Color("#e8e8e8"), [123, 766, 1193, 184], border_radius=5)
                text(screen, dialog[story_num][dialog_num][1], (0, 0, 0), 48, [153, 776])

                # effect
                if (dialog[story_num][dialog_num][0] == 1.1):
                    if(time > 0):
                        time += 1
                        text_sp(screen, "あ", (120, 0, 0), 200, [WIDTH/2, HEIGHT/2], int((fps*2-time)/(fps*2)*255), "center")
                    elif(time >= fps*2):
                        time = 0
                    

                for event in pygame.event.get():
                    # allow close game
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0]:
                            if click_check(pygame.mouse.get_pos(), [1111, 35, images[6].get_width(), images[6].get_height()]):
                                dialog_num = len(dialog[story_num])
                            else:
                                dialog_num += 1
                                if dialog_num != len(dialog[story_num]):
                                    if dialog[story_num][dialog_num][0] == 1.1:
                                        time = 1

        if game_state == "playing":
            if battle_detail[stage]["question_type"] == "MC":
                # BG image
                screen.blit(images[3], (0, 0))

                # right character
                screen.blit(pygame.transform.flip(images[4], flip_x=True, flip_y=False), (959, 263))
                pygame.draw.rect(screen, pygame.Color("#d9d9d9"), [1130, 0, 310, 80])
                text(screen, "HP", (0, 0, 0), 24, [1158, 22])
                pygame.draw.rect(screen, (0, 0, 0), [1209, 34, 204, 13])
                pygame.draw.rect(screen, (255, 0, 0), [1209, 34, player_hp/100*204, 13])
                

                # left enemy
                screen.blit(battle_detail[stage]["enemy_surf"], (-51, 100))
                pygame.draw.rect(screen, pygame.Color("#d9d9d9"), [0, 0, 310, 80])
                text(screen, "HP", (0, 0, 0), 24, [28, 22])
                pygame.draw.rect(screen, (0, 0, 0), [79, 34, 204, 13])
                pygame.draw.rect(screen, (255, 0, 0), [79, 34, enemy_hp/100*204, 13])

                pygame.draw.rect(screen, pygame.Color("#d9d9d9"), [324, 552, 791, 408])
                pygame.draw.rect(screen, pygame.Color("#ececec"), [407, 729, 194, 94])
                pygame.draw.rect(screen, pygame.Color("#ececec"), [840, 729, 194, 94])
                pygame.draw.rect(screen, pygame.Color("#ececec"), [407, 842, 194, 94])
                pygame.draw.rect(screen, pygame.Color("#ececec"), [840, 842, 194, 94])

                text(screen, battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]], (0, 0, 0), 64, [688, 601], "center")
                
                text(screen, battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][0], (0, 0, 0), 64, [504, 776], "center")
                text(screen, battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][1], (0, 0, 0), 64, [937, 776], "center")
                text(screen, battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][2], (0, 0, 0), 64, [504, 889], "center")
                text(screen, battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1][3], (0, 0, 0), 64, [937, 889], "center")

                for event in pygame.event.get():
                    # allow close game
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            question_num += 1
                        if question_num >= battle_detail[stage]["num_of_qs"]:
                            game_state = "menu"
                        else:
                            random.shuffle(battle_detail[stage]["answer"][battle_detail[stage]["question"][battle_detail[stage]["order"][question_num]]][1])



            else:
                for event in pygame.event.get():
                    # allow close game
                    if event.type == pygame.QUIT:
                        running = False
                    # set up in-game keyboard input
                    if event.type == pygame.KEYDOWN and pause == False:
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
                        if event.key == pygame.K_RETURN:
                            temptime = pygame.time.get_ticks()
                            pause = True
                            inputing = False
                            qs_answered += 1
                            # check()
                            prevScore = score
                            if made == "jisyo" and outputArr == verb_ru_hira[choise]:
                                score += 1
                            elif made == "masu" and outputArr == verb_masu_hira[choise]:
                                score += 1
                            elif made == "te" and outputArr == verb_te_hira[choise]:
                                score += 1
                            elif made == "ta" and outputArr == verb_ta_hira[choise]:
                                score += 1
                            elif made == "nai" and outputArr == verb_nai_hira[choise]:
                                score += 1

                            elif made == "kanou" and outputArr == verb_kanou_hira[choise]:
                                score += 1
                            elif made == "tiugin" and outputArr == verb_ba_hira[choise]:
                                score += 1
                            elif made == "mingling" and outputArr == verb_ro_hira[choise]:
                                score += 1
                            elif made == "jiheung" and outputArr == verb_ikou_hira[choise]:
                                score += 1
                            elif made == "gamji" and outputArr == verb_na_hira[choise]:
                                score += 1

                            elif made == "sausan" and outputArr == verb_rareru_hira[choise]:
                                score += 1
                            elif made == "siyik" and outputArr == verb_saseru_hira[choise]:
                                score += 1
                            elif made == "siyiksausan" and outputArr == verb_saseru_rareru_hira[choise]:
                                score += 1

                            screen.fill((135, 206, 235))

                            # back button
                            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [64-12, 64, 64, 30])
                            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [66-12, 66, 64-4, 30-4])
                            text(screen, "戻る", (0, 0, 0), 16, (64+64/2-12, 64+32/2), "center")

                            # input box (english)
                            text_input_box = pygame.draw.rect(screen, (200, 200, 200), [200, 250, 400, 64])
                            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [202, 252, 396, 60])
                            text(screen, inputArr, (255, 255, 255), 24, (206, 256))

                            # input box (japanese)
                            text_input_box = pygame.draw.rect(screen, (200, 200, 200), [200, 250 + 96, 400, 64])
                            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [202, 252 + 96, 396, 60])
                            text(screen, outputArr, (255, 255, 255), 24, (206, 256 + 96))

                            if kara == "jisyo":
                                verb = verb_ru[choise]
                            elif kara == "masu":
                                verb = verb_masu[choise]
                            elif kara == "te":
                                verb = verb_te[choise]
                            elif kara == "ta":
                                verb = verb_ta[choise]
                            elif kara == "nai":
                                verb = verb_nai[choise]

                            elif kara == "kanou":
                                verb = verb_kanou[choise]
                            elif kara == "tiugin":
                                verb = verb_ba[choise]
                            elif kara == "mingling":
                                verb = verb_ro[choise]
                            elif kara == "jiheung":
                                verb = verb_ikou[choise]
                            elif kara == "gamji":
                                verb = verb_na[choise]

                            elif kara == "sausan":
                                verb = verb_rareru[choise]
                            elif kara == "siyik":
                                verb = verb_saseru[choise]
                            elif kara == "siyiksausan":
                                verb = verb_saseru_rareru[choise]
                                
                            text(screen, str(qs_answered) + ") " + verb, (0, 0, 0), 24, (206, 186))
                            text(screen, "スコア: " + str(score), (0, 0, 0), 24, (550, 120))

                            text1 = ""
                            if kara == "jisyo":
                                text1 = "辞書形"
                            elif kara == "masu":
                                text1 = "ます形"
                            elif kara == "te":
                                text1 = "て形"
                            elif kara == "ta":
                                text1 = "た形"
                            elif kara == "nai":
                                text1 = "ない形"

                            elif kara == "kanou":
                                text1 = "可能形"
                            elif kara == "tiugin":
                                text1 = "条件形"
                            elif kara == "mingling":
                                text1 = "命令形"
                            elif kara == "jiheung":
                                text1 = "意向形"
                            elif kara == "gamji":
                                text1 = "禁止形"

                            elif kara == "sausan":
                                text1 = "受身形"
                            elif kara == "siyik":
                                text1 = "使役形"
                            elif kara == "siyiksausan":
                                text1 = "使役受身形"

                            text2 = ""
                            if made == "jisyo":
                                text2 = "辞書形"
                            elif made == "masu":
                                text2 = "ます形"
                            elif made == "te":
                                text2 = "て形"
                            elif made == "ta":
                                text2 = "た形"
                            elif made == "nai":
                                text2 = "ない形"

                            elif made == "kanou":
                                text2 = "可能形"
                            elif made == "tiugin":
                                text2 = "条件形"
                            elif made == "mingling":
                                text2 = "命令形"
                            elif made == "jiheung":
                                text2 = "意向形"
                            elif made == "gamji":
                                text2 = "禁止形"

                            elif made == "sausan":
                                text2 = "受身形"
                            elif made == "siyik":
                                text2 = "使役形"
                            elif made == "siyiksausan":
                                text2 = "使役受身形"

                            text(screen, text1 + "から、" + text2 + "まで", (0, 0, 0), 48, (128, 64))

                            if score - prevScore == 1:
                                pygame.draw.circle(screen, (255, 50, 50), (WIDTH - 128, HEIGHT/2), 48)
                                pygame.draw.circle(screen, (135, 206, 235), (WIDTH - 128, HEIGHT/2), 32)
                            else:
                                pygame.draw.line(screen, (255, 50, 50), [WIDTH - 128-48, HEIGHT/2-48], [WIDTH - 128+48, HEIGHT/2+48], 16)
                                pygame.draw.line(screen, (255, 50, 50), [WIDTH - 128+48, HEIGHT/2-48], [WIDTH - 128-48, HEIGHT/2+48], 16)

                            if score - prevScore != 1:
                                no_of_heart -= 1

                            #heart
                            for i in range(no_of_heart):
                                screen.blit(heart, (128 + 32 * i, 120))

                            pygame.display.update()
                            # pygame.time.wait(1000)

                            
                            inputArr = ""
                            outputArr = ""
                                
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        # all button action will be set up here
                        if click_check(pos, [64-12, 64, 64, 30]):
                            game_state = "menu"

                # game bg color
                screen.fill((135, 206, 235))

                # the game will stop for 1 second after user answered a question, for let them view whether that question is correct or wrong
                if(pygame.time.get_ticks()-temptime>= 1000):
                    pause = False
                else:
                    # draw the correct symbol: O; and wrong symbol: X
                    if score - prevScore == 1:
                        pygame.draw.circle(screen, (255, 50, 50), (WIDTH - 128, HEIGHT/2), 48)
                        pygame.draw.circle(screen, (135, 206, 235), (WIDTH - 128, HEIGHT/2), 32)
                    else:
                        pygame.draw.line(screen, (255, 50, 50), [WIDTH - 128-48, HEIGHT/2-48], [WIDTH - 128+48, HEIGHT/2+48], 16)
                        pygame.draw.line(screen, (255, 50, 50), [WIDTH - 128+48, HEIGHT/2-48], [WIDTH - 128-48, HEIGHT/2+48], 16)

                # draw heart, here use screen blit to paste a pygame.Surface to screen. transparent png image must use this.
                for i in range(no_of_heart):
                    screen.blit(heart, (128 + 32 * i, 120))

                # back button
                text_input_box = pygame.draw.rect(screen, (20, 20, 20), [64-12, 64, 64, 30])
                text_input_box = pygame.draw.rect(screen, (140, 235, 52), [66-12, 66, 64-4, 30-4])
                text(screen, "戻る", (0, 0, 0), 16, (64+64/2-12, 64+32/2), "center")

                # input box (english)
                text_input_box = pygame.draw.rect(screen, (200, 200, 200), [200, 250, 400, 64])
                text_input_box = pygame.draw.rect(screen, (20, 20, 20), [202, 252, 396, 60])
                text(screen, inputArr, (255, 255, 255), 24, (206, 256))

                # input box (japanese)
                text_input_box = pygame.draw.rect(screen, (200, 200, 200), [200, 250 + 96, 400, 64])
                text_input_box = pygame.draw.rect(screen, (20, 20, 20), [202, 252 + 96, 396, 60])
                text(screen, outputArr, (255, 255, 255), 24, (206, 256 + 96))
                
                # generate new qs
                if inputing == False and qs_answered < no_of_qs and pause == False:
                    not_chosen_list = []
                    for i in range(len(choose_list)):
                        if choose_list[i] == 0:
                            not_chosen_list.append(i)
                    choise = random.choice(not_chosen_list)
                    choose_list[choise] = 1
                    inputing = True

                # let variable verb be the answer            
                if kara == "jisyo":
                    verb = verb_ru[choise]
                elif kara == "masu":
                    verb = verb_masu[choise]
                elif kara == "te":
                    verb = verb_te[choise]
                elif kara == "ta":
                    verb = verb_ta[choise]
                elif kara == "nai":
                    verb = verb_nai[choise]

                elif kara == "kanou":
                    verb = verb_kanou[choise]
                elif kara == "tiugin":
                    verb = verb_ba[choise]
                elif kara == "mingling":
                    verb = verb_ro[choise]
                elif kara == "jiheung":
                    verb = verb_ikou[choise]
                elif kara == "gamji":
                    verb = verb_na[choise]

                elif kara == "sausan":
                    verb = verb_rareru[choise]
                elif kara == "siyik":
                    verb = verb_saseru[choise]
                elif kara == "siyiksausan":
                    verb = verb_saseru_rareru[choise]

                # draw the question text on screen
                if(pause):
                    text(screen, str(qs_answered) + ") " + verb, (0, 0, 0), 24, (206, 186))
                else:
                    text(screen, str(qs_answered+1) + ") " + verb, (0, 0, 0), 24, (206, 186))

                # score text
                text(screen, "スコア: " + str(score), (0, 0, 0), 24, (550, 120))


                # players' goal is to convert verb in <text1> form into <text2> form, and this is just converting romaji into kanji
                text1 = ""
                if kara == "jisyo":
                    text1 = "辞書形"
                elif kara == "masu":
                    text1 = "ます形"
                elif kara == "te":
                    text1 = "て形"
                elif kara == "ta":
                    text1 = "た形"
                elif kara == "nai":
                    text1 = "ない形"

                elif kara == "kanou":
                    text1 = "可能形"
                elif kara == "tiugin":
                    text1 = "条件形"
                elif kara == "mingling":
                    text1 = "命令形"
                elif kara == "jiheung":
                    text1 = "意向形"
                elif kara == "gamji":
                    text1 = "禁止形"

                elif kara == "sausan":
                    text1 = "受身形"
                elif kara == "siyik":
                    text1 = "使役形"
                elif kara == "siyiksausan":
                    text1 = "使役受身形"

                text2 = ""
                if made == "jisyo":
                    text2 = "辞書形"
                elif made == "masu":
                    text2 = "ます形"
                elif made == "te":
                    text2 = "て形"
                elif made == "ta":
                    text2 = "た形"
                elif made == "nai":
                    text2 = "ない形"

                elif made == "kanou":
                    text2 = "可能形"
                elif made == "tiugin":
                    text2 = "条件形"
                elif made == "mingling":
                    text2 = "命令形"
                elif made == "jiheung":
                    text2 = "意向形"
                elif made == "gamji":
                    text2 = "禁止形"

                elif made == "sausan":
                    text2 = "受身形"
                elif made == "siyik":
                    text2 = "使役形"
                elif made == "siyiksausan":
                    text2 = "使役受身形"

                # show text on screen: from <text1>, to <text2>
                text(screen, text1 + "から、" + text2 + "まで", (0, 0, 0), 48, (128, 64))

                # change game state after win or lose
                if no_of_heart <= 0 and pause == False:
                    game_state = "lost"
                elif qs_answered >= no_of_qs and pause == False:
                    game_state = "showScore"

        # game state for seleting stage: from <text1>
        if game_state == "select_kara":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if click_check(pos, [128, 128, 128, 60]):
                        kara = "masu"
                        game_state = "select_made"
                    if click_check(pos, [128, 128+64, 128, 60]):
                        kara = "jisyo"
                        game_state = "select_made"
                    if click_check(pos, [128, 128+128, 128, 60]):
                        kara = "te"
                        game_state = "select_made"
                    if click_check(pos, [128, 128+128+64, 128, 60]):
                        kara = "ta"
                        game_state = "select_made"
                    if click_check(pos, [128, 128+256, 128, 60]):
                        kara = "nai"
                        game_state = "select_made"

                    if click_check(pos, [128 + 135, 128, 128, 60]):
                        kara = "kanou"
                        game_state = "select_made"
                    if click_check(pos, [128 + 135, 128+64, 128, 60]):
                        kara = "tiugin"
                        game_state = "select_made"
                    if click_check(pos, [128 + 135, 128+128, 128, 60]):
                        kara = "mingling"
                        game_state = "select_made"
                    if click_check(pos, [128 + 135, 128+128+64, 128, 60]):
                        kara = "jiheung"
                        game_state = "select_made"
                    if click_check(pos, [128 + 135, 128+256, 128, 60]):
                        kara = "gamji"
                        game_state = "select_made"

                    if click_check(pos, [128 + 270, 128+64, 128, 60]):
                        kara = "sausan"
                        game_state = "select_made"
                    if click_check(pos, [128 + 270, 128+128, 128, 60]):
                        kara = "siyik"
                        game_state = "select_made"
                    if click_check(pos, [128 + 270, 128+128+64, 128, 60]):
                        kara = "siyiksausan"
                        game_state = "select_made"
                    

            screen.fill((135, 206, 235))

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128, 128, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128+2, 128+2, 128-4, 60-4])
            text(screen, "ます形", (0, 0, 0), 24, (128+64, 128+30), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128, 128+64, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128+2, 128+2+64, 128-4, 60-4])
            text(screen, "辞書形", (0, 0, 0), 24, (128+64, 128+30+64), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128, 128+128, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128+2, 128+2+128, 128-4, 60-4])
            text(screen, "て形", (0, 0, 0), 24, (128+64, 128+30+128), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128, 128+128+64, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128+2, 128+2+128+64, 128-4, 60-4])
            text(screen, "た形", (0, 0, 0), 24, (128+64, 128+30+128+64), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128, 128+256, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128+2, 128+2+256, 128-4, 60-4])
            text(screen, "ない形", (0, 0, 0), 24, (128+64, 128+30+256), "center")


            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 135, 128, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 135 +2, 128+2, 128-4, 60-4])
            text(screen, "可能形", (0, 0, 0), 24, (128 + 135 + 64, 128+30), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 135, 128+64, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 135 +2, 128+2+64, 128-4, 60-4])
            text(screen, "条件形", (0, 0, 0), 24, (128 + 135 + 64, 128+30+64), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 135, 128+128, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 135 +2, 128+2+128, 128-4, 60-4])
            text(screen, "命令形", (0, 0, 0), 24, (128 + 135 + 64, 128+30+128), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 135, 128+128+64, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 135 +2, 128+2+128+64, 128-4, 60-4])
            text(screen, "意向形", (0, 0, 0), 24, (128 + 135 + 64, 128+30+128+64), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 135, 128+256, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 135 +2, 128+2+256, 128-4, 60-4])
            text(screen, "禁止形", (0, 0, 0), 24, (128 + 135 + 64, 128+30+256), "center")


            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 270, 128+64, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 270 + 2, 128+2+64, 128-4, 60-4])
            text(screen, "受身形", (0, 0, 0), 24, (128 + 270 + 64, 128+30+64), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 270, 128+128, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 270 + 2, 128+2+128, 128-4, 60-4])
            text(screen, "使役形", (0, 0, 0), 24, (128 + 270 + 64, 128+30+128), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 270, 128+128+64, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 270 + 2, 128+2+128+64, 128-4, 60-4])
            text(screen, "使役受身形", (0, 0, 0), 24, (128 + 270 + 64, 128+30+128+64), "center")


            text(screen, "から", (0, 0, 0), 48, (128+270+135+64, 128+30+128), "center")

        # game state for seleting stage: to <text2>
        if game_state == "select_made":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if click_check(pos, [128, 128, 128, 60]):
                        made = "masu"
                        game_state = "chooseNumOfQs"
                    if click_check(pos, [128, 128+64, 128, 60]):
                        made = "jisyo"
                        game_state = "chooseNumOfQs"
                    if click_check(pos, [128, 128+128, 128, 60]):
                        made = "te"
                        game_state = "chooseNumOfQs"
                    if click_check(pos, [128, 128+128+64, 128, 60]):
                        made = "ta"
                        game_state = "chooseNumOfQs"
                    if click_check(pos, [128, 128+256, 128, 60]):
                        made = "nai"
                        game_state = "chooseNumOfQs"

                    if click_check(pos, [128 + 135, 128, 128, 60]):
                        made = "kanou"
                        game_state = "chooseNumOfQs"
                    if click_check(pos, [128 + 135, 128+64, 128, 60]):
                        made = "tiugin"
                        game_state = "chooseNumOfQs"
                    if click_check(pos, [128 + 135, 128+128, 128, 60]):
                        made = "mingling"
                        game_state = "chooseNumOfQs"
                    if click_check(pos, [128 + 135, 128+128+64, 128, 60]):
                        made = "jiheung"
                        game_state = "chooseNumOfQs"
                    if click_check(pos, [128 + 135, 128+256, 128, 60]):
                        made = "gamji"
                        game_state = "chooseNumOfQs"

                    if click_check(pos, [128 + 270, 128+64, 128, 60]):
                        made = "sausan"
                        game_state = "chooseNumOfQs"
                    if click_check(pos, [128 + 270, 128+128, 128, 60]):
                        made = "siyik"
                        game_state = "chooseNumOfQs"
                    if click_check(pos, [128 + 270, 128+128+64, 128, 60]):
                        made = "siyiksausan"
                        game_state = "chooseNumOfQs"

            screen.fill((135, 206, 235))

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128, 128, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128+2, 128+2, 128-4, 60-4])
            text(screen, "ます形", (0, 0, 0), 24, (128+64, 128+30), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128, 128+64, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128+2, 128+2+64, 128-4, 60-4])
            text(screen, "辞書形", (0, 0, 0), 24, (128+64, 128+30+64), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128, 128+128, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128+2, 128+2+128, 128-4, 60-4])
            text(screen, "て形", (0, 0, 0), 24, (128+64, 128+30+128), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128, 128+128+64, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128+2, 128+2+128+64, 128-4, 60-4])
            text(screen, "た形", (0, 0, 0), 24, (128+64, 128+30+128+64), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128, 128+256, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128+2, 128+2+256, 128-4, 60-4])
            text(screen, "ない形", (0, 0, 0), 24, (128+64, 128+30+256), "center")


            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 135, 128, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 135 +2, 128+2, 128-4, 60-4])
            text(screen, "可能形", (0, 0, 0), 24, (128 + 135 + 64, 128+30), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 135, 128+64, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 135 +2, 128+2+64, 128-4, 60-4])
            text(screen, "条件形", (0, 0, 0), 24, (128 + 135 + 64, 128+30+64), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 135, 128+128, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 135 +2, 128+2+128, 128-4, 60-4])
            text(screen, "命令形", (0, 0, 0), 24, (128 + 135 + 64, 128+30+128), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 135, 128+128+64, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 135 +2, 128+2+128+64, 128-4, 60-4])
            text(screen, "意向形", (0, 0, 0), 24, (128 + 135 + 64, 128+30+128+64), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 135, 128+256, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 135 +2, 128+2+256, 128-4, 60-4])
            text(screen, "禁止形", (0, 0, 0), 24, (128 + 135 + 64, 128+30+256), "center")


            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 270, 128+64, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 270 + 2, 128+2+64, 128-4, 60-4])
            text(screen, "受身形", (0, 0, 0), 24, (128 + 270 + 64, 128+30+64), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 270, 128+128, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 270 + 2, 128+2+128, 128-4, 60-4])
            text(screen, "使役形", (0, 0, 0), 24, (128 + 270 + 64, 128+30+128), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [128 + 270, 128+128+64, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [128 + 270 + 2, 128+2+128+64, 128-4, 60-4])
            text(screen, "使役受身形", (0, 0, 0), 24, (128 + 270 + 64, 128+30+128+64), "center")


            text(screen, "まで", (0, 0, 0), 48, (128+270+135+64, 128+30+128), "center")

            text1 = ""
            if kara == "jisyo":
                text1 = "辞書形"
            elif kara == "masu":
                text1 = "ます形"
            elif kara == "te":
                text1 = "て形"
            elif kara == "ta":
                text1 = "た形"
            elif kara == "nai":
                text1 = "ない形"

            elif kara == "kanou":
                text1 = "可能形"
            elif kara == "tiugin":
                text1 = "条件形"
            elif kara == "mingling":
                text1 = "命令形"
            elif kara == "jiheung":
                text1 = "意向形"
            elif kara == "gamji":
                text1 = "禁止形"

            elif kara == "sausan":
                text1 = "受身形"
            elif kara == "siyik":
                text1 = "使役形"
            elif kara == "siyiksausan":
                text1 = "使役受身形"
            text(screen, text1 + "から、", (0, 0, 0), 48, (128, 64))

        # difficulty selection
        if game_state == "chooseNumOfQs":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if click_check(pos, [WIDTH/2-128, HEIGHT/2-60/2, 256, 60]):
                        no_of_qs = 5
                        game_state = "start"
                    if click_check(pos, [WIDTH/2-128, HEIGHT/2-60/2+64, 256, 60]):
                        no_of_qs = 10
                        game_state = "start"
                    if click_check(pos, [WIDTH/2-128, HEIGHT/2-60/2+128, 256, 60]):
                        no_of_qs = 25
                        game_state = "start"
            
            screen.fill((135, 206, 235))
            text(screen, "難易度を選択", (0, 0, 0), 48, (WIDTH/2, HEIGHT/2 - 64), "center")

            # 5 button
            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [WIDTH/2-128, HEIGHT/2-60/2, 256, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [WIDTH/2-128+2, HEIGHT/2-60/2+2, 256-4, 60-4])
            text(screen, "簡単: 5つの質問", (0, 0, 0), 24, (WIDTH/2, HEIGHT/2), "center")

            # 10 button
            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [WIDTH/2-128, HEIGHT/2-60/2+64, 256, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [WIDTH/2-128+2, HEIGHT/2-60/2+2+64, 256-4, 60-4])
            text(screen, "中等: 10つの質問", (0, 0, 0), 24, (WIDTH/2, HEIGHT/2+64), "center")

            # 25 button
            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [WIDTH/2-128, HEIGHT/2-60/2+128, 256, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [WIDTH/2-128+2, HEIGHT/2-60/2+2+128, 256-4, 60-4])
            text(screen, "難しい: 25つの質問", (0, 0, 0), 24, (WIDTH/2, HEIGHT/2+128), "center")

            text1 = ""
            if kara == "jisyo":
                text1 = "辞書形"
            elif kara == "masu":
                text1 = "ます形"
            elif kara == "te":
                text1 = "て形"
            elif kara == "ta":
                text1 = "た形"
            elif kara == "nai":
                text1 = "ない形"

            elif kara == "kanou":
                text1 = "可能形"
            elif kara == "tiugin":
                text1 = "条件形"
            elif kara == "mingling":
                text1 = "命令形"
            elif kara == "jiheung":
                text1 = "意向形"
            elif kara == "gamji":
                text1 = "禁止形"

            elif kara == "sausan":
                text1 = "受身形"
            elif kara == "siyik":
                text1 = "使役形"
            elif kara == "siyiksausan":
                text1 = "使役受身形"

            text2 = ""
            if made == "jisyo":
                text2 = "辞書形"
            elif made == "masu":
                text2 = "ます形"
            elif made == "te":
                text2 = "て形"
            elif made == "ta":
                text2 = "た形"
            elif made == "nai":
                text2 = "ない形"

            elif made == "kanou":
                text2 = "可能形"
            elif made == "tiugin":
                text2 = "条件形"
            elif made == "mingling":
                text2 = "命令形"
            elif made == "jiheung":
                text2 = "意向形"
            elif made == "gamji":
                text2 = "禁止形"

            elif made == "sausan":
                text2 = "受身形"
            elif made == "siyik":
                text2 = "使役形"
            elif made == "siyiksausan":
                text2 = "使役受身形"

            text(screen, text1 + "から、" + text2 + "まで", (0, 0, 0), 48, (128, 64))


        # this is game state of winning the game
        if game_state == "showScore":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if click_check(pos, [WIDTH/2-128/2, HEIGHT/2-60/2+128, 128, 60]):
                        game_state = "menu"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_state = "menu"

            screen.fill((135, 206, 235))
            text(screen, "最終スコア: " + str(score) + "/" + str(no_of_qs), (0, 0, 0), 24, (WIDTH/2, HEIGHT/2 - 64), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [WIDTH/2-128/2, HEIGHT/2-60/2+128, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [WIDTH/2-128/2+2, HEIGHT/2-60/2+2+128, 128-4, 60-4])
            text(screen, "戻る", (0, 0, 0), 24, (WIDTH/2, HEIGHT/2+128), "center")

        # this is game state for losing the game
        if game_state == "lost":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if click_check(pos, [WIDTH/2-128/2, HEIGHT/2-60/2+128, 128, 60]):
                        game_state = "menu"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_state = "menu"
                        

            screen.fill((135, 206, 235))
            text(screen, "残念でした。次回も頑張ってください‼", (0, 0, 0), 24, (WIDTH/2, HEIGHT/2 - 64), "center")

            text_input_box = pygame.draw.rect(screen, (20, 20, 20), [WIDTH/2-128/2, HEIGHT/2-60/2+128, 128, 60])
            text_input_box = pygame.draw.rect(screen, (140, 235, 52), [WIDTH/2-128/2+2, HEIGHT/2-60/2+2+128, 128-4, 60-4])
            text(screen, "戻る", (0, 0, 0), 24, (WIDTH/2, HEIGHT/2+128), "center")

        clock.tick(fps)
        pygame.display.update()


# run the game
if __name__ == "__main__":
    main()