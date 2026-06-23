import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set environment variables for headless Pygame
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
pygame.init()

from game import Game
from enemy import Enemy
from settings import (
    ENEMY_TYPE_NORMAL, ENEMY_TYPE_ARMORED, ENEMY_TYPE_SPLITTER
)

# Test 1: Initialize game and verify systems load
print("Running Test 1: Initialization...")
screen = pygame.display.set_mode((1280, 720))
game = Game(screen)
assert game.state == "menu"
print("Test 1 passed!")

# Test 2: Verify normal enemy HP and defeat logic
print("Running Test 2: Normal enemy hit & defeat...")
game._start_game()
game.enemies.clear()

# Spawn normal enemy manually
normal_enemy = Enemy(text="print", speed=1.0, is_boss=False, enemy_type=ENEMY_TYPE_NORMAL)
game.enemies.append(normal_enemy)
assert normal_enemy.hp == 1

# Simulate keystrokes to type "print"
for char in "print":
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UNKNOWN, unicode=char)
    game._handle_gameplay_input(event)

# Normal enemy should be dead immediately
assert not normal_enemy.alive
# Filter dead enemies
game._update(16)
assert len(game.enemies) == 0
assert game.stats.enemies_defeated == 1
print("Test 2 passed!")

# Test 3: Verify armored enemy 2 HP logic
print("Running Test 3: Armored enemy 2 HP hit & defeat...")
game.enemies.clear()
game.stats.reset()
game.targeted_enemy = None
game.current_input = ""

armored_enemy = Enemy(text="input", speed=1.0, is_boss=False, enemy_type=ENEMY_TYPE_ARMORED)
game.enemies.append(armored_enemy)
assert armored_enemy.hp == 2

# Simulate first typing pass
for char in "input":
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UNKNOWN, unicode=char)
    game._handle_gameplay_input(event)

# Armored enemy should still be alive, but HP reduced to 1
assert armored_enemy.alive
assert armored_enemy.hp == 1
game._update(16)
assert len(game.enemies) == 1
assert game.stats.enemies_defeated == 0
assert game.stats.words_completed == 1  # counts as a word completion for score/combo

# Simulate second typing pass
for char in "input":
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UNKNOWN, unicode=char)
    game._handle_gameplay_input(event)

# Now it should be destroyed
assert not armored_enemy.alive
game._update(16)
assert len(game.enemies) == 0
assert game.stats.enemies_defeated == 1
assert game.stats.words_completed == 2
print("Test 3 passed!")

# Test 4: Verify boss enemy 3 HP logic
print("Running Test 4: Boss enemy 3 HP hit & defeat...")
game.enemies.clear()
game.stats.reset()
game.targeted_enemy = None
game.current_input = ""

boss_enemy = Enemy(text="lambda", speed=1.0, is_boss=True)
game.enemies.append(boss_enemy)
assert boss_enemy.hp == 3

# First typing pass
for char in "lambda":
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UNKNOWN, unicode=char)
    game._handle_gameplay_input(event)
assert boss_enemy.alive
assert boss_enemy.hp == 2

# Second typing pass
for char in "lambda":
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UNKNOWN, unicode=char)
    game._handle_gameplay_input(event)
assert boss_enemy.alive
assert boss_enemy.hp == 1

# Third typing pass
for char in "lambda":
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UNKNOWN, unicode=char)
    game._handle_gameplay_input(event)
assert not boss_enemy.alive
game._update(16)
assert len(game.enemies) == 0
assert game.stats.boss_kills == 1
print("Test 4 passed!")

# Test 5: Verify splitter enemy speed scaling and split logic
print("Running Test 5: Splitter enemy split logic & speed scaling...")
game.enemies.clear()
game.targeted_enemy = None
game.current_input = ""
game.wave_number = 3

splitter_enemy = Enemy(text="split", speed=1.0, is_boss=False, enemy_type=ENEMY_TYPE_SPLITTER)
game.enemies.append(splitter_enemy)

# Defeat the splitter
for char in "split":
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UNKNOWN, unicode=char)
    game._handle_gameplay_input(event)

