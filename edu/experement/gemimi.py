import pygame
import random
import math

upgrade_wheel_angle = 0.0          
upgrade_wheel_speed = 0.0          
upgrade_wheel_target_angle = 0.0   

# Инициализация графического движка
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Case-Battle Python Edition")
clock = pygame.time.Clock()

# Цвета
BG_COLOR = (27, 24, 38)        
CARD_TEXT_COLOR = (220, 220, 220)
BUTTON_COLOR = (255, 126, 0)   
WHITE = (255, 255, 255)
DARK_PANEL = (15, 12, 23)
GREEN = (46, 204, 113)
RED = (231, 76, 60)

# Глобальная экономика и инвентарь
USER_BALANCE = 10000.0
inventory = []  

# База цен предметов
ITEM_PRICES = {
    "Glock-18 | Fade": 158000,
    "AK-47 | Slate": 315.0,
    "Desert Eagle | Printstream": 5580.0,
    "M4A1-S | Printstream": 15120.0,
    "AWP | Asiimov": 2150.0,
    "Desert Eagle | Code Red": 14545.0,
    "Knife | Karambit | Lore": 75800.0,
    "AK-47 | Fire Serpent": 212600.0,
    "AWP | Gungnir": 720000.0,
}

# Данные о кейсах
cases = [
    {
        "name": "LEON KENNEDY", 
        "price": 1000.0,
        "color": (60, 80, 140),
        "items": ["Glock-18 | Fade", "AK-47 | Slate", "Desert Eagle | Printstream"]
    },
    {
        "name": "VICTOR GIDEON", 
        "price": 4000.0,
        "color": (50, 120, 70),
        "items": ["M4A1-S | Printstream", "AWP | Asiimov", "Desert Eagle | Code Red"]
    },
    {
        "name": "HOMELANDER", 
        "price": 10000.0,
        "color": (140, 50, 50),
        "items": ["Knife | Karambit | Lore", "AK-47 | Fire Serpent", "AWP | Gungnir"]
    }
]

case_rects = [
    pygame.Rect(80, 150, 240, 180),
    pygame.Rect(380, 150, 240, 180),
    pygame.Rect(680, 150, 240, 180)
]

# Навигация (вкладки меню)
current_tab = "cases"  
tab_cases_rect = pygame.Rect(30, 20, 100, 35)
tab_inv_rect = pygame.Rect(140, 20, 130, 35)
tab_upgrade_rect = pygame.Rect(280, 20, 110, 35)
tab_exit_rect = pygame.Rect(400, 20, 90, 35)

# Состояния кейсов
selected_case = None 
last_dropped_items = [] 
show_drop_window = False

# Переменные для горизонтальной рулетки
roulette_animating = False
roulette_x = 0.0
roulette_speed = 0.0
roulette_items = []
roulette_chosen_idx = 40
roulette_opening_count = 1  # Сколько кейсов открываем (1 или 10)

# Все необходимые кнопки управления
btn_open_1 = pygame.Rect(300, 440, 160, 45)
btn_open_10 = pygame.Rect(540, 440, 160, 45)
btn_collect_drop = pygame.Rect(250, 440, 220, 40)
btn_sell_drop = pygame.Rect(530, 440, 220, 40)

# Сетка кнопок быстрой продажи для инвентаря
sell_buttons_rects = []
for idx in range(15):
    col = idx % 5
    row = idx // 5
    x = 30 + col * 190
    y = 140 + row * 110
    sell_buttons_rects.append(pygame.Rect(x + 95, y + 55, 65, 25))

# Состояния вкладки апгрейда
upgrade_selected_inv_idx = None  
upgrade_target_item_name = None  
upgrade_chance = 0.0
upgrade_result_text = ""
upgrade_result_color = WHITE
upgrade_anim_ticks = 0
upgrade_wheel_animating = False
upgrade_is_success = False

