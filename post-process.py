# import json
# from collections import defaultdict

# def find_unused_node(tree_level, used_nodes):
#     # 寻找同一层级的未使用节点
#     max_node = max(used_nodes, key=lambda x: int(x.split(",")[1].strip(" )")))
#     level, node = max_node.split(",")
#     next_node = int(node.strip(" )")) + 1
#     return f"({level}, {next_node})"

# def update_steps(steps):
#     node_history = defaultdict(list)  # 记录每个层级的所有出现过的节点
#     node_mapping = {}  # 记录节点替换映射
#     updated_steps = []
    
#     for i, step in enumerate(steps):
#         tree_tag = step["tree tag"]
#         step_taken = step["step taken"]
#         step_parts = step_taken.split(" -> ")

#         from_node = step_parts[0]
#         to_node = step_parts[1]

#         # 检查当前回溯的目标节点是否已经出现过
#         if "Backtrack" in step["decision"] and to_node in node_history[to_node.split(",")[0]]:
#             # 如果目标节点已经出现，找到一个同层级的未使用节点
#             new_to_node = find_unused_node(to_node.split(",")[0], node_history[to_node.split(",")[0]])
#             node_mapping[to_node] = new_to_node
#             to_node = new_to_node

#             # 更新 title 中的回溯目标节点信息
#             step["title"] = step["title"].replace(step_parts[1], new_to_node)

#         # 更新回溯之后的节点，如果节点已经被替换，应用相应的替换
#         if from_node in node_mapping:
#             from_node = node_mapping[from_node]
#         if to_node in node_mapping:
#             to_node = node_mapping[to_node]

#         # 更新树标签历史记录
#         node_history[from_node.split(",")[0]].append(from_node)
#         node_history[to_node.split(",")[0]].append(to_node)

#         # 更新当前步骤的 tree tag 和 step taken
#         step["tree tag"] = to_node
#         step["step taken"] = f"{from_node} -> {to_node}"
#         updated_steps.append(step)

#         # 同时更新后续步骤中的相关节点
#         for j in range(i + 1, len(steps)):
#             future_step = steps[j]
#             future_step_from = future_step["step taken"].split(" -> ")[0]
#             future_step_to = future_step["step taken"].split(" -> ")[1]

#             # 更新后续步骤中的 tree tag 和 step taken
#             if future_step_from in node_mapping:
#                 future_step_from = node_mapping[future_step_from]
#                 future_step["step taken"] = f"{future_step_from} -> {future_step_to}"
#             if future_step_to in node_mapping:
#                 future_step_to = node_mapping[future_step_to]
#                 future_step["step taken"] = f"{future_step_from} -> {future_step_to}"

#             # 更新 tree tag
#             if future_step["tree tag"] in node_mapping:
#                 future_step["tree tag"] = node_mapping[future_step["tree tag"]]

#             updated_steps.append(future_step)

#     return updated_steps

# def process_json_file(filename):
#     with open(filename, "r", encoding="utf-8") as file:
#         data = json.load(file)

#     for item in data:
#         item['steps'] = update_steps(item['steps'])

#     # 输出修改后的内容
#     output_file = f"/nas/shared/GAIR/yyliu/AI-Only-streamlit/data/result_gpt4o-v8_with-gold-answer_all-steps-processed.jsonl"
#     with open(output_file, "w", encoding="utf-8") as file:
#         json.dump(data, file, ensure_ascii=False, indent=4)
#     print(f"更新后的JSON文件已保存为 {output_file}")

# # 使用方法，传入json文件路径
# process_json_file("/nas/shared/GAIR/yyliu/AI-Only-streamlit/data/result_gpt4o-v8_with-gold-answer_all-steps.jsonl")



import streamlit as st
import graphviz
import json

# 设置页面配置为全宽模式
st.set_page_config(layout="wide")

