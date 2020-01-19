def count_tex_istances(path):
    print('Opening 2001.05970.tex file...')
    fp = open(path, 'rb')

    objects = []

# TITLES                                    category: 1
    title = '\\title'
    abstract = '\\begin{abstract}'
    section = 'section'
    num_sections = 0

    all_titles = []

#FIGURES                                    category: 2
    figure = '\\begin{figure}'
    num_figures = 0
    sub_figure = '\\begin{subfigure}'
    num_sub_figure = 0
    is_subfigure = False

#LISTS                                      category: 3
    list = '\\begin{itemize}'
    num_lists = 0

#TABLES                                     category: 4
    table = '\\begin{table}'
    num_tables = 0

    end = '\\end{figure}'

    for line in fp:
        string_line = str(line)
        if string_line.count(section) or string_line.count(title) or string_line.count(abstract):
            num_sections += 1
            # CHECK FOR COURSIVE TEXT
            if ('textit' in string_line):
                replace_values = []
                for i in range (string_line.count('textit')):
                    replace_value = string_line.split('textit{')[i + 1].split('}')[0]
                    replace_values.append(replace_value)
                for i in range (string_line.count('textit')):
                    string_line = string_line.replace('\\textit{' + replace_values[i] + '}', replace_values[i])
            # CHECK FOR BOLD TEXT
            if ('textbf' in string_line):
                replace_values = []
                for i in range (string_line.count('textbf')):
                    replace_value = string_line.split('textbf{')[i + 1].split('}')[0]
                    replace_values.append(replace_value)
                for i in range (string_line.count('textbf')):
                    string_line = string_line.replace('\\textbf{' + replace_values[i] + '}', replace_values[i])

            string_line = string_line.replace('\\', '').split('{')[1].split('}')[0]
            title_to_add = [1, string_line]
            all_titles.append(title_to_add)
            print('Title num:   ', num_sections, '   ', string_line)
        elif string_line.count(figure):
            num_figures += 1
            print('Figure num:  ', num_figures, '   ', string_line)
        elif string_line.count(sub_figure):
            is_subfigure = True
            num_sub_figure += 1
            print('Subfigure num:   ', num_sub_figure, '   ', string_line)
        elif string_line.count(list):
            num_lists += 1
            print('List num:    ', num_lists, '   ', string_line)
        elif string_line.count(table):
            num_tables += 1
            print('Table num:   ', num_tables, '   ', string_line)
            
#CHECK IF I'M IN A SUB-FIGURES LIST
        if (string_line.count(end) and is_subfigure):
            num_figures -= 1
            is_subfigure = False

    print('Titles:    ', num_sections)
    print('Figures:     ', num_figures)
    print('Subfigures:  ', num_sub_figure)
    print('List:        ', num_lists)
    print('Tables:      ', num_tables)
    print(all_titles)

path = '2001.05970.tex'
count_tex_istances(path)

