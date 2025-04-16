# 音声ファイル変換ツール

このツールは、Mac のダウンロードフォルダ内の音声ファイル（.m4a, .wav）を MP3 形式に変換します。

## 必要条件

- macOS
- Python 3.6 以上
- ffmpeg

## インストール方法

1. Homebrew のインストール（まだインストールしていない場合）:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

インストール後、Homebrew が PATH に追加されていない場合は、以下のコマンドを `.bash_profile` または `.zshrc` に追加します:

```bash
# Homebrew の環境変数設定
eval "$(/opt/homebrew/bin/brew shellenv)"  # Apple Silicon Mac の場合
# または
eval "$(/usr/local/bin/brew shellenv)"     # Intel Mac の場合
```

2. ffmpeg のインストール:

```bash
brew install ffmpeg
```

3. スクリプトの実行権限を付与:

```bash
chmod +x ~/Documents/convert-mp3-main/convert_audio.py
```

4. エイリアスの設定:

以下を`~/.bash_profile`または`~/.zshrc`に追加します（macOS のバージョンによって異なります）:

```bash
alias mp3='~/Documents/convert-mp3-main/convert_audio.py'
```

設定を反映するために、以下のコマンドを実行するか、ターミナルを再起動します:

```bash
source ~/.bash_profile  # または source ~/.zshrc
```

## 使用方法

### 基本的な使い方

1. 変換したい音声ファイル（.m4a, .wav）をダウンロードフォルダに配置します。
2. 以下のコマンドを実行します：

```bash
mp3
```

### コマンドオプション

既存の MP3 ファイルも含めて最小サイズに変換:

```bash
mp3 --reconvert-mp3
```

## 進捗状況の表示

処理中は以下のような進捗状況が表示されます：

1. 変換時:

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

## 出力

- 変換された MP3 ファイルは元のファイルと同じ場所に保存
  - 変換前後のファイルサイズと圧縮率を表示
  - ファイルサイズを最小限に抑える設定を使用

## 注意事項

- 元のファイルは削除されません
- 変換された MP3 ファイルは元のファイルと同じ名前で、拡張子が.mp3 になります
- 既に MP3 ファイルが存在する場合は上書きされます
- `--reconvert-mp3`オプションを使用すると、既存の MP3 ファイルも最小サイズに変換されます
