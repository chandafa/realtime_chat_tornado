import tornado.ioloop
import tornado.web
import tornado.websocket

# List untuk menyimpan koneksi pengguna
connections = []

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        if self not in connections:
            connections.append(self)
            print("New connection")

    def on_message(self, message):
        for conn in connections:
            conn.write_message(message)

    def on_close(self):
        if self in connections:
            connections.remove(self)
            print("Connection closed")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/chatsocket", ChatSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server started on port 8888")
    tornado.ioloop.IOLoop.current().start()
