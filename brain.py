import pygame
import random
import csv
import time
from pylsl import StreamInlet, resolve_bypred
# import serial
import os

# Cambiar el directorio de trabajo al directorio del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def readCsv():
    with open('bestScores.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                data = {row[0]: [], row[1]: []}
                line_count += 1
            else:
                data["name"].insert(len(data["name"]), row[0])
                data["score"].insert(len(data["score"]), row[1])
    return data
            
def writeToCsv():
    with open('bestScores.csv', mode='w', newline="") as csv_file:
        fieldnames = ['name', 'score']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for name, score in zip(data["name"], data["score"]):
            print("score nuevo", score)
            writer.writerow({"name": name, "score": score})

class Hearts:
    def __init__(self):
        self.sprites = []
        self.lifes = 3
        for i in range(4):
            self.sprites.insert(i, Spritesheet("hearts.png", 1).get_sprite(0, 143 / 4 * i, 117, 143 / 4))

    def render(self):
        screen.blit(self.sprites[abs(self.lifes - 3)], (10, 10))

class Explosion:
    def __init__(self, x, y):
        self.sprites = []
        self.x = x
        self.y = y
        self.actualFrame = 0
        self.acc = 0
        for i in range(6):
            self.sprites.insert(i, Spritesheet("explosion.png").get_sprite(((384 * 3) / 6) * (i), 0, ((384 * 3) / 6), 64 * 3))

    def render(self):
        screen.blit(self.sprites[self.actualFrame], (self.x, self.y))

    def changeFrame(self):
        if self.actualFrame == 5:
            explosions.remove(self)
        else:
            self.actualFrame += 1

class Spritesheet:
    def __init__(self, filename, scale = 3):
        self.filename = filename
        self.scale = scale
        self.spriteSheet = pygame.image.load(self.filename).convert()
        self.spriteSheet = pygame.transform.scale(self.spriteSheet, (self.spriteSheet.get_width() * self.scale, self.spriteSheet.get_height() * self.scale))

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.spriteSheet, (0, 0), (x, y, w, h))
        return sprite

class Sprite:
    def __init__(self, img, tag):
        self.tag = tag

        self.image = pygame.image.load(img).convert()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 3, self.image.get_height() * 3))

        self.sprite = pygame.Surface((self.image.get_width(), self.image.get_height()))
        self.sprite.set_colorkey((0, 0, 0))
        self.sprite.blit(self.image, (0, 0), (0, 0, self.image.get_width(), self.image.get_height()))

        if self.tag != "beam":
            self.pos_y = random.randrange(10, screen.get_height() - self.image.get_height())
            self.pos_x = screen.get_width()
            self.speed_x = random.randrange(450, 600)
            self.speed_y = random.randrange(0, 300) * random.choice([-1, 1])
        else:
            self.pos_y = player.pos_y + player.image.get_height() / 2 - self.sprite.get_height() / 2
            self.pos_x = player.pos_x
            self.speed_x = 800
            self.speed_y = 0   
    
    def updatePos(self, dt):
        if self.tag != "beam":
            self.pos_x -= self.speed_x * dt / 3 * difficulty
            self.pos_y -= self.speed_y * dt / 3 * difficulty

            if self.pos_y <= 0:
                self.pos_y = 0
                self.speed_y *= -1
            if self.pos_y >= screen.get_height() - 10 - self.sprite.get_height():
                self.pos_y = screen.get_height() - 10 - self.sprite.get_height()
                self.speed_y *= -1
        else:
            self.pos_x += self.speed_x * dt
        

    def render(self):
        screen.blit(self.sprite, (self.pos_x, self.pos_y))

class Player:
    def __init__(self):
        self.tag = "player"

        self.score = 0

        self.alive = False

        self.hasPowerup = False

        self.image = pygame.image.load("player1.png").convert()
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 3, self.image.get_height() * 3))

        self.sprite = pygame.Surface((self.image.get_width(), self.image.get_height()))
        self.sprite.set_colorkey((0, 0, 0))
        self.sprite.blit(self.image, (0, 0), (0, 0, self.image.get_width(), self.image.get_height()))

        self.pos_x = 0 + margin
        self.pos_y = screen.get_height() / 2

def checkNewHighScore():
    for i, score in enumerate(data["score"]):
        if player.score > int(score):
            print(player.score, score)
            data["score"].insert(i, "0" * (5 - len(str(player.score))) + str(player.score))
            data["score"].pop()
            for score in data["score"]:
                print(score)
            return i
        elif player.score == int(score) and i != 2:
            data["score"].insert(i, "0" * (5 - len(str(player.score))) + str(player.score))
            return i
    return False

newName = [65, 65, 65]

