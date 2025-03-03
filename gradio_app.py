import gradio as gr
import subprocess
import os
from datetime import datetime

def synthesize_audio(content, prompt_text, audio_file):
    if not content:
        return "請輸入要合成的文本", None
    if not prompt_text:
        return "請輸入參考音訊的文本內容", None
    if not audio_file:
        return "請上傳參考音訊", None

    # 生成基於當前時間的輸出檔案名稱
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    output_audio = f"output_{current_time}.wav"

    # 構建命令行命令
    command = [
        "python", "single_inference.py",  # 確保這裡的路徑是正確的
        "--content_to_synthesize", content,
        "--speaker_prompt_text_transcription", prompt_text,
        "--speaker_prompt_audio_path", audio_file,
        "--output_path", output_audio  # 加入 output_path 參數
    ]

    try:
        # 執行命令
        result = subprocess.run(command, capture_output=True, text=True)

        # 檢查是否生成音訊檔案
        if result.returncode == 0 and os.path.exists(output_audio):
            return "合成完成！", output_audio
        else:
            return f"錯誤: {result.stderr}", None
    except Exception as e:
        return f"執行錯誤: {str(e)}", None

# 建立 Gradio 介面
demo = gr.Interface(
    fn=synthesize_audio,
    inputs=[
        gr.Textbox(label="輸入要合成的文本"),
        gr.Textbox(label="輸入參考音訊的文本內容"),
        gr.Audio(label="選擇參考音訊", type="filepath")
    ],
    outputs=[
        gr.Textbox(label="狀態"),
        gr.Audio(label="合成音訊", type="filepath")
    ],
    examples=[
        # 範例 1：文本、參考文本、參考音訊路徑
        ["今天天氣真好",
         "我們從您的文字中看見了您對生命的熱情與對世界的深刻觀察，您是我們這個時代的思想領袖",
         "./data/chen_very_short.wav"],

        # 範例 2：文本、參考文本、參考音訊路徑
        ["這是一個測試",
         "我們從您的文字中看見了您對生命的熱情與對世界的深刻觀察，您是我們這個時代的思想領袖",
         "./data/chen_very_short.wav"],
    ],
    title="Text-to-Speech 合成 Demo",
    description="請輸入要轉換的文本，提供對應的參考音訊和文本內容，進行語音合成。"
)

if __name__ == "__main__":
    demo.launch(share=True)