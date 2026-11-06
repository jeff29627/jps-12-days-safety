"""Usage: python make_qr.py https://USERNAME.github.io/jps-12-days-safety/"""
import sys
import qrcode
if len(sys.argv)!=2 or not sys.argv[1].startswith('https://'):
    raise SystemExit('Usage: python make_qr.py https://YOUR-USERNAME.github.io/jps-12-days-safety/')
qrcode.make(sys.argv[1]).save('jps-game-qr.png')
print('Created jps-game-qr.png')
