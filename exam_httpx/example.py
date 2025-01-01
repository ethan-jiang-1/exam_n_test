import asyncio
from pathlib import Path
from downloader import WebDownloader, download_page

async def main():
    # 示例 1: 使用 WebDownloader 类
    print("示例 1: 使用 WebDownloader 类下载页面")
    downloader = WebDownloader(timeout=30)
    content = await downloader.download_page("https://python.org")
    print(f"下载完成，内容长度: {len(content)} 字符\n")
    
    # 示例 2: 下载并保存到文件
    print("示例 2: 下载并保存到文件")
    save_path = Path("downloads/python.html")
    await downloader.download_page("https://python.org", save_path)
    print(f"文件已保存到: {save_path}\n")
    
    # 示例 3: 使用便捷函数
    print("示例 3: 使用便捷函数下载")
    content = await download_page("https://httpbin.org/html")
    print(f"使用便捷函数下载完成，内容长度: {len(content)} 字符\n")
    
    # 示例 4: 错误处理
    print("示例 4: 错误处理示例")
    try:
        await downloader.download_page("https://thiswebsitedoesnotexist.com/")
    except Exception as e:
        print(f"预期中的错误发生: {e}\n")

if __name__ == "__main__":
    # 创建下载目录
    Path("downloads").mkdir(exist_ok=True)
    # 运行异步主函数
    asyncio.run(main()) 