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

    textureID = glGenTextures(1)  # Generate texture ID
    glBindTexture(GL_TEXTURE_2D, textureID)  # Bind the texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    return textureID

def drawSquare(x, y, textureID):
    glBindTexture(GL_TEXTURE_2D, textureID)  # Bind our texture
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(x - 0.5, y - 0.5, 0)  # Bottom Left
    glTexCoord2f(1, 0); glVertex3f(x + 0.5, y - 0.5, 0)  # Bottom Right
    glTexCoord2f(1, 1); glVertex3f(x + 0.5, y + 0.5, 0)  # Top Right
    glTexCoord2f(0, 1); glVertex3f(x - 0.5, y + 0.5, 0)  # Top Left
    glEnd()

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)

    glEnable(GL_TEXTURE_2D)
    textureIDs = [loadTexture(f'texture{i}.png') for i in range(1, 4)]  # Load textures

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    for i, textureID in enumerate(textureIDs, start=-1):
        drawSquare(i, 0, textureID)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    for textureID in textureIDs:  # Clean up textures
        glDeleteTextures(textureID)
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
