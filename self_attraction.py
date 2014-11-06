#/usr/bin/env python2

import pymunk
import pygame

def     add_object(space, objs, size, pos):
    mass = size * 150.0
    radius = size

    inertia = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, inertia)
    body.position = pos

    shape = pymunk.Circle(body, radius)
    space.add(body, shape)
    objs.append(shape)
    return shape

def     draw_ball(screen, ball):
    coords = (int(ball.body.position.x), int(ball.body.position.y))
    pygame.draw.circle(screen, 0x123456, coords, int(ball.radius), 2)

def     main():
    pygame.init()
    
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))

    space = pymunk.Space()
    space.gravity = (0.0, 0.0)

    clock = pygame.time.Clock()
    ended = False

    bodies = []

    s = add_object(space, bodies, 100, (640, 360))
    space.remove(s.body)

    while not ended:
        screen.fill(0xFFFFFFFF)
        # event
        for event in pygame.event.get():
            if event.type == 5:
                cur_dot = pygame.mouse.get_pos()
                cur_dot = (cur_dot[0], height - cur_dot[1])
                add_object(space, bodies, 10, cur_dot)

        # display
        for ball in bodies:
            for ball2 in bodies:
                if ball != ball2:
                    ball.body.apply_force((ball2.body.position - ball.body.position).normalized() * (250 - ball2.body.position.get_distance(ball.body.position)))
            draw_ball(screen, ball)

        postscreen = pygame.transform.flip(screen, False, True)
        screen.blit(postscreen, (0, 0))
        pygame.display.flip()

        # time
        space.step(1/50.0)
        clock.tick(50)

main()
