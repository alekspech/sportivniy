import pygame
import random
import time

# Инициализация
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Case-Battle Python Edition")
clock = pygame.time.Clock()

# Цвета (в стиле темной темы Case-Battle)
BG_COLOR = (27, 24, 38)        # Темный фон
CARD_TEXT_COLOR = (220, 220, 220)
BUTTON_COLOR = (255, 126, 0)   # Оранжевые кнопки открытия
WHITE = (255, 255, 255)

# Данные о кейсах (3 штуки, разных цветов и с разным дропом)
cases = [
    {
        "name": "ЛЕОН КЕННЕДИ", 
        "color": (60, 80, 140), # Синеватый карточка
        "items": ["Glock-18 | Fade", "P250 | Sand Dune", "AK-47 | Сланец"]
    },
    {
        "name": "ВИКТОР ГИДЕОН", 
        "color": (50, 120, 70), # Зеленоватая карточка
        "items": ["M4A1-S | Поток", "AWP | Азимов", "Desert Eagle | Код красный"]
    },
    {
        "name": "ХОУМЛЕНДЕР", 
        "color": (140, 50, 50), # Красноватая карточка
        "items": ["Нож | Керамбит | Кровавая паутина", "AK-47 | Огненный змей", "AWP | Гунгнир"]
    }
]

# Координаты карточек кейсов на экране
case_rects = [
    pygame.Rect(80, 150, 240, 180),
    pygame.Rect(380, 150, 240, 180),
    pygame.Rect(680, 150, 240, 180)
]

# Переменные состояния
selected_case = None # Индекс выбранного кейса (None, если никакой не выбран)
last_dropped_items = [] # Список выпавших предметов
show_drop_window = False

# Шрифты
font_main = pygame.font.SysFont("Arial", 22, bold=True)
font_sub = pygame.font.SysFont("Arial", 16)

def draw_cases_page():
    screen.fill(BG_COLOR)
    
    # Заголовок страницы
    title = font_main.render("СЕРИЙНЫЕ КЕЙСЫ (ПРОТОТИП)", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
    
    # Отрисовка 3 кейсов
    for i, case in enumerate(cases):
        rect = case_rects[i]
        # Рисуем цветной квадрат вместо картинки кейса
        pygame.draw.rect(screen, case["color"], rect, border_radius=10)
        
        # Название кейса
        text = font_main.render(case["name"], True, WHITE)
        screen.blit(text, (rect.x + rect.width // 2 - text.get_width() // 2, rect.y + 20))
        
        # Инфо-текст внутри карточки
        info = font_sub.render(f"Содержит: {len(case['items'])} предметов", True, CARD_TEXT_COLOR)
        screen.blit(info, (rect.x + rect.width // 2 - info.get_width() // 2, rect.y + 80))

# Кнопки для выбора количества (1 или 10)
btn_open_1 = pygame.Rect(300, 420, 160, 50)
btn_open_10 = pygame.Rect(540, 420, 160, 50)

# Цикл игры
running = True
while running:
    # 1. Логика отрисовки
    draw_cases_page()
    
    # Если выбран кейс — рисуем снизу панель выбора "Открыть 1 / 10"
    if selected_case is not None:
        case_name = cases[selected_case]["name"]
        choice_text = font_main.render(f"Выбран кейс [{case_name}]. Сколько открыть?", True, WHITE)
        screen.blit(choice_text, (WIDTH // 2 - choice_text.get_width() // 2, 370))
        
        # Кнопка Открыть x1
        pygame.draw.rect(screen, BUTTON_COLOR, btn_open_1, border_radius=5)
        text_1 = font_main.render("Открыть x1", True, WHITE)
        screen.blit(text_1, (btn_open_1.x + btn_open_1.width//2 - text_1.get_width()//2, btn_open_1.y + 12))
        
        # Кнопка Открыть x10
        pygame.draw.rect(screen, BUTTON_COLOR, btn_open_10, border_radius=5)
        text_10 = font_main.render("Открыть x10", True, WHITE)
        screen.blit(text_10, (btn_open_10.x + btn_open_10.width//2 - text_10.get_width()//2, btn_open_10.y + 12))

    # Если открыли кейс — выводим дроп поверх экрана
    if show_drop_window:
        # Темная подложка
        pygame.draw.rect(screen, (15, 12, 23), (150, 100, 700, 400), border_radius=15)
        drop_title = font_main.render("ВАШ ВЫИГРЫШ:", True, BUTTON_COLOR)
        screen.blit(drop_title, (WIDTH // 2 - drop_title.get_width() // 2, 130))
        
        # Вывод выпавших пушек списком
        for index, item in enumerate(last_dropped_items):
            item_text = font_sub.render(f"• {item}", True, WHITE)
            # Распределяем текст в 2 колонки, если выпало 10 штук
            x_offset = 250 if index < 5 else 550
            y_offset = 180 + (index % 5) * 40
            screen.blit(item_text, (x_offset, y_offset))
            
        tip_text = font_sub.render("(Кликните мышкой в любом месте, чтобы закрыть)", True, CARD_TEXT_COLOR)
        screen.blit(tip_text, (WIDTH // 2 - tip_text.get_width() // 2, 450))

    # 2. Обработка кликов и событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            # Если окно дропа открыто — любой клик его закрывает
            if show_drop_window:
                show_drop_window = False
                last_dropped_items.clear()
                continue
                
            # Проверяем клик по карточкам кейсов
            for i, rect in enumerate(case_rects):
                if rect.collidepoint(mouse_pos):
                    selected_case = i
            
            # Проверяем клик по кнопкам открытия (только если кейс выбран)
            if selected_case is not None:
                if btn_open_1.collidepoint(mouse_pos):
                    # Открываем 1 предмет
                    possible_items = cases[selected_case]["items"]
                    last_dropped_items = [random.choice(possible_items)]
                    show_drop_window = True
                    
                elif btn_open_10.collidepoint(mouse_pos):
                    # Открываем 10 предметов
                    possible_items = cases[selected_case]["items"]
                    last_dropped_items = [random.choice(possible_items) for _ in range(10)]
                    show_drop_window = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
