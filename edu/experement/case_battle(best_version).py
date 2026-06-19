import pygame
import random
import math

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Case-Battle Python Edition")
clock = pygame.time.Clock()

# ==================== ЦВЕТА ====================
BG_COLOR = (27, 24, 38)
CARD_TEXT_COLOR = (220, 220, 220)
BUTTON_COLOR = (255, 126, 0)
WHITE = (255, 255, 255)
DARK_PANEL = (15, 12, 23)
GREEN = (46, 204, 113)
RED = (231, 76, 60)

# ==================== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ====================
USER_BALANCE = 10000.0
inventory = []

ITEM_PRICES = {
    "Glock-18 | Fade": 158000,
    "AK-47 | Slate": 315.0,
    "Desert Eagle | Printstream": 5580.0,
    "M4A1-S | Printstream": 15120.0,
    "AWP | Asiimov": 2150.0,
    "Desert Eagle | Code Red": 14545.0,
    "Butterfly Knife | Gamma Doppler Emerald ST": 1145483.00,
    "AK-47 | Wild Lotus": 1143253.00,
    "AWP | Dragon Lore": 905000.00,
    "★ Butterfly Knife | Doppler Ruby": 834010.00,
    "★ Flip Knife | Doppler Black Pearl": 772235.32,
    "M4A4 | Howl": 760980.00,
    "Knife | Karambit | Lore": 750800.0,
    "AWP | Gungnir": 720000.0,
    "★ Sport Gloves | Ultra Violent": 700000.00,
    "★ Sport Gloves | Superconductor": 676529.48,
    "★ Sport Gloves | Hedge Maze": 666000.00,
    "★ Karambit | Doppler Black Pearl": 650000.00,
    "★ M9 Bayonet | Doppler Ruby": 630500.00,
    "★ Butterfly Knife | Doppler Sapphire": 580000.00,
    "★ Moto Gloves | Spearmint": 550590.00,
    "★ M9 Bayonet | Gamma Doppler Emerald": 550000.00,
    "★ Karambit | Gamma Doppler Emerald": 540750.00,
    "★ Karambit | Crimson Web": 532000.00,
    "★ Sport Gloves | Pandora's Box": 486000.99,
    "AK-47 | Hydroponic": 444232.00,
    "★ Specialist Gloves | Emerald Web": 369563.00,
    "AWP | Medusa": 360000.00,
    "★ Butterfly Knife | Doppler Phase 2": 350000.00,
    "★ Sport Gloves | Arid": 300000.00,
    "★ Sport Gloves | Occult": 250000.00,
    "★ Specialist Gloves | Crimson Kimono": 230000.00,
    "AK-47 | Fire Serpent": 236305.99,
    "★ Butterfly Knife | Ultraviolet": 234076.07,
    "M4A1-S | Knight": 231763.73,
    "★ Butterfly Knife | Doppler Phase 4": 230630.32,
    "Souvenir AK-47 | Gold Arabesque": 231000.30,
    "★ Skeleton Knife | Doppler Ruby": 229550.80,
    "AWP | The Prince": 220254.05,
    "AK-47 | X-Ray": 223000.54,
    "★ Talon Knife | Doppler Ruby": 222460.47,
    "★ Paracord Knife | Crimson Web": 216087.00,
    "★ Butterfly Knife | Lore": 214209.88,
    "★ Butterfly Knife | Doppler Phase 1": 209600.00,
    "MP9 | Wild Lily": 208883.11,
    "★ Sport Gloves | Slingshot": 205728.00,
    "★ Driver Gloves | Crimson Weave": 205024.96,
    "★ Driver Gloves | King Snake": 198850.70,
    "★ Sport Gloves | Nocts": 197801.71,
    "★ Karambit | Autotronic": 196922.03,
    "★ Moto Gloves | Cool Mint": 184747.40,
    "M4A4 | Poseidon": 177690.25,
    "★ Sport Gloves | Amphibious": 180315.00,
    "★ Butterfly Knife | Fade": 176071.26,
    "Negev | Mjölnir": 175275,
    "M4A4 | The Coalition": 174654.33,
    "★ Specialist Gloves | Cloud Chaser": 173754.42,
    "★ Bayonet | Doppler Ruby": 172423.67,
    "M4A1-S | Hot Rod": 160110.26,
    "★ Talon Knife | Doppler Sapphire ST": 165452.18,
    "★ Bayonet | Gamma Doppler Emerald": 162750.20,
    "★ Driver Gloves | Garden": 160950.69,
    "M4A1-S | Welcome to the Jungle": 160000.21,
    "★ Sport Gloves | Violet Beadwork": 160316.48,
    "★ Stiletto Knife | Doppler Black Pearl": 158232.67,
    "★ Karambit | Slaughter": 157564.30,
    "★ Specialist Gloves | Foundation": 157193.39,
    "★ Karambit | Fade": 155300.66,
    "★ Driver Gloves | Snow Leopard": 154417.99,
    "AWP | Desert Hydra": 153711.40,
    "AK-47 | Vulcan": 150586.82,
    "Sticker | Vox Eminor (Holo) | Katowice 2015": 149683.91,
    "★ Bayonet | Doppler Black Pearl": 149394.68,
    "Glock-18 | Fade": 147824.15,
    "★ Specialist Gloves | Fade": 146804.35,
    "★ Stiletto Knife | Doppler Ruby": 144772.25,
    "★ Karambit | Night": 143621.32,
    "★ M9 Bayonet | Autotronic": 139775.17,
    "AK-47 | Wasteland Rebel": 134274.54,
    "Sticker | ropz (Gold) | Krakow 2017": 132005.94,
    "★ Flip Knife | Doppler Ruby": 131223.48,
    "★ Karambit | Case Hardened": 131005.17,
    "★ M9 Bayonet | Case Hardened": 130495.78,
    "★ Sport Gloves | Omega": 127567.00,
    "★ Butterfly Knife | Blue Steel": 124613.47,
    "★ Karambit | Ultraviolet": 123384.64,
    "M4A4 | Daybreak": 121843.73,
    "★ Flip Knife | Gamma Doppler Emerald": 121194.81,
    "★ Butterfly Knife | Slaughter": 117489.57,
    "★ Butterfly Knife | Marble Fade": 117347.03,
    "★ Specialist Gloves | Pillow Punchers": 116996.69,
    "★ M9 Bayonet | Lore": 115957.66,
    "★ Skeleton Knife | Doppler Sapphire": 115593.06,
    "M4A1-S | Imminent Danger": 114813.60,
    "★ Sport Gloves | Vice": 114682.32,
    "★ Karambit | Doppler Phase 1": 113656.05,
    "★ Hand Wraps | Leather": 113470.75,
    "★ Huntsman Knife | Doppler Black Pearl": 112430.22,
    "★ Butterfly Knife | Freehand": 111337.18,
    "★ Hand Wraps | Slaughter": 108446.66,
    "★ Kukri Knife | Crimson Web": 105604.90,
    "★ M9 Bayonet | Doppler Phase 2": 105526.13,
    "★ Moto Gloves | Eclipse": 104377.57,
    "★ Driver Gloves | Lunar Weave": 103914.70,
    "★ Moto Gloves | Boom!": 103700.14,
    "★ Butterfly Knife | Tiger Tooth": 103450.32,
    "★ M9 Bayonet | Doppler Phase 1": 101829.14,
    "★ Butterfly Knife": 100545.55,
    "★ Hand Wraps | Cobalt Skulls": 99410.50,
    "★ Butterfly Knife | Tiger Tooth ST": 98964.88,
    "AK-47 | Jet Set": 93453.91,
    "AWP | CMYK": 93128.32,
    "★ Talon Knife | Fade ST": 92780.23,
    "★ Nomad Knife | Doppler Black Pearl": 91481.63,
    "★ Nomad Knife | Doppler Ruby": 90702.93,
    "★ Driver Gloves | Convoy": 90460.61,
    "AWP | Oni Taiji": 90449.36,
    "★ Survival Knife | Doppler Ruby": 89880.71,
    "★ Flip Knife | Crimson Web": 89039.73,
    "M4A4 | Eye of Horus": 87689.37,
    "AK-47 | Red Laminate": 87279.01,
    "★ M9 Bayonet | Doppler Phase 4": 86402.03,
    "AWP | Fade": 86396.03,
    "★ Stiletto Knife | Crimson Web": 86395.28,
    "★ Nomad Knife | Doppler Ruby ST": 86233.23,
    "★ Driver Gloves | Plum Quill": 85999.92,
    "★ Specialist Gloves | Field Agent": 85741.85,
    "★ Stiletto Knife | Doppler Sapphire": 85237.72,
    "★ Karambit Knife": 84912.13,
    "★ Driver Gloves | Diamondback": 84726.83,
    "M4A1-S | Printstream": 84373.49,
    "★ M9 Bayonet | Doppler Phase 1": 84012.64,
    "★ M9 Bayonet | Case Hardened": 83598.53,
    "AWP | Oni Taiji": 82922.60,
    "★ Ursus Knife | Doppler Black Pearl": 82684.79,
    "★ Karambit | Black Laminate": 82342.70,
    "MP9 | Bulldozer": 81748.54,
    "★ Falchion Knife | Doppler Black Pearl": 81402.70,
    "★ Flip Knife | Doppler Sapphire": 81170.88,
    "★ Specialist Gloves | Crimson Web": 81053.10,
    "★ Talon Knife | Doppler Phase 2 ST": 80875.31,
    "Souvenir AK-47 | B the Monster": 80769.53,
    "AK-47 | Case Hardened": 79849.79,
    "Glock-18 | Twilight Galaxy": 79689.99,
    "Sticker | Team Dignitas (Holo) | Cologne 2016": 77308.86,
    "★ Skeleton Knife | Case Hardened": 77308.86,
    "MLG Columbus 2016 Cobblestone Souvenir Package": 77149.06,
    "AWP | LongDog": 76836.98,
    "★ Bowie Knife | Doppler Black Pearl": 76035.77,
    "AUG | Akihabara Accept": 75617.90,
    "★ Huntsman Knife | Doppler Ruby": 74259.29,
    "★ Driver Gloves | Imperial Plaid": 73482.84,
    "★ Falchion Knife | Gamma Doppler Emerald": 73064.22,
    "M4A4 | The Coalition": 73052.97,
    "★ Specialist Gloves | Tiger Strike": 73049.22,
}

