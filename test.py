import pygame
pygame.init()

X = 400
Y = 400

display_surface = pygame.display.set_mode((X, Y))
display_surface.fill((255, 255, 0))

font = pygame.font.SysFont('Calibri', 32)
clock = pygame.image.load('clock.png')
clock = pygame.transform.scale(clock, (250, 150))
rect = clock.get_rect()
rect = rect.move(200, 200)
display_surface.blit(clock, rect)
pygame.display.flip()
while True:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        pygame.display.update()


    