def refactor_coursive_text(string_line):
    replaces_coursive_values = []
    for i in range(string_line.count('textit')):
        replace_coursive_value = string_line.split('textit{')[i + 1].split('}')[0]
        replaces_coursive_values.append(replace_coursive_value)
    for replace_coursive_value in replaces_coursive_values:
        string_line = string_line.replace('\\textit{' + replace_coursive_value + '}', replace_coursive_value)
    return string_line

def refactor_bold_text(string_line):
    replaces_bold_values = []
    for i in range(string_line.count('textbf')):
        replace_bold_value = string_line.split('textbf{')[i + 1].split('}')[0]
        replaces_bold_values.append(replace_bold_value)
    for replace_bold_value in replaces_bold_values:
        string_line = string_line.replace('\\textbf{' + replace_bold_value + '}', replace_bold_value)
    return string_line

def string_refactor(string_line):
    #remove {}
    string_line = string_line.replace('\\', '').split('{')[1].split('}')[0]
    # remove double spaces
    string_line = string_line.replace('  ', ' ')
    return string_line



def find_tex_istances(path):
    print('Opening 2001.05970.tex file...')
    fp = open(path, 'rb')
    # TITLES                                    category: 1
    title = '\\title'
    abstract = '\\begin{abstract}'
    section = '\\section'
    subsection = '\\subsection'
    num_sections = 0
    all_titles = []

    # FIGURES                                    category: 2
    figure = '\\begin{figure}'
    num_figures = 0
    sub_figure = '\\begin{subfigure}'
    num_sub_figure = 0
    is_figure = False
    is_subfigure = False
    caption = '\caption{'
    end_figure = '\\end{figure}'
    all_figures = []

    # LISTS                                      category: 3
    list = '\\begin{itemize}'
    end_list = '\\end{itemize}'
    enumerated_list = '\\begin{enumerate}'
    end_enumerated_list = '\end{enumerate}'
    item = '\\item'
    num_lists = 0
    is_list = False
    item_counter = 0
    all_lists = []

    # TABLES                                     category: 4
    table = '\\begin{table}'
    num_tables = 0

    for line in fp:
        string_line = str(line)
        # 1 category 1: titles
        if string_line.count(section) or string_line.count(subsection) or string_line.count(title) or string_line.count(abstract):
            num_sections += 1
            # CHECK FOR COURSIVE TEXT
            if ('textit' in string_line):
                string_line = refactor_coursive_text(string_line)

            # CHECK FOR BOLD TEXT
            if ('textbf' in string_line):
                string_line = refactor_bold_text(string_line)
            #string refacotr
            string_line = string_refactor(string_line)
            title_to_add = [1, num_sections, string_line]
            all_titles.append(title_to_add)
            print('Title num:   ', num_sections, '   ', string_line)
        elif string_line.count(figure):
            # 2 category 2: figures
            is_figure = True
            num_figures += 1
            print('Figure num:  ', num_figures, '   ', string_line)
        elif string_line.count(sub_figure):
            is_subfigure = True
            num_sub_figure += 1
            print('Subfigure num:   ', num_sub_figure, '   ', string_line)
        elif string_line.count(list) or string_line.count(enumerated_list):
            # 3 category 3: lists
            is_list = True
            num_lists += 1
            print('List num:    ', num_lists, '   ', string_line)
        elif string_line.count(table):
            num_tables += 1
            print('Table num:   ', num_tables, '   ', string_line)

        # CHECK IF I'M IN A SUB-FIGURES LIST
        if (string_line.count(end_figure) and is_subfigure):
            num_figures -= 1
            is_subfigure = False

        # SAVE FIGURE CAPTION IN ORDER TO HAVE A UNIVOCAL CORRESPONDENCE
        if (string_line.count(caption) and (is_figure or is_subfigure)):
            is_figure = False

            if ('textit' in string_line):
                string_line = refactor_coursive_text(string_line)

            # CHECK FOR BOLD TEXT
            if ('textbf' in string_line):
                string_line = refactor_bold_text(string_line)

            string_line = string_refactor(string_line)

            figure_to_add = [2, num_figures, string_line]
            all_figures.append(figure_to_add)

        if string_line.count(item) and is_list:
            if ('textit' in string_line):
                string_line = refactor_coursive_text(string_line)

            # CHECK FOR BOLD TEXT
            if ('textbf' in string_line):
                string_line = refactor_bold_text(string_line)

            string_line = string_line.split('\item')[1].replace('\\n', '').replace('\\', '')
            item_to_add = [3, num_lists, item_counter, string_line]
            all_lists.append(item_to_add)
            item_counter += 1

        if string_line.count(end_enumerated_list or end_list):
            is_list = False
            item_counter = 0



    print('Titles:    ', num_sections)
    print('Figures:     ', num_figures)
    print('Subfigures:  ', num_sub_figure)
    print('List:        ', num_lists)
    print('Tables:      ', num_tables)
    print(all_titles)
    print(all_figures)
    print(all_lists)


path = '2001.05994.tex'  # path to .tex file
find_tex_istances(path)
