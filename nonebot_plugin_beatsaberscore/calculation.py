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

def calculate_position(record,start_x_offset = 170,start_y_position = 1750,change = 0):
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
        x_change += change + 65
        if x_change > 3600:
            x_change = start_x_offset
            y_change += 550
        else:
            pass
    position = (x_change, y_change)
    return position

def calculate_acc(basescore,maxscore):
    i = 0
    accuracy = []
    for base in basescore:
        acc = float(base) / float(maxscore[i])
        accuracy.append(acc)
        i += 1
    return accuracy

def calculate_acc_note(goal_acc,total_notes):
    max_note_score = 115 
    hight_average_score = 110
    low_average_score = 105
    # 各阶段倍率需要累计击打的note
    score_1x = 1
    score_2x = 4
    score_4x = 8
    score_8x = total_notes - (score_1x + score_2x + score_4x)
    # 计算总得分(加个括号好看点)
    total_score = score_1x * max_note_score + (score_2x * max_note_score) * 2 + (score_4x * max_note_score) * 4 + (score_8x * max_note_score) * 8
    goal_score = total_score * float(goal_acc / 100)
    # 无倍数情况下计算最大miss个数
    no_double_max_score_miss = int((total_score - goal_score) / max_note_score * 8)
    no_double_hight_average_score_miss = int((total_score - goal_score) / (hight_average_score * (8 + (4 * score_4x))))
    no_double_low_average_score_miss = int((total_score - goal_score) / (low_average_score * (8 + (4 * score_4x))))
    # 以无倍数为一个单位,有倍数情况下丢失x个无倍数单位
    one_miss = 8 + (4 * score_4x)
    double_max_miss = no_double_max_score_miss / one_miss
    double_hight_average_score_miss = no_double_hight_average_score_miss / one_miss
    double_low_average_score_max_miss = no_double_low_average_score_miss / one_miss
    # 格式化字符串
    goal_score = str(goal_score)
    double_hight_average_score_miss = str(double_hight_average_score_miss)
    double_low_average_score_max_miss = str(double_low_average_score_max_miss)
    return {
        'double_max_miss': double_max_miss,
        'goal_score': goal_score,
        'double_hight_average_score_miss': double_hight_average_score_miss,
        'double_low_average_score_max_miss': double_low_average_score_max_miss
        }