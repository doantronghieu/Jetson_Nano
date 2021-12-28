from adafruit_platformdetect import Detector
detector = Detector()

print(f"Chip ID: {detector.chip.id}")
print(f'Board ID: {detector.board.id}')