# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 13:59:35 2025

@author: lcuev
"""
import pygame
from math import cos, sin, atan2

pygame.init()
pink = (255, 100, 255)
green = (100, 255, 50)
purple = (20, 10, 30)
white = (255, 255, 255)
black = (0, 0, 0)


class GUI:
    def __init__(self, size):
        self.size = size
        self.half_size = size // 2
        self.surface = pygame.display.set_mode((size,) * 2)
        self.running = True
        self.start = (400, 0)
        self.finish = (250, 3.14 / 4)
        self.held = False
        self.reset()
        pygame.display.set_caption('Bracciostrome')

    def dradius(self):
        R = self.start[0]
        r = self.pos[0]
        l = 1 - (R - r) / r ** 2 / self.A
        if l >= 0:
            return -l ** 0.5
        return (-l) ** 0.5

    def dtheta(self):
        R = self.start[0]
        r = self.pos[0]
        l = R - r
        if l == 0:
            return 0
        if l >= 0:
            return (-1) ** int(self.finish[1] < 0) * (abs(self.A * r ** 4 / l)) ** -0.5
        return (-1) ** int(self.finish[1] < 0) * (abs(self.A * r ** 4 / l)) ** -0.5

    def reset(self, h=0.1):
        self.surface.fill(purple)
        self.finish
        self.pos = [self.start[0], self.start[1]]
        self.A = (self.start[0] - self.finish[0]) / self.finish[0] ** 2
        self.finished = False

    def rect(self):
        x, y = self.project(self.pos)
        return (x, y, 1, 1)

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
        return (X-x) ** 2 + (Y-y)**2 < 20 ** 2

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
                if self.held and self.is_motion(pos):
                    self.finish = self.reverse_project(pos)
                    self.last_pos = pos
                    self.reset()

    def update(self, h=1):
        if self.finished:
            return
        if self.is_finished():
            self.finished = True
            return
        self.pos[1] += h * self.dtheta()
        self.pos[0] += h * self.dradius()

    def display(self):
        pygame.draw.rect(self.surface, white, self.rect())
        pygame.draw.circle(self.surface, pink, self.project(self.start), 20)
        pygame.draw.circle(self.surface, green, self.project(self.finish), 20)
        pygame.draw.circle(self.surface, black,
                           (self.half_size, self.half_size), 20)
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
