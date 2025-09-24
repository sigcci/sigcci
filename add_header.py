# -*- coding: utf-8 -*-

import io
import os
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

prefix = "SIG-CCI-009-"

# PDFファイルを処理
for filename in glob("[0-9][0-9].pdf"):
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

print("すべてのファイルの処理が完了しました。")