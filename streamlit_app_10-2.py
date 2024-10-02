import streamlit as st
import graphviz
import json

# 设置页面配置为全宽模式
st.set_page_config(layout="wide")

# 从 JSON 文件中读取数据
with open('/nas/shared/GAIR/yyliu/Thought_plus/teacher_only/result_gpt4o-v9_with-gold-answer_all-steps.jsonl', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Sidebar for question selection
selected_image_index = st.sidebar.selectbox("Select Question", range(1, len(data) + 1)) - 1

def insert_line_breaks_for_graphviz(text, line_length=30):
    words = text.split(' ')  # 按空格拆分为单词
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 > line_length:
            lines.append(current_line.strip())
            current_line = word
        else:
            current_line += " " + word
    
    if current_line:
        lines.append(current_line.strip())
    
    return '\n'.join(lines)

# 函数：生成 Graphviz 图
def generate_graph(question_data, show_full_text=False):
    dot = graphviz.Digraph()
    
    question_title = question_data['question']
    steps = question_data['steps']

    formatted_question_title = insert_line_breaks_for_graphviz(question_title, line_length=60)
    dot.node('question', formatted_question_title)

    step_nodes = {}  # 用来存储每个步骤的节点信息

    # 添加步骤和边
    for i, step in enumerate(steps):
        step_number = step["number"]
        step_type = step["type"]
        content = step["content"]
        display_content = content[:30] + '...' if not show_full_text else content

        # 为每个步骤创建唯一标识符，即使 step_number 相同，content 不同也会被区别开
        step_id = f"step_{step_number}_{i}"
        step_nodes[(step_number, i)] = step_id

        # 将 number, type, content 都显示在节点上
        node_label = f"Step {step_number}\nType: {step_type}\n{display_content}"
        dot.node(step_id, node_label)

        # 连接步骤
        if step_number == 1:
            dot.edge('question', step_id)  # 第一个步骤连接到根节点
        else:
            # 寻找上一个 number 为 n-1 的步骤节点
            prev_step_id = None
            for j in range(i-1, -1, -1):
                if steps[j]["number"] == step_number - 1:
                    prev_step_id = step_nodes.get((steps[j]["number"], j))
                    break
            if prev_step_id:
                dot.edge(prev_step_id, step_id)  # 连接到最近的 number 为 n-1 的步骤

    return dot

# 生成图基于选中的问题
dots_data = generate_graph(data[selected_image_index])

# 页面布局展示图
st.header("Step-by-Step Graph")
st.graphviz_chart(dots_data)