cases = [
    {"name": "LEON KENNEDY", "price": 1000.0, "color": (60, 80, 140),
     "items": ["Glock-18 | Fade", "AK-47 | Slate", "Desert Eagle | Printstream"]},
    {"name": "VICTOR GIDEON", "price": 4000.0, "color": (50, 120, 70),
     "items": ["M4A1-S | Printstream", "AWP | Asiimov", "Desert Eagle | Code Red"]},
    {"name": "HOMELANDER", "price": 10000.0, "color": (140, 50, 50),
     "items": ["Knife | Karambit | Lore", "AK-47 | Fire Serpent", "AWP | Gungnir"]}
]

case_rects = [
    pygame.Rect(80, 150, 240, 180),
    pygame.Rect(380, 150, 240, 180),
    pygame.Rect(680, 150, 240, 180)
]

# ==================== ВКЛАДКИ ====================
tab_cases_rect = pygame.Rect(30, 20, 100, 35)
tab_inv_rect = pygame.Rect(140, 20, 130, 35)
tab_upgrade_rect = pygame.Rect(280, 20, 110, 35)
tab_exit_rect = pygame.Rect(400, 20, 90, 35)

current_tab = "cases"
selected_case = None
last_dropped_items = []
show_drop_window = False

# ==================== РУЛЕТКА ====================
roulette_animating = False
roulette_x = 0.0
roulette_speed = 0.0
roulette_items = []
roulette_chosen_idx = 40
roulette_opening_count = 1

