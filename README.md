<p>
<div align="center">
  <a><img src='./Nonebot.png' alt="logo"></a>
</div>
<p>
  
# nonebot-plugin-beatsaberscore
  
## 📖 介绍

Nonebot2的节奏光剑BeatLeader查分



## 💿 安装


## ⚙️ 配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| BS_RETRIES | 否 | 8 | 网络错误重试次数 |
| BS_TIMEOUT | 否 | 5 |网络超时时间 |

PS:最好是有科学上网,如果没有,BS_RETRIES向建议调至6以上

## 🎉 使用
BS bind绑定beatleaderID后,输入BS score就可以查分了
也可以输入` BS绑定 `绑定beatleaderID,` BS查分 `用于触发查分的指令
**beatleaderID是什么?**
 在登入beatleader.xyz后打开个人信息
 <img src='./explanation.png'>
 这个就是你的beatleaderID辣
 (说人话也就是SteamID)

## ✨ 未来规划
- [ ] 定时推送beatsaver的新曲,渲染新曲图片
- [ ] 添加更细致的响应规则
- [ ] 歌曲的推荐
- [ ] 添加对ScoreSaber的查分支持

## 📝 更新日志

### 0.9.0
- 完成基础的beatleader查分

最后,效果图(●′ω`●)
<img src='./result.png'>
