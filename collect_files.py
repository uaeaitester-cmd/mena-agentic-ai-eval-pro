import os
from pathlib import Path

def collect_project_files(root_dir, output_file=None):
    """
    جمع‌آوری تمام فایل‌های پروژه در یک فایل متنی
    """
    # تعیین مسیر خروجی
    if output_file is None:
        output_file = os.path.join(root_dir, "project_analysis.txt")
    
    print(f"📁 پوشه پروژه: {root_dir}")
    print(f"📄 فایل خروجی: {output_file}")
    
    # فرمت‌های فایل مورد نظر
    INCLUDE_EXTENSIONS = {
        '.py', '.js', '.jsx', '.ts', '.tsx',
        '.json', '.yaml', '.yml', '.toml',
        '.md', '.txt', '.env.example',
        '.html', '.css', '.scss', '.ipynb'
    }
    
    # پوشه‌هایی که نباید اسکن بشن
    EXCLUDE_DIRS = {
        'node_modules', '__pycache__', '.git', 
        'venv', 'env', '.venv', 'dist', 'build',
        '.next', '.cache', 'coverage', '.pytest_cache'
    }
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # نوشتن header
            f.write("=" * 80 + "\n")
            f.write(f"تحلیل کامل پروژه: {Path(root_dir).name}\n")
            f.write("=" * 80 + "\n\n")
            
            # ساختار پروژه
            f.write("📂 ساختار پروژه:\n")
            f.write("-" * 80 + "\n")
            write_tree_structure(root_dir, f, EXCLUDE_DIRS)
            f.write("\n" + "=" * 80 + "\n\n")
            
            # محتوای فایل‌ها
            f.write("📄 محتوای فایل‌ها:\n")
            f.write("=" * 80 + "\n\n")
            
            file_count = 0
            for root, dirs, files in os.walk(root_dir):
                # حذف پوشه‌های غیرضروری
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
                
                for file in sorted(files):
                    if file.startswith('.'):
                        continue
                    ext = Path(file).suffix.lower()
                    if ext in INCLUDE_EXTENSIONS:
                        file_path = Path(root) / file
                        relative_path = file_path.relative_to(root_dir)
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8') as source:
                                content = source.read()
                                
                            f.write("\n" + "=" * 80 + "\n")
                            f.write(f"📄 فایل: {relative_path}\n")
                            f.write("=" * 80 + "\n")
                            f.write(content)
                            f.write("\n\n")
                            file_count += 1
                            
                            print(f"✓ پردازش شد: {relative_path}")
                            
                        except Exception as e:
                            print(f"✗ خطا در {relative_path}: {str(e)}")
            
            # آمار نهایی
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"✅ تعداد کل فایل‌های پردازش شده: {file_count}\n")
            f.write("=" * 80 + "\n")
        
        print(f"\n🎉 فایل خروجی آماده شد: {output_file}")
        print(f"📊 تعداد فایل: {file_count}")
        return output_file
        
    except PermissionError:
        print(f"❌ خطا: دسترسی به فایل {output_file} رو نداری!")
        print("💡 سعی کن پوشه دیگه‌ای انتخاب کنی یا VS Code رو با Admin اجرا کن")
        return None
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {str(e)}")
        return None

def write_tree_structure(root_dir, file, exclude_dirs, prefix="", max_depth=4):
    """نمایش ساختار درختی پروژه"""
    if max_depth == 0:
        return
    
    try:
        items = sorted(Path(root_dir).iterdir(), key=lambda x: (not x.is_dir(), x.name))
        for i, item in enumerate(items):
            if item.name in exclude_dirs or item.name.startswith('.'):
                continue
                
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            file.write(f"{prefix}{current_prefix}{item.name}")
            
            if item.is_dir():
                file.write("/\n")
                extension = "    " if is_last else "│   "
                write_tree_structure(item, file, exclude_dirs, 
                                   prefix + extension, max_depth - 1)
            else:
                try:
                    size = item.stat().st_size / 1024  # KB
                    file.write(f" ({size:.1f} KB)\n")
                except:
                    file.write("\n")
    except PermissionError:
        pass

# استفاده
if __name__ == "__main__":
    # پوشه فعلی (محل اسکریپت)
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    
    print("🚀 شروع جمع‌آوری فایل‌ها...")
    print("-" * 80)
    
    output = collect_project_files(PROJECT_PATH)
    
    if output:
        print("\n" + "=" * 80)
        print(f"✨ حالا فایل '{os.path.basename(output)}' رو آپلود کن!")
        print("=" * 80)
    else:
        print("\n❌ متأسفانه مشکلی پیش اومد!")