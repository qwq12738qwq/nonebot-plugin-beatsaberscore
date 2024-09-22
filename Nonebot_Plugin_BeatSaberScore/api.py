import httpx
from . import retry
from nonebot.log import logger

async def player_scores(player_id):
    api_url = f'https://api.beatleader.xyz/player/{player_id}/scores'

    async with httpx.AsyncClient() as client:
        scores_data = {
        'sortBy': 'pp',
        'count': '12',
        'page':'1'
    }
        scores_response = await client.get(api_url, params=scores_data)
        if scores_response.status_code == 200:
            score_data = scores_response.json()
            if 'data' in score_data:
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
                    logger.info('获取歌曲数据完成')
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
                return 114514
        else:
            logger.error(f'获取歌曲数据失败,请康康网络或这个id没有注册beatleader?Σ(っ °Д °;)っ')
            return 114514


async def handle_player(player_id):
    api_url = f'https://api.beatleader.xyz/player/{player_id}'
    async with httpx.AsyncClient() as client:
        player_data = {
            'stats': 'true',
            'keepOriginalId':'false'
        }
        player_response = await client.get(api_url, params=player_data)
        if player_response.status_code == 200:
                player_data = player_response.json()
                if 'scoreStats' in player_data:
                    player_top = player_data['scoreStats']['topPp']
                    player_name = player_data['name']
                    player_avatar = player_data['avatar']
                    player_pp = player_data['pp']
                    player_country = player_data['country']
                    player_rank = player_data['rank']
                    player_country_rank = player_data['countryRank']
                    logger.info('获取玩家数据完成')
                    return{
                        "total_pp": player_pp,
                        "top_pp": player_top,
                        "name": player_name,
                        "player_avatar": player_avatar,
                        "player_country": player_country,
                        "player_rank": player_rank,
                        "player_country_rank": player_country_rank
                    }
                else:
                    return 114514
        else:
            logger.error(f'获取歌曲数据失败,请康康网络或这个id没有注册beatleader?Σ(っ °Д °;)っ')
            return 114514
