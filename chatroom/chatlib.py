#-*- coding:utf-8 -*-

import socket
import pdb # like gdb tool
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# 使用參數
MAX_USER = 30  #可以容納的最大使用者數量
port = 10000
QUIT_COMMAND = '<$quit$>'


# 初始化及啟動socket
def socketInit(addr):
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #設定socket選項,設定供給某個IP的port使用完畢立刻斷開,1是True
    ss.setblocking(0) #flag:0 如果recv或send沒收到任何資料則回傳error,模擬timeout功能,此設計可以保持server有最大使用率
    ss.bind(addr)
    ss.listen(MAX_USER)
    print("socket Listening on", addr)
    return ss

class Lobby():
    def __init__(self):
        self.rooms = {}  #儲存格式： {room_id: Room}
        self.room_maping = {}  #儲存格式: {clientname: room_id}

    #新連線進來的socket client,請他輸入他的使用者id
    def new_socket_client(self, new_client):
        new_client.socket.sendall(u'you are first connection,\nPlease keyin your name:\n')

    #列出目前房間id的功能
    def list_room_id(self, user):
        #檢查目前是否有房間的存在,沒有則發出警報
        if len(self.rooms) == 0:
            msg = '目前沒有房間的存在,你可以用 [<join> room_name]來創立新房間\n'
            user.socket.sendall(msg.encode('utf-8'))
        else:
            msg = '目前現有房間列表\n'
            for room in self.rooms:
                msg += room + ":" +str(len(self.rooms[room].users)) + 'user(s)\n'  #rooms[room].users宣告在下面的class Room內
            user.socket.sendall(msg.encode('utf-8'))

    #處理房間相關的控制指令
    def handle_msg(self, user, msg):
        instructions = u'Instructions:\n'\
                        + u'[<list>] 列出所有房間id\n'\
                        + u'[<help>] 顯示所有控制指令\n'\
                        + u'[<quit>] 離開服務\n'\
                        + u'直接打字即可開始傳送訊息\n'

        print(user.name + "says: " + msg)
        if "name" in msg:
            name = msg.split()[1]
            user.name = name
            print("新連線從 ", user.name)
            user.socket.sendall(instructions)

        elif "<join>" in msg:
            same_room = False
            if len(msg.split()) >= 2: # error check
                room_name = msg.split()[1]
                if user.name in self.room_maping: # 切換房間
                    if self.room_maping[user.name] == room_name:  #如果使用者在指定的房間內則不事情
                        user.socket.sendall(u'你已在房間內' + room_name.encode('utf-8'))
                        same_room = True
                    else: #換房間囉～
                        old_room = self.room_maping[user.name]
                        self.rooms[old_room].remove_user(user) #將原本房間內的使用者移除

                if not same_room:
                    if not room_name in self.rooms: #如果使用者不在任何房間內
                        new_room = RoomFunction(room_name)
                        self.rooms[room_name] = new_room
                    self.rooms[room_name].users.append(user)  #將新的user加入他所選的房間
                    self.rooms[room_name].welcome_new(user)
                    self.room_maping[user.name] = room_name
            else:
                user.socket.sendall(instructions)

        elif "<list>" in msg:
            self.list_room_id(user)

        elif "<help>" in msg:
            user.socket.sendall(instructions)

        elif "<quit>" in msg:
            user.socket.sendall(QUIT_COMMAND.encode('utf-8'))
            self.remove_user(user)

        else:
            #確認user有沒有在房間裡面或者使用者不是房間內排在第一位的user
            if user.name in self.room_maping:
                self.rooms[self.room_maping[user.name]].broadcast(user, msg.encode('utf-8'))
            else:
                msg = u'你目前不在房間內\n'\
                    + u'用<list> 看目前所有房間\n'\
                    + u'用<join> 選擇欲加入的房間\n'
                user.socket.sendall(msg.encode('utf-8'))

        #將user的socket 物件移除
    def remove_user(self, user):
        if user.name in self.room_maping:
            self.rooms[self.room_maping[user.name]].remove_user(user)
            del self.room_maping[user.name]
        print ("user: " + user.name + "已經離開\n")

#房間內的事件紀錄
class RoomFunction():
    def __init__(self, name):
        self.users = []  #socket物件的list
        self.name = name

    def welcome_new(self, from_user):
        msg = self.name + u"歡迎" + from_user.name + '\n'
        for user in self.users:
            user.socket.sendall(msg.encode('utf-8'))

    def broadcast(self, from_user, msg):
        msg = from_user.name.encode('utf-8') + u":" + msg
        for user in self.users:
            user.socket.sendall(msg)

    def remove_user(self, user):
        self.users.remove(user)
        leave_msg = user.name.encode('utf-8') + u"已經離開房間\n"
        self.broadcast(user, leave_msg)

#使用者相關socket資訊
class User:
    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name

    def fileno(self):
        return self.socket.fileno()
