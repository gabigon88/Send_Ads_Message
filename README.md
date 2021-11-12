# Send_Ads_Message
練習實作在中國多個熱門網站自動發送廣告訊息  

發垃圾訊息可拆成兩個步驟
1. 要先知道發送對象 ---> 爬蟲找到user名單 ---> 以requests實現
2. 執行批次發送訊息 ---> 自動化執行批次發送 ---> 以selenium實現

當初網上查了資料後，挑選幾個中國熱門的社群網站，想發垃圾訊息  
1. 新浪
   + sina_send_message.py
2. 百度貼吧
   + tieba_crawler.py
3. 天涯論壇
   + tianya_crawler.py
   + tianya_messager.py

但實作了這麼多網站發現，中國各大網站 早就針對發送垃圾訊息做各種千奇百怪的花式阻擋了  
簡單總結的話是: 發現經常對 "非好友的人" 發送訊息很快就會被鎖  
一般加好友要經過雙向同意，基本上你發垃圾訊息一定是對方沒按過同意  

最後這些code雖然沒實用性，但就留作紀念留存吧  