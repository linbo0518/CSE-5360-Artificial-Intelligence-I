import sys


class BayesianNetworkNode:

    def __init__(self,
                 name=None,
                 parents=None,
                 children=None,
                 truth_table=None):
        self.name = name
        self.parents = parents
        self.children = children
        self.truth_table = self._fill_truth_table(truth_table)

    def get_p(self, conditions=None):
        return self.truth_table[conditions]

    def _fill_truth_table(self, truth_table):
        complete_truth_table = dict()
        for each_key in truth_table:
            complete_truth_table[each_key] = truth_table[each_key]
            if each_key[-1] == 't':
                complete_truth_table[each_key[:-1] +
                                     'f'] = 1 - truth_table[each_key]
            else:
                complete_truth_table[each_key[:-1 +
                                              't']] = 1 - truth_table[each_key]
        return complete_truth_table


class BayesianNetwork:

    def __init__(self, nodes):
        self.nodes = dict()
        for node in nodes:
            self.nodes[node.name] = node

    def calcuate_p(self, conditions):
        kv = self._cond2kv(conditions)
        conds = self._gen_enumerate(kv)
        p = 0
        for cond in conds:
            tmp = 1
            for node_name in cond:
                key = ''
                if self.nodes[node_name].parents:
                    for each_parent in self.nodes[node_name].parents:
                        key += cond[each_parent.name]
                key += cond[node_name]
                tmp *= self.nodes[node_name].get_p(key)
            p += tmp
        return p

    def run(self, inputs, keyword='given'):
        before, after = self._parse_inputs(inputs, keyword)
        return self.calcuate_p(before + after) / self.calcuate_p(after)

    def _cond2kv(self, conditions):
        kv = dict()
        for cond in conditions:
            kv[cond[:-1]] = cond[-1]
        return kv

    def _gen_enumerate(self, kv):
        hidden_var = list()
        res = list()
        for node_name in self.nodes:
            if node_name not in kv.keys():
                hidden_var.append(node_name)
        if len(hidden_var) > 0:
            spec = '0' + str(len(hidden_var)) + 'b'
            for i in range(2**len(hidden_var)):
                hidden_var_cond = dict()
                for idx, each in enumerate(format(i, spec)):
                    if each == '0':
                        hidden_var_cond[hidden_var[idx]] = 't'
                    else:
                        hidden_var_cond[hidden_var[idx]] = 'f'
                res.append(dict(kv, **hidden_var_cond))
        else:
            res.append(kv)
        return res

    def _parse_inputs(self, inputs, keyword='given'):
        before_keyword = []
        after_keyword = []
        keyword_flag = False
        for arg in inputs:
            if arg == keyword:
                keyword_flag = True
                continue
            if keyword_flag:
                after_keyword.append(arg)
            else:
                before_keyword.append(arg)
        return before_keyword, after_keyword


if __name__ == "__main__":
    # inputs
    inputs = sys.argv[1:]
    # bayesian network
    node_b = BayesianNetworkNode('B', truth_table={'t': 0.001})
    node_e = BayesianNetworkNode('E', truth_table={'t': 0.002})
    node_a = BayesianNetworkNode('A',
                                 truth_table={
                                     'ttt': 0.95,
                                     'tft': 0.94,
                                     'ftt': 0.29,
                                     'fft': 0.001
                                 })
    node_j = BayesianNetworkNode('J', truth_table={'tt': 0.90, 'ft': 0.05})
    node_m = BayesianNetworkNode('M', truth_table={'tt': 0.70, 'ft': 0.01})
    node_b.children = [node_a]
    node_e.children = [node_a]
    node_a.parents = [node_b, node_e]
    node_a.children = [node_j, node_m]
    node_j.parents = [node_a]
    node_m.parents = [node_a]
    bnet = BayesianNetwork([node_b, node_e, node_a, node_j, node_m])
    # calc
    print(f"Probability = {bnet.run(inputs):.5f}")