btn_open_1 = pygame.Rect(300, 440, 160, 45)
btn_open_10 = pygame.Rect(540, 440, 160, 45)

# ==================== НАСТРОЙКИ ====================
show_settings = False
add_balance_input = ""
add_balance_active = False

# ==================== АПГРЕЙД ====================
upgrade_selected_inv_idx = None
upgrade_target_item_name = None
upgrade_chance = 0.0
upgrade_result_text = ""
upgrade_result_color = WHITE
upgrade_wheel_animating = False
upgrade_wheel_angle = 0.0
upgrade_wheel_speed = 0.0

upgrade_scroll_y = 0
upgrade_scroll_speed = 40

font_main = pygame.font.Font(None, 28)
font_sub = pygame.font.Font(None, 22)
font_small = pygame.font.Font(None, 18)


def calculate_upgrade_chance(item_price, target_price):
    if target_price <= 0:
        return 0.0
    chance = (item_price / target_price) * 85.0
    return max(5.0, min(85.0, chance))


def roll_item(case_idx):
    possible_items = cases[case_idx]["items"]
    weights = [10000.0 / max(ITEM_PRICES[item], 0.1) for item in possible_items]
    item_name = random.choices(possible_items, weights=weights, k=1)[0]
    return {"name": item_name, "price": ITEM_PRICES[item_name]}


