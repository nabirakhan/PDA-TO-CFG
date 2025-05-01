import xml.etree.ElementTree as ET


class PDA:
    def __init__(self, file_name):
        self.file_name = file_name
        self.load_file()

    def load_file(self):
        tree = ET.parse(self.file_name)
        self.root = tree.getroot()
        self.parse()
    
    def parse(self):
        self.parse_alphabets()
        self.parse_states()
        self.parse_transitions()

    def parse_alphabets(self):
        alphabets_element = self.root.find('Alphabets')
        input_alphabets_element = alphabets_element.find('Input_alphabets')
        stack_alphabets_element = alphabets_element.find('Stack_alphabets')

        self.input_alphabets = set()
        self.stack_alphabets = set()
        self.stack_tail_letter = None

        for alphabet in input_alphabets_element:
            self.input_alphabets.add(alphabet.attrib['letter'])

        for alphabet in stack_alphabets_element:
            if alphabet.tag == 'alphabet':
                self.stack_alphabets.add(alphabet.attrib['letter'])
            elif alphabet.tag == 'tail':
                if self.stack_tail_letter is not None:
                    raise Exception('More than one tail letter for stack!')
                self.stack_tail_letter = alphabet.attrib['letter']

        if self.stack_tail_letter is None:
            raise Exception('No tail letter for stack!')

    def parse_states(self):
        states_element = self.root.find('States')
        state_elements = states_element.findall('state')
        initial_state_element = states_element.find('initialState')
        final_states_element = states_element.find('FinalStates')

        self.states = set()
        self.final_states = set()

        for state in state_elements:
            self.states.add(state.attrib['name'])

        for state in final_states_element:
            self.final_states.add(state.attrib['name'])

        self.initial_state = initial_state_element.attrib['name']

    def parse_transitions(self):
        transitions_element = self.root.find('Transitions')
        self.transitions = []

        for transition in transitions_element:
            self.transitions.append({
                'source': transition.attrib['source'],
                'destination': transition.attrib['destination'],
                'input': transition.attrib['input'],
                'stack_read': transition.attrib['stackRead'],
                'stack_write': transition.attrib['stackWrite']
            })

    @staticmethod
    def lambda_symbol(input_str, empty=False):
        return '' if empty and input_str in ('', 'lambda') else 'λ' if input_str in ('', 'lambda') else input_str

    def convert_to_cfg(self):
        cfg_rules = []

        for transition in self.transitions:
            if transition['stack_write'] in ('', 'lambda'):
                cfg_rules.append(f"({transition['source']}{transition['stack_read']}{transition['destination']}) → "
                               f"{self.lambda_symbol(transition['input'])}")
            elif len(transition['stack_write']) == 2:
                for state1 in self.states:
                    for state2 in self.states:
                        cfg_rules.append(
                            f"({transition['source']}{transition['stack_read']}{state1}) → "
                            f"{self.lambda_symbol(transition['input'], True)}"
                            f"({self.initial_state}{transition['stack_write'][0]}{state2})"
                            f"({state2}{transition['stack_write'][1]}{state1})"
                        )
            else:
                raise Exception(f'Stack write should be 0 or 2 characters: "{transition["stack_write"]}"')

        return cfg_rules
