def count_tex_istances(path):
    print('Opening 2001.05970.tex file...')
    fp = open(path, 'rb')

    title = '\\title'
    abstract = '\\begin{abstract}'
    section = 'section'
    num_sections = 0
    figure = '\\begin{figure}'
    num_figures = 0
    list = '\\begin{itemize}'
    num_lists = 0
    table = '\\begin{table}'
    num_tables = 0

    for line in fp:
        l = str(line)
        if l.count(section) or l.count(title) or l.count(abstract):
            num_sections += 1
            print('Title num: ', num_sections, '   ', l)
        if l.count(figure):
            num_figures += 1
            print('Figure num: ', num_figures, '   ', l)
        if l.count(list):
            num_lists += 1
            print('List num: ', num_lists, '   ', l)
        if l.count(table):
            num_tables += 1
            print('Figure num: ', num_tables, '   ', l)

    print('Sections: ', num_sections)
    print('Figures: ', num_figures)
    print('List: ', num_lists)
    print('Tables: ', num_tables)

path = '2001.05970.tex'
count_tex_istances(path)