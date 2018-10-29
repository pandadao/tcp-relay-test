#!/usr/bin/python
# encoding: utf-8

from asyncore import dispatcher
from asynchat import async_chat
import socket, asyncore

PORT = 6666 #端口

class EndSession(Exception):
    """
    自定義會話結束時的異常
    """
    pass

class CommandHandler:
    """
    命令處理類
    """

    def unknown(self, session, cmd):
        '響應未知命令'
        session.push('Unknown command: %sn' % cmd)

    def handle(self, session, line):
        '命令處理'
        if not line.strip():
            return
        parts = line.split(' ', 1)
        cmd = parts[0]
        try:
            line = parts[1].strip()
        except IndexError:
            line = ''
        meth = getattr(self, 'do_' + cmd, None)
        try:
            meth(session, line)
        except TypeError:
            self.unknown(session, cmd)

class Room(CommandHandler):
    """
    包含多個用戶的環境，負責基本的命令處理和廣播
    """

    def __init__(self, server):
        self.server = server
        self.sessions = []

    def add(self, session):
        '一個用戶進入房間'
        self.sessions.append(session)

    def remove(self, session):
        '一個用戶離開房間'
        self.sessions.remove(session)

    def broadcast(self, line):
        '向所有的用戶發送指定消息'
        for session in self.sessions:
            session.push(line)

    def do_logout(self, session, line):
        '退出房間'
        raise EndSession

class LoginRoom(Room):
    """
    剛登錄的用戶的房間
    """

    def add(self, session):
        '用戶連接成功的回應'
        Room.add(self, session)
        session.push('Connect Success')

    def do_login(self, session, line):
        '登錄命令處理'
        name = line.strip()
        if not name:
            session.push('UserName Empty')
        elif name in self.server.users:
            session.push('UserName Exist')
        else:
            session.name = name
            session.enter(self.server.main_room)

class ChatRoom(Room):
    """
    聊天用的房間
    """

    def add(self, session):
        '廣播新用戶進入'
        session.push('Login Success')
        self.broadcast(session.name + ' has entered the room.n')
        self.server.users[session.name] = session
        Room.add(self, session)

    def remove(self, session):
        '廣播用戶離開'
        Room.remove(self, session)
        self.broadcast(session.name + ' has left the room.n')

    def do_say(self, session, line):
        '客戶端發送消息'
        self.broadcast(session.name + ': ' + line + 'n')

    def do_look(self, session, line):
        '查看在線用戶'
        session.push('Online Users:n')
        for other in self.sessions:
            session.push(other.name + 'n')

class LogoutRoom(Room):
    """
    用戶退出時的房間
    """

    def add(self, session):
        '從服務器中移除'
        try:
            del self.server.users[session.name]
        except KeyError:
            pass

class ChatSession(async_chat):
    """
    負責和單用戶通信
    """

    def __init__(self, server, sock):
        async_chat.__init__(self, sock)
        self.server = server
        self.set_terminator('n')
        self.data = []
        self.name = None
        self.enter(LoginRoom(server))

    def enter(self, room):
        '從當前房間移除自身，然後添加到指定房間'
        try:
            cur = self.room
        except AttributeError:
            pass
        else:
            cur.remove(self)
        self.room = room
        room.add(self)

    def collect_incoming_data(self, data):
        '接受客戶端的數據'
        self.data.append(data)

    def found_terminator(self):
        '當客戶端的一條數據結束時的處理'
        line = ''.join(self.data)
        self.data = []
        try:
            self.room.handle(self, line)
        except EndSession:
            self.handle_close()

    def handle_close(self):
        async_chat.handle_close(self)
        self.enter(LogoutRoom(self.server))

class ChatServer(dispatcher):
    """
    聊天服務器
    """

    def __init__(self, port):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        self.users = {}
        self.main_room = ChatRoom(self)

    def handle_accept(self):
        conn, addr = self.accept()
        ChatSession(self, conn)

if __name__ == '__main__':
    s = ChatServer(PORT)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print
