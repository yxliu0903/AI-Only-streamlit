import streamlit as st
import os
from PIL import Image
import graphviz
import json

# 从 JSON 文件中读取数据
with open('/nas/shared/GAIR/yyliu/Thought_plus/teacher_only/result_gpt4o-v8_with-gold-answer_all-steps.jsonl', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define the paths to the image folders
folder1 = 'data/graph/v8_with-gold-solution'
folder2 = 'data/graph/v8_with-gold-solution_cleaned'

# Get a list of images from each folder
images_folder1 = sorted([f for f in os.listdir(folder1) if f.endswith(('.png', '.jpg', '.jpeg'))])
images_folder2 = sorted([f for f in os.listdir(folder2) if f.endswith(('.png', '.jpg', '.jpeg'))])

# Ensure both folders have the same number of images
assert len(images_folder1) == len(images_folder2), "Both folders must contain the same number of images."

# Sidebar for image selection
selected_image_index = st.sidebar.selectbox("Select Image Number", range(1, len(images_folder1) + 1)) - 1

# Load and display the selected images
image1 = Image.open(os.path.join(folder1, images_folder1[selected_image_index]))
image2 = Image.open(os.path.join(folder2, images_folder2[selected_image_index]))

# Display images side by side
col1, col2 = st.columns(2)

with col1:
    st.image(image1, caption=f"Image from Folder 1: {images_folder1[selected_image_index]}", use_column_width=True)

with col2:
    st.image(image2, caption=f"Image from Folder 2: {images_folder2[selected_image_index]}", use_column_width=True)

dots=[]

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
    dots.append(dot)

    # 渲染并保存图像
    #dot.render(f'/nas/shared/GAIR/yyliu/Thought_plus/teacher_only/graph/v8_with-gold-solution/flowchart_{j+1}', format='json', cleanup=True)
    # st.graphviz_chart(dot)
st.graphviz_chart(dots[selected_image_index])
