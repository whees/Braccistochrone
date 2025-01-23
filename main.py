# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 13:59:35 2025

@author: lcuev
"""
import pygame
from math import cos, sin, atan2

pygame.init()
light_blue = (100, 150, 200)
green = (100, 200, 80)
dark_green = (30, 50, 20)
purple = (20, 10, 30)
light_purple = (66, 30, 100)
white = (255, 255, 255)
black = (0, 0, 0)
earth_radius = 75
knob_radius = 20


class GUI:
    def __init__(self, size):
        self.size = size
        self.half_size = size // 2
        self.surface = pygame.display.set_mode((size,) * 2)
        self.running = True
        self.start = (400, 0)
        self.finish = (earth_radius, 3.14)
        self.held = False
        self.wipe = False
        self.reset()
        pygame.display.set_caption('Bracciostrome')

    def center(self):
        return (self.half_size, self.half_size)

    def dtheta(self):
        R = self.start[0]
        r = self.pos[0]
        return abs((R - r) / self.A / r ** 4) ** 0.5

    def dradius(self):
        R = self.start[0]
        r = self.pos[0]

        if r < self.thresh:
            self.flipped = True

        dr = abs(1 - (R - r) / self.A / r ** 2) ** 0.5
        return dr if self.flipped else -dr

    def reset(self):
        self.pos = [self.start[0], self.start[1]]
        self.A = (self.start[0] - self.finish[0]) / self.finish[0] ** 2
        self.thresh = (-1 + (1 + 4 * self.A *
                       self.start[0]) ** 0.5) / 2 / self.A
        self.flipped = False
        self.finished = False
        self.wipe = True

    def rects(self):
        x, y = self.project(self.pos)
        return (x, y, 3, 3), (x, self.size - y, 3, 3)

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
        if self.finished:
            return True
        return self.pos[0] > self.start[0] or self.pos[0] < earth_radius

    def handle_events(self):
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
                propos = self.reverse_project(pos)
                if self.held and self.is_motion(pos) and propos[0] < self.start[0] - knob_radius / 2:
                    self.finish = propos
                    self.last_pos = pos
                    self.reset()

    def update(self, h=1):
        self.finished = self.is_finished()
        if self.finished:
            return

        self.pos[0] += h * self.dradius()
        self.pos[1] += h * self.dtheta()

    def display(self):
        if self.finished:
            return
        if self.wipe:
            pygame.draw.circle(self.surface, purple,
                               self.center(), self.start[0])
            self.wipe = False

        rect, rev_rect = self.rects()
        pygame.draw.circle(self.surface, dark_green,
                           self.center(), self.finish[0], width=3)
        pygame.draw.rect(self.surface, white, rect)
        pygame.draw.rect(self.surface, white, rev_rect)
        pygame.draw.circle(self.surface, light_blue,
                           self.center(), earth_radius)
        pygame.draw.circle(self.surface, light_purple,
                           self.center(), self.start[0] + 10, width=10)

        pygame.draw.circle(self.surface, white,
                           self.project(self.start), knob_radius)
        pygame.draw.circle(self.surface, green,
                           self.project(self.finish), knob_radius)
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
