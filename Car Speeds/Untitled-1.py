from ursina import *
import random

app = Ursina()
camera.orthographic = True
camera.fov = 10

background_music = Audio('bg.mp3', loop=True, autoplay=True)
crash_sound = Audio('crash.mp3', loop=False, autoplay=False)

background = Entity(model='quad', texture='need', scale=(20, 10), z=2)

car = Entity(model='quad', texture='mbem', collider='box', scale=(2,1), rotation_z=-90, y=-3)
road1 = Entity(model='quad', texture='road', scale=18, z=1)
road1.original_y = road1.y  
road2 = duplicate(road1, y=15)
road2.original_y = road2.y  
pair = [road1, road2]

enemies = []

def newEnemy():
    val = random.uniform(-2,2)
    new = duplicate(car, texture='mbem1', x=2*val, y=25, color=color.random_color(), rotation_z=90 if val < 0 else -90)
    enemies.append(new)
    invoke(newEnemy, delay=1)
newEnemy()

def reset_game():
    global score
    car.x = 0
    car.y = -3
    score = 0
    for enemy in enemies:
        destroy(enemy)
    enemies.clear()
    for road in pair:
        road.y = road.original_y 

def update():
    global score, high_score
    if not menu.enabled:
        car.x -= held_keys['a'] * 5 * time.dt 
        car.x += held_keys['d'] * 5 * time.dt   
        car.y += held_keys['w'] * 5 * time.dt
        car.y -= held_keys['s'] * 5 * time.dt
        
        if car.x > 5:
            car.x = 4  
            car.shake() 
        elif car.x < -5.5:
            car.x = -5  
            car.shake() 
        
        for road in pair: 
            road.y -= 6 * time.dt
            if road.y < -15:
                road.y += 30
        for enemy in enemies:
            if enemy.x < 0:
                enemy.y -= 10 * time.dt
            else:
                enemy.y -= 5 * time.dt
            if enemy.y < -10:
                enemies.remove(enemy)
                destroy(enemy)
        
        for enemy in enemies:
            if car.intersects(enemy).hit:
                show_crash_effect(car, enemy) 
                show_restart_button()
                application.pause()
                background_music.stop()  
                crash_sound.play() 
                if score > high_score:
                    high_score = score
                    high_score_text.text = f'High Score: {int(high_score)}'

        score += time.dt
        score_text.text = f'Score: {int(score)}'

score = 0
high_score = 0
score_text = Text(text=f'Score: {score}', position=(-0.85, 0.45), scale=2)
high_score_text = Text(text=f'High Score: {high_score}', position=(0.85, 0.45), scale=1.5, origin=(1,0))

def show_crash_effect(car, enemy):
    car.shake(duration=0.5, magnitude=0.1)

def reset_car_color(car):
    car.color = color.white

def show_restart_button():
    restart_button.enabled = True
    car.disable()
    for road in pair:
        road.disable()
    for enemy in enemies:
        enemy.disable()

def restart_game():
    restart_button.enabled = False
    reset_game()
    car.enable()
    for road in pair:
        road.enable()
    for enemy in enemies:
        enemy.enable()
    application.resume()
    background_music.play()

def disable_menu():
    menu.disable()
    car.enable()
    for road in pair:
        road.enable()
    background_music.play()

menu = Entity(enabled=True)
title_text = Text(parent=menu, text='Cars Speed', origin=(0, -1), scale=50)
start_button = Button(parent=menu, text='Start', color=color.azure, scale=1, x=-0.80, y=-0.5, on_click=Func(disable_menu))
exit_button = Button(parent=menu, text='Exit', color=color.red, scale=1, x=0.80, y=-0.5, on_click=application.quit)


restart_button = Button(text='Restart', color=color.azure, scale=0.1, y=-0, enabled=False, on_click=Func(restart_game))

car.disable()
for road in pair:
    road.disable()

app.run()