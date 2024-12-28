import httpx
from . import retry
from nonebot.log import logger

async def BL_player_scores(player_id,text = False):
    if text == True:
        async with httpx.AsyncClient():
            response = await retry.time_out_retry(url = f'https://api.beatleader.xyz/player/{player_id}/scores', params = {'sortBy': 'pp','count': '1','page':'1'}, retries = 4)
        if response == None:
            return 'BL_None'
        else:
            return 'BL_data'
              
    async with httpx.AsyncClient():
        scores_response = await retry.time_out_retry(url = f'https://api.beatleader.xyz/player/{player_id}/scores', params = {'sortBy': 'pp','count': '40','page':'1'}, retries = 4)
        date_response = await retry.time_out_retry(url = f'https://api.beatleader.xyz/player/{player_id}/scores', params = {'sortBy': 'data','count': '4','page':'1'}, retries = 4)
    if scores_response == None:
        logger.error(f'获取歌曲数据失败,请康康网络或这个id没有注册beatleader?Σ(っ °Д °;)っ')
        return None
    else:
        pass
    all_data = {}
    all_data['songs'] = {}
    all_data['date'] = {}
    all_data['player'] = {}
    score_data = scores_response.json()
    score_data = score_data['data']
    ster_pp = i = 0
    for datas in score_data:
        ster_pp += datas['pp']
        # 解决准度提升无数据问题
        try:
            Improvement = datas['scoreImprovement']['accuracy']
        except:
            datas['scoreImprovement'] = {}
            datas['scoreImprovement']['accuracy'] = {}
            datas['scoreImprovement']['accuracy'] = '0.00'
        # 标识歌曲,防止字典冲突
        if datas.get('accLeft') == float(0) or datas.get('accRight') == float(0):
            OneSaber = '|'
        else:
            OneSaber = ''
        songs = {
            f"{datas['leaderboard']['song']['name']}{datas['leaderboard']['difficulty']['difficultyName']}{OneSaber}": {
                'id': f"{datas['leaderboard']['song']['id']}",
                'image_url': f"{datas['leaderboard']['song']['coverImage']}",
                'pp': f"{datas['pp']}",
                'difficulty': f"{datas['leaderboard']['difficulty']['difficultyName']}",
                'stars': f"{datas['leaderboard']['difficulty']['stars']}",
                'weight': f"{datas['weight']}",
                'accuracy': f"{datas['accuracy']}",
                'improvement': f"{datas['scoreImprovement']['accuracy']}",
                'accleft': f"{datas['accLeft']}",
                'accright': f"{datas['accRight']}",
                'bpm':  f"{datas['leaderboard']['song']['bpm']}",
                'position': f'{i}'
            }
        }
        all_data['songs'].update(songs)
        i += 1
    if date_response == None:
        logger.error(f'获取歌曲数据失败,请康康网络或这个id没有注册beatleader?Σ(っ °Д °;)っ')
        return None
    else:
        pass

    async with httpx.AsyncClient():
        player_response = await retry.time_out_retry(f'https://api.beatleader.xyz/player/{player_id}', params = {'stats': 'true','keepOriginalId':'false'})
        if player_response == None:
            return None
        else:
            pass
        player_data = player_response.json()
        all_data['player'] = {
            'player_stars': f"{(ster_pp / 40 * 0.96 / 52) * 0.9 + 0.075 * (i)}",
            'player_name': f"{player_data.get('name')}",
            'player_avatar': f"{player_data.get('avatar')}",
            'player_pp': f"{player_data.get('pp')}",
            'player_country': f"{player_data.get('country')}",
            'player_rank': f"{player_data.get('rank')}",
            'player_country_rank': f"{player_data.get('countryRank')}"
            }
        logger.info('获取BeatLeader玩家数据完成')

    date = date_response.json()
    date = date['data']
    i = 41
    for datas in date:
        # 标识歌曲,防止字典冲突
        if datas.get('accLeft') == float(0) or datas.get('accRight') == float(0):
            OneSaber = '|'
        else:
            OneSaber = ''
        if datas.get('pp') == None:
            pp = 000.00
        else:
            pp = datas['pp']
        if datas.get('weight') == None:
            weight = 1
        else:
            weight = datas['weight']
        if datas.get('stars') == None:
            stars = datas['leaderboard']['difficulty']['difficultyName']
        else:
            stars = datas['leaderboard']['difficulty']['stars']
        if datas.get('improvement') == None:
            improvement = 0.00
        else:
            improvement = datas['scoreImprovement']['accuracy']
        songs = {
            f"{datas['leaderboard']['song']['name']}{datas['leaderboard']['difficulty']['difficultyName']}{OneSaber}": {
                'id': f"{datas['leaderboard']['song']['id']}",
                'image_url': f"{datas['leaderboard']['song']['coverImage']}",
                'pp': f"{pp}",
                'difficulty': f"{datas['leaderboard']['difficulty']['difficultyName']}",
                'stars': f"{stars}",
                'weight': f"{weight}",
                'accuracy': f"{datas['accuracy']}",
                'improvement': f"{improvement}",
                'accleft': f"{datas['accLeft']}",
                'accright': f"{datas['accRight']}",
                'bpm':  f"{datas['leaderboard']['song']['bpm']}",
                'position': f'{i}'
            }
        }
        i += 1
        all_data['date'].update(songs)
    logger.info('获取BeatLeader歌曲数据完成')
    return all_data

