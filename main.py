"""
Script chạy tất cả các file generate theo đúng thứ tự
"""
import subprocess
import sys

def run_script(script_name):
    """Chạy một script Python và kiểm tra kết quả"""
    print(f"\n{'='*60}")
    print(f"🚀 Đang chạy: {script_name}")
    print('='*60)
    
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    
    if result.returncode != 0:
        print(f"\n❌ Lỗi khi chạy {script_name}!")
        return False
    return True

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║     KTPM - GENERATE ALL TEST DATA FOR ORANGEHRM          ║
╠══════════════════════════════════════════════════════════╣
║  Thứ tự chạy:                                            ║
║  1. generate_dim.py        (Nhân viên, Users)            ║
║  2. generate_time_attendance.py (Time & Attendance)      ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    scripts = [
        'generate_dim.py',           
        'generate_time_attendance.py', 
    ]
    
    success_count = 0
    
    for script in scripts:
        if run_script(script):
            success_count += 1
        else:
            print(f"\n⚠️ Dừng lại do lỗi ở {script}")
            break
    
    print(f"\n{'='*60}")
    print(f"📊 KẾT QUẢ: {success_count}/{len(scripts)} scripts chạy thành công")
    print('='*60)
    
    if success_count == len(scripts):
        print("""✅ HOÀN THÀNH! Tất cả dữ liệu đã được tạo.""")

if __name__ == "__main__":
    main()
