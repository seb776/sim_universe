#!/usr/bin/env python2

import sys
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk #1
import random

def add_ball(space, pos):
    mass = 1
    radius = random.random() * 15 + 10
    inertia = pymunk.moment_for_circle(mass, 0, radius) # 1
    body = pymunk.Body(mass, inertia) # 2
    x = random.randint(120,140)
    body.position = x, 550 # 3
    body.position = pos[0], 600 - pos[1]
    shape = pymunk.Circle(body, radius) # 4
    shape.friction = 150.1
    # body.angular_velocity_limit = 0.1
    space.add(body, shape) # 5
    return shape

def draw_ball(screen, ball):
    p = int(ball.body.position.x), 600-int(ball.body.position.y)
    pygame.draw.circle(screen, int(ball.radius) * 1500, p, int(ball.radius), 2)

def add_L(space):
    rotation_center_body = pymunk.Body()
    rotation_center_body.position = (300,300)
    
    rotation_limit_body = pymunk.Body() # 1
    rotation_limit_body.position = (200,300)
    
    body = pymunk.Body(10, 10000)
    body.position = (300,300)
    body.angular_velocity_limit = 0.1
    l1 = pymunk.Segment(body, (-150, 0), (255.0, 0.0), 5.0)
    l2 = pymunk.Segment(body, (-150.0, 0), (-150.0, 50.0), 5.0)
    l1.friction = 0.1
    l2.friction = 0.1
    
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0,0), (0,0)) 
    joint_limit = 25
    rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-100,0), (0,0), 0, joint_limit) # 2

    space.add(l1, l2, body, rotation_center_joint, rotation_limit_joint)
    return l1,l2

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

def draw_lines(screen, lines):
    for line in lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle) # 1
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1) # 2
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, THECOLORS["black"], False, [p1,p2])
 
def main():
    balls = []
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()
    running = True
    
    space = pymunk.Space() #2
    space.gravity = (0.0, -900.0)
    
    lines = add_L(space)
    while running:
        balls_to_remove = []
        for event in pygame.event.get():
            balls.append(add_ball(space, pygame.mouse.get_pos()))
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                space.gravity = (0.0, random.randint(-900, 900))
                balls.append(add_ball(space, (42, 42)))
        screen.fill(THECOLORS["white"])
        for ball in balls:
            draw_ball(screen, ball)
            if ball.body.position.y < 0: # 1
                balls_to_remove.append(ball) # 2
        
        draw_lines(screen, lines)
        space.step(1/50.0) #3
        for ball in balls_to_remove:
            space.remove(ball, ball.body) # 3
            balls.remove(ball) # 4
        
        pygame.display.flip()
        clock.tick(50)
        
if __name__ == '__main__':
    sys.exit(main())
