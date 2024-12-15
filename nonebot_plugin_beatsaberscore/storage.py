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
        with open(json_file_path, 'r', encoding='utf-8') as test:
            groud_data = json.load(test)
    else:
        groud_data = {}

    groud_data[QQ_id] = BS_id
    with open(json_file_path, 'w', encoding='utf-8') as QQ_list:
        json.dump(groud_data, QQ_list, sort_keys=True, indent=4, ensure_ascii=False)

    # 尝试读取文件
    try:
        with open(json_file_path, 'r', encoding='utf-8') as QQ_list:
            QQ_data = json.load(QQ_list)
    except:
        QQ_data = {}

    # 检查是否成功写入
    if QQ_id not in QQ_data or QQ_data[QQ_id] != BS_id:
        return 810
    else:
        msg = f'QQ号: {QQ_id} 已绑定SteamID: {BS_id} ヾ(*´▽‘*)ﾉ'
        return msg
    
def save_user_data(QQ_id,data_dir,datas,SS = False):
    if datas == None:
        return None
    else:
        pass
    user_data_path = Path(f'{data_dir}/{QQ_id}.json')
     # 尝试打开文件,测试是否有文件
    try:
        with open(user_data_path, 'r', encoding='utf-8') as test:
            all_song_data = json.load(test)
    except:
        # 如果没有文件,则初始化文件数据
        all_song_data = {}
        with open(user_data_path, 'w', encoding='utf-8') as test:
            json.dump(all_song_data, test, sort_keys=True, indent=4, ensure_ascii=False)
    if SS == False:
        all_song_data['BL_data'] = {}
        all_song_data['BL_data'].update(datas)
        with open(user_data_path, 'w', encoding='utf-8') as scores:
            json.dump(all_song_data, scores, sort_keys=True, indent=4, ensure_ascii=False)
        return
    else:
        all_song_data['SS_data'] = {}
        all_song_data['SS_data'].update(datas)
        with open(user_data_path, 'w', encoding='utf-8') as scores:
            json.dump(all_song_data, scores, sort_keys=True, indent=4, ensure_ascii=False)
        return

def cache_data(save_id,data_path):
    cache_file_path = Path(f'{data_path}/cache_data.json')
    # 记录各个图片使用的次数
    if cache_file_path.exists():
        with open(cache_file_path, 'r', encoding='utf-8') as use_list:
            cache_data = json.load(use_list)
    else:
        cache_data = {}
        with open(cache_file_path, 'w', encoding='utf-8') as use_list:
            json.dump(cache_data, use_list, sort_keys=True, indent=4, ensure_ascii=False)
    try:
        cache_num = int(cache_data[save_id]) + 1
    except:
        cache_num = int(1)
    cache_data.update({f'{save_id}': cache_num})
    with open(cache_file_path, 'w', encoding='utf-8') as use_list:
        json.dump(cache_data, use_list, sort_keys=True, indent=4, ensure_ascii=False)
    return

    