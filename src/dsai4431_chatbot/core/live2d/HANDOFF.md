# 交接记忆 · PyQt5 里播放 Live2D（大肥鱼）

> 写于 2026-11-11。换新上下文时把这份丢给模型即可接着干。
>
> **已迁入 DSAI4431_Chatbot（2026-11-11）**，目录结构变了，本文中出现的旧路径需按此表换算：
>
> | 本文旧路径 | 现在的位置 |
> |---|---|
> | `live2d-python-demo\`（工作目录） | `src\dsai4431_chatbot\core\live2d\` |
> | `demo_interactive.py` 等代码 | 同上（同目录） |
> | `vendor\` | `asset\live2d\vendor\` |
> | `CubismSdkForWeb-5-r.5\Core\` | `asset\live2d\cubism-core\` |
> | `models\` | `asset\live2d\models\` |
> | `CubismSdkForWeb-5-r.5\DeepSeek免费公皮\` | `asset\live2d\models\DeepSeek免费公皮\`（已 gitignore） |
> | `.venv\` | 项目根 `DSAI4431_Chatbot\.venv\` |
> | 早期版本（index.html、pyqt5_*.py、option_*.py） | `legacy\` 子目录 |
>
> 代码侧已改：`demo_interactive.py` 用 `ASSET_ROOT` 解析资源位置（向上找
> `<repo>/asset/live2d`，可用 `L2D_ASSET_DIR` 覆盖），静态服务把 `/vendor/`
> 和 `/model/` 映射到 asset 下，HTML 里的相对引用不用改。
> 启动方式见该目录下的 `启动.bat` 或 §0。

---

## 0. 现在是什么状态

一个可交互的 Live2D 桌面演示程序，双击 `启动.bat` 就跑。

| 能力 | 状态 |
|---|---|
| 大肥鱼模型渲染 | ✅ |
| 8 组换装/手势动作 + 23 个表情 | ✅ |
| 窗口缩放 / 全屏自适应 | ✅ |
| 脸上黑块 | ✅ 已修（隐藏两个画黑层 drawable） |
| 戳一下（闭眼 + 歪头） | ✅ |
| 摸头（`><` 眼睛 + 小张嘴 + 脸红） | ✅ |
| 摸头循环（GIF 式，手动停） | ✅ |
| 点击 / 摸头的判定 | ✅ 按时长：<300ms 松手=点击，按住 ≥300ms=摸头（见 §7.3b） |
| 头部跟随鼠标 | ✅ 但**牺牲物理晃动**（见 §7.4） |
| 口型接麦克风 / 桌宠模式 | ❌ 没做 |

**启动**：

```powershell
cd P:\Deekseek_playground\live2d-python-demo
.\.venv\Scripts\python.exe demo_interactive.py --model "CubismSdkForWeb-5-r.5\DeepSeek免费公皮\DeepSeek\大肥鱼.demo.model3.json"
```

或直接双击 `启动.bat`（自动找模型，优先 `*.demo.model3.json`）。

**必须用 `.demo.model3.json`，不能用原始的 `.model3.json`** —— 见 §5.3。

---

## 1. 文件清单

| 文件 | 作用 |
|---|---|
| `demo_interactive.py` | **主程序**。Stage（QWidget + QWebEngineView + 本地 HTTP）、DemoWindow（4 个页签：动作/表情/参数/设置）、`react()` / `stop_reaction()` 对外 API |
| `demo_live2d.html` | **渲染页**。pixi + pixi-live2d-display + Cubism Core，`window.l2d` API，反应系统、跟随系统、黑层修正 |
| `make_demo_model.py` | 扫描 `Animation/*.motion3.json` 和 `Exp3/*.exp3.json`，生成 `<name>.demo.model3.json` |
| `启动.bat` | 纯 ASCII 启动器（中文路径不能写进 bat，见 §3.6） |
| `demo_probe.html` | 占位页（没有模型时用），同一套 `window.l2d` 签名 |
| `index.html` / `pyqt5_*.py` / `option_*.py` | 早期版本，保留但不用 |

模型：`CubismSdkForWeb-5-r.5\DeepSeek免费公皮\DeepSeek\`
- `大肥鱼.moc3`（15.7 MB）、5 张 4096 贴图、`大肥鱼.physics3.json`（131 个物理设置）、`大肥鱼.cdi3.json`
- **没有 `pose3.json`** ← 这是黑块问题的根源

---

## 2. 环境

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --disable-pip-version-check ^
    -i https://pypi.tuna.tsinghua.edu.cn/simple PyQt5 PyQtWebEngine
```

实际版本：PyQt5 5.15.11 / PyQtWebEngine 5.15.7 / **Qt 5.15.2（内嵌 Chromium 83）**。

---

## 3. 环境与初始化相关的坑

### 3.1 必须开 `--no-sandbox`
不开的话 `QWebEngineView` **白屏，`loadFinished` 永远不触发**，而且没有任何报错。
只加 `--disable-gpu` 无效，**必须 `--no-sandbox`**。

已在 `demo_interactive.py` 里硬编码：

```python
os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")
os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--no-sandbox --disable-gpu ...")
```

跳过它：`L2D_KEEP_SANDBOX=1`。

### 3.2 `AA_ShareOpenGLContexts` 必须在 QApplication 之前
否则 WebEngine 直接崩。

### 3.3 高分屏必须开 DPI 缩放
```python
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
```
这台机器 `AppliedDPI = 192`（**200% 缩放**）。不开的话 15px 字看起来只有 7.5px，界面小到看不清。
**我一开始靠调 QSS 字号来救，完全无效——那种方向就是错的。**

### 3.4 Chromium 83 没有顶层 await
页面脚本里的 `await` 必须包在 `(async () => { ... })();` 里，否则报 `Uncaught SyntaxError: Unexpected reserved word`。

### 3.5 本地 HTTP，不能用 file://
CORS 会拦住 `fetch` model3.json 和贴图。用 `ThreadingHTTPServer` 起在 `127.0.0.1:<随机端口>`，`/model/` 前缀指向模型目录。

### 3.6 bat 里不能写中文路径
cmd.exe 按系统 ANSI(GBK) 解析 `.bat`，中文会变成乱码命令。`启动.bat` 是**纯 ASCII**（验证过：非 ASCII 字节数 = 0），中文路径交给 Python 处理。

---

## 4. Cubism Core 相关

### 4.1 Core 6 与 pixi-live2d-display 0.4.0 不兼容

`pixi-live2d-display@0.4.0` 是按 Cubism **4** 写的。Core 6（`csmGetVersion() = 0x06000001`）里 `drawables.renderOrders` 被改名成 `drawables.drawOrders`，导致：

```
TypeError: Cannot read property '0' of undefined
    at Wt.doDrawModel (cubism4.min.js:1:75844)
```

**垫片**（已写在 `demo_live2d.html`）：

```js
try {
  const dr = im.coreModel._model.drawables;
  if (!dr.renderOrders && dr.drawOrders) {
    dr.renderOrders = new Int32Array(cm.getRenderOrders());
  }
} catch (_) {}
```

⚠ 直接 `renderOrders = drawOrders` **是错的** —— drawOrders 是"序号"，renderOrders 是"索引"，长度也不同（176 vs 715）。必须用 `getRenderOrders()`。

### 4.2 用的是官方 CDN 的 Core
`vendor/live2dcubismcore.min.js`，207155 字节，SHA256 `25ae938c...`，与鲸语项目 `vendor-sources.json` 记录的一致。
来源：`https://cubism.live2d.com/sdk-web/cubismcore/live2dcubismcore.min.js`

---

## 5. 模型数据相关的坑

### 5.1 这是 VTS 风格模型，动作/表情不在 model3.json 里
`大肥鱼.model3.json` 的 `FileReferences` **没有 `Motions` 也没有 `Expressions`**。
实际资源在 `Animation/*.motion3.json`（8 个）和 `Exp3/*.exp3.json`（23 个），文件名就是动作/表情名。

`make_demo_model.py` 扫描目录后生成带 `Motions` + `Expressions` 的 `大肥鱼.demo.model3.json`。**原始文件不要改。**

### 5.2 表情文件里可能只有一行参数
`Exp3/＞＜.exp3.json` 全文只做一件事：

```json
{ "Id": "key5", "Value": 1.0, "Blend": "Add" }
```

**`key5 = 1` 就是 `><` 眼睛。** 我为了让眼睛笑成 `><`，把 `EyeSmile`、`ParamEyeLOpen`、`LEyes1/2`、`REyes1/2`、`Eyeball1/2/3` 全试了一遍，都做不出来——**答案一早就在表情文件里，我没先去翻 Exp3 目录。**

⚠ 文件名用的是**全角**字符 `＞＜`，用 `<` `>` 去匹配会漏掉。

### 5.3 脸上的黑块 = drawable 级问题，不是 Part 级

**现象**：鼻梁位置一个 4×7 像素纯黑方块。

**实际数据**：`Part46` 下挂了 **5 个 drawable**：

| drawable | multiplyColor | 是什么 |
|---|---|---|
| `#513` | `(0,0,0)` | 黑脸覆盖层（贴图本身就是黑的） |
| `#514` | `(0,0,0)` | 同上 |
| `#515` | `(1,1,1)` | 鼻子 |
| `#516` | `(1,1,1)` | 鼻子 |
| `#517` | `(1,1,1)` | 鼻子 |

模型没有 `pose3.json`，所以 VTS 里本该被隐藏的黑脸层直接露在脸上。

**修法**（已写进 `demo_live2d.html`）：

```js
const HIDDEN_DRAWABLES_BY_MODEL = { '大肥鱼': [513, 514] };
```

⚠⚠ **踩过的坑**：第一次用 `setPartOpacityById('Part46', 0)` 整 Part 关掉 → **鼻子也没了**，被用户指出"没鼻子太奇怪"。
**一个 Part 可以挂任意多个 drawable，它们的颜色/透明度/图层都独立。要精确到 drawable。**

⚠ 另一个弯：`multiplyColor=(0,0,0)` 说明贴图乘黑，**改回 (1,1,1) 还是黑**（贴图本身黑）。想靠调颜色救是死路。

---

## 6. 参数系统（反应、跟随的底座）

### 6.1 参数写入的唯一有效位置

**规格**：`pixi-live2d-display` 的 `Cubism4InternalModel.update()` 内部会跑 motion → eyeBlink → focus → natural-movement → `coreModel.update()`，最后 Core 会把参数重置。

实测结论：

| 写入位置 | 结果 |
|---|---|
| `beforeModelUpdate` 事件里 | ❌ 写进去当场读回对，下一帧被 Core 重置 |
| hook `coreModel.update` 内部（orig 前后都试过） | ❌ 同上 |
| **包住整个 `internalModel.update`，在进入前写** | ✅ **唯一有效** |

```js
const origIMUpdate = im.update.bind(im);
im.update = function () {
  if (_rx) _tickReaction(performance.now());   // 反应优先
  else _tickFollow();                          // 否则跟随
  return origIMUpdate.apply(im, arguments);
};
```

### 6.2 会覆盖参数的三个系统

写进去不等于看得到。以下三个都会在之后重算并盖掉：

| 系统 | 影响 | 处理 |
|---|---|---|
| **物理**（`im.physics`） | 把 `ParamEyeLOpen` 当 OUTPUT 重算；**还会锁死头部角度** | 反应/跟随期间 `im.physics = null` |
| **动作**（Idle） | 每帧写全部参数 | 反应期间 `im.motionManager.stopAllMotions()` |
| **自动眨眼**（`im.eyeBlink`） | 写 `ParamEyeLOpen` | 反应期间置 `null` |

### 6.3 参数名陷阱

- 这个模型有 **509 个参数**，大量 VTS 自定义名：`EyeSmile`、`key3`~`key6`、`LEyes1/2`、`LEyeball1/2/3`、`LEyeSquint`、`SHOCKEYE`…
- **不一定带 `Param` 前缀**，`setParameterValueById` 按 id 精确匹配，写不存在的 id 会抛错（要用 try/catch 兜）
- `getParameterIndex(id)` 对存在参数返回索引；**`getPartId()` / `getParameterId()` 在 pixi 的 coreModel 上不存在**，会 `is not a function`
- `ParamCheek` 索引是 **509**，越界（总数 509，有效 0~508）——写它能"成功"，但没有任何效果

### 6.4 停止时必须复位参数
`_stopReaction()` 里要把反应碰过的参数写回 `getParameterDefaultValue(idx)`，否则会卡在眯眼微笑的样子不动。

---

## 7. 反应系统与跟随系统

### 7.1 反应怎么编的
模型自带的 8 个 motion 全是换装/手势（举手、狗尾草、竖手指、脱捕…），**没有"被点/被摸头"**。
所以用**参数时间轴**手写，不依赖任何模型资源，换模型也能用：

```js
const REACTIONS = {
  tap:        { duration: 1050, tracks: { ParamEyeLOpen: [[0,1],[110,0],[430,0],[720,1],[1050,1]], ... } },
  headpat:    { duration: 1950, tracks: { key5: [[0,0],[200,1],[1450,1],[1950,0]], ... } },
  headpatLoop:{ duration: 2200, loop: true, tracks: { key5: [[0,1],[2200,1]], ... } },
};
```

插值用 smoothstep。`loop: true` 的轨**首尾值必须相等**，否则接缝会跳。

### 7.2 三个反应的效果

**`tap`（戳一下，1.05s）**：闭紧眼（`ParamEyeLOpen=0`）+ 歪头 `ParamAngleZ=13°` + 微低头 + 皱眉

**`headpat`（摸头，1.95s）**：
```
key5 = 1                  → 眼睛 ><
ParamMouthOpenY = 0.35    → 小张嘴
ParamMouthForm = 0.5      → 轻微笑
ParamCheek = 0.7          → 脸红
+ 头微低 7°、偏 8°、身体侧倾 3°
```

**`headpatLoop`（循环摸头，2.2s 一圈）**：上面那些保持住，头左右轻晃 5→10→4→10→5°，前后微点 6→3→6°。

### 7.3 Python 端 API

```python
win.react('tap')          # 戳一下
win.react('headpat')      # 摸头（一次性）
win.react('headpatLoop')  # 摸头（循环）
win.stop_reaction()       # 停止 + 复位参数 + 接回待机动作
```

页面侧对应 `window.l2d.react(name)` / `stopReaction()` / `reacting` / `reaction`（当前反应名）。

### 7.3b 页面内的「点击 / 摸头」判定（只看时长，不看位置）

早期版本按**点在哪**判：`hitTest` 命中 `Head` 或落在模型上部 28% → 摸头，否则戳一下。现在改成只按**按住多久**：

| 操作 | 结果 |
| --- | --- |
| 按住 **< 300ms** 就撒手 | `tap`（被戳一下，1.05s） |
| 按住 **≥ 300ms** 还不松 | `headpatLoop`（摸头，一直摸到你松手） |
| 摸头中松手 | 淡出 `fade`（280ms 把参数拉回默认），然后回待机 |

- 阈值可用 URL 参数 `hold=` 覆盖：`demo_live2d.html?...&hold=450`。
- 300ms 判定用 `pointerdown/pointerup`（挂在 canvas / window 上），抬起在画布外也收得到；`pointercancel` 和 window `blur`（Alt+Tab 切走）也算松手。
- `window.l2d.input` 返回 `{pressed, patting, holdMs}`，调试/自动化测试用它读状态。

修改前实测（2026-11-11）：`framing=bust&zoom=1.9`，用 QTest 往 render widget 发真实鼠标事件，`pointerdown/up` 都能进到页面（target 是 `CANVAS`）；按住 450ms → `headpatLoop`，松手 → `fade` → `null`。

### 7.4 头部跟随（当前方案，有取舍）

**`model.focus()` 在这个配置下完全不工作** —— 实测调用后 `ParamAngleX/ParamEyeBallX/BodyAngleX` 全是 0，一个都没改。所以自己实现。

**鼠标位置来源**：`QWebEngineView` **不保证把 `mousemove` 转发进页面**，页面上监听 `document.addEventListener('mousemove')` 收不到。
改成 **Qt 端每 60ms 轮询 `QCursor.pos()`**，映射到 view 局部坐标归一化到 ±1，调 `l2d.setAim(nx, ny)`。

**写参数**（在 `im.update` 进入前）：

```
ParamAngleX     = nx * 30
ParamAngleY     = -ny * 30
ParamEyeBallX   = nx
ParamEyeBallY   = -ny
ParamBodyAngleX = nx * 12
```

阻尼系数 0.13，60ms 轮询，变化 < 0.008 不发。

**⚠ 代价（未解决）**：这个模型的**物理把头部角度锁死** —— 物理开着时 `ParamAngleX` 从 -24 扫到 +30，画面纹丝不动；物理一关立刻正常转。
所以现在的做法是**跟随开启期间挂起物理**，头发/裙摆的晃动随之停止。

```
物理开 + ParamAngleX 变化 = 头不动
物理关 + ParamAngleX 变化 = 头正常转
```

想两头都要，得找出 131 个物理设置里锁头部的那几个单独关掉 —— **没做**。

---

## 8. 调试方法论（这次学到的最值钱的东西）

### 8.1 不要只看参数值，要看画面

我犯的最大的错：读到 `ParamAngleX = 29.7` 就宣布"跟随生效了"，而图像根本纹丝不动。
**参数正确 ≠ 画面正确**，中间还隔着一层物理/动作/Core。

**验证必须端到端**：改完 → `renderer.extract.canvas()` 截图 → 人眼看 → 才算过。

### 8.2 测试路径要和真实路径一致

我有一次"测试通过"是因为测试脚本里**顺手把物理和动作都关了**，而真实运行时它们是开的。
后来加了一致的对比实验（只变一个变量）才找出真凶。

### 8.3 用一次性调试 HUD

排查跟随不生效时，在页面左上角贴了个读数框：

```
aim  -0.82, -0.82     ← Qt 推过来的
平滑 -0.82, -0.82     ← 阻尼后
角度 -24.7, 24.6      ← 实际写进模型的值
```

一眼就能判断断在哪一环。**这种 HUD 值得在排查任何"设置不生效"问题时先加。**

`demo_live2d.html` 里 `const DEBUG_HUD = true;` 可以关掉。

### 8.4 会咬人的小 bug
- `Math.round(x*100)*100/100` = `Math.round(x*100)` —— 我的取值函数把 29.47 显示成 2947，白排查了一轮（`x*1000/1000` 才对）
- 改 HTML 后 `edit` 报 `file has not been read` 说明是全新上下文，先 `read` 再改

### 8.5 常用排查片段

```js
// 看某个 Part 下有哪些 drawable、它们的颜色
var cm = l2d.model.internalModel.coreModel, m = cm._model;
m.drawables.parentPartIndices;   // Int32Array
m.drawables.multiplyColors;      // Float32Array，4 个一组

// 参数存在性 + 范围（注意 getParameterIndex 才靠谱）
var idx = cm.getParameterIndex('ParamAngleX');
cm.getParameterMinimumValue(idx); cm.getParameterMaximumValue(idx);

// 表达式到底改了什么 → 直接读 Exp3/*.exp3.json
```

---

## 9. 已知但没做的

| 项 | 说明 |
|---|---|
| 物理 + 头部跟随共存 | 见 §7.4，要挖 `_physicsRig` |
| 口型接真实麦克风 | 现在 `PARAM_TABS` 里只有手动滑块 |
| 透明桌宠拖拽 | `pyqt5_web.py` 里有个雏形 `make_pet_window()` |
| 部件开关面板 | 148 个 Part 可勾选显隐（用户提过，后来没要） |
| B站参考视频 | `BV1FccfzDE4S` 0:45 的摸头表现始终没看到（B站风控 HTTP 567，360P 匿名也拒），现在的手感是按常见摸头表情猜的 |

---

## 10. 关于这个模型的事实（省得重复探测）

| 项 | 值 |
|---|---|
| drawable 数 | 715 |
| Part 数 | 147 |
| 参数数 | 509 |
| 带 mask 的 drawable | 181（其中 51 个 inverted mask） |
| blendModes | `{0: 631, 1: 9, 2: 75}` |
| 贴图 | 5 × 4096 |
| 物理设置 | 131 |
| 表情 | 23（`Exp3/*.exp3.json`） |
| 动作组 | 8（`Animation/*.motion3.json`） |
| `ParamCheek` | 索引 509，**越界无效** |
| `＞＜` 表情 | 只设 `key5 = 1` |
