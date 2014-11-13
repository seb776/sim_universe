#/usr/bin/env python2

import pymunk
import pygame

def     add_object(space, objs, size, pos):
    mass = size
    if size > 15:
        mass = size * 100
    radius = size

    inertia = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, inertia)
    body.position = pos
    body.friction = 2

    shape = pymunk.Circle(body, radius)
    space.add(body, shape)
    objs.append(shape)
    return shape

def     draw_ball(screen, ball):
    coords = (int(ball.body.position.x), int(ball.body.position.y))
    pygame.draw.circle(screen, 0x123456, coords, int(ball.radius), 0)

def     main():
    pygame.init()
    
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))

    space = pymunk.Space()
    space.gravity = (0.0, 0.0)

    clock = pygame.time.Clock()
    ended = False

    background = pygame.image.load("space.png")

    bodies = []

    s = add_object(space, bodies, 1000, (-500, -500))
    # space.remove(s.body)

    while not ended:
        # screen.fill(0xFFFFFFFF)
        screen.blit(background, (0, 0))
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
                    vec = (ball2.body.position - ball.body.position).normalized() * ((ball.body.mass * ball2.body.mass) / pow(ball2.body.position.get_distance(ball.body.position), 2))
                    pygame.draw.line(screen, 0x03C6FF, ball.body.position, ball.body.position + (vec * 50000.0))
                    ball.body.apply_force(vec)
            draw_ball(screen, ball)

        postscreen = pygame.transform.flip(screen, False, True)
        screen.blit(postscreen, (0, 0))
        pygame.display.flip()

        # time
        space.step(1/50.0)
        clock.tick(50)

main()
