import sys
from enum import Enum

class COLORS(Enum):
    white       = 0
    yellow      = 1
    cyan        = 2
    green       = 3
    magenta     = 4
    red         = 5
    blue        = 6
    black       = 7


BAR_COLOR = [
    [ 255, 255, 255 ],  # 100% White
    [ 255, 255,   0 ],  # Yellow
    [   0, 255, 255 ],  # Cyan
    [   0, 255,   0 ],  # Green
    [ 255,   0, 255 ],  # Magenta
    [ 255,   0,   0 ],  # Red
    [   0,   0, 255 ],  # Blue
    [   0,   0,   0 ],  # Black
]

if __name__ == "__main__":
    args        = sys.argv
    source      = args[1]
    target      = args[2]
    color       = None
    comp_path   = args[3]
    blend_path  = args[4]
    epsilon     = int(args[5])

    if len(args) > 7:
        color = [int(args[6]), int(args[7]), int(args[8])]
        assert color[0] <= 255 and color[1] <= 255 and color[2] <= 255, "The pixel is out of range"
    else:
        color = eval("COLORS." + args[6]).value
        color = BAR_COLOR[color]
    
    source_d = None
    with open(source, "r") as f:
        source_d = f.read()

    target_d = None
    with open(target, "r") as f:
        target_d = f.read()

    source_d = source_d.split("\n")
    target_d = target_d.split("\n")
    

    height, width   = source_d[1].split()
    height          = int(height)
    width           = int(width)
    pixel_limit     = int(source_d[2])
    result_image    = source_d[:3]
    blend_image     = source_d[:3]
    source_d        = source_d[3:]
    target_d        = target_d[3:]
    succesfull      = 0
    error           = 0

    for i in range(width):
        src_row     = list(map(int,source_d[i].split()))
        target_row  = list(map(int,target_d[i].split()))
        result_row  = []
        blend_row   = []
        for j in range(height):
            if  abs(src_row[j * 3]      - target_row[j * 3])        < epsilon   and \
                abs(src_row[j * 3 + 1]  - target_row[j * 3 + 1])    < epsilon   and \
                abs(src_row[j * 3 + 2]  - target_row[j * 3 + 2])    < epsilon: # the pixel is the same.
                succesfull += 1
                result_row += src_row[j*3 : j*3 + 3]
                
            else: # the pixel is wrong
                result_row += color
                error += 1
            blend_row += [abs(src_row[j * 3]      - target_row[j * 3]), abs(src_row[j * 3 + 1]  - target_row[j * 3 + 1]), abs(src_row[j * 3 + 2]  - target_row[j * 3 + 2])]
        result_image.append(
            " ".join(list(map(str, result_row))) # convert every element into a string and join them.
        )
        blend_image.append(
            " ".join(list(map(str, blend_row)))
        )

    print(f"Total pixel num -> {succesfull + error}")
    print(f"Total successful pixel -> {succesfull}")
    print(f"Total erroroneus pixel -> {error}")
    print(f"The percentage of erroroneus pixel {error / (succesfull + error)}")
    result          = "\n".join(result_image)
    blended_result  = "\n".join(blend_image)
    with open(comp_path, "w") as f:
        f.write(result)
    
    with open(blend_path, "w") as f:
        f.write(blended_result)