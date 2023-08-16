import pygame
import sys


def run_animation():
    # Initialize pygame
    pygame.init()

    # Set up the display
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Animation Example")

    # Load the image
    image_path = r"C:\Users\hedia\OneDrive\Desktop\IT-Projects\Terminal\terminal.ico"
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, screen_size)

    # Set initial transparency value
    alpha = 0
    image.set_alpha(alpha)

    # Clock to control frame rate
    clock = pygame.time.Clock()

    # Animation loop
    running = True
    fading_in = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((255, 255, 255))

        # Adjust transparency
        if fading_in:
            alpha += 1
            if alpha >= 255:
                alpha = 255
                fading_in = False
        else:
            alpha -= 1
            if alpha <= 0:
                alpha = 0
                fading_in = True

        # Update image transparency
        image.set_alpha(alpha)

        # Draw the image on the screen
        screen.blit(image, (0, 0))

        # Update the display
        pygame.display.flip()

        # Control frame rate
        clock.tick(60)

    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_animation()
