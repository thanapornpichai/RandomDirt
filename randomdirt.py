import pygame
import random
import time

# -----------------------------------------------------------------------
#  Begin
# -----------------------------------------------------------------------
pygame.init()

# Load assets
BG_sprite = pygame.image.load("./assets/minecraftBG.png")
dirt0_sprite = pygame.image.load("./assets/dirt0.png")
dirt1_sprite = pygame.image.load("./assets/dirt1.png")
dirt2_sprite = pygame.image.load("./assets/dirt2.png")
dirt3_sprite = pygame.image.load("./assets/dirt3.png")
silver_sprite = pygame.image.load("./assets/silver.png")
gold_sprite = pygame.image.load("./assets/gold.png")
diamond_sprite = pygame.image.load("./assets/diamond.png")

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BLOCK_SIZE = 100
WHITE = (255, 255, 255)
RESPAWN_DELAY = 1

mineral_list = ['silver', 'gold', 'diamond']
mineral_rates = {
    "silver": 50,
    "gold": 30,
    "diamond": 10
}

# -----------------------------------------------------------------------
#  Block Class
# -----------------------------------------------------------------------
class Block:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.exists = True
        self.time_of_destruction = None
        self.click_count = 0
        self.sprites = [dirt0_sprite, dirt1_sprite, dirt2_sprite, dirt3_sprite]
        self.current_sprite = 0

    def draw(self, screen):
        if self.exists:
            sprite = pygame.transform.scale(self.sprites[self.current_sprite], (self.size, self.size))
            screen.blit(sprite, (self.x, self.y))

    def destroy(self):
        self.exists = False
        self.time_of_destruction = time.time()

    def respawn(self):
        if not self.exists and self.time_of_destruction:
            elapsed_time = time.time() - self.time_of_destruction
            if elapsed_time >= RESPAWN_DELAY:
                self.exists = True
                self.current_sprite = 0
                self.click_count = 0
                self.time_of_destruction = None

    def update_sprite(self):
        self.current_sprite = min(self.click_count, 3)


# -----------------------------------------------------------------------
#  Miner Class
# -----------------------------------------------------------------------
class Miner:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dirt Block Miner")
        self.font = pygame.font.Font(None, 36)

        self.block = Block((SCREEN_WIDTH - BLOCK_SIZE) // 2, (SCREEN_HEIGHT - BLOCK_SIZE) // 2, BLOCK_SIZE)
        self.fail_streak = 0
        self.minerals_collected = {"gold": 0, "silver": 0, "diamond": 0}
        self.running = True

    def run(self):
        while self.running:
            self.screen.fill(WHITE)
            
            self.screen.blit(BG_sprite, (0, 0))
            
            self.block.draw(self.screen)
            
            self.display_collected_minerals()

            self.handle_events()
            self.block.respawn()

            pygame.display.flip()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.block.exists:
                self.handle_click(event.pos)

    def handle_click(self, mouse_pos):
        if self.is_block_clicked(mouse_pos):
            self.block.click_count += 1
            self.block.update_sprite()

            if self.block.click_count % 4 == 0:
                self.collect_mineral()
            else:
                if self.progressive_random():
                    if self.fixed_limit_random():
                        self.collect_mineral()
                    elif self.predetermination_random(target_round=5):
                        self.collect_mineral()
                    else:
                        self.fail_streak += 1
                else:
                    self.fail_streak += 1

    def is_block_clicked(self, pos):
        return self.block.x <= pos[0] <= self.block.x + self.block.size and self.block.y <= pos[1] <= self.block.y + self.block.size

    def collect_mineral(self):
        mineral = self.marblebag_random()
        self.minerals_collected[mineral] += 1
        self.block.destroy()

    def display_collected_minerals(self):
        icon_size = 30
        x_offset = 20
        y_offset = 20
        spacing = 50

        silver_icon = pygame.transform.scale(silver_sprite, (icon_size, icon_size))
        self.screen.blit(silver_icon, (x_offset, y_offset))
        silver_text = self.font.render(f"{self.minerals_collected['silver']}", True, (0, 0, 0))
        self.screen.blit(silver_text, (x_offset + icon_size + 10, y_offset))

        gold_icon = pygame.transform.scale(gold_sprite, (icon_size, icon_size))
        self.screen.blit(gold_icon, (x_offset, y_offset + spacing))
        gold_text = self.font.render(f"{self.minerals_collected['gold']}", True, (0, 0, 0))
        self.screen.blit(gold_text, (x_offset + icon_size + 10, y_offset + spacing))

        diamond_icon = pygame.transform.scale(diamond_sprite, (icon_size, icon_size))
        self.screen.blit(diamond_icon, (x_offset, y_offset + 2 * spacing))
        diamond_text = self.font.render(f"{self.minerals_collected['diamond']}", True, (0, 0, 0))
        self.screen.blit(diamond_text, (x_offset + icon_size + 10, y_offset + 2 * spacing))

    def marblebag_random(self):
        mineral_weights = [mineral_rates['silver'], mineral_rates['gold'], mineral_rates['diamond']]
        return random.choices(mineral_list, weights=mineral_weights, k=1)[0]

    def progressive_random(self):
        if self.fail_streak == 3:
            self.fail_streak = 0
            return True
        return random.random() < 0.5

    def fixed_limit_random(self):
        return random.random() < 0.3

    def predetermination_random(self, target_round=4):
        return self.block.click_count % target_round == 0


if __name__ == "__main__":
    game = Miner()
    game.run()
