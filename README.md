# voice_conversion_v1

## 概要
SPTKを用いた統計的声質変換

## 必要環境
- pythonとrequirements.txtにあるライブラリがインストールされていること
- SPTKとsox.exeがインストールされていて、パスが通っていること

## フォルダ構成
- wav/
    - train/
        - [name1]/
        - [name2]/
        - ...
    - production/
        - [name1]/
        - [name2]/
        - ...
- mcep/
    - [name1]/
    - [name2]/
    - ...
- mcep_aligned/
    - [name1_to_name2]/
        - [name1]/
            - text/
        - [name2]/
            - text/
        - graph/
    - ...
- train_result/
    - [name1_to_name2]/

## 実行方法
name1の音声をname2に変換する場合

1. wav/train/にフォルダname1/とname2/を作り、学習データとなるname1の音声ファイルとname2の音声ファイルを格納する
    - 内容は同じでなければならない
    - 同じ内容の音声でファイル名を同じにする
2. wav/production/にフォルダname1/を作り、name2の声に変換したいname1の音声ファイルを格納する
3. setting.txtで計算パラメータを指定
4. main.pyでVoiceConverterのコンストラクタの第1引数に'name1'を、第2引数に'name2'を指定してrun()を実行
5. wav/production/name2/に、wav/production/name1/にある音声ファイルからname2の声に変換したものが出力される

## その他のツール
- resynthesis_test.py 音声ファイルからピッチとメルケプストラムを抽出し、変換を行わずに両者から音声を再合成する
- audio_file_analyzer.py 任意のWavファイルのチャンネル数やサンプリング周波数などを調べる
