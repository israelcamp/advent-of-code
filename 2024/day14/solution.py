from pathlib import Path
import re
from dataclasses import dataclass
from collections import Counter


@dataclass
class Robot:
    x: int  # col
    y: int  # row
    vx: int
    vy: int


def read_input(file: str):
    robots, dimension = Path(file).read_text().split("\n\n")
    robs = []
    for line in robots.splitlines():
        x, y, vx, vy = re.findall(r"-?\d+", line)
        robs.append(Robot(x=int(x), y=int(y), vx=int(vx), vy=int(vy)))

    h, w = [int(v) for v in re.findall(r"[0-9]{1,}", dimension)]
    return robs, h, w


def move_robot(robot: Robot, height: int, width: int) -> Robot:
    new_x, new_y = robot.x + robot.vx, robot.y + robot.vy

    if new_x >= width:
        new_x = new_x - width
    elif new_x < 0:
        new_x = width + new_x

    if new_y >= height:
        new_y = new_y - height
    elif new_y < 0:
        new_y = height + new_y

    robot.x = new_x
    robot.y = new_y
    return robot


def draw_grid(points, height: int, width: int, step: int) -> str:
    point_count = Counter(points)
    grid = []
    for i in range(height):
        row = []
        for j in range(width):
            text = str(point_count.get((i, j), "."))
            row.append(text)
        grid.append("".join(row))

    field = "\n".join(grid)
    drawing = f"STEP {step}\n{field}"

    return drawing


if __name__ == "__main__":
    file = "./input.txt"
    robots, H, W = read_input(file)

    max_steps = 10_000
    drawings = []
    step = 0
    trees = []
    counter_list = []
    while step < max_steps:
        robots_points = []
        for robot in robots:
            move_robot(robot, H, W)
            robots_points.append((robot.y, robot.x))

        if (
            abs(len(set(robots_points)) - len(robots_points))
            < len(robots_points) * 0.01
        ):
            print("NO OVERLAP", step)
            drawings.append(draw_grid(robots_points, H, W, step))

        counter_list.append((step, len(Counter(robots_points))))
        step += 1

    Path("drawings.txt").write_text("\n\n".join(drawings))

    middle_h = H // 2
    middle_w = W // 2

    first_quadrant = list(filter(lambda r: r.x < middle_w and r.y < middle_h, robots))
    print("FIRST", len(first_quadrant))
    second_quadant = list(filter(lambda r: r.x > middle_w and r.y < middle_h, robots))
    print("SECOND", len(second_quadant))
    third_quadrant = list(filter(lambda r: r.x > middle_w and r.y > middle_h, robots))
    print("THIRD", len(third_quadrant))
    fourth_quadrant = list(filter(lambda r: r.x < middle_w and r.y > middle_h, robots))
    print("FOURTH", len(fourth_quadrant))
    result = (
        len(first_quadrant)
        * len(second_quadant)
        * len(third_quadrant)
        * len(fourth_quadrant)
    )

    print("LEN ROBOTS", len(robots))
    print(result)
