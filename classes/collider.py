import math


def collide_rect_circle(rect, circle):
    """
    Return True if a rect and a circle are overlapping.

    We actually wrap the rect in a circle and do circle-circle collision,
    so it's a bit conservative.
    """
    # First wrap rect in a circle of radius r1
    x1, y1 = rect.centerx, rect.centery
    r1 = math.sqrt((rect.height / 2) ^ 2 + (rect.width / 2) ^ 2)

    x2, y2 = circle.x, circle.y
    r2 = circle.radius

    distance = math.sqrt((abs(x2 - x1)) ^ 2 + (abs(y2 - y1)) ^ 2)
    if distance < (r1 + r2):  # If distance from center to center < r1 + r2
        return True
    else:
        return False


class Collider(object):
    def __init__(self, world):
        self.world = world

    def update(self):
        """ Run the collider. """

        h = self.world.hero
        # Check hero against walls
        for w in self.world.walls:
            if w.rect.colliderect(h.rect):
                h.collide(w, 0.5, True)
                break

        for m in self.world.monsters:
            # Monster versus hero
            if m.rect.colliderect(h.rect):
                h.collide(m, 1.0, False)
                m.collide(h)
                self.world.add_explosion(m)
                if not h.dead:
                    self.world.assets.sounds['hit'].play()

            # Monster versus Bullets
            for b in self.world.bullets:
                if m.rect.colliderect(b.rect) \
                    or m.rect.colliderect(b.next_rect):
                    self.world.stats['bullets_hit'] += 1
                    m.collide(b)
                    b.collide(m)
                    if m.dead:
                        self.world.stats['monsters_killed'] += 1
                        self.world.add_explosion(m)
                    else:
                        self.world.assets.sounds['hit'].play()
                    break  # Can only hit one bullet at a time

            for b in self.world.bombs:
                if not b.exploding:
                    collision = m.rect.colliderect(b.rect)
                else:
                    collision = collide_rect_circle(m.rect, b.blast_radius)

                if collision:
                    m.collide(b)
                    b.collide(m)
                    if m.dead:
                        self.world.stats['monsters_killed'] += 1
                        self.world.add_explosion(m)
                    else:
                        self.world.assets.sounds['hit'].play()
                    if b.dead:
                        self.world.add_explosion(b)

            # Monster versus planet
            if m.rect.colliderect(self.world.planet) and not m.landed:
                m.collide(self.world.planet)
                self.world.stats['monsters_missed'] += 1
                self.world.infection += getattr(m, 'infection', 0)
                m.landed = True


        # Bullets versus Walls
        for b in self.world.bullets:
            if b.rect.bottom < 0:  # Off screen
                b.dead = True
            for w in self.world.walls:
                if b.rect.colliderect(w.rect):
                    b.dead = True

