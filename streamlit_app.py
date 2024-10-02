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
        
        # 如果 show_full_text 为 False，只显示前30个字符
        display_content = content[:30] + '...' if not show_full_text else content
        
        layers[layer].append((step_taken[0], step_taken[0] + '\n' + display_content))

        # 存储步骤和完整的文本用于后面展示
        step_options.append(f"Step {i}")  # 使用从 0 开始的 Step i 的格式
        full_texts.append((step_taken[0], content))

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
    
    return dot, step_options, full_texts

# 生成两组图，分别基于选中的问题
dots_data, step_options_data, full_texts_data = generate_graph(data[selected_image_index])
dots_data1, step_options_data1, full_texts_data1 = generate_graph(data1[selected_image_index])

# 页面布局：左侧展示 data，右侧展示 data1，设置列的比例，调整比例增加宽度
col1, col2 = st.columns([1.5, 1.5], gap="large")  # 使列宽更大

# 左侧选择要展示的步骤，默认为 "All Steps"
selected_step = st.sidebar.selectbox("Select Step from Gragh 1", step_options_data, index=0)
selected_step1 = st.sidebar.selectbox("Select Step from Gragh 2", step_options_data1, index=0)

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
        st.subheader(f"Full Text for {selected_step1}"  )
        st.write(full_texts_data1[step_index1][1])


# import streamlit as st
# import graphviz
# import json

# # 设置页面配置为全宽模式
# st.set_page_config(layout="wide")

# # 从 JSON 文件中读取数据
# with open('data/result_gpt4o-v8_with-gold-answer.jsonl', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# with open('data/result_gpt4o-v8_with-gold-answer_all-steps.jsonl', 'r', encoding='utf-8') as f:
#     data1 = json.load(f)

# # Sidebar for image selection
# selected_image_index = st.sidebar.selectbox("Select Image Number", range(1, len(data) + 1)) - 1

# def insert_line_breaks_for_graphviz(text, line_length=30):
#     words = text.split(' ')
#     lines = []
#     current_line = ""

#     for word in words:
#         if len(current_line) + len(word) + 1 > line_length:
#             lines.append(current_line.strip())  # 添加当前行，并去掉末尾多余的空格
#             current_line = word  # 把当前单词放到新行
#         else:
#             current_line += " " + word  # 将单词添加到当前行
    
#     if current_line:
#         lines.append(current_line.strip())

#     return '\n'.join(lines)

# # 函数：生成 Graphviz 图
# def generate_graph(question_data, show_full_text=False):
#     dot = graphviz.Digraph()
#     step_options = ['All Steps']  # 包含 "All Steps" 选项
#     full_texts = []  # 用于存储完整的文本
    
#     question_title = question_data['question']
#     steps = question_data['steps']

#     formatted_question_title = insert_line_breaks_for_graphviz(question_title, line_length=60)
#     dot.node('question', formatted_question_title)  # 根节点用 'question' 作为标识符

#     # 使用字典按层次存储节点，同时记录节点的唯一标识符
#     nodes_added = {}  # 记录已经添加的节点，key为 tree tag 和内容hash组合
#     layers = {}  # 用于按 tree tag 层次存储节点
#     non_numeric_layers = []  # 记录非数字的 tree tag，例如 'END'

#     for i, step in enumerate(steps):
#         content = step["content"]
#         step_taken = step["step taken"].split(" -> ")
#         tree_tag = step["tree tag"]

#         # 当前步骤的起点节点标识符，使用 tree tag 和内容的 hash 值来唯一标识
#         node_id = f"{step_taken[0]}_{hash(content)}"

#         # 获取当前层次，尝试将 tree tag 的第一位转换为整数，若失败则处理为字符串层次
#         try:
#             layer = int(tree_tag.split(",")[0].strip('()'))
#         except ValueError:
#             layer = tree_tag  # 对于非数字的 tree tag，我们直接用字符串表示层次
#             if layer not in non_numeric_layers:
#                 non_numeric_layers.append(layer)  # 记录非数字的层次

#         # 如果层次不存在，初始化它
#         if layer not in layers:
#             layers[layer] = []

#         # 如果该节点尚未添加到图中，则添加
#         if node_id not in nodes_added:
#             nodes_added[node_id] = {
#                 "tree_tag": tree_tag,
#                 "content": content,
#             }
#             display_content = content[:30] + '...' if not show_full_text else content
#             dot.node(node_id, step_taken[0] + '\n' + insert_line_breaks_for_graphviz(display_content))
#             layers[layer].append(node_id)

