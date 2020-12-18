class PSM:

    def __init__(self, records, attribute_list):
        print("Calculating PSM matrices...")
        attribute_list.extend(['none','begin','end'])
        self.f_matrix = self.init_f_matrix(records, attribute_list)

        attribute_list.remove('end')
        attribute_list.remove('begin')
        self.p_matrix = self.init_p_matrix(records, attribute_list)
        attribute_list.remove('none')

    def init_f_matrix(self, records, attribute_list):
        transitions = {}
        matrix = {}
        for i in attribute_list:
            transitions[i] = 0
            matrix[i] = {}
            for j in attribute_list:
                matrix[i][j] = 0

        for blocks in records:
            #begin
            i = 'begin'
            j = blocks[0].label
            matrix[i][j] += 1
            transitions[i] += 1
            #middle
            last = len(blocks)-1
            for aux in range(0,last):
                i = blocks[aux].label
                j = blocks[aux+1].label
                matrix[i][j] += 1
                transitions[i] += 1
            #ending
            i = blocks[last].label
            j = 'end'
            matrix[i][j] += 1
            transitions[i] += 1

        for i in attribute_list:
            for j in attribute_list:
                if transitions[i] > 0:
                    matrix[i][j] /= transitions[i]

        return matrix



    def init_p_matrix(self, records, attribute_list):
        max_positions = max([len(v) for v in records])
        total_in_pos = [0 for i in range(max_positions)]
        matrix = {}
        for attr in attribute_list:
            matrix[attr] = [0 for i in range(max_positions)]

        for blocks in records:
            for i in range(0,len(blocks)):
                attr = blocks[i].label
                matrix[attr][i] += 1
                total_in_pos[i] += 1

        for attr in attribute_list:
            for i in range(max_positions):
                matrix[attr][i] /= total_in_pos[i]

        return matrix
