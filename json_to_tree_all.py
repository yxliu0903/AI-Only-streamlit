import graphviz
import json

# 从 JSON 文件中读取数据
with open('/nas/shared/GAIR/yyliu/Thought_plus/teacher_only/result_gpt4o-v8_with-gold-answer_all-steps.jsonl', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 创建图
for j,question in enumerate(data):
    question_title = question['question']
    steps = question['steps']

    dot = graphviz.Digraph()

    # 添加问题作为根节点
    dot.node(question_title, question_title)

    # 使用字典按层次存储节点
    layers = {}

    # 添加步骤和边
    for i, step in enumerate(steps):
        content = step["content"]
        step_taken = step["step taken"].split(" -> ")
        layer = step["tree tag"].split(",")[0].strip('()')  # 获取第一项

        # 将节点按层次存储
        if layer not in layers:
            layers[layer] = []
        layers[layer].append((step_taken[0], step_taken[0]+'\n'+content[:30] + '...'))

        # 添加边
        if len(step_taken) > 1:
            dot.edge(step_taken[0], step_taken[1], label=str(i))

    # 为每一层添加子图
    for layer, nodes in layers.items():
        with dot.subgraph() as s:
            s.attr(rank='same')  # 设置为同一层
            for node, label in nodes:
                s.node(node, label)

    # 连接根节点和第一个步骤
    dot.edge(question_title, steps[0]["step taken"].split(" -> ")[0])

    # 渲染并保存图像
    dot.render(f'/nas/shared/GAIR/yyliu/Thought_plus/teacher_only/graph/v8_with-gold-solution/flowchart_{j+1}', format='json', cleanup=True)
