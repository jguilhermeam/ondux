from reinforcement.psm import PSM

def reinforce(records, attribute_list):
    psm = PSM(records, attribute_list)
    for blocks in records:
        for i in range(len(blocks)):
            classify(i,blocks,attribute_list,psm)


def classify(j,blocks,attribute_list,psm):
    if j == 0:
        i_attr = 'begin'
    else:
        i_attr = blocks[j-1].label
    teste = blocks[j].label
    attribute_score = {}
    for attr in attribute_list:
        if i_attr == 'none':
            fw = 0
        else:
            fw = psm.f_matrix[i_attr][attr]
        attribute_score[attr] = 1 - ((1-blocks[j].matching_score[attr])*(1-fw)*(1-psm.p_matrix[attr][j]))
    blocks[j].reinforcement_score = attribute_score
    blocks[j].label = blocks[j].get_top_reinforcement_score()
