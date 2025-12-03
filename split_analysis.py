import os
from pathlib import Path

def analyze_project_split(root_dir):
    """تقسیم تحلیل به بخش‌های کوچک‌تر"""
    
    INCLUDE_EXTENSIONS = {
        '.py', '.js', '.jsx', '.ts', '.tsx',
        '.json', '.yaml', '.yml', '.toml',
        '.md', '.txt', '.env.example',
        '.html', '.css', '.scss', '.ipynb'
    }
    
    EXCLUDE_DIRS = {
        'node_modules', '__pycache__', '.git', 
        'venv', 'env', '.venv', 'dist', 'build',
        '.next', '.cache', 'coverage', '.pytest_cache',
        'output'  # فایل‌های HTML خروجی رو نادیده بگیر
    }
    
    # فایل‌های بزرگ HTML رو نادیده بگیر
    EXCLUDE_FILES = {'bias_3d_interactive.html', 'bias_radar.html'}
    
    print("🔍 در حال اسکن پروژه...\n")
    
    all_files = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        
        for file in files:
            if file.startswith('.') or file in EXCLUDE_FILES:
                continue
            
            ext = Path(file).suffix.lower()
            if ext not in INCLUDE_EXTENSIONS:
                continue
                
            file_path = Path(root) / file
            all_files.append(file_path)
    
    print(f"📊 پیدا شد: {len(all_files)} فایل\n")
    
    # تقسیم به چند فایل خروجی
    output_files = []
    max_size = 1.5 * 1024 * 1024  # 1.5 مگابایت
    
    part = 1
    current_file = None
    current_size = 0
    files_in_part = 0
    
    for file_path in sorted(all_files):
        relative = file_path.relative_to(root_dir)
        
        # اگه فایل خیلی بزرگه، رد کن
        try:
            file_size = file_path.stat().st_size
            if file_size > 500 * 1024:  # بزرگتر از 500KB
                print(f"⏭️  رد شد (خیلی بزرگ): {relative}")
                continue
        except:
            continue
        
        # فایل جدید بساز اگه لازمه
        if current_file is None or current_size > max_size:
            if current_file:
                current_file.write(f"\n{'='*80}\n")
                current_file.write(f"✅ {files_in_part} فایل در این بخش\n")
                current_file.write(f"{'='*80}\n")
                current_file.close()
            
            output_path = os.path.join(root_dir, f"analysis_part_{part}.txt")
            current_file = open(output_path, 'w', encoding='utf-8')
            output_files.append(output_path)
            current_size = 0
            files_in_part = 0
            
            current_file.write("="*80 + "\n")
            current_file.write(f"📦 بخش {part} - تحلیل پروژه MENA Agentic AI Eval\n")
            current_file.write("="*80 + "\n\n")
            
            part += 1
        
        # خواندن و نوشتن فایل
        try:
            with open(file_path, 'r', encoding='utf-8') as source:
                content = source.read()
            
            current_file.write("\n" + "="*80 + "\n")
            current_file.write(f"📄 فایل: {relative}\n")
            current_file.write("="*80 + "\n")
            current_file.write(content)
            current_file.write("\n\n")
            
            current_size += len(content.encode('utf-8'))
            files_in_part += 1
            
            print(f"✓ افزودن شد: {relative}")
            
        except Exception as e:
            print(f"✗ خطا: {relative} - {str(e)}")
    
    # بستن آخرین فایل
    if current_file:
        current_file.write(f"\n{'='*80}\n")
        current_file.write(f"✅ {files_in_part} فایل در این بخش\n")
        current_file.write(f"{'='*80}\n")
        current_file.close()
    
    # نمایش نتیجه
    print("\n" + "="*80)
    print(f"🎉 تمام! {len(output_files)} فایل ساخته شد:\n")
    for i, f in enumerate(output_files, 1):
        size = os.path.getsize(f) / (1024 * 1024)
        print(f"  {i}. {os.path.basename(f)} ({size:.2f} MB)")
    print("="*80)
    print("\n📤 آماده آپلود! فایل‌ها رو یکی یکی اینجا بفرست\n")
    
    return output_files

if __name__ == "__main__":
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    
    print("🚀 شروع تقسیم‌بندی پروژه...\n")
    print("-"*80 + "\n")
    
    try:
        output = analyze_project_split(PROJECT_PATH)
        print("\n✨ موفق!")
    except Exception as e:
        print(f"\n❌ خطا: {str(e)}")