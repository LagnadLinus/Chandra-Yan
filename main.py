import randomfrom kivy.config import Configfrom kivy.core.audio import SoundLoaderfrom kivy.lang import Builderfrom kivy.uix.relativelayout import RelativeLayout# We need to do this before any other kivy import.Config.set('graphics', 'width', '900')Config.set('graphics', 'height', '400')from kivy import platformfrom kivy.core.window import Windowfrom kivy.app import Appfrom kivy.graphics import Color, Line, Quad, Trianglefrom kivy.properties import NumericProperty, Clock, ObjectProperty, StringPropertyBuilder.load_file("menu.kv")  # Calling menu#   1. Creating Perspectiveclass MainWidget(RelativeLayout):    from trans import transform, transform_2D, transform_perspective    from client_steps import keyboard_closed, on_keyboard_up, on_keyboard_down    menu_widget = ObjectProperty()    perspective_point_x = NumericProperty(0)  # Creating Variable    perspective_point_y = NumericProperty(0)    # Creating Vertical Lines    V_NB_LINES = 8  # we need to put odd number here to balance the line and put 1 in centre    V_LINES_SPACING = .4  # Percentage in screen width    # The value given above is in % because the app needs to adapt in different windows size for eg: in ipad, phone..    vertical_lines = []  # To manage multiple vertical lines    # Creating Horizontal Lines    H_NB_LINES = 15    H_LINES_SPACING = .1  # Percentage in screen height    horizontal_lines = []  # To manage multiple horizontal lines    SPEED = .8    current_offset_y = 0  # defining and initializing the variable    current_y_loop = 0    SPEED_X = 3.0    current_speed_x = 0  # intermediate value to make the touch value precise.    current_offset_x = 0    # Collection of tiles with a list    NB_TILES = 16    tiles = []  # Here we can put how many tiles we want.    tiles_coordinates = []  # list of tile coordinates    # Giving spaceship sizes    YAN_WIDTH = .1    YAN_HEIGHT = 0.035    YAN_BASE_Y = 0.04    yan = None  # This contains triangle instructions    yan_coordinates = [(0, 0), (0, 0), (0, 0)]    state_game_over = False  # default is not game over for the game    # For making the game not start directly    state_game_has_started = False    menu_title = StringProperty("C H A N D R A    Y A N ")    menu_button_title = StringProperty("START")    score_txt = StringProperty()    sound_begin = None    sound_galaxy = None    sound_gameover_impact = None    sound_gameover_voice = None    sound_music1 = None    sound_restart = None    # Note: We don't give pixel dimension size for the spaceship because it looks small when the screen size is bigger.    # To get the size of the windows, we are using init    def __init__(self, **kwargs):        super(MainWidget, self).__init__(**kwargs)        # print("INIT W:" + str(self.width) + "H:" + str(self.height))        # (Using it Later)        self.init_audio()        self.init_vertical_lines()  # Calling from init function vertical_lines.        self.init_horizontal_lines()        self.init_tiles()        self.init_yan()        self.reset_game()        if self.is_desktop():  # if desktop then we are going to implement keyboard            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)            self._keyboard.bind(on_key_down=self.on_keyboard_down)            self._keyboard.bind(on_key_up=self.on_keyboard_up)        Clock.schedule_interval(self.update, 1.0 / 60.0)  # calling update function with time interval: 1 is 1        # time /s        self.sound_galaxy.play()    # For adding the sound    def init_audio(self):        self.sound_begin = SoundLoader.load("audio/begin.wav")        self.sound_galaxy = SoundLoader.load("audio/galaxy.wav")        self.sound_gameover_impact = SoundLoader.load("audio/gameover_impact.wav")        self.sound_gameover_voice = SoundLoader.load("audio/gameover_voice.wav")        self.sound_music1 = SoundLoader.load("audio/music1.wav")        self.sound_restart = SoundLoader.load("audio/restart.wav")        self.sound_music1.volume = .2        self.sound_begin.volume = .60        self.sound_galaxy.volume = .60        self.sound_gameover_voice.volume = .25        self.sound_restart.volume = .6        self.sound_gameover_impact.volume = .3    # For resetting the game    def reset_game(self):        self.current_offset_y = 0        self.current_y_loop = 0        self.current_speed_x = 0        self.current_offset_x = 0        self.tiles_coordinates = []        self.score_txt = "SCORE: 0 " + str(self.current_y_loop)        self.pre_fill_tiles_coordinates()        self.generate_tiles_coordinates()        self.state_game_over = False    # Defining a function if in mobile or desktop    def is_desktop(self):        if platform in ('linux', 'windows', 'macosx'):            return True        return False    # So the value matches, when the size of the windows change, it automatically adapts    # We can also do this in different way in which we can do from the chandra.kv file.    # commenting the self.perspective_point,and using equivalent  on kv file.    # Creating a spaceship    def init_yan(self):        with self.canvas:            Color(0, 0, 0)            self.yan = Triangle()    # Updating a coordinates for a ship    def update_yan(self):        center_x = self.width / 2        base_y = self.YAN_BASE_Y * self.height        yan_half_width = self.YAN_WIDTH * self.width / 2        yan_height = self.YAN_HEIGHT * self.height        # .......        #     2        #   1   3        # self.transform        self.yan_coordinates[0] = (center_x - yan_half_width, base_y)  # For the first point        self.yan_coordinates[1] = (center_x, base_y + yan_height)  # For the second point        self.yan_coordinates[2] = (center_x + yan_half_width, base_y)  # For the third point        x1, y1 = self.transform(*self.yan_coordinates[0])  # Transform function needs two arguments, i.e., x & y.        # self_yan_coordinates[0] looks like only 1 argument containing a tuple hence to expand it we add star to        # make it two arguments.        x2, y2 = self.transform(*self.yan_coordinates[1])        x3, y3 = self.transform(*self.yan_coordinates[2])        self.yan.points = [x1, y1, x2, y2, x3, y3]    # Now making collision effect and printing game over when the ship stays out of track    def check_yan_collision(self):  # This will return True if the ship is on the track else False & Game-over.        for i in range(0, len(self.tiles_coordinates)):            ti_x, ti_y = self.tiles_coordinates[i]            if ti_y > self.current_y_loop + 1:  # We are testing the first two range of tile therefore +1 because                # ship is always at the bottom                return False            if self.check_yan_collision_with_tile(ti_x, ti_y):                return True        return False    def check_yan_collision_with_tile(self, ti_x, ti_y):        xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)        xmax, ymax = self.get_tile_coordinates(ti_x + 1, ti_y + 1)        for i in range(0, 3):  # looping to see collision or not            px, py = self.yan_coordinates[i]            if xmin <= px <= xmax and ymin <= py <= ymax:                return True        return False    # Creating tiles in 2D and then transforming it to perspective.    def init_tiles(self):        with self.canvas:  # adding line instruction in canvas            Color(1, 1, 1)  # Tile Color            for i in range(0, self.NB_TILES):                self.tiles.append(Quad())    def pre_fill_tiles_coordinates(self):        for i in range(0, 10):            self.tiles_coordinates.append((0, i))  # in the tuple i.e. parentheses inside parentheses we put 0 for            # the x and i for the range (y).    # Defining a function to generate infinite tile coordinates    def generate_tiles_coordinates(self):        last_x = 0        last_y = 0        # clean the coordinates that are out of the screen        # condition i.e. ti_y < self.current_y_loop        for i in range(len(self.tiles_coordinates)-1, -1, -1):  # starting with maximum value and the decrementing            # with -1 and the middle -1 is to put on the position 0.            if self.tiles_coordinates[i][1] < self.current_y_loop:                del self.tiles_coordinates[i]        if len(self.tiles_coordinates) > 0:            last_coordinates = self.tiles_coordinates[-1]            last_x = last_coordinates[0]            last_y = last_coordinates[1] + 1  # For generating next tile        print("I")        for i in range(len(self.tiles_coordinates), self.NB_TILES):            r = random.randint(0, 2)  # random number for moving tile left and right            # lets say:            # 0 -> straight            # 1 -> right            # 2 -> left            start_index = -int(self.V_NB_LINES / 2) + 1            end_index = start_index + self.V_NB_LINES - 1            if last_x <= start_index:                r = 1            if last_x >= end_index - 1:                r = 2            self.tiles_coordinates.append((last_x, last_y))            if r == 1:  # if its equal to 1, we go right                last_x += 1  # For the 2nd pattern                self.tiles_coordinates.append((last_x, last_y))                last_y += 1  # For going forward 1st Pattern                self.tiles_coordinates.append((last_x, last_y))            if r == 2:  # if its equal to 1, we go left                last_x -= 1  # For the 3rd pattern                self.tiles_coordinates.append((last_x, last_y))                last_y += 1  # For going forward 1st Pattern                self.tiles_coordinates.append((last_x, last_y))            last_y += 1        print("T")    # 2. Creating Vertical Lines in 2D and then transforming it to perspective.    def init_vertical_lines(self):        with self.canvas:  # adding line instruction in canvas            Color(1, 1, 1)            # Line(points=[100, 0, 100, 100])  # Line instructions with points            # Making line in the centre even when we adjust the windows            # To create a line in the centre first create a variable at the top named as Line            # self.Line = Line(points=[100, 0, 100, 100])                           # Might use later            for i in range(0, self.V_NB_LINES):                self.vertical_lines.append(Line())    def get_line_x_from_index(self, index):        central_line_x = self.perspective_point_x        spacing = self.V_LINES_SPACING * self.width        offset = index - 0.5  # when index is 0, we will be half-way to the left        line_x = central_line_x + offset * spacing + self.current_offset_x        return line_x    def get_line_y_from_index(self, index):        spacing_y = self.H_LINES_SPACING * self.height        line_y = index * spacing_y - self.current_offset_y  # suppose we start from 0 and it will be 0-offset created        # for illusion of going forward.        return line_y    def get_tile_coordinates(self, ti_x, ti_y):        ti_y = ti_y - self.current_y_loop  # This will make tile evolving on the initial level        x = self.get_line_x_from_index(ti_x)        y = self.get_line_y_from_index(ti_y)        return x, y    def update_tiles(self):        for i in range(0, self.NB_TILES):            tile = self.tiles[i]            tile_coordinates = self.tiles_coordinates[i]            xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])            xmax, ymax = self.get_tile_coordinates(tile_coordinates[0] + 1, tile_coordinates[1] + 1)            # computing the below points.            #  2    3            #            #  1    4            x1, y1 = self.transform(xmin, ymin)            x2, y2 = self.transform(xmin, ymax)            x3, y3 = self.transform(xmax, ymax)            x4, y4 = self.transform(xmax, ymin)            # We are giving points to the tile.            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]    # Creating a new Fn to give lines new points    def update_vertical_lines(self):        # computing this and adding int coordinate because there are some decimals in the coordinate        # The line will be drawn but not totally well.        # Now to have multiple vertical lines on left and right.        # We are going to define the total number of lines and spacing in between them.        # We are also going to have 7 lines in our case which is from V_NB_LINES.        # we are also going to re-assign the points to each line.        # For ex: if we have 4 lines i.e. -1, 0, 1, 2        start_index = -int(self.V_NB_LINES / 2) + 1        for i in range(start_index, start_index + self.V_NB_LINES):            line_x = self.get_line_x_from_index(i)            # Transforming 2D coordinates            x1, y1 = self.transform(line_x, 0)            x2, y2 = self.transform(line_x, self.height)            self.vertical_lines[i].points = [x1, y1, x2, y2]    def init_horizontal_lines(self):        with self.canvas:  # adding line instruction in canvas            Color(1, 1, 1)            # Line(points=[100, 0, 100, 100])  # Line instructions with points            # Making line in the centre even when we adjust the windows            # To create a line in the centre first create a variable at the top named as Line            for i in range(0, self.H_NB_LINES):                self.horizontal_lines.append(Line())    def update_horizontal_lines(self):        start_index = -int(self.V_NB_LINES / 2) + 1  # It gives the index of the line in the left.        end_index = start_index + self.V_NB_LINES - 1  # It gives the index of the line in the right.        xmin = self.get_line_x_from_index(start_index)        xmax = self.get_line_x_from_index(end_index)        for i in range(0, self.H_NB_LINES):            line_y = self.get_line_y_from_index(i)            # Transforming 2D coordinates            x1, y1 = self.transform(xmin, line_y)            x2, y2 = self.transform(xmax, line_y)            self.horizontal_lines[i].points = [x1, y1, x2, y2]    # 3. Principle: Perspective transformation    #    Check the documentation file for the transformation process.    # let's define a new function first.    # we need to call a transform function before we display the lines.    def update(self, dt):        # print("dt: " + str(dt*60))     # dt is the time difference with previous call of the        # update function        time_factor = dt * 60        self.update_vertical_lines()        self.update_horizontal_lines()        self.update_tiles()        self.update_yan()        if not self.state_game_over and self.state_game_has_started:  # if we are in game over, we stop going forward            # in the game.            speed_y = self.SPEED * self.height / 100  # to match the speed when the window size is small            self.current_offset_y += speed_y * time_factor            spacing_y = self.H_LINES_SPACING * self.height            #  this is sort of looping mechanism so the horizontal line level is displayed always            # We are going to stop moving loop effect if the game is over.            while self.current_offset_y >= spacing_y:  # when we reach the spacing between two lines                self.current_offset_y -= spacing_y  # We go back to initial position                # this is a loop index                self.current_y_loop += 1                self.score_txt = "SCORE: " + str(self.current_y_loop)  # to display the score                self.generate_tiles_coordinates()                print(" loop:" + str(self.current_y_loop))            # we are also stopping going left and right when game is over.            speed_x = self.current_speed_x * self.width / 100  # to match the speed when the widow size is small            self.current_offset_x += speed_x * time_factor  # To go left and right        # If collision game over is displayer and if not then game will be going on.        if not self.check_yan_collision() and not self.state_game_over:            self.state_game_over = True            self.menu_title = " G  A  M  E    O  V  E  R"            self.menu_button_title = " Restart "            self.menu_widget.opacity = 1            self.sound_music1.stop()            self.sound_gameover_impact.play()            Clock.schedule_once(self.play_game_over_voice_sound, 3)            print("GAME OVER")    def play_game_over_voice_sound(self, dt):        if self.state_game_over:            self.sound_gameover_voice.play()    def on_menu_button_pressed(self):        print("BUTTON")        if self.state_game_over:            self.sound_restart.play()        else:            self.sound_begin.play()        self.sound_music1.play()        self.reset_game()        self.state_game_has_started = True        self.menu_widget.opacity = 0class ChandraApp(App):    passChandraApp().run()