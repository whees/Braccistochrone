# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 13:59:35 2025

@author: lcuev
"""
import pygame
from math import cos, sin, atan2

pygame.init()
pink = (255, 100, 255)
light_blue = (100, 150, 200)
green = (100, 255, 80)
purple = (20, 10, 30)
light_purple = (66, 30, 100)
white = (255, 255, 255)
black = (0, 0, 0)


class GUI:
    def __init__(self, size):
        self.size = size
        self.half_size = size // 2
        self.surface = pygame.display.set_mode((size,) * 2)
        self.running = True
        self.start = (400, 0)
        self.finish = (65, 3.14)
        self.held = False
        pygame.draw.circle(self.surface, purple,
                           (self.half_size, self.half_size), self.start[0])
        pygame.draw.circle(self.surface, light_blue,
                           (self.half_size, self.half_size), 75)
        self.reset()
        pygame.display.set_caption('Bracciostrome')

    def dradius(self):
        R = self.start[0]
        r = self.pos[0]
        if r == R:
            return -10000
        if r < self.thresh:
            self.flipped = True
        dr = (abs(self.A * r ** 4 / (R - r) - r ** 2)) ** 0.5
        if self.flipped:
            return dr
        return -dr

    def reset(self, h=0.01):
        self.pos = [self.start[0], self.start[1]]
        self.A = (self.start[0] - self.finish[0]) / self.finish[0] ** 2
        self.thresh = (-1 + (1 + 4 * self.A *
                       self.start[0]) ** 0.5) / 2 / self.A + h
        self.flipped = False
        self.finished = False

    def rect(self):
        x, y = self.project(self.pos)
        return (x, y, 3, 3)

    def project(self, pos):
        r, t = pos
        return (int(r * cos(t)) + self.half_size, int(r * sin(t)) + self.half_size)

    def reverse_project(self, pos):
        X, Y = pos
        x, y = X - self.half_size, Y - self.half_size
        return (x ** 2 + y ** 2) ** 0.5, atan2(y, x)

    def is_click(self, pos):
        x, y = pos
        X, Y = self.project(self.finish)
        return (X-x) ** 2 + (Y-y)**2 < 20 ** 2

    def is_motion(self, pos):
        x, y = pos
        X, Y = self.last_pos
        return (x - X) ** 2 + (y - Y) ** 2 > 5 ** 2

    def is_finished(self):
        x, y = self.project(self.finish)
        X, Y = self.project(self.pos)
        return (X-x) ** 2 + (Y-y)**2 < 20 ** 2 or self.pos[0] > int(self.start[0]) or self.pos[0] < 75

    def handle_events(self, d=2):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.is_click(pos):
                    self.held = True
                    self.last_pos = pos
            if event.type == pygame.MOUSEBUTTONUP:
                self.held = False
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if self.finish[0] < 65:
                    pygame.draw.circle(self.surface, green,
                                       self.project(self.finish), 10)
                elif self.finish[0] > 95:
                    pygame.draw.circle(self.surface, purple,
                                       self.project(self.finish), 10)
                if self.held and self.is_motion(pos):
                    self.finish = self.reverse_project(pos)
                    self.last_pos = pos
                    self.reset()

    def update(self, h=0.001):
        if self.finished or self.finish[0] < 95:
            return
        if self.is_finished():
            self.finished = True
            return
        self.pos[1] += h
        self.pos[0] += h * self.dradius()

    def display(self):
        rect = self.rect()
        pygame.draw.rect(self.surface, white, rect)
        pygame.draw.rect(self.surface, white,
                         (rect[0], self.size - rect[1], 3, 3))
        pygame.draw.circle(self.surface, light_purple,
                           (self.half_size, self.half_size), self.start[0] + 10, width=10)
        pygame.draw.circle(self.surface, black,
                           (self.half_size, self.half_size), self.start[0] + 40, width=30)
        pygame.draw.circle(self.surface, pink, self.project(self.start), 20)

        if self.finish[0] > 95:
            pygame.draw.circle(self.surface, green,
                               self.project(self.finish), 10)

        pygame.display.update()

    def main_loop(self):
        self.handle_events()
        self.update()
        self.display()
        return self.running


if __name__ == '__main__':
    pygame.init()
    gui = GUI(1000)
    while gui.main_loop():
        pass
    pygame.quit()
