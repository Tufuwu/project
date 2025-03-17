import matplotlib.pyplot as plt
import networkx as nx

# 解析输入数据
data = [
    "<Node kind=stream, start_point=(0, 0), end_point=(25, 0)>",
    "<Node kind=document, start_point=(0, 0), end_point=(25, 0)>",
    "<Node kind=block_node, start_point=(0, 0), end_point=(25, 0)>",
    "<Node kind=block_mapping, start_point=(0, 0), end_point=(25, 0)>",
    "<Node kind=block_mapping_pair, start_point=(5, 0), end_point=(25, 0)>",
    "<Node kind=block_node, start_point=(6, 2), end_point=(25, 0)>",
    "<Node kind=block_mapping, start_point=(6, 2), end_point=(25, 0)>",
    "<Node kind=block_mapping_pair, start_point=(6, 2), end_point=(25, 0)>",
    "<Node kind=block_node, start_point=(7, 4), end_point=(25, 0)>",
    "<Node kind=block_mapping, start_point=(7, 4), end_point=(25, 0)>",
    "<Node kind=block_mapping_pair, start_point=(13, 4), end_point=(25, 0)>",
    "<Node kind=block_node, start_point=(14, 4), end_point=(25, 0)>",
    "<Node kind=block_sequence, start_point=(14, 4), end_point=(25, 0)>",
]

# 创建树状结构
G = nx.DiGraph()
parent_stack = []

for i, node in enumerate(data):
    node_type = node.split("kind=")[1].split(",")[0]  # 提取节点类型
    G.add_node(i, label=node_type)
    
    if i > 0:
        parent = parent_stack[-1] if parent_stack else 0  # 连接到上一层节点
        G.add_edge(parent, i)

    # 控制层级关系（这里简单处理，具体可以根据 indent 或 start_point 计算）
    if "mapping" in node_type or "sequence" in node_type:
        parent_stack.append(i)
    elif "pair" in node_type:
        parent_stack.append(i)
    elif "node" in node_type and parent_stack:
        parent_stack.pop()

# 绘制树状结构
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G, seed=42, k=0.5)  # 生成布局
labels = nx.get_node_attributes(G, "label")
nx.draw(G, pos, with_labels=True, labels=labels, node_size=2000, node_color="lightblue", edge_color="gray")
plt.title("YAML 语法树结构")
plt.show()
