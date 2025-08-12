from __future__ import annotations
import math
import random
import sys
from dataclasses import dataclass
from typing import List, Tuple

import pygame

# ----------------------------- Config ---------------------------------

WIDTH, HEIGHT = 1000, 650
BG_COLOR = (18, 18, 22)
WALL_MARGIN = 12  # visual padding so circles don't clip the window edges

N_BODIES = 3
RADIUS_RANGE = (20, 35)       # pixels
MASS_FROM_RADIUS = True       # mass = k * r^2 if True, else uniform
MASS_SCALE = 1.0              # k for mass = k * r^2
SPEED_RANGE = (60, 180)       # pixels/s initial speed magnitude
E_COEFF = 1.0                 # 1.0 elastic, <1 inelastic (e.g., 0.8)
SHOW_VECTORS = True
SHOW_TRAILS = False
TRAIL_LENGTH = 140            # points

TARGET_FPS = 60
VELOCITY_VECTOR_SCALE = 0.20  # arrow length = scale * |v| (tuned for readability)

# Chart settings
CHART_WIDTH = 280
CHART_HEIGHT = 180
CHART_HISTORY = 300  # frames to keep in history
SHOW_CHARTS = True

# Positional correction to prevent sinking after collision resolution
PERCENT_CORRECTION = 0.8
SLOP = 0.01

# ----------------------------------------------------------------------

Vec = pygame.math.Vector2


@dataclass
class Chart:
    """Simple real-time chart for physics data visualization"""
    def __init__(self, title: str, color: Tuple[int, int, int], max_history: int = CHART_HISTORY):
        self.title = title
        self.color = color
        self.data = []
        self.max_history = max_history
        self.min_val = 0
        self.max_val = 1
    
    def add_point(self, value: float):
        self.data.append(value)
        if len(self.data) > self.max_history:
            self.data.pop(0)
        
        # Update min/max for scaling
        if self.data:
            self.min_val = min(self.data)
            self.max_val = max(self.data)
            if self.max_val == self.min_val:  # prevent division by zero
                self.max_val = self.min_val + 1
    
    def draw(self, surf: pygame.Surface, x: int, y: int, width: int, height: int, font):
        if len(self.data) < 2:
            return
        
        # Background
        pygame.draw.rect(surf, (30, 30, 35), (x, y, width, height))
        pygame.draw.rect(surf, (60, 60, 70), (x, y, width, height), 2)
        
        # Title
        title_text = font.render(self.title, True, (200, 200, 210))
        surf.blit(title_text, (x + 5, y + 5))
        
        # Current value
        current_val = self.data[-1] if self.data else 0
        val_text = font.render(f"{current_val:.1f}", True, self.color)
        surf.blit(val_text, (x + width - 60, y + 5))
        
        # Graph area
        graph_y = y + 25
        graph_height = height - 30
        
        # Plot data points
        points = []
        for i, value in enumerate(self.data):
            # Normalize value to graph height
            normalized = (value - self.min_val) / (self.max_val - self.min_val)
            plot_x = x + (i * width) // len(self.data)
            plot_y = graph_y + graph_height - (normalized * graph_height)
            points.append((plot_x, int(plot_y)))
        
        if len(points) > 1:
            pygame.draw.lines(surf, self.color, False, points, 2)


@dataclass
class Body:
    pos: Vec
    vel: Vec
    radius: float
    mass: float
    color: Tuple[int, int, int]
    trail: List[Tuple[int, int]]

    def inv_mass(self) -> float:
        return 0.0 if self.mass == 0 else 1.0 / self.mass

    def move(self, dt: float):
        self.pos += self.vel * dt

    def record_trail(self):
        self.trail.append((int(self.pos.x), int(self.pos.y)))
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop(0)


