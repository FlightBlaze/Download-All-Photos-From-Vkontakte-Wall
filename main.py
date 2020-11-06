# Загрузить все фото со стены профиля или сообщества

import vk_api
import requests
import shutil
import math
import os

if __name__ == '__main__':
    # Интерактивная авторизация
    print("Phone number or e-mail address:")
    login = input()
    print("Password:")
    password = input()

    # ID профиля или сообщества
    # Уберите id в начале или замените club на -
    owner = '-116082295'

    # Имя папки с загрузками
    downloads = 'Downloads'
    if not os.path.isdir(downloads):
        os.mkdir(downloads)

    session = vk_api.VkApi(login, password, scope=vk_api.VkUserPermissions.GROUPS)
    session.auth()
    vk = session.get_api()
    posts = vk.wall.get(owner_id=owner, count=1)
    count = posts.get('count')
    step = 16
    steps = math.ceil(count / 16)

    for p in range(steps):
        offset = p * step
        remaining = count - offset
        posts = vk.wall.get(owner_id=owner, count=step, offset=offset)
        print("{} posts remaining".format(remaining))
        for i in posts.get('items'):
            attachments = i.get('attachments')
            if attachments is None:
                continue
            for a in attachments:
                if a.get('type') != 'photo':
                    continue
                sizes = a.get('photo').get('sizes')
                url = sizes[-1].get('url')
                result = requests.get(url, stream=True)
                result.raw.decode_content = True
                filename = url.split("/")[-1].split("?")[0]
                localpath = "{}/{}".format(downloads, filename)
                with open(localpath, 'wb') as file:
                    shutil.copyfileobj(result.raw, file)
    print("Done!")
