# import matplotlib.pyplot as plt
# import pandas as pd
# import matplotlib.font_manager as fm
# import io

# def table_to_image(table_markdown: str, font_path: str = None) -> io.BytesIO:
#     # Load Japanese font (fallback to NotoSansCJK or IPA)
#     if not font_path:
#         jp_fonts = [f for f in fm.findSystemFonts(fontext='ttf') if 'NotoSansCJK' in f or 'IPA' in f or 'YuGothic' in f or 'msgothic' in f.lower()]
#         if not jp_fonts:
#             raise RuntimeError("No Japanese font found. Please specify font_path manually.")
#         font_path = jp_fonts[0]

#     prop = fm.FontProperties(fname=font_path)

#     # Parse markdown table
#     lines = [line.strip() for line in table_markdown.strip().split('\n') if '|' in line]

#     if len(lines) < 3:
#         raise ValueError("Invalid table format")

#     headers = [h.strip() for h in lines[0].split('|') if h.strip()]
#     rows = []
#     for line in lines[2:]:
#         row = [cell.strip() for cell in line.split('|') if cell.strip()]
#         if len(row) == len(headers):
#             rows.append(row)

#     if not rows:
#         raise ValueError("No valid data rows found")

#     df = pd.DataFrame(rows, columns=headers)

#     # Create plot
#     fig, ax = plt.subplots(figsize=(14, len(df) * 0.7))
#     ax.axis('off')

#     table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')

#     table.auto_set_font_size(False)
#     table.set_fontsize(10)
#     table.scale(1.2, 1.5)

#     # ✅ Set font on cell text correctly
#     for key, cell in table.get_celld().items():
#         cell.get_text().set_fontproperties(prop)

#     # Save as PNG image
#     buf = io.BytesIO()
#     plt.savefig(buf, format='png', bbox_inches='tight')
#     buf.seek(0)
#     plt.close(fig)

#     return buf
