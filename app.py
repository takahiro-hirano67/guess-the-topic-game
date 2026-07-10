"""Flask Webアプリケーションのメインエントリーポイント"""

import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from game import process_game_turn

app = Flask(__name__)
# セッション用のシークレットキー
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default-secret-key-for-dev")

@app.route("/")
def index():
    """
    メインページを表示します。
    """
    # セッションの初期化（存在しない場合のみ）
    if "messages" not in session:
        session["messages"] = []
    if "topic" not in session:
        session["topic"] = None

    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    """
    ユーザーのメッセージを処理し、AIの回答を返します。
    """
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "メッセージが空です"}), 400

    # セッションから履歴とお題を取得
    messages = session.get("messages", [])
    topic = session.get("topic")

    # ゲームロジックの処理
    # sessionに保存されているリストを直接編集せず、コピーを渡す
    current_messages = list(messages)
    reply, updated_messages, current_topic = process_game_turn(
        current_messages, user_input, topic
    )

    # セッションを更新
    session["messages"] = updated_messages
    session["topic"] = current_topic

    return jsonify({"reply": reply})

@app.route("/reveal", methods=["POST"])
def reveal():
    """
    正解（お題）を開示します。
    """
    topic = session.get("topic")
    if not topic:
        return jsonify({"error": "現在ゲームが進行していません"}), 400

    return jsonify({"topic": topic})

@app.route("/reset", methods=["POST"])
def reset():
    """
    ゲームの状態をリセットします。
    """
    session.pop("messages", None)
    session.pop("topic", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
