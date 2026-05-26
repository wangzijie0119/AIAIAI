# app.py - 自动写实验报告智能体
import streamlit as st
import requests

# 页面配置
st.set_page_config(
    page_title="实验报告智能助手",
    page_icon="📝",
    layout="wide"
)

st.title("📝 自动写实验报告智能体")
st.markdown("---")

# 侧边栏
with st.sidebar:
    st.header("📌 使用说明")
    st.markdown("""
    1. 输入你的**实验名称**
    2. 填写**实验数据/现象**
    3. 选择**报告类型**
    4. 点击生成按钮
    
    **支持的报告类型：**
    - 理工科实验报告
    - 物理/化学/生物实验
    - 计算机/数据分析实验
    - 研究性学习报告
    """)

# 主界面
exp_name = st.text_input("📋 实验名称", placeholder="例如：探究光的折射规律")

exp_data = st.text_area(
    "🔬 实验数据/现象",
    placeholder="请描述你的实验过程、测得的数据...",
    height=150
)

report_type = st.selectbox(
    "📂 报告类型",
    ["理工科实验报告", "物理实验报告", "化学实验报告", "计算机实验报告"]
)

# 从 secrets 读取 API Key
api_key = st.secrets.get("DEEPSEEK_API_KEY", "")

def call_deepseek(exp_name, exp_data, report_type):
    """调用 DeepSeek API"""
    if not api_key:
        return "⚠️ 请先在 Streamlit Secrets 中配置 DEEPSEEK_API_KEY"
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""你是一个专业的实验报告写作助手。请根据以下信息，撰写一份完整的{report_type}。

实验名称：{exp_name}
实验数据/现象：{exp_data}

请按照以下结构输出：
## 一、实验目的
## 二、实验原理
## 三、实验步骤
## 四、实验数据记录
## 五、结果分析
## 六、实验结论

要求：内容专业、格式清晰。"""
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"API 错误: {response.status_code}"
    except Exception as e:
        return f"请求失败: {str(e)}"

# 生成按钮
if st.button("🚀 生成实验报告", type="primary"):
    if not exp_name:
        st.error("请填写实验名称")
    elif not exp_data:
        st.error("请填写实验数据")
    else:
        with st.spinner("AI 正在撰写..."):
            report = call_deepseek(exp_name, exp_data, report_type)
            st.markdown(report)

st.markdown("---")
st.caption("Powered by DeepSeek API")
