# bilibili修改小钻石程序

本程序不会再进行维护更新，此为最终版本

配合教程视频[BV1WD4y1V7SE](https://www.bilibili.com/video/BV1WD4y1V7SE/)食用更佳，欢迎关注

# 声明

**本程序仅供学习使用，请勿用于违法违规用途，使用后出现任何问题需自行承担！**

**代码开源免费,拿我项目收费的都是骗子**

**本项目仅在[GitHub](https://github.com/aristorechina/NFT_auto)和[Gitee](https://gitee.com/aristore/NFT_auto)开源发布，要是从其他渠道下载此程序请自行甄别程序的安全性与可行性**

**打包好的程序目前可能不支持低于或等于Windows7系统**

# 你需要准备的

1. 任意一个数字周边卡片
2. 一张`正方形`的，名为`face`，且格式为`jpg`或`png`的头像图片，图片大小需小于`2M`
3. 一个可以正常使用的bilibili账号
4. 一台电脑（release下打包的程序仅支持`Windows`系统）
5. (可选)自行下载程序运行

# 操作步骤

1. 前往[Releases](https://github.com/aristorechina/NFT_auto/releases/tag/The_final_release)下载打包好的程序后运行`NFT.exe`
2. 将用于更换的头像文件置于程序所在目录下（注意，头像名称应为`face`,格式应为`jpg`或`png`,程序默认优先识别`face.jpg`）
3. 根据程序指引选择登录方式
   - 若选择`复制链接`登录，请将程序输出的链接复制下来打开登录
   - 若选择`扫码`登录，程序将会在程序所在目录下生成一个二维码，请打开手机B站扫码登录
   - 若选择`自行输入数据`，请按照程序指引输入您的UID和ACCESS_KEY登录
4. 输入你所拥有的且你想更改的数字藏品项目id（例如：如果你拥有的数字周边是`三体动画数字周边`，那就输入`14`）后按下回车键继续
   - SNH48荣耀时刻数字写真集:1
   - 胶囊计划数字典藏集:4
   - 天官赐福动画2周年数字典藏:5
   - A-AKB48TSH四周年数字集换卡:6
   - B-AKB48TSH四周年数字集换卡:7
   - C-AKB48TSH四周年数字集换卡:8
   - D-AKB48TSH四周年数字集换卡:9
   - E-AKB48TSH四周年数字集换卡:10
   - F-AKB48TSH四周年数字集换卡:11
   - G-AKB48TSH四周年数字集换卡:12
   - H-AKB48TSH四周年数字集换卡:13
   - 三体动画数字周边:14
   - 2022百大UP主数字卡集:18
5. 接下来会出现当前数字周边下你所拥有的卡片名称及其id，复制卡片id后输入，按下回车继续
6. 恭喜🎉此时就大功告成了，等待头像审核完成即可

# 自行运行程序指南

1. 前往官网下载安装[Python](https://www.python.org/)，建议运行版本：`3.8+`

   - 查看Python版本的方式：打开控制台输入以下命令

     ```bash
     python -V
     ```

     

2. 打开控制台，输入以下命令安装依赖库

   ```bash
   pip install -r requirements.txt
   ```

3. 运行程序，详细操作步骤请见上文

# 参考的开源仓库

https://github.com/XiaoMiku01/custom_bilibili_nft

https://github.com/cibimo/bilibiliLogin