#         # 处理下一个步骤的节点
#         if i < len(steps) - 1:
#             next_step = steps[i + 1]
#             next_content = next_step["content"]
#             next_tree_tag = next_step["tree tag"]
#             next_node_id = f"{step_taken[1]}_{hash(next_content)}"

#             # 确保目标节点与相同 tree tag 的节点放在同一层
#             try:
#                 next_layer = int(next_tree_tag.split(",")[0].strip('()'))
#             except ValueError:
#                 next_layer = next_tree_tag

#             # 如果 `tree tag` 相同但 `content` 不同，新建节点，并确保它与同层的节点放在一起
#             if next_node_id in nodes_added and nodes_added[next_node_id]["content"] != next_content:
#                 next_node_id = f"{step_taken[1]}_new_{i}"  # 创建新节点
#                 nodes_added[next_node_id] = {
#                     "tree_tag": next_tree_tag,
#                     "content": next_content,
#                 }
#                 display_content = next_content[:30] + '...' if not show_full_text else next_content
#                 dot.node(next_node_id, step_taken[1] + '\n' + insert_line_breaks_for_graphviz(display_content))

#                 # 确保层次已经初始化
#                 if next_layer not in layers:
#                     layers[next_layer] = []

#                 layers[next_layer].append(next_node_id)  # 确保新建的节点放在与相同 `tree tag` 的节点同一层

#             # 否则，正常处理节点和边的连接
#             if next_node_id not in nodes_added:
#                 nodes_added[next_node_id] = {
#                     "tree_tag": next_tree_tag,
#                     "content": next_content,
#                 }
#                 display_content = next_content[:30] + '...' if not show_full_text else next_content
#                 dot.node(next_node_id, step_taken[1] + '\n' + insert_line_breaks_for_graphviz(display_content))

#                 # 确保层次已经初始化
#                 if next_layer not in layers:
#                     layers[next_layer] = []

#                 layers[next_layer].append(next_node_id)

#             # 连接当前步骤到下一个步骤
#             dot.edge(node_id, next_node_id, label=f"Step {i}")
#         else:
#             # 处理最后一个节点
#             dot.node(node_id, step_taken[0] + '\n' + insert_line_breaks_for_graphviz(content[:30]))

#         # 存储步骤和完整的文本用于后面展示
#         step_options.append(f"Step {i}")
#         full_texts.append((step_taken[0], content))

#     # 将节点按层次排序，并确保同层的节点在同一水平
#     for layer in sorted([l for l in layers if isinstance(l, int)]):  # 数字层次优先排序
#         with dot.subgraph() as s:
#             s.attr(rank='same')  # 将相同 `tree tag` 的节点放置在同一层
#             for node_id in layers[layer]:
#                 s.node(node_id)

#     # 处理非数字的层次，如 'END' 等
#     for layer in non_numeric_layers:
#         with dot.subgraph() as s:
#             s.attr(rank='same')
#             for node_id in layers[layer]:
#                 s.node(node_id)

#     # 连接根节点和第一个步骤
#     first_step = steps[0]
#     first_node_id = f"{first_step['step taken'].split(' -> ')[0]}_{hash(first_step['content'])}"
#     dot.edge('question', first_node_id)

#     return dot, step_options, full_texts

# # 生成两组图，分别基于选中的问题
# dots_data, step_options_data, full_texts_data = generate_graph(data[selected_image_index])
# dots_data1, step_options_data1, full_texts_data1 = generate_graph(data1[selected_image_index])

# # 页面布局：左侧展示 data，右侧展示 data1，设置列的比例，调整比例增加宽度
# col1, col2 = st.columns([1.5, 1.5], gap="large")

# # 左侧选择要展示的步骤，默认为 "All Steps"
# selected_step = st.sidebar.selectbox("Select Step from Graph 1", step_options_data, index=0)
# selected_step1 = st.sidebar.selectbox("Select Step from Graph 2", step_options_data1, index=0)

# # 左侧：展示简化的图和选定步骤的完整内容
# with col1:
#     st.header("Graph 1: Without Backtrace")
#     st.graphviz_chart(dots_data)

#     if selected_step == 'All Steps':
#         st.subheader("Full Text for All Steps")
#         for i, (node, content) in enumerate(full_texts_data):
#             st.markdown(f"**Step {i}**")
#             st.write(content)
#     else:
#         step_index = int(selected_step.split()[-1])
#         st.subheader(f"Full Text for {selected_step}")
#         st.write(full_texts_data[step_index][1])

# # 右侧：展示简化的图和选定步骤的完整内容
# with col2:
#     st.header("Graph 2: With Backtrace")
#     st.graphviz_chart(dots_data1)

