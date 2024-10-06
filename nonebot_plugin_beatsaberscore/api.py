import httpx
from . import retry
from nonebot.log import logger

async def BL_player_scores(player_id):

    async with httpx.AsyncClient():
        scores_response = await retry.time_out_retry(url = f'https://api.beatleader.xyz/player/{player_id}/scores', params = {'sortBy': 'pp','count': '12','page':'1'}, retries = 4)
        if scores_response != None:
            score_data = scores_response.json()
            score_data = score_data['data']
            song_name = [
                all_song_name['leaderboard']['song']['name']
                for all_song_name in score_data
            ]
            song_bpm = [
                all_song_bpm['leaderboard']['song']['bpm']
                for all_song_bpm in score_data
            ]
            song_stars = [
                all_song_stars['leaderboard']['difficulty']['stars']
                for all_song_stars in score_data
            ]
            song_image_url = [
                all_song_image['leaderboard']['song']['coverImage']
                for all_song_image in score_data
            ]
            song_difficulty = [
                all_song_difficulty['leaderboard']['difficulty']['difficultyName']
                for all_song_difficulty in score_data
            ]
            song_pp = [
                all_song_pp['pp']
                for all_song_pp in score_data
            ]
            weight = [
                all_weight['weight']
                for all_weight in score_data
            ]
            accuracy = [
                all_accuracy['accuracy']
                for all_accuracy in score_data
            ]
            improvement = [
                all_improvement_acc['scoreImprovement']['accuracy']
                for all_improvement_acc in score_data
            ]
            song_id = [
                all_song_id['leaderboard']['song']['id']
                for all_song_id in score_data
            ]
            logger.info('获取BeatLeader歌曲全部数据完成')
            return {
                'song_name': song_name,
                'song_bpm': song_bpm,
                'song_stars': song_stars,
                'song_image_url': song_image_url,
                'song_difficulty': song_difficulty,
                'song_pp': song_pp,
                'song_weight': weight,
                'song_accuracy': accuracy,
                'improve_acc': improvement,
                'song_id': song_id
                }
        else:
            logger.error(f'获取歌曲数据失败,请康康网络或这个id没有注册beatleader?Σ(っ °Д °;)っ')
            return None


async def BL_handle_player(player_id):
    api_url = f'https://api.beatleader.xyz/player/{player_id}'
    async with httpx.AsyncClient():
        player_response = await retry.time_out_retry(api_url, params = {'stats': 'true','keepOriginalId':'false'})
        if player_response != None:
            player_data = player_response.json()
            if 'scoreStats' in player_data:
                player_top = player_data['scoreStats']['topPp']
                player_name = player_data.get('name')
                player_avatar = player_data.get('avatar')
                player_pp = player_data.get('pp')
                player_country = player_data.get('country')
                player_rank = player_data.get('rank')
                player_country_rank = player_data.get('countryRank')
                logger.info('获取BeatLeader玩家数据完成')
                return{
                    'total_pp': player_pp,
                    'top_pp': player_top,
                    'name': player_name,
                    'player_avatar': player_avatar,
                    'player_country': player_country,
                    'player_rank': player_rank,
                    'player_country_rank': player_country_rank
                }
            else:
                return None
        else:
            logger.error(f'获取歌曲数据失败,请康康网络或这个id没有注册beatleader?Σ(っ °Д °;)っ')
            return None

