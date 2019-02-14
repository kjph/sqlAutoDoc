import re

from ..strutils import md_heading, is_indented

class StoredProcedure(object):

    # Match all lines between a line containing 'as/*' followed by a line of equal characters 
    # and another line of equals followed by the line '*/begin'
    RE_DocString = re.compile(r'as/\*\n=*\n((?:.+\n+)+)=*\n\*/begin', re.MULTILINE)

    # Match the text between the line starting 'create procedure' and the line starting with 'as'
    RE_ParameterBlock = re.compile(r'create procedure .+\n((?:.+\n)+)as', re.MULTILINE)

    def __init__(self, raw):
        self._raw = raw

        # The object identifier
        self._object = re.search(r'create procedure (.+)\n', self._raw, re.IGNORECASE).group(1)
        
        # Determine the schema and object name
        match = re.search(r'\[?(\w+)\]?.\[?(\w+)\]?', self._object)
        self._schema = match.group(1)
        self._name = match.group(2)
        self._autodoc_level = 2

    def get_docstring(self):

        match = StoredProcedure.RE_DocString.search(self._raw)
        if not(match):
            return {}

        lines = match.group(1).splitlines()
        _docstring_sections = {}
        current_heading = ''

        for line in lines:
            if line.strip() == '':
                continue
            
            if not(is_indented(line)):
                current_heading = line.strip()

                # Check to see if this is the description
                test_pattern = r'\[?' + self._schema + r'\]?.\[?' + self._name + r'\]?'
                test_main_heading = re.search(test_pattern, current_heading)
                #current_heading = self._object if test_main_heading else current_heading.title()
                current_heading = self._object if current_heading == 'Description' else current_heading.title()
                
                _docstring_sections[current_heading] = ''
    
            else:
                _docstring_sections[current_heading] += "{}\n".format(line.strip())
            
        return _docstring_sections

    def get_parameters(self):
        """ Parsers the section between the prodcure create statement and the 'as' statement.
        It is important that EACH parameter is defined on its own separate line for this
        method to correctly work.
        """

        match = StoredProcedure.RE_ParameterBlock.search(self._raw)

        parameters = {}

        if match:
            parameter_block = match.group(1)
            for line in [x.strip() for x in parameter_block.splitlines()]:

                # Match parameter either defined as
                #   ,@<TEXT>    <TYPE> <DEFAULT SETTING>
                #   @<TEXT <TYPE> <DEFAULT SETTING>
                # Notice we do not care about space here
                match = re.search(r'\s*,?\s*@(\w+)\s+([\w]+\(?[0-9]*\)?)(=?.*)', line)
                if match:
                    param = match.group(1)
                    param_type = match.group(2).lower()

                    parameters[param] = {'type': param_type, 'notes': []}

                    default = match.group(3).replace('=', '').strip()
                    if default != '':
                        parameters[param]['default'] = default
                else:
                    if line.startswith('--') and param in parameters:
                        parameters[param]['notes'].append(line.replace('--', '').strip())

        return parameters

    def parameter_docs(self):
        """ Formats the parameter documentation. See get_parameters() to determine
        how these are parsed.
        """

        params = self.get_parameters()

        param_docs = ""

        for p, t in params.items():
            param_docs += '* '
            if 'default' in t:
                param_docs += '`{}` (`{}`, default `{}`)'.format(p, t['type'], t['default'])
            else:
                param_docs += '`{}` (`{}`)'.format(p, t['type'])

            notes = ' '.join(t['notes']).strip()
            if notes != '':
                param_docs += ': {}'.format(notes)

            param_docs += '\n'

        return param_docs

    @property
    def autodoc(self):
        """ The objects documentation in plaintext (string)

        This property will parse any documentation which matches the 
        RE_DocString regex pattern.
        """

        doc = ""

        # Start of AUTODOC
        doc += md_heading(self._autodoc_level, "Stored procedure [{}].[{}]".format(self._schema, self._name))
        docstring_sections = self.get_docstring()

        # Main body
        if self._object in docstring_sections:
            doc += docstring_sections.pop(self._object, None)            

        # Parameters
        doc += "\n"
        doc += md_heading(self._autodoc_level + 1, "Parameters")
        doc += self.parameter_docs()

        # Other user defined sections in docstring
        for heading, body in docstring_sections.items():
            section = "\n{}{}".format(
                md_heading(self._autodoc_level + 1, heading)
                ,body
            )
            doc += section

        doc += '\n'
        return doc