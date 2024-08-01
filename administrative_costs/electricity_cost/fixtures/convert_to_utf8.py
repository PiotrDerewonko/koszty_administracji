import codecs
import os


def convert_to_utf8():
    filename = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     f'energymeters.json'))
    filename_output = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     f'energymeters_utf8.json'))
    with codecs.open(filename, 'r', 'iso-8859-1') as f:
        content = f.read()

    with codecs.open(filename_output, 'w', 'utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    convert_to_utf8()
