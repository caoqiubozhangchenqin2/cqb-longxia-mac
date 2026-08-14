# 身高小助理

身高小助理是一款面向 Windows 的本地家庭成长记录程序。它可以管理一个或多个孩子，记录身高、体重、备注和多种用药阶段，并生成可缩放、可悬停查看的成长图表。

## 下载

普通用户请前往 [身高小助理 v1.0.1 发布页面](https://github.com/caoqiubozhangchenqin2/cqb-longxia-mac/releases/tag/height-assistant-v1.0.1)，下载 Windows x64 ZIP，完整解压后双击 `身高小助理.exe`。

软件是免安装便携版。请保留 exe 与 `_internal` 文件夹的相对位置，不要只复制 exe。

## 主要功能

- 支持任意数量的孩子及独立成长档案
- 身高、体重、测量方式、长备注和多药品记录
- 身高、增长速度、体重、BMI、同龄中位差图表
- 7～18 岁 `-2SD / -1SD / 中位数 / +1SD / +2SD` 参考线
- 独立数据卡显示成年遗传靶身高，不影响图表比例
- 鼠标悬停查看节点，滚轮缩放、左键拖动、右键恢复全图
- 历史记录排序、搜索、编辑、撤回和归档
- 孩子归档与恢复
- 用户自选位置备份与恢复
- Excel、CSV、JSON、PNG、PDF 导出

## 隐私

程序默认只把数据保存在自身目录下的 `data/height_assistant.db`，不会自动上传到 GitHub、云端或作者服务器。

不要把使用后的整个程序目录发给别人，其中可能包含孩子姓名、出生日期、身高、体重、备注和用药信息。备份文件同样包含完整家庭数据。

## 从源码运行

需要 Python 3.12：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

运行测试：

```powershell
$env:QT_QPA_PLATFORM = "offscreen"
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

构建 Windows 便携版：

```powershell
.\.venv\Scripts\pyinstaller.exe --noconfirm --clean .\身高小助理.spec
```

## 医疗提示

本软件用于家庭记录和趋势观察，不提供诊断、处方或用药剂量建议。图表参考线与遗传靶身高属于统计学参考，不能替代规范测量、骨龄检查或儿科内分泌医生评估。

设置页面包含作者的微信与支付宝自愿支持入口；是否打赏不影响任何功能。
