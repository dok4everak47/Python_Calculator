"""
热重载启动器 - 使用watchdog监控文件变化自动重启应用
"""

import os
import sys
import time
import subprocess
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self, restart_callback):
        self.restart_callback = restart_callback
        self.last_restart = 0
        self.restart_delay = 1  # 防抖延迟（秒）
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        # 只监控.py文件
        if event.src_path.endswith('.py'):
            current_time = time.time()
            # 防抖处理，避免频繁重启
            if current_time - self.last_restart > self.restart_delay:
                print(f"\n🔍 检测到文件变化: {os.path.basename(event.src_path)}")
                self.last_restart = current_time
                self.restart_callback()

class HotReloader:
    def __init__(self):
        self.process = None
        self.observer = None
        self.running = True
        
    def start_application(self):
        """启动主应用程序"""
        if self.process and self.process.poll() is None:
            # 如果进程还在运行，先终止
            self.process.terminate()
            self.process.wait()
            
        print("🚀 启动应用程序...")
        self.process = subprocess.Popen([sys.executable, 'main.py'])
        
    def stop_application(self):
        """停止应用程序"""
        if self.process:
            print("🛑 停止应用程序...")
            self.process.terminate()
            self.process.wait()
            
    def restart_application(self):
        """重启应用程序"""
        self.stop_application()
        self.start_application()
        
    def start_monitoring(self):
        """开始监控文件变化"""
        print("👀 开始监控文件变化...")
        print("监控目录: .")
        print("支持的文件类型: .py")
        print("按 Ctrl+C 停止监控")
        
        event_handler = CodeChangeHandler(self.restart_application)
        self.observer = Observer()
        self.observer.schedule(event_handler, '.', recursive=True)
        self.observer.start()
        
        # 首次启动应用
        self.start_application()
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 停止监控...")
        finally:
            self.cleanup()
            
    def cleanup(self):
        """清理资源"""
        self.running = False
        if self.observer:
            self.observer.stop()
            self.observer.join()
        self.stop_application()

def main():
    """主函数"""
    print("🔥 SciCalc Pro 热重载模式")
    print("=" * 40)
    
    # 检查是否安装了watchdog
    try:
        import watchdog
    except ImportError:
        print("❌ 未安装watchdog，请先安装:")
        print("pip install watchdog>=3.0.0")
        return
        
    reloader = HotReloader()
    reloader.start_monitoring()

if __name__ == "__main__":
    main()