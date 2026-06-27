#!/usr/bin/env python3
"""HTTPS static server สำหรับ Photo Booth (ใช้กล้องบนมือถือ/อุปกรณ์อื่นในวง LAN ได้)"""
import http.server, ssl, socket, os

PORT = 8443
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80)); return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain("cert.pem", "key.pem")

httpd = http.server.HTTPServer(("0.0.0.0", PORT), http.server.SimpleHTTPRequestHandler)
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

ip = lan_ip()
print("=" * 52)
print("  📸  Photo Booth · Pride  — HTTPS server พร้อมแล้ว")
print("=" * 52)
print(f"  เครื่องนี้   :  https://localhost:{PORT}")
print(f"  มือถือ/อื่น :  https://{ip}:{PORT}")
print("-" * 52)
print("  มือถือจะเตือน 'ไม่ปลอดภัย' (cert ทำเอง) —")
print("  กด Advanced / รายละเอียด -> Proceed / ไปต่อ ได้เลย")
print("  ปิดเซิร์ฟเวอร์: กด Ctrl+C")
print("=" * 52)
httpd.serve_forever()
