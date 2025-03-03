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

    command = [
        "python", "single_inference.py",
        "--content_to_synthesize", content,
        "--speaker_prompt_text_transcription", prompt_text,
        "--speaker_prompt_audio_path", audio_file,
        "--output_path", output_audio  # 加入 output_path 參數
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
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
    title="Text-to-Speech 合成 Demo",
    description="請輸入要轉換的文本，提供對應的參考音訊和文本內容，進行語音合成。"
)

if __name__ == "__main__":
    demo.launch(share=True)