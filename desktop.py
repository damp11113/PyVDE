import sys
import os
import time
import cv2
import threading

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from PyVDE import __version__

class Desktop:
    def __init__(self, title=f"PyVDE v{__version__}", background="default", displaysize=(1280, 720)):
        self.title = title
        if background.lower() == "default":
            self.background = "/".join(str(__file__).split("\\")[:-1]) + '/assets/background.png'
        self.displaysize = displaysize

        # System Variable
        self.screen = None
        self.clock = None
        self.running = False
        self.apps = {}
        self.currentapp = {}
        self.backgroundimagearray = None
        self.backgroundimagesize = []

        # Start menu properties
        self.start_menu_active = False
        self.start_menu_font = None
        self.start_menu_text = "Start"
        self.start_menu_text_color = (255, 255, 255)
        self.start_menu_text_position = None

        self.taskbar_height = 40
        self.taskbar_color = (51, 51, 51)  # Dark gray color
        self.taskbar_icon_spacing = 10
        self.taskbar_icon_size = 30

        self.power_button_icon = None
        self.power_menu_active = False
        self.power_menu_text = []

        self.edtiontext = None

    def start(self):
        pygame.init()
        loadtime = time.time()

        # Set up the display
        self.screen = pygame.display.set_mode(self.displaysize, pygame.RESIZABLE)
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(pygame.image.load("/".join(str(__file__).split("\\")[:-1]) + '/assets/icon.ico'))

        self.startloadassets()

        print("loaded in", time.time() - loadtime, "sec")
        self.clock = pygame.time.Clock()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                self.event(event)

            self.render()

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(60)

        self.exit()

    def startloadassets(self):
        assetspath = "/".join(str(__file__).split("\\")[:-1]) + '/assets/'

        self.power_button_icon = pygame.image.load(assetspath + "power.png")
        self.power_button_icon = pygame.transform.scale(self.power_button_icon, (30, 30))  # Resize icon to 20x20

        self.start_menu_font = pygame.font.SysFont('Arial', 16)

        self.setbackgroundimage()
        self.start_menu_text_position = (10, self.displaysize[1] - 20)

        power_options_font = pygame.font.SysFont('Arial', 20)
        shutdown_text = power_options_font.render("Shutdown", True, (255, 255, 255))
        restart_text = power_options_font.render("Restart", True, (255, 255, 255))
        logout_text = power_options_font.render("Logout", True, (255, 255, 255))
        cancel_text = power_options_font.render("Cancel", True, (255, 255, 255))
        self.power_menu_text = [shutdown_text, restart_text, logout_text, cancel_text]

        self.edtiontext = pygame.font.SysFont('Arial', 10).render(f"PyVDE v{__version__} Development", True, (255, 255, 255))

    def event(self, event):
        if event.type == pygame.QUIT:
            self.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:  # Left mouse button
                self.handle_start_menu_click(pos)

                if self.start_menu_active:
                    self.handle_start_menu_power_button_click(pos)

                if self.power_menu_active:
                    self.handle_power_menu_click(pos)
        elif event.type == pygame.VIDEORESIZE:  # Handle window resize event
            self.displaysize = event.size
            self.setbackgroundimage()
            self.start_menu_text_position = (10, self.displaysize[1] - 20)

        currentapp_copy = self.currentapp.copy()

        for app in currentapp_copy.keys():
            classapp = currentapp_copy[app]["app"]
            classapp.handle_event(event)

    def handle_start_menu_click(self, pos):
        # Check if the start menu text area is clicked
        text_rect = self.start_menu_font.render(self.start_menu_text, True, self.start_menu_text_color).get_rect(topleft=self.start_menu_text_position)
        if text_rect.collidepoint(pos):
            self.start_menu_active = not self.start_menu_active

    def handle_start_menu_power_button_click(self, pos):
        # Check if the start menu text area is clicked
        power_button_rect = pygame.Rect(5, self.displaysize[1] - 20 - 35, 30, 30)  # Adjust dimensions as needed
        if power_button_rect.collidepoint(pos):
            self.power_menu_active = True
            self.start_menu_active = False

    def handle_power_menu_click(self, pos):
        power_menu_width = 200
        power_menu_height = 200
        power_menu_x = (self.displaysize[0] - power_menu_width) // 2
        power_menu_y = (self.displaysize[1] - power_menu_height) // 2

        option_spacing = 20
        option_y = power_menu_y + 20
        option_rects = []
        for i in range(len(self.power_menu_text) - 1):
            option_rect = self.power_menu_text[i].get_rect(topleft=(power_menu_x + 20, option_y))
            option_rects.append(option_rect)
            option_y += option_spacing

        option_rect = self.power_menu_text[3].get_rect(topleft=(power_menu_x + 20, option_y + 50))
        option_rects.append(option_rect)
        option_y += option_spacing

        for i, option_rect in enumerate(option_rects):
            if option_rect.collidepoint(pos):
                if i == 0:
                    # Shutdown option
                    self.exit()
                elif i == 1:
                    # Restart option
                    print("Restart clicked")
                elif i == 2:
                    # Logout option
                    pass
                elif i == 3:
                    # Cancel option
                    self.power_menu_active = False

    def render_start_menu(self):
        # Background for start menu
        pygame.draw.rect(self.screen, (100, 100, 100), (0, self.displaysize[1] - 20 - 320, 210, 320))  # Example dimensions, adjust as needed
        if self.power_button_icon:
            self.screen.blit(self.power_button_icon, (5, self.displaysize[1] - 20 - 35))  # Adjust position as needed

    def render_power_menu(self):
        power_menu_width = 200
        power_menu_height = 200
        power_menu_x = (self.displaysize[0] - power_menu_width) // 2
        power_menu_y = (self.displaysize[1] - power_menu_height) // 2

        # Background for power menu
        pygame.draw.rect(self.screen, (100, 100, 100), (power_menu_x, power_menu_y, power_menu_width, power_menu_height))  # Adjust dimensions as needed

        option_spacing = 20
        option_y = power_menu_y + 20
        self.screen.blit(self.power_menu_text[0], (power_menu_x + 20, option_y))
        option_y += option_spacing
        self.screen.blit(self.power_menu_text[1], (power_menu_x + 20, option_y))
        option_y += option_spacing
        self.screen.blit(self.power_menu_text[2], (power_menu_x + 20, option_y))
        option_y += option_spacing
        self.screen.blit(self.power_menu_text[3], (power_menu_x + 20, option_y + 50))

    def setbackgroundimage(self, image=None):
        if image is None:
            image = self.background

        image_cv = cv2.imread(image)
        screen_width, screen_height = self.screen.get_width(), self.screen.get_height()

        height, width, _ = image_cv.shape
        aspect_ratio = width / height
        if width > height:
            new_width = screen_width
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = screen_height
            new_width = int(new_height * aspect_ratio)

        self.backgroundimagesize = [screen_width, new_width, screen_height, new_height]

        image_cv_resized = cv2.resize(image_cv, (new_width, new_height))

        # Convert the resized image from BGR to RGB (Pygame uses RGB format)
        image_rgb = cv2.cvtColor(image_cv_resized, cv2.COLOR_BGR2RGB)

        # Convert the image to a format Pygame can work with
        self.backgroundimagearray = pygame.image.frombuffer(image_rgb.flatten(), image_rgb.shape[:2][::-1], 'RGB')

    def render(self):
        self.screen.fill((0, 0, 0))  # Clear the screen
        self.screen.blit(self.backgroundimagearray, ((self.backgroundimagesize[0] - self.backgroundimagesize[1]) // 2, (self.backgroundimagesize[2] - self.backgroundimagesize[3]) // 2))
        self.rendertaskbar()
        # Render start menu text
        start_menu_surface = self.start_menu_font.render(self.start_menu_text, True, self.start_menu_text_color)
        self.screen.blit(start_menu_surface, self.start_menu_text_position)
        self.screen.blit(self.edtiontext, (self.displaysize[0] - 100, self.displaysize[1] - 35))

        if self.start_menu_active:
            self.render_start_menu()

        if self.power_menu_active:
            self.render_power_menu()

        # Create a copy of currentapp dictionary
        currentapp_copy = self.currentapp.copy()

        # Iterate over the copy
        for app in currentapp_copy.keys():
            classapp = currentapp_copy[app]["app"]
            classapp.render()
            classapp.titlebar()
            self.screen.blit(classapp.window, currentapp_copy[app]["pos"])
            if classapp.running == False:
                tempthread = threading.Thread(target=classapp.exit)
                tempthread.start()
                del self.currentapp[app]

    def rendertaskbar(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (0, self.displaysize[1] - 20, self.displaysize[0], 20))

    def exit(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def register(self, name, appclass):
        if not name in self.apps:
            self.apps.update({name: appclass})
        else:
            raise NameError(f"{name} is exist")

    def runapp(self, name, pos=(0, 0)):
        if name in self.apps:
            appclass = self.apps[name]()
            self.currentapp.update({name: {
                "app": appclass,
                "pos": pos,
            }})
            appclass.running = True
            tempthread = threading.Thread(target=appclass.init)
            tempthread.start()
        else:
            raise NameError(f"{name} isn't exist")