# Currently building

import re

class MarkdownParser:
    escaper = '\\'
    result = ''
    special_chars = ['#']
    
    def __init__(self, md):
        self.md = md
        print('aaaa')
        print(self.escaper)
        self.mainn(md)
        
        # if '\n' in md:
        #     print('aaaminirjirg')
        
        # https://www.markdownguide.org/cheat-sheet/
        # https://www.dataquest.io/blog/regex-cheatsheet/
        
        
       # ^#{1,6} .+$|\*{2}.+\*{2}|^- .+$|    |^.+$
    def mainn(self, md):
        # Titulos | negritas | listas desordenadas | Links
        # \*{2}.+\*{2}|    |\[.+?\]\(.+?\)
        
        # Hay problemas con detectar por ejemplo negrita o links si estan dentro de un heading
        # Falta capturar el texto normal
        pattern = re.compile(r'^#{1,6} .+$|^- .+$|.+', re.MULTILINE)
        matches = pattern.findall(md)
        print(matches)
        
        for match in matches:
            if re.findall(r'^#{1,6} .+$', match):
                htmlified = self.processHeadings(match)
                #print(htmlified)
                
    def main(self, md):
        i = 0
        prev = ''
        
        while (i < len(md)):
            if i != 0:
                prev = md[i - 1]
            if '\n' == md[i]:
                print('/n')
            else:
                
                print(md[i])
            # match md[i]:
            #     case '#':
            #         if (prev != self.escaper):
            #             self.processHeadings(md[i:])
            i += 1
        
        
    def processHeadings(self, text):
        count = 0
        for i in range(5):
            if (text[i] == '#'):
                count += 1
            else:
                break
        withoutNumerals = text.replace(text[0:count+1], f'<h{count}>')
        headingTag = withoutNumerals + f'</h{count}>'
        # print("1..."+text, "2..."+text[0:count+1], "3..."+str(count), '4...'+withoutNumerals, "      "+headingTag)
        return text
         
        

MarkdownParser('''# Git

Git is a version control tool that can be used to keep track of versions of a software project.

## GitHub [HTML](/wiki/HTML) AAAA

- Hola
-Si Buenas[HTML](/wiki/HTML)[HTML](/wiki/HTML)
hjnsdjn - sdsdg[HTML](/wiki/HTML)
- Jajajaj
[HTML](/wiki/HTML)

- 0Jajajaj

GitHub is an **online** service for hosting git repositories.
''')