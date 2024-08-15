from Player import Player
from mode import Mode
from flask import Flask
from flask import Response


app = Flask(__name__)
player = Player("resources/01－A Puma at Large.wav")


@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <script type="text/css">
        iframe {
            height:0px;
            width:0px;
        }
    </script>
</head>
<body>
    <a href="http://127.0.0.1:5000/start" target="iframeName">start</a> <br>
    <a href="http://127.0.0.1:5000/repeat" target="iframeName">repeat</a> <br>
    <a href="http://127.0.0.1:5000/pause" target="iframeName">pause</a> <br>
    <a href="http://127.0.0.1:5000/resume" target="iframeName">resume</a> <br>
    <a href="http://127.0.0.1:5000/stop" target="iframeName">stop</a> <br>

    <hr>
    <a href="http://127.0.0.1:5000/set_a" target="iframeName">set_a</a> <br>
    <a href="http://127.0.0.1:5000/set_b" target="iframeName">set_b</a> <br>
    <a href="http://127.0.0.1:5000/quit_ab_repeat" target="iframeName">quit_ab_repeat</a> <br>

    <iframe src="" frameborder="0" name="iframeName"></iframe> <br>
</body>
</html>
    """


@app.route("/start")
def start():
    player.start()
    print("/start")
    return Response()


@app.route("/repeat")
def repeat():
    player.set_mode(Mode.REPEAT)
    print("/repeat")
    return Response()


@app.route("/pause")
def pause():
    player.pause()
    print("/pause")
    return Response()


@app.route("/resume")
def resume():
    player.resume()
    print("/resume")
    return Response()


@app.route("/stop")
def stop():
    player.stop()
    print("/stop")
    return Response()


@app.route("/set_a")
def set_a():
    player.set_a()
    print("/set_a")
    return Response()


@app.route("/set_b")
def set_b():
    player.set_b()
    print("/set_b")
    return Response()


@app.route("/quit_ab_repeat")
def quit_ab():
    player.quit_ab()
    print("/quit_ab")
    return Response()


if __name__ == '__main__':
    app.run()
