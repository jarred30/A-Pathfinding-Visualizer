import operator
import sys
import pygame
import numpy as np
from settings import Settings
from neighbors import find_neighbors
from cost import cost_calc
from node import Node


class PathFinding:
    """Creates and runs path finding GUI"""

    def __init__(self):
        self.settings = Settings()
        pygame.init()
        self.display = pygame.display.set_mode((self.settings.screen_w, self.settings.screen_h))
        pygame.display.set_caption(self.settings.title)
        self._restart()
        self._instructions()

    def _restart(self):
        self._get_map()
        self.goals = []
        self._draw_screen()
        self.open_list = []
        self.closed_list = []

    def _get_map(self):
        self.num_rows = self.settings.screen_w // self.settings.sq_width
        self.num_cols = self.settings.screen_h // self.settings.sq_height
        self.closed_map = np.zeros([self.num_rows + 1, self.num_cols + 1])
        self.open_map = np.zeros([self.num_rows, self.num_cols])

    def _get_map_position(self, x, y):
        self.map_x = x // self.settings.sq_width
        self.map_y = y // self.settings.sq_height

    def _instructions(self):
        self.font = pygame.font.Font(None, 40)
        text_1 = "Welcome to Jarred's pathfinding visualizer."
        text_2 = "Please refer to README.txt for instructions."
        text_3 = "Press the space key to begin pathfinding."
        render_1 = self.font.render(text_1, True, (0, 0, 0))
        render_2 = self.font.render(text_2, True, (0, 0, 0))
        render_3 = self.font.render(text_3, True, (0, 0, 0))
        self.display.blit(render_1, (self.settings.sq_width, self.settings.sq_height * 4))
        self.display.blit(render_2, (self.settings.sq_width, self.settings.sq_height * 8))
        self.display.blit(render_3, (self.settings.sq_width, self.settings.sq_height * 12))
        pygame.display.flip()
        self.start_flag = False  # To block entry until instructions hidden

    def _failure(self):
        text_1 = "There is no solution to the input nodes."
        text_2 = "Press the space key to restart."
        render_1 = self.font.render(text_1, True, self.settings.red)
        render_2 = self.font.render(text_2, True, self.settings.red)
        self.display.blit(render_1, (self.settings.sq_width, self.settings.sq_height * 4))
        self.display.blit(render_2, (self.settings.sq_width, self.settings.sq_height * 8))
        pygame.display.flip()

    def _success(self):
        text_1 = "The fastest path has been found."
        text_2 = "Press the space key to restart."
        render_1 = self.font.render(text_1, True, self.settings.red)
        render_2 = self.font.render(text_2, True, self.settings.red)
        self.display.blit(render_1, (self.settings.sq_width, self.settings.sq_height * 4))
        self.display.blit(render_2, (self.settings.sq_width, self.settings.sq_height * 8))
        pygame.display.flip()

    def _event(self, event):
        if event.key == pygame.K_RETURN:
            if len(self.goals) == 2 and self.closed_list == []:
                self.open_list.append([self.goals[0].x, self.goals[0].y, 0])
                self._a_star()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.start_flag = True
            self._restart()

    def _get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._event(event)
            elif pygame.mouse.get_pressed()[0] and self.start_flag:
                self.position = pygame.mouse.get_pos()
                self._get_map_position(self.position[0], self.position[1])
                if self.closed_map[self.map_x, self.map_y] == 0 and self.closed_list == []:
                    self._fill_square(self.map_x, self.map_y, self.settings.black)
                    self.closed_map[self.map_x][self.map_y] = 1
            elif pygame.mouse.get_pressed()[2] and self.start_flag:
                self.position = pygame.mouse.get_pos()
                self._get_map_position(self.position[0], self.position[1])
                if self.closed_map[self.map_x, self.map_y] == 0:
                    if len(self.goals) == 0:
                        self._fill_square(self.map_x, self.map_y, self.settings.yellow)
                        self.closed_map[self.map_x, self.map_y] = 1
                    elif len(self.goals) == 1:
                        self._fill_square(self.map_x, self.map_y, self.settings.orange)
                        self.closed_map[self.map_x, self.map_y] = 1
        pygame.display.flip()

    def _draw_screen(self):
        self.display.fill(self.settings.background)
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self._fill_square(row, col, self.settings.white)
        self._draw_border()
        pygame.display.flip()

    def _draw_border(self):
        for row in range(self.num_rows):
            self._fill_square(row, 0, self.settings.black)
            self._fill_square(row, self.num_rows, self.settings.black)
            self.closed_map[row][0] = 1
            self.closed_map[row][self.num_rows] = 1
        for col in range(self.num_cols + 1):  # +1 to capture bottom right corner
            self._fill_square(0, col, self.settings.black)
            self._fill_square(self.num_cols, col, self.settings.black)
            self.closed_map[0][col] = 1
            self.closed_map[self.num_cols][col] = 1

    def _fill_square(self, row, col, color):
        pygame.draw.rect(self.display, color,
                         (self.settings.sq_width * row, self.settings.sq_height * col,
                          self.settings.sq_width - 1,
                          self.settings.sq_height - 1))
        if color == self.settings.yellow or color == self.settings.orange:
            goal = Node(x=row, y=col)
            self.goals.append(goal)

    def _a_star(self):
        h_cost, f_cost = cost_calc(self.goals[1].x, self.goals[1].y, self.goals[0].x, self.goals[0].y, 0)
        open_node = Node(x=self.goals[0].x, y=self.goals[0].y, f_cost=f_cost, g_cost=0, h_cost=h_cost)
        self.open_list = [open_node]
        flag = True  # flipped to False if path found
        while self.open_list:
            self.open_list.sort(key=operator.attrgetter('h_cost'))
            self.open_list.sort(key=operator.attrgetter('f_cost'))
            test = self.open_list.pop(0)
            if [test.x, test.y] != [self.goals[0].x, self.goals[0].y]:
                self._fill_square(test.x, test.y, self.settings.green)
                pygame.display.flip()
            self.closed_map[test.x, test.y] = 1
            self.closed_list.append(test)
            neighbors = find_neighbors(test.x, test.y, test.g_cost, self.goals)
            for node in neighbors:
                h_cost, f_cost = cost_calc(self.goals[1].x, self.goals[1].y, node.x, node.y, test.g_cost)
                node.h_cost = h_cost
                node.f_cost = f_cost
                if node.x == self.goals[1].x and node.y == self.goals[1].y:
                    self.closed_list.append(test)
                    self._shortest_path()
                    flag = False
                    break
                elif self.closed_map[node.x, node.y] == 1:
                    continue
                elif self.open_map[node.x, node.y] == 1:
                    filter_1 = filter(lambda x: x.x == node.x, self.open_list)
                    filter_2 = next(filter(lambda x: x.y == node.y, filter_1))
                    if node.g_cost < filter_2.g_cost:
                        index = self.open_list.index(filter_2)
                        self.open_list[index] = node
                        continue
                else:
                    self.open_map[node.x, node.y] = 1
                    self.open_list.append(node)
        if flag:
            self._failure()

    def _shortest_path(self):
        self.open_list = []
        node = self.closed_list[-1]
        while node:
            self._fill_square(node.x, node.y, self.settings.purple)
            pygame.display.flip()
            node = self._traceback(node)
        self._success()

    def _traceback(self, node):
        """Finds previous position"""
        for closed_node in self.closed_list:
            if node.old_x == self.goals[0].x and node.old_y == self.goals[0].y:
                return []
            elif node.old_x == closed_node.x and node.old_y == closed_node.y:
                return closed_node
        return 0

    def run(self):
        while True:
            self._get_input()


if __name__ == '__main__':
    path_finding = PathFinding()
    path_finding.run()