#     if selected_step1 == 'All Steps':
#         st.subheader("Full Text for All Steps")
#         for i, (node, content) in enumerate(full_texts_data1):
#             st.markdown(f"**Step {i}**")
#             st.write(content)
#     else:
#         step_index1 = int(selected_step1.split()[-1])
#         st.subheader(f"Full Text for {selected_step1}")
#         st.write(full_texts_data1[step_index1][1])



# import streamlit as st
# import graphviz
# import json

# # 设置页面配置为全宽模式
# st.set_page_config(layout="wide")

# # 从 JSON 文件中读取数据
# with open('data/result_gpt4o-v8_with-gold-answer.jsonl', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# with open('data/result_gpt4o-v8_with-gold-answer_all-steps.jsonl', 'r', encoding='utf-8') as f:
#     data1 = json.load(f)

# # Sidebar for image selection
# selected_image_index = st.sidebar.selectbox("Select Image Number", range(1, len(data) + 1)) - 1

# def insert_line_breaks_for_graphviz(text, line_length=30):
#     words = text.split(' ')
#     lines = []
#     current_line = ""

#     for word in words:
#         if len(current_line) + len(word) + 1 > line_length:
#             lines.append(current_line.strip())  # 添加当前行，并去掉末尾多余的空格
#             current_line = word  # 把当前单词放到新行
#         else:
#             current_line += " " + word  # 将单词添加到当前行
    
#     if current_line:
#         lines.append(current_line.strip())

#     return '\n'.join(lines)

# # 函数：生成 Graphviz 图
# def generate_graph(question_data, show_full_text=False):
#     dot = graphviz.Digraph()
#     step_options = ['All Steps']  # 包含 "All Steps" 选项
#     full_texts = []  # 用于存储完整的文本
    
#     question_title = question_data['question']
#     steps = question_data['steps']

#     formatted_question_title = insert_line_breaks_for_graphviz(question_title, line_length=60)
#     dot.node('question', formatted_question_title)  # 根节点用 'question' 作为标识符

#     # 使用字典按层次存储节点，同时记录节点的唯一标识符
#     nodes_added = {}  # 记录已经添加的节点，key为 tree tag 和内容hash组合
#     layers = {}  # 用于按 tree tag 层次存储节点
#     non_numeric_layers = []  # 记录非数字的 tree tag，例如 'END'

#     for i, step in enumerate(steps):
#         content = step["content"]
#         step_taken = step["step taken"].split(" -> ")
#         decision = step.get("decision", "")  # 获取 "decision"，如果没有则默认为空字符串
#         tree_tag = step["tree tag"]

#         # 当前步骤的起点节点标识符，使用 tree tag 和内容的 hash 值来唯一标识
#         node_id = f"{step_taken[0]}_{hash(content)}"

#         # 获取当前层次，尝试将 tree tag 的第一位转换为整数，若失败则处理为字符串层次
#         try:
#             layer = int(tree_tag.split(",")[0].strip('()'))
#         except ValueError:
#             layer = tree_tag  # 对于非数字的 tree tag，我们直接用字符串表示层次
#             if layer not in non_numeric_layers:
#                 non_numeric_layers.append(layer)  # 记录非数字的层次

#         # 如果层次不存在，初始化它
#         if layer not in layers:
#             layers[layer] = []

#         # 如果该节点尚未添加到图中，则添加
#         if node_id not in nodes_added:
#             nodes_added[node_id] = {
#                 "tree_tag": tree_tag,
#                 "content": content,
#             }
#             display_content = content[:30] + '...' if not show_full_text else content
#             dot.node(node_id, step_taken[0] + '\n' + insert_line_breaks_for_graphviz(display_content))
#             layers[layer].append(node_id)

#         # 判断是否为 "Check" 决策，如果是，创建自环边
#         if decision == "Check":
#             # 创建一条边指向自身，并显示当前的步骤编号
#             dot.edge(node_id, node_id, label=f"Step {i}")
#         else:
#             # 处理下一个步骤的节点
#             if i < len(steps) - 1:
#                 next_step = steps[i + 1]
#                 next_content = next_step["content"]
#                 next_tree_tag = next_step["tree tag"]
#                 next_node_id = f"{step_taken[1]}_{hash(next_content)}"

#                 # 确保目标节点与相同 tree tag 的节点放在同一层
#                 try:
#                     next_layer = int(next_tree_tag.split(",")[0].strip('()'))
#                 except ValueError:
#                     next_layer = next_tree_tag

