import os
import sys

import pygame
import requests

def update():
    global delta, lat, api_server, lon, params, response, map_file
    api_server = "http://static-maps.yandex.ru/1.x/"

    params = {
        "ll": ",".join([str(lat), str(lon)]),
        "l": "map",
        "z": str(z)
    }
    response = requests.get(api_server, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file
api_server = "http://static-maps.yandex.ru/1.x/"

lon, lat, delta = map(float, sys.argv[1:])
z = 1
params = {
    "ll": ",".join([str(lat), str(lon)]),
    "l": "map",
    "z": str(z)
}
response = requests.get(api_server, params=params)

if not response:
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_PAGEUP]:
        z = z + 1 if z < 21 else z
        screen.blit(pygame.image.load(update()), (0, 0))
        pygame.display.flip()

    if keys[pygame.K_PAGEDOWN]:
        z = z - 1 if z > 0 else z
        update()
        screen.blit(pygame.image.load(update()), (0, 0))
        pygame.display.flip()

pygame.quit()
os.remove(map_file)