def detectCollisions(sprite1, sprite2):
    w1 = sprite1.image.get_width()
    w2 = sprite2.image.get_width()
    h1 = sprite1.image.get_height()
    h2 = sprite2.image.get_height()
    x1 = sprite1.pos_x
    x2 = sprite2.pos_x
    y1 = sprite1.pos_y
    y2 = sprite2.pos_y

    if (x1 + w1 >= x2 and x1 <= x2 + w2) and (y1 + h1 >= y2 and y1 <= y2 + h2):
        if sprite2.tag == "enemy" and sprite1.tag == "player" and player.alive:
            if hearts.lifes > 0:
                hearts.lifes -= 1
            if hearts.lifes == 0:
                explosions.insert(0, Explosion(sprite1.pos_x, sprite1.pos_y))
                sprite1.alive = False
            return True
        elif sprite2.tag == "powerup" and sprite1.tag == "player" and player.alive:
            sprite1.hasPowerup = True
            return True
        elif sprite1.tag == "enemy" and sprite2.tag == "beam":
            player.score += 5
            explosions.insert(0, Explosion(sprite1.pos_x, sprite1.pos_y))
            enemies.remove(sprite1)
            beams.remove(sprite2)
    return False

pygame.init()

pygame.display.set_caption("BrainDash")

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

font = pygame.font.Font(None, 36)
fontTitle = pygame.font.Font(None, 144)

menu_options = ["Play", "HighScores", "Exit"]
selected_option = 0
selected_letter = 0

x, y, acc, beamAcc, dt, powerupTimer, animationTimer = 0, 0, 0, 0, 0, 0, 0.085
delay = 0
newHighScoreIndex = -1
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
margin = 10
hearts = Hearts()

bg = pygame.image.load("SpaceBg.png")
dashboard = False

player = Player()
arduino = False
difficultySelection = False
difficulty = 1
enemies = []
powerups = []
beams = []
explosions = []

data = readCsv()

streams = resolve_bypred('name', 'openvibeMarkers', timeout=1)

while len(streams) == 0:
    print("Conexión con OpenViBE fallida. Intentando de nuevo...")
    time.sleep(2)
    streams = resolve_bypred('name', 'openvibeMarkers', timeout=1)

print("Conexión con OpenViBE establecida :D")

# Crear un inlet para el stream de marcadores
inlet = StreamInlet(streams[0])

