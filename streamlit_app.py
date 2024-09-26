# import streamlit as st
# import os
# from PIL import Image
# import graphviz
# import json

# # 从 JSON 文件中读取数据
# with open('data/result_gpt4o-v8_with-gold-answer.jsonl', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# with open('data/result_gpt4o-v8_with-gold-answer_all-steps.jsonl', 'r', encoding='utf-8') as f:
#     data1 = json.load(f)



# # Sidebar for image selection
# selected_image_index = st.sidebar.selectbox("Select Image Number", range(1, len(data) + 1)) - 1

# dots=[]

# for j,question in enumerate(data):
#     question_title = question['question']
#     steps = question['steps']

#     dot = graphviz.Digraph()

#     # 添加问题作为根节点
#     dot.node(question_title, question_title)

#     # 使用字典按层次存储节点
#     layers = {}

#     # 添加步骤和边
#     for i, step in enumerate(steps):
#         content = step["content"]
#         step_taken = step["step taken"].split(" -> ")
#         layer = step["tree tag"].split(",")[0].strip('()')  # 获取第一项

#         # 将节点按层次存储
#         if layer not in layers:
#             layers[layer] = []
#         layers[layer].append((step_taken[0], step_taken[0]+'\n'+content[:30] + '...'))

#         # 添加边
#         if len(step_taken) > 1:
#             dot.edge(step_taken[0], step_taken[1], label=str(i))

#     # 为每一层添加子图
#     for layer, nodes in layers.items():
#         with dot.subgraph() as s:
#             s.attr(rank='same')  # 设置为同一层
#             for node, label in nodes:
#                 s.node(node, label)

#     # 连接根节点和第一个步骤
#     dot.edge(question_title, steps[0]["step taken"].split(" -> ")[0])
#     dots.append(dot)

#     # 渲染并保存图像
#     #dot.render(f'/nas/shared/GAIR/yyliu/Thought_plus/teacher_only/graph/v8_with-gold-solution/flowchart_{j+1}', format='json', cleanup=True)
#     # st.graphviz_chart(dot)
# st.graphviz_chart(dots[selected_image_index])


# import streamlit as st
# import os
# from PIL import Image
# import graphviz
# import json

# # 从 JSON 文件中读取数据
# with open('data/result_gpt4o-v8_with-gold-answer.jsonl', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# with open('data/result_gpt4o-v8_with-gold-answer_all-steps.jsonl', 'r', encoding='utf-8') as f:
#     data1 = json.load(f)

# # Sidebar for image selection
# selected_image_index = st.sidebar.selectbox("Select Image Number", range(1, len(data) + 1)) - 1

# # 函数：生成 Graphviz 图
# def generate_graph(data):
#     dots = []
#     for j, question in enumerate(data):
#         question_title = question['question']
#         steps = question['steps']

#         dot = graphviz.Digraph()

#         # 添加问题作为根节点
#         dot.node(question_title, question_title)

#         # 使用字典按层次存储节点
#         layers = {}

#         # 添加步骤和边
#         for i, step in enumerate(steps):
#             content = step["content"]
#             step_taken = step["step taken"].split(" -> ")
#             layer = step["tree tag"].split(",")[0].strip('()')  # 获取第一项

#             # 将节点按层次存储
#             if layer not in layers:
#                 layers[layer] = []
#             layers[layer].append((step_taken[0], step_taken[0] + '\n' + content[:30] + '...'))

#             # 添加边
#             if len(step_taken) > 1:
#                 dot.edge(step_taken[0], step_taken[1], label=str(i))

#         # 为每一层添加子图
#         for layer, nodes in layers.items():
#             with dot.subgraph() as s:
#                 s.attr(rank='same')  # 设置为同一层
#                 for node, label in nodes:
#                     s.node(node, label)

#         # 连接根节点和第一个步骤
#         dot.edge(question_title, steps[0]["step taken"].split(" -> ")[0])
#         dots.append(dot)
#     return dots

# # 分别生成两组图
# dots_data = generate_graph(data)
# dots_data1 = generate_graph(data1)


# # 页面布局：左侧展示 data，右侧展示 data1，设置列的比例
# col1, col2 = st.columns([1, 1], gap="large")  # 使用相同宽度的两列

