from Parser import Parser

def main():
    parser = Parser('log.txt')
    parser.parse()
    parser.collectData()

if __name__ == '__main__':
    main()