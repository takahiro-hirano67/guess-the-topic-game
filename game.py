"""ゲームのコアロジックを管理するモジュール"""

from typing import List, Dict, Tuple, Optional
from config import llm_client, LLM_NAME
from system_prompt import SYSTEM_PROMPT
from topics import get_random_topic

def process_game_turn(
    messages: List[Dict[str, str]],
    user_input: str,
    topic: Optional[str] = None
) -> Tuple[str, List[Dict[str, str]], str]:
    """
    ゲームの1ターンを処理します。

    Args:
        messages: これまでのチャット履歴（メッセージ配列）
        user_input: ユーザーからの入力文字列
        topic: 現在のお題（初回はNoneで渡す）

    Returns:
        Tuple[AIの回答, 更新後のメッセージ配列, 現在のお題]
    """
    # 初回実行時の初期化
    if topic is None:
        topic = get_random_topic()
        # システムプロンプトをメッセージ配列の先頭に挿入
        messages.append({
            "role": "system",
            "content": SYSTEM_PROMPT.format(topic=topic),
        })

    # ユーザーの入力を追加
    messages.append({"role": "user", "content": user_input})

    try:
        # LLMによる生成
        response = llm_client.chat.completions.create(
            model=LLM_NAME,
            messages=messages,
            reasoning_effort=None, # 思考オフ
        )

        assistant_reply = response.choices[0].message.content or ""

        # AIの回答を履歴に追加
        messages.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply, messages, topic

    except Exception as e:
        # エラーハンドリング
        error_msg = f"エラーが発生しました: {e}"
        return error_msg, messages, topic