# Безопасные встроенные шрифты
font_main = pygame.font.Font(None, 28)
font_sub = pygame.font.Font(None, 22)
font_small = pygame.font.Font(None, 18)

def roll_item(case_idx):
    """Взвешенный рандом: чем дороже предмет, тем меньше у него шансов выпасть"""
    possible_items = cases[case_idx]["items"]
    weights = []
    for item in possible_items:
        price = ITEM_PRICES[item]
        weight = 10000.0 / max(price, 0.1)
        weights.append(weight)
        
    item_name = random.choices(possible_items, weights=weights, k=1)[0]
    return {"name": item_name, "price": ITEM_PRICES[item_name]}

def start_roulette(case_idx, count):
    """Запуск рулетки при открытии кейса"""
    global roulette_animating, roulette_x, roulette_speed, roulette_items, roulette_chosen_idx, last_dropped_items, roulette_opening_count
    
    roulette_opening_count = count
    roulette_items = []
    last_dropped_items = []
    
    # Генерируем 50 предметов для ленты
    for i in range(50):
        roulette_items.append(roll_item(case_idx))
    
    # Запоминаем выигрышный предмет (или несколько)
    if count == 1:
        last_dropped_items = [roulette_items[roulette_chosen_idx]]
    else:
        # Для x10 берем несколько случайных из сгенерированных
        last_dropped_items = [roll_item(case_idx) for _ in range(count)]
        roulette_items[roulette_chosen_idx] = last_dropped_items[0]
    
    roulette_x = 0.0
    roulette_speed = random.uniform(45.0, 60.0)
    roulette_animating = True

