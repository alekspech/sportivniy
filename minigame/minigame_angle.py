import sys
import math
import pygame

# ========================== НАСТРОЙКИ ==========================
WIDTH, HEIGHT = 1200, 720
PANEL_W = 360                      # правая панель
CANVAS_W = WIDTH - PANEL_W

SCALE = 40
MAJOR_STEP = 1 * SCALE             # клетка

BG = (28, 28, 32)
GRID_MAJOR = (70, 70, 78)
GRID_MINOR = (45, 45, 50)
AXIS_X = (220, 60, 60)             # OX (красная)
AXIS_Y = (60, 200, 90)             # OY (зелёная)

LINE_COL = (180, 210, 255)
LINE_SEL = (255, 200, 120)
LINE_PREVIEW = (140, 200, 160)
POINT_COL = (255, 160, 160)

TEXT = (230, 230, 240)
MUTED = (160, 160, 170)
BORDER = (90, 90, 96)
BUBBLE = (18, 18, 22)

PROTRACTOR_RADIUS = 90             # уменьшенный транспортир

MAX_LINES = 10

# ============================ INIT =============================
pygame.init()
screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
     pygame.FULLSCREEN | pygame.SCALED
)
pygame.display.set_caption("geom.001 — прямые, углы и транспортир")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 22)
big = pygame.font.SysFont(None, 26)