async def SS_player_scores(player_id):
    async with httpx.AsyncClient():
        scores_response = await retry.time_out_retry(url = f'https://scoresaber.com/api/player/{player_id}/scores', params = {'sort': 'top','limit': '12','page':'1'}, retries = 4)
        if scores_response != None:
            score_data = scores_response.json()
            score_data = score_data['playerScores']
            song_name = [
                all_song_name['leaderboard']['songName']
                for all_song_name in score_data
            ]
            song_stars = [
                all_song_stars['leaderboard']['stars']
                for all_song_stars in score_data
            ]
            song_image_url = [
                all_song_image['leaderboard']['coverImage']
                for all_song_image in score_data
            ]
            song_difficulty_numbers = [
                all_song_difficulty['leaderboard']['difficulty']['difficulty']
                for all_song_difficulty in score_data
            ]
            song_pp = [
                all_song_pp['score']['pp']
                for all_song_pp in score_data
            ]
            weight = [
                all_weight['score']['weight']
                for all_weight in score_data
            ]
            basescore = [
                all_basescore['score']['baseScore']
                for all_basescore in score_data
            ]
            maxscore = [
                all_maxscore['leaderboard']['maxScore']
                for all_maxscore in score_data
            ]
            ''' ScoreSaberAPI不给这个数据,有机会再解决这个数据的获取了
            improvement = [
                all_improvement_acc['scoreImprovement']['accuracy']
                for all_improvement_acc in score_data
            ]
            '''
            song_sash = [
                all_song_sash['leaderboard']['songHash']
                for all_song_sash in score_data
            ]
            logger.info('ScoreSaber基础歌曲数据处理完成')
            # 计算准度
            i = 0
            accuracy = []
            for base in basescore:
                acc = float(base) / float(maxscore[i])
                accuracy.append(acc)
                i += 1

            sash = ''
            # 排列歌曲的sash值
            for list_sash in song_sash:
                sash += f'{list_sash},'

            beatsaver_to_scoresaber = await search_beatsaver(song_hash = sash)
            if beatsaver_to_scoresaber == None:
                return None
            else:
                pass     
            song_id = []
            song_bpm = []
            # .values()函数遍历全部字典中的值(而不是遍历被赋值的键)
            for summary in beatsaver_to_scoresaber.values():
                # 想不通为什么这api竟然会有这么多的id赋值...
                # 判断是否存在id
                if summary and 'id' in summary != None:
                    song_id.append(summary['id'])
                else:
                    pass
                if summary and 'metadata' in summary != None:
                    song_bpm.append(summary['metadata']['bpm'])
                else: 
                    pass

            song_difficulty = []
            for numbers in song_difficulty_numbers:
                if numbers == int(1):
                    song_difficulty.append('Easy')
                elif numbers == int(3):
                    song_difficulty.append('Normal')
                elif numbers == int(5):
                    song_difficulty.append('Hard')
                elif numbers == int(7):
                    song_difficulty.append('Expert')
                else:
                    song_difficulty.append('ExpertPlus')
            logger.info('ScoreSaber全部歌曲数据处理完成')
            return {
                'song_name': song_name,
                'song_bpm': song_bpm,
                'song_stars': song_stars,
                'song_image_url': song_image_url,
                'song_difficulty': song_difficulty,
                'song_pp': song_pp,
                'song_weight': weight,
                'song_accuracy': accuracy,
                'song_id': song_id
                }
        else:
            logger.error(f'获取歌曲数据失败,请康康网络或这个id没有注册beatleader?Σ(っ °Д °;)っ')
            return None

async def SS_handle_player(player_id):
    api_url = f'https://scoresaber.com/api/player/{player_id}/full'
    async with httpx.AsyncClient():
        player_response = await retry.time_out_retry(api_url, params = {'stats': 'true','keepOriginalId':'false'})
        if player_response != None:
            player_data = player_response.json()
            if player_data != None:
                player_name = player_data.get('name')
                player_avatar = player_data.get('profilePicture')
                player_pp = player_data.get('pp')
                player_country = player_data.get('country')
                player_rank = player_data.get('rank')
                player_country_rank = player_data.get('countryRank')
                logger.info('获取ScoreSaber玩家数据完成')
                return{
                    'total_pp': player_pp,
                    'name': player_name,
                    'player_avatar': player_avatar,
                    'player_country': player_country,
                    'player_rank': player_rank,
                    'player_country_rank': player_country_rank
                }
            else:
                return None
        else:
            logger.error(f'获取歌曲数据失败,请康康网络或这个id没有注册beatleader?Σ(っ °Д °;)っ')
            return None

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
