import json
import re
from pathlib import Path

def save_BSid(QQ_id, message,data_dir):
    # 简单粗暴提取数字
    id_list = re.findall(r'\d+', message)
    if not id_list:
        # 用于应对id不是纯数字的童鞋
        message.replace('BS查歌', '').replace('BS search', '').replace('节奏光剑查歌', '').strip()
        special_id = message.replace('BS绑定', '').replace('节奏光剑绑定', '').replace('BS bind', '').strip()
        BS_id = special_id
    else:
        BS_id = id_list[0]

    json_file_path = Path(f'{data_dir}/BSgroup.json')
    # 检查是否存在json文件
    if json_file_path.exists():
        with open(json_file_path, 'r', encoding='utf-8') as f:
            groud_data = json.load(f)
    else:
        groud_data = {}

    groud_data[QQ_id] = BS_id
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(groud_data, f, sort_keys=True, indent=4, ensure_ascii=False)

    # 尝试读取文件
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            QQ_data = json.load(f)
    except FileNotFoundError:
        QQ_data = {}

    # 检查是否成功写入
    if QQ_id not in QQ_data or QQ_data[QQ_id] != BS_id:
        return 810
    else:
        msg = f'QQ号: {QQ_id} 已绑定 BeatLeaderID: {BS_id} ヾ(*´▽‘*)ﾉ'
        return msg
    
def save_user_data(QQ_id,data_dir,scores_data = None):

    user_data_path = Path(f'{data_dir}/{QQ_id}.json')
    if user_data_path.exists():
        with open(user_data_path, 'r', encoding='utf-8') as f:
            song_data = json.load(f)
    else:
        song_data = {}
    
    if scores_data == None:
        return ##############
    song_data['id_data'] = scores_data['song_id']
    song_data['pp_data'] = scores_data['song_pp']

    with open(user_data_path, 'w', encoding='utf-8') as f:
        json.dump(song_data, f, sort_keys=True, indent=4, ensure_ascii=False)

    try:
        with open(user_data_path, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
    except FileNotFoundError:
        return None
    
    return 