# It should be dead, and 2 normal children should have spawned
assert not splitter_enemy.alive
game._update(16)
assert len(game.enemies) == 2

# Check their speed to ensure wave scaling is applied
from settings import WAVE_SPEED_SCALE
base_speed = game.difficulty_config["enemy_speed"]
expected_child_speed = base_speed * 1.2 * (1.0 + (game.wave_number - 1) * WAVE_SPEED_SCALE)
for child in game.enemies:
    assert child.enemy_type == ENEMY_TYPE_NORMAL
    assert abs(child.speed - expected_child_speed) < 0.001
print("Test 5 passed!")

# Test 6: Wave completion check
print("Running Test 6: Wave completion logic...")
game.enemies.clear()
game.targeted_enemy = None
game.current_input = ""
game.wave_enemies_total = 2
game.enemies_spawned = 2
game.wave_active = True

# Spawn one enemy
normal_enemy = Enemy(text="a", speed=1.0)
game.enemies.append(normal_enemy)

# When active and enemies present, wave shouldn't be complete
game._update(16)
assert game.wave_active

# Defeat the enemy
for char in "a":
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UNKNOWN, unicode=char)
    game._handle_gameplay_input(event)

# First update filters it out
game._update(16)
# Second update triggers wave completion check when len(enemies) is 0
game._update(16)

assert not game.wave_active
assert game.wave_rest_timer > 0
print("Test 6 passed!")

# Test 7: Verify Focus Flow charging, penalty, double scoring, and chain lightning
print("Running Test 7: Focus Flow mechanics...")
game.enemies.clear()
game.stats.reset()
game.targeted_enemy = None
game.current_input = ""

# Initial state
assert game.stats.focus_charge == 0.0
assert not game.stats.focus_active

# 1. Test charging: type some correct characters
enemy1 = Enemy(text="hello", speed=1.0)
game.enemies.append(enemy1)

event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UNKNOWN, unicode="h")
game._handle_gameplay_input(event)
# Each correct character increases focus by 1.5%
assert game.stats.focus_charge == 1.5

# 2. Test typo penalty: type wrong character
event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UNKNOWN, unicode="x")
game._handle_gameplay_input(event)
# Typo reduces focus by 10.0%, floor at 0.0
assert game.stats.focus_charge == 0.0

# 3. Test Focus Activation (type 67 correct chars to reach 100%)
# Let's set charge to 99.0% manually to easily test activation
game.stats.focus_charge = 99.0
event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UNKNOWN, unicode="e")
game._handle_gameplay_input(event)
assert game.stats.focus_charge == 100.0
assert game.stats.focus_active
assert game.stats.focus_timer == 6000.0

# 4. Test Double Score under Focus Flow
# Defeat enemy1 to verify doubled scoring
for char in "llo":
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UNKNOWN, unicode=char)
    game._handle_gameplay_input(event)

# Since we finished the word "hello" (length 5) in Focus Flow:
# Base character score: 5 * 10 = 50
# Word bonus: 50
# Total raw score = 100
# Multiplier is x1. Focus doubles the score, so final score should be 100 * 2 = 200!
game._update(16)
assert game.stats.score == 200

# 5. Test Chain Lightning
# With Focus active, completing a word should damage/defeat another enemy on screen.
game.enemies.clear()
enemy2 = Enemy(text="a", speed=1.0)
enemy3 = Enemy(text="b", speed=1.0) # This will be the chain target
game.enemies.append(enemy2)
game.enemies.append(enemy3)

# Reset targeting
game.targeted_enemy = None
game.current_input = ""

# Type "a" to defeat enemy2
event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UNKNOWN, unicode="a")
game._handle_gameplay_input(event)

# This should trigger chain lightning on enemy3 and defeat it too!
assert not enemy2.alive
assert not enemy3.alive # both should be defeated by the chain
game._update(16) # filter them
game._update(16)
assert len(game.enemies) == 0

print("Test 7 passed!")

print("All tests completed successfully!")
