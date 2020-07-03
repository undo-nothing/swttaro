import os
import re
import fnmatch
from pathlib import Path


def normalize_path_patterns(patterns):
    """Normalize an iterable of glob style patterns based on OS."""
    patterns = [os.path.normcase(p) for p in patterns]
    dir_suffixes = {'%s*' % path_sep for path_sep in {'/', os.sep}}
    norm_patterns = []
    for pattern in patterns:
        for dir_suffix in dir_suffixes:
            if pattern.endswith(dir_suffix):
                norm_patterns.append(pattern[:-len(dir_suffix)])
                break
        else:
            norm_patterns.append(pattern)
    return norm_patterns


def is_ignored_path(path, ignore_patterns):
    """
    Check if the given path should be ignored or not based on matching
    one of the glob style `ignore_patterns`.
    """
    path = Path(path)

    def ignore(pattern):
        return fnmatch.fnmatchcase(path.name, pattern) or fnmatch.fnmatchcase(str(path), pattern)

    return any(ignore(pattern) for pattern in normalize_path_patterns(ignore_patterns))


class SearchStr(object):
    """search str in a dir
    """

    ignore_patterns = None
    include_patterns = None

    def __init__(self, **options):

        ignore_patterns = options.get('ignore_patterns', [])
        self.ignore_patterns = list(set(ignore_patterns))

        include_patterns = options.get('include_patterns', ['*'])
        self.include_patterns = list(set(include_patterns))

    def find_files(self, root):
        """
        Get all files in the given root.
        """
        all_files = []
        if not os.path.exists(root):
            return []

        if os.path.isfile(root):
            all_files.append(root)
        for dirpath, dirnames, filenames in os.walk(root, topdown=True):
            for filename in filenames:
                file_path = os.path.normpath(os.path.join(dirpath, filename))
                if not is_ignored_path(file_path, self.ignore_patterns):
                    if is_ignored_path(file_path, self.include_patterns):
                        all_files.append(file_path)
        return all_files

    def iter_path(self, root):
        if not os.path.exists(root):
            return

        if os.path.isfile(root):
            yield root
        for dirpath, dirnames, filenames in os.walk(root, topdown=True):
            for filename in filenames:
                file_path = os.path.normpath(os.path.join(dirpath, filename))
                if not is_ignored_path(file_path, self.ignore_patterns):
                    if is_ignored_path(file_path, self.include_patterns):
                        yield file_path

    def search_str(self, word, root, match_all=False):
        root = os.path.abspath(root)
        root_len = len(root) + 1
        result = []
        if match_all:
            iter_path = self.find_files
        else:
            iter_path = self.iter_path
        for filepath in iter_path(root):
            with open(filepath, 'r', encoding='utf-8') as fp:
                src_data = fp.readlines()

            index = 0
            for line in src_data:
                index += 1
                if line.find(word) != -1:
                    # print('%s, line: %s' % (filepath[root_len:], index))
                    dispaly_name = filepath[root_len:]
                    dispaly_name = dispaly_name if dispaly_name else filepath
                    result.append((dispaly_name, index))
                    if match_all is False:
                        return result
        return result

    def mul_search_str(self, words, root, match_all=False):
        words = set(words)
        result = {i: [] for i in words}

        root = os.path.abspath(root)
        root_len = len(root) + 1
        if match_all:
            iter_path = self.find_files
        else:
            iter_path = self.iter_path
        for filepath in iter_path(root):
            with open(filepath, 'r', encoding='utf-8') as fp:
                src_data = fp.readlines()

            index = 0
            for line in src_data:
                index += 1
                match_words = set()
                for word in words:
                    if line.find(word) != -1:
                        # print('%s, line: %s' % (filepath[root_len:], index))
                        dispaly_name = filepath[root_len:]
                        dispaly_name = dispaly_name if dispaly_name else filepath
                        result[word].append((dispaly_name, index))
                        match_words.add(word)

                if match_all is False:
                    words = words - match_words
                if not words:
                    return result

        return result

    def re_search_str(self, pattern, root, match_all=False):
        pattern = re.compile(pattern)
        root = os.path.abspath(root)
        root_len = len(root) + 1
        result = []
        all_files = self.find_files(root)
        for filepath in all_files:
            with open(filepath, 'r', encoding='utf-8') as fp:
                src_data = fp.readlines()

            index = 0
            for line in src_data:
                index += 1
                if pattern.search(line):
                    dispaly_name = filepath[root_len:]
                    dispaly_name = dispaly_name if dispaly_name else filepath
                    result.append((dispaly_name, index))
                    if match_all is False:
                        return result
        return result
