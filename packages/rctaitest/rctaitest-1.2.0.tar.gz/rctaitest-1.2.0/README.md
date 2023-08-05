# rctaitest &middot; [![Build status](https://travis-ci.org/rctaitestProject/rctaitest.svg?branch=master)](https://travis-ci.org/rctaitestProject/rctaitest)

**Cross-Platform UI Automation Framework for Games and Apps**

**跨平台的UI自动化框架，适用于游戏和App** （[中文版点这里](./README_zh.md)）


![image](./demo.gif)


## Features

*   **Write Once, Run Anywhere:** rctaitest provides cross-platform APIs, including app installation, simulated input, assertion and so forth. rctaitest uses image recognition technology to locate UI elements so that you can automate games and apps without injecting any code. 

*   **Fully Scalable:** rctaitest cases can be easily run on large device farms, using commandline or python API. HTML reports with detailed info and screen recording allow you to quickly locate failure points. NetEase builds [Airlab](https://airlab.163.com/) on top of the rctaitest Project.

*   **rctaitestIDE:** rctaitestIDE is an out of the box GUI tool that helps to create and run cases in a user-friendly way. rctaitestIDE supports a complete automation workflow: ``create -> run -> report``.

*   **Poco:** [Poco](https://github.com/rctaitestProject/Poco) adds the ability to directly access object(UI widget) hierarchy across the major platforms and game engines. It allows writing instructions in Python, to achieve more advanced automation.

Get started from [rctaitest homepage](http://rctaitest.netease.com/)

#### [Supported Platforms](./docs/wiki/device/platforms.md)


## Installation

Use `pip` to install the rctaitest python library. 

```Shell
pip install -U rctaitest
```

On MacOS/Linux platform, you need to grant adb execute permission.

```Shell
# for mac
cd {your_python_path}/site-packages/rctaitest/core/android/static/adb/mac
# for linux
# cd {your_python_path}/site-packages/rctaitest/core/android/static/adb/linux
chmod +x adb
```

Download rctaitestIDE from our [homepage](http://rctaitest.netease.com/) if you need to use the GUI tool.


## Documentation

You can find the complete rctaitest documentation on [readthedocs](http://rctaitest.readthedocs.io/).


## Examples

rctaitest aims at providing platform-independent API so that you can write automated cases once and run it on multiple devices and platforms.

1. Using [connect_device](http://rctaitest.readthedocs.io/en/latest/README_MORE.html#connect-device) API you can connect to any android/iOS device or windows application.
1. Then perform [simulated input](http://rctaitest.readthedocs.io/en/latest/README_MORE.html#simulate-input) to automate your game or app.
1. **DO NOT** forget to [make assertions](http://rctaitest.readthedocs.io/en/latest/README_MORE.html#make-assertion) of the expected result. 

```Python
from rctaitest.core.api import *

# connect an android phone with adb
init_device("Android")
# or use connect_device api
# connect_device("Android:///")

install("path/to/your/apk")
start_app("package_name_of_your_apk")
touch(Template("image_of_a_button.png"))
swipe(Template("slide_start.png"), Template("slide_end.png"))
assert_exists(Template("success.png"))
keyevent("BACK")
home()
uninstall("package_name_of_your_apk")
```

For more detailed info, please refer to [rctaitest Python API reference](http://rctaitest.readthedocs.io/en/latest/all_module/rctaitest.core.api.html) or take a look at [API code](./rctaitest/core/api.py)


## Running ``.air`` cases from CLI

Using rctaitestIDE, you can easily create automated cases as ``.air`` directories.
rctaitest CLI provides the possibility to execute cases on different host machines and target device platforms without using rctaitestIDE itself.

```Shell
# run cases targeting on Android phone connected to your host machine via ADB
rctaitest run "path to your .air dir" --device Android:///

# run cases targeting on Windows application whose title matches Unity.*
rctaitest run "path to your .air dir" --device "Windows:///?title_re=Unity.*"

# generate HTML report after running cases
rctaitest report "path to your .air dir"

# or use as a python module
python -m rctaitest run "path to your .air dir" --device Android:///
```

Try running provided example case: [``rctaitest/playground/test_blackjack.air``](./playground/test_blackjack.air) and see [Usage of CLI](http://rctaitest.readthedocs.io/en/latest/README_MORE.html#running-air-from-cli). Here is a [multi-device runner sample](https://github.com/rctaitestProject/multi-device-runner).


## Contribution

Pull requests are very welcome. 


## Thanks

Thanks for all these great works that make this project better.

- [stf](https://github.com/openstf)
- [atx](https://github.com/NetEaseGame/ATX)
- [pywinauto](https://github.com/pywinauto/pywinauto)
