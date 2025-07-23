import re
from pathlib import Path

# --- 配置区 ---
LOG_FILE_PATH = "challenges/01_7-day-declutter/LOG.md"
README_PATH = "README.md"
CHALLENGE_TOTAL_DAYS = 7
PROGRESS_BAR_MARKER = ""

# 定义不同状态对应的方块和徽章颜色
STATUS_MAP = {
    "✅": ("🟢", "brightgreen"), # 成功 -> 绿色圆
    "❌": ("🔴", "red"),       # 失败 -> 红色圆
    "‍🤔": ("🟡", "yellow"),    # 跳过 -> 黄色圆
}
PENDING_SYMBOL = "⚪️"

# --- 脚本主逻辑 ---
print("--- Starting smart progress update script. ---")

# 1. 读取日志并解析状态
log_content = Path(LOG_FILE_PATH).read_text(encoding='utf-8')
day_blocks_statuses = re.findall(r"##\s+Day\s+\d+.*?状态:.*?(\S+)", log_content, re.DOTALL)

days_logged = len(day_blocks_statuses)
print(f"Found {days_logged} logged days.")

# 2. 生成进度条符号
progress_symbols = [STATUS_MAP.get(status, (PENDING_SYMBOL, "lightgrey"))[0] for status in day_blocks_statuses]
progress_symbols.extend([PENDING_SYMBOL] * (CHALLENGE_TOTAL_DAYS - days_logged))
progress_blocks_str = "".join(progress_symbols)

# 3. 生成新的徽章
# 找到最后一个有效状态的颜色作为徽章主色调
last_status_color = STATUS_MAP.get(day_blocks_statuses[-1], (None, "lightgrey"))[1] if day_blocks_statuses else "lightgrey"
badge_text = f"Day%20{days_logged}%2F{CHALLENGE_TOTAL_DAYS}"

label_bg_color = "white" #左侧底色
new_badge_url = f"https://img.shields.io/badge/{progress_blocks_str}-{badge_text}-{last_status_color}?labelColor={label_bg_color}"
new_progress_bar_md = f"![Challenge Progress]({new_badge_url})"

# 4. 更新 README.md
readme_content = Path(README_PATH).read_text(encoding='utf-8')
# 使用正则表达式找到标记和它下面的旧图片链接，并替换它们
new_readme_content = re.sub(
    f"({re.escape(PROGRESS_BAR_MARKER)}\s*?\n)!\[Challenge Progress\].*",
    f"\\1{new_progress_bar_md}",
    readme_content
)
Path(README_PATH).write_text(new_readme_content, encoding='utf-8')
print("--- README.md updated successfully. ---")