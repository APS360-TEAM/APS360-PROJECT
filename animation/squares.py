import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def loadTexture(imageName):
    textureSurface = pygame.image.load(imageName)  # Load the image file
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    return textureID

# def drawSquare(x, y, z, textureID):
#     glBindTexture(GL_TEXTURE_2D, textureID)
#     glBegin(GL_QUADS)
#     glTexCoord2f(0, 0); glVertex3f(x - 0.5, y - 0.5, z)
#     glTexCoord2f(1, 0); glVertex3f(x + 0.5, y - 0.5, z)
#     glTexCoord2f(1, 1); glVertex3f(x + 0.5, y + 0.5, z)
#     glTexCoord2f(0, 1); glVertex3f(x - 0.5, y + 0.5, z)
#     glEnd()
def drawSquare(x, y, z, textureID, color):
    glBindTexture(GL_TEXTURE_2D, textureID)
    glColor4f(color[0], color[1], color[2], 1.0)  # Apply the tint color
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(x - 0.5, y - 0.5, z)
    glTexCoord2f(1, 0); glVertex3f(x + 0.5, y - 0.5, z)
    glTexCoord2f(1, 1); glVertex3f(x + 0.5, y + 0.5, z)
    glTexCoord2f(0, 1); glVertex3f(x - 0.5, y + 0.5, z)
    glEnd()

def main():
    pygame.init()
    display = (1200,900)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)

    glEnable(GL_TEXTURE_2D)
    textureIDs = [loadTexture(f'texture{i}.png') for i in range(1, 4)]

    # Define initial and target colors
    initial_color = (1.0, 1.0, 1.0)  # White (no tint)
    target_colors = [(1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0)]  # Red, Blue, Green


    start_time = pygame.time.get_ticks()
    running = True
    while running:
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        t = (pygame.time.get_ticks() - start_time) / 1000.0  # Time in seconds
        print(t)
        x_positions = [-1, 0, 1]  # Ensure x_positions is always defined
        # Smooth transition to 3/4 view over 1 second after 3 seconds
        if 3 < t <= 4:
            angle_y = (t - 3) * 45  # Rotate up to 45 degrees around y-axis
            angle_x = (t - 3) * -20  # Rotate up to -20 degrees around x-axis
            glLoadIdentity()
            gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
            glTranslatef(0.0, 0.0, -5)
            glRotatef(angle_y, 0, 1, 0)  # Apply gradual rotation around y-axis
            glRotatef(angle_x, 1, 0, 0)  # Apply gradual rotation around x-axis
        elif t > 4:
            glLoadIdentity()
            gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
            glTranslatef(0.0, 0.0, -5)
            glRotatef(45, 0, 1, 0)  # Fixed 3/4 view after transition
            glRotatef(-20, 1, 0, 0)

        # Maintain z_positions after initial forward/backward movement
        if t <= 6:
            progress = min(max((t - 4) / 2, 0), 1)
            z_positions = [-progress, 0, progress]  # Updated to smoothly transition

        # Smoothly move squares left and right
        if 6 < t <= 8:
            progress = (t - 6) / 4
            x_positions = [-1 + progress * 2, 0, 1 - progress * 2]  # Updated to smoothly transition
        # Compute the color transition after t=8 and before t=8.5
        if 8 < t <= 8.5:
            x_positions = [0, 0, 0]  # Ensure x_positions is always defined
            transition_progress = (t - 8) / 0.5
            colors = [tuple(initial_color[j] + (target_colors[i][j] - initial_color[j]) * transition_progress for j in range(3)) for i in range(3)]
            z_positions = [-1, 0, 1]  # Maintain previous z_positions
        elif t > 8.5 and t <= 9.5:
            # After the color transition is complete
            x_positions = [0, 0, 0]  # Ensure x_positions is aligned
            colors = target_colors  # Use target colors
            # Smooth transition of z_positions back to z=0 with a tiny gap over 1 second
            z_transition_progress = (t - 8.5) / 1
            z_positions = [-1 + 0.8 *  z_transition_progress, 0, 1 - 0.8 * z_transition_progress]  # Calculate the new z_positions
            # z_positions = [-0.2 + z_transition_progress * 0.2, 0, 0.2 - z_transition_progress * 0.2]  # Calculate the new z_positions
        elif t > 9.5:
            # Keep everything stationary after all transitions are complete
            x_positions = [0, 0, 0]
            colors = target_colors
            z_positions = [-0.2, 0, 0.2]  # Final z_positions after transition
        else:
            # Before t=8, handle other animations as before
            # This is where you handle the existing logic for colors and positions before the new final modification
            colors = [initial_color for _ in range(3)]  # Before t=8, use initial color
            # pass

        # Drawing squares with updated positions and colors
        for i, textureID in enumerate(textureIDs):
            drawSquare(x_positions[i], 0, z_positions[i], textureID, colors[i])

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    for textureID in textureIDs:  # Clean up textures
        glDeleteTextures(textureID)
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