def start_roulette(case_idx, count):
    global roulette_animating, roulette_x, roulette_speed, roulette_items, last_dropped_items, roulette_opening_count

    roulette_opening_count = count
    roulette_items = []
    last_dropped_items = []

    for i in range(100):
        roulette_items.append(roll_item(case_idx))

    if count == 1:
        last_dropped_items = [roulette_items[roulette_chosen_idx]]
    else:
        last_dropped_items = [roll_item(case_idx) for _ in range(count)]
        roulette_items[roulette_chosen_idx] = last_dropped_items[0]

    # Случайный стартовый сдвиг, чтобы рулетка не начиналась с победного предмета
    roulette_x = random.uniform(-800, -200)
    roulette_speed = random.uniform(48.0, 65.0)
    roulette_animating = True


def draw_header():
    for rect, text, tab_id in [(tab_cases_rect, "Cases", "cases"),
                               (tab_inv_rect, "Inventory", "inventory"),
                               (tab_upgrade_rect, "Upgrade", "upgrade"),
                               (tab_exit_rect, "Exit", "exit")]:
        color = BUTTON_COLOR if current_tab == tab_id else DARK_PANEL
        pygame.draw.rect(screen, color, rect, border_radius=5)
        txt_render = font_sub.render(text, True, WHITE)
        screen.blit(txt_render, (rect.x + rect.width // 2 - txt_render.get_width() // 2, rect.y + 8))

    # Баланс
    balance_text = font_main.render(f"Balance: {USER_BALANCE:.2f} rub.", True, GREEN)
    screen.blit(balance_text, (WIDTH - balance_text.get_width() - 140, 25))

    # Кнопка Settings
    settings_rect = pygame.Rect(WIDTH - 120, 25, 90, 35)
    pygame.draw.rect(screen, DARK_PANEL, settings_rect, border_radius=5)
    sett_txt = font_sub.render("Settings", True, WHITE)
    screen.blit(sett_txt, (settings_rect.x + settings_rect.width // 2 - sett_txt.get_width() // 2, settings_rect.y + 8))

    pygame.draw.line(screen, (50, 50, 60), (0, 70), (WIDTH, 70), 2)
    return settings_rect


def draw_cases_page():
    title = font_main.render("AVAILABLE CASES", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 95))

    for i, case in enumerate(cases):
        rect = case_rects[i]
        if selected_case == i:
            pygame.draw.rect(screen, BUTTON_COLOR, rect.inflate(8, 8), border_radius=12)
        pygame.draw.rect(screen, case["color"], rect, border_radius=10)
        name = font_main.render(case["name"], True, WHITE)
        screen.blit(name, (rect.x + rect.width // 2 - name.get_width() // 2, rect.y + 20))
        price = font_main.render(f"Price: {case['price']:.0f} rub.", True, WHITE)
        screen.blit(price, (rect.x + rect.width // 2 - price.get_width() // 2, rect.y + 70))
        info = font_sub.render(f"{len(case['items'])} items", True, CARD_TEXT_COLOR)
        screen.blit(info, (rect.x + rect.width // 2 - info.get_width() // 2, rect.y + 130))

    if selected_case is not None:
        c = cases[selected_case]
        pygame.draw.rect(screen, BUTTON_COLOR, btn_open_1, border_radius=5)
        t1 = font_sub.render(f"Open x1 ({c['price']:.0f}r)", True, WHITE)
        screen.blit(t1, (btn_open_1.x + btn_open_1.width // 2 - t1.get_width() // 2, btn_open_1.y + 12))

        pygame.draw.rect(screen, BUTTON_COLOR, btn_open_10, border_radius=5)
        t10 = font_sub.render(f"Open x10 ({c['price'] * 10:.0f}r)", True, WHITE)
        screen.blit(t10, (btn_open_10.x + btn_open_10.width // 2 - t10.get_width() // 2, btn_open_10.y + 12))


def draw_roulette():
    cx, cy = WIDTH // 2, HEIGHT // 2
    rw, rh = 240, 160
    padding = 15

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(230)
    overlay.fill(BG_COLOR)
    screen.blit(overlay, (0, 0))

    pygame.draw.rect(screen, DARK_PANEL, (0, cy - 140, WIDTH, 280))
    pygame.draw.rect(screen, (50, 50, 65), (0, cy - 140, WIDTH, 280), width=3)

    title = font_main.render("SPINNING THE CASE...", True, BUTTON_COLOR)
    screen.blit(title, (cx - title.get_width() // 2, cy - 200))

    start_x = cx - (roulette_chosen_idx * (rw + padding)) - (rw // 2) + roulette_x

    for idx, item in enumerate(roulette_items):
        item_x = start_x + idx * (rw + padding)
        if -rw < item_x < WIDTH:
            rect = pygame.Rect(item_x, cy - 80, rw, rh)
            pygame.draw.rect(screen, (35, 32, 48), rect, border_radius=10)
            # Убираем оранжевое выделение во время анимации
            border_color = BUTTON_COLOR if (idx == roulette_chosen_idx and not roulette_animating) else (60, 60, 75)
            pygame.draw.rect(screen, border_color, rect, width=3, border_radius=10)

            name_txt = font_small.render(item["name"][:20], True, WHITE)
            screen.blit(name_txt, (item_x + rw // 2 - name_txt.get_width() // 2, cy - 40))
            price_txt = font_small.render(f"{item['price']:.0f} r", True, GREEN)
            screen.blit(price_txt, (item_x + rw // 2 - price_txt.get_width() // 2, cy + 20))

    pygame.draw.line(screen, BUTTON_COLOR, (cx, cy - 150), (cx, cy + 150), 4)
    pygame.draw.polygon(screen, BUTTON_COLOR, [(cx, cy - 140), (cx - 15, cy - 165), (cx + 15, cy - 165)])
    pygame.draw.polygon(screen, BUTTON_COLOR, [(cx, cy + 140), (cx - 15, cy + 165), (cx + 15, cy + 165)])


def draw_inventory_page():
    title = font_main.render(f"YOUR INVENTORY ({len(inventory)} items)", True, WHITE)
    screen.blit(title, (30, 95))

    if not inventory:
        empty_txt = font_main.render("Your inventory is empty. Open some cases!", True, (100, 100, 110))
        screen.blit(empty_txt, (WIDTH // 2 - empty_txt.get_width() // 2, HEIGHT // 2))
        return

    for idx, item in enumerate(inventory[:15]):
        col = idx % 5
        row = idx // 5
        x = 30 + col * 190
        y = 140 + row * 110

        rect = pygame.Rect(x, y, 170, 95)
        if upgrade_selected_inv_idx == idx:
            pygame.draw.rect(screen, BUTTON_COLOR, rect.inflate(6, 6), border_radius=8)

        pygame.draw.rect(screen, DARK_PANEL, rect, border_radius=8)
        pygame.draw.rect(screen, (50, 50, 70), rect, width=1, border_radius=8)

        name_txt = font_small.render(item["name"][:20], True, WHITE)
        screen.blit(name_txt, (x + 10, y + 20))
        price_txt = font_sub.render(f"{item['price']:.1f}r", True, GREEN)
        screen.blit(price_txt, (x + 10, y + 58))

        s_rect = pygame.Rect(x + 95, y + 55, 65, 25)
        pygame.draw.rect(screen, RED, s_rect, border_radius=4)
        sell_lbl = font_small.render("Sell", True, WHITE)
        screen.blit(sell_lbl, (s_rect.x + s_rect.width // 2 - sell_lbl.get_width() // 2, s_rect.y + 5))


def draw_upgrade_page():
    global upgrade_chance

    left_panel_x = 50
    pygame.draw.rect(screen, DARK_PANEL, (left_panel_x, 110, 350, 200), border_radius=10)
    screen.blit(font_sub.render("Your Item:", True, CARD_TEXT_COLOR), (left_panel_x + 15, 125))

    if upgrade_selected_inv_idx is not None and upgrade_selected_inv_idx < len(inventory):
        inv_item = inventory[upgrade_selected_inv_idx]
        screen.blit(font_main.render(inv_item["name"][:22], True, WHITE), (left_panel_x + 15, 165))
        screen.blit(font_main.render(f"{inv_item['price']:.2f} rub.", True, GREEN), (left_panel_x + 15, 205))
    else:
        screen.blit(font_sub.render("Select item in Inventory", True, (100, 100, 110)), (left_panel_x + 15, 175))

    # Правая панель
    right_panel_x = WIDTH - 380
    pygame.draw.rect(screen, DARK_PANEL, (right_panel_x, 80, 350, 520), border_radius=10)
    screen.blit(font_sub.render("Target Item:", True, CARD_TEXT_COLOR), (right_panel_x + 15, 85))

    start_y = 130 + upgrade_scroll_y
    for i, name in enumerate(list(ITEM_PRICES.keys())):
        y_pos = start_y + i * 43
        if 90 < y_pos < 580:
            rect = pygame.Rect(right_panel_x + 10, y_pos, 330, 38)
            bg = (60, 55, 75) if upgrade_target_item_name == name else (23, 20, 32)
            pygame.draw.rect(screen, bg, rect, border_radius=5)
            if upgrade_target_item_name == name:
                pygame.draw.rect(screen, BUTTON_COLOR, rect, width=2, border_radius=5)
            screen.blit(font_small.render(name[:28], True, WHITE), (rect.x + 10, rect.y + 10))
            screen.blit(font_small.render(f"{ITEM_PRICES[name]:.0f}r", True, GREEN), (rect.x + 250, rect.y + 10))

    # Колесо
    cx, cy = WIDTH // 2, 350
    radius = 120
    pygame.draw.circle(screen, (20, 17, 28), (cx, cy), radius)

    yellow_sector_width = int((upgrade_chance / 100.0) * 360)
    for deg in range(360):
        rad = math.radians(deg - 90)
        color = BUTTON_COLOR if deg < yellow_sector_width else (40, 35, 50)
        tx = cx + int(math.cos(rad) * (radius - 4))
        ty = cy + int(math.sin(rad) * (radius - 4))
        pygame.draw.circle(screen, color, (tx, ty), 4)

    pointer_angle = upgrade_wheel_angle - 90
    rad_arrow = math.radians(pointer_angle)
    p_tip = (cx + int(math.cos(rad_arrow) * (radius - 6)), cy + int(math.sin(rad_arrow) * (radius - 6)))
    p_left = (cx + int(math.cos(math.radians(pointer_angle - 10)) * (radius - 30)),
              cy + int(math.sin(math.radians(pointer_angle - 10)) * (radius - 30)))
    p_right = (cx + int(math.cos(math.radians(pointer_angle + 10)) * (radius - 30)),
               cy + int(math.sin(math.radians(pointer_angle + 10)) * (radius - 30)))
    pygame.draw.polygon(screen, WHITE, [p_tip, p_left, p_right])
    pygame.draw.circle(screen, WHITE, (cx, cy), 8)

    chance_txt = font_main.render(f"{upgrade_chance:.1f}%", True, BUTTON_COLOR)
    screen.blit(chance_txt, (cx - chance_txt.get_width() // 2, cy - 20))

    if upgrade_chance > 0 and not upgrade_wheel_animating:
        btn_upgrade_action = pygame.Rect(WIDTH // 2 - 100, 600, 200, 45)
        pygame.draw.rect(screen, BUTTON_COLOR, btn_upgrade_action, border_radius=5)
        act_txt = font_main.render("UPGRADE", True, WHITE)
        screen.blit(act_txt, (btn_upgrade_action.x + btn_upgrade_action.width // 2 - act_txt.get_width() // 2,
                              btn_upgrade_action.y + 14))

    if upgrade_result_text:
        res_render = font_main.render(upgrade_result_text, True, upgrade_result_color)
        screen.blit(res_render, (cx - res_render.get_width() // 2, cy + radius + 40))


# ==================== ГЛАВНЫЙ ЦИКЛ ====================
running = True
while running:
    if roulette_animating:
        roulette_x -= roulette_speed
        roulette_speed *= 0.975
        if roulette_speed < 0.8:
            roulette_animating = False
            roulette_x = -(roulette_chosen_idx * 255)
            show_drop_window = True

    if upgrade_wheel_animating:
        upgrade_wheel_angle += upgrade_wheel_speed
        upgrade_wheel_speed -= 0.15
        if upgrade_wheel_speed <= 0:
            upgrade_wheel_animating = False
            final_angle = upgrade_wheel_angle % 360
            success = final_angle <= (upgrade_chance / 100.0) * 360

            if success:
                inventory.pop(upgrade_selected_inv_idx)
                inventory.insert(0, {"name": upgrade_target_item_name, "price": ITEM_PRICES[upgrade_target_item_name]})
                upgrade_result_text = "✓ SUCCESS!"
                upgrade_result_color = GREEN
            else:
                inventory.pop(upgrade_selected_inv_idx)
                upgrade_result_text = "✗ FAIL! Item lost."
                upgrade_result_color = RED

            upgrade_selected_inv_idx = None
            upgrade_target_item_name = None
            upgrade_chance = 0.0

    screen.fill(BG_COLOR)
    settings_rect = draw_header()

    if roulette_animating:
        draw_roulette()
    else:
        if current_tab == "cases":
            draw_cases_page()
        elif current_tab == "inventory":
            draw_inventory_page()
        elif current_tab == "upgrade":
            draw_upgrade_page()

    # Окно дропа
    if show_drop_window and not roulette_animating:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(WIDTH // 2 - 400, HEIGHT // 2 - 250, 800, 500)
        pygame.draw.rect(screen, DARK_PANEL, panel, border_radius=15)
        pygame.draw.rect(screen, BUTTON_COLOR, panel, width=3, border_radius=15)

        drop_title = font_main.render("YOU WON:", True, BUTTON_COLOR)
        screen.blit(drop_title, (WIDTH // 2 - drop_title.get_width() // 2, HEIGHT // 2 - 220))

        for index, item in enumerate(last_dropped_items):
            item_text = font_sub.render(f"• {item['name']} ({item['price']:.1f} r)", True, WHITE)
            x_offset = WIDTH // 2 - 350 if index < 5 else WIDTH // 2
            y_offset = HEIGHT // 2 - 170 + (index % 5) * 45
            screen.blit(item_text, (x_offset, y_offset))

        collect_btn = pygame.Rect(WIDTH // 2 - 360, HEIGHT // 2 + 150, 320, 50)
        sell_btn = pygame.Rect(WIDTH // 2 + 40, HEIGHT // 2 + 150, 320, 50)

        pygame.draw.rect(screen, GREEN, collect_btn, border_radius=5)
        screen.blit(font_sub.render("Keep & Add to Inventory", True, WHITE),
                    (collect_btn.x + 20, collect_btn.y + 16))

        total = sum(itm["price"] for itm in last_dropped_items)
        pygame.draw.rect(screen, RED, sell_btn, border_radius=5)
        screen.blit(font_sub.render(f"Sell All (+{total:.1f}r)", True, WHITE),
                    (sell_btn.x + 40, sell_btn.y + 16))

    # Окно настроек
    if show_settings:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        sett_panel = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 150, 500, 300)
        pygame.draw.rect(screen, DARK_PANEL, sett_panel, border_radius=12)
        pygame.draw.rect(screen, BUTTON_COLOR, sett_panel, width=3, border_radius=12)

        title = font_main.render("Add Balance", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 120))

        input_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 50, 300, 50)
        pygame.draw.rect(screen, (40, 35, 55), input_rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, input_rect, width=2, border_radius=8)

        input_txt = font_main.render(add_balance_input + ("|" if add_balance_active else ""), True, WHITE)
        screen.blit(input_txt, (input_rect.x + 15, input_rect.y + 12))

        add_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 30, 200, 50)
        pygame.draw.rect(screen, GREEN, add_btn, border_radius=8)
        screen.blit(font_main.render("ADD BALANCE", True, WHITE),
                    (add_btn.x + 20, add_btn.y + 12))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL and current_tab == "upgrade":
            upgrade_scroll_y += event.y * upgrade_scroll_speed
            max_scroll = -len(ITEM_PRICES) * 43 + 400
            if upgrade_scroll_y > 0:
                upgrade_scroll_y = 0
            if upgrade_scroll_y < max_scroll:
                upgrade_scroll_y = max_scroll

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if show_settings:
                if add_btn.collidepoint(mouse_pos) and add_balance_input:
                    try:
                        amount = float(add_balance_input)
                        if amount > 0:
                            USER_BALANCE += amount
                    except:
                        pass
                    show_settings = False
                    add_balance_input = ""
                elif input_rect.collidepoint(mouse_pos):
                    add_balance_active = True
                else:
                    show_settings = False
                    add_balance_active = False
                continue

            if show_drop_window and not roulette_animating:
                if collect_btn.collidepoint(mouse_pos):
                    for itm in last_dropped_items:
                        inventory.insert(0, itm)
                    show_drop_window = False
                    last_dropped_items.clear()
                elif sell_btn.collidepoint(mouse_pos):
                    USER_BALANCE += sum(itm["price"] for itm in last_dropped_items)
                    show_drop_window = False
                    last_dropped_items.clear()
                continue

            if roulette_animating:
                continue

            # Вкладки
            if tab_cases_rect.collidepoint(mouse_pos):
                current_tab = "cases"
            elif tab_inv_rect.collidepoint(mouse_pos):
                current_tab = "inventory"
            elif tab_upgrade_rect.collidepoint(mouse_pos):
                current_tab = "upgrade"
            elif tab_exit_rect.collidepoint(mouse_pos):
                running = False
            elif settings_rect.collidepoint(mouse_pos):
                show_settings = True
                add_balance_input = ""
                add_balance_active = True
                continue

            if current_tab == "cases":
                for i, rect in enumerate(case_rects):
                    if rect.collidepoint(mouse_pos):
                        selected_case = i
                if selected_case is not None:
                    cost = cases[selected_case]["price"]
                    if btn_open_1.collidepoint(mouse_pos) and USER_BALANCE >= cost:
                        USER_BALANCE -= cost
                        start_roulette(selected_case, 1)
                    elif btn_open_10.collidepoint(mouse_pos) and USER_BALANCE >= (cost * 10):
                        USER_BALANCE -= (cost * 10)
                        start_roulette(selected_case, 10)

            elif current_tab == "inventory":
                sold = False
                for idx in range(min(len(inventory), 15)):
                    x = 30 + (idx % 5) * 190
                    y = 140 + (idx // 5) * 110
                    sell_rect = pygame.Rect(x + 95, y + 55, 65, 25)
                    if sell_rect.collidepoint(mouse_pos):
                        USER_BALANCE += inventory[idx]["price"]
                        inventory.pop(idx)
                        if upgrade_selected_inv_idx == idx:
                            upgrade_selected_inv_idx = None
                        sold = True
                        break
                if not sold:
                    for idx in range(min(len(inventory), 15)):
                        x = 30 + (idx % 5) * 190
                        y = 140 + (idx // 5) * 110
                        if pygame.Rect(x, y, 170, 95).collidepoint(mouse_pos):
                            upgrade_selected_inv_idx = idx
                            current_tab = "upgrade"
                            upgrade_target_item_name = None
                            upgrade_result_text = ""
                            upgrade_chance = 0.0
                            break

            elif current_tab == "upgrade" and not upgrade_wheel_animating:
                # Выбор цели
                start_y = 130 + upgrade_scroll_y
                for i, name in enumerate(ITEM_PRICES.keys()):
                    y_pos = start_y + i * 43
                    rect = pygame.Rect(WIDTH - 370, y_pos, 330, 38)
                    if rect.collidepoint(mouse_pos):
                        upgrade_target_item_name = name
                        if upgrade_selected_inv_idx is not None:
                            item_price = inventory[upgrade_selected_inv_idx]["price"]
                            target_price = ITEM_PRICES[name]
                            upgrade_chance = calculate_upgrade_chance(item_price, target_price)
                        upgrade_result_text = ""
                        break

                # Кнопка Upgrade
                btn_upgrade_action = pygame.Rect(WIDTH // 2 - 100, 600, 200, 45)
                if btn_upgrade_action.collidepoint(mouse_pos) and upgrade_chance > 0:
                    upgrade_wheel_animating = True
                    upgrade_wheel_speed = random.uniform(24.0, 32.0)

        # Ввод суммы баланса
        if event.type == pygame.KEYDOWN and show_settings and add_balance_active:
            if event.key == pygame.K_RETURN:
                try:
                    amount = float(add_balance_input)
                    if amount > 0:
                        USER_BALANCE += amount
                except:
                    pass
                show_settings = False
                add_balance_input = ""
            elif event.key == pygame.K_BACKSPACE:
                add_balance_input = add_balance_input[:-1]
            elif event.unicode.isdigit() or event.unicode == ".":
                if add_balance_input.count(".") < 1 or event.unicode != ".":
                    add_balance_input += event.unicode

    pygame.display.flip()
    clock.tick(60)

pygame.quit()