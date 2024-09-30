from PIL import Image, ImageDraw, ImageOps

def handle_corn(image, size, corner_radius):
    image = image.resize(size)
    # 头像改圆角
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    # 圆角半径
    draw.rounded_rectangle([0, 0, image.size[0], image.size[1]], radius=corner_radius, fill=255)
    image = ImageOps.fit(image, size, centering=(0.5, 0.5))
    image.putalpha(mask)
    return image