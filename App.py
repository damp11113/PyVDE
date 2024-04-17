import pygame

class AppWindow:
    def __init__(self, title="myapp", window_size=(450, 250), font='Arial'):
        window_size = (window_size[0] + 20, window_size[1]) # for title bar
        self.window = pygame.Surface(window_size)
        self.title = title
        self.window_size = window_size
        self.running = False
        self.dragging = False
        self.drag_offset = (0, 0)
        self.pos = (0, 0)

        self.font = pygame.font.SysFont(font, 15)
        self.titletext = self.font.render(title, True, (200, 200, 200))

    def set_window_size(self, window_size=(450, 250)):
        window_size = (window_size[0] + 20, window_size[1]) # for title bar
        self.window = pygame.Surface(window_size)
        self.window_size = window_size

    def set_title(self, title):
        self.titletext = self.font.render(title, True, (200, 200, 200))
        self.title = title

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                if 0 <= mouse_pos[0] < self.window_size[0] and 0 <= mouse_pos[1] < 20:  # Check if clicked on title bar
                    self.dragging = True
                    self.drag_offset = (mouse_pos[0], mouse_pos[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.dragging = False

        if event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_pos = pygame.mouse.get_pos()
                new_pos = (mouse_pos[0] - self.drag_offset[0], mouse_pos[1] - self.drag_offset[1])
                print(new_pos)


    def titlebar(self):
        rect = self.titletext.get_rect()
        rect.left = 2
        pygame.draw.rect(self.window, (0, 0, 0), (0, 0, self.window_size[0], 20))
        self.window.blit(self.titletext, rect)

    def init(self):
        """call on start app"""
        pass

    def render(self):
        """call on app running"""
        pass

    def exit(self):
        """call on app exiting"""
        pass
