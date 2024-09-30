import json
import re
from pathlib import Path

def save_BSid(QQ_id, message,data_dir):
    # 简单粗暴提取数字
    id_list = re.findall(r'\d+', message)
    if not id_list:
        # 用于应对id不是纯数字的童鞋
        special_id = message.replace('BS绑定', '').strip()
        BS_id = special_id
    else:
        BS_id = id_list[0]

    json_file_path = Path(f'{data_dir}/BSgroup.json')
    # 检查是否存在json文件
    if json_file_path.exists():
        with open(json_file_path, 'r', encoding='utf-8') as f:
            Groud_data = json.load(f)
    else:
        Groud_data = {}

    Groud_data[QQ_id] = BS_id
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(Groud_data, f, sort_keys=True, indent=4, ensure_ascii=False)

    # 尝试读取文件
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    # 检查是否成功写入
    if QQ_id not in data or data[QQ_id] != BS_id:
        return 810
    else:
        msg = f'QQ号: {QQ_id} 已绑定 BeatLeaderID: {BS_id} ヾ(*´▽‘*)ﾉ'
        return msg