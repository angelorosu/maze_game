import random
import pygame
import sys
from maze_generator1 import MazeGenerator

class MazeLevel:
    def __init__(self, width, height, walls, end_rect):
        self.width = width
        self.height = height
        self.walls = walls
        self.end_rect = end_rect

class MazeLevelGenerator:
    def __init__(self, width, height, wall_size):
        self.maze_generator = MazeGenerator(width, height, wall_size)

    def create_level(self):
        self.maze_generator.generate_maze()
        return self.maze_generator.get_maze_layout()

class MazeGame:
    def __init__(self):
        pygame.init()
        
        self.death_count = 0
        self.font = pygame.font.Font(None, 36)
        self.current_level = 0  
        self.levels = []

        self.width, self.height = 150, 150
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Game")
        self.clock = pygame.time.Clock()
        self.running = True

        self.level_generator = MazeLevelGenerator(self.width // 20, self.height // 20, 10)
        self.current_level_layout = self.level_generator.create_level()

        self.create_levels()

        self.player = pygame.Rect(0, 0, 10, 10)

    def create_levels(self):
        wall_size = 0
        level_walls = []
        for y, row in enumerate(self.current_level_layout):
            for x, cell in enumerate(row):
                if cell == 1:
                    level_walls.append(pygame.Rect(x * 20, y * 20, 20, 20))

        level_end_rect = pygame.Rect(random.randint(0, self.width - 30), random.randint(0, self.height - 30), 30, 30)

        level = MazeLevel(self.width, self.height, level_walls, level_end_rect)
        self.levels.append(level)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def switch_level(self):
        self.current_level += 1

        if self.current_level < len(self.levels):
            self.death_count = 0

        # Generate a new level layout
            self.current_level_layout = self.level_generator.create_level()

        # Find an empty space in the maze for the player
            empty_spaces = [
                (x, y) for y, row in enumerate(self.current_level_layout)
                for x, cell in enumerate(row) if cell == 0
        ]

            if empty_spaces:
                player_start = random.choice(empty_spaces)
                self.player.x, self.player.y = player_start[0] * 20, player_start[1] * 20
            else:
                print("Error: No empty space found in the maze!")

        # Create a new MazeLevel object for the current level
            self.create_levels()

        else:
            print(f"Game completed! Current level: {self.current_level}, Number of levels: {len(self.levels)}")
            self.running = False




    def run(self):
        while self.running:
            self.handle_events()

            keys = pygame.key.get_pressed()
            self.handle_player_movement(keys)

            self.screen.fill((255, 255, 255))
            self.draw_level()
            self.draw_death_count()

            pygame.display.flip()
            self.clock.tick(30)

            if self.check_collision(0, 0):
                print("Collision with wall detected! Player can't move.")
                self.player.x, self.player.y = 0, 0
                self.death_count += 1

            elif self.current_level < len(self.levels) and self.player.colliderect(self.levels[self.current_level].end_rect):
                self.death_count = 0
                print(f"Level {self.current_level + 1} completed!")
                self.switch_level()

            elif self.current_level == len(self.levels):
                print("Game completed! Generating new levels...")
                self.current_level_layout = self.level_generator.create_level()
                self.create_levels()
                self.player.x, self.player.y = 0, 0  # Reset player position for the new level

        pygame.quit()
        sys.exit()

    def handle_player_movement(self, keys):
        if keys[pygame.K_LEFT] and not self.check_collision(-5, 0):
            self.player.x -= 5
        if keys[pygame.K_RIGHT] and not self.check_collision(5, 0):
            self.player.x += 5
        if keys[pygame.K_UP] and not self.check_collision(0, -5):
            self.player.y -= 5
        if keys[pygame.K_DOWN] and not self.check_collision(0, 5):
            self.player.y += 5

    def check_collision(self, dx, dy):
        temp_rect = self.player.copy()
        temp_rect.x += dx
        temp_rect.y += dy

        for wall in self.levels[self.current_level].walls:
            if temp_rect.colliderect(wall):
                return True
        return False

    def draw_level(self):
        if self.current_level < len(self.levels):
            pygame.draw.rect(self.screen, (0, 0, 255), self.levels[self.current_level].end_rect)

            for wall in self.levels[self.current_level].walls:
                pygame.draw.rect(self.screen, (0, 0, 0), wall)

            pygame.draw.rect(self.screen, (255, 0, 0), self.player)

    def draw_death_count(self):
        death_text = self.font.render(f"Deaths: {self.death_count}", True, (0, 0, 0))
        background_rect = pygame.Rect(10, 10, death_text.get_width() + 10, death_text.get_height() + 10)
        pygame.draw.rect(self.screen, (255, 255,255), background_rect)

        # Draw the death count text on the white background
        self.screen.blit(death_text, (15, 15))

if __name__ == "__main__":
    game = MazeGame()
    game.run()
