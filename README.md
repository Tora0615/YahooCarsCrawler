# YahooCarsCrawler
A crawler can get all cars' info from https://autos.yahoo.com.tw/

Only when crawl cars's data, the data has exceeded 350,000 storage cells

一個可以從 Yahoo 汽機車(https://autos.yahoo.com.tw/) 爬取資料的爬蟲。

僅爬取汽車資料時，就已超過350,000個存儲格。

## Example Data

| 品牌ID | 品牌名稱       | 生產年份 | 型號名稱           | 型號ID | 年份型號合併              | 版本ID | 版本名稱        | 新車售價 | 動力型式 | 引擎型式                       | 排氣量    | 最大馬力          | 最大扭力            | 驅動型式 | 變速系統  | 前輪懸吊 | 後輪懸吊 | 煞車型式 | 輪胎尺碼(前)   | 輪胎尺碼(後)   | 車型分類  | 車門數 | 座位數   | 車長     | 車寬     | 車高     | 車重     | 軸距     | 市區油耗       | 高速油耗       | 平均油耗       | 牌照稅    | 燃料稅   |
| ---- | ---------- | ---- | -------------- | ---- | ------------------- | ---- | ----------- | ---- | ---- | -------------------------- | ------ | ------------- | --------------- | ---- | ----- | ---- | ---- | ---- | --------- | --------- | ----- | --- | ----- | ------ | ------ | ------ | ------ | ------ | ---------- | ---------- | ---------- | ------ | ----- |
| 1    | Alfa Romeo | 2008 | 159            | 101  | 2008 159            | 5001 | 1.9 JTDM    | 182  | 柴油   | 渦輪增壓, 直列4缸, DOHC雙凸輪軸, 16氣門 | 1910cc | 150hp@4000rpm | 32.6kgm@2000rpm | 前輪驅動 | 6速自手排 | 雙A臂  | 多連桿  | 前後碟煞 | 225/50R17 | 225/50R17 | 轎車    | 4門  | 5人座   | 4660mm | 1828mm | 1417mm | 1535kg | 2700mm | 11.6km/ltr | 16.4km/ltr | 13.3km/ltr | 11230元 | 3726元 |
| 1    | Alfa Romeo | 2008 | 159            | 101  | 2008 159            | 5002 | 2.4 JTDM    | 209  | 柴油   | 渦輪增壓, 直列5缸, DOHC雙凸輪軸, 20氣門 | 2387cc | 200hp@4000rpm | 40.8kgm@2000rpm | 前輪驅動 | 6速自手排 | 雙A臂  | 多連桿  | 前後碟煞 | 225/50R17 | 225/50R17 | 轎車    | 4門  | 5人座   | 4660mm | 1828mm | 1422mm | 1630kg | 2700mm | 10.7km/ltr | 15.5km/ltr | 12.5km/ltr | 11230元 | 3726元 |
| 1    | Alfa Romeo | 2008 | 159            | 101  | 2008 159            | 5003 | 3.2 JTS Q4  | 259  | 汽油   | 自然進氣, V型6缸, DOHC雙凸輪軸, 24氣門 | 3195cc | 260hp@6200rpm | 32.8kgm@4500rpm | 四輪驅動 | 6速自手排 | 雙A臂  | 多連桿  | 前後碟煞 | 225/50R17 | 225/50R17 | 轎車    | 4門  | 5人座   | 4660mm | 1828mm | 1422mm | 1680kg | 2700mm |            |            |            | 28220元 | 8640元 |
| 1    | Alfa Romeo | 2008 | 159 Sportwagon | 102  | 2008 159 Sportwagon | 5004 | 2.4 JTDM    | 219  | 柴油   | 渦輪增壓, 直列5缸, DOHC雙凸輪軸, 20氣門 | 2387cc | 200hp@4000rpm | 40.8kgm@2000rpm | 前輪驅動 | 6速自手排 | 雙A臂  | 多連桿  | 前後碟煞 | 225/50R17 | 225/50R17 | 轎式旅行車 | 5門  | 5人座   | 4660mm | 1828mm | 1425mm | 1680kg | 2700mm | 8.1km/ltr  | 11.7km/ltr | 10.1km/ltr | 11230元 | 3726元 |
| 1    | Alfa Romeo | 2008 | Brera          | 103  | 2008 Brera          | 5005 | 3.2 JTS Q4  | 288  | 汽油   | 自然進氣, V型6缸, DOHC雙凸輪軸, 24氣門 | 3195cc | 260hp@6200rpm | 32.8kgm@4500rpm | 四輪驅動 | 6速自手排 | 雙A臂  | 多連桿  | 前後碟煞 | 225/50R17 | 225/50R17 | 雙門轎跑車 | 2門  | 4人座   | 4410mm | 1830mm | 1341mm | 1630kg | 2528mm |            |            |            | 28220元 | 8640元 |
