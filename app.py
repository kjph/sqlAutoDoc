import sqlAutoDoc

def main():

    sqlAutoDoc.parse_sql_procedure('tests/res/', 'test2.md')
        
if __name__ == '__main__':
    main()