#                 # 如果 `tree tag` 相同但 `content` 不同，新建节点，并确保它与同层的节点放在一起
#                 if next_node_id in nodes_added and nodes_added[next_node_id]["content"] != next_content:
#                     next_node_id = f"{step_taken[1]}_new_{i}"  # 创建新节点
#                     nodes_added[next_node_id] = {
#                         "tree_tag": next_tree_tag,
#                         "content": next_content,
#                     }
#                     display_content = next_content[:30] + '...' if not show_full_text else next_content
#                     dot.node(next_node_id, step_taken[1] + '\n' + insert_line_breaks_for_graphviz(display_content))

#                     # 确保层次已经初始化
#                     if next_layer not in layers:
#                         layers[next_layer] = []

#                     layers[next_layer].append(next_node_id)  # 确保新建的节点放在与相同 `tree tag` 的节点同一层

#                 # 否则，正常处理节点和边的连接
#                 if next_node_id not in nodes_added:
#                     nodes_added[next_node_id] = {
#                         "tree_tag": next_tree_tag,
#                         "content": next_content,
#                     }
#                     display_content = next_content[:30] + '...' if not show_full_text else next_content
#                     dot.node(next_node_id, step_taken[1] + '\n' + insert_line_breaks_for_graphviz(display_content))

#                     # 确保层次已经初始化
#                     if next_layer not in layers:
#                         layers[next_layer] = []

#                     layers[next_layer].append(next_node_id)

#                 # 连接当前步骤到下一个步骤
#                 dot.edge(node_id, next_node_id, label=f"Step {i}")
#             else:
#                 # 处理最后一个节点
#                 dot.node(node_id, step_taken[0] + '\n' + insert_line_breaks_for_graphviz(content[:30]))

#         # 存储步骤和完整的文本用于后面展示
#         step_options.append(f"Step {i}")
#         full_texts.append((step_taken[0], content))

#     # 将节点按层次排序，并确保同层的节点在同一水平
#     for layer in sorted([l for l in layers if isinstance(l, int)]):  # 数字层次优先排序
#         with dot.subgraph() as s:
#             s.attr(rank='same')  # 将相同 `tree tag` 的节点放置在同一层
#             for node_id in layers[layer]:
#                 s.node(node_id)

#     # 处理非数字的层次，如 'END' 等
#     for layer in non_numeric_layers:
#         with dot.subgraph() as s:
#             s.attr(rank='same')
#             for node_id in layers[layer]:
#                 s.node(node_id)

#     # 连接根节点和第一个步骤
#     first_step = steps[0]
#     first_node_id = f"{first_step['step taken'].split(' -> ')[0]}_{hash(first_step['content'])}"
#     dot.edge('question', first_node_id)

#     return dot, step_options, full_texts

# # 生成两组图，分别基于选中的问题
# dots_data, step_options_data, full_texts_data = generate_graph(data[selected_image_index])
# dots_data1, step_options_data1, full_texts_data1 = generate_graph(data1[selected_image_index])

# # 页面布局：左侧展示 data，右侧展示 data1，设置列的比例，调整比例增加宽度
# col1, col2 = st.columns([1.5, 1.5], gap="large")

# # 左侧选择要展示的步骤，默认为 "All Steps"
# selected_step = st.sidebar.selectbox("Select Step from Graph 1", step_options_data, index=0)
# selected_step1 = st.sidebar.selectbox("Select Step from Graph 2", step_options_data1, index=0)

# # 左侧：展示简化的图和选定步骤的完整内容
# with col1:
#     st.header("Graph 1: Without Backtrace")
#     st.graphviz_chart(dots_data)

#     if selected_step == 'All Steps':
#         st.subheader("Full Text for All Steps")
#         for i, (node, content) in enumerate(full_texts_data):
#             st.markdown(f"**Step {i}**")
#             st.write(content)
#     else:
#         step_index = int(selected_step.split()[-1])
#         st.subheader(f"Full Text for {selected_step}")
#         st.write(full_texts_data[step_index][1])

# # 右侧：展示简化的图和选定步骤的完整内容
# with col2:
#     st.header("Graph 2: With Backtrace")
#     st.graphviz_chart(dots_data1)

#     if selected_step1 == 'All Steps':
#         st.subheader("Full Text for All Steps")
#         for i, (node, content) in enumerate(full_texts_data1):
#             st.markdown(f"**Step {i}**")
#             st.write(content)
#     else:
#         step_index1 = int(selected_step1.split()[-1])
#         st.subheader(f"Full Text for {selected_step1}")
#         st.write(full_texts_data1[step_index1][1])


