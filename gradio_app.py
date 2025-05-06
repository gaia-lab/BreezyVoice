import gradio as gr
import subprocess
import os
from datetime import datetime
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=7860, help='指定啟動的 port')
    return parser.parse_args()

def synthesize_audio(content, prompt_text, audio_file, speed):
    if not content:
        return "請輸入要合成的文本", None, None
    if not prompt_text:
        return "請輸入參考音訊的文本內容", None, None
    if not audio_file:
        return "請上傳參考音訊", None, None

    # 生成基於當前時間的輸出檔案名稱
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    output_audio = f"output_{current_time}.wav"

    # 構建命令行命令
    command = [
        "python", "single_inference.py",  # 確保這裡的路徑是正確的
        "--content_to_synthesize", content,
        "--speaker_prompt_text_transcription", prompt_text,
        "--speaker_prompt_audio_path", audio_file,
        "--output_path", output_audio
    ]

    try:
        # 執行命令
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            return f"錯誤: {result.stderr}", None, None

        # 如果 speed != 1.0，使用 ffmpeg 調整速度
        if speed != 1.0:
            adjusted_audio = output_audio.replace(".wav", f"_{speed}.wav")
            ffmpeg_cmd = [
                "ffmpeg", "-i", output_audio,
                "-filter:a", f"atempo={speed}",
                "-y", adjusted_audio
            ]
            subprocess.run(ffmpeg_cmd, check=True)
            return "合成並調整速度完成！", output_audio, adjusted_audio

        return "合成完成！", output_audio, None

    except Exception as e:
        return f"執行錯誤: {str(e)}", None, None

# 建立 Gradio 介面
demo = gr.Interface(
    fn=synthesize_audio,
    inputs=[
        gr.Textbox(label="輸入要合成的文本"),
        gr.Textbox(label="輸入參考音訊的文本內容"),
        gr.Audio(label="選擇參考音訊", type="filepath"),
        gr.Slider(minimum=0.5, maximum=2.0, step=0.1, value=1.0, label="語速")
    ],
    outputs=[
        gr.Textbox(label="狀態"),
        gr.Audio(label="合成音訊", type="filepath"),
        gr.Audio(label="調整後音訊 (如果有調速)", type="filepath")
    ],
    examples=[
        ["今天天氣真好", "這是一段測試文本", "./data/chen_very_short.wav", 1.2],
        ["你好，我是 AI 語音合成", "這是一段測試文本", "./data/chen_very_short.wav", 0.8]
    ],
    title="Text-to-Speech 合成 Demo",
    description="請輸入要轉換的文本，提供對應的參考音訊和文本內容，並選擇語速進行語音合成。"
)

if __name__ == "__main__":
    args = get_args()
    demo.launch(share=True, server_port=args.port)
