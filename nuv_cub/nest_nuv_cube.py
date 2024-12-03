import cv2
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    return thresh

def find_obstacles(thresh):
    edges = cv2.Canny(thresh, 50, 150, apertureSize=3)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def generate_grid(obstacles, cell_size=10):
    h, w = thresh.shape[:2]
    grid = np.zeros((h // cell_size, w // cell_size), dtype=np.uint8)

    for obstacle in obstacles:
        rect = cv2.boundingRect(obstacle)
        x1, y1, w1, h1 = rect
        x2, y2 = x1 + w1, y1 + h1
        grid[y1 // cell_size:y2 // cell_size, x1 // cell_size:x2 // cell_size] = 1

    return grid


def grid_to_graph(grid):
    G = nx.Graph()
    h, w = grid.shape

    for i in range(h):
        for j in range(w):
            if grid[i, j] == 0:
                neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                for x, y in neighbors:
                    if 0 <= x < h and 0 <= y < w and grid[x, y] == 0:
                        G.add_edge((i, j), (x, y))

    return G

def find_shortest_path(G, start, goal):
    path = nx.astar_path(G, start, goal)
    return path


def visualize_result(grid, path):
    h, w = grid.shape
    img = np.zeros((h * 20, w * 20, 3), dtype=np.uint8)

    for i in range(h):
        for j in range(w):
            color = (255, 255, 255) if grid[i, j] == 0 else (0, 0, 0)
            cv2.rectangle(img, (j * 20, i * 20), ((j + 1) * 20, (i + 1) * 20), color, -1)

    for u, v in zip(path[:-1], path[1:]):
        cv2.line(img, (v[1] * 20 + 10, u[0] * 20 + 10), (u[1] * 20 + 10, v[0] * 20 + 10), (0, 0, 255), 2)

    cv2.imshow("Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":

    image = capture_image()
    thresh = preprocess_image(image)
    obstacles = find_obstacles(thresh)
    grid = generate_grid(obstacles)
    G = grid_to_graph(grid)

    start = (0, 0)
    goal = (grid.shape[0] - 1, grid.shape[1] - 1)
    path = find_shortest_path(G, start, goal)

    visualize_result(grid, path)