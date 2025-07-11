#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
import argparse

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

def main():
    parser = argparse.ArgumentParser(description='音声ファイルの変換')
    parser.add_argument('--reconvert-mp3', action='store_true', help='既存のMP3ファイルも最小サイズに変換')
    args = parser.parse_args()

    # ダウンロードフォルダのパスを取得
    downloads_dir = str(Path.home() / "Downloads")
    
    # 対応する音声ファイルの拡張子
    if args.reconvert_mp3:
        audio_extensions = ('.m4a', '.wav', '.mp3', '.webm')
    else:
        audio_extensions = ('.m4a', '.wav', '.webm')
    
    # ダウンロードフォルダ内の音声ファイルを検索
    for file in os.listdir(downloads_dir):
        if file.lower().endswith(audio_extensions):
            input_file = os.path.join(downloads_dir, file)
            # 変換を実行
            convert_to_mp3(input_file)

if __name__ == "__main__":
    main() 