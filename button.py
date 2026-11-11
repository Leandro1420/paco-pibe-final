import pygame

class Button():
    def __init__(self):
        self.menu = ''
        self.rect = pygame.rect.Rect((0,0),(10,10))
        self.hovering = False
        self.pressing = False
        self.default_color = (100,100,100)
        self.hovering_color = (50,50,50)
        self.pressed_color = (20,20,20)
        self.current_color = self.default_color
        self.border_radius = -1
        self.border_color = (0,0,0)
        self._text = ''
        self.text_color = (255,255,255)
        self.font_size = 30
        self.font = pygame.font.SysFont('consolas', self.font_size)
        self.text_surface = self.font.render(self.text, False, self.text_color)
        self.border_width = 3


    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovering:
                self.on_hover()
            self.hovering = True
            self.on_hovering
            self.current_color = self.hovering_color

            if pygame.mouse.get_pressed()[0]:
                if not self.pressing:
                    self.on_press()
                self.pressing = True
                self.on_pressing()
                self.current_color = self.pressed_color
            else:
                self.pressing = False
        else:
            self.hovering = False
            self.pressing = False
            self.current_color = self.default_color


    def draw(self, screen):
        pygame.draw.rect(screen, self.border_color, self.rect, 0, self.border_radius)
        inner_rect = (self.rect.x + self.border_width, self.rect.y + self.border_width),(self.rect.w - 2*self.border_width, self.rect.h - 2*self.border_width)
        pygame.draw.rect(screen, self.current_color, inner_rect, 0, self.border_radius)

        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)


    def on_press(self):
        pass


    def on_pressing(self):
        pass


    def on_hover(self):
        pass


    def on_hovering(self):
        pass


    @property
    def text(self):
        return self._text


    @text.setter
    def text(self, text: str):
        self._text = text
        self.text_surface = self.font.render(self.text, True, self.text_color)
