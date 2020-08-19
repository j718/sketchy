import json
import string
import subprocess
import os
from pathlib import Path
import re

FNULL = open(os.devnull, 'w')

decks = ['']

outdir = 'build'
p = Path('/home/kde/repos/sketchy')

def build_deck(deck: str):
    with (p / deck / 'deck.json').open() as data_file:
        file_json = json.load(data_file)

    for note in file_json["notes"]:
        try: 
            tag = next(tag for tag in note['tags'] if "#" in tag and "::" in tag)
        except:
            print("no tag")
            return
        path = p / outdir / (tag.replace("::", "/").replace(" ", "_").replace("&","and") + '.tex')
        fields  = [field for field in note['fields'] if 'src=' in field]
        fields.insert(0, fields[-1])
        fields.pop(-1)
        images_2d = list(map(lambda field: re.findall(r'img src="([^"].*?)"', field), fields))
        images_flat = [j for sub in images_2d for j in sub if '%' not in j and '.gif' not in j] 
        images_flat.insert(0, images_flat[1])
        images_flat.pop(2)
        printable = set(string.printable)
        # images_flat = list(map(lambda word: ''.join([x for x in word if x in printable]), images_flat))

        main_image =  f"\includegraphics[width=\linewidth]{{{p / deck / 'media' / images_flat[0]}}}"
        images = list(map(lambda image: f"\includegraphics[width=.33\linewidth]{{{p / deck / 'media' / image}}}", images_flat))

        nl = '\n'
        output = f"""\\documentclass{{article}}
\\usepackage{{graphicx}}
\\title{{Card Item}}
\\usepackage[margin=0.25in]{{geometry}}

\\begin{{document}}
\\section{{{re.sub(r'[-_!@#$%^&*αβγ]', '', path.name)}}}
{main_image}
{nl.join(images[1:])}
\\end{{document}}
    """
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open(errors=None, mode='w') as outfile:
            outfile.write(output)

        print(f'Finished note {path}')

def delete():
    subprocess.run(["rm", "-rf", "build"])

def build():
    for path in (p / 'build').rglob('*.tex'):
        os.chdir(path.resolve().parent)
        print(f"Building {path.name}")
        subprocess.run(['pdflatex', path.name, '-interaction=nonstopmode'])
        globs = map(lambda x: f"{path.name[:-4]}{x}",['.aux', '.dvi', '.fdb_latexmk', '.fls', '.log', '.tex'])
        for glob in globs:
            for path in (path.resolve().parent).rglob(f'*{glob}'):
                path.unlink()
    
def optimize():
    globs = ['.pdf']
    for glob in globs:
        for path in (p / 'build').rglob(f'*{glob}'):
        # path =  next((p / 'build').rglob(f'*{glob}'))
            print(path)
            os.chdir(path.resolve().parent)
            subprocess.run(['gs' ,'-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4', '-dPDFSETTINGS=/ebook', '-dNOPAUSE', '-dQUIET', '-dBATCH', '-sOutputFile=small.pdf', path.name])
            path.unlink()
            (path.resolve().parent / 'small.pdf').rename(path.resolve())

if __name__ == "__main__":
    delete()
    for deck in decks:
        build_deck(deck)
    build()
    optimize()
print("done")

