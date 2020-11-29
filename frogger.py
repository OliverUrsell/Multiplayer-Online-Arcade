import pygame
from pygame.locals import *
import random
#import mqtt-frogger
import paho.mqtt.client as mqtt
import sys



PLAYERMAX = 40
REFRESH = 60
EASY_MODE = True

FramePerSecond = pygame.time.Clock()

vec = pygame.math.Vector2

sprites = pygame.sprite.Group()

pygame.font.init()

myfont = pygame.font.Font("JetBrainsMono-Medium.ttf", 30)








class Frogger:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._intro = True
        self._gameover = False
        #self.size = self.width, self.height = WIDTH, HEIGHT
        self.elapsed_time = 0
        self.frogs = []
        self.cars = []
        self.finished = []
        self.names = []
        self.font = myfont#pygame.font.SysFont('Arial', 25)



    # CLIent stuff
    def mqtt_on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("check/server")
        client.subscribe("move/server")
        print("subscribed")

    def send_message(self, client, topic, payload):
        client.publish(topic, payload=payload, qos=1, retain=False)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        # Convert bits to string and remove b''
        payload = str(msg.payload)[2:-1]
        if msg.topic == "check/server":
            if payload[:-3] in self.names:
                self.send_message(client, "check/player/", payload + 'n')
            else:
                self.on_connect(payload[:-3])
                self.send_message(client, "check/player/" + payload , 'frogger')
        elif msg.topic == "move/server":
            if payload[-1:] == "f":
                self.move_forward(payload[:-1])
            elif payload[-1:] == "b":
                self.move_backward(payload[:-1])
            elif payload[-4:] == "lost":
                self.on_disconnect(payload[:-4])


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self._running = True
        pygame.display.set_caption("fro gge")

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False



    def on_loop(self):


        for car in self.cars:
            car.move()
            if car.pos.x < -30 or car.pos.x > self.WIDTH + 50:
                self.cars.remove(car)
                car.remove()


        for frog in self.frogs:
            #frog.move()
            if frog.finished:
                self.finished.append(frog.name)
                self._gameover = True
                print("Frog: ",frog.name, " Finished")
                frog.pass_away()
                self.frogs.remove(frog)
                # here they pass away peacefully after a long and fufilling life, surrounded by people who love them ;_;

            elif frog.rect.collidelist(self.cars) != -1:

                if EASY_MODE:
                    frog.restart()

                else:
                    self.frogs.remove(frog)

                    # rip frog ;_;
                    frog.pass_away()


        self.elapsed_time += FramePerSecond.get_time()
        if int(self.elapsed_time / 90) > 1:
            self.elapsed_time = 0
            self.make_car()

        FramePerSecond.tick(REFRESH)

    # hehe makes all the frogs :)
    def create_frogs(self):
        frog_count = len(self.names)
        # functional with
        gap = ((3/4)*self.WIDTH)/frog_count
        xpos = (1/8)*self.WIDTH
        if frog_count == 1:
            xpos = 1/2*self.WIDTH
            size = self.X_INC/2
            gap = 0
        elif frog_count < 30:
            size = self.X_INC/2
        else:
            smaller = (frog_count - 30)/35
            size = self.X_INC/(2+smaller)

        for name in self.names:
            frog = Frog(xpos,self,name,size)
            xpos += gap + gap/frog_count
            self.frogs.append(frog)
            sprites.add(frog)

            colour = frog.colour
            self.setColor(self.client,name,"{0:0=3d}".format(colour.r),"{0:0=3d}".format(colour.g),"{0:0=3d}".format(colour.b))


    def setColor(self,client, player_name, r, g, b):
        # Set the color of the player controls to match their own
        self.send_message(self.client, "move/player/"+player_name, r + g + b)


    def find_frog(self,name):
        for frog in self.frogs:
            if frog.name == name:
                return frog
        return -1

    def remove_frog(self,name): # :(
        frog_to_bonk = find_frog(name)
        if frog_to_bonk != -1:
            frog.pass_away()
            self.frogs.remove(frog)

    def make_car(self):
        car = Car(random.randint(3,18),random.randint(0,4),self)
        self.cars.append(car)


    def on_render(self):
        self._display_surf.fill((0,0,0))
        if self._intro:
            self._display_surf.blit(self.font.render("                           /// Press 'p' to start /// ", True, (255,0,0)), (self.WIDTH/7, self.HEIGHT/7))
            self._display_surf.blit(self.font.render("Connected players:                                    ", True, (255,0,0)), (self.WIDTH/7, self.HEIGHT/6))
            y_offset = 60
            x_offset = 20
            rowcount = 1
            for player in self.names:
                self._display_surf.blit(self.font.render(str(player),True, (255,0,0)), ((self.WIDTH/4)+x_offset, (self.HEIGHT/6)+y_offset))
                y_offset += 30
                rowcount += 1
                if rowcount >= 15:
                    x_offset += 240
                    y_offset = 60
                    rowcount = 1
        if self._gameover:
            self._display_surf.blit(self.font.render("/// Leaderboard /// ", True, (255,0,0)), (self.WIDTH/7, self.HEIGHT/7))
            place = 1
            for winner in self.finished:
                self._display_surf.blit(self.font.render("{}. {}".format(place,self.finished[place-1]), True, (255,0,0)), (self.WIDTH/7, (self.HEIGHT/7)+ place*35))
                place += 1



        for entity in sprites:
            self._display_surf.blit(entity.surf, entity.rect)

        pygame.display.update()


    def on_cleanup(self):
        pygame.quit()
        self.client.loop_stop()
        sys.exit(0)



    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        self.WIDTH = pygame.display.Info().current_w
        self.HEIGHT = pygame.display.Info().current_h
        self.X_INC = self.WIDTH/40
        self.Y_INC = self.HEIGHT/20

        plat1 = Platform(self.HEIGHT -10,self.WIDTH)
        plat2 = Platform(10,self.WIDTH)



        # connection stuff
        self.client = mqtt.Client()
        self.client.on_connect = self.mqtt_on_connect
        self.client.on_message = self.on_message
        self.client.will_set("move/player", payload="disconnected", qos=1, retain=False)
        self.client.connect("test.mosquitto.org", 1883, 60)
        self.client.loop_start()



        sprites.add(plat1,plat2)

        # TO TEST LOTS OF PEOPLE
        #self.names = ["1234567890" for x in range(100)]

        while(self._intro):
            events = pygame.event.get()
            for event in events:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p and len(self.names) > 0:
                        self._intro=False
                    elif event.key == pygame.K_q:
                        self.on_cleanup()
                self.on_event(event)
            self.on_loop()
            self.on_render()


        self.create_frogs()

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.on_cleanup()
            self.on_loop()
            self.on_render()

        self.on_cleanup()




    def on_connect(self, player_name):
        self.names.append(player_name)
        #self.create_frog(player_name)
        # Player has joined the game



    def on_disconnect(self, player_name):
        self.names.remove(player_name)
        self.remove_frog(player_name)
        # Player has disconnected

    def move_forward(self, player_name):
        #print(player_name + "forward")
        frog = self.find_frog(player_name)
        if frog != -1:
            frog.move(1)
        pass

    def move_backward(self, player_name):
        # Code here
        #print(player_name + "back")
        frog = self.find_frog(player_name)
        if frog != -1:
            frog.move(-1)
        pass

    def disconnect(self,client):
        # Send all players back to homescreen
        self.send_message(client, "move/player", "disconnect")

    def set_playercolour(self,name,color):
        pass


