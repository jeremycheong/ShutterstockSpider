# ShutterstockSpider
Shutterstock Spider   


图片爬取分两步，先使用`analysis_page`方法将图片url获取并保存到txt中，有三种图片格式，分别是小图（无水印），中图（一个logo水印），原图（大量logo水印） 

图片下载使用`download_from_file`方法，后端建议使用`_wget_download_image`下载
