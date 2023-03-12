class Target:
    def __init__(self):
        self.points = 0
        self.live = 1
        self.new_target()
        self.screen = screen
        self.x = random.randint(50, 750)
        self.y = random.randint(50, 550)
        self.radius = random.randint(20, 40)
        self.color = constants.RED

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = "red"

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.radius
        )