import clang.cindex
from clang.cindex import TokenKind
from clang.cindex import TranslationUnitLoadError
import re

class HeaderParser:
    def __init__(self, file_path) -> None:
        self._file_path = file_path
        self.idx_parser = clang.cindex.Index.create()
        self._function_USR_regex = re.compile(r'c\:(@S@[a-zA-Z0-9_]+){0,}@F@~{0,1}[a-zA-Z0-9_]+#')
    
    def _get_functions(self, tokens : list[clang.cindex.Token]):
        func_list = []
        for token in tokens:
            token_kind = token.kind
            usr_desc = str(token.cursor.get_usr())
            # print(str(token.kind )+ "\t" + str(token.spelling) + "\t" + usr_desc)
            if token_kind != TokenKind.IDENTIFIER:
                continue 
            
            match_obj = self._function_USR_regex.match(usr_desc)
            if match_obj != None and match_obj.group(0) not in func_list:
                func_list.append(match_obj.group(0))
        
        func_list = [line[2:-1] for line in func_list]
        
        res = {}
        for func in func_list:
            sep = func.split("@F@")
            func_name = sep[-1]

            func_class_path = [p for p in sep[0].split("@S@") if p != ""]
            iterator = res
            for i in range(len(func_class_path)):
                if i == len(func_class_path) - 1:
                    if func_class_path[i] not in iterator:
                        iterator[func_class_path[i]] = {}
                    iterator = iterator[func_class_path[i]]
                    if "func-list" not in iterator:
                        iterator["func-list"] = []
                    iterator["func-list"].append(func_name)
                else:
                    if func_class_path[i] not in iterator:
                        iterator[func_class_path[i]] = {}
                    if 'sub-class' not in iterator[func_class_path[i]]:
                        iterator[func_class_path[i]]['sub-class'] = {}
                    iterator = iterator[func_class_path[i]]['sub-class']
        return res
            

    def parse(self):
        try:
            with open(self._file_path, 'r') as file:
                data = file.read()
                file.close()
            
            translation_unit = self.idx_parser.parse("abc.cpp", args=['-std=c++11'],  
                                                    unsaved_files=[("abc.cpp", data)],  options=0)
        except TranslationUnitLoadError as e:
            print(f"Error while parsing file: {self._file_path}")
            return None
        except FileNotFoundError as e:
            print(f"Cannot find file {self._file_path}")
            return None
        
        tokens = translation_unit.get_tokens(extent=translation_unit.cursor.extent)
        return self._get_functions(tokens)