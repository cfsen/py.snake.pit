"""
Creates composite images for a set of image sets, following a 
naming scheme with an identifier at the end. Uses alpha values
to determine the boundaries for cropping.
"""
import numpy as np
import cv2 as cv
from os import listdir
from os.path import isfile, isdir, join
from pathlib import Path
from matplotlib import pyplot

def boundaries_find(png: np.ndarray, offset: int = 0) -> dict:
    non_zero_indices = np.argwhere(png != 0)
    if non_zero_indices.size == 0:
        return None
    
    y_min = np.min(non_zero_indices[:, 0]) + offset
    y_max = np.max(non_zero_indices[:, 0]) + offset
    x_min = np.min(non_zero_indices[:, 1]) + offset
    x_max = np.max(non_zero_indices[:, 1]) + offset
    width = x_max - x_min + offset
    height = y_max - y_min + offset

    return {"y_min": y_min, "y_max": y_max, "x_min": x_min, 
            "x_max": x_max, "width": width, "height": height}

def set_generator(tags: list) -> dict:
    set = {}
    for t in tags:
        set[t] = [None, None, None]
    return set


def process_batch(files: list, tags: list, allow_incomplete: bool = False, 
        composites_dir: str = "composites", apply_caption: bool = False) -> bool:
    buffer_set = set_generator(tags)
    processed = matched = 0
    sets = []
    for f in files:
        for w in buffer_set:
            if(f[-len(w)-4:-4] == w and buffer_set[w][0] is None):
                buffer_set[w][0] = f
                matched += 1
                break

        processed += 1
        
        if(processed == len(tags)):
            if (processed != matched and not allow_incomplete):
                raise ValueError("Unable to match tags to files.")
            sets.append(buffer_set)
            buffer_set = set_generator(tags)
            processed = matched = 0

    for working_set in sets:
        canvas_y = canvas_x = 0
        for w in working_set:
            if working_set[w][0] is not None:
                working_set[w][1] = cv.cvtColor(cv.imread(join(raw_dir, working_set[w][0]), 
                                                cv.IMREAD_UNCHANGED), cv.COLOR_BGRA2RGBA)
            if working_set[w][1] is not None:
                working_set[w][2] = boundaries_find(working_set[w][1][:,:,3])
                if(canvas_y < working_set[w][2]["height"]): 
                    canvas_y = working_set[w][2]["height"]
                canvas_x += working_set[w][2]["width"]

        canvas = cv.cvtColor(np.zeros((canvas_y, canvas_x, 4), np.uint8), cv.COLOR_RGB2RGBA)
        
        cur = 0
        for w in working_set:
            i = working_set[w]
            offset_y = 0
            if(i[2]["height"] < canvas_y):
                offset_y = canvas_y - i[2]["height"]
            canvas[offset_y:i[2]["height"]+offset_y, 
                   cur:cur+i[2]["width"]] = i[1][i[2]["y_min"]:i[2]["y_max"], 
                                                 i[2]["x_min"]:i[2]["x_max"]]
            cur+=i[2]["width"]
    

        fname = working_set[tags[0]][0][:-4-len(tags[0])]

        if(apply_caption):
            canvas[canvas_y-100:canvas_y, 0:canvas_x] = [0,0,0,255]
            canvas = cv.putText(canvas, fname, (35, canvas_y-30), 
                                cv.FONT_HERSHEY_SIMPLEX, 2, (255,255,255,255), 2, cv.LINE_AA)
            
        canvas = cv.cvtColor(canvas, cv.COLOR_RGBA2BGRA)
        fname = fname + ".png"

        cv.imwrite(join(composites_dir, fname), canvas)
        
if(__name__ == '__main__'):
    tags = ["Profile", "3Q", "3Q Above", "Above", "Front"]

    raw_dir = join(Path.cwd(), "raw")
    composites_dir = join(Path.cwd(), "composite")
    files = [f for f in listdir(raw_dir)]
    working_set = set_generator(tags)
    process_batch(files=files, tags=tags, apply_caption=True, 
        allow_incomplete=True, composites_dir=composites_dir)

    print("Processing complete.")