class World:
    def __init__(self, w: int, h: int, e: float):
        self.w, self.h = w, h
        self.e = e
        self.bodies: List[Body] = []
        
        # Initialize charts
        self.charts = {
            'momentum': Chart("Total Momentum", (108, 163, 255)),  # blue
            'kinetic_energy': Chart("Kinetic Energy", (235, 99, 132)),  # pink
            'speed_avg': Chart("Avg Speed", (116, 222, 163)),  # green
            'collisions': Chart("Collisions/Frame", (255, 187, 99))  # orange
        }
        self.collision_count = 0

    # ---------- initialization ----------
    def random_bodies(self, n: int):
        self.bodies.clear()
        attempts = 0
        for _ in range(n):
            for _try in range(2000):
                r = random.randint(*RADIUS_RANGE)
                x = random.randint(WALL_MARGIN + r, self.w - WALL_MARGIN - r)
                y = random.randint(WALL_MARGIN + r, self.h - WALL_MARGIN - r)
                pos = Vec(x, y)

                speed = random.uniform(*SPEED_RANGE)
                angle = random.uniform(0, 2 * math.pi)
                vel = Vec(math.cos(angle), math.sin(angle)) * speed

                mass = (MASS_SCALE * (r ** 2)) if MASS_FROM_RADIUS else 1.0

                if all((pos.distance_to(b.pos) >= (r + b.radius + 2)) for b in self.bodies):
                    color = self._nice_color()
                    self.bodies.append(Body(pos, vel, r, mass, color, []))
                    break
            else:
                attempts += 1
        if attempts:
            print(f"[warn] had trouble placing {attempts} body/bodies without overlap.")

    @staticmethod
    def _nice_color():
        palette = [
            (235, 99, 132),  # pink
            (108, 163, 255), # blue
            (255, 187, 99),  # orange
            (116, 222, 163), # green
            (210, 127, 255), # purple
            (255, 122, 122), # red
            (129, 236, 255), # cyan
        ]
        return random.choice(palette)

    # ---------- physics ----------
    def step(self, dt: float):
        # move
        for b in self.bodies:
            b.move(dt)

        # walls
        for b in self.bodies:
            # left/right
            if b.pos.x - b.radius < WALL_MARGIN and b.vel.x < 0:
                b.pos.x = WALL_MARGIN + b.radius
                b.vel.x *= -self.e
            elif b.pos.x + b.radius > self.w - WALL_MARGIN and b.vel.x > 0:
                b.pos.x = self.w - WALL_MARGIN - b.radius
                b.vel.x *= -self.e
            # top/bottom
            if b.pos.y - b.radius < WALL_MARGIN and b.vel.y < 0:
                b.pos.y = WALL_MARGIN + b.radius
                b.vel.y *= -self.e
            elif b.pos.y + b.radius > self.h - WALL_MARGIN and b.vel.y > 0:
                b.pos.y = self.h - WALL_MARGIN - b.radius
                b.vel.y *= -self.e

        # pairwise collisions
        n = len(self.bodies)
        for i in range(n):
            for j in range(i + 1, n):
                self.resolve_collision(self.bodies[i], self.bodies[j])

        # trails
        for b in self.bodies:
            if SHOW_TRAILS:
                b.record_trail()
            else:
                b.trail.clear()

    def resolve_collision(self, A: Body, B: Body):
        # Vector from A to B
        n = B.pos - A.pos
        dist = n.length()
        min_dist = A.radius + B.radius

        if dist == 0:
            # Rare pathological overlap; separate along arbitrary axis
            n = Vec(1, 0)
            dist = 1e-6

        if dist < min_dist:  # overlap => collide/resolve
            # Normalize collision normal
            normal = n / dist

            # Relative velocity along normal
            rv = B.vel - A.vel
            vel_along_normal = rv.dot(normal)

            # If moving apart, skip impulse (but still positional correction)
            if vel_along_normal > 0:
                pass
            else:
                e = self.e
                inv_mass_sum = A.inv_mass() + B.inv_mass()
                if inv_mass_sum == 0:
                    return

                j = -(1 + e) * vel_along_normal
                j /= inv_mass_sum

                impulse = j * normal
                A.vel -= impulse * A.inv_mass()
                B.vel += impulse * B.inv_mass()

            # Positional correction to prevent sticking
            penetration = min_dist - dist
            correction_mag = max(penetration - SLOP, 0.0) * (PERCENT_CORRECTION / (A.inv_mass() + B.inv_mass()))
            correction = correction_mag * normal
            A.pos -= correction * A.inv_mass()
            B.pos += correction * B.inv_mass()

    # ---------- measures ----------
    def totals(self) -> Tuple[Vec, float]:
        p = Vec(0, 0)
        ke = 0.0
        for b in self.bodies:
            p += b.mass * b.vel
            ke += 0.5 * b.mass * b.vel.length_squared()
        return p, ke


# ----------------------------- Drawing --------------------------------

def draw_arrow(surf: pygame.Surface, start: Vec, vec: Vec, width: int = 2):
    end = start + vec
    pygame.draw.line(surf, (230, 230, 230), (start.x, start.y), (end.x, end.y), width)
    # simple head
    if vec.length_squared() > 1e-3:
        head = vec.normalize() * 8
        left = Vec(-head.y, head.x) * 0.4
        right = Vec(head.y, -head.x) * 0.4
        p1 = end
        p2 = end - head + left
        p3 = end - head + right
        pygame.draw.polygon(surf, (230, 230, 230), [(p1.x, p1.y), (p2.x, p2.y), (p3.x, p3.y)])


def main():
    global SHOW_VECTORS, SHOW_TRAILS

    pygame.init()
    pygame.display.set_caption("2D Collision Sandbox (elastic/inelastic)")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)

    world = World(WIDTH, HEIGHT, E_COEFF)
    world.random_bodies(N_BODIES)

    paused = False
    running = True

    while running:
        dt = clock.tick(TARGET_FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    world.random_bodies(N_BODIES)
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_t:
                    SHOW_TRAILS = not SHOW_TRAILS
                elif event.key == pygame.K_v:
                    SHOW_VECTORS = not SHOW_VECTORS

        if not paused:
            world.step(dt)

        # ---- draw ----
        screen.fill(BG_COLOR)

        # trails
        if SHOW_TRAILS:
            for b in world.bodies:
                if len(b.trail) > 1:
                    pygame.draw.lines(screen, b.color, False, b.trail, 2)

        # bodies & vectors
        for b in world.bodies:
            pygame.draw.circle(screen, b.color, (int(b.pos.x), int(b.pos.y)), b.radius)
            pygame.draw.circle(screen, (25, 25, 30), (int(b.pos.x), int(b.pos.y)), b.radius, 2)
            if SHOW_VECTORS:
                draw_arrow(screen, b.pos, b.vel * VELOCITY_VECTOR_SCALE)

        # HUD
        p, ke = world.totals()
        hud = f"e={world.e:.2f} | bodies={len(world.bodies)} | Σ|p|={p.length():7.1f} | KE={ke:9.1f} | FPS={clock.get_fps():5.1f}"
        text = font.render(hud, True, (230, 230, 235))
        screen.blit(text, (14, 12))

        help1 = font.render("[Space]=reset  [P]=pause  [T]=trails  [V]=vectors  [Esc/Q]=quit", True, (160, 160, 170))
        screen.blit(help1, (14, 36))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
