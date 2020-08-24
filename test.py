import pygame
pygame.init()

X = 400
Y = 400

display_surface = pygame.display.set_mode((X, Y))

font = pygame.font.SysFont('Calibri', 32)
text = font.render('MODE', True, [255, 255, 255], [0, 255, 255])

textRect = text.get_rect()

textRect.center = (X // 2, Y // 2)

while True:
    display_surface.fill([255, 255, 255])
    display_surface.blit(text, textRect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        pygame.display.update()


    