def draw_header():
    for rect, text, tab_id in [(tab_cases_rect, "Cases", "cases"), (tab_inv_rect, "Inventory", "inventory"), (tab_upgrade_rect, "Upgrade", "upgrade"), (tab_exit_rect, "Exit", "exit")]:
        color = BUTTON_COLOR if current_tab == tab_id else DARK_PANEL
        pygame.draw.rect(screen, color, rect, border_radius=5)
        txt_render = font_sub.render(text, True, WHITE)
        screen.blit(txt_render, (rect.x + rect.width//2 - txt_render.get_width()//2, rect.y + 8))
        
    balance_text = font_main.render(f"Balance: {USER_BALANCE:.2f} rub.", True, GREEN)
    screen.blit(balance_text, (WIDTH - balance_text.get_width() - 30, 25))
    pygame.draw.line(screen, (50, 50, 60), (0, 70), (WIDTH, 70), 2)

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
        screen.blit(t1, (btn_open_1.x + btn_open_1.width//2 - t1.get_width()//2, btn_open_1.y + 12))
        
        pygame.draw.rect(screen, BUTTON_COLOR, btn_open_10, border_radius=5)
        t10 = font_sub.render(f"Open x10 ({c['price']*10:.0f}r)", True, WHITE)
        screen.blit(t10, (btn_open_10.x + btn_open_10.width//2 - t10.get_width()//2, btn_open_10.y + 12))

def draw_roulette():
    """Отрисовка горизонтальной рулетки на FullHD экране"""
    cx, cy = WIDTH // 2, HEIGHT // 2
    rw, rh = 240, 160
    padding = 15
    
    # Затемняем весь экран
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(230)
    overlay.fill(BG_COLOR)
    screen.blit(overlay, (0, 0))
    
    # Темная подложка под рулетку
    pygame.draw.rect(screen, DARK_PANEL, (0, cy - 140, WIDTH, 280))
    pygame.draw.rect(screen, (50, 50, 65), (0, cy - 140, WIDTH, 280), width=3)
    
    # Заголовок
    title = font_main.render("SPINNING THE CASE...", True, BUTTON_COLOR)
    screen.blit(title, (cx - title.get_width()//2, cy - 200))
    
    # Отрисовка карточек
    start_x = cx - (roulette_chosen_idx * (rw + padding)) - (rw // 2) + roulette_x
    
    for idx, item in enumerate(roulette_items):
        item_x = start_x + idx * (rw + padding)
        
        if -rw < item_x < WIDTH:
            rect = pygame.Rect(item_x, cy - 80, rw, rh)
            pygame.draw.rect(screen, (35, 32, 48), rect, border_radius=10)
            pygame.draw.rect(screen, BUTTON_COLOR if idx == roulette_chosen_idx else (60, 60, 75), rect, width=2, border_radius=10)
            
            name_txt = font_small.render(item["name"][:20], True, WHITE)
            screen.blit(name_txt, (item_x + rw//2 - name_txt.get_width()//2, cy - 40))
            
            price_txt = font_small.render(f"{item['price']:.0f} r", True, GREEN)
            screen.blit(price_txt, (item_x + rw//2 - price_txt.get_width()//2, cy + 20))
            
    # Центральный указатель
    pygame.draw.line(screen, BUTTON_COLOR, (cx, cy - 150), (cx, cy + 150), 4)
    pygame.draw.polygon(screen, BUTTON_COLOR, [(cx, cy - 140), (cx - 15, cy - 165), (cx + 15, cy - 165)])
    pygame.draw.polygon(screen, BUTTON_COLOR, [(cx, cy + 140), (cx - 15, cy + 165), (cx + 15, cy + 165)])

def draw_inventory_page():
    title = font_main.render(f"YOUR INVENTORY ({len(inventory)} items)", True, WHITE)
    screen.blit(title, (30, 95))
    
    if not inventory:
        empty_txt = font_main.render("Your inventory is empty. Open some cases!", True, (100, 100, 110))
        screen.blit(empty_txt, (WIDTH//2 - empty_txt.get_width()//2, HEIGHT//2))
        return

    for idx, item in enumerate(inventory[:15]):
        col = idx % 5
        row = idx // 5
        x = 30 + col * 190
        y = 140 + row * 110
        
        rect = pygame.Rect(x, y, 170, 95)
        
        # Подсветка выбранного предмета для апгрейда
        if upgrade_selected_inv_idx == idx:
            pygame.draw.rect(screen, BUTTON_COLOR, rect.inflate(6, 6), border_radius=8)
        
        pygame.draw.rect(screen, DARK_PANEL, rect, border_radius=8)
        pygame.draw.rect(screen, (50, 50, 70), rect, width=1, border_radius=8)
        
        name_txt = font_small.render(item["name"][:20], True, WHITE)
        screen.blit(name_txt, (x + 10, y + 20))
        price_txt = font_sub.render(f"{item['price']:.1f}r", True, GREEN)
        screen.blit(price_txt, (x + 10, y + 58))
        
        s_rect = sell_buttons_rects[idx]
        pygame.draw.rect(screen, RED, s_rect, border_radius=4)
        sell_lbl = font_small.render("Sell", True, WHITE)
        screen.blit(sell_lbl, (s_rect.x + s_rect.width//2 - sell_lbl.get_width()//2, s_rect.y + 5))

btn_upgrade_action = pygame.Rect(WIDTH//2 - 100, 600, 200, 45)
target_items_list = list(ITEM_PRICES.keys())
target_rects = []
for i in range(len(target_items_list)):
    target_rects.append(pygame.Rect(WIDTH - 380, 110 + i*43, 330, 35))

def draw_upgrade_page():
    global upgrade_chance
    
    # Левая панель - Ваш предмет
    left_panel_x = 50
    pygame.draw.rect(screen, DARK_PANEL, (left_panel_x, 110, 350, 200), border_radius=10)
    lbl1 = font_sub.render("Your Item:", True, CARD_TEXT_COLOR)
    screen.blit(lbl1, (left_panel_x + 15, 125))
    
    if upgrade_selected_inv_idx is not None and upgrade_selected_inv_idx < len(inventory):
        inv_item = inventory[upgrade_selected_inv_idx]
        item_txt = font_main.render(inv_item["name"][:22], True, WHITE)
        price_txt = font_main.render(f"{inv_item['price']:.2f} rub.", True, GREEN)
        screen.blit(item_txt, (left_panel_x + 15, 165))
        screen.blit(price_txt, (left_panel_x + 15, 205))
        
        # Картинка предмета (заглушка)
        item_img_rect = pygame.Rect(left_panel_x + 15, 240, 100, 100)
        pygame.draw.rect(screen, (40, 35, 55), item_img_rect, border_radius=8)
        pygame.draw.rect(screen, BUTTON_COLOR, item_img_rect, width=2, border_radius=8)
    else:
        hint = font_sub.render("Select item in Inventory", True, (100, 100, 110))
        screen.blit(hint, (left_panel_x + 15, 175))

    # Правая панель - Целевой предмет
    right_panel_x = WIDTH - 380
    pygame.draw.rect(screen, DARK_PANEL, (right_panel_x, 80, 350, 520), border_radius=10)
    lbl2 = font_sub.render("Target Item:", True, CARD_TEXT_COLOR)
    screen.blit(lbl2, (right_panel_x + 15, 85))
    
    for i, name in enumerate(target_items_list):
        rect = target_rects[i]
        bg = (60, 55, 75) if upgrade_target_item_name == name else (23, 20, 32)
        pygame.draw.rect(screen, bg, rect, border_radius=5)
        if upgrade_target_item_name == name:
            pygame.draw.rect(screen, BUTTON_COLOR, rect, width=2, border_radius=5)
        
        n_txt = font_small.render(name[:25], True, WHITE)
        p_txt = font_small.render(f"{ITEM_PRICES[name]:.0f}r", True, GREEN)
        screen.blit(n_txt, (rect.x + 8, rect.y + 10))
        screen.blit(p_txt, (rect.x + 240, rect.y + 10))

    current_val = inventory[upgrade_selected_inv_idx]["price"] if upgrade_selected_inv_idx is not None else 0.0
    target_val = ITEM_PRICES[upgrade_target_item_name] if upgrade_target_item_name else 0.0
    
    if current_val > 0 and target_val > 0:
        upgrade_chance = (current_val / target_val) * 100.0
        if upgrade_chance > 100.0: upgrade_chance = 100.0
    else:
        upgrade_chance = 0.0
        
    # === КОЛЕСО УДАЧИ ПО ЦЕНТРУ ===
    cx, cy = WIDTH // 2, 350
    radius = 120
    
    pygame.draw.circle(screen, (20, 17, 28), (cx, cy), radius)
    
    # Рисуем сектора
    yellow_sector_width = int((upgrade_chance / 100.0) * 360)
    for deg in range(360):
        rad = math.radians(deg - 90)
        color = BUTTON_COLOR if deg < yellow_sector_width else (40, 35, 50)
        tx = cx + int(math.cos(rad) * (radius - 4))
        ty = cy + int(math.sin(rad) * (radius - 4))
        pygame.draw.circle(screen, color, (tx, ty), 4)

    # Вращающаяся стрелка
    pointer_angle = upgrade_wheel_angle - 90
    rad_arrow = math.radians(pointer_angle)
    rad_left = math.radians(pointer_angle - 10)
    rad_right = math.radians(pointer_angle + 10)
    
    p_tip = (cx + int(math.cos(rad_arrow) * (radius - 6)), cy + int(math.sin(rad_arrow) * (radius - 6)))
    p_left = (cx + int(math.cos(rad_left) * (radius - 30)), cy + int(math.sin(rad_left) * (radius - 30)))
    p_right = (cx + int(math.cos(rad_right) * (radius - 30)), cy + int(math.sin(rad_right) * (radius - 30)))
    
    pygame.draw.polygon(screen, WHITE, [p_tip, p_left, p_right])
    pygame.draw.circle(screen, WHITE, (cx, cy), 8)

    # Текст по центру колеса
    chance_txt = font_main.render(f"{upgrade_chance:.1f}%", True, BUTTON_COLOR)
    lbl_chance = font_sub.render("CHANCE", True, CARD_TEXT_COLOR)
    screen.blit(chance_txt, (cx - chance_txt.get_width()//2, cy - 20))
    screen.blit(lbl_chance, (cx - lbl_chance.get_width()//2, cy - 40))
    
    # Кнопка апгрейда
    if upgrade_chance > 0 and not upgrade_wheel_animating:
        if upgrade_chance >= 90.0:
            pygame.draw.rect(screen, (80, 80, 90), btn_upgrade_action, border_radius=5)
            err_txt = font_sub.render("CHANCE TOO HIGH!", True, RED)
            screen.blit(err_txt, (btn_upgrade_action.x + btn_upgrade_action.width//2 - err_txt.get_width()//2, btn_upgrade_action.y + 14))
            
            hint_txt = font_small.render("(Max 89.99%)", True, CARD_TEXT_COLOR)
            screen.blit(hint_txt, (cx - hint_txt.get_width()//2, 660))
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, btn_upgrade_action, border_radius=5)
            act_txt = font_main.render("UPGRADE", True, WHITE)
            screen.blit(act_txt, (btn_upgrade_action.x + btn_upgrade_action.width//2 - act_txt.get_width()//2, btn_upgrade_action.y + 14))
        
    if upgrade_result_text:
        res_render = font_main.render(upgrade_result_text, True, upgrade_result_color)
        screen.blit(res_render, (cx - res_render.get_width()//2, cy + radius + 40))

# ==================== ГЛАВНЫЙ ИГРОВОЙ ЦИКЛ ====================
running = True
while running:
    # Логика рулетки кейсов
    if roulette_animating:
        roulette_x -= roulette_speed
        roulette_speed *= 0.98  # Замедление
        
        # Целевая позиция (предмет останавливается по центру)
        rw, padding = 240, 15
        target_x = -(roulette_chosen_idx * (rw + padding))
        
        if roulette_speed < 0.5:
            roulette_animating = False
            roulette_x = target_x
            show_drop_window = True

    # Логика колеса апгрейда
    if upgrade_wheel_animating:
        upgrade_wheel_angle += upgrade_wheel_speed
        upgrade_wheel_speed -= 0.12
        
        if upgrade_wheel_speed <= 0:
            upgrade_wheel_animating = False
            upgrade_wheel_speed = 0.0
            
            final_arrow_angle = upgrade_wheel_angle % 360
            max_yellow_angle = (upgrade_chance / 100.0) * 360
            
            if final_arrow_angle <= max_yellow_angle:
                inventory.pop(upgrade_selected_inv_idx)
                inventory.insert(0, {"name": upgrade_target_item_name, "price": ITEM_PRICES[upgrade_target_item_name]})
                upgrade_result_text = "✓ SUCCESS!"
                upgrade_result_color = GREEN
            else:
                inventory.pop(upgrade_selected_inv_idx)
                upgrade_result_text = "✗ FAIL! Item lost."
                upgrade_result_color = RED
            upgrade_selected_inv_idx = None

    screen.fill(BG_COLOR)
    draw_header()
    
    if roulette_animating:
        draw_roulette()
    else:
        if current_tab == "cases":
            draw_cases_page()
        elif current_tab == "inventory":
            draw_inventory_page()
        elif current_tab == "upgrade":
            draw_upgrade_page()

    if show_drop_window and not roulette_animating:
        # Окно выигрыша
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(screen, DARK_PANEL, (WIDTH//2 - 400, HEIGHT//2 - 250, 800, 500), border_radius=15)
        pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH//2 - 400, HEIGHT//2 - 250, 800, 500), width=3, border_radius=15)
        
        drop_title = font_main.render("YOU WON:", True, BUTTON_COLOR)
        screen.blit(drop_title, (WIDTH // 2 - drop_title.get_width() // 2, HEIGHT//2 - 220))
        
        for index, item in enumerate(last_dropped_items):
            item_text = font_sub.render(f"• {item['name']} ({item['price']:.1f} r)", True, WHITE)
            x_offset = WIDTH//2 - 350 if index < 5 else WIDTH//2
            y_offset = HEIGHT//2 - 170 + (index % 5) * 45
            screen.blit(item_text, (x_offset, y_offset))
        
        collect_btn = pygame.Rect(WIDTH//2 - 360, HEIGHT//2 + 150, 320, 50)
        sell_btn = pygame.Rect(WIDTH//2 + 40, HEIGHT//2 + 150, 320, 50)
        
        pygame.draw.rect(screen, GREEN, collect_btn, border_radius=5)
        c_lbl = font_sub.render("Keep & Add to Inventory", True, WHITE)
        screen.blit(c_lbl, (collect_btn.x + collect_btn.width//2 - c_lbl.get_width()//2, collect_btn.y + 16))
        
        pygame.draw.rect(screen, RED, sell_btn, border_radius=5)
        total_drop_worth = sum(itm["price"] for itm in last_dropped_items)
        s_lbl = font_sub.render(f"Sell All (+{total_drop_worth:.1f}r)", True, WHITE)
        screen.blit(s_lbl, (sell_btn.x + sell_btn.width//2 - s_lbl.get_width()//2, sell_btn.y + 16))
        
        btn_collect_drop = collect_btn
        btn_sell_drop = sell_btn

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            if show_drop_window and not roulette_animating:
                if btn_collect_drop.collidepoint(mouse_pos):
                    for itm in last_dropped_items:
                        inventory.insert(0, itm)
                    show_drop_window = False
                    last_dropped_items.clear()
                elif btn_sell_drop.collidepoint(mouse_pos):
                    USER_BALANCE += sum(itm["price"] for itm in last_dropped_items)
                    show_drop_window = False
                    last_dropped_items.clear()
                continue
            
            if roulette_animating:
                continue
                
            if tab_cases_rect.collidepoint(mouse_pos):
                current_tab = "cases"
                upgrade_result_text = ""
            elif tab_inv_rect.collidepoint(mouse_pos):
                current_tab = "inventory"
                upgrade_result_text = ""
            elif tab_upgrade_rect.collidepoint(mouse_pos):
                current_tab = "upgrade"
                upgrade_result_text = ""
            elif tab_exit_rect.collidepoint(mouse_pos):
                running = False
                
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
                sold_action = False
                for idx in range(min(len(inventory), 15)):
                    if sell_buttons_rects[idx].collidepoint(mouse_pos):
                        USER_BALANCE += inventory[idx]["price"]
                        inventory.pop(idx)
                        if upgrade_selected_inv_idx == idx:
                            upgrade_selected_inv_idx = None
                        sold_action = True
                        break
                        
                if not sold_action:
                    for idx in range(min(len(inventory), 15)):
                        col = idx % 5
                        row = idx // 5
                        x = 30 + col * 190
                        y = 140 + row * 110
                        if pygame.Rect(x, y, 170, 95).collidepoint(mouse_pos):
                            upgrade_selected_inv_idx = idx
                            current_tab = "upgrade"
                            upgrade_result_text = ""
                            
            elif current_tab == "upgrade" and not upgrade_wheel_animating:
                for i, rect in enumerate(target_rects):
                    if rect.collidepoint(mouse_pos):
                        upgrade_target_item_name = target_items_list[i]
                        upgrade_result_text = ""
                        
                if btn_upgrade_action.collidepoint(mouse_pos) and upgrade_chance > 0 and upgrade_chance < 90:
                    upgrade_wheel_animating = True
                    upgrade_wheel_speed = random.uniform(22.0, 30.0)

    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()