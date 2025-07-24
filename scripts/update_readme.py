# scripts/update_readme.py
import yaml
from pathlib import Path
import re

# --- 配置 ---
DATA_FILE = "challenges.yml"
TEMPLATE_FILE = "README.template.md"
OUTPUT_FILE = "README.md" # 我们将直接覆盖这个文件

# ... (之前脚本里的 STATUS_MAP 和 PENDING_SYMBOL 定义可以复制过来)
STATUS_MAP = {
    "✅": ("🟢", "brightgreen"), "❌": ("🔴", "red"), "🥱": ("🟡", "yellow"),
}
PENDING_SYMBOL = "⚪️"

def get_progress(challenge):
    """读取日志文件，计算进度"""
    log_path = Path(challenge['log_path'])
    if not log_path.exists():
        return 0
    log_content = log_path.read_text(encoding='utf-8')
    return len(re.findall(r"##\s+Day\s+\d+", log_content))

def create_badge(progress, total_days):
    """根据进度创建徽章 URL"""
    # (这里可以把之前脚本里拼接徽章URL的逻辑搬过来)
    completed_symbols = "🟢" * progress
    pending_symbols = PENDING_SYMBOL * (total_days - progress)
    badge_text = f"Day%20{progress}%2F{total_days}"
    return f"https://img.shields.io/badge/{completed_symbols}{pending_symbols}-{badge_text}-lightgrey?labelColor=lightgrey"

def generate_challenge_markdown(challenge):
    """为单个挑战生成 Markdown 文本块"""
    progress = get_progress(challenge)
    total_days = challenge['total_days']
    badge_url = create_badge(progress, total_days)

    return f"""
### {challenge['name']}
* 进度: ![{challenge['name']} Progress]({badge_url})
* 日志: [➡️ 查看日志]({challenge['log_path']})
* 看板: [➡️ 前往任务看板]({challenge['project_url']})
"""

# --- 主逻辑 ---
print("--- Starting README generation based on data model. ---")

# 1. 读取数据和模板
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    challenges = yaml.safe_load(f)

template_content = Path(TEMPLATE_FILE).read_text(encoding='utf-8')

# 2. 按状态分类并生成 Markdown
ongoing_md = ""
planned_md = ""
completed_md = ""

for c in challenges:
    if c['status'] == 'ongoing':
        ongoing_md += generate_challenge_markdown(c)
    elif c['status'] == 'planned':
        planned_md += f"- [ ] {c['name']}\n"
    elif c['status'] == 'completed':
        completed_md += f"- ✅ {c['name']} - [查看日志]({c['log_path']})\n"

# 3. 替换模板中的占位符
output_content = template_content.replace("{{ONGOING_CHALLENGES}}", ongoing_md)
output_content = output_content.replace("{{PLANNED_CHALLENGES}}", planned_md)
output_content = output_content.replace("{{COMPLETED_CHALLENGES}}", completed_md)

# 4. 写入最终的 README.md 文件
Path(OUTPUT_FILE).write_text(output_content, encoding='utf-8')
print(f"--- Successfully generated {OUTPUT_FILE}. ---")