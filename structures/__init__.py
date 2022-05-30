from sys import path

backslash = "\ "[:1]

path.append(backslash.join(__file__.split(backslash)[:-1:]))
