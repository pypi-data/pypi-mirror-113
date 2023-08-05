import requests


def buscar_avatar(user):
    """
    Busca o avatar de um usuario no Github
    :param user: string com nome do usuario no github
    :return: string com url do avatar
    """
    url = f'https://api.github.com/users/{user}'
    resp = requests.get(url)
    return resp.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('victorsmorais'))
