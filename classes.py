import pygame
import cv2


pygame.mixer.init()
pygame.mixer.set_num_channels(20)
pygame.font.init()


class WorldObject:
    def __init__(self, w: pygame.display, position: list):
        self.position = position
        self.w = w

    def update(self, events: list[pygame.event], keys, elapsed_time_ms: int, camera_pos: list) -> None:
        pass


class WorldObjectDrawn(WorldObject):
    def __init__(self, w: pygame.display, position: list, draw_layer: int):
        WorldObject.__init__(self, w, position)
        self.draw_layer = draw_layer

    def draw(self, camera_pos: list, elapsed_time_ms: int) -> None:
        pass


class WorldObjectSprite(WorldObjectDrawn):
    def __init__(self, w: pygame.display, position: list, texture_path: str, draw_layer: int, texture_scale=1):
        WorldObjectDrawn.__init__(self, w, position, draw_layer)
        self.image_file = texture_path
        if self.image_file.split(".")[-1] == "png":
            self.image_surface = pygame.image.load(self.image_file).convert_alpha()
        else:
            self.image_surface = pygame.image.load(self.image_file).convert()
        self.image_surface = pygame.transform.scale_by(self.image_surface, texture_scale)

    def draw(self, camera_pos: list, elapsed_time_ms: int) -> None:
        self.w.blit(self.image_surface, (self.position[0] - camera_pos[0], self.position[1] - camera_pos[1]))


class WorldObjectVideo(WorldObjectDrawn):
    def __init__(self, w: pygame.display, position: list, video_path: str, draw_layer: int,
                 audio_path=None, paused=True, loop=True, texture_scale=1, play_icon_path=None):
        WorldObjectDrawn.__init__(self, w, position, draw_layer)
        self.texture_scale = texture_scale

        self.play_icon_file = play_icon_path
        self.play_icon_surface = play_icon_path
        if self.play_icon_file is not None:
            if self.play_icon_file.split(".")[-1] == "png":
                self.play_icon_surface = pygame.image.load(self.play_icon_file).convert_alpha()
            else:
                self.play_icon_surface = pygame.image.load(self.play_icon_file).convert()
            self.play_icon_surface = pygame.transform.scale_by(self.play_icon_surface, texture_scale)

        self.video_path = video_path
        self.audio_path = audio_path
        self.audio_channel = None
        self.audio_pygame_sound = None
        self.audio_is_playing = False
        if self.audio_path is not None:
            self.audio_channel = pygame.mixer.find_channel(True)
            self.audio_pygame_sound = pygame.mixer.Sound(self.audio_path)
            self.audio_channel.play(self.audio_pygame_sound, loops=-1)
            if paused:
                self.audio_channel.pause()
                self.audio_is_playing = False
            else:
                self.audio_is_playing = True
            # self.audio_channel.play(self.audio_pygame_sound)
        self.cv2_video_capture = cv2.VideoCapture(video_path)
        self.video_fps = self.cv2_video_capture.get(cv2.CAP_PROP_FPS)
        self.video_frame_interval_ms = 1000 / self.video_fps
        self.ms_since_last_frame = 0
        self.video_paused = paused
        self.video_loop = loop
        self.video_surface = None
        self.video_image = None
        self.success = None
        self.update_video_frame()  # set the first frame

    def update(self, events: list[pygame.event], keys, elapsed_time_ms: int, camera_pos: list) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                real_pos = [self.position[0] - camera_pos[0], self.position[1] - camera_pos[1]]
                mouse_pos = pygame.mouse.get_pos()
                if real_pos[0] < mouse_pos[0] < real_pos[0] + self.video_surface.get_width() and \
                        real_pos[1] < mouse_pos[1] < real_pos[1] + self.video_surface.get_height():
                    self.video_paused = not self.video_paused
                    # print(self.video_paused)

        if self.audio_path is not None:
            if self.video_paused:
                self.audio_is_playing = False
                self.audio_channel.pause()
                return
            if not self.audio_is_playing:
                self.audio_is_playing = True
                self.audio_channel.unpause()
        self.ms_since_last_frame += elapsed_time_ms
        if self.ms_since_last_frame >= self.video_frame_interval_ms:
            self.update_video_frame()

    def draw(self, camera_pos: list, elapsed_time_ms: int) -> None:
        self.w.blit(self.video_surface, (self.position[0] - camera_pos[0], self.position[1] - camera_pos[1]))
        if self.play_icon_surface is not None and self.video_paused:
            play_button_x_offset = self.video_surface.get_width() / 2 - self.play_icon_surface.get_width() / 2
            play_button_y_offset = self.video_surface.get_height() / 2 - self.play_icon_surface.get_height() / 2
            self.w.blit(self.play_icon_surface, (
                self.position[0] - camera_pos[0] + play_button_x_offset,
                self.position[1] - camera_pos[1] + play_button_y_offset
            ))

    def update_video_frame(self):
        self.ms_since_last_frame -= self.video_frame_interval_ms
        self.success, self.video_image = self.cv2_video_capture.read()

        if self.success:
            self.video_surface = pygame.image.frombuffer(  # BGR cause opencv does bgr not rgb for some reason
                self.video_image.tobytes(), self.video_image.shape[1::-1], "BGR")
            self.video_surface = pygame.transform.scale_by(self.video_surface, self.texture_scale)
        else:  # the video ended
            if self.video_loop:
                self.cv2_video_capture = cv2.VideoCapture(self.video_path)
                # self.audio_channel.stop()
                # self.audio_channel.play(self.audio_pygame_sound)
                # self.audio_is_playing = True
            else:
                self.video_paused = True
                self.audio_is_playing = False


