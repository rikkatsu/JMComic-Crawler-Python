# Python API For JMComic (禁漫天堂)

封装了一套可用于爬取JM的Python API.

简单来说，就是可以通过简单的几行Python代码，实现下载JM上的本子到本地，并且是处理好的图片.

**友情提示：珍爱JM，为了减轻JM的服务器压力，请不要一次性爬取太多本子，西门🙏🙏🙏**.

## 安装教程

* 通过pip官方源安装（推荐，并且更新也是这个命令）

  ```shell
  pip install jmcomic -i https://pypi.org/project --upgrade
  ```
* 本地安装

  ```shell
  pip install -e ./
  ```

## 快速上手

使用下面的两行代码，即可实现功能：把某个本子（album）里的所有章节（photo）下载到本地

```python
import jmcomic  # 导入此模块，需要先安装.
jmcomic.download_album('422866')  # 传入要下载的album的id，即可下载整个album到本地.
# 上面的这行代码，还有一个可选参数option: JmOption，表示配置项，
# 配置项的作用是告诉程序下载时候的一些选择，
# 比如，要下载到哪个文件夹，使用怎样的路径组织规则（比如[/作者/本子id/图片] 或者 [/作者/本子名称/图片]）.
# 如果没有配置，则会使用 JmOption.default()，下载的路径是[当前工作文件夹/本子名称/图片].
# 如果你想要配置，请参考文件 assets/config/常用配置介绍.yml
```

* v2.2.9: 新增命令行调用方式，上述的代码可以转为一行命令

```bash
# 下载album_id为422866的本子
$ jmcomic 422866
# 更多用法请参考文件 usage/usage_cl.py (命令行使用介绍)
```

## 进阶使用

进阶使用可以参考本repo下usage文件夹内的示例代码文件，下面是各个文件的作用，你可以挑感兴趣的阅读：

- API上手介绍: `getting_started.py`
- 命令行使用介绍: `usage_cl.py`
- 配置客户端的实现（网页端、移动端）: `usage_configure_client_impl.py`
- 使用API实现简单功能: `usage_simple.py`
- 演示jmcomic模块的可自定义功能点: `usage_custom.py`
- 使用API的Filter过滤功能: `usage_feature_filter.py`
- 演示jmcomic模块的Plugin插件体系: `usage_feature_plugin.py`
- 演示一个综合使用实例: `usage_advanced.py`
  - 包括6个功能需求的介绍、实现方案和完整运行日志
  - 实现方案非常简洁，充分jmcomic的便利性，以及强大的插件扩展机制

以及一些趣味用法：

- 测试你的ip可以访问哪些禁漫域名: `pick_domain.py`
- 基于GitHub Actions下载本子: `workflow_download.py`

## 项目特点

- **绕过Cloudflare的反爬虫**
- 支持使用**命令行**下载本子，无需写Python代码，简单易用
- 支持使用**GitHub Actions**下载本子，网页上直接输入本子id就能下载（[教程：使用GitHub Actions下载禁漫本子](./assets/docs/教程：使用GitHub%20Actions下载禁漫本子.md)）
- 支持**网页端**和**移动端**两种客户端实现，可通过配置切换（**移动端不限ip兼容性好，网页端限制ip地区但效率高**）
- 支持**自动重试和域名切换**机制
- **多线程下载**（可细化到一图一线程，效率极高）
- 跟进了JM最新的图片分割算法（2023-02-08）
- **可配置性强**

  - 不配置也能使用，十分方便
  - 配置可以从**配置文件**生成，支持多种文件格式
  - 配置点有：`请求域名` `客户端实现` `是否使用磁盘缓存` `同时下载的章节/图片数量` `图片格式转换` `下载路径规则` `请求元信息（headers,cookies,proxies）`等
- **可扩展性强**

  - **支持Plugin插件，可以方便地扩展功能，以及使用别人的插件**
    - 目前内置支持的插件有：`登录插件` `硬件占用监控插件` `只下载新章插件` `压缩文件插件`
  - 支持自定义本子/章节/图片下载前后的回调函数
  - 支持自定义debug日志
  - 支持自定义类：`Downloader（负责调度）` `Option（负责配置）` `Client（负责请求）` `实体类`等

## 使用小说明

* Python >= 3.7
* 个人项目，文档和示例会有不及时之处，可以Issue提问

## 项目文件夹介绍

* assets：存放一些非代码的资源文件

  * config：存放配置文件
  * docs：项目文档
* src：存放源代码

  * jmcomic：`jmcomic`模块
* tests：测试目录，存放测试代码，使用unittest
* usage：用法目录，存放示例/使用代码

## 感谢以下项目

### 图片分割算法代码+禁漫移动端API

[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=tonquer&repo=JMComic-qt)](https://github.com/tonquer/JMComic-qt)
