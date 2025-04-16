# 音声ファイル変換ツール

このツールは、Mac のダウンロードフォルダ内の音声ファイル（.m4a, .wav）を MP3 形式に変換します。

## セットアップ方法（初心者向け）

以下のコマンドを順番にターミナルにコピー＆ペーストして実行するだけで、セットアップが完了します。

### 1. Homebrew のインストール

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Homebrew のパス設定（Apple Silicon Mac の場合）

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

### 2. Homebrew のパス設定（Intel Mac の場合）

```bash
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

### 3. ffmpeg のインストール

```bash
brew install ffmpeg
```

### 4. 変換ツールのダウンロード

```bash
cd ~/Documents
git clone https://github.com/jeq/convert-mp3.git
cd convert-mp3
chmod +x convert_audio.py
```

### 5. エイリアスの設定

```bash
echo 'alias mp3="~/Documents/convert-mp3/convert_audio.py"' >> ~/.zshrc
source ~/.zshrc
```

## 使用方法

### 基本的な使い方

1. 変換したい音声ファイル（.m4a, .wav）をダウンロードフォルダに配置します。
2. 以下のコマンドをターミナルで実行します：

```bash
mp3
```

### コマンドオプション

既存の MP3 ファイルも含めて最小サイズに変換:

```bash
mp3 --reconvert-mp3
```

## 変換結果

処理中は以下のような情報が表示されます：

```
変換成功: example.mp3
元のサイズ: 10.50MB
変換後サイズ: 1.25MB
圧縮率: 88.1%
```

## 機能

- ダウンロードフォルダ内の.m4a と.wav ファイルを自動検出
- 検出したファイルを MP3 形式に変換（最小サイズ設定）
  - ビットレート: 64kbps
  - サンプリングレート: 22.05kHz
  - チャンネル: モノラル
  - 品質設定: 最小サイズ

## 注意事項

- 元のファイルは削除されません
- 変換された MP3 ファイルは元のファイルと同じ名前で、拡張子が.mp3 になります
- 既に MP3 ファイルが存在する場合は上書きされます
