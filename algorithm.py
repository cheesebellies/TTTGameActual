import random, math
import numpy as np
import copy

class Node:
    def __init__(self, bias: float):
        self.bias = bias
        self.connection_weights = []
        self.connection_nodes = []
        self.running_sum = bias
        
    def receive(self, value: float):
        self.running_sum += value
    
    def propogate(self):
        sval = self.sigmoid(self.running_sum)
        self.running_sum = self.bias
        for i in range(len(self.connection_nodes)):
            self.connection_nodes[i].receive(sval*self.connection_weights[i])
    
    def sigmoid(self, value: float):
        # value = max(min(value,709),-709)
        if value > 0.0:
            return value
        else:
            return 0.0 # 1.0/(1+(math.e**(-value)))
    
    def return_value(self):
        tr = self.running_sum
        self.running_sum = self.bias
        return self.sigmoid(tr)
    
    def connect_to(self, node: 'Node', weight: float):
        self.connection_nodes.append(node)
        self.connection_weights.append(weight)
    
    def randomize(self, scale: float):
        r = random.uniform(-scale,scale)
        if random.randint(0,5) == 5:
            self.bias += r*0.1
        for i in range(len(self.connection_weights)):
            if random.randint(0,5) != 5: continue
            r = random.uniform(-scale,scale)
            self.connection_weights[i] += r
            # self.connections[connection] = max(min(self.connections[connection],10.0),-10.0)



class Layer:
    def __init__(self, width: int):
        self.width = width
        self.nodes = []
        for i in range(width):
            # r = random.uniform(-0.1,0.1)
            self.nodes.append(Node(0.1))
    
    def connect_nodes(self, to_layer):
        for node in self.nodes:
            node.connection_weights = []
            node.connection_nodes = []
            if to_layer:
                for onode in to_layer.nodes:
                    node.connect_to(onode,random.uniform(-0.5,0.5))

    def reconnect_nodes(self,to_layer):
        for node in self.nodes:
            node.connection_nodes = []
            for onode in to_layer.nodes:
                node.connection_nodes.append(onode)
    
    def input_values(self, values: list):
        for i in range(len(self.nodes)):
            self.nodes[i].receive(values[i])
    
    def return_values(self):
        trl = []
        for node in self.nodes:
            trl.append(node.return_value())
        return trl

    def propogate_nodes(self):
        for node in self.nodes:
            node.propogate()
    
    def randomize(self, scale: float):
        for node in self.nodes:
            node.randomize(scale)


class Algorithm:
    def __init__(self, input_nodes: int, hidden_layers: int, hidden_layer_width: int, output_nodes: int):
        self.input_layer = Layer(input_nodes)
        self.output_layer = Layer(output_nodes)
        self.hidden_layers = []
        for i in range(hidden_layers):
            self.hidden_layers.append(Layer(hidden_layer_width))
        tl = [self.input_layer] + self.hidden_layers + [self.output_layer]
        for l in range(len(tl)-1):
            tl[l].connect_nodes(tl[l+1])
        self.score = 0.0
    
    def run(self, inputs: list):
        self.input_layer.input_values(inputs)
        self.input_layer.propogate_nodes()
        for layer in self.hidden_layers:
            layer.propogate_nodes()
        return self.output_layer.return_values()

    def mutate(self, scale: float):
        for layer in ([self.input_layer] + self.hidden_layers + [self.output_layer]):
            for node in layer.nodes:
                node.randomize(scale)
    
    def splice(self, l1,l2,s):
        l = len(l1)
        o = int(l/2)
        b = [i for i in range(l)]
        c = [i for i in range(l)]
        for i in range(o):
            v = (s+i)%l 
            c[v] = l1[v]
            b.remove(v)
        for i in b:
            c[i] = l2[i]
        return c
    
    def crossover(self, all: 'Algorithm', oll: 'Algorithm'):
        al = ([all.input_layer] + all.hidden_layers + [all.output_layer])
        ol = ([oll.input_layer] + oll.hidden_layers + [oll.output_layer])
        child_node_layout = []
        for i in range(3):
            nodes = al[i].nodes
            s = random.randint(0,(len(nodes)-1))
            child_node_layout.append(self.splice(al[i].nodes,ol[i].nodes,s))
        alg = Algorithm(len(self.input_layer.nodes),len(self.hidden_layers),len(self.hidden_layers[0].nodes),len(self.output_layer.nodes))
        fcnl = [[copy.deepcopy(i) for i in j] for j in child_node_layout]
        child_node_layout = fcnl
        alg.input_layer.nodes = child_node_layout[0]
        for i in range(len(child_node_layout)-2):
            alg.hidden_layers[i].nodes = child_node_layout[i+1]
        alg.output_layer.nodes = child_node_layout[-1]
        tl = [alg.input_layer] + alg.hidden_layers + [alg.output_layer]
        for l in range(len(tl)-1):
            tl[l].reconnect_nodes(tl[l+1])
        return alg

        