import argparse
import yaml
from HeaderParser import HeaderParser

def handle_header_parser(args):
    file_path = args.file_path
    save_path = args.o
    header_handler = HeaderParser(file_path=file_path)
    parse_obj = header_handler.parse()
    if parse_obj == None:
        print("Parsing header returns None. Please check for error")
        return

    result = yaml.dump(parse_obj)
    if save_path == "":
        print(result)
    else:
        with open(save_path, 'w') as file:
            file.write(result)
            file.close()

def main():
    header_parser = argparse.ArgumentParser(
                    prog='Parsing header file to list of functions',
                    description='Currently support parsing header file to get function names')
    header_parser.add_argument("file_path", 
                        metavar="path",
                        type=str,
                        help="Path to header file")

    header_parser.add_argument("-o", metavar="save_path", type=str, default="", help="save result to")
    return header_parser.parse_args()
if __name__ == '__main__':
    args = main()
    handle_header_parser(args)
    pass