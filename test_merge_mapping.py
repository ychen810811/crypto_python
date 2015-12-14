import simple_sub_hacker
import pprint
letter_mapping_1 = {'B': [], 'P': [], 'Q': ['C'], 'S': [], 'A': [], 'H': ['M'], 'I': ['O'], 'E': [], 'J': [], 'N': ['L'], 'D': [], 'W': [], 'L': ['N'], 'O': ['U'], 'V': [], 'Y': [], 'C': ['T'], 'M': [], 'G': ['B'], 'F': [], 'U': [], 'T': [], 'R': ['R'], 'K': ['A'], 'Z': ['E', 'Y'], 'X': ['F']}
letter_mapping_2 = {'B': ['S', 'D'], 'P': ['C', 'I', 'P', 'U'], 'Q': ['N', 'C', 'R', 'I'], 'S': [], 'A': [], 'H': [], 'I': [], 'E': [], 'J': [], 'N': [], 'D': [], 'W': [], 'L': ['O', 'N'], 'O': [], 'V': [], 'Y': [], 'C': [], 'M': [], 'G': [], 'F': [], 'U': [], 'T': [], 'R': ['V', 'R', 'T'], 'K': ['R', 'A', 'N'], 'Z': ['E'], 'X': []}
letter_mapping_3 = {'W': [], 'M': ['A', 'D'], 'O': [], 'F': [], 'D': [], 'B': ['M', 'S'], 'T': [], 'C': ['Y', 'T'], 'N': [], 'J': [], 'U': [], 'G': [], 'A': [], 'E': [], 'P': ['D', 'I'], 'Q': [], 'K': ['I', 'A'], 'L': ['L', 'N'], 'V': [], 'Z': [], 'R': [], 'I': ['E', 'O'], 'S': ['T', 'P'], 'X': [], 'H': [], 'Y': []}

letter_mapping = simple_sub_hacker._blank_letter_mapping()

simple_sub_hacker._intersect_mapping(letter_mapping, letter_mapping_1)
simple_sub_hacker._intersect_mapping(letter_mapping, letter_mapping_2)
simple_sub_hacker._intersect_mapping(letter_mapping, letter_mapping_3)

pprint.pprint(letter_mapping)