import pygame
from varname.helpers import debug
import random
from game.game_settings import *
from game.bullet import Bullet

class PlayerKapibara(pygame.sprite.Sprite):
    def __init__(self, img_path, player_x, player_y):
        super().__init__()
        self.original_image = pygame.image.load(img_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50, 100))
        self.image = self.original_image
        self.flipped_image = pygame.transform.flip(self.original_image, flip_x=True, flip_y=False)
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y - self.rect.height
        self.hp = player_hp
        self.world_position = pygame.math.Vector2(player_x, player_y)

        self.jump_power = player_jump_power
        self.direction = pygame.math.Vector2(0,0)
        self.velocity = pygame.math.Vector2(0, 0) 
        self.last_direction = pygame.math.Vector2(1,0)  #default right
        self.bullet_timer = weapon_timer
        self.is_facing_right = True
        self.on_ground = False
        print('player created')

    def global_center(self):
        return self.world_position + pygame.math.Vector2(self.rect.width // 2, self.rect.height // 2)

    def jump(self):
        if self.on_ground:
            self.velocity.y = player_jump_power
            self.on_ground = False

    def shoot(self, dt, bullets_group, camera_offset):
        self.bullet_timer -= dt
        if self.bullet_timer <= 0:
            player_center = self.world_position + pygame.math.Vector2(self.rect.width // 2, self.rect.height // 2)
            mouse_position = camera_offset + pygame.math.Vector2(pygame.mouse.get_pos())
            print(mouse_position, player_center, self.world_position)
            shoot_direction = (mouse_position - player_center).normalize()
            print(shoot_direction)
            bullets_group.add(
                Bullet(
                    img_path=bullet_img_path,
                    position=player_center,
                    direction=shoot_direction
                )
            )
            self.bullet_timer = weapon_timer

        

    def update(self, dt, bullets_group, walls_group, camera_offset):
        keys = pygame.key.get_pressed()
        movement = pygame.math.Vector2(0, 0)

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            movement.x -= 1
            self.flip_image(is_facing_left=True)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            movement.x += 1
            self.flip_image(is_facing_left=False)
        if keys[pygame.K_SPACE]:
            self.jump()
        if keys[pygame.K_RETURN]:
            self.shoot(dt, bullets_group, camera_offset)

        if movement.length() > 0:
            movement = movement.normalize()

       # Horizontal movement
        self.world_position.x += movement.x * player_speed * dt
        self.rect.topleft = self.world_position
        collided_object = pygame.sprite.spritecollideany(self, walls_group)
        if collided_object:
            if movement.x > 0:  # Moving right
                self.world_position.x = collided_object.rect.left - self.rect.width
            elif movement.x < 0:  # Moving left
                self.world_position.x = collided_object.rect.right
            self.rect.topleft = self.world_position

        # Gravity / Vertical movement
        self.velocity.y += gravity
        self.world_position.y += self.velocity.y
        self.rect.topleft = self.world_position
        collided_object = pygame.sprite.spritecollideany(self, walls_group)
        if collided_object:
            if self.velocity.y > 0:  # Falling down
                self.on_ground = True
                self.world_position.y = collided_object.rect.top - self.rect.height
                self.velocity.y = 0
            elif self.velocity.y < 0:  # Jumping up
                self.world_position.y = collided_object.rect.bottom
                self.velocity.y = 0
        else:
            self.on_ground = False  # If no collision, the player is in the air

        self.rect.topleft = self.world_position  # Sync rect to world position

        # print(movement)

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            self.shoot(dt, bullets_group, camera_offset)

    def draw(self, screen, camera_offset):
        screen_position = self.world_position - camera_offset
        screen.blit(self.image, (int(screen_position.x), int(screen_position.y)))

    def draw_hp(self, screen, camera_offset):
        """Draw the player's HP above their head."""
        hp_position = self.world_position - camera_offset
        hp_position.y -= int(self.rect.height * 3 / 4)
        text_generator = pygame.font.SysFont('Comic Sans MS', size=20)
        text = text_generator.render(f'{self.hp}', 1, (0, 225, 0))
        screen.blit(text, dest=hp_position)

    def flip_image(self, is_facing_left ):
        if is_facing_left and self.is_facing_right:
            self.image = self.flipped_image
            self.is_facing_right = False
        elif not is_facing_left and not self.is_facing_right:
            self.image = self.original_image
            self.is_facing_right = True     
