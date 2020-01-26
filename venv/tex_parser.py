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
    string_line = string_line.replace('\\', '').split('{')[1].split('}')[0]
    string_line = string_line.replace('  ', ' ')
    return string_line

def find_tex_istances(path):
    print('Opening ' + path)
    fp = open(path, 'rb')

    #LIST WHICH WILL BE RETURNED FOR PDF PARSING COMPARISON
    all_tex_objects = []

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

    #CAPTION VALUE
    caption = '\caption{'

    # TABLES                                     category: 4
    table = '\\begin{table}'
    end_table = '\\end{table]'
    is_table = False
    num_tables = 0
    all_tables = []

    for line in fp:
        string_line = line.decode("utf-8")
        # 1 category 1: titles
        if string_line.count(section) or string_line.count(subsection) or string_line.count(title) or string_line.count(abstract):
            num_sections += 1
            if ('textit' in string_line):
                string_line = refactor_coursive_text(string_line)
            if ('textbf' in string_line):
                string_line = refactor_bold_text(string_line)
            string_line = string_refactor(string_line)
            title_to_add = [1, num_sections, string_line]
            all_titles.append(title_to_add)

        # 2 category 2: figures
        elif string_line.count(figure):
            is_figure = True
            num_figures += 1
        elif string_line.count(sub_figure):
            is_subfigure = True
            num_sub_figure += 1

        # 3 category 3: lists
        elif string_line.count(list) or string_line.count(enumerated_list):
            is_list = True
            num_lists += 1

        # 3 category 3: tables
        elif string_line.count(table):
            num_tables += 1
            is_table = True

        # CHECK IF I'M IN A SUB-FIGURES LIST
        if (string_line.count(end_figure) and is_subfigure):
            num_figures -= 1
            is_subfigure = False

        # SAVE FIGURE CAPTION IN ORDER TO HAVE A UNIVOCAL CORRESPONDENCE
        if (string_line.count(caption) and (is_figure or is_subfigure)):
            is_figure = False

            if ('textit' in string_line):
                string_line = refactor_coursive_text(string_line)

            if ('textbf' in string_line):
                string_line = refactor_bold_text(string_line)
            string_line = string_refactor(string_line)

            figure_to_add = [2, num_figures, string_line]
            all_figures.append(figure_to_add)

        # SAVE LIST CAPTION IN ORDER TO HAVE A UNIVOCAL CORRESPONDENCE
        if (string_line.count(caption) and is_table):
            is_table = False

            if ('textit' in string_line):
                string_line = refactor_coursive_text(string_line)

            # CHECK FOR BOLD TEXT
            if ('textbf' in string_line):
                string_line = refactor_bold_text(string_line)

            string_line = string_refactor(string_line)
            table_to_add = [4, num_tables, string_line]
            all_tables.append(table_to_add)

        # ITEMS IN LISTS
        if string_line.count(item) and is_list:
            if ('textit' in string_line):
                string_line = refactor_coursive_text(string_line)

            if ('textbf' in string_line):
                string_line = refactor_bold_text(string_line)

            string_line = string_line.split('\\item')[1]
            item_to_add = [3, num_lists, item_counter, string_line]
            all_lists.append(item_to_add)
            item_counter += 1

        #VERIFY IF A LISTS ENDS
        if string_line.count(end_enumerated_list or end_list):
            is_list = False
            item_counter = 0


#SAVE ALL OBJECTS AND RETURN
    all_tex_objects.append(all_titles)          #TITLES     0
    all_tex_objects.append(all_figures)         #FIGURES    1
    all_tex_objects.append(all_lists)           #LISTS      2
    all_tex_objects.append(all_tables)          #TABLES     3

    print('Titles:    ', num_sections)
    print('Figures:     ', num_figures)
    print('Subfigures:  ', num_sub_figure)
    print('List:        ', num_lists)
    print('Tables:      ', num_tables)

    return all_tex_objects


# path = '2001.05970.tex'  # path to .tex file
# objects = find_tex_istances(path)
# print(objects[2])
