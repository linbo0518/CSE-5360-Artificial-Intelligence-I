import sys


class CandyBag:

    def __init__(self, prior: float, cherry: float, lime: float):
        assert (prior <= 1 and cherry <= 1 and lime <= 1 and prior >= 0 and
                cherry >= 0 and lime >= 0)
        self._prior = prior
        self._cherry = cherry
        self._lime = lime

    @property
    def prior(self):
        return self._prior

    @property
    def cherry(self):
        return self._cherry

    @property
    def lime(self):
        return self._lime

    def get_prob(self, key: str):
        if key == 'C':
            return self.cherry
        elif key == 'L':
            return self.lime
        else:
            return self.prior


class PosteriorProbabilityCalculator:

    def __init__(self, priors: list, cherries: list, limes: list):
        self.bags = list()
        for prior, cherry, lime in zip(priors, cherries, limes):
            self.bags.append(CandyBag(prior, cherry, lime))
        self._prob = [bag.prior for bag in self.bags]
        self._p_cherry = self._compute_prob('C')
        self._p_lime = self._compute_prob('L')

    @property
    def prob(self):
        return self._prob

    @property
    def p_cherry(self):
        return self._p_cherry

    @property
    def p_lime(self):
        return self._p_lime

    def update_prob(self):
        self._p_cherry = self._compute_prob('C')
        self._p_lime = self._compute_prob('L')
        return self._p_cherry, self._p_lime

    def update_prob_each(self, key: str):
        for idx, (prob, bag) in enumerate(zip(self.prob, self.bags)):
            self._prob[idx] = (prob * bag.get_prob(key)) / self.get_prob(key)
        return self._prob

    def get_prob(self, key: str):
        if key == 'C':
            return self._p_cherry
        elif key == 'L':
            return self._p_lime
        else:
            return self._prob

    def run(self, observations: str):
        if self._check_observations(observations):
            with open('result.txt', 'w') as f:
                log = ""
                log += f"Observation sequence Q: {observations}\n"
                log += f"Length of Q: {len(observations)}\n\n"
                for idx, key in enumerate(observations):
                    probability = self.update_prob_each(key)
                    p_cherry, p_lime = self.update_prob()
                    log += f"After Observation {idx+1} = {key}:\n\n"
                    for h_idx, prob in enumerate(probability):
                        log += f"P(h{h_idx+1} | Q) = {prob:.5f}\n"
                    log += '\n'
                    log += f"Probability that the next candy we pick will be C, given Q: {p_cherry:.5f}\n"
                    log += f"Probability that the next candy we pick will be L, given Q: {p_lime:.5f}\n\n"
                f.write(log)
            return self.prob, self.p_cherry, self.p_lime
        else:
            pass

    def _compute_prob(self, key: str):
        result = 0
        for prob, bag in zip(self.prob, self.bags):
            result += prob * bag.get_prob(key)
        return result

    def _check_observations(self, string: str):
        remain = string.replace('C', '').replace('L', '')
        if len(remain) == 0:
            return True
        else:
            print(f"Your input is invalid, input should be either 'C' or 'L'")
            False


if __name__ == "__main__":
    # config
    priors = [0.1, 0.2, 0.4, 0.2, 0.1]
    cherries = [1.0, 0.75, 0.5, 0.25, 0.0]
    limes = [0.0, 0.25, 0.5, 0.75, 1.0]
    # input
    observations = sys.argv[1].upper()
    # run
    calc = PosteriorProbabilityCalculator(priors, cherries, limes)
    calc.run(observations)
