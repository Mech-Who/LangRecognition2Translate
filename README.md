# 命令行展示语音识别+翻译

## 功能

识别电脑的输出声音，并翻译成中文。目前的默认设置是韩语，需要的话可以在代码中修改声音的语种。其他支持的语言，可以参考百炼模型的 paraformer_v2 的支持语种。阿里云均有详细的文档。

主要用法：

- 勉强可用于看直播：打开视频，运行程序，一段连续语音结束后会进行翻译并输出到命令行。
- 可以帮助进行视频翻译：在代码中设置好输入语言的代码，然后播放视频语音节课查看到翻译。

不足：

- 难以支持多人同时语音：因为没办法根据音色区分不同人的声音，所以同事说话会干扰识别和翻译，导致效果不尽如人意。
- 不支持 GUI 界面：毕竟是临时项目，没有这么完善，欢迎大家自行升级设计。
- 代码的功能划分不明确，一个类解决所有问题。需要进行代码结构的改进。
- 无法进行流式输出（如果一句话太长要等整句话结束才能输出）。
- 目前测试只有浏览器音频可以，PotPlayer 等播放器的音频就不行（输入设置的问题？）
- 音频输入选择不可用时无法正常处理（异常处理需要完善）。
- 尚未打包成应用程序，只能在命令行界面直接运行。
- 缺少日志记录功能，无法把翻译过的内容都保存下来。
- 无法热更新配置。

## 使用说明

1. 安装 VB-Cable 虚拟声卡
2. 重启电脑
3. 测试是否可以正常识别设备（Cable Output）
4. 配置环境变量，包括：
   1. 阿里百炼模型 api key（用于语音识别）
   2. 阿里云 access key id（用于机器翻译）
   3. 阿里云 access key secret（用于机器翻译）
5. 执行 main 尝试使用

## 依赖包

本项目使用 uv 进行项目管理，一切依赖均可以在`pyproject.toml`文件中的`dependencies`部分进行查看。

## 其他说明

由于本项目是因为临时喜欢的团要进行直播，然后没有看到合适的翻译，并且本人并不懂韩语，因此临时急着搭了个架子出来。项目中的 bug 应该还有一些，并且目前只能代码直接运行，没有进行打包等操作，所以只能在命令行看翻译。不过感觉稍微布局一下就 ok 了。

后续更新不好说，如果我还会用到的话也许还会更新。或者某天心血来潮可以更新一下哈哈，大家不要抱有期望，可以尝试自己更新。稍后我可以添加 GPL3 协议，免费开源，欢迎自行升级。

## 未来计划

- [x] 确定种类的变量通过枚举去定义会更好。
- [ ] asyncio 异步编程实现语音识别和机器翻译两个功能（IO 密集型任务，无需多进程）
- [x] 添加日志记录，保存识别翻译结果。
- [x] 使用配置文件保存配置，通过动态加载实现热更新配置。
- [ ] 添加 GUI，打包成应用程序进行使用。
- [ ] 在翻译文本的时候再进行分句。
- [ ] 针对输入设备进行适配，适配不同设备。

## 致谢

感谢阿里云提供的服务，以及各项服务提供的免费额度，让这个项目得以诞生。