class Car(pygame.sprite.Sprite):
    def __init__(self,ypos,length,frogger):
        super().__init__()
        self.direction = -1 if ypos % 2 == 0 else 1
        xcoord = -30 if self.direction == 1 else frogger.WIDTH + 30
        self.pos = vec((xcoord,frogger.Y_INC*ypos))
        self.speed = ypos % 3 + 2
        self.surf = pygame.Surface((50+15*length, 30))
        self.surf.fill((180,180,180))
        self.rect = self.surf.get_rect(center = (self.pos))
        self.rect.midbottom = self.pos
        sprites.add(self)

    def move(self):
        self.pos.x += self.speed*self.direction
        self.rect.midbottom = self.pos

    def remove(self):
        self.rect = None
        sprites.remove(self)




class Frog(pygame.sprite.Sprite):
    def __init__(self,xpos,frogger,name,size):
        super().__init__()
        self.surf = pygame.Surface((size,size)) #30 for bigg frogg, 15 for smalll frigg
        self.name = name

        colourval = ((xpos-(frogger.WIDTH*1/8))/(frogger.WIDTH*3/4)) * 360
        self.colour = pygame.Color(255,255,255)
        self.colour.hsva = (colourval,100,100,1)


        self.surf.fill(self.colour)#(128,255,40))
        self.pos = vec((xpos,frogger.HEIGHT - frogger.Y_INC))
        self.vel = vec(0,frogger.Y_INC)
        self.HEIGHT = frogger.HEIGHT
        self.Y_INC = frogger.Y_INC
        self.rect = self.surf.get_rect(center = (self.pos))
        self.finished = False
        sprites.add(self)


    def move(self, direction):
        #pressed_keys = pygame.key.get_pressed()

        if direction == 1:
            self.pos -= self.vel
        if direction == -1:
            self.pos += self.vel

        if self.pos.y > self.HEIGHT-self.Y_INC:
            self.pos.y = self.HEIGHT - self.Y_INC
        if self.pos.y < self.Y_INC:
            self.finished = True
            self.pos.y = self.Y_INC

        self.rect.midbottom = self.pos

    def restart(self):
        self.pos.y = self.HEIGHT - self.Y_INC
        self.rect.midbottom = self.pos

    def pass_away(self):
        self.rect = None
        sprites.remove(self)



class Platform(pygame.sprite.Sprite):
    def __init__(self,ypos,width):
        super().__init__()
        self.surf = pygame.Surface((width, 20))
        self.surf.fill((255,0,0))
        self.pos = vec((width/2, ypos)) # (WIDTH/2, HEIGHT - 10)
        self.rect = self.surf.get_rect(center = (self.pos))




if __name__ == "__main__":
    froggerInstance = Frogger()
    froggerInstance.on_execute()
