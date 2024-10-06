def contrast(new_id_data,new_pp_data,old_id_data,old_pp_data):
    statistics = []
    for old_id in old_id_data:
        # 判断旧数据在新数据中是否存在
        if old_id in new_id_data:
            for new_id in range(len(new_id_data)):
                # 判断旧数据的歌是否还存在新数据
                if new_id_data[new_id] == old_id: # old_id去遍历新数据,如果存在就记录这首歌之前的位置
                    statistics.append(new_id)
                else:
                    pass
        else:
            pass
    contrast = []
    # 列出新数据的歌曲总数目
    for number in range(len(new_id_data)):
        contrast.append(number)
    # 提取变化新歌曲位置数目
    record = list(set(contrast) - set(statistics))
    return record

def calculate_position(record,start_x_offset,start_y_position,change):
    if record == 0:
        position = (start_x_offset, start_y_position)
        return position
    else:
        pass
    i = 1
    x_change = start_x_offset
    y_change = start_y_position
    while record >= i:
        i += 1
        x_change += change + 100
        if x_change > 3600:
            x_change = start_x_offset
            y_change +=  650
        else:
            pass
    position = (x_change, y_change)
    return position