# with col1:
#     st.header("Without Backtrace")
#     # 使用大图宽度参数
#     st.graphviz_chart(dots_data[selected_image_index])  # 调整图表的大小

# with col2:
#     st.header("With Backtrace")
#     # 使用大图宽度参数
#     st.graphviz_chart(dots_data1[selected_image_index])  # 调整图表的大小


# import streamlit as st
# import graphviz
# import json
# st.set_page_config(layout="wide")
# # 从 JSON 文件中读取数据
# with open('data/result_gpt4o-v8_with-gold-answer.jsonl', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# with open('data/result_gpt4o-v8_with-gold-answer_all-steps.jsonl', 'r', encoding='utf-8') as f:
#     data1 = json.load(f)

# # Sidebar for image selection
# selected_image_index = st.sidebar.selectbox("Select Image Number", range(1, len(data) + 1)) - 1

# # 函数：生成 Graphviz 图
# def generate_graph(data, show_full_text=False):
#     dots = []
#     node_options = []
#     full_texts = []  # 用于存储完整的文本
#     for j, question in enumerate(data):
#         question_title = question['question']
#         steps = question['steps']

#         dot = graphviz.Digraph()

#         # 添加问题作为根节点
#         dot.node(question_title, question_title)

#         # 使用字典按层次存储节点
#         layers = {}

#         # 添加步骤和边
#         for i, step in enumerate(steps):
#             content = step["content"]
#             step_taken = step["step taken"].split(" -> ")
#             layer = step["tree tag"].split(",")[0].strip('()')  # 获取第一项

#             # 将节点按层次存储
#             if layer not in layers:
#                 layers[layer] = []
            
#             # 如果 show_full_text 为 False，只显示前30个字符
#             display_content = content[:30] + '...' if not show_full_text else content
            
#             layers[layer].append((step_taken[0], step_taken[0] + '\n' + display_content))

#             # 存储节点和完整的文本用于后面展示
#             node_options.append(step_taken[0])
#             full_texts.append((step_taken[0], content))

#             # 添加边
#             if len(step_taken) > 1:
#                 dot.edge(step_taken[0], step_taken[1], label=str(i))

#         # 为每一层添加子图
#         for layer, nodes in layers.items():
#             with dot.subgraph() as s:
#                 s.attr(rank='same')  # 设置为同一层
#                 for node, label in nodes:
#                     s.node(node, label)

#         # 连接根节点和第一个步骤
#         dot.edge(question_title, steps[0]["step taken"].split(" -> ")[0])
#         dots.append(dot)

#     return dots, node_options, full_texts

# # 分别生成两组图
# dots_data, node_options_data, full_texts_data = generate_graph(data)
# dots_data1, node_options_data1, full_texts_data1 = generate_graph(data1)

# # 页面布局：左侧展示 data，右侧展示 data1，设置列的比例
# col1, col2 = st.columns([1, 1], gap="large")  # 使用相同宽度的两列

# # 选择要展示的节点
# selected_node = st.sidebar.selectbox("Select Node from Data", node_options_data)
# selected_node1 = st.sidebar.selectbox("Select Node from Data1", node_options_data1)

# # 左侧：展示简化的图和选定节点的完整内容
# with col1:
#     st.header("Data Graph")
#     # 使用大图宽度参数
#     st.graphviz_chart(dots_data[selected_image_index])

#     # 展示选定节点的完整文本
#     st.subheader(f"Full Text for Selected Node: {selected_node}")
#     for node, content in full_texts_data:
#         if node == selected_node:
#             st.write(content)

# # 右侧：展示简化的图和选定节点的完整内容
# with col2:
#     st.header("Data1 Graph")
#     # 使用大图宽度参数
#     st.graphviz_chart(dots_data1[selected_image_index])

#     # 展示选定节点的完整文本
#     st.subheader(f"Full Text for Selected Node: {selected_node1}")
#     for node, content in full_texts_data1:
#         if node == selected_node1:
#             st.write(content)




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
        st.subheader(f"Full Text for {selected_step1}")
        st.write(full_texts_data1[step_index1][1])


