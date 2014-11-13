#!/usr/bin/env python2

import math
import  sys
import  pymunk
import  pygame
from    pygame.color import *
from    pygame.locals import *

static_body = pymunk.Body()

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

camera_pos = (0, 0)

class   Car:
    def __init__(self, pos, space):
        self.wheelImg = pygame.image.load("wheel.png")
        size = 50.0
        self.points = [(-size * 2.5, size / 2),
                       (size * 2.5, size / 2),
                       (size, -size / 2),
                       (-size, -size / 2)]
        boxInertia = pymunk.moment_for_poly(100.0, self.points)
        boxBody = pymunk.Body(1.0, boxInertia)
        boxBody.position = pos
        self.box = pymunk.Poly(boxBody, self.points)
        self.box.friction = 0.85

        wheelMass = 10
        wheelRadius = size / 2
        wheelInertia = pymunk.moment_for_circle(2, 0, wheelRadius)

        wheelBodyB = pymunk.Body(wheelMass, wheelInertia)
        wheelBodyB.position.x = pos[0] + size * 1.9
        wheelBodyB.position.y = pos[1] - size * 0.8
        wheelShapeB = pymunk.Circle(wheelBodyB, wheelRadius)
        wheelShapeB.friction = 0.5

        wheelBodyA = pymunk.Body(wheelMass, wheelInertia)
        wheelBodyA.position.x = pos[0] - size * 1.9
        wheelBodyA.position.y = pos[1] - size * 0.8
        wheelShapeA = pymunk.Circle(wheelBodyA, wheelRadius)
        wheelShapeA.friction = 0.5
        

        self.rearWheel = wheelShapeA
        self.frontWheel = wheelShapeB

        rotation_center_jointA = pymunk.PivotJoint(self.rearWheel.body, boxBody, self.rearWheel.body.position)
        rotation_center_jointB = pymunk.PivotJoint(self.frontWheel.body, boxBody, self.frontWheel.body.position)
        

        self.motor = pymunk.constraint.SimpleMotor(self.box.body, wheelBodyA, 0)
        space.add(self.motor)
        space.add(rotation_center_jointA)
        space.add(rotation_center_jointB)
        space.add(wheelBodyA, wheelShapeA)
        space.add(wheelBodyB, wheelShapeB)
        space.add(boxBody, self.box)
    def render(self, screen, camera_pos):
        # pos = self.frontWheel.body.position
        # realPos = (int(pos.x), int(pos.y))
        nImg = rot_center(self.wheelImg, -self.frontWheel.body.angle * 20)
        nImg = pygame.transform.rotozoom(nImg, 0, 0.15)
        imgPos = (self.frontWheel.body.position.x - nImg.get_width() / 2 - camera_pos[0] + 640, self.frontWheel.body.position.y - nImg.get_height() / 2 - camera_pos[1] + 360)

        screen.blit(nImg, imgPos)

        nImg = rot_center(self.wheelImg, -self.rearWheel.body.angle * 20)
        nImg = pygame.transform.rotozoom(nImg, 0, 0.15)
        imgPos = (self.rearWheel.body.position.x - camera_pos.x - nImg.get_width() / 2 + 640, self.rearWheel.body.position.y - camera_pos.y - nImg.get_height() / 2 + 360)
        # print(camera_pos)

        screen.blit(nImg, imgPos)
        nvertices = []
        vertices = self.box.get_vertices()
        for dot in vertices:
            nvertices.append((dot.x - camera_pos.x + 640, dot.y - camera_pos.y + 360))
        pygame.draw.polygon(screen, THECOLORS["black"], nvertices)

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+720)

def     draw_line(screen, line, camera_pos):
    body = line.body
    pv1 = body.position + line.a.rotated(body.angle) # 1
    pv2 = body.position + line.b.rotated(body.angle)
    pos1 = (pv1.x - camera_pos[0] + 640, pv1.y - camera_pos[1] + 360)
    pos2 = (pv2.x - camera_pos[0] + 640, pv2.y - camera_pos[1] + 360)
    pygame.draw.lines(screen, THECOLORS["black"], False, [pos1,pos2], 6)
    
def     add_line(space, dot1, dot2):
    groundBody = pymunk.Body()
    groundBody.position = (0, 0)
    groundShape = pymunk.Segment(groundBody, dot1, dot2, 5.0)
    groundShape.friction = 5.0
    space.add(groundShape)
    return groundShape


def     main():
    pygame.init()

    width = 1280
    height = 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Universe")

    space = pymunk.Space()
    space.gravity = (0.0, -900.0)

    clock = pygame.time.Clock()

    lines = []
    ended = False
    prescreen = pygame.Surface((width, height))
    camera_pos = [0, 0]
    lines.append(add_line(space, (-100, 30), (420, 0)))
    last_dot = (420, 0)
    while not ended:
        for event in pygame.event.get():
            print(event.type)
            prescreen.fill(THECOLORS["white"])
            if event.type == 5: # left click
                cur_dot = pygame.mouse.get_pos()
                cur_dot = (cur_dot[0] + camera_pos[0] - 640, 720 - cur_dot[1] + camera_pos[1] - 360)
                print(cur_dot)
                lines.append(add_line(space, last_dot, cur_dot))
                last_dot = cur_dot
                # print(pygame.mouse.get_pos())
            for line in lines:
                draw_line(prescreen, line, camera_pos)
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    camera_pos[0] += 50
                if event.key == K_RIGHT:
                    camera_pos[0] -= 50
                if event.key == K_UP:
                    ended = True
            postscreen = pygame.transform.flip(prescreen, False, True)
            screen.blit(postscreen, (0, 0))
            pygame.display.flip()

    # lines.append(add_line(space, (420, 0), (1500, 500)))
    # lines.append(add_line(space, (1500, 500), (2500, 400)))
    # lines.append(add_line(space, (2500, 400), (5000, -100)))
    ended = False
    vehicle = Car((200, 250.0), space)
    while not ended:
        camera_pos = vehicle.box.body.position
        # print(camera_pos)
        for event in pygame.event.get():
            if event.type == KEYUP:
                vehicle.motor.rate = 0
            if event.type == KEYDOWN:
                print(event.key)
                if event.key == 97:
                    vehicle.box.body.angular_velocity = 0
                    vehicle.box.body._set_angle(0)
                    vehicle.box.body.position = (200, 250)
                if event.key == 114:
                    vehicle.box.body.angular_velocity = 0
                    vehicle.box.body._set_angle(0)
                    vehicle.box.body.position.y += 25
                if event.key == K_LEFT:
                    if vehicle.motor.rate > -5000:
                        vehicle.motor.rate -= 15
                    vehicle.motor.max_force = float('Inf')
                if event.key == K_RIGHT:
                    if vehicle.motor.rate < 5000:
                        vehicle.motor.rate += 20
                    vehicle.motor.max_force = float('Inf')
            if event.type == KEYUP:
                vehicle.motor.max_force = 0
            if event.type == QUIT:
                ended = True
        prescreen.fill(THECOLORS["white"])
        for line in lines:
            draw_line(prescreen, line, camera_pos)
        vehicle.render(prescreen, camera_pos)

        postscreen = pygame.transform.flip(prescreen, False, True)
        print(vehicle.box.body.angle)
        nscreen = rot_center(postscreen, -math.degrees(vehicle.box.body.angle))
        screen.blit(nscreen, (0, 0))
        pygame.display.flip()
        space.step(1/50.0)
        clock.tick(50)
    

if __name__ == '__main__':
    sys.exit(main())
