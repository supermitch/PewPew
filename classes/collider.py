
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

            if m.rect.colliderect(self.world.planet) and not m.landed:
                m.collide(self.world.planet)
                self.world.stats['monsters_missed'] += 1
                self.world.infection += getattr(m, 'infection', 0)
                m.landed = True


        # Bullets versus Walls
        for b in self.world.bullets:
            if b.rect.bottom < 0:  # Off screen
                b.dead = True

