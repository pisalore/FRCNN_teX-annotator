fp = open('samplebody-conf.tex', 'rb')
section = 'section'
num_sections = 0
figure = '\\begin{figure}'
num_figures = 0
list = '\\begin{itemize}'
num_list = 0
table = '\\begin{table}'
num_tables = 0

for line in fp:
    l = str(line)
    if l.count(section):
        num_sections += 1
        print('Title num: ', num_sections, '   ', l)
    if l.count(figure):
        num_figures += 1
        print('Figure num: ', num_figures, '   ', l)
    if l.count(list):
        num_list += 1
        print('List num: ', num_list, '   ', l)
    if l.count(table):
        num_tables += 1
        print('Figure num: ', num_table, '   ', l)

print ('Sections: ', num_sections)
print ('Figures: ', num_figures)
print ('List: ', num_list)
print ('Tables: ', num_tables)