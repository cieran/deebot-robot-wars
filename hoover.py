import json
import os
import pygame
from sucks import *

config = {
    'device_id': EcoVacsAPI.md5(str(time.time())),
    'email': 'your_email',
    'password_hash': EcoVacsAPI.md5('your_pwd'),
    'country': 'xx',
    'continent': 'xx'
}

api = EcoVacsAPI(
    config['device_id'],
    config['email'],
    config['password_hash'],
    config['country'],
    config['continent']
)

vacs = api.devices()
my_vac = vacs[0]

vacbot = VacBot(
    api.uid,
    api.REALM,
    api.resource,
    api.user_access_token,
    my_vac,
    config['continent']
)

vacbot.connect_and_wait_until_ready()

with open(os.path.join("ps4_keys.json"), 'r+') as file:
    button_keys = json.load(file)

pygame.init()
controller = pygame.joystick.Joystick(0)
controller.init()

# directional arrow mapping proved difficult so i settled for:
# R2 - forward
# L2 - turnaround
# R1 - right
# L1 - left

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONUP:
            if event.button == button_keys['square']:
                vacbot.run(PlaySound())
            if event.button == button_keys['x']:
                vacbot.run(Clean())
            if event.button == button_keys['circle']:
                vacbot.run(Stop())
            if event.button == button_keys['triangle']:
                vacbot.run(Charge())
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == button_keys['up_arrow']:
                vacbot.run(Move('forward'))
            if event.button == button_keys['down_arrow']:
                vacbot.run(Move('turn_around'))
            if event.button == button_keys['left_arrow']:
                vacbot.run(Move('left'))
            if event.button == button_keys['right_arrow']:
                vacbot.run(Move('right'))