V2 = pygame.math.Vector2
ORIGIN = V2(CANVAS_W // 2, HEIGHT // 2)  # (0,0) в центре холста

# ========================= ВСПОМОГАТЕЛЬНЫЕ ======================
def draw_grid(surf, origin):
    """Координатная сетка: только major-линии, центр выровнен по (0,0)."""
    pygame.draw.rect(surf, BG, (0, 0, CANVAS_W, HEIGHT))

    # вертикальные линии
    x0 = origin.x % MAJOR_STEP
    for x in range(int(x0), CANVAS_W, MAJOR_STEP):
        pygame.draw.line(surf, GRID_MAJOR, (x, 0), (x, HEIGHT), 1)

    # горизонтальные линии
    y0 = origin.y % MAJOR_STEP
    for y in range(int(y0), HEIGHT, MAJOR_STEP):
        pygame.draw.line(surf, GRID_MAJOR, (0, y), (CANVAS_W, y), 1)

    # оси
    pygame.draw.line(surf, AXIS_X, (0, origin.y), (CANVAS_W, origin.y), 3)
    pygame.draw.line(surf, AXIS_Y, (origin.x, 0), (origin.x, HEIGHT), 3)


def to_math_coords(p_screen: V2) -> V2:
    """Экран -> математика (центр в ORIGIN, Y вверх), c учётом SCALE."""
    x = (p_screen.x - ORIGIN.x) / SCALE
    y = (ORIGIN.y - p_screen.y) / SCALE
    return V2(x, y)

def from_math_coords(p_math: V2) -> V2:
    """Математика -> экран, c учётом SCALE."""
    x = ORIGIN.x + p_math.x * SCALE
    y = ORIGIN.y - p_math.y * SCALE
    return V2(x, y)

def length_px(p1: V2, p2: V2) -> float:
    return (p2 - p1).length()

def length_units(p1: V2, p2: V2) -> float:
    """Длина в математических единицах, а не в пикселях."""
    a = to_math_coords(p1)
    b = to_math_coords(p2)
    return (b - a).length()

def angle_between_segments(a1: V2, a2: V2, b1: V2, b2: V2) -> float:
    """Угол между отрезками (0..180) в градусах по нормированному скалярному произведению."""
    v1 = a2 - a1
    v2 = b2 - b1
    if v1.length() == 0 or v2.length() == 0:
        return float("nan")
    v1n = v1.normalize()
    v2n = v2.normalize()
    dot = max(-1.0, min(1.0, v1n.x * v2n.x + v1n.y * v2n.y))
    return math.degrees(math.acos(dot))

def draw_protractor(surf, center: V2, radius=PROTRACTOR_RADIUS):
    """Транспортир: окружность, метки каждые 10°, подписи каждые 30°."""
    pygame.draw.circle(surf, (120, 120, 130), center, radius, 2)
    for deg in range(0, 360, 10):
        a = math.radians(deg)
        v = V2(math.cos(a), -math.sin(a))  # мат. система -> экран (Y вниз)
        p1 = center + v * (radius - 8)
        p2 = center + v * radius
        width = 2 if deg % 30 == 0 else 1
        pygame.draw.line(surf, (140, 140, 150), p1, p2, width)
        if deg % 30 == 0:
            label = big.render(str(deg), True, (190, 190, 200))
            lp = center + v * (radius + 12)
            surf.blit(label, (lp.x - label.get_width() / 2, lp.y - label.get_height() / 2))

def draw_mouse_coords(surf, mouse: V2):
    """Отобразить текущие координаты мыши в математических единицах рядом с курсором."""
    # Рисуем только в области холста
    if mouse.x >= CANVAS_W:
        return
    m = to_math_coords(mouse)
    txt = f"({m.x:.1f}, {m.y:.1f})"
    img = font.render(txt, True, TEXT)
    pad = 6
    rect = pygame.Rect(mouse.x + 12, mouse.y - 10, img.get_width() + 2*pad, img.get_height() + 2*pad)
    pygame.draw.rect(surf, BUBBLE, rect)
    surf.blit(img, (rect.x + pad, rect.y + pad))

def draw_panel(surf, lines, selected_idx_set, angle_display, mouse: V2):
    """Правая информационная панель."""
    x0 = CANVAS_W
    pygame.draw.rect(surf, (22, 22, 25), (x0, 0, PANEL_W, HEIGHT))
    pygame.draw.line(surf, BORDER, (x0, 0), (x0, HEIGHT), 2)

    y = 12
    surf.blit(big.render("geom.001 — Прямые и углы", True, TEXT), (x0 + 14, y)); y += 34

    # Координаты мыши (в математических ед.)
    mm = to_math_coords(mouse)
    surf.blit(font.render(f"Координаты мыши: ({mm.x:.1f}, {mm.y:.1f})", True, TEXT), (x0 + 14, y)); y += 24

    controls = [
        "ЛКМ: поставить 2 точки — отрезок",
        "ПКМ: отменить текущий отрезок",
        "P: транспортир (при рисовании — у 1-й точки)",
        "H: показать/скрыть подсказку снизу",
        "C: очистить, R: удалить последний",
        "1..9,0: выбрать/снять отрезок (0 — 10-й)",
        "Esc: выход",
    ]
    for t in controls:
        surf.blit(font.render(t, True, MUTED), (x0 + 14, y)); y += 18
    y += 8

    pygame.draw.line(surf, BORDER, (x0 + 10, y), (x0 + PANEL_W - 10, y), 1); y += 10
    surf.blit(big.render("Угол между выбранными:", True, TEXT), (x0 + 14, y)); y += 28
    if angle_display is None:
        surf.blit(font.render("— выберите ровно два отрезка —", True, MUTED), (x0 + 14, y)); y += 24
    else:
        surf.blit(big.render(f"{angle_display:.2f}°", True, (255, 230, 140)), (x0 + 14, y)); y += 30
    y += 4

    pygame.draw.line(surf, BORDER, (x0 + 10, y), (x0 + PANEL_W - 10, y), 1); y += 10
    surf.blit(big.render("Отрезки (до 10):", True, TEXT), (x0 + 14, y)); y += 28

    if not lines:
        surf.blit(font.render("Нет отрезков. Кликните ЛКМ дважды.", True, MUTED), (x0 + 14, y))
        return

    for idx, seg in enumerate(lines, start=1):
        sel = (idx - 1) in selected_idx_set
        col = LINE_SEL if sel else TEXT
        (x1m, y1m) = to_math_coords(seg.p1)
        (x2m, y2m) = to_math_coords(seg.p2)
        Lpx = length_px(seg.p1, seg.p2)
        Lun = round(length_units(seg.p1, seg.p2), 2)
        label = f"{idx:>2}) A({x1m:.1f},{y1m:.1f})  B({x2m:.1f},{y2m:.1f})  |AB|={Lun:.2f}"
        surf.blit(font.render(label, True, col), (x0 + 14, y)); y += 20
        if y > HEIGHT - 24:
            break

# ============================= СУЩНОСТИ ===========================
class Segment:
    __slots__ = ("p1", "p2")

    def __init__(self, p1: V2, p2: V2):
        self.p1 = V2(p1)
        self.p2 = V2(p2)

    def draw(self, surf, color, width=3):
        pygame.draw.line(surf, color, self.p1, self.p2, width)
        pygame.draw.circle(surf, POINT_COL, self.p1, 4)
        pygame.draw.circle(surf, POINT_COL, self.p2, 4)

        # --- draw arrowhead at p2 ---
        direction = (self.p2 - self.p1)
        if direction.length() > 0:
            direction = direction.normalize()
            # make arrow smaller for thick lines
            arrow_size = 14 + width * 1.2
            left = direction.rotate(30) * (arrow_size * 0.6)
            right = direction.rotate(-30) * (arrow_size * 0.6)
            tip = self.p2
            pygame.draw.polygon(
                surf,
                color,
                [tip, tip - left, tip - right],
            )


# ============================= MAIN ===============================
def main():
    running = True
    show_help = True
    show_protractor = False

    lines = []                   # список Segment (до 10)
    selected = set()             # индексы выбранных (0..)
    drawing = False              # флаг набора отрезка
    start_pt = V2(0, 0)

    while running:
        dt = clock.tick(60) / 1000.0
        mx, my = pygame.mouse.get_pos()
        mouse = V2(mx, my)

        # --------- события ---------
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    running = False
                elif e.key == pygame.K_p:
                    show_protractor = not show_protractor
                elif e.key == pygame.K_h:
                    show_help = not show_help
                elif e.key == pygame.K_c:
                    lines.clear(); selected.clear()
                elif e.key == pygame.K_r:
                    if lines:
                        last_idx = len(lines) - 1
                        lines.pop()
                        selected = {i for i in selected if i <= last_idx - 1}
                # выбор по цифрам 1..9,0
                elif pygame.K_1 <= e.key <= pygame.K_9 or e.key == pygame.K_0:
                    if e.key == pygame.K_0:
                        idx = 9
                    else:
                        idx = e.key - pygame.K_1
                    if idx < len(lines):
                        if idx in selected:
                            selected.remove(idx)
                        else:
                            if len(selected) < 2:
                                selected.add(idx)
                            else:
                                selected = set(sorted(selected)[1:] + [idx])
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if mx >= CANVAS_W:
                    continue
                if e.button == 1:  # ЛКМ
                    if not drawing:
                        drawing = True
                        start_pt = V2(mouse)
                    else:
                        if len(lines) < MAX_LINES:
                            end_pt = V2(mouse)
                            if (end_pt - start_pt).length() > 0:
                                lines.append(Segment(start_pt, end_pt))
                        drawing = False
                elif e.button == 3:  # ПКМ — отмена
                    drawing = False

        # --------- рисование холста ---------
        draw_grid(screen, ORIGIN)

        # отрезки сохранённые
        for i, seg in enumerate(lines):
            col = LINE_SEL if i in selected else LINE_COL
            seg.draw(screen, col, 4 if i in selected else 3)

        # превью отрезка + транспортир
        if drawing:
            # превью
            pygame.draw.line(screen, LINE_PREVIEW, start_pt, mouse, 2)
            pygame.draw.circle(screen, POINT_COL, start_pt, 4)
            # транспортир фиксируется в первой точке касания
            if show_protractor:
                draw_protractor(screen, start_pt, radius=PROTRACTOR_RADIUS)
        else:
            # обычный транспортир вокруг курсора (если включен и на холсте)
            if show_protractor and mx < CANVAS_W:
                draw_protractor(screen, mouse, radius=PROTRACTOR_RADIUS)

        # координаты мыши у курсора
        draw_mouse_coords(screen, mouse)

        # расчёт угла между выбранными
        angle_display = None
        if len(selected) == 2:
            i, j = sorted(selected)
            s1, s2 = lines[i], lines[j]
            angle_display = angle_between_segments(s1.p1, s1.p2, s2.p1, s2.p2)

        # правая панель
        draw_panel(screen, lines, selected, angle_display, mouse)

        # подсказка внизу
        if show_help:
            hint = "ЛКМ×2 — создать отрезок | P — транспортир (при рисовании — у 1-й точки) | 1..9,0 — выбрать два отрезка | C — очистить | R — удалить последний"
            img = font.render(hint, True, (240, 240, 240))
            rect = pygame.Rect(8, HEIGHT - 28, CANVAS_W - 16, 20)
            pygame.draw.rect(screen, (20, 20, 22), rect)
            screen.blit(img, (12, HEIGHT - 26))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
