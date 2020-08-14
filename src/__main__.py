import json
import subprocess
import os
from pathlib import Path
import re

decks = ['micro/Sketchy__Sketchy_Micro/', 'pharm/Sketchy__Sketchy_Pharm']
outdir = 'build'
p = Path('/home/default/repos/sketchy')

def build_deck(deck: str):
    with (p / deck / 'deck.json').open() as data_file:
        file_json = json.load(data_file)

    for note in file_json["notes"]:
        try: 
            tag = next(tag for tag in note['tags'] if "#Sketchy" in tag and "::" in tag)
        except:
            print("no tag")
            return
        path = p / outdir / (tag.replace("::", "/").replace(" ", "_") + '.tex')
        fields  = [field for field in note['fields'] if 'src=' in field]
        fields.insert(0, fields[-1])
        fields.pop(-1)
        images_2d = list(map(lambda field: re.findall(r'img src="([^"].*?)"', field), fields))
        images_flat = [j for sub in images_2d for j in sub] 
        main_image =  f"\includegraphics[width=\linewidth]{{{p / deck / 'media' / images_flat[0]}}}"
        images = list(map(lambda image: f"\includegraphics[width=.33\linewidth]{{{p / deck / 'media' / image}}}", images_flat))

        nl = '\n'
        output = f"""\\documentclass{{article}}
\\usepackage{{graphicx}}
% \\graphicspath{{/home/default/repos/sketchy/micro/Sketchy__Sketchy_Micro/media/}} 
\\title{{Sketchy Item}}
\\usepackage[margin=0.25in]{{geometry}}

\\begin{{document}}
\\maketitle
{main_image}
{nl.join(images[1:])}
\\end{{document}}
    """
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open(errors=None, mode='w') as outfile:
            outfile.write(output)

        print(f'Finished note {path}')

def build():
    for path in Path('build').rglob('*.tex'):
        os.chdir(path.resolve().parent)
        subprocess.run(['latexmk', path.name])
        subprocess.run(['latexmk', path.name])

    print("Cleaning files")
    globs = ['.aux', '.dvi', '.fdb_latexmk', '.fls', '.log']
    for glob in globs:
        Path('build').rglob(f'*{glob}')
        for 
        print(path.name)
    
if __name__ == "__main__":
    for deck in decks:
        build_deck(deck)
print("done")

