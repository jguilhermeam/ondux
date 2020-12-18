class PSM:

    def __init__(self, records, attribute_list):
        attribute_list.append('begin')
        self.f_matrix = self.init_f_matrix(records, attribute_list)

        attribute_list.remove('begin')
        self.p_matrix = self.init_p_matrix(records, attribute_list)


    def init_f_matrix(self, records, attribute_list):
        transitions = {}
        matrix = {}
        for i in attribute_list:
            transitions[i] = 0
            matrix[i] = {}
            for j in attribute_list:
                matrix[i][j] = 0

        for blocks in records:
            for aux in range(len(blocks)):
                i = blocks[aux].label
                if aux == 0:
                    j = 'begin'
                else:
                    j = blocks[aux-1].label

                if i != 'none' and j != 'none':
                    matrix[j][i] += 1
                    transitions[j] += 1

        for i in attribute_list:
            for j in attribute_list:
                if transitions[i] > 0:
                    matrix[i][j] /= transitions[i]
                else:
                    matrix[i][j] = 0

        return matrix



    def init_p_matrix(self, records, attribute_list):
        max_positions = max([len(v) for v in records])
        total_in_pos = [0 for i in range(max_positions)]
        matrix = {}
        for attr in attribute_list:
            matrix[attr] = [0 for i in range(max_positions)]

        for blocks in records:
            for k in range(len(blocks)):
                attr = blocks[k].label
                if attr != 'none':
                    matrix[attr][k] += 1
                    total_in_pos[k] += 1

        for attr in attribute_list:
            for i in range(max_positions):
                matrix[attr][i] /= total_in_pos[i]

        return matrix
