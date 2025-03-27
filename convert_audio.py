#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
import whisper
from dotenv import load_dotenv
import json
from datetime import datetime
import argparse

# 環境変数の読み込み
load_dotenv()

# グローバル変数としてモデルを保持
whisper_model = None

def convert_to_mp3(input_file):
    """音声ファイルをMP3に変換する"""
    input_path = Path(input_file)
    output_path = input_path.with_suffix('.mp3')
    
    try:
        # 一時ファイルのパスを設定
        temp_path = output_path.with_suffix('.temp.mp3')
        
        # ffmpegを使用して変換（最小サイズ）
        cmd = [
            'ffmpeg',
            '-i', str(input_path),
            '-codec:a', 'libmp3lame',
            '-b:a', '64k',     # ビットレートを64kbpsに設定（最小サイズ）
            '-ar', '22050',    # サンプリングレートを22.05kHzに設定
            '-ac', '1',        # モノラルに設定
            '-q:a', '9',       # 品質設定を最低に設定（0-9、9が最小サイズ）
            str(temp_path)
        ]
        subprocess.run(cmd, check=True)
        
        # 変換前後のファイルサイズを表示
        original_size = input_path.stat().st_size / (1024 * 1024)  # MB
        converted_size = temp_path.stat().st_size / (1024 * 1024)  # MB
        print(f"変換成功: {output_path}")
        print(f"元のサイズ: {original_size:.2f}MB")
        print(f"変換後サイズ: {converted_size:.2f}MB")
        print(f"圧縮率: {(1 - converted_size/original_size) * 100:.1f}%")
        
        # 一時ファイルを最終的な出力ファイルに移動
        if output_path.exists():
            output_path.unlink()  # 既存のファイルを削除
        temp_path.rename(output_path)  # 一時ファイルをリネーム
        
        return str(output_path)
    except subprocess.CalledProcessError as e:
        print(f"変換エラー: {e}")
        if temp_path.exists():
            temp_path.unlink()  # エラー時に一時ファイルを削除
        return None
    except Exception as e:
        print(f"予期せぬエラー: {e}")
        if temp_path.exists():
            temp_path.unlink()  # エラー時に一時ファイルを削除
        return None

def load_whisper_model(model_name="large"):
    """Whisperモデルを読み込む"""
    global whisper_model
    
    if whisper_model is None:
        print(f"Whisperモデル '{model_name}' を読み込んでいます...")
        # キャッシュディレクトリをユーザーのホームディレクトリに設定
        cache_dir = Path.home() / ".whisper_cache"
        cache_dir.mkdir(exist_ok=True)
        os.environ["XDG_CACHE_HOME"] = str(cache_dir)
        
        # 警告を非表示にする
        import warnings
        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
        
        whisper_model = whisper.load_model(model_name)
        print("モデルの読み込みが完了しました")
    
    return whisper_model

def transcribe_audio(audio_path, model_name="large"):
    """音声ファイルを文字起こしする"""
    try:
        print("文字起こしを開始します...")
        
        # モデルの読み込み（既に読み込まれている場合は再利用）
        model = load_whisper_model(model_name)
        
        print("音声ファイルを処理中...")
        # 文字起こしの実行
        result = model.transcribe(audio_path)
        
        print("結果を保存中...")
        # 結果の保存
        output_dir = Path.home() / "Downloads" / "transcriptions"
        output_dir.mkdir(exist_ok=True)
        
        # 元のファイル名を取得（拡張子なし）
        original_filename = Path(audio_path).stem
        output_file = output_dir / f"{original_filename}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"文字起こし結果を保存しました: {output_file}")
        return result["text"]
    except Exception as e:
        print(f"文字起こしエラー: {e}")
        return None

def format_transcription(text):
    """文字起こし結果を構造化された形式に整形する"""
    # ここにプロンプトに基づいた整形ロジックを実装
    # 現時点では単純なテキストを返す
    return text

def process_audio_file(input_file, transcribe_only=False, model_name="large"):
    """音声ファイルを処理する"""
    print(f"\n処理開始: {input_file}")
    
    if transcribe_only:
        # 文字起こしのみ実行
        transcription = transcribe_audio(input_file, model_name)
    else:
        # MP3に変換してから文字起こし
        mp3_path = convert_to_mp3(input_file)
        if mp3_path:
            transcription = transcribe_audio(mp3_path, model_name)
    
    if transcription:
        formatted_text = format_transcription(transcription)
        print("\n文字起こし結果:")
        print(formatted_text)

def main():
    parser = argparse.ArgumentParser(description='音声ファイルの変換と文字起こし')
    parser.add_argument('--transcribe', action='store_true', help='文字起こしを実行')
    parser.add_argument('--reconvert-mp3', action='store_true', help='既存のMP3ファイルも最小サイズに変換')
    parser.add_argument('--model', default="large", help='使用するWhisperモデル（base, small, medium, large）')
    args = parser.parse_args()

    # ダウンロードフォルダのパスを取得
    downloads_dir = str(Path.home() / "Downloads")
    
    # 対応する音声ファイルの拡張子
    if args.reconvert_mp3:
        audio_extensions = ('.m4a', '.wav', '.mp3')
    else:
        audio_extensions = ('.m4a', '.wav')
    
    # ダウンロードフォルダ内の音声ファイルを検索
    for file in os.listdir(downloads_dir):
        if file.lower().endswith(audio_extensions):
            input_file = os.path.join(downloads_dir, file)
            # 変換を実行
            mp3_path = convert_to_mp3(input_file)
            
            # 文字起こしオプションが指定されている場合
            if args.transcribe and mp3_path:
                process_audio_file(mp3_path, transcribe_only=True, model_name=args.model)

if __name__ == "__main__":
    main() 