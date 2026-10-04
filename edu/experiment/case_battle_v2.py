from __future__ import annotations

import json
import math
import random
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

import pygame


Color = tuple[int, int, int]
RectKey = tuple[str, str]


@dataclass(frozen=True, slots=True)
class Colors:
    bg: Color = (27, 24, 38)
    panel: Color = (15, 12, 23)
    panel_soft: Color = (35, 32, 48)
    panel_light: Color = (50, 50, 70)
    text: Color = (235, 235, 240)
    text_muted: Color = (155, 155, 165)
    card_text: Color = (220, 220, 220)
    accent: Color = (255, 126, 0)
    green: Color = (46, 204, 113)
    red: Color = (231, 76, 60)
    white: Color = (255, 255, 255)
    black: Color = (0, 0, 0)
    blue: Color = (70, 130, 210)
    purple: Color = (155, 89, 182)
    gold: Color = (241, 196, 15)


@dataclass(frozen=True, slots=True)
class AppSettings:
    width: int
    height: int
    fps: int
    title: str
    save_path: Path
    starting_balance: float
    colors: Colors
    card_width: int
    card_height: int
    card_gap: int
    roulette_duration: float
    roulette_cards: int
    roulette_target_index: int
    inventory_columns: int
    inventory_card_width: int
    inventory_card_height: int
    inventory_card_gap: int
    case_card_width: int
    case_card_height: int
    case_card_gap: int
    scroll_step: int


@dataclass(frozen=True, slots=True)
class ItemDef:
    name: str
    price: float


@dataclass(frozen=True, slots=True)
class CaseDef:
    case_id: str
    name: str
    price: float
    color: Color
    item_names: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ItemSettings:
    items: dict[str, ItemDef]
    cases: tuple[CaseDef, ...]
    price_probability_power: float


@dataclass(slots=True)
class InventoryEntry:
    entry_id: str
    name: str
    price: float
    source_case_id: str
    created_at: float


@dataclass(slots=True)
class PlayerState:
    balance: float
    inventory: list[InventoryEntry] = field(default_factory=list)
    total_opened: int = 0


@dataclass(slots=True)
class RouletteState:
    active: bool = False
    track_x: float = 0.0
    start_x: float = 0.0
    end_x: float = 0.0
    elapsed: float = 0.0
    duration: float = 0.0
    target_index: int = 0
    tape: list[InventoryEntry] = field(default_factory=list)
    pending_drops: list[InventoryEntry] = field(default_factory=list)


@dataclass(slots=True)
class UpgradeState:
    selected_entry_id: str | None = None
    target_name: str | None = None
    chance: float = 0.0
    result_text: str = ""
    result_color: Color = (255, 255, 255)
    animating: bool = False
    elapsed: float = 0.0
    duration: float = 2.1
    start_angle: float = 0.0
    end_angle: float = 0.0
    angle: float = 0.0
    success: bool = False


@dataclass(slots=True)
class ModalState:
    show_settings: bool = False
    add_balance_input: str = ""
    add_balance_active: bool = False
    show_drop_window: bool = False


@dataclass(slots=True)
class ScrollState:
    cases: int = 0
    inventory: int = 0
    upgrade_targets: int = 0


@dataclass(slots=True)
class Fonts:
    main: pygame.font.Font
    sub: pygame.font.Font
    small: pygame.font.Font
    tiny: pygame.font.Font


