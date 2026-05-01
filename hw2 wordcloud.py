import tkinter as tk
from tkinter import filedialog, messagebox
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class EnglishWordCloudApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Article Word Cloud (Top 20 Words)")
        self.root.geometry("600x500")

        # 介面佈局
        tk.Label(root, text="Article Text:", font=("Arial", 10)).pack(anchor="nw", padx=10, pady=5)
        
        self.text_area = tk.Text(root, font=("Arial", 10), undo=True)
        self.text_area.pack(expand=True, fill="both", padx=10, pady=5)

        # 按鈕列
        btn_frame = tk.Frame(root)
        btn_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        tk.Button(btn_frame, text="Open .txt File", command=self.load_file).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Generate Word Cloud", command=self.generate_cloud).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Save Word Cloud", command=self.save_image).pack(side="left", padx=5)

        self.current_wc = None

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, f.read())

    def generate_cloud(self):
        raw_text = self.text_area.get(1.0, tk.END).strip()
        if not raw_text:
            messagebox.showwarning("Warning", "Text area is empty!")
            return

        # --- 1. 運用 Hash 技巧統計詞頻 ---
        # 使用正規表達式只抓取英文字母，並轉為小寫
        words = re.findall(r'\b[a-z]{2,}\b', raw_text.lower())
        
        # 定義 Stop Words (排除常見無意義字彙)
        stop_words = {
            'the', 'and', 'are', 'is', 'it', 'to', 'for', 'of', 'in', 'on', 'with', 
            'as', 'at', 'by', 'an', 'be', 'this', 'that', 'was', 'were'
        }
        
        # 建立 Hash Table (Dictionary)
        word_counts = {}
        for w in words:
            if w not in stop_words:
                # 核心 Hash 操作
                word_counts[w] = word_counts.get(w, 0) + 1
        
        # 排序並取出前 20 名
        top_20 = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20])

        if not top_20:
            messagebox.showinfo("Info", "No valid words found to generate cloud.")
            return

        # --- 2. 呼叫函式畫成文字雲 ---
        self.current_wc = WordCloud(
            background_color="white",
            width=800,
            height=600,
            colormap='viridis' # 設定顏色風格
        ).generate_from_frequencies(top_20)

        # 彈出視窗顯示
        plt.figure(figsize=(10, 7))
        plt.imshow(self.current_wc, interpolation='bilinear')
        plt.axis("off")
        plt.show()

    def save_image(self):
        if self.current_wc:
            path = filedialog.asksaveasfilename(defaultextension=".png")
            if path:
                self.current_wc.to_file(path)
                messagebox.showinfo("Success", "Saved successfully!")
        else:
            messagebox.showwarning("Warning", "Generate a cloud first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnglishWordCloudApp(root)
    root.mainloop()
