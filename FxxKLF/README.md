# FxxKLF

目标是买到周边。（估计也不行😅）

## 准备工作

1. Selenium的安装

   一个自动化测试工具，利用它我们可以驱动浏览器执行特定的动作，如点击、下拉等等操作。

   Selenium安装好之后，并不能直接使用，它需要与浏览器进行对接。这里拿Chrome浏览器为例。若想使用Selenium成功调用Chrome浏览器完成相应的操作，需要通过ChromeDriver来驱动。

2. ChromeDriver的安装

   [ChromeDriver的官方下载地址](https://chromedriver.storage.googleapis.com/index.html)

   找到自己电脑上的Chrome浏览器版本，根据你电脑系统的平台类型进行下载。

   - windows：下载完成之后，解压，将其放置在Python安装路径下Scripts文件夹中即可。

   - MacOS：跟python同级目录即可

   上述操作结束后，我们执行如下命令，测试一下

   ```python
   from selenium import webdriver
   # 打开Chrome浏览器
   browser = webdriver.Chrome()
   ```

   若成功打开了浏览器，则证明你的ChromeDriver安装的没问题，可以正常愉快地使用Selenium了。

## 参考

[用Python完成毫秒级抢单，助你秒杀淘宝大单](https://juejin.im/post/6844903860750778382)