class WorldObjectText(WorldObjectDrawn):
    def __init__(self, w: pygame.display, position: list, draw_layer: int, text: str, font: str, font_size: int,
                 color=(255, 255, 255)):
        WorldObjectDrawn.__init__(self, w, position, draw_layer)
        self.pygame_font = pygame.font.SysFont(font, font_size)
        self.text_surface = self.pygame_font.render(text, False, color)

    def draw(self, camera_pos: list, elapsed_time_ms: int) -> None:
        self.w.blit(self.text_surface, (self.position[0] - camera_pos[0], self.position[1] - camera_pos[1]))
        # self.w.blit(self.video_surface, (self.position[0] - camera_pos[0], self.position[1] - camera_pos[1]))


class Player(WorldObjectSprite):
    def __init__(self, w: pygame.display, texture_path: str, player_speed: int, texture_scale=1):
        WorldObjectSprite.__init__(self, w, [0, 0], texture_path, 8, texture_scale)
        self.player_speed = player_speed

    def update(self, events: list[pygame.event], keys, elapsed_time_ms: int, camera_pos: list) -> None:
        # print("player update")
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            speed_mult = 2
        else:
            speed_mult = 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.position[1] -= self.player_speed * speed_mult
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.position[1] += self.player_speed * speed_mult
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.position[0] -= self.player_speed * speed_mult
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.position[0] += self.player_speed * speed_mult


class Camera:
    def __init__(self, w: pygame.display, camera_lag: int):
        self.w = w
        self.position = [self.w.get_width() / 2, self.w.get_height() / 2]
        self.camera_lag = camera_lag

    def track_object(self, world_object: WorldObjectSprite):
        x_offset = self.w.get_width() / 2 - world_object.image_surface.get_width() / 2
        y_offset = self.w.get_height() / 2 - world_object.image_surface.get_height() / 2
        self.position[0] += ((world_object.position[0] - x_offset) - (self.position[0])) / self.camera_lag
        self.position[1] += ((world_object.position[1] - y_offset) - (self.position[1])) / self.camera_lag


class World:
    def __init__(self, w: pygame.display, player: Player, camera_lag: int):
        self.world_objects = []
        self.camera = Camera(w, camera_lag)
        self.player = player
        self.world_objects.append(self.player)

    def update_world(self, events: list[pygame.event], keys, elapsed_time_ms: int):
        for world_object in self.world_objects:
            world_object.update(events, keys, elapsed_time_ms, self.camera.position)

    def draw_world(self, elapsed_time_ms: int):
        self.camera.track_object(self.player)

        draw_layer = 0
        drawn_objects = 0
        already_drawn_objects = []
        while drawn_objects < len(self.world_objects):
            for world_object in self.world_objects:
                if world_object in already_drawn_objects:
                    continue
                if not isinstance(world_object, WorldObjectDrawn):  # if the object doesnt get drawn
                    drawn_objects += 1
                    continue
                if world_object.draw_layer <= draw_layer:
                    drawn_objects += 1
                    already_drawn_objects.append(world_object)
                    world_object.draw(self.camera.position, elapsed_time_ms)
            draw_layer += 1
