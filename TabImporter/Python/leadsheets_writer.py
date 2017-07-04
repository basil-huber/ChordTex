


class LeadsheetsWriter:
    PREAMBLE_LATEX = '\n\input{../Latex/preamble.tex}\n\\begin{document}\n\n\\begin{song}{title={%s}, interpret={%s}}\n\n'
    POSTAMBLE_LATEX = '\end{song}\n\end{document}'

    def __init__(self, file_name, title, interpret):
        self.file = open(file_name, 'w')
        self.file.write(self.PREAMBLE_LATEX % (title, interpret))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.file.write(self.POSTAMBLE_LATEX)
        self.file.close()

    def write_line(self, line, chord_list):
        # pad line with white spaces if line is shorter than last chord index
        if len(chord_list) > 0:
            line  = line.ljust(chord_list[-1][1])

        line_out = ''
        i_start_old = 0
        for chord, i_start in chord_list:
            self.file.write('%s\chord{%s}' % (line[i_start_old:i_start], chord))
            i_start_old = i_start

        self.file.write(line[i_start_old:len(line)])

        if len(line) > 0:
            self.file.write('  \\\\\n')