while running:
    #try:
    marker, timestamp = inlet.pull_sample()
    #if marker:
    #    print("Marcador de OpenViBE:", marker[0])
        #time.sleep(0.1)  # Puedes ajustar este valor para controlar la velocidad de visualización
    #except KeyboardInterrupt:
    #    print("Saliendo...")

    if not player.alive and player.score != 0 and newHighScoreIndex < 0:
        newHighScoreIndex = checkNewHighScore()

    acc += dt
    if player.hasPowerup and player.alive:
        beamAcc += dt
        powerupTimer += dt
        if beamAcc >= 0.5:
            beamAcc = 0
            beams.insert(0, Sprite("beam1.png", "beam"))
            if powerupTimer >= 3:
                powerupTimer = 0
                player.hasPowerup = False

    if acc >= delay * 3 / difficulty and player.alive:
        player.score += 1
        delay = random.randrange(1, 3)
        newEnemy = Sprite("enemy1.png", "enemy")
        enemies.insert(0, newEnemy)
        acc = 0
        if random.randrange(1, 11) == 5:
            powerups.insert(1, Sprite("ammo1.png", "powerup"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not player.alive:
            if event.key == pygame.K_UP and not dashboard:
                if newHighScoreIndex >= 0:
                    newName[selected_letter] = newName[selected_letter] == 90 and 65 or newName[selected_letter] + 1
                else:
                    selected_option = (selected_option - 1) % len(menu_options)
            elif event.key == pygame.K_DOWN and not dashboard:
                if newHighScoreIndex >= 0:
                    newName[selected_letter] = newName[selected_letter] == 65 and 90 or newName[selected_letter] - 1
                else:
                    selected_option = (selected_option + 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                if difficultySelection:
                    difficulty = selected_option + 1
                    print(difficulty)
                    if len(enemies) == 0:
                        difficultySelection = False
                        hearts.lifes = 3
                        player.alive = True
                    continue
                if dashboard:
                    dashboard = False
                    selected_option = 0
                    continue
                elif newHighScoreIndex >= 0:
                    data["name"].insert(newHighScoreIndex, "".join([chr(letter) for letter in newName]))
                    data["name"].pop()
                    writeToCsv()
                    player.score = 0
                    newHighScoreIndex = -1
                    dashboard = True
                    continue
                if selected_option == 0:
                    difficultySelection = True
                elif selected_option == 1:
                    dashboard = True
                elif selected_option == 2 and difficultySelection:
                    running = False
            elif event.key == pygame.K_LEFT and newHighScoreIndex >= 0:
                selected_letter = selected_letter == 0 and 2 or selected_letter - 1
            elif event.key == pygame.K_RIGHT and newHighScoreIndex >= 0:
                selected_letter = selected_letter != 2 and selected_letter + 1 or 0

    screen.blit(bg, (x, y))
    screen.blit(bg, (x + bg.get_width(), y))
    if player.alive:
        hearts.render()

    if len(explosions) > 0:
        for explosion in explosions:
            explosion.render()
            explosion.acc += dt
            if explosion.acc >= animationTimer:
                explosion.acc = 0
                explosion.changeFrame()

    for beam in beams:
        if beam.pos_x >= screen.get_width():
            beams.remove(beam)
        else:
            for enemy in enemies:
                detectCollisions(enemy, beam)
            beam.render()
            beam.updatePos(dt)

    if player.alive:
        screen.blit(player.sprite, (player.pos_x, player.pos_y))
        draw_text(f"Score: {player.score}", font, (255, 255, 255), screen.get_width() - 100, 20)

    for enemy in enemies:
        if detectCollisions(player, enemy) or enemy.pos_x <= -enemy.sprite.get_width():
            enemies.remove(enemy)
        else:
            enemy.render()
            enemy.updatePos(dt)

    for powerup in powerups:
        if detectCollisions(player, powerup) or powerup.pos_x <= -powerup.sprite.get_width():
            powerups.remove(powerup)
        else:
            powerup.render()
            powerup.updatePos(dt)

    # keys = pygame.key.get_pressed()
    if marker[0] == 33031:
        player.pos_y -= 250 * dt
        if player.pos_y <= 0:
            player.pos_y = 0
    else:
        player.pos_y += 250 * dt
        if player.pos_y >= screen.get_height() - player.image.get_height():
            player.pos_y = screen.get_height() - player.image.get_height()

    if x <= -bg.get_width():
        x = 0
    else:
        x -= 300 * dt
    
    if not player.alive:
        if difficultySelection:
            draw_text("Select Difficulty:", fontTitle, (255, 255, 255), screen.get_width() / 2, ((screen.get_height() / 2) + 50 - 18) / 2)
            for i, option in enumerate(["Easy1", "Easy2", "Medium", "Hard"]):
                if i == selected_option:
                    draw_text(option, font, (255, 255, 255), screen.get_width() / 2, (screen.get_height() / 2) + (i * 50) - 18)
                else:
                    draw_text(option, font, (150, 150, 150), screen.get_width() / 2, (screen.get_height() / 2) + (i * 50) - 18)
        if dashboard:
            draw_text("Name:", font, (255, 255, 255), screen.get_width() / 2 - 100, (screen.get_height() / 2) - 50 - 18)
            draw_text("Score:", font, (255, 255, 255), screen.get_width() / 2 + 100, (screen.get_height() / 2) - 50 - 18)
            for name, score, i in zip(data["name"], data["score"], enumerate(data["name"])):
                draw_text(name, font, (255, 255, 255), screen.get_width() / 2 - 100, (screen.get_height() / 2) + (i[0] * 50) - 18)
                draw_text(score, font, (255, 255, 255), screen.get_width() / 2 + 100, (screen.get_height() / 2) + (i[0] * 50) - 18)

            draw_text("Press return to exit", font, (255, 255, 255), screen.get_width() / 2, (screen.get_height() / 2) + (3 * 50) - 18)
        elif newHighScoreIndex >= 0: 
            draw_text("Congratulations! You have a new HighScore", font, (255, 255, 255), screen.get_width() / 2, ((screen.get_height() / 2) + 50 - 18) / 2)
            for name, score, i in zip(data["name"], data["score"], enumerate(newName)):
                draw_text(chr(i[1]), fontTitle, i[0] == selected_letter and (255, 255, 255) or (150, 150, 150), (screen.get_width() / 2) + (100 * (i[0] - 1)), screen.get_height() / 2)

            draw_text("Press return to exit", font, (255, 255, 255), screen.get_width() / 2, (screen.get_height() / 2) + (3 * 50) - 18)
        elif not difficultySelection:
            draw_text("Brain Dash", fontTitle, (255, 255, 255), screen.get_width() / 2, ((screen.get_height() / 2) + 50 - 18) / 2)
            for i, option in enumerate(menu_options):
                if i == selected_option:
                    draw_text(option, font, (255, 255, 255), screen.get_width() / 2, (screen.get_height() / 2) + (i * 50) - 18)
                else:
                    draw_text(option, font, (150, 150, 150), screen.get_width() / 2, (screen.get_height() / 2) + (i * 50) - 18)
    
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()