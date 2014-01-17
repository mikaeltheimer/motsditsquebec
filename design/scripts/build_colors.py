"""Build colors script
Generates the colors.less file direct from the database

@author Stephen Young
"""

from motsdits.models import Color


def run():

    header = (
        '/**',
        ' * Official Color sheet for MDQ',
        ' * NOTE: This gets autogenerated, please run:',
        ' *       python manage.py runscript build_colors',
        ' * to update the color sheet instead of editing directly',
        ' */\n'
    )

    with open('design/assets/less/includes/colors.less', 'w') as colorfile:

        def writeline(text, breaks=1):
            return colorfile.write(text + '\n' * breaks)

        for line in header:
            writeline(line)

        for color in Color.objects.all():
            writeline('@{}: #{};'.format(color.name, color.hex_code))
            if color.name != 'white':
                writeline('.%s { background: @%s; border-color: @%s; color: white; }' % (color.name, color.name, color.name))
            else:
                writeline('.%s { background: @%s; border-color: @%s; color: black; }' % (color.name, color.name, color.name))

            # Lighter version
            writeline('.%s-light { background: lighten(@%s, 10%%); border-color: lighten(@%s, 10%%); color: inherit; }' % (color.name, color.name, color.name))
            # And the text lines
            writeline('.%s-text { color: @%s; }' % (color.name, color.name), 2)
