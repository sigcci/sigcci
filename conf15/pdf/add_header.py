# -*- coding: utf-8 -*-

import io
import os
import re
from glob import glob
from decimal import Decimal
from pypdf import PdfWriter, PdfReader
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# フォントファイルのパスを設定（WSL環境対応）
font_paths = [
    # WSL環境でWindowsフォントにアクセスする場合
    '/mnt/c/Windows/Fonts/yumin.ttf',
    # Ubuntuの日本語フォント
    '/usr/share/fonts/truetype/fonts-japanese-mincho.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',
    # その他の一般的な日本語フォントパス
    '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc',
    '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
]

# 利用可能なフォントを探して登録
font_registered = False
for font_path in font_paths:
    if os.path.exists(font_path):
        try:
            if font_path.endswith('.ttc'):
                # TTCファイルの場合はUnicodeCIDFontを使用
                pdfmetrics.registerFont(UnicodeCIDFont('Yu Mincho Regular'))
            else:
                pdfmetrics.registerFont(TTFont('Yu Mincho Regular', font_path))
            print(f"フォントを登録しました: {font_path}")
            font_registered = True
            break
        except Exception as e:
            print(f"フォント登録に失敗: {font_path} - {e}")
            continue

if not font_registered:
    print("警告: 日本語フォントが見つかりません。デフォルトフォントを使用します。")
    # デフォルトフォントとしてHelveticaを使用
    font_name = 'Helvetica'
else:
    font_name = 'Yu Mincho Regular'

# デフォルトのprefix
default_prefix = "SIG-CCI-009-"

def get_prefix():
    """ユーザーからprefixを取得する"""
    print(f"現在のprefix設定: {default_prefix}")
    user_input = input(f"prefixを変更しますか？ (現在: {default_prefix}) [Enter=そのまま使用]: ").strip()
    
    if user_input:
        # ハイフンがない場合は自動で追加
        if not user_input.endswith('-'):
            user_input += '-'
        return user_input
    return default_prefix

def find_and_rename_files(prefix):
    """既存ファイルの確認とリネーム処理"""
    # [0-9][0-9].pdf パターンのファイルを探す
    direct_files = glob("[0-9][0-9].pdf")
    
    if direct_files:
        print(f"処理対象ファイルが見つかりました: {direct_files}")
        return direct_files
    
    # prefix付きの[0-9][0-9].pdf パターンを探す
    prefixed_pattern = f"{prefix}[0-9][0-9].pdf"
    prefixed_files = glob(prefixed_pattern)
    
    if not prefixed_files:
        print(f"処理対象のファイルが見つかりません。")
        print(f"以下のパターンのファイルを探しました:")
        print(f"  - [0-9][0-9].pdf")
        print(f"  - {prefixed_pattern}")
        return []
    
    print(f"prefix付きファイルが見つかりました: {prefixed_files}")
    print("これらのファイルをリネームして処理を続行します。")
    
    # ユーザーに確認
    confirm = input("リネームを実行しますか？ [y/N]: ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("処理を中止しました。")
        return []
    
    renamed_files = []
    for old_file in prefixed_files:
        # prefixを除去した新しいファイル名を生成
        new_file = old_file.replace(prefix, "")
        
        # ファイル名が正しい形式かチェック
        if re.match(r'^[0-9][0-9]\.pdf$', new_file):
            try:
                os.rename(old_file, new_file)
                print(f"リネーム: {old_file} → {new_file}")
                renamed_files.append(new_file)
            except Exception as e:
                print(f"エラー: {old_file} のリネームに失敗しました - {e}")
        else:
            print(f"警告: {old_file} は正しい形式ではありません。スキップします。")
    
    return renamed_files

def process_pdf_files(prefix, files):
    """PDFファイルの処理"""
    if not files:
        return
    
    print(f"\n=== PDF処理開始 (prefix: {prefix}) ===")
    
    for filename in files:
        print(f"処理中: {filename}")
        out_filename = prefix + filename
        id = out_filename[:len(out_filename)-4]
        
        try:
            # PdfReaderでPDFを読み込み
            with open(filename, 'rb') as f:
                pdf = PdfReader(f)
                page = pdf.pages[0]
                
                # ヘッダー用のPDFを作成
                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=A4)
                
                font_size = 8
                can.setFont(font_name, font_size)
                can.setFillColor(Color(0, 0, 0, alpha=1))
                can.drawString(426, 812, "人工知能学会第二種研究会資料")
                can.drawString(474, 803, "市民共創知研究会")
                can.drawString(478, 794, id)
                
                can.save()
                
                # ヘッダーPDFを既存のページにマージ
                packet.seek(0)
                header_pdf = PdfReader(packet)
                page.merge_page(header_pdf.pages[0])
                
                # 出力用のPdfWriterを作成
                output = PdfWriter()
                output.add_page(page)
                
                # 残りのページを追加
                for i in range(1, len(pdf.pages)):
                    output.add_page(pdf.pages[i])
                
                # ファイルに保存
                with open(out_filename, "wb") as fout:
                    output.write(fout)
                    print(f"完了: {out_filename}")
                    
        except Exception as e:
            print(f"エラー: {filename} の処理中にエラーが発生しました - {e}")
            continue

def main():
    print("=== PDF ヘッダー追加ツール ===")
    
    # 1. prefixの確認と設定
    prefix = get_prefix()
    print(f"使用するprefix: {prefix}")
    
    # 2. ファイルの検索とリネーム
    files = find_and_rename_files(prefix)
    
    # 3. PDF処理
    process_pdf_files(prefix, files)
    
    print("\nすべての処理が完了しました。")

if __name__ == "__main__":
    main()