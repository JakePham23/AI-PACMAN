import sys
import pygame.freetype
import random
import Pacman
import Food
import Monster
import Map
from Specification import *
import BFS
import DFS
import UCS
import AStar



class MyApp:
    ################################################## CORE FUNCTIONS ##################################################
    def __init__(self):
        pygame.init()

        self.font = pygame.freetype.SysFont("Arial", 20)
        self.screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
        self.caption = pygame.display.set_caption(APP_CAPTION)

        self.current_map_index = 0
        self.current_level = 1
        self.score = 0
        self.cur_speed_index = 1
        self.speed_list = [("SPEED: 0.5", 0.5), ("SPEED: 1.0", 1), ("SPEED: 2.0", 2), ("SPEED: 5.0", 5), ("SPEED: 10.0", 10)]

        self.map = pygame.image.load(MAP_IMG[self.current_map_index])
        self.map = pygame.transform.scale(self.map, (MAP_WIDTH, MAP_HEIGHT))
        self.home_background = pygame.image.load(HOME_BACKGROUND)
        self.home_background = pygame.transform.scale(self.home_background, (HOME_BG_WIDTH, HOME_BG_HEIGHT))
        self.about_background = pygame.image.load(ABOUT_BACKGROUND)
        self.about_background = pygame.transform.scale(self.about_background, (APP_WIDTH, APP_HEIGHT))
        self.level_background = self.home_background
        self.gameover_background = pygame.image.load(GAMEOVER_BACKGROUND)
        self.gameover_background = pygame.transform.scale(self.gameover_background,
                                                          (GAMEOVER_BACKGROUND_WIDTH, GAMEOVER_BACKGROUND_HEIGHT))
        self.coin = pygame.image.load(COIN_IMAGE)
        self.coin = pygame.transform.scale(self.coin, (COIN_WIDTH, COIN_HEIGHT))
        self.victory_background = pygame.image.load(VICTORY_BACKGROUND)
        self.victory_background = pygame.transform.scale(self.victory_background, (VICTORY_WIDTH, VICTORY_HEIGHT))
        self.pacman1 = pygame.image.load(PACMAN1)
        self.pacman1 = pygame.transform.scale(self.pacman1, (PACMAN_WIDTH, PACMAN_HEIGHT))
        self.pacman2 = pygame.image.load(PACMAN2)
        self.pacman2 = pygame.transform.scale(self.pacman2, (PACMAN_WIDTH, PACMAN_HEIGHT))
        self.pacman3 = pygame.image.load(PACMAN3)
        self.pacman3 = pygame.transform.scale(self.pacman3, (PACMAN_WIDTH, PACMAN_HEIGHT))
        self.pacman4 = pygame.image.load(PACMAN4)
        self.pacman4 = pygame.transform.scale(self.pacman4, (PACMAN_WIDTH, PACMAN_HEIGHT))
        self.pacman5 = pygame.image.load(PACMAN5)
        self.pacman5 = pygame.transform.scale(self.pacman5, (PACMAN_WIDTH, PACMAN_HEIGHT))
        # self.pacman5 = pygame.image.load(PACMAN6)
        # self.pacman5 = pygame.transform.scale(self.pacman6, (PACMAN_WIDTH, PACMAN_HEIGHT))

        self.state = STATE_HOME
        self.clock = pygame.time.Clock()
        self.mouse = None

    def launch_pacman_game(self):
        """
        Launch the Pacman game with the corresponding level and map.
        """
        self.launch_game_draw()

        if self.current_level == 1:
            self.level_1()
        elif self.current_level == 2:
            self.level_2()
        elif self.current_level == 3:
            self.level_3()
        elif self.current_level == 4:
            self.level_4()
        elif self.current_level == 5:
            self.level_5()
        elif self.current_level == 6:
            self.level_6()

    def level_1(self):
        """
        Level 1: Pac-man keep position fixed. Blue gost using BFS algorithms to chase Pacman.
        """
        graph_map, pacman_pos, monster_pos = Map.read_map_level_1_monster(
            MAP_INPUT_TXT[self.current_level - 1][self.current_map_index])
        

        # path = GraphSearchAStar.search(graph_map, pacman_pos, monster_pos)
        path = BFS.bfs(graph_map, monster_pos, pacman_pos)


        pacman = Pacman.Pacman(self, pacman_pos)
        pacman.appear()

        monster = Monster.Monster(self, monster_pos, "blue")
        monster.appear()

        # food = Food.Food(self, monster_pos)
        # food.appear()

        if self.ready():
            if path is not None:
                back_home = False
                goal = path[-1]
                path = path[1:-1]

                for cell in path:
                    monster.move(cell)
                    self.update_score(SCORE_PENALTY)
                    pygame.time.delay(int(SPEED // self.speed_list[self.cur_speed_index][1]))

                    if self.launch_game_event():
                        back_home = True
                        break

                if not back_home:
                    monster.move(goal)
                    self.update_score(SCORE_PENALTY + SCORE_BONUS)
                    self.state = STATE_GAMEOVER
                    pygame.time.delay(2000)
            else:
                self.state = STATE_VICTORY
                pygame.time.delay(2000)
    def level_2(self):
        """
        Level 2: Pac-man keep position fixed. Pink ghost using DFS algorithms to chase Pacman.
        """
        # Đọc bản đồ và vị trí của Pacman và Monster
        graph_map, pacman_pos, monster_pos = Map.read_map_level_1_monster(
            MAP_INPUT_TXT[self.current_level - 1][self.current_map_index])

        # Sử dụng DFS để tìm đường đi của monster (thay vì UCS)
        path = DFS.dfs(graph_map, monster_pos, pacman_pos)

        pacman = Pacman.Pacman(self, pacman_pos)
        pacman.appear()

        # Tạo đối tượng monster màu hồng
        monster = Monster.Monster(self, monster_pos, "pink")
        monster.appear()

        # Thực hiện nếu Pacman sẵn sàng
        if self.ready():
            if path is not None:
                back_home = False
                goal = path[-1]
                path = path[1:-1]

                for cell in path:
                    monster.move(cell)
                    self.update_score(SCORE_PENALTY)
                    pygame.time.delay(int(SPEED // self.speed_list[self.cur_speed_index][1]))

                    if self.launch_game_event():
                        back_home = True
                        break

                if not back_home:
                    monster.move(goal)
                    self.update_score(SCORE_PENALTY + SCORE_BONUS)
                    self.state = STATE_GAMEOVER
                    pygame.time.delay(2000)
            else:
                self.state = STATE_VICTORY
                pygame.time.delay(2000)

    def level_3(self):
        """
        Level 3: Pac-man keep position fixed. Orange gost using UCS algorithms to chase Pacman.
        """
        graph_map, pacman_pos, monster_pos = Map.read_map_level_1_monster(
            MAP_INPUT_TXT[self.current_level - 1][self.current_map_index])
        
        # path = GraphSearchAStar.search(graph_map, pacman_pos, monster_pos)
        path = UCS.ucs(graph_map, monster_pos, pacman_pos)

        pacman = Pacman.Pacman(self, pacman_pos)
        pacman.appear()

        monster = Monster.Monster(self, monster_pos, "orange")
        monster.appear()

        # food = Food.Food(self, monster_pos)
        # food.appear()

        if self.ready():
            if path is not None:
                back_home = False
                goal = path[-1]
                path = path[1:-1]

                for cell in path:
                    monster.move(cell)
                    self.update_score(SCORE_PENALTY)
                    pygame.time.delay(int(SPEED // self.speed_list[self.cur_speed_index][1]))

                    if self.launch_game_event():
                        back_home = True
                        break

                if not back_home:
                    monster.move(goal)
                    self.update_score(SCORE_PENALTY + SCORE_BONUS)
                    self.state = STATE_GAMEOVER
                    pygame.time.delay(2000)
            else:
                self.state = STATE_VICTORY
                pygame.time.delay(2000)

    def level_4(self):
        """
        Level 4: Pac-man keep position fixed. Red ghost using A* algorithm to chase Pacman.
        """
        graph_map, pacman_pos, monster_pos = Map.read_map_level_1_monster(
            MAP_INPUT_TXT[self.current_level - 1][self.current_map_index])
        
        # Sử dụng thuật toán A*
        path = AStar.astar(graph_map, monster_pos, pacman_pos)

        pacman = Pacman.Pacman(self, pacman_pos)
        pacman.appear()

        monster = Monster.Monster(self, monster_pos, "red")
        monster.appear()

        if self.ready():
            if path is not None:
                back_home = False
                goal = path[-1]
                path = path[1:-1]

                for cell in path:
                    monster.move(cell)
                    self.update_score(SCORE_PENALTY)
                    pygame.time.delay(int(SPEED // self.speed_list[self.cur_speed_index][1]))

                    if self.launch_game_event():
                        back_home = True
                        break

                if not back_home:
                    monster.move(goal)
                    self.update_score(SCORE_PENALTY + SCORE_BONUS)
                    self.state = STATE_GAMEOVER
                    pygame.time.delay(2000)
            else:
                self.state = STATE_VICTORY
                pygame.time.delay(2000)


    def level_5(self):
        """
        Level 5: Pac-man keep position fixed. 4 ghosts using BFS, DFS, UCS, A* algorithms to chase Pacman.
        """
        graph_map, pacman_pos, monster_pos_blue, monster_pos_orange, monster_pos_pink, monster_pos_red = Map.read_map_level_5_monster(
            MAP_INPUT_TXT[self.current_level - 1][self.current_map_index])
        print("Current level:", self.current_level)
        print("Current map index:", self.current_map_index)
        print("Number of levels in MAP_INPUT_TXT:", len(MAP_INPUT_TXT))
        print("Number of maps in current level:", len(MAP_INPUT_TXT[self.current_level - 1]))
        # path = GraphSearchAStar.search(graph_map, pacman_pos, monster_pos)
        path_blue = BFS.bfs(graph_map, monster_pos_blue, pacman_pos)
        path_orange = UCS.ucs(graph_map, monster_pos_orange, pacman_pos)
        path_pink = DFS.dfs(graph_map, monster_pos_pink, pacman_pos)
        path_red = AStar.astar(graph_map, monster_pos_red, pacman_pos)
        
        pacman = Pacman.Pacman(self, pacman_pos)
        pacman.appear()

        blue_monster = Monster.Monster(self, monster_pos_blue, "blue")
        blue_monster.appear()

        orange_monster = Monster.Monster(self, monster_pos_orange, "orange")
        orange_monster.appear()

        pink_monster = Monster.Monster(self, monster_pos_pink, "pink")
        pink_monster.appear()

        red_monster = Monster.Monster(self, monster_pos_red, "red")
        red_monster.appear()

        # food = Food.Food(self, monster_pos)
        # food.appear()

        if self.ready():
            if path_blue and path_orange and path_pink and path_red:
                min_path = min(len(path_blue), len(path_orange), len(path_pink), len(path_red))
                goal = path_red[-1]
                back_home = False
                for i in range(min_path):

                    blue_monster.move(path_blue[i])
                    orange_monster.move(path_orange[i])
                    pink_monster.move(path_pink[i])
                    red_monster.move(path_red[i])

                    self.update_score(SCORE_PENALTY)
                    pygame.time.delay(int(SPEED // self.speed_list[self.cur_speed_index][1]))

                    if self.launch_game_event():
                        back_home = True
                        break

                if not back_home:
                    if len(path_blue) == min_path:
                        blue_monster.move(goal)
                    elif len(path_orange) == min_path:
                        orange_monster.move(goal)
                    elif len(path_pink) == min_path:
                        pink_monster.move(goal)
                    elif len(path_red) == min_path:
                        red_monster.move(goal)

                    self.update_score(SCORE_PENALTY + SCORE_BONUS)
                    self.state = STATE_GAMEOVER
                    pygame.time.delay(2000)
            else:
                self.state = STATE_VICTORY
                pygame.time.delay(2000)
    def level_6(self):
      
        graph_map, pacman_pos, monster_pos_blue, monster_pos_orange, monster_pos_pink, monster_pos_red = \
            Map.read_map_level_5_monster(MAP_INPUT_TXT[self.current_level - 2][self.current_map_index])
      
        
        # Tạo và hiển thị Pac-Man
        pacman = Pacman.Pacman(self, pacman_pos)
        pacman.appear()
        
        # Tạo và hiển thị 4 ghost theo vị trí và màu sắc xác định
        blue_monster = Monster.Monster(self, monster_pos_blue, "blue")
        blue_monster.appear()
        
        orange_monster = Monster.Monster(self, monster_pos_orange, "orange")
        orange_monster.appear()
        
        pink_monster = Monster.Monster(self, monster_pos_pink, "pink")
        pink_monster.appear()
        
        red_monster = Monster.Monster(self, monster_pos_red, "red")
        red_monster.appear()
        
        # Thiết lập một số biến để kiểm soát tốc độ và cache DFS của ghost Pink
        clock = pygame.time.Clock()
        game_over = False
        
        if self.ready():
            while not game_over:
                clock.tick(5) 
                
                # Xử lý sự kiện, bao gồm điều khiển Pac-Man
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            pacman.try_move('up', graph_map)
                        elif event.key == pygame.K_DOWN:
                            pacman.try_move('down', graph_map)
                        elif event.key == pygame.K_LEFT:
                            pacman.try_move('left', graph_map)
                        elif event.key == pygame.K_RIGHT:
                            pacman.try_move('right', graph_map)
                
                # --- Ghost Blue dùng BFS ---
                path_blue = BFS.bfs(graph_map, tuple(blue_monster.grid_pos), tuple(pacman.grid_pos))
                if path_blue is not None and len(path_blue) > 1:
                    blue_monster.move(path_blue[1])
                
                    
                # --- Ghost Pink dùng DFS ---
                path_pink = DFS.dfs(graph_map, tuple(pink_monster.grid_pos), tuple(pacman.grid_pos))
                if path_pink is not None and len(path_pink) > 1:
                    next_step = path_pink[1]
                    # Kiểm tra nếu bước kế tiếp trùng với vị trí ghost vừa rời (oscillation)
                    if hasattr(pink_monster, "last_position") and next_step == pink_monster.last_position:
                        # Nếu có các lựa chọn khác ở các ô kề, hãy chọn ô nào có khoảng cách Manhattan nhỏ hơn đến Pac-Man.
                        current = tuple(pink_monster.grid_pos)
                        candidates = graph_map.get(current, [])
                        pac_x, pac_y = tuple(pacman.grid_pos)
                        best = None
                        best_dist = float("inf")
                        for cand in candidates:
                            if cand == pink_monster.last_position:
                                continue
                            # Tính khoảng cách Manhattan
                            dist = abs(cand[0] - pac_x) + abs(cand[1] - pac_y)
                            if dist < best_dist:
                                best = cand
                                best_dist = dist
                        if best is not None:
                            next_step = best
                    else:
                        # Nếu không có thuộc tính last_position, gán nó lần đầu
                        pink_monster.last_position = None
                    pink_monster.last_position = tuple(pink_monster.grid_pos)
                    pink_monster.move(next_step)
                
                # --- Ghost Orange dùng UCS ---
                path_orange = UCS.ucs(graph_map, tuple(orange_monster.grid_pos), tuple(pacman.grid_pos))
                if path_orange is not None and len(path_orange) > 1:
                    orange_monster.move(path_orange[1])
                
                # --- Ghost Red dùng A* ---
                path_red = AStar.astar(graph_map, tuple(red_monster.grid_pos), tuple(pacman.grid_pos))
                if path_red is not None and len(path_red) > 1:
                    red_monster.move(path_red[1])
                
                # Kiểm tra va chạm giữa ghost và Pac-Man
                for ghost in [blue_monster, pink_monster, orange_monster, red_monster]:
                    if tuple(ghost.grid_pos) == tuple(pacman.grid_pos):
                        print("DEBUG: Pac-Man bị bắt!")
                        self.state = STATE_GAMEOVER

                        # Hiển thị thông báo GAME OVER trên màn hình
                        font = pygame.font.SysFont("Arial", 36)
                        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
                        self.screen.blit(game_over_text, ((APP_WIDTH - game_over_text.get_width()) // 2,
                                                        (APP_HEIGHT - game_over_text.get_height()) // 2))
                        pygame.display.update()
                        pygame.time.delay(2000)
                        game_over = True
                        break
                
                self.update_score(SCORE_PENALTY)
                pygame.display.update()
                pygame.time.delay(int(SPEED // self.speed_list[self.cur_speed_index][1]))



    def run(self):
        """
        Run this program.
        """
        while True:
            if self.state == STATE_HOME:
                self.home_draw()
                self.home_event()
            elif self.state == STATE_PLAYING:
                self.play_draw()
                self.launch_pacman_game()
                self.play_event()
            elif self.state == STATE_ABOUT:
                self.about_draw()
                self.about_event()
            elif self.state == STATE_LEVEL:
                self.level_draw()
                self.level_event()
            elif self.state == STATE_SETTING:
                self.setting_draw()
                self.setting_event()
            elif self.state == STATE_GAMEOVER:
                self.gameover_draw1()
                self.gameover_draw2()
                self.gameover_event()
            elif self.state == STATE_VICTORY:
                self.victory_draw1()
                self.victory_draw2()
                self.victory_draw3()
                self.victory_draw4()
                self.victory_draw5()
            self.clock.tick(FPS)

    ####################################################################################################################

    def launch_game_draw(self):
        """
        Draw the initial Play Screen.
        """
        pygame.display.update()
        self.score = 0
        self.cur_speed_index = 1
        self.update_score(0)

        text_surf, text_rect = self.font.render("HOME", WHITE)
        self.screen.blit(text_surf, HOME_RECT)
        pygame.display.update(HOME_RECT)

        text_surf, text_rect = self.font.render(self.speed_list[self.cur_speed_index][0], WHITE)
        self.screen.blit(text_surf, SPEED_RECT)
        pygame.display.update(SPEED_RECT)

    def launch_game_event(self):
        """
        Get events while the Pacman is moving.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if HOME_RECT[0] <= self.mouse[0] <= HOME_RECT[0] + HOME_RECT[2] and \
                        HOME_RECT[1] <= self.mouse[1] <= HOME_RECT[1] + HOME_RECT[3]:
                    self.state = STATE_HOME
                    break
                if SPEED_RECT[0] <= self.mouse[0] <= SPEED_RECT[0] + SPEED_RECT[2] and \
                        SPEED_RECT[1] <= self.mouse[1] <= SPEED_RECT[1] + SPEED_RECT[3]:
                    self.cur_speed_index += 1
                    self.cur_speed_index %= len(self.speed_list)
                    break

        self.mouse = pygame.mouse.get_pos()
        if HOME_RECT[0] <= self.mouse[0] <= HOME_RECT[0] + HOME_RECT[2] and \
                HOME_RECT[1] <= self.mouse[1] <= HOME_RECT[1] + HOME_RECT[3]:
            text_surf, text_rect = self.font.render("HOME", TOMATO)
            self.screen.blit(text_surf, HOME_RECT)
            pygame.display.update(HOME_RECT)
        else:
            text_surf, text_rect = self.font.render("HOME", WHITE)
            self.screen.blit(text_surf, HOME_RECT)
            pygame.display.update(HOME_RECT)
        if SPEED_RECT[0] <= self.mouse[0] <= SPEED_RECT[0] + SPEED_RECT[2] and \
                SPEED_RECT[1] <= self.mouse[1] <= SPEED_RECT[1] + SPEED_RECT[3]:
            pygame.draw.rect(self.screen, BLACK, SPEED_RECT)
            text_surf, text_rect = self.font.render(self.speed_list[self.cur_speed_index][0], TOMATO)
            self.screen.blit(text_surf, SPEED_RECT)
            pygame.display.update(SPEED_RECT)
        else:
            pygame.draw.rect(self.screen, BLACK, SPEED_RECT)
            text_surf, text_rect = self.font.render(self.speed_list[self.cur_speed_index][0], WHITE)
            self.screen.blit(text_surf, SPEED_RECT)
            pygame.display.update(SPEED_RECT)

        if self.state == STATE_HOME:
            return True

        return False

    def ready(self):
        """
        Ready effect (3, 2, 1, GO).
        """
        text_list = ['3', '3', '3', '3', '2', '2', '2', '2', '1', '1', '1', '1', 'GO', 'GO', 'GO', 'GO']
        for text in text_list:
            text_surf, text_rect = self.font.render(text, WHITE)

            text_pos = (READY_POS[0] - len(text) * 5, READY_POS[1])
            text_rect[0] = text_pos[0]
            text_rect[1] = text_pos[1]

            self.screen.blit(text_surf, text_pos)
            pygame.display.update(text_rect)

            pygame.time.delay(250)
            pygame.display.update(pygame.draw.rect(self.screen, BLACK, text_rect))

            if self.launch_game_event():
                return False

        return True

    def victory_draw1(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.victory_background, (50, 0))
        self.screen.blit(self.pacman1, (50, 350))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 255 <= self.mouse[0] <= 355 and 620 <= self.mouse[1] <= 670:
                    self.state = STATE_HOME
        self.mouse = pygame.mouse.get_pos()
        if 255 <= self.mouse[0] <= 355 and 620 <= self.mouse[1] <= 670:
            self.draw_button(self.screen, OK_POS, DARK_GREY, RED, "OK")
        else:
            self.draw_button(self.screen, OK_POS, LIGHT_GREY, BLACK, "OK")
        pygame.time.delay(100)
        pygame.display.update()

    def victory_draw2(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.victory_background, (50, 0))
        self.screen.blit(self.pacman2, (125, 350))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 255 <= self.mouse[0] <= 355 and 620 <= self.mouse[1] <= 670:
                    self.state = STATE_HOME
        self.mouse = pygame.mouse.get_pos()
        if 255 <= self.mouse[0] <= 355 and 620 <= self.mouse[1] <= 670:
            self.draw_button(self.screen, OK_POS, DARK_GREY, RED, "OK")
        else:
            self.draw_button(self.screen, OK_POS, LIGHT_GREY, BLACK, "OK")
        pygame.time.delay(100)
        pygame.display.update()

    def victory_draw3(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.pacman3, (200, 350))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 255 <= self.mouse[0] <= 355 and 620 <= self.mouse[1] <= 670:
                    self.state = STATE_HOME
        self.mouse = pygame.mouse.get_pos()
        if 255 <= self.mouse[0] <= 355 and 620 <= self.mouse[1] <= 670:
            self.draw_button(self.screen, OK_POS, DARK_GREY, RED, "OK")
        else:
            self.draw_button(self.screen, OK_POS, LIGHT_GREY, BLACK, "OK")
        pygame.time.delay(100)
        pygame.display.update()

    def victory_draw4(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.victory_background, (50, 0))
        self.screen.blit(self.pacman4, (275, 350))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 255 <= self.mouse[0] <= 355 and 620 <= self.mouse[1] <= 670:
                    self.state = STATE_HOME
        self.mouse = pygame.mouse.get_pos()
        if 255 <= self.mouse[0] <= 355 and 620 <= self.mouse[1] <= 670:
            self.draw_button(self.screen, OK_POS, DARK_GREY, RED, "OK")
        else:
            self.draw_button(self.screen, OK_POS, LIGHT_GREY, BLACK, "OK")
        pygame.time.delay(100)
        pygame.display.update()

    def victory_draw5(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.victory_background, (50, 0))
        self.screen.blit(self.pacman5, (350, 350))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 255 <= self.mouse[0] <= 355 and 620 <= self.mouse[1] <= 670:
                    self.state = STATE_HOME
        self.mouse = pygame.mouse.get_pos()
        if 255 <= self.mouse[0] <= 355 and 620 <= self.mouse[1] <= 670:
            self.draw_button(self.screen, OK_POS, DARK_GREY, RED, "OK")
        else:
            self.draw_button(self.screen, OK_POS, LIGHT_GREY, BLACK, "OK")
        pygame.time.delay(100)
        pygame.display.update()

    def gameover_draw1(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.gameover_background, (0, 0))
        self.screen.blit(self.coin, COIN_POS)
        pygame.time.delay(350)
        pygame.display.update()

    def gameover_draw2(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.gameover_background, (0, 0))
        pygame.time.delay(350)

    def gameover_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 200 <= self.mouse[0] <= 400 and 430 <= self.mouse[1] <= 630:
                    self.state = STATE_HOME
        self.mouse = pygame.mouse.get_pos()

        pygame.display.update()

    def update_score(self, achived_score):
        """
        Add 'achived_score' to the current score and display onto the screen.
        """
        text_surf, text_rect = self.font.render("SCORES: " + str(self.score), WHITE)
        text_rect[0] = SCORE_POS[0]
        text_rect[1] = SCORE_POS[1]
        pygame.draw.rect(self.screen, BLACK, text_rect)
        pygame.display.update(text_rect)

        self.score += achived_score

        text_surf, text_rect = self.font.render("SCORES: " + str(self.score), WHITE)
        text_rect[0] = SCORE_POS[0]
        text_rect[1] = SCORE_POS[1]
        pygame.draw.rect(self.screen, BLACK, text_rect)

        self.screen.blit(text_surf, SCORE_POS)
        pygame.display.update(text_rect)

    def draw_grids(self):
        """
        Draw the grid onto the map for better designing.
        """
        for x in range(int(MAP_WIDTH / CELL_SIZE) + 1):
            self.screen.blit(self.font.render(str(x % 10), WHITE)[0],
                             (x * CELL_SIZE + MAP_POS_X + CELL_SIZE // 4, MAP_POS_Y - CELL_SIZE))

            pygame.draw.line(self.screen, (107, 107, 107),
                             (x * CELL_SIZE + MAP_POS_X, MAP_POS_Y),
                             (x * CELL_SIZE + MAP_POS_X, MAP_HEIGHT + MAP_POS_Y))

        for y in range(int(MAP_HEIGHT / CELL_SIZE) + 1):
            self.screen.blit(self.font.render(str(y % 10), WHITE)[0],
                             (MAP_POS_X - CELL_SIZE, y * CELL_SIZE + MAP_POS_Y))

            pygame.draw.line(self.screen, (107, 107, 107),
                             (MAP_POS_X, y * CELL_SIZE + MAP_POS_Y),
                             (MAP_WIDTH + MAP_POS_X, y * CELL_SIZE + MAP_POS_Y))

    # def draw_button(self, surf, rect, button_color, text_color, text):
    #     pygame.draw.rect(surf, button_color, rect)
    #     text_surf, text_rect = self.font.render(text, text_color)
    #     text_rect.center = rect.center
    #     self.screen.blit(text_surf, text_rect)

    def draw_button(self, surf, rect, button_color, text_color, text):
        rect = pygame.Rect(rect)  # ← Chuyển tuple thành pygame.Rect
        pygame.draw.rect(surf, button_color, rect)
        text_surf, text_rect = self.font.render(text, text_color)
        text_rect.center = rect.center  # Giờ thì .center sẽ hợp lệ
        self.screen.blit(text_surf, text_rect)


    @staticmethod
    def draw_triangle_button(surf, rect, button_color):
        pygame.draw.polygon(surf, button_color, rect)

    def home_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.home_background, (0, 0))

    def play_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.map, (MAP_POS_X, MAP_POS_Y))

    def about_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.about_background, (0, 0))
        text_surf, text_rect = self.font.render("PROGRAMMERS", TOMATO)
        self.screen.blit(text_surf, (240, 100))
        text_surf, text_rect = self.font.render("22120230 - Pham Tan Nghia", TOMATO)
        self.screen.blit(text_surf, (150, 150))
        text_surf, text_rect = self.font.render("22120xxx - Nguyen Van A", TOMATO)
        self.screen.blit(text_surf, (150, 200))
        text_surf, text_rect = self.font.render("22120xxx - Nguyen Van B", TOMATO)
        self.screen.blit(text_surf, (150, 250))
        text_surf, text_rect = self.font.render("22120xxx - Nguyen Van C", TOMATO)
        self.screen.blit(text_surf, (150, 300))

    def level_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.level_background, (0, 0))

    def setting_draw(self):
        self.screen.fill(BLACK)

    def setting_event(self):
        self.map = pygame.transform.scale(self.map, (MAP_WIDTH, MAP_HEIGHT))
        self.screen.blit(self.map, (ROW_PADDING // 2, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 255 <= self.mouse[0] <= 355 and 620 <= self.mouse[1] <= 670:
                    self.state = STATE_HOME
                elif 360 <= self.mouse[0] <= 403.3 and 620 <= self.mouse[1] <= 670:
                    self.current_map_index += 1
                    self.current_map_index %= MAP_NUM
                elif 206.7 <= self.mouse[0] <= 250 and 620 <= self.mouse[1] <= 670:
                    self.current_map_index += MAP_NUM - 1
                    self.current_map_index %= MAP_NUM
                self.map = pygame.image.load(MAP_IMG[self.current_map_index])

        self.mouse = pygame.mouse.get_pos()
        if 255 <= self.mouse[0] <= 355 and 620 <= self.mouse[1] <= 670:
            self.draw_button(self.screen, OK_POS, DARK_GREY, RED, "OK")
        else:
            self.draw_button(self.screen, OK_POS, LIGHT_GREY, BLACK, "OK")
        if 360 <= self.mouse[0] <= 403.3 and 620 <= self.mouse[1] <= 670:
            self.draw_triangle_button(self.screen, TRIANGLE_1_POS, DARK_GREY)
        else:
            self.draw_triangle_button(self.screen, TRIANGLE_1_POS, LIGHT_GREY)
        if 206.7 <= self.mouse[0] <= 250 and 620 <= self.mouse[1] <= 670:
            self.draw_triangle_button(self.screen, TRIANGLE_2_POS, DARK_GREY)
        else:
            self.draw_triangle_button(self.screen, TRIANGLE_2_POS, LIGHT_GREY)
        pygame.display.update()

    @staticmethod
    def play_event():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

    def about_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 225 <= self.mouse[0] <= 375 and 530 <= self.mouse[1] <= 580:
                    self.state = STATE_HOME

        self.mouse = pygame.mouse.get_pos()
        if 225 <= self.mouse[0] <= 375 and 530 <= self.mouse[1] <= 580:
            self.draw_button(self.screen, BACK_POS, DARK_GREY, RED, "Back")
        else:
            self.draw_button(self.screen, BACK_POS, LIGHT_GREY, BLACK, "Back")
        pygame.display.update()

    def level_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 150 <= self.mouse[0] <= 450 and 280 <= self.mouse[1] <= 320:
                    self.state = STATE_PLAYING
                    self.current_level = 1
                elif 150 <= self.mouse[0] <= 450 and 340 <= self.mouse[1] <= 380:
                    self.state = STATE_PLAYING
                    self.current_level = 2
                elif 150 <= self.mouse[0] <= 450 and 400 <= self.mouse[1] <= 440:
                    self.state = STATE_PLAYING
                    self.current_level = 3
                elif 150 <= self.mouse[0] <= 450 and 460 <= self.mouse[1] <= 500:
                    self.state = STATE_PLAYING
                    self.current_level = 4
                elif 150 <= self.mouse[0] <= 450 and 520 <= self.mouse[1] <= 560:
                    self.state = STATE_PLAYING
                    self.current_level = 5
                elif 150 <= self.mouse[0] <= 450 and 580 <= self.mouse[1] <= 620:
                    self.state = STATE_PLAYING
                    self.current_level = 6
                elif 500 <= self.mouse[0] <= 570 and 580 <= self.mouse[1] <= 620:
                    self.state = STATE_HOME
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.mouse = pygame.mouse.get_pos()

        if 150 <= self.mouse[0] <= 450 and 280 <= self.mouse[1] <= 320:
            self.draw_button(self.screen, LEVEL_1_POS, DARK_GREY, RED, "Level 1")
        else:
            self.draw_button(self.screen, LEVEL_1_POS, LIGHT_GREY, BLACK, "Level 1")

        if 150 <= self.mouse[0] <= 450 and 340 <= self.mouse[1] <= 380:
            self.draw_button(self.screen, LEVEL_2_POS, DARK_GREY, RED, "Level 2")
        else:
            self.draw_button(self.screen, LEVEL_2_POS, LIGHT_GREY, BLACK, "Level 2")

        if 150 <= self.mouse[0] <= 450 and 400 <= self.mouse[1] <= 440:
            self.draw_button(self.screen, LEVEL_3_POS, DARK_GREY, RED, "Level 3")
        else:
            self.draw_button(self.screen, LEVEL_3_POS, LIGHT_GREY, BLACK, "Level 3")

        if 150 <= self.mouse[0] <= 450 and 460 <= self.mouse[1] <= 500:
            self.draw_button(self.screen, LEVEL_4_POS, DARK_GREY, RED, "Level 4")
        else:
            self.draw_button(self.screen, LEVEL_4_POS, LIGHT_GREY, BLACK, "Level 4")

        if 150 <= self.mouse[0] <= 450 and 520 <= self.mouse[1] <= 560:
            self.draw_button(self.screen, LEVEL_5_POS, DARK_GREY, RED, "Level 5")
        else:
            self.draw_button(self.screen, LEVEL_5_POS, LIGHT_GREY, BLACK, "Level 5")

        if 150 <= self.mouse[0] <= 450 and 580 <= self.mouse[1] <= 620:
            self.draw_button(self.screen, LEVEL_6_POS, DARK_GREY, RED, "Level 6")
        else:
            self.draw_button(self.screen, LEVEL_6_POS, LIGHT_GREY, BLACK, "Level 6")

        if 500 <= self.mouse[0] <= 570 and 580 <= self.mouse[1] <= 620:
            self.draw_button(self.screen, BACK_LEVEL_POS, DARK_GREY, RED, "Back")
        else:
            self.draw_button(self.screen, BACK_LEVEL_POS, LIGHT_GREY, BLACK, "Back")

        pygame.display.update()


    def home_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 150 <= self.mouse[0] <= 450 and 320 <= self.mouse[1] <= 395:
                    self.state = STATE_LEVEL
                elif 150 <= self.mouse[0] <= 450 and 400 <= self.mouse[1] <= 450:
                    self.state = STATE_SETTING
                elif 150 <= self.mouse[0] <= 450 and 480 <= self.mouse[1] <= 530:
                    self.state = STATE_ABOUT
                elif 150 <= self.mouse[0] <= 450 and 560 <= self.mouse[1] <= 610:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.mouse = pygame.mouse.get_pos()
        if 150 <= self.mouse[0] <= 450 and 320 <= self.mouse[1] <= 375:
            self.draw_button(self.screen, START_POS, DARK_GREY, RED, "Start")
        else:
            self.draw_button(self.screen, START_POS, LIGHT_GREY, BLACK, "Start")
        if 150 <= self.mouse[0] <= 450 and 400 <= self.mouse[1] <= 450:
            self.draw_button(self.screen, SETTING_POS, DARK_GREY, RED, "Setting")
        else:
            self.draw_button(self.screen, SETTING_POS, LIGHT_GREY, BLACK, "Setting")
        if 150 <= self.mouse[0] <= 450 and 480 <= self.mouse[1] <= 530:
            self.draw_button(self.screen, ABOUT_POS, DARK_GREY, RED, "About")
        else:
            self.draw_button(self.screen, ABOUT_POS, LIGHT_GREY, BLACK, "About")
        if 150 <= self.mouse[0] <= 450 and 560 <= self.mouse[1] <= 610:
            self.draw_button(self.screen, EXIT_POS, DARK_GREY, RED, "Exit")
        else:
            self.draw_button(self.screen, EXIT_POS, LIGHT_GREY, BLACK, "Exit")
        pygame.display.update()
