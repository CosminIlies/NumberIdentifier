from consts import SCREEN_SIZE
from drawing import drawing_frame
from threading import Thread

grid = [[0] * SCREEN_SIZE for i in range(SCREEN_SIZE)]

drawing_tread = Thread(target=lambda: drawing_frame(grid))
drawing_tread.start()

from AiModel import AiModel

model = AiModel()

drawing_tread.join()

model.predict(grid)
