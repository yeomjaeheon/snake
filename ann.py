import numpy as np

def crossover(parent1, parent2, p): #가능하면 한 쪽의 유전정보만을 가져옴
    child = nn(parent1.structure)
    for i in range(0, len(parent1.structure) - 1):
        if np.random.random() <= p:
            child.weights[i] = parent1.weights[i].copy()
        else:
            child.weights[i] = parent2.weights[i].copy()
    return child

def distance(parent1, parent2):
    delta = 0
    for i in range(0, len(parent1.structure) - 1):
        delta += np.sum((parent1.weights[i] - parent2.weights[i]) ** 2)
    return delta

class nn:
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def relu(x):
        return np.maximum(0, x)

    def __init__(self, structure):
        self.structure = structure
        self.weights = []
        for i in range(0, len(self.structure) - 1):
            self.weights.append(np.random.normal(loc = 0.0, scale = (4 / (self.structure[i] + self.structure[i + 1])) ** 0.5, size = (self.structure[i], self.structure[i + 1])))
    
    def prop(self, input_data, bias = 0.1):
        input_data = np.array(input_data)
        for w in self.weights[:-1]:
            input_data = nn.relu(np.dot(input_data + bias, w))
        return np.dot(input_data, self.weights[-1])

    def mut(self, mut_rate = 0.03, mut_scale = 0.05):
        for i in range(0, len(self.weights)):
            if np.random.random() <= mut_rate:
                #print('돌연변이 발생')
                self.weights[i] += np.random.normal(loc = 0.0, scale = mut_scale, size = (self.structure[i], self.structure[i + 1]))