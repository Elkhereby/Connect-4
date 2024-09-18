import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib
matplotlib.use('agg')

class Node:
    def __init__(self, value=0, type="Max"):
        self.value = value
        self.type = type
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self, level=0):
        ret = "\t" * level + f"{self.type} Node(Value: {self.value})" + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

class Tree:
    def __init__(self, root_value=0, root_type="Max"):
        self.root = Node(root_value, root_type)

    def add_node(self, parent_node, child_value, child_type="Max"):
        new_node = Node(child_value, child_type)
        parent_node.add_child(new_node)
        return new_node

    def build_graph(self, G, node, pos=None, x=0, y=0, layer=1, dx=1.0):
        if pos is None:
            pos = {}
        node_id = id(node)
        pos[node_id] = (x, y)

        label = f"{node.type}\n{node.value}"
        color = {
            "Max": "green",
            "Min": "red",
            "Chance": "yellow"
        }.get(node.type, "gray")

        G.add_node(node_id, label=label, color=color)

        next_x = x - dx * (len(node.children) - 1) / 2

        for child in node.children:
            G.add_edge(node_id, id(child))
            pos = self.build_graph(G, child, pos=pos, x=next_x, y=y - 1, layer=layer + 1, dx=dx / 2)
            next_x += dx

        return pos

    def __repr__(self):
        return self.root.__repr__()

    def draw_tree(self, filename="tree.svg"):

        G = nx.DiGraph()

        # Build the graph
        pos = self.build_graph(G, self.root, dx=2.0)

        colors = [G.nodes[node]['color'] for node in G.nodes()]
        labels = {node: G.nodes[node]['label'] for node in G.nodes()}

        plt.figure(figsize=(12, 12))
        nx.draw(G, pos, labels=labels, node_color=colors, node_size=3000, font_size=10, font_color="white")
        plt.savefig(filename, format="svg")
        plt.close()

        return filename
