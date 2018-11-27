# -*- coding:utg-8 -*-

'''
client 和server連接的流程:
1. 建立server的監聽窗口,綁定server主機的ip和port,保持Listen狀態來接受client連線請求
2. client根據server的ip和port發出連線請求,連接到server的socket上,client socket 需要提供自己的socket fd,以便讓server socket回應
3. 當server監聽到client連接請求時,回應client的請求,建立一個新的thread,把server fd發送給client
4. 處理完之後server繼續Listen其他client的連線請求,通過socket連接戶發data通訊
'''

import socket
import select
import thread

# server Information: port: 5963, address: 0.0.0.0
port = 5963
server_addr = ("0.0.0.0", port)

# table儲存房間id跟socket物件,來方便查找
# chatroom_id\socket物件 conn1, conn2
# 0
# 1
# 3
inputs = []
# client的nick name,  fd:file descriptor
fd_name = {}

# 初始化server端的socket狀態
def serverInit():
    ss = socket.socket()    #創建server socket
    ss.bind(server_addr)    #綁定server的IP和port
    ss.listen(10)           #可同時在port監聽的最大數量
    return ss               #回傳初始化後的server socket

# // TODO: event handler,處理連線事件,尚未規劃細節

# // TODO: 建立一個新的socket連接

# // TODO: 產生chatroom_id,回傳房間id給發出請求的client,將發出請求的client加進inputs這個table中

# // TODO: 搜尋chatroom_id並且將發出1.2.請求的client加進對應的表格位置上

# // TODO: 關閉連線



def run():
    ss = serverInit()
    print "Server has initialized"
    inputs.append([])
    inputs[0].append(ss) #第一個連接上server的client一定沒有在table中,因此先創建第一欄儲存這一筆資訊
    while True:
        # rlist, wlist, elist = select.select(inputs, [], inputs, 100) #如果只是server開啟,100秒內沒有client連接就當作timeout關閉連線
        # //TODO: ***這個部份要另外開一份thread去處理才對
        for i in range(len(inputs)):
            rlist, wlist, elist = select.select(inputs[i], [], [])  #此處的inputs[0]是檢查第一間聊天室內是否有連線的數量
            #當沒有可讀的fd時,表示server錯誤,關閉連線
            if not rlist:
                print "time out..."
                ss.close()
                break
            for r in rlist:

if __name__ == "__main__":
    run()
