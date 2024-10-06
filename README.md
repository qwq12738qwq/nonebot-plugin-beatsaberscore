<p>
<div align="center">
  <a><img src='./Nonebot.png' alt="logo"></a>
</div>
<p>

<div align="center">
  
暗色模式有惊喜(指变好看力)
  
</div>
   
## 📖 介绍

Nonebot2的节奏光剑BeatLeader查分(ﾉ≧∀≦)ﾉ

~~完全不需要介绍~~

## 💿 安装(以下选择其一安装即可)
<details open>
<summary>使用 nb-cli 安装 (十分甚至九分的推荐)</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装
  
    nb plugin install nonebot-plugin-beatsaberscore

</details>

<details>
<summary>使用 pip 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装
  
    pip install nonebot-plugin-beatsaberscore

如果安装完插件不载入的话,在nonebot文件夹中找到**pyproject.toml**,在**plugins**里面添加**nonebot-plugin-beatsaberscore**就完成了

</details>

>如果你的Nonebot2项目下已经启用虚拟环境,可以使用Pipenv安装到项目中,但你需要安装pipenv包
>
<details>
<summary>使用 pipenv 安装</summary>
先安装pipenv
  
    pip install pipenv
  
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装
  
    pipenv install nonebot-plugin-beatsaberscore

</details>

## 🔄 更新
***请不要用上面的安装方式更新!!!!!!!!!!!!***
<details open>
<summary>使用 nb-cli 更新</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令更新
  
    nb plugin install nonebot-plugin-beatsaberscore --upgrade

</details>

<details>
<summary>使用 pip 更新</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可更新
  
    pip install nonebot-plugin-beatsaberscore --upgrade

</details>

## ⚙️ 配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| BS_RETRIES | 否 | 8 | 网络错误重试次数 |
| BS_TIMEOUT | 否 | 5 | 网络超时时间 |
| COMMAND_START | 否 | [] | 响应前缀设置 |

PS:最好是有科学上网,如果没有,BS_RETRIES向建议调至6以上

## 🎉 使用

如果设置了响应前缀,使用以下命令的时候不要忘记加上响应前缀

可以发送` BS help `或` BS帮助 `获取帮助(其实也就导航到这里力)

` BS绑定 ` + SteamID 绑定SteamID,绑定ID才可以查分,也可发送` BS bind `,等效` BS绑定 `

***ScoreSaber查分***

发送` SS查分 `,也可发送` SS score `,等效于` SS查分 `

***BeatLeader查分***

发送` BL查分 `,也可发送` BL score `,等效于` BL查分 `

***Song_ID查歌***

发送` BS search ` + 歌曲的ID或者` BS查歌 ` + 歌曲的id可以查询歌曲的信息

**SteamID是什么?**

 在登入` beatleader.xyz `后打开个人信息
 
 <img src='./explanation.png'>
 
 这个就是你的` SteamID `辣(即使ID不是纯数字也是可以用的)

 即使是scoresaber排行榜网站也是同理
 
 也可以到Steam个人主页去找SteamID,这里就不多赘述了

## ✨ 未来规划
- [X] 添加对ScoreSaber的查分支持
- [ ] ......()
- [ ] 定时推送beatsaver的新曲,渲染新曲图片
- [ ] 添加更细致的响应规则
- [ ] 给自制谱投票功能
- [ ] 歌曲的推荐
- [ ] 优化运行速度,使用线上+本地缓存来提高响应速度


## 📝 更新日志
### 0.9.6
- 新增 ScoreSaber的查分支持
- 修复 绑定错误ID时返回的一些错误信息进行修正
### 0.9.3
- 增加了歌曲id的搜歌功能(十分的简陋啊)
### 0.9.0
- 完成基础的beatleader查分

## 🔍 已知问题
有极少数的beatleader账号获取不到某些信息导致代码报错(之后也会改改)

比其他查分器运行的要慢一些~
(歌曲图片都在海外,如果没有科学上网下载图片会很慢,导致响应时间会变得有些长)

绑定信息存在本地,如果换Bot查分的话你需要再绑定一次

## 🗨️ 想说的话

写这个纯粹是因为喜欢Beat Saber(也是因为Beat Saber没查分器这东西嘛)

本人代码写的比较烂,谨慎pr~~

这个假期之后是真没时间了,等寒假或者高考完吧(不过一有时间我肯定也会更新的)

我们正在考虑做个背景图?就这么点我自己都嫌不够看...

如果你有更好的想法或者修改代码的建议,随时欢迎提出issues(●´∀｀●)

可以的话,给个小小的star~,你的star会让我获得happy buff♪（＾∀＾●）ﾉｼ

## 💡 鸣谢

### [背景图片来源](https://github.com/ComputerElite/ComputerElite.github.io)

(其实是偷来的......)

### [Nonebot框架](https://github.com/nonebot/nonebot2)

**还有身边的一位homo大佬,绝大多数的美术资源(包括read.me的标签图)都出自他之手,如果没有他估计也没这个项目力(悲)**

At last,效果图(●′ω`●)
<img src='./result.png'>
<img src='./SS_result.png'>
enjoy~
