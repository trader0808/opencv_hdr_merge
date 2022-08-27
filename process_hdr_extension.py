from pathlib import Path
import cv2

current_folder = Path().resolve()

filename = "hdr"
hdr_path = str(Path(current_folder, filename + ".hdr"))


img = cv2.imread(hdr_path,flags=cv2.IMREAD_ANYDEPTH)

import matplotlib.pyplot as plt

plt.imshow(img)
plt.axis('off')
result_path = Path(current_folder, filename + '.png')
plt.savefig(result_path)