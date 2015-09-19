from PIL import Image, ImageDraw, ImageFont, ImageOps

from Tasky import settings
from user_account.models import Achievement


def generate_achieve_on_image(image, achievements, name, pos):
    ach = Achievement.objects.get(name=name)
    try:
        picture = Image.open(settings.BASE_DIR + ach.imageUrl)
        picture.thumbnail((100, 100))
    except Exception as e:
        print(6, e)
        return image

    try:
        if not achievements.filter(achievement=ach).exists():
            picture = ImageOps.colorize(ImageOps.grayscale(picture), (0, 0, 0), (50, 50, 50))
        image.paste(picture, pos)
    except Exception as e:
        print(7, e)

def generate_picture_from_user_info(username, statistics, achievements):
    image = Image.new("RGB", (450, 470), color=(180, 180, 180))
    try:
        draw = ImageDraw.Draw(image)
        color = (94, 73, 15)
        username = ((10, 10), username)
        stats = [
            ((10, 50), "Создано задач: {}".format(statistics['task_count'])),
            ((10, 70), "Решено задач: {}".format(statistics['solved_task_count'])),
            ((10, 90), "Процент правильных ответов: {}%".format(statistics['percentage'])),
            ((10, 110), "Рейтинг: {}".format(statistics['rating'])), ]
    except Exception as e:
        print(1, e)
        return image

    try:
        header_font_size, statistic_font_size = 30, 15
        # header_font = ImageFont.truetype("arial.ttf", header_font_size)
        # statistic_font = ImageFont.truetype("arial.ttf", statistic_font_size)
    except Exception as e:
        print(2, e)
        return image

    try:
        draw.text(username[0], username[1], fill=color)
        for stat in stats:
            draw.text(stat[0], stat[1], fill=color)
    except Exception as e:
        print(3, e)
        return image

    try:
        ach_first = Achievement.objects.get(name='First')
        first = Image.open(settings.BASE_DIR + ach_first.imageUrl)
        first.thumbnail((100, 100))
        if achievements.filter(achievement=ach_first).exists():
            image.paste(first, (340, 30))
            draw.text((430, 110), str(achievements.get(achievement=ach_first).count),
                      fill=(255, 0, 0))
        else:
            com = ImageOps.colorize(ImageOps.grayscale(first), (0, 0, 0), (50, 50, 50))
            image.paste(com, (340, 30))
        pictures_and_positions = (('Creator1', (10, 140)), ('Creator2', (120, 140)),
                                  ('Creator3', (230, 140)), ('Creator4', (340, 140)),
                                  ('Solver1', (10, 250)), ('Solver2', (120, 250)),
                                  ('Solver3', (230, 250)), ('Solver4', (340, 250)),
                                  ('Commentator1', (10, 360)), ('Commentator2', (120, 360)),
                                  ('Commentator3', (230, 360)), ('Commentator4', (340, 360)),)

    except Exception as e:
        print(4, e)
        return image

    try:
        for pp in pictures_and_positions:
            generate_achieve_on_image(image, achievements, pp[0], pp[1])
        return image
    except Exception as e:
        print(5, e)
        return image

