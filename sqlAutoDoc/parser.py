import os
from .parsers import StoredProcedure

def parse_sql_procedure(target, output_file):

    # Generate a list of files to parse
    # the target parameter is overloaded and we handle 3 options
    #   - string: either specifying a single file or a directory
    #       of files with .sql files in them
    #   - list: a list of files
    if isinstance(target, str):
        if os.path.isfile(target):
            files_to_parse = [target]
        else:
            if os.path.isdir(target):
                files_to_parse = []
                for file in os.listdir(target):
                    if file.endswith('.sql'):
                        files_to_parse.append(os.path.join(target, file))
    elif isinstance(target, list):
        files_to_parse = target
    else:
        return

    # Iterate target
    with open(output_file, 'w') as out:

        for file in files_to_parse:
            with open(file, 'r') as sqlfile:
                sqlcmd = sqlfile.read()

            sp = StoredProcedure(sqlcmd)
            out.write(sp.autodoc)