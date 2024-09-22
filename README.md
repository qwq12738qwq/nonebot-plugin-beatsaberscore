<p>
<div align="center">
  <a><img src='./Nonebot.png' alt="logo"></a>
</div>
<p>
  
#    nonebot-plugin-beatsaberscore
  
## 📖 介绍

Nonebot2的节奏光剑BeatLeader查分

_(介绍没啥好写的)_

## 💿 安装(以下选择其一安装即可)
<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装
  
    nb plugin install nonebot-plugin-beatsaberscore

</details>

<details open>
<summary>使用 pip 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装
  
    pip install nonebot-plugin-beatsaberscore

</details>

>如果你的Nonebot2项目下已经启用虚拟环境,可以使用Pipenv安装到项目中,但你需要安装pipenv包
>
<details open>
<summary>使用 pipenv 安装</summary>
先安装pipenv
  
    pip install pipenv
  
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装
  
    pipenv install nonebot-plugin-beatsaberscore

</details>

## ⚙️ 配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| BS_RETRIES | 否 | 8 | 网络错误重试次数 |
| BS_TIMEOUT | 否 | 5 |网络超时时间 |

PS:最好是有科学上网,如果没有,BS_RETRIES向建议调至6以上

## 🎉 使用
可以发送` BS help `或` BS帮助 `获取帮助(其实也就导航到这里力)

` BS bind `绑定beatleaderID后,输入` BS score `就可以查分了

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
- [ ] 优化运行速度,使用线上+本地缓存来提高响应速度
- [ ] 添加对ScoreSaber的查分支持

## 📝 更新日志

### 0.9.0
- 完成基础的beatleader查分

## 已知问题
有极少数的beatleader账号获取不到某些信息导致代码报错(之后也会改改)

比其他查分器运行的要慢一些~
(歌曲图片都在海外,如果没有科学上网下载图片会很慢,导致响应时间会变得有些长)

## 想说的话
本人代码写的比较烂,谨慎pr~~

还有些想法还没往里面弄,高三牲时间不太充裕QAQ,所以版本定为0.9.0

如果你有更好的想法或者修改代码的建议,随时欢迎提出issues(●´∀｀●)

可以的话,给个小小的star~,你的star会让我获得happy buff♪（＾∀＾●）ﾉｼ

At last,效果图(●′ω`●)
<img src='./result.png'>
enjoy~