class SaveManager:
    def __init__(self, save_path: Path, item_settings: ItemSettings, starting_balance: float) -> None:
        self.save_path = save_path
        self.item_settings = item_settings
        self.starting_balance = starting_balance

    def load(self) -> PlayerState:
        if not self.save_path.exists():
            return PlayerState(balance=self.starting_balance)
        try:
            data = json.loads(self.save_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return PlayerState(balance=self.starting_balance)

        balance = query_float(data.get("balance"), self.starting_balance)
        total_opened = int(query_float(data.get("total_opened"), 0.0))
        inventory: list[InventoryEntry] = []
        raw_inventory = data.get("inventory", [])
        if isinstance(raw_inventory, list):
            for raw in raw_inventory:
                if not isinstance(raw, dict):
                    continue
                name = str(raw.get("name", ""))
                item = self.item_settings.items.get(name)
                if item is None:
                    continue
                inventory.append(
                    InventoryEntry(
                        entry_id=str(raw.get("entry_id") or uuid.uuid4()),
                        name=item.name,
                        price=item.price,
                        source_case_id=str(raw.get("source_case_id", "unknown")),
                        created_at=query_float(raw.get("created_at"), time.time()),
                    )
                )
        return PlayerState(balance=max(0.0, balance), inventory=inventory, total_opened=max(0, total_opened))

    def save(self, state: PlayerState) -> None:
        payload = {
            "version": 2,
            "balance": round(state.balance, 2),
            "total_opened": state.total_opened,
            "inventory": [
                {
                    "entry_id": entry.entry_id,
                    "name": entry.name,
                    "price": entry.price,
                    "source_case_id": entry.source_case_id,
                    "created_at": entry.created_at,
                }
                for entry in state.inventory
            ],
        }
        self.save_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.save_path.with_suffix(self.save_path.suffix + ".tmp")
        temp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        temp_path.replace(self.save_path)


class CaseBattleGame:
    def __init__(self, app_settings: AppSettings, item_settings: ItemSettings, rng: random.Random) -> None:
        pygame.init()
        pygame.font.init()
        self.app = app_settings
        self.item_settings = item_settings
        self.rng = rng
        self.screen = pygame.display.set_mode(
            (self.app.width, self.app.height),
            pygame.FULLSCREEN | pygame.SCALED
        )
        pygame.display.set_caption(self.app.title)
        self.clock = pygame.time.Clock()
        self.fonts = Fonts(
            main=pygame.font.Font(None, 32),
            sub=pygame.font.Font(None, 24),
            small=pygame.font.Font(None, 20),
            tiny=pygame.font.Font(None, 17),
        )
        self.save_manager = SaveManager(self.app.save_path, self.item_settings, self.app.starting_balance)
        self.state = self.save_manager.load()
        self.roulette = RouletteState(duration=self.app.roulette_duration, target_index=self.app.roulette_target_index)
        self.upgrade = UpgradeState(result_color=self.app.colors.white)
        self.modals = ModalState()
        self.scroll = ScrollState()
        self.rects: dict[RectKey, pygame.Rect] = {}
        self.current_tab = "cases"
        self.selected_case_id = self.item_settings.cases[0].case_id if self.item_settings.cases else None
        self.running = True

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(self.app.fps) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
            pygame.display.flip()
        self.save_manager.save(self.state)
        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                continue
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
                continue
            if event.type == pygame.MOUSEWHEEL:
                self.handle_mouse_wheel(event)
                continue
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_left_click(event.pos)

    def handle_keydown(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            if self.modals.show_settings:
                self.modals.show_settings = False
                return
            if self.modals.show_drop_window:
                return
            self.current_tab = "cases"
            return
        if not self.modals.show_settings or not self.modals.add_balance_active:
            return
        if event.key == pygame.K_RETURN:
            self.try_add_balance_from_input()
            return
        if event.key == pygame.K_BACKSPACE:
            self.modals.add_balance_input = self.modals.add_balance_input[:-1]
            return
        if event.unicode.isdigit() or event.unicode == ".":
            if event.unicode == "." and "." in self.modals.add_balance_input:
                return
            if len(self.modals.add_balance_input) < 12:
                self.modals.add_balance_input += event.unicode

    def handle_mouse_wheel(self, event: pygame.event.Event) -> None:
        delta = event.y * self.app.scroll_step
        if self.current_tab == "cases":
            self.scroll.cases = clamp_int(self.scroll.cases + delta, -900, 0)
        elif self.current_tab == "inventory":
            max_scroll = min(0, self.app.height - 240 - query_inventory_total_height(self.state, self.app))
            self.scroll.inventory = clamp_int(self.scroll.inventory + delta, max_scroll, 0)
        elif self.current_tab == "upgrade":
            max_scroll = min(0, self.app.height - 260 - len(self.item_settings.items) * 46)
            self.scroll.upgrade_targets = clamp_int(self.scroll.upgrade_targets + delta, max_scroll, 0)

    def handle_left_click(self, mouse_pos: tuple[int, int]) -> None:
        if self.modals.show_settings:
            self.handle_settings_click(mouse_pos)
            return
        if self.modals.show_drop_window:
            self.handle_drop_modal_click(mouse_pos)
            return
        if self.roulette.active or self.upgrade.animating:
            return
        for tab_name in ("cases", "inventory", "upgrade"):
            if self.query_rect(("tab", tab_name)).collidepoint(mouse_pos):
                self.current_tab = tab_name
                return
        if self.query_rect(("tab", "exit")).collidepoint(mouse_pos):
            self.running = False
            return
        if self.query_rect(("button", "settings")).collidepoint(mouse_pos):
            self.modals.show_settings = True
            self.modals.add_balance_input = ""
            self.modals.add_balance_active = True
            return
        if self.current_tab == "cases":
            self.handle_cases_click(mouse_pos)
        elif self.current_tab == "inventory":
            self.handle_inventory_click(mouse_pos)
        elif self.current_tab == "upgrade":
            self.handle_upgrade_click(mouse_pos)

    def handle_settings_click(self, mouse_pos: tuple[int, int]) -> None:
        if self.query_rect(("settings", "input")).collidepoint(mouse_pos):
            self.modals.add_balance_active = True
            return
        if self.query_rect(("settings", "add")).collidepoint(mouse_pos):
            self.try_add_balance_from_input()
            return
        self.modals.show_settings = False
        self.modals.add_balance_active = False

    def handle_drop_modal_click(self, mouse_pos: tuple[int, int]) -> None:
        if self.query_rect(("drop", "keep")).collidepoint(mouse_pos):
            self.state.inventory[0:0] = self.roulette.pending_drops
            self.roulette.pending_drops = []
            self.modals.show_drop_window = False
            self.save_manager.save(self.state)
            return
        if self.query_rect(("drop", "sell")).collidepoint(mouse_pos):
            self.state.balance += sum(entry.price for entry in self.roulette.pending_drops)
            self.roulette.pending_drops = []
            self.modals.show_drop_window = False
            self.save_manager.save(self.state)

    def handle_cases_click(self, mouse_pos: tuple[int, int]) -> None:
        for case in self.item_settings.cases:
            if self.query_rect(("case", case.case_id)).collidepoint(mouse_pos):
                self.selected_case_id = case.case_id
                return
        selected_case = self.query_selected_case()
        if selected_case is None:
            return
        if self.query_rect(("open", "1")).collidepoint(mouse_pos):
            self.try_open_case(selected_case, 1)
            return
        if self.query_rect(("open", "10")).collidepoint(mouse_pos):
            self.try_open_case(selected_case, 10)

    def handle_inventory_click(self, mouse_pos: tuple[int, int]) -> None:
        for index, entry in enumerate(self.state.inventory):
            if self.query_rect(("sell", entry.entry_id)).collidepoint(mouse_pos):
                self.state.balance += entry.price
                self.state.inventory.pop(index)
                if self.upgrade.selected_entry_id == entry.entry_id:
                    self.upgrade = UpgradeState(result_color=self.app.colors.white)
                self.save_manager.save(self.state)
                return
        for entry in self.state.inventory:
            if self.query_rect(("inventory", entry.entry_id)).collidepoint(mouse_pos):
                self.upgrade.selected_entry_id = entry.entry_id
                self.upgrade.target_name = None
                self.upgrade.chance = 0.0
                self.upgrade.result_text = ""
                self.current_tab = "upgrade"
                return

    def handle_upgrade_click(self, mouse_pos: tuple[int, int]) -> None:
        selected_entry = self.query_selected_inventory_entry()
        for item in self.query_sorted_items_for_upgrade():
            if self.query_rect(("target", item.name)).collidepoint(mouse_pos):
                self.upgrade.target_name = item.name
                self.upgrade.result_text = ""
                if selected_entry is not None:
                    self.upgrade.chance = compute_upgrade_chance(selected_entry.price, item.price)
                return
        if self.query_rect(("upgrade", "run")).collidepoint(mouse_pos):
            if selected_entry is not None and self.upgrade.target_name is not None and self.upgrade.chance > 0:
                self.start_upgrade_roll(selected_entry)

    def try_add_balance_from_input(self) -> None:
        try:
            amount = float(self.modals.add_balance_input)
        except ValueError:
            amount = 0.0
        if amount > 0:
            self.state.balance += amount
            self.save_manager.save(self.state)
        self.modals.show_settings = False
        self.modals.add_balance_input = ""
        self.modals.add_balance_active = False

    def try_open_case(self, case: CaseDef, count: int) -> None:
        cost = case.price * count
        if self.state.balance < cost:
            return
        self.state.balance -= cost
        self.state.total_opened += count
        drops = [roll_item(case, self.item_settings, self.rng) for _ in range(count)]
        self.roulette.pending_drops = drops
        self.start_roulette(case, drops[0])
        self.save_manager.save(self.state)

    def start_roulette(self, case: CaseDef, winning_entry: InventoryEntry) -> None:
        card_step = self.app.card_width + self.app.card_gap
        target_index = self.app.roulette_target_index
        tape: list[InventoryEntry] = []
        for index in range(self.app.roulette_cards):
            if index == target_index:
                tape.append(winning_entry)
            else:
                tape.append(roll_item(case, self.item_settings, self.rng))
        marker_x = self.app.width / 2
        end_x = marker_x - target_index * card_step - self.app.card_width / 2
        start_x = end_x + self.rng.randint(22, 29) * card_step
        self.roulette = RouletteState(
            active=True,
            track_x=start_x,
            start_x=start_x,
            end_x=end_x,
            elapsed=0.0,
            duration=self.app.roulette_duration,
            target_index=target_index,
            tape=tape,
            pending_drops=self.roulette.pending_drops,
        )

    def start_upgrade_roll(self, selected_entry: InventoryEntry) -> None:
        sector = (self.upgrade.chance / 100.0) * 360.0
        sector = clamp_float(sector, 0.0, 360.0)
        self.upgrade.success = self.rng.random() <= self.upgrade.chance / 100.0
        if self.upgrade.success:
            final_angle = self.rng.uniform(2.0, max(2.1, sector - 2.0)) if sector > 4.0 else sector / 2.0
        else:
            final_angle = self.rng.uniform(min(359.0, sector + 3.0), 359.0) if sector < 357.0 else 359.0
        self.upgrade.elapsed = 0.0
        self.upgrade.start_angle = self.upgrade.angle % 360.0
        self.upgrade.end_angle = self.upgrade.start_angle + self.rng.randint(5, 7) * 360.0 + final_angle
        self.upgrade.animating = True
        self.upgrade.result_text = ""

    def update(self, dt: float) -> None:
        self.update_roulette(dt)
        self.update_upgrade(dt)

    def update_roulette(self, dt: float) -> None:
        if not self.roulette.active:
            return
        self.roulette.elapsed += dt
        progress = clamp_float(self.roulette.elapsed / self.roulette.duration, 0.0, 1.0)
        eased = ease_out_cubic(progress)
        self.roulette.track_x = lerp(self.roulette.start_x, self.roulette.end_x, eased)
        if progress >= 1.0:
            self.roulette.active = False
            self.roulette.track_x = self.roulette.end_x
            self.modals.show_drop_window = True

    def update_upgrade(self, dt: float) -> None:
        if not self.upgrade.animating:
            return
        self.upgrade.elapsed += dt
        progress = clamp_float(self.upgrade.elapsed / self.upgrade.duration, 0.0, 1.0)
        eased = ease_out_cubic(progress)
        self.upgrade.angle = lerp(self.upgrade.start_angle, self.upgrade.end_angle, eased)
        if progress < 1.0:
            return
        self.upgrade.animating = False
        selected_entry = self.query_selected_inventory_entry()
        target_name = self.upgrade.target_name
        if selected_entry is None or target_name is None:
            return
        self.remove_inventory_entry(selected_entry.entry_id)
        if self.upgrade.success:
            item = self.item_settings.items[target_name]
            self.state.inventory.insert(0, create_inventory_entry(item, "upgrade"))
            self.upgrade.result_text = "success: upgraded item added"
            self.upgrade.result_color = self.app.colors.green
        else:
            self.upgrade.result_text = "fail: source item lost"
            self.upgrade.result_color = self.app.colors.red
        self.upgrade.selected_entry_id = None
        self.upgrade.target_name = None
        self.upgrade.chance = 0.0
        self.save_manager.save(self.state)

    def draw(self) -> None:
        self.rects.clear()
        self.screen.fill(self.app.colors.bg)
        self.draw_header()
        if self.roulette.active:
            self.draw_roulette()
        elif self.current_tab == "cases":
            self.draw_cases_page()
        elif self.current_tab == "inventory":
            self.draw_inventory_page()
        elif self.current_tab == "upgrade":
            self.draw_upgrade_page()
        if self.modals.show_drop_window:
            self.draw_drop_modal()
        if self.modals.show_settings:
            self.draw_settings_modal()

    def draw_header(self) -> None:
        tabs = (("cases", "Cases"), ("inventory", "Inventory"), ("upgrade", "Upgrade"), ("exit", "Exit"))
        x = 30
        for tab_id, label in tabs:
            width = 130 if tab_id != "exit" else 90
            rect = pygame.Rect(x, 22, width, 38)
            self.rects[("tab", tab_id)] = rect
            color = self.app.colors.accent if self.current_tab == tab_id else self.app.colors.panel
            pygame.draw.rect(self.screen, color, rect, border_radius=6)
            draw_text_center(self.screen, self.fonts.sub, label, self.app.colors.white, rect)
            x += width + 12
        balance = self.fonts.main.render(f"balance: {format_money(self.state.balance)}", True, self.app.colors.green)
        self.screen.blit(balance, (self.app.width - balance.get_width() - 150, 26))
        settings_rect = pygame.Rect(self.app.width - 130, 24, 100, 36)
        self.rects[("button", "settings")] = settings_rect
        pygame.draw.rect(self.screen, self.app.colors.panel, settings_rect, border_radius=6)
        draw_text_center(self.screen, self.fonts.sub, "Settings", self.app.colors.white, settings_rect)
        pygame.draw.line(self.screen, (50, 50, 60), (0, 78), (self.app.width, 78), 2)

    def draw_cases_page(self) -> None:
        left_x = 50
        top_y = 112 + self.scroll.cases
        cols = 4
        title = self.fonts.main.render("available cases", True, self.app.colors.white)
        self.screen.blit(title, (left_x, 92))
        for index, case in enumerate(self.item_settings.cases):
            col = index % cols
            row = index // cols
            x = left_x + col * (self.app.case_card_width + self.app.case_card_gap)
            y = top_y + row * (self.app.case_card_height + self.app.case_card_gap)
            rect = pygame.Rect(x, y, self.app.case_card_width, self.app.case_card_height)
            self.rects[("case", case.case_id)] = rect
            if rect.bottom < 90 or rect.top > self.app.height - 20:
                continue
            if self.selected_case_id == case.case_id:
                pygame.draw.rect(self.screen, self.app.colors.accent, rect.inflate(8, 8), border_radius=14)
            pygame.draw.rect(self.screen, case.color, rect, border_radius=12)
            pygame.draw.rect(self.screen, self.app.colors.panel_light, rect, width=2, border_radius=12)
            name = self.fonts.main.render(case.name, True, self.app.colors.white)
            self.screen.blit(name, (rect.x + 18, rect.y + 18))
            price = self.fonts.sub.render(f"price: {format_money(case.price)}", True, self.app.colors.white)
            self.screen.blit(price, (rect.x + 18, rect.y + 62))
            item_count = self.fonts.sub.render(f"{len(case.item_names)} possible drops", True, self.app.colors.card_text)
            self.screen.blit(item_count, (rect.x + 18, rect.y + 96))
            ev = compute_expected_value(case, self.item_settings)
            ev_text = self.fonts.tiny.render(f"expected value: {format_money(ev)}", True, self.app.colors.text_muted)
            self.screen.blit(ev_text, (rect.x + 18, rect.y + 132))
        self.draw_selected_case_panel()

    def draw_selected_case_panel(self) -> None:
        case = self.query_selected_case()
        panel = pygame.Rect(self.app.width - 610, 110, 560, self.app.height - 160)
        pygame.draw.rect(self.screen, self.app.colors.panel, panel, border_radius=12)
        pygame.draw.rect(self.screen, self.app.colors.panel_light, panel, width=2, border_radius=12)
        if case is None:
            draw_text_center(self.screen, self.fonts.main, "select a case", self.app.colors.text_muted, panel)
            return
        self.screen.blit(self.fonts.main.render(case.name, True, self.app.colors.white), (panel.x + 24, panel.y + 22))
        self.screen.blit(self.fonts.sub.render(f"case price: {format_money(case.price)}", True, self.app.colors.green), (panel.x + 24, panel.y + 64))
        open_1 = pygame.Rect(panel.x + 24, panel.y + 108, 190, 46)
        open_10 = pygame.Rect(panel.x + 232, panel.y + 108, 190, 46)
        self.rects[("open", "1")] = open_1
        self.rects[("open", "10")] = open_10
        pygame.draw.rect(self.screen, self.app.colors.accent, open_1, border_radius=7)
        pygame.draw.rect(self.screen, self.app.colors.accent, open_10, border_radius=7)
        draw_text_center(self.screen, self.fonts.sub, "open x1", self.app.colors.white, open_1)
        draw_text_center(self.screen, self.fonts.sub, "open x10", self.app.colors.white, open_10)
        if self.state.balance < case.price:
            warn = self.fonts.small.render("not enough balance for this case", True, self.app.colors.red)
            self.screen.blit(warn, (panel.x + 24, panel.y + 170))
        header = self.fonts.sub.render("drop probabilities", True, self.app.colors.white)
        self.screen.blit(header, (panel.x + 24, panel.y + 212))
        probabilities = compute_item_probabilities(case, self.item_settings)
        sorted_names = sorted(case.item_names, key=lambda name: self.item_settings.items[name].price)
        start_y = panel.y + 250
        for index, name in enumerate(sorted_names[:15]):
            item = self.item_settings.items[name]
            y = start_y + index * 38
            rarity_color = query_rarity_color(item.price, self.app.colors)
            pygame.draw.circle(self.screen, rarity_color, (panel.x + 34, y + 13), 6)
            name_text = fit_text(self.fonts.small, name, 275)
            self.screen.blit(self.fonts.small.render(name_text, True, self.app.colors.white), (panel.x + 50, y + 4))
            price = self.fonts.tiny.render(format_money(item.price), True, self.app.colors.green)
            self.screen.blit(price, (panel.x + 340, y + 5))
            prob = self.fonts.tiny.render(f"{probabilities[name] * 100:.2f}%", True, self.app.colors.text_muted)
            self.screen.blit(prob, (panel.x + 445, y + 5))

    def draw_roulette(self) -> None:
        cx = self.app.width // 2
        cy = self.app.height // 2
        overlay = pygame.Surface((self.app.width, self.app.height))
        overlay.set_alpha(235)
        overlay.fill(self.app.colors.bg)
        self.screen.blit(overlay, (0, 0))
        band = pygame.Rect(0, cy - 150, self.app.width, 300)
        pygame.draw.rect(self.screen, self.app.colors.panel, band)
        pygame.draw.rect(self.screen, self.app.colors.panel_light, band, width=3)
        title = self.fonts.main.render("case is rolling", True, self.app.colors.accent)
        self.screen.blit(title, (cx - title.get_width() // 2, cy - 220))
        step = self.app.card_width + self.app.card_gap
        for index, entry in enumerate(self.roulette.tape):
            x = int(self.roulette.track_x + index * step)
            if x + self.app.card_width < 0 or x > self.app.width:
                continue
            rect = pygame.Rect(x, cy - self.app.card_height // 2, self.app.card_width, self.app.card_height)
            self.draw_item_card(rect, entry.name, entry.price, index == self.roulette.target_index)
        pygame.draw.line(self.screen, self.app.colors.accent, (cx, cy - 165), (cx, cy + 165), 5)
        pygame.draw.polygon(self.screen, self.app.colors.accent, [(cx, cy - 148), (cx - 18, cy - 178), (cx + 18, cy - 178)])
        pygame.draw.polygon(self.screen, self.app.colors.accent, [(cx, cy + 148), (cx - 18, cy + 178), (cx + 18, cy + 178)])

    def draw_inventory_page(self) -> None:
        title = self.fonts.main.render(f"inventory: {len(self.state.inventory)} items", True, self.app.colors.white)
        self.screen.blit(title, (50, 98))
        if not self.state.inventory:
            draw_text_center(
                self.screen,
                self.fonts.main,
                "inventory is empty. open cases first.",
                self.app.colors.text_muted,
                pygame.Rect(0, 120, self.app.width, self.app.height - 160),
            )
            return
        start_x = 50
        start_y = 145 + self.scroll.inventory
        step_x = self.app.inventory_card_width + self.app.inventory_card_gap
        step_y = self.app.inventory_card_height + self.app.inventory_card_gap
        for index, entry in enumerate(self.state.inventory):
            col = index % self.app.inventory_columns
            row = index // self.app.inventory_columns
            x = start_x + col * step_x
            y = start_y + row * step_y
            rect = pygame.Rect(x, y, self.app.inventory_card_width, self.app.inventory_card_height)
            sell_rect = pygame.Rect(x + self.app.inventory_card_width - 84, y + self.app.inventory_card_height - 34, 70, 26)
            self.rects[("inventory", entry.entry_id)] = rect
            self.rects[("sell", entry.entry_id)] = sell_rect
            if rect.bottom < 90 or rect.top > self.app.height - 20:
                continue
            selected = self.upgrade.selected_entry_id == entry.entry_id
            if selected:
                pygame.draw.rect(self.screen, self.app.colors.accent, rect.inflate(6, 6), border_radius=10)
            self.draw_item_card(rect, entry.name, entry.price, False)
            pygame.draw.rect(self.screen, self.app.colors.red, sell_rect, border_radius=5)
            draw_text_center(self.screen, self.fonts.tiny, "sell", self.app.colors.white, sell_rect)

    def draw_upgrade_page(self) -> None:
        selected_entry = self.query_selected_inventory_entry()
        left_panel = pygame.Rect(50, 112, 400, 210)
        pygame.draw.rect(self.screen, self.app.colors.panel, left_panel, border_radius=12)
        pygame.draw.rect(self.screen, self.app.colors.panel_light, left_panel, width=2, border_radius=12)
        self.screen.blit(self.fonts.sub.render("source item", True, self.app.colors.text_muted), (left_panel.x + 18, left_panel.y + 18))
        if selected_entry is None:
            self.screen.blit(self.fonts.sub.render("select an item in inventory", True, self.app.colors.text_muted), (left_panel.x + 18, left_panel.y + 76))
        else:
            self.screen.blit(self.fonts.sub.render(fit_text(self.fonts.sub, selected_entry.name, 350), True, self.app.colors.white), (left_panel.x + 18, left_panel.y + 72))
            self.screen.blit(self.fonts.main.render(format_money(selected_entry.price), True, self.app.colors.green), (left_panel.x + 18, left_panel.y + 112))
        self.draw_upgrade_wheel()
        self.draw_upgrade_targets()
        if self.upgrade.result_text:
            result = self.fonts.main.render(self.upgrade.result_text, True, self.upgrade.result_color)
            self.screen.blit(result, (self.app.width // 2 - result.get_width() // 2, 560))
        if selected_entry is not None and self.upgrade.target_name is not None and self.upgrade.chance > 0 and not self.upgrade.animating:
            btn = pygame.Rect(self.app.width // 2 - 110, 610, 220, 50)
            self.rects[("upgrade", "run")] = btn
            pygame.draw.rect(self.screen, self.app.colors.accent, btn, border_radius=8)
            draw_text_center(self.screen, self.fonts.main, "upgrade", self.app.colors.white, btn)

    def draw_upgrade_wheel(self) -> None:
        cx, cy = self.app.width // 2, 330
        radius = 125
        pygame.draw.circle(self.screen, (20, 17, 28), (cx, cy), radius)
        pygame.draw.circle(self.screen, self.app.colors.panel_light, (cx, cy), radius, width=2)
        sector_width = int((self.upgrade.chance / 100.0) * 360)
        for deg in range(360):
            rad = math.radians(deg - 90)
            color = self.app.colors.accent if deg < sector_width else (42, 37, 52)
            tx = cx + int(math.cos(rad) * (radius - 6))
            ty = cy + int(math.sin(rad) * (radius - 6))
            pygame.draw.circle(self.screen, color, (tx, ty), 4)
        pointer_angle = self.upgrade.angle - 90
        rad_arrow = math.radians(pointer_angle)
        p_tip = (cx + int(math.cos(rad_arrow) * (radius - 8)), cy + int(math.sin(rad_arrow) * (radius - 8)))
        p_left = (cx + int(math.cos(math.radians(pointer_angle - 11)) * (radius - 35)), cy + int(math.sin(math.radians(pointer_angle - 11)) * (radius - 35)))
        p_right = (cx + int(math.cos(math.radians(pointer_angle + 11)) * (radius - 35)), cy + int(math.sin(math.radians(pointer_angle + 11)) * (radius - 35)))
        pygame.draw.polygon(self.screen, self.app.colors.white, [p_tip, p_left, p_right])
        pygame.draw.circle(self.screen, self.app.colors.white, (cx, cy), 9)
        chance = self.fonts.main.render(f"{self.upgrade.chance:.1f}%", True, self.app.colors.accent)
        self.screen.blit(chance, (cx - chance.get_width() // 2, cy - 18))

    def draw_upgrade_targets(self) -> None:
        panel = pygame.Rect(self.app.width - 455, 92, 405, self.app.height - 125)
        pygame.draw.rect(self.screen, self.app.colors.panel, panel, border_radius=12)
        pygame.draw.rect(self.screen, self.app.colors.panel_light, panel, width=2, border_radius=12)
        self.screen.blit(self.fonts.sub.render("target item", True, self.app.colors.white), (panel.x + 18, panel.y + 18))
        start_y = panel.y + 58 + self.scroll.upgrade_targets
        for index, item in enumerate(self.query_sorted_items_for_upgrade()):
            y = start_y + index * 46
            rect = pygame.Rect(panel.x + 12, y, panel.width - 24, 38)
            self.rects[("target", item.name)] = rect
            if rect.bottom < panel.y + 50 or rect.top > panel.bottom - 10:
                continue
            selected = self.upgrade.target_name == item.name
            color = (60, 55, 75) if selected else (23, 20, 32)
            pygame.draw.rect(self.screen, color, rect, border_radius=6)
            if selected:
                pygame.draw.rect(self.screen, self.app.colors.accent, rect, width=2, border_radius=6)
            rarity_color = query_rarity_color(item.price, self.app.colors)
            pygame.draw.circle(self.screen, rarity_color, (rect.x + 12, rect.y + 19), 5)
            self.screen.blit(self.fonts.tiny.render(fit_text(self.fonts.tiny, item.name, 250), True, self.app.colors.white), (rect.x + 24, rect.y + 11))
            price = self.fonts.tiny.render(format_money(item.price), True, self.app.colors.green)
            self.screen.blit(price, (rect.right - price.get_width() - 10, rect.y + 11))

    def draw_drop_modal(self) -> None:
        overlay = pygame.Surface((self.app.width, self.app.height))
        overlay.set_alpha(205)
        overlay.fill(self.app.colors.black)
        self.screen.blit(overlay, (0, 0))
        panel = pygame.Rect(self.app.width // 2 - 430, self.app.height // 2 - 270, 860, 540)
        pygame.draw.rect(self.screen, self.app.colors.panel, panel, border_radius=16)
        pygame.draw.rect(self.screen, self.app.colors.accent, panel, width=3, border_radius=16)
        title = self.fonts.main.render("you won", True, self.app.colors.accent)
        self.screen.blit(title, (panel.centerx - title.get_width() // 2, panel.y + 28))
        for index, entry in enumerate(self.roulette.pending_drops[:20]):
            col = 0 if index < 10 else 1
            row = index % 10
            x = panel.x + 42 + col * 405
            y = panel.y + 82 + row * 34
            color = query_rarity_color(entry.price, self.app.colors)
            pygame.draw.circle(self.screen, color, (x, y + 10), 5)
            text = self.fonts.small.render(f"{fit_text(self.fonts.small, entry.name, 250)}  {format_money(entry.price)}", True, self.app.colors.white)
            self.screen.blit(text, (x + 14, y))
        total = sum(entry.price for entry in self.roulette.pending_drops)
        keep_btn = pygame.Rect(panel.x + 55, panel.bottom - 82, 330, 48)
        sell_btn = pygame.Rect(panel.right - 385, panel.bottom - 82, 330, 48)
        self.rects[("drop", "keep")] = keep_btn
        self.rects[("drop", "sell")] = sell_btn
        pygame.draw.rect(self.screen, self.app.colors.green, keep_btn, border_radius=8)
        pygame.draw.rect(self.screen, self.app.colors.red, sell_btn, border_radius=8)
        draw_text_center(self.screen, self.fonts.sub, "keep and add to inventory", self.app.colors.white, keep_btn)
        draw_text_center(self.screen, self.fonts.sub, f"sell all +{format_money(total)}", self.app.colors.white, sell_btn)

    def draw_settings_modal(self) -> None:
        overlay = pygame.Surface((self.app.width, self.app.height))
        overlay.set_alpha(180)
        overlay.fill(self.app.colors.black)
        self.screen.blit(overlay, (0, 0))
        panel = pygame.Rect(self.app.width // 2 - 260, self.app.height // 2 - 155, 520, 310)
        input_rect = pygame.Rect(panel.x + 90, panel.y + 110, 340, 52)
        add_btn = pygame.Rect(panel.x + 150, panel.y + 190, 220, 50)
        self.rects[("settings", "input")] = input_rect
        self.rects[("settings", "add")] = add_btn
        pygame.draw.rect(self.screen, self.app.colors.panel, panel, border_radius=14)
        pygame.draw.rect(self.screen, self.app.colors.accent, panel, width=3, border_radius=14)
        title = self.fonts.main.render("add balance", True, self.app.colors.white)
        self.screen.blit(title, (panel.centerx - title.get_width() // 2, panel.y + 38))
        pygame.draw.rect(self.screen, (40, 35, 55), input_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.app.colors.white, input_rect, width=2, border_radius=8)
        cursor = "|" if self.modals.add_balance_active else ""
        value = self.fonts.main.render(self.modals.add_balance_input + cursor, True, self.app.colors.white)
        self.screen.blit(value, (input_rect.x + 14, input_rect.y + 13))
        pygame.draw.rect(self.screen, self.app.colors.green, add_btn, border_radius=8)
        draw_text_center(self.screen, self.fonts.sub, "add balance", self.app.colors.white, add_btn)

    def draw_item_card(self, rect: pygame.Rect, name: str, price: float, selected: bool) -> None:
        pygame.draw.rect(self.screen, self.app.colors.panel_soft, rect, border_radius=10)
        border = self.app.colors.accent if selected else query_rarity_color(price, self.app.colors)
        pygame.draw.rect(self.screen, border, rect, width=3, border_radius=10)
        rarity = query_rarity_name(price)
        rarity_txt = self.fonts.tiny.render(rarity, True, border)
        self.screen.blit(rarity_txt, (rect.x + 12, rect.y + 10))
        name_txt = fit_text(self.fonts.small, name, rect.width - 24)
        self.screen.blit(self.fonts.small.render(name_txt, True, self.app.colors.white), (rect.x + 12, rect.y + 42))
        price_txt = self.fonts.sub.render(format_money(price), True, self.app.colors.green)
        self.screen.blit(price_txt, (rect.x + 12, rect.bottom - 34))

    def query_selected_case(self) -> CaseDef | None:
        if self.selected_case_id is None:
            return None
        return query_case_by_id(self.item_settings.cases, self.selected_case_id)

    def query_selected_inventory_entry(self) -> InventoryEntry | None:
        if self.upgrade.selected_entry_id is None:
            return None
        for entry in self.state.inventory:
            if entry.entry_id == self.upgrade.selected_entry_id:
                return entry
        return None

    def query_sorted_items_for_upgrade(self) -> list[ItemDef]:
        return sorted(self.item_settings.items.values(), key=lambda item: item.price)

    def query_rect(self, key: RectKey) -> pygame.Rect:
        return self.rects.get(key, pygame.Rect(-10000, -10000, 1, 1))

    def remove_inventory_entry(self, entry_id: str) -> None:
        self.state.inventory = [entry for entry in self.state.inventory if entry.entry_id != entry_id]


def create_app_settings() -> AppSettings:
    colors = Colors()
    return AppSettings(
        width=1920,
        height=1080,
        fps=60,
        title="Case-Battle Python Edition",
        save_path=Path("case_battle_save.json"),
        starting_balance=10000.0,
        colors=colors,
        card_width=240,
        card_height=160,
        card_gap=16,
        roulette_duration=3.4,
        roulette_cards=90,
        roulette_target_index=52,
        inventory_columns=6,
        inventory_card_width=270,
        inventory_card_height=116,
        inventory_card_gap=18,
        case_card_width=250,
        case_card_height=170,
        case_card_gap=24,
        scroll_step=48,
    )


def create_item_settings() -> ItemSettings:
    # all item and case data is isolated here so balance, ui, and animation code do not know raw prices.
    raw_items = [
        ("AK-47 | Slate", 315.0),
        ("AWP | Asiimov", 2150.0),
        ("Desert Eagle | Printstream", 5580.0),
        ("Desert Eagle | Code Red", 14545.0),
        ("M4A1-S | Printstream", 84373.49),
        ("Glock-18 | Fade", 147824.15),
        ("Knife | Karambit | Lore", 750800.0),
        ("AK-47 | Fire Serpent", 236305.99),
        ("AWP | Gungnir", 720000.0),
        ("Butterfly Knife | Gamma Doppler Emerald ST", 1145483.0),
        ("AK-47 | Wild Lotus", 1143253.0),
        ("AWP | Dragon Lore", 905000.0),
        ("★ Butterfly Knife | Doppler Ruby", 834010.0),
        ("★ Flip Knife | Doppler Black Pearl", 772235.32),
        ("M4A4 | Howl", 760980.0),
        ("★ Sport Gloves | Ultra Violent", 700000.0),
        ("★ Sport Gloves | Superconductor", 676529.48),
        ("★ Sport Gloves | Hedge Maze", 666000.0),
        ("★ Karambit | Doppler Black Pearl", 650000.0),
        ("★ M9 Bayonet | Doppler Ruby", 630500.0),
        ("★ Butterfly Knife | Doppler Sapphire", 580000.0),
        ("★ Moto Gloves | Spearmint", 550590.0),
        ("★ M9 Bayonet | Gamma Doppler Emerald", 550000.0),
        ("★ Karambit | Gamma Doppler Emerald", 540750.0),
        ("★ Karambit | Crimson Web", 532000.0),
        ("★ Sport Gloves | Pandora's Box", 486000.99),
        ("AK-47 | Hydroponic", 444232.0),
        ("★ Specialist Gloves | Emerald Web", 369563.0),
        ("AWP | Medusa", 360000.0),
        ("★ Butterfly Knife | Doppler Phase 2", 350000.0),
        ("★ Sport Gloves | Arid", 300000.0),
        ("★ Sport Gloves | Occult", 250000.0),
        ("★ Specialist Gloves | Crimson Kimono", 230000.0),
        ("M4A1-S | Knight", 231763.73),
        ("★ Butterfly Knife | Doppler Phase 4", 230630.32),
        ("Souvenir AK-47 | Gold Arabesque", 231000.30),
        ("★ Skeleton Knife | Doppler Ruby", 229550.80),
        ("AWP | The Prince", 220254.05),
        ("AK-47 | X-Ray", 223000.54),
        ("★ Talon Knife | Doppler Ruby", 222460.47),
        ("★ Paracord Knife | Crimson Web", 216087.0),
        ("★ Butterfly Knife | Lore", 214209.88),
        ("★ Butterfly Knife | Doppler Phase 1", 209600.0),
        ("MP9 | Wild Lily", 208883.11),
        ("★ Sport Gloves | Slingshot", 205728.0),
        ("★ Driver Gloves | Crimson Weave", 205024.96),
        ("★ Driver Gloves | King Snake", 198850.70),
        ("★ Sport Gloves | Nocts", 197801.71),
        ("★ Karambit | Autotronic", 196922.03),
        ("★ Moto Gloves | Cool Mint", 184747.40),
        ("M4A4 | Poseidon", 177690.25),
        ("★ Sport Gloves | Amphibious", 180315.0),
        ("★ Butterfly Knife | Fade", 176071.26),
        ("Negev | Mjölnir", 175275.0),
        ("M4A4 | The Coalition", 174654.33),
        ("★ Specialist Gloves | Cloud Chaser", 173754.42),
        ("★ Bayonet | Doppler Ruby", 172423.67),
        ("M4A1-S | Hot Rod", 160110.26),
        ("★ Talon Knife | Doppler Sapphire ST", 165452.18),
        ("★ Bayonet | Gamma Doppler Emerald", 162750.20),
        ("★ Driver Gloves | Garden", 160950.69),
        ("M4A1-S | Welcome to the Jungle", 160000.21),
        ("★ Sport Gloves | Violet Beadwork", 160316.48),
        ("★ Stiletto Knife | Doppler Black Pearl", 158232.67),
        ("★ Karambit | Slaughter", 157564.30),
        ("★ Specialist Gloves | Foundation", 157193.39),
        ("★ Karambit | Fade", 155300.66),
        ("★ Driver Gloves | Snow Leopard", 154417.99),
        ("AWP | Desert Hydra", 153711.40),
        ("AK-47 | Vulcan", 150586.82),
        ("Sticker | Vox Eminor (Holo) | Katowice 2015", 149683.91),
        ("★ Bayonet | Doppler Black Pearl", 149394.68),
        ("★ Specialist Gloves | Fade", 146804.35),
        ("★ Stiletto Knife | Doppler Ruby", 144772.25),
        ("★ Karambit | Night", 143621.32),
        ("★ M9 Bayonet | Autotronic", 139775.17),
        ("AK-47 | Wasteland Rebel", 134274.54),
        ("Sticker | ropz (Gold) | Krakow 2017", 132005.94),
        ("★ Flip Knife | Doppler Ruby", 131223.48),
        ("★ Karambit | Case Hardened", 131005.17),
        ("★ M9 Bayonet | Case Hardened", 130495.78),
        ("★ Sport Gloves | Omega", 127567.0),
        ("★ Butterfly Knife | Blue Steel", 124613.47),
        ("★ Karambit | Ultraviolet", 123384.64),
        ("M4A4 | Daybreak", 121843.73),
        ("★ Flip Knife | Gamma Doppler Emerald", 121194.81),
        ("★ Butterfly Knife | Slaughter", 117489.57),
        ("★ Butterfly Knife | Marble Fade", 117347.03),
        ("★ M9 Bayonet | Lore", 115957.66),
        ("M4A1-S | Imminent Danger", 114813.60),
        ("★ Sport Gloves | Vice", 114682.32),
        ("★ Karambit | Doppler Phase 1", 113656.05),
        ("★ Hand Wraps | Leather", 113470.75),
        ("★ Huntsman Knife | Doppler Black Pearl", 112430.22),
        ("★ Butterfly Knife | Freehand", 111337.18),
        ("★ Hand Wraps | Slaughter", 108446.66),
        ("★ Kukri Knife | Crimson Web", 105604.90),
        ("★ M9 Bayonet | Doppler Phase 2", 105526.13),
        ("★ Moto Gloves | Eclipse", 104377.57),
        ("★ Driver Gloves | Lunar Weave", 103914.70),
        ("★ Moto Gloves | Boom!", 103700.14),
        ("★ Butterfly Knife | Tiger Tooth", 103450.32),
        ("★ M9 Bayonet | Doppler Phase 1", 101829.14),
        ("★ Butterfly Knife", 100545.55),
        ("★ Hand Wraps | Cobalt Skulls", 99410.50),
        ("AK-47 | Jet Set", 93453.91),
        ("AWP | CMYK", 93128.32),
        ("★ Talon Knife | Fade ST", 92780.23),
        ("★ Nomad Knife | Doppler Black Pearl", 91481.63),
        ("★ Nomad Knife | Doppler Ruby", 90702.93),
        ("★ Driver Gloves | Convoy", 90460.61),
        ("AWP | Oni Taiji", 90449.36),
        ("★ Survival Knife | Doppler Ruby", 89880.71),
        ("★ Flip Knife | Crimson Web", 89039.73),
        ("M4A4 | Eye of Horus", 87689.37),
        ("AK-47 | Red Laminate", 87279.01),
        ("★ M9 Bayonet | Doppler Phase 4", 86402.03),
        ("AWP | Fade", 86396.03),
        ("★ Stiletto Knife | Crimson Web", 86395.28),
        ("★ Driver Gloves | Plum Quill", 85999.92),
        ("★ Specialist Gloves | Field Agent", 85741.85),
        ("★ Stiletto Knife | Doppler Sapphire", 85237.72),
        ("★ Karambit Knife", 84912.13),
        ("★ Driver Gloves | Diamondback", 84726.83),
        ("★ Ursus Knife | Doppler Black Pearl", 82684.79),
        ("★ Karambit | Black Laminate", 82342.70),
        ("MP9 | Bulldozer", 81748.54),
        ("★ Falchion Knife | Doppler Black Pearl", 81402.70),
        ("★ Flip Knife | Doppler Sapphire", 81170.88),
        ("★ Specialist Gloves | Crimson Web", 81053.10),
        ("AK-47 | Case Hardened", 79849.79),
        ("Glock-18 | Twilight Galaxy", 79689.99),
        ("Sticker | Team Dignitas (Holo) | Cologne 2016", 77308.86),
        ("★ Skeleton Knife | Case Hardened", 77308.86),
        ("MLG Columbus 2016 Cobblestone Souvenir Package", 77149.06),
        ("AWP | LongDog", 76836.98),
        ("★ Bowie Knife | Doppler Black Pearl", 76035.77),
        ("AUG | Akihabara Accept", 75617.90),
        ("★ Huntsman Knife | Doppler Ruby", 74259.29),
        ("★ Driver Gloves | Imperial Plaid", 73482.84),
        ("★ Falchion Knife | Gamma Doppler Emerald", 73064.22),
        ("★ Specialist Gloves | Tiger Strike", 73049.22),
    ]
    items = {name: ItemDef(name=name, price=float(price)) for name, price in raw_items}
    cases = (
        CaseDef(
            case_id="leon_kennedy",
            name="LEON KENNEDY",
            price=1000.0,
            color=(60, 80, 140),
            item_names=(
                "AK-47 | Slate",
                "AWP | Asiimov",
                "Desert Eagle | Printstream",
                "Desert Eagle | Code Red",
                "AK-47 | Case Hardened",
                "Glock-18 | Twilight Galaxy",
                "M4A1-S | Printstream",
                "Glock-18 | Fade",
                "★ Butterfly Knife",
                "★ Butterfly Knife | Tiger Tooth",
            ),
        ),
        CaseDef(
            case_id="victor_gideon",
            name="VICTOR GIDEON",
            price=4000.0,
            color=(50, 120, 70),
            item_names=(
                "M4A1-S | Printstream",
                "AWP | Asiimov",
                "Desert Eagle | Code Red",
                "M4A4 | Eye of Horus",
                "AWP | Fade",
                "★ Flip Knife | Crimson Web",
                "★ Driver Gloves | Diamondback",
                "★ Karambit Knife",
                "★ M9 Bayonet | Case Hardened",
                "★ Sport Gloves | Omega",
            ),
        ),
        CaseDef(
            case_id="homelander",
            name="HOMELANDER",
            price=10000.0,
            color=(140, 50, 50),
            item_names=(
                "Knife | Karambit | Lore",
                "AK-47 | Fire Serpent",
                "AWP | Gungnir",
                "M4A4 | Howl",
                "AWP | Dragon Lore",
                "★ Butterfly Knife | Doppler Ruby",
                "★ Flip Knife | Doppler Black Pearl",
                "★ Karambit | Doppler Black Pearl",
                "AK-47 | Wild Lotus",
                "Butterfly Knife | Gamma Doppler Emerald ST",
            ),
        ),
        CaseDef(
            case_id="mirage_gold",
            name="MIRAGE GOLD",
            price=25000.0,
            color=(148, 105, 45),
            item_names=(
                "Souvenir AK-47 | Gold Arabesque",
                "AK-47 | Hydroponic",
                "AK-47 | X-Ray",
                "AK-47 | Vulcan",
                "AK-47 | Wasteland Rebel",
                "AK-47 | Jet Set",
                "AK-47 | Red Laminate",
                "AK-47 | Case Hardened",
                "Sticker | Vox Eminor (Holo) | Katowice 2015",
                "Sticker | ropz (Gold) | Krakow 2017",
            ),
        ),
        CaseDef(
            case_id="dragon_vault",
            name="DRAGON VAULT",
            price=75000.0,
            color=(95, 58, 155),
            item_names=(
                "AWP | Dragon Lore",
                "AWP | Gungnir",
                "AWP | Medusa",
                "AWP | The Prince",
                "AWP | Desert Hydra",
                "AWP | Fade",
                "AWP | CMYK",
                "AWP | Oni Taiji",
                "AWP | LongDog",
                "AUG | Akihabara Accept",
            ),
        ),
        CaseDef(
            case_id="glove_room",
            name="GLOVE ROOM",
            price=150000.0,
            color=(100, 100, 55),
            item_names=(
                "★ Sport Gloves | Pandora's Box",
                "★ Sport Gloves | Superconductor",
                "★ Sport Gloves | Hedge Maze",
                "★ Sport Gloves | Ultra Violent",
                "★ Sport Gloves | Vice",
                "★ Sport Gloves | Omega",
                "★ Sport Gloves | Amphibious",
                "★ Sport Gloves | Slingshot",
                "★ Moto Gloves | Spearmint",
                "★ Moto Gloves | Cool Mint",
                "★ Driver Gloves | Crimson Weave",
                "★ Driver Gloves | King Snake",
                "★ Driver Gloves | Snow Leopard",
                "★ Specialist Gloves | Crimson Kimono",
            ),
        ),
        CaseDef(
            case_id="doppler_dream",
            name="DOPPLER DREAM",
            price=300000.0,
            color=(54, 95, 145),
            item_names=(
                "★ Butterfly Knife | Doppler Ruby",
                "★ Butterfly Knife | Doppler Sapphire",
                "★ Butterfly Knife | Doppler Phase 2",
                "★ Butterfly Knife | Doppler Phase 4",
                "★ Butterfly Knife | Doppler Phase 1",
                "★ M9 Bayonet | Doppler Ruby",
                "★ M9 Bayonet | Gamma Doppler Emerald",
                "★ M9 Bayonet | Doppler Phase 2",
                "★ M9 Bayonet | Doppler Phase 1",
                "★ Flip Knife | Doppler Ruby",
                "★ Flip Knife | Doppler Sapphire",
                "★ Flip Knife | Gamma Doppler Emerald",
                "★ Skeleton Knife | Doppler Ruby",
                "★ Stiletto Knife | Doppler Ruby",
                "★ Bayonet | Doppler Black Pearl",
            ),
        ),
        CaseDef(
            case_id="katowice_legends",
            name="KATOWICE LEGENDS",
            price=500000.0,
            color=(115, 55, 90),
            item_names=(
                "Sticker | Vox Eminor (Holo) | Katowice 2015",
                "Sticker | ropz (Gold) | Krakow 2017",
                "MLG Columbus 2016 Cobblestone Souvenir Package",
                "M4A4 | Howl",
                "M4A4 | Poseidon",
                "M4A4 | Daybreak",
                "M4A4 | Eye of Horus",
                "M4A4 | The Coalition",
                "M4A1-S | Welcome to the Jungle",
                "M4A1-S | Imminent Danger",
                "M4A1-S | Hot Rod",
                "M4A1-S | Knight",
            ),
        ),
    )
    validate_case_items(items, cases)
    return ItemSettings(items=items, cases=cases, price_probability_power=0.62)


def validate_case_items(items: dict[str, ItemDef], cases: tuple[CaseDef, ...]) -> None:
    missing = []
    for case in cases:
        for name in case.item_names:
            if name not in items:
                missing.append(f"{case.case_id}: {name}")
    if missing:
        raise ValueError("missing item settings: " + ", ".join(missing))


def roll_item(case: CaseDef, item_settings: ItemSettings, rng: random.Random) -> InventoryEntry:
    probabilities = compute_item_probabilities(case, item_settings)
    names = list(probabilities.keys())
    weights = [probabilities[name] for name in names]
    selected_name = rng.choices(names, weights=weights, k=1)[0]
    selected_item = item_settings.items[selected_name]
    return create_inventory_entry(selected_item, case.case_id)


def compute_item_probabilities(case: CaseDef, item_settings: ItemSettings) -> dict[str, float]:
    # high price means lower weight, but never zero chance.
    raw_weights: dict[str, float] = {}
    for name in case.item_names:
        price = max(1.0, item_settings.items[name].price)
        raw_weights[name] = 1.0 / (price ** item_settings.price_probability_power)
    total = sum(raw_weights.values())
    if total <= 0:
        fair = 1.0 / max(1, len(case.item_names))
        return {name: fair for name in case.item_names}
    return {name: weight / total for name, weight in raw_weights.items()}


def compute_expected_value(case: CaseDef, item_settings: ItemSettings) -> float:
    probabilities = compute_item_probabilities(case, item_settings)
    return sum(item_settings.items[name].price * probability for name, probability in probabilities.items())


def compute_upgrade_chance(item_price: float, target_price: float) -> float:
    if target_price <= 0:
        return 0.0
    chance = (item_price / target_price) * 100.0 # 100% drop of less expensive item
    return clamp_float(chance, 5.0, 100.0)


def create_inventory_entry(item: ItemDef, source_case_id: str) -> InventoryEntry:
    return InventoryEntry(
        entry_id=uuid.uuid4().hex,
        name=item.name,
        price=item.price,
        source_case_id=source_case_id,
        created_at=time.time(),
    )


def query_case_by_id(cases: tuple[CaseDef, ...], case_id: str) -> CaseDef | None:
    for case in cases:
        if case.case_id == case_id:
            return case
    return None


def query_inventory_total_height(state: PlayerState, app: AppSettings) -> int:
    if not state.inventory:
        return 0
    rows = math.ceil(len(state.inventory) / app.inventory_columns)
    return rows * (app.inventory_card_height + app.inventory_card_gap)


def query_float(value: object, fallback: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def query_rarity_name(price: float) -> str:
    if price >= 500000:
        return "legendary"
    if price >= 200000:
        return "red special"
    if price >= 75000:
        return "covert"
    if price >= 10000:
        return "classified"
    if price >= 1000:
        return "restricted"
    return "consumer"


def query_rarity_color(price: float, colors: Colors) -> Color:
    if price >= 500000:
        return colors.gold
    if price >= 200000:
        return colors.red
    if price >= 75000:
        return colors.purple
    if price >= 10000:
        return colors.blue
    if price >= 1000:
        return (70, 170, 220)
    return (120, 120, 135)


def format_money(value: float) -> str:
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}m r"
    if value >= 100_000:
        return f"{value / 1000:.0f}k r"
    if value >= 10_000:
        return f"{value / 1000:.1f}k r"
    return f"{value:.0f} r"


def fit_text(font: pygame.font.Font, text: str, max_width: int) -> str:
    if font.size(text)[0] <= max_width:
        return text
    clipped = text
    while clipped and font.size(clipped + "...")[0] > max_width:
        clipped = clipped[:-1]
    return clipped + "..." if clipped else "..."


def draw_text_center(surface: pygame.Surface, font: pygame.font.Font, text: str, color: Color, rect: pygame.Rect) -> None:
    rendered = font.render(text, True, color)
    surface.blit(rendered, (rect.centerx - rendered.get_width() // 2, rect.centery - rendered.get_height() // 2))


def ease_out_cubic(t: float) -> float:
    t = clamp_float(t, 0.0, 1.0)
    return 1.0 - (1.0 - t) ** 3


def lerp(start: float, end: float, t: float) -> float:
    return start + (end - start) * t


def clamp_float(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def clamp_int(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def main() -> None:
    app_settings = create_app_settings()
    item_settings = create_item_settings()
    game = CaseBattleGame(app_settings, item_settings, random.Random())
    game.run()


if __name__ == "__main__":
    main()
