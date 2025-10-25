import pygame
import sys
import json
from train_helper.data_classes import Question, Answer, QuestionType
from attempts import AttemptStorage

pygame.init()
screen = pygame.display.set_mode((1500, 1050), pygame.FULLSCREEN | pygame.SCALED)
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 28)
SMALL = pygame.font.SysFont("Arial", 20)
WHITE, BLACK, GRAY, GREEN, RED, BLUE = (255, 255, 255), (0, 0, 0), (200, 200, 200), (50, 200, 100), (200, 50, 50), (50, 50, 255)

def render_multiline_text(text, font, color, max_width, line_spacing=10):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    surfaces = []
    width = 0
    height = 0
    for line in lines:
        surf = font.render(line, True, color)
        surfaces.append(surf)
        width = max(width, surf.get_width())
        height += surf.get_height() + line_spacing

    return surfaces, width, height - line_spacing  # remove last spacing


class AnswerButton:
    def __init__(self, answer: Answer, rect: pygame.Rect):
        self.answer = answer
        self.rect = rect
        self.active = False
        self.validated = False

    def draw(self, surf):
        if self.validated:
            color = GREEN if self.answer.is_true else RED if self.active else GRAY
        else:
            color = GREEN if self.active else GRAY
        pygame.draw.rect(surf, color, self.rect)
        pygame.draw.rect(surf, BLACK, self.rect, 2)
        text = SMALL.render(self.answer.data, True, BLACK)
        surf.blit(text, (self.rect.x + 10, self.rect.y + 8))

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.active = not self.active

# TODO
# вьювер не использует тип вопроса, сейчас он по умолчанию работает по QuestionType.CHOISE, нужно добавить эту логику
class QuizApp:
    def __init__(self, questions: list[Question]):
        self.questions = questions
        self.index = 0
        self.buttons: list[AnswerButton] = []
        self.correct_count = 0
        self.wrong_count = 0
        self.selected_answers: dict[str, list[str]] = {}  # question_id -> list of selected answer ids
        self.validated = False
        self.storage = AttemptStorage()
        self.screen_w, self.screen_h = screen.get_size()
        self.base_y = int(self.screen_h * 0.45)
        self.spacing_y = int(self.screen_h * 0.06)

        self.load_question()
        self.run()

    def load_question(self):
        self.buttons.clear()
        self.validated = False
        q = self.questions[self.index]
        for i, ans in enumerate(q.answers_set):
            btn = AnswerButton(ans, pygame.Rect(self.screen_w * 0.1, self.base_y + i * self.spacing_y, self.screen_w * 0.8, 50))
            self.buttons.append(btn)
        qid = q.id
        selected_ids = self.selected_answers.get(qid, [])
        if selected_ids:  # если уже был ответ
            self.validated = True
            for btn in self.buttons:
                if btn.answer.id in selected_ids:
                    btn.active = True
                btn.validated = True


    def draw(self):
        screen.fill(WHITE)
        q = self.questions[self.index]

        # Вопрос — многострочный текст
        lines, text_w, text_h = render_multiline_text(q.task, FONT, BLACK, int(self.screen_w * 0.85))
        y = int(self.screen_h * 0.05)
        for line in lines:
            screen.blit(line, (self.screen_w * 0.05, y))
            y += line.get_height() + 10

        # Картинка
        if q.img_path:
            try:
                img = pygame.image.load(q.img_path)
                img_size = int(self.screen_h * 0.3)
                img = pygame.transform.scale(img, (img_size, img_size))
                screen.blit(img, (self.screen_w * 0.05, y + 10))
            except:
                err = SMALL.render("[Image not found]", True, RED)
                screen.blit(err, (self.screen_w * 0.05, y + 10))

        # Ответы
        for btn in self.buttons:
            btn.draw(screen)

        # Навигация
        nav = SMALL.render(
            f"Question {self.index + 1}/{len(self.questions)} - [{q.field.value}]", True, BLUE
        )
        screen.blit(nav, (self.screen_w * 0.05, self.screen_h - 40))

        score = SMALL.render(
            f"Correct {self.correct_count}   Wrong {self.wrong_count}", True, (100, 100, 100)
        )
        screen.blit(score, (self.screen_w * 0.75, self.screen_h - 40))

        # Результат
        if self.validated:
            qid = self.questions[self.index].id
            selected_ids = self.selected_answers.get(qid, [])
            is_correct = all(
                (btn.answer.id in selected_ids) == btn.answer.is_true
                for btn in self.buttons
            )
            result_text = "Ответ верный" if is_correct else "Ответ неверный"
            color = GREEN if is_correct else RED
            msg = FONT.render(result_text, True, color)
            y_result = self.base_y + len(self.buttons) * self.spacing_y + 20
            screen.blit(msg, (self.screen_w * 0.1, y_result))


    def handle_click(self, pos):
        if self.validated:
            return
        for btn in self.buttons:
            btn.handle_click(pos)

    def validate(self):
        self.validated = True
        qid = self.questions[self.index].id
        selected_ids = [btn.answer.id for btn in self.buttons if btn.active]
        self.selected_answers[qid] = selected_ids

        correct = all(
            (btn.active == btn.answer.is_true) for btn in self.buttons
        )
        for btn in self.buttons:
            btn.validated = True

        if correct:
            self.correct_count += 1
        else:
            self.wrong_count += 1

        self.storage.add_attempt(qid, correct)
        # self.next()


    def next(self):
        self.index = (self.index + 1) % len(self.questions)
        self.load_question()

    def prev(self):
        self.index = (self.index - 1 + len(self.questions)) % len(self.questions)
        self.load_question()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.next()
                    elif event.key == pygame.K_LEFT:
                        self.prev()
                    elif event.key == pygame.K_RETURN:
                        self.validate()

            self.draw()
            pygame.display.flip()
            clock.tick(60)

def load_questions(path: str) -> list[Question]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Question.from_dict(q) for q in (data if isinstance(data, list) else [data])]




if __name__ == '__main__':
    questions = load_questions("train_helper/data/python_questions.json")
    quiz = QuizApp(questions)