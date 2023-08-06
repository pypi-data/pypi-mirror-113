"""
Copyright (c) 2021 Synopsys, Inc.
Use subject to the terms and conditions of the Synopsys End User Software License and Maintenance Agreement.
All rights reserved worldwide.
"""

import os
import re
import fnmatch
import ntpath
import logging
from blackduck_c_cpp.util import global_settings


class LogParser:
    """
    Parses a build log output file from coverity build command
    """

    def __init__(self):
        self.lib_path = set()
        self.dash_l_path = set()
        self.all_paths = set()
        self.abs_paths = set()
        self.rpath_binary_paths = set()
        self.pkgconf_file_paths = dict()
        self.executable_list = set()

    def resolve_path(self, path):
        """
            Function to resolve a path that contains "../" segments
            For example /lib/a/b/../c -> /lib/a/c
        """
        new_path = []
        for component in path.split('/'):
            if len(component) > 0:
                if component == '..':
                    new_path = new_path[0:len(new_path) - 1]
                else:
                    new_path = new_path + [component]
        return '/' + '/'.join(new_path)

    def find_file(self, pattern, path):
        """
            Fuzzy find files from a root path.
        """
        result = []
        for root, dirs, files in os.walk(path):
            result.extend((os.path.join(root, x) for x in fnmatch.filter(files, pattern)))
        return result

    def path_leaf(self, path):
        """
            Windows-safe filename finder.
        """
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def parse_build_log(self, log_file):
        """
        Parses on build-log.txt file and returns files called in linker invocation
        """
        try:
            with open(log_file, 'r') as text_file:
                for line in text_file:
                    match_list = [re.match(r".*EXECUTING: .*\Sc\+\+ ", line),
                                  re.match(r".*EXECUTING: .*\Sg\+\+ ", line),
                                  re.match(r".*EXECUTING: .*\Scc ", line), re.match(r".*EXECUTING: .*\Sgcc ", line)]
                    non_match_list = [re.match(r".* -c .*", line), re.match(r".* -E .*", line)]
                    linker_list = [re.match(r".*EXECUTING: .*\Sld ", line), re.match(r".*EXECUTING: .*\SLINK ", line)]
                    if any(linker_list) or (any(match_list) and not any(non_match_list)):
                        line_components = re.split(',|\s+|:', line)
                        line_components = set(map(lambda x: x.strip('"').strip("'"), line_components))
                        in_rpath = False  # are we inside of an rpath section?
                        rpath_path_set = None  # path(s) the rpath defines.
                        rpath_library_set = None  # the libraries that will be linked to said paths
                        for i, lc in enumerate(line_components):
                            if lc == "-rpath":
                                in_rpath = True
                                rpath_path_set = set()
                                rpath_library_set = set()
                            elif in_rpath:  # if we're in an "-rpath", now capture the paths, and the binaries.
                                if (":" in lc and all([os.path.exists(x) for x in lc.split(":")])) or os.path.exists(
                                        lc):
                                    rpath_path_set = set(lc.split(":"))
                                elif not lc.startswith("-"):  # when '-' shows up, we're out of the rpath
                                    for x in rpath_path_set:
                                        if os.path.exists(self.resolve_path(os.path.join(x, lc))):
                                            self.rpath_binary_paths.add(self.resolve_path(os.path.join(x, lc)))
                                        else:
                                            self.rpath_binary_paths.add(lc)
                                    # self.rpath_binary_paths = self.rpath_binary_paths.union(set([self.resolve_path(os.path.join(x, lc))
                                    #                                                    for x in rpath_path_set if os.path.exists(self.resolve_path(os.path.join(x, lc)))]))
                                    rpath_library_set.add(lc)
                                else:
                                    in_rpath = False
                                # TODO: In future, when adding pkg config
                                """
                                    for path in rpath_path_set:
                                        pkgconf_files = self.find_file("*.pc", path)
                                        if len(pkgconf_files) > 0:
                                            for pc_path in pkgconf_files:
                                                f_name = self.path_leaf(pc_path).split('.')[0]
                                                if f_name not in self.pkgconf_file_paths:
                                                    self.pkgconf_file_paths[f_name] = pc_path
                                """
                            if not in_rpath:
                                if lc.startswith('-L') and '/home' not in lc:
                                    self.lib_path.add(self.resolve_path(lc.replace('-L', '')))
                                if lc.startswith('-l'):
                                    self.dash_l_path.add(lc.strip('\n '))
                                elif re.match(global_settings.so_pattern, lc.strip()) or re.match(
                                        global_settings.dll_pattern, lc.strip()) \
                                        or re.match(global_settings.a_pattern, lc.strip()) or re.match(
                                    global_settings.lib_pattern, lc.strip()) \
                                        or re.match(global_settings.o_pattern, lc.strip()):
                                    self.all_paths.add(self.resolve_path(lc.strip('\n"')))
            # logging.debug("rpath binaries are : {}".format(self.rpath_binary_paths))
            self.all_paths.union(self.rpath_binary_paths)
            # logging.debug("all paths from build log are : {}".format(self.all_paths))

        except FileNotFoundError:
            logging.error("build-log.txt not found from cov-build..make sure cov-build is successful")

        for base_path in self.lib_path:
            for lib in self.dash_l_path:
                libname = lib.replace('-l', 'lib')
                x_so = "{}/{}.so".format(base_path, libname)
                x_a = "{}/{}.a".format(base_path, libname)
                self.all_paths.add(x_a)
                self.all_paths.add(x_so)
        basefile_list = set(map(lambda path: os.path.basename(path).strip(), self.all_paths))
        if len(basefile_list) == 0:
            logging.warning("No linker files found")
        logging.info("No of distinct components are {}".format(len(basefile_list)))
        self.all_paths.update(basefile_list)
        self.all_paths = sorted(self.all_paths, key=self.key_fn)
        return self.all_paths

    def key_fn(self, key):
        """
        Sort function to sort the paths in the order of .so, .a and .o files
        """
        if re.match(global_settings.so_pattern, key):
            return (0, key)
        elif re.match(global_settings.a_pattern, key):
            return (1, key)
        else:
            return (2, key)

    def get_exectuable(self, log_file):
        """ Parses on build-log.txt file to get output executable
               """
        try:
            with open(log_file, 'r') as text_file:
                for line in text_file:
                    match_list = [re.match(r".*EXECUTING: .*", line), re.match(r".* -o .*", line)]
                    if all(match_list):
                        pattern = re.compile('(?<=-o )([^ ])*')
                        executable_mid = re.search(pattern, line).group()
                        if not re.match(global_settings.o_pattern, executable_mid) and not re.match(
                                global_settings.cpp_pattern, executable_mid) \
                                and not re.match(global_settings.so_pattern, executable_mid) and not re.match(
                            global_settings.hpp_pattern, executable_mid) \
                                and not re.match(global_settings.a_pattern, executable_mid) and not re.match(
                            global_settings.h_pattern, executable_mid) \
                                and not re.match(global_settings.c_pattern, executable_mid) and not re.match(
                            global_settings.dll_pattern, executable_mid):
                            if not re.match(r'.*\.s$', executable_mid):
                                self.executable_list.add(re.search(pattern, line).group())
        except FileNotFoundError:
            logging.error("build-log.txt not found from cov-build..make sure cov-build is successful")
        return self.executable_list
