def count_tex_istances(path):
    print('Opening 2001.05970.tex file...')
    fp = open(path, 'rb')

# TITLES
    title = '\\title'
    abstract = '\\begin{abstract}'
    section = 'section'
    num_sections = 0

#FIGURES
    figure = '\\begin{figure}'
    num_figures = 0
    sub_figure = '\\begin{subfigure}'
    num_sub_figure = 0
    is_subfigure = False

#LISTS
    list = '\\begin{itemize}'
    num_lists = 0

#TABLES
    table = '\\begin{table}'
    num_tables = 0

    end = '\\end{figure}'

    for line in fp:
        l = str(line)
        if l.count(section) or l.count(title) or l.count(abstract):
            num_sections += 1
            print('Title num:   ', num_sections, '   ', l)
        elif l.count(figure):
            num_figures += 1
            print('Figure num:  ', num_figures, '   ', l)
        elif l.count(sub_figure):
            is_subfigure = True
            num_sub_figure += 1
            print('Subfigure num:   ', num_sub_figure, '   ', l)
        elif l.count(list):
            num_lists += 1
            print('List num:    ', num_lists, '   ', l)
        elif l.count(table):
            num_tables += 1
            print('Table num:   ', num_tables, '   ', l)
            
#CHECK IF I'M IN A SUB-FIGURES LIST
        if (l.count(end) and is_subfigure):
            num_figures -= 1
            is_subfigure = False

    print('Sections:    ', num_sections)
    print('Figures:     ', num_figures)
    print('Subfigures:  ', num_sub_figure)
    print('List:        ', num_lists)
    print('Tables:      ', num_tables)

path = '2001.05994.tex'
count_tex_istances(path)