async def SS_player_scores(player_id,text = False,old_data = {}):
    if text == True:
        async with httpx.AsyncClient():
            response = await retry.time_out_retry(url = f'https://scoresaber.com/api/player/{player_id}/scores', params = {'sort': 'top','limit': '1','page':'1'}, retries = 4)
        if response == None:
            return 'SS_None'
        else:
            return 'SS_data'
    async with httpx.AsyncClient():
        scores_response = await retry.time_out_retry(url = f'https://scoresaber.com/api/player/{player_id}/scores', params = {'sort': 'top','limit': '40','page':'1'}, retries = 4)
    if scores_response == None:
        logger.error(f'获取歌曲数据失败,请康康网络或这个id没有注册beatleader?Σ(っ °Д °;)っ')
        return None
    else:
        pass
    score_data = scores_response.json()
    score_data = score_data['playerScores']
    all_data = {}
    all_data['songs'] = {}
    all_data['player'] = {}
    difficulty = id = bpm = ''
    ster_pp = i = 0
    for datas in score_data:
        ster_pp += datas['score']['pp']
        # 解决准度提升无数据问题
        if datas.get('scoreImprovement') == None:
            datas['scoreImprovement'] = {}
            datas['scoreImprovement']['accuracy'] = {}
            datas['scoreImprovement']['accuracy'] = '0.00'
        else:
            pass
        # 标识歌曲,防止字典冲突
        if datas.get('accLeft') == float(0) or datas.get('accRight') == float(0):
            OneSaber = '|'
        else:
            OneSaber = ''
        # 计算准度
        accuracy = float(datas['score']['baseScore']) / float(datas['leaderboard']['maxScore'])
        # 准度转化
        if datas['leaderboard']['difficulty']['difficulty'] == int(1):
            difficulty = 'Easy'
        elif datas['leaderboard']['difficulty']['difficulty'] == int(3):
            difficulty = 'Normal'
        elif datas['leaderboard']['difficulty']['difficulty'] == int(5):
            difficulty = 'Hard'
        elif datas['leaderboard']['difficulty']['difficulty'] == int(7):
            difficulty = 'Expert'
        else:
            difficulty = 'ExpertPlus'
        # hash转化成id
        try:
            id = old_data[f"{datas['leaderboard']['songName']}{difficulty}{OneSaber}"]['id']
            bpm = old_data[f"{datas['leaderboard']['songName']}{difficulty}{OneSaber}"]['bpm']
        except:
            beatsaver_to_scoresaber = await search_beatsaver(song_hash = datas['leaderboard']['songHash'])
            if beatsaver_to_scoresaber == None:
                return None
            id = beatsaver_to_scoresaber['id']
            bpm = beatsaver_to_scoresaber['metadata']['bpm']
        songs = {
            f"{datas['leaderboard']['songName']}{difficulty}{OneSaber}": {
                'id': f"{id}",
                'image_url': f"{datas['leaderboard']['coverImage']}",
                'pp': f"{datas['score']['pp']}",
                'difficulty': f"{difficulty}",
                'stars': f"{datas['leaderboard']['stars']}",
                'weight': f"{datas['score']['weight']}",
                'accuracy': f"{accuracy}",
                'improvement': f"{float(0.00)}",
                'accleft': f"{float(000.00)}",
                'accright': f"{float(000.00)}",
                'bpm':  f"{bpm}",
                'position': f'{i}'
            }
        }
        all_data['songs'].update(songs)
        i += 1
    logger.info('获取ScoreSaber歌曲数据完成')
    async with httpx.AsyncClient():
        player_response = await retry.time_out_retry(f'https://scoresaber.com/api/player/{player_id}/full', params = {'stats': 'true','keepOriginalId':'false'})
        if player_response == None:
            return None
        else:
            pass
        player_data = player_response.json()
        all_data['player'] = {
            'player_stars': f"{(ster_pp / 40 * 0.96 / 52) * 0.9 + 0.075 * (i)}",
            'player_name': f"{player_data.get('name')}",
            'player_avatar': f"{player_data.get('profilePicture')}",
            'player_pp': f"{player_data.get('pp')}",
            'player_country': f"{player_data.get('country')}",
            'player_rank': f"{player_data.get('rank')}",
            'player_country_rank': f"{player_data.get('countryRank')}"
            }
        logger.info('获取ScoreSaber玩家数据完成')
        return all_data

async def search_beatsaver(song_id = None,song_hash = None):
    if song_hash == None:
        api_url = f'https://api.beatsaver.com/maps/id/{song_id}'
    else:
        api_url = f'https://api.beatsaver.com/maps/hash/{song_hash}'

    async with httpx.AsyncClient():
        song_data_response = await retry.time_out_retry(api_url, params = None, retries = 4)
        if song_data_response != None:
            song_data = song_data_response.json()
            return song_data
        else:
            logger.warning('获取歌曲数据发生错误')
            return None

async def beatsaver_timing():
    return

async def beatsaver_vote():
    return