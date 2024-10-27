import pygame
import sys
import random

# Configuración general
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
ROWS, COLS = 20, 10

# Colores y piezas de Tetromino
COLORS = [
    (0, 255, 255),  # Cyan (I)
    (255, 165, 0),  # Orange (L)
    (255, 0, 0),    # Red (J)
    (0, 255, 0),    # Green (O)
    (255, 255, 0),  # Yellow (S)
    (128, 0, 128),  # Purple (T)
    (0, 0, 255)     # Blue (Z)
]
TETROMINOS = [
    [[1, 1, 1, 1]],  # I
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]]   # Z
]

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.color = COLORS[TETROMINOS.index(shape)]
    
    def rotate(self):
        self.shape = [list(row)[::-1] for row in zip(*self.shape)]

    def draw(self, surface, offset):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col] == 1:
                    pygame.draw.rect(surface, self.color, ((offset[0] + col) * GRID_SIZE, (offset[1] + row) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Tablero:
    def __init__(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    def draw(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col] > 0:
                    pygame.draw.rect(surface, COLORS[self.grid[row][col] - 1], (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def add_tetromino(self, tetromino, offset):
        for row in range(len(tetromino.shape)):
            for col in range(len(tetromino.shape[row])):
                if tetromino.shape[row][col] == 1:
                    self.grid[offset[1] + row][offset[0] + col] = COLORS.index(tetromino.color) + 1

    def check_collision(self, tetromino, offset):
        for row in range(len(tetromino.shape)):
            for col in range(len(tetromino.shape[row])):
                if tetromino.shape[row][col] == 1:
                    x, y = offset[0] + col, offset[1] + row
                    if x < 0 or x >= COLS or y >= ROWS or (y >= 0 and self.grid[y][x] > 0):
                        return True
        return False

    def clear_complete_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        lines_cleared = ROWS - len(new_grid)
        new_grid = [[0 for _ in range(COLS)] for _ in range(lines_cleared)] + new_grid
        self.grid = new_grid
        return lines_cleared

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")

    tablero = Tablero()
    tetromino = Tetromino(random.choice(TETROMINOS))
    tetromino_position = [3, 0]
    score, level, lines_cleared_total = 0, 1, 0
    base_speed, fall_speed = 500, 500
    last_fall_time = pygame.time.get_ticks()

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_pos = [tetromino_position[0] - 1, tetromino_position[1]]
                    if not tablero.check_collision(tetromino, new_pos):
                        tetromino_position = new_pos
                elif event.key == pygame.K_RIGHT:
                    new_pos = [tetromino_position[0] + 1, tetromino_position[1]]
                    if not tablero.check_collision(tetromino, new_pos):
                        tetromino_position = new_pos
                elif event.key == pygame.K_DOWN:
                    new_pos = [tetromino_position[0], tetromino_position[1] + 1]
                    if not tablero.check_collision(tetromino, new_pos):
                        tetromino_position = new_pos
                elif event.key == pygame.K_UP:
                    tetromino.rotate()
                    if tablero.check_collision(tetromino, tetromino_position):
                        tetromino.rotate()  # Revertir rotación si hay colisión

        # Caída automática del Tetromino
        current_time = pygame.time.get_ticks()
        if current_time - last_fall_time > fall_speed:
            new_pos = [tetromino_position[0], tetromino_position[1] + 1]
            if not tablero.check_collision(tetromino, new_pos):
                tetromino_position = new_pos
            else:
                tablero.add_tetromino(tetromino, tetromino_position)
                cleared_lines = tablero.clear_complete_lines()
                lines_cleared_total += cleared_lines
                score += cleared_lines * 100
                if lines_cleared_total >= level * 10:
                    level += 1
                    fall_speed = max(base_speed - (level - 1) * 50, 100)
                tetromino = Tetromino(random.choice(TETROMINOS))
                tetromino_position = [3, 0]
                if tablero.check_collision(tetromino, tetromino_position):  # Game Over
                    print("Game Over")
                    pygame.quit()
                    sys.exit()
            last_fall_time = pygame.time.get_ticks()

        # Dibuja el tablero y el Tetromino actual
        tablero.draw(screen)
        tetromino.draw(screen, tetromino_position)
        
        # Mostrar puntuación y nivel
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Puntuación: {score}", True, (255, 255, 255))
        level_text = font.render(f"Nivel: {level}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))

        pygame.display.flip()

if __name__ == "__main__":
    main()
