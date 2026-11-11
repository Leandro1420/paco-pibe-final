import pygame

class TextBar():
    def __init__(self):
        self.menu = ''
        self._text = 'Nombre'
        self.text_color = (0,0,0)
        self.color = (255,255,255)
        self.hovering = False
        self.pressing = False
        self.focused = False
        self.font_size = 20
        self.font = pygame.font.SysFont('consolas', self.font_size)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.rect = pygame.rect.Rect((0,0),(50,self.font_size + 4))


    def update(self, text_input):
        #si paso el mouse por arriba
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovering:
                self.on_hover()
            self.hovering = True
            self.on_hovering
            #si presiono
            if pygame.mouse.get_pressed()[0]:
                if not self.pressing:
                    self.on_press()
                self.pressing = True
                self.on_pressing()
            else:
                self.pressing = False
        else:
            self.hovering = False
            self.pressing = False

            if pygame.mouse.get_pressed()[0]:
                self.focused = False

        if self.focused:
            if text_input != '':
                self.text += text_input

            keys = pygame.key.get_just_pressed()
            if keys[pygame.K_BACKSPACE]:
                self.text = self.text[:-2]


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_rect = self.text_surface.get_rect(midleft=self.rect.midleft)
        text_rect.update((pygame.Vector2(text_rect.topleft) + (5,2)), (text_rect.size))
        screen.blit(self.text_surface, text_rect)


    def on_press(self):
        self.focused = True
        self.text = ''



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