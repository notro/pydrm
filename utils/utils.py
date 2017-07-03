def draw_smpte_rects(draw, x, y, width, height, colors):
    for i in range(len(colors)):
        draw.rectangle([(x + (width * i), y), (x + (width * (i + 1)), y + height)], fill=colors[i], outline=colors[i])

def draw_smpte_pattern(draw):
    fb_width, fb_height = draw.im.size

    # top colors: grey/silver, yellow, cyan, green, magenta, red, blue
    y = 0
    width = fb_width / 7
    height = fb_height * 6 / 9
    draw_smpte_rects(draw, 0, 0, width, height, ['#c0c0c0', '#c0c000', '#00c0c0', '#00c000', '#c000c0', '#c00000', '#0000c0'])

    # middle colors: blue, black magenta, black, cyan, black, grey
    y = height
    width = fb_width / 7
    height = fb_height * 1 / 9
    draw_smpte_rects(draw, 0, y, width, height, ['#0000c0', '#131313', '#c000c0', '#131313', '#00c0c0', '#131313', '#c0c0c0'])

    # bottom colors: in-phase, super white, quadrature, black, 3.5%, 7.5%, 11.5%, black
    y += height
    width = fb_width / 6
    height = fb_height * 2 / 9
    draw_smpte_rects(draw, 0, y, width, height, ['#00214c', '#ffffff', '#32006a', '#131313'])

    x = width * 4
    width = fb_width / 6 / 3
    draw_smpte_rects(draw, x, y, width, height, ['#090909', '#131313', '#1d1d1d'])

    x = fb_width * 5 / 6
    width = fb_width / 6
    draw_smpte_rects(draw, x, y, width, height, ['#131313'])

def draw_mono_pattern(draw):
    fb_width, fb_height = draw.im.size
    c = 'white'
    draw.rectangle([(0, 0), (fb_width - 1, fb_height - 1)], fill=None, outline=c)
    draw.line([(0, 0), (fb_width - 1, fb_height - 1)], fill=c)
    draw.line([(fb_width - 1, 0), (0, fb_height - 1)], fill=c)
    draw.ellipse([(fb_width*1/4, fb_height*1/4), (fb_width*3/4, fb_height*3/4)], fill=None, outline=c)