# 从 JSON 文件中读取数据
with open('data/result_gpt4o-v8_with-gold-answer.jsonl', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('data/result_gpt4o-v8_with-gold-answer_all-steps.jsonl', 'r', encoding='utf-8') as f:
    data1 = json.load(f)

# Sidebar for image selection
selected_image_index = st.sidebar.selectbox("Select Image Number", range(1, len(data) + 1)) - 1

def insert_line_breaks_for_graphviz(text, line_length=30):
    words = text.split(' ')  # 按空格拆分为单词
    lines = []
    current_line = ""

    for word in words:
        # 如果当前行加上这个单词的长度超过了 line_length，就换行
        if len(current_line) + len(word) + 1 > line_length:  # +1 是为了空格
            lines.append(current_line.strip())  # 添加当前行，并去掉末尾多余的空格
            current_line = word  # 把当前单词放到新行
        else:
            # 否则将单词添加到当前行
            current_line += " " + word
    
    # 添加最后一行
    if current_line:
        lines.append(current_line.strip())

    # 用 \n 拼接所有行
    return '\n'.join(lines)

# 函数：生成 Graphviz 图
def generate_graph(question_data, show_full_text=False):
    dot = graphviz.Digraph()
    step_options = ['All Steps']  # 包含 "All Steps" 选项
    full_texts = []  # 用于存储完整的文本
    
    question_title = question_data['question']
    steps = question_data['steps']

    formatted_question_title = insert_line_breaks_for_graphviz(question_title, line_length=60)  # 30 是每行的字符数
    # 将格式化后的标题应用到 Graphviz 节点中
    dot.node(question_title, formatted_question_title)

    # 使用字典按层次存储节点，同时记录节点的唯一标识符
    layers = {}
    nodes_added = {}  # 记录已经添加的节点，key为tree tag, value为节点信息（包含tree tag和content的组合）

    # 添加步骤和边
    for i, step in enumerate(steps):
        content = step["content"]
        step_taken = step["step taken"].split(" -> ")
        tree_tag = step["tree tag"]
        layer = tree_tag.split(",")[0].strip('()')  # 获取第一项
        
        # 生成节点的唯一标识符，使用tree tag和content的组合
        node_id = step_taken[0] + "_" + content[:10]  # 可以根据需要调整唯一标识符生成规则
        display_content = content[:30] + '...' if not show_full_text else content
        
        # 如果节点尚未添加，或者内容不同，则创建新的节点
        if node_id not in nodes_added:
            nodes_added[node_id] = {
                "tree_tag": tree_tag,
                "content": content,
            }
            # 将节点按层次存储
            if layer not in layers:
                layers[layer] = []
            layers[layer].append((step_taken[0], step_taken[0] + '\n' + display_content))

        # 存储步骤和完整的文本用于后面展示
        step_options.append(f"Step {i}")  # 使用从 0 开始的 Step i 的格式
        full_texts.append((step_taken[0], content))

        # 添加边，连接上一个节点和当前节点
        if len(step_taken) > 1:
            parent_node_id = step_taken[1] + "_" + content[:10]  # 同样生成父节点的唯一标识符
            dot.edge(node_id, parent_node_id, label=str(i))

    # 为每一层添加子图
    for layer, nodes in layers.items():
        with dot.subgraph() as s:
            s.attr(rank='same')  # 设置为同一层
            for node, label in nodes:
                s.node(node, label)

    # 连接根节点和第一个步骤
    dot.edge(question_title, steps[0]["step taken"].split(" -> ")[0])
    
    return dot, step_options, full_texts

# 生成两组图，分别基于选中的问题
dots_data, step_options_data, full_texts_data = generate_graph(data[selected_image_index])
dots_data1, step_options_data1, full_texts_data1 = generate_graph(data1[selected_image_index])

# 页面布局：左侧展示 data，右侧展示 data1，设置列的比例，调整比例增加宽度
col1, col2 = st.columns([1.5, 1.5], gap="large")  # 使列宽更大

# 左侧选择要展示的步骤，默认为 "All Steps"
selected_step = st.sidebar.selectbox("Select Step from Graph 1", step_options_data, index=0)
selected_step1 = st.sidebar.selectbox("Select Step from Graph 2", step_options_data1, index=0)

# 左侧：展示简化的图和选定步骤的完整内容
with col1:
    st.header("Graph 1: Without Backtrace")
    # 使用大图宽度参数
    st.graphviz_chart(dots_data)

    # 展示选定步骤的完整文本
    if selected_step == 'All Steps':
        st.subheader("Full Text for All Steps")
        for i,(node, content) in enumerate(full_texts_data):
            st.markdown(f"**Step {i}**")
            st.write(content)
    else:
        step_index = int(selected_step.split()[-1])  # 从 "Step X" 中提取步骤索引，从 0 开始
        st.subheader(f"Full Text for {selected_step}")
        st.write(full_texts_data[step_index][1])

# 右侧：展示简化的图和选定步骤的完整内容
with col2:
    st.header("Graph 2: With Backtrace")
    # 使用大图宽度参数
    st.graphviz_chart(dots_data1)

    # 展示选定步骤的完整文本
    if selected_step1 == 'All Steps':
        st.subheader("Full Text for All Steps")
        for i,(node, content) in enumerate(full_texts_data1):
            st.markdown(f"**Step {i}**")
            st.write(content)
    else:
        step_index1 = int(selected_step1.split()[-1])  # 从 "Step X" 中提取步骤索引，从 0 开始
        st.subheader(f"Full Text for {selected_step1}")
        st.write(full_texts_data1[step_index1][1])
