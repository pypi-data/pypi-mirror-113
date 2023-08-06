import re

so_pattern = re.compile(r".*\.so$|.*\.so\..+$")
a_pattern = re.compile(r".*\.a$|.*\.a\..+$")
o_pattern = re.compile(r".*\.o$|.*\.o\..+$")
cpp_pattern = re.compile(r".*\.cpp$|.*\.cpp\..+$")
c_pattern = re.compile(r".*\.c$|.*\.c\..+$")
hpp_pattern = re.compile(r".*\.hpp$|.*\.hpp\..+$")
h_pattern = re.compile(r".*\.h$|.*\.h\..+$")
dll_pattern = re.compile(r".*\.dll$|.*\.dll\..+$")
lib_pattern = re.compile(r".*\.lib|.*\.lib\..+$")
