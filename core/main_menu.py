
# use this one to capture someone pressing esc
# terminal_menu = TerminalMenu()
# if not terminal_menu.chosen_accept_key:
#   exit()

import os
import time
import readline
from core.stash import *
from random import choice
from string import ascii_letters
from simple_term_menu import TerminalMenu

from os import popen, system
from colorama import Fore, Back, Style

class MainMenu :
    def __init__(self, stash):
        self.stash = stash

        # general styling
        self.h_style = ('bg_green', 'fg_black', 'italics')
        self.h_kill_style = ('bg_red', 'italics')
        self.cursor = '       > '
        self.cursor_kill = '       X '
        self.cursor_style = ('fg_green', 'bold')
        self.cursor_style_kill = ('fg_red', 'bold')

        self.index = 0
        self.menu_entry = ['Listeners', 'Agents', 'Overview', 'Quit']

        self.CMD = ['shell', 'powershell', 'sleep', 'rename', 'back_to_previous_menu']

    def completer(self, text, state):
        options = [cmd for cmd in self.CMD if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        else :
            return None

    def on_activate_r(self):
        self.index = (self.index + 1) % (len(self.menu_entry))
        self.print_menu()
    def on_activate_l(self):
        self.index = (self.index - 1) % (len(self.menu_entry))
        self.print_menu()

    def print_menu(self):
        system('clear')
        rows, columns = popen('/usr/bin/stty size', 'r').read().split()
        # print(f'Rows {rows}')
        # print(f'Columns {columns}')

        slot = int(columns) / len(self.menu_entry)
        # rem = int(columns) % len(self.menu_entry)

        # print(len(self.menu_entry))
        # print(f'{slot}')
        print('''
 
  ██▓███   ▄▄▄       ██▓     ██▓ ███▄    █  ██ ▄█▀▄▄▄          ▄████▄   ░██████ 
 ▓██░  ██▒▒████▄    ▓██▒    ▓██▒ ██ ▀█   █  ██▄█▒▒████▄       ▒██▀ ▀█    ░   ██▒ 
 ▓██░ ██▓▒▒██  ▀█▄  ▒██░    ▒██▒▓██  ▀█ ██▒▓███▄░▒██  ▀█▄     ▒▓█    ▄    ▄██▓▒   
 ▒██▄█▓▒ ▒░██▄▄▄▄██ ▒██░    ░██░▓██▒  ▐▌██▒▓██ █▄░██▄▄▄▄██    ▒▓▓▄ ▄██▒ ▄█▓▒░
 ▒██▒ ░  ░ ▓█   ▓██▒░██████▒░██░▒██░   ▓██░▒██▒ █▄▓█   ▓██▒   ▒ ▓███▀ ░ ██████▒▒
 ▒██░ ░  ░ ▒▒   ▓▒█░░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒ ▒ ▒▒ ▓▒▒▒   ▓▒█░   ░ ░▒ ▒  ░ ▒ ▒▓▒ ▒ ░
 ░▓▒░       ▒   ▒▒ ░░ ░ ▒  ░ ▒ ░░ ░░   ░ ▒░░ ░▒ ▒░ ▒   ▒▒ ░     ░  ▒    ░ ░▒  ░ ░
 ░▒         ░   ▒     ░ ░    ▒ ░   ░   ░ ░ ░ ░░ ░  ░   ▒      ░         ░  ░  ░  
  ░             ░  ░    ░  ░ ░           ░ ░  ░        ░  ░   ░ ░            ░  
                                                              ░                 
                                       
    ''')

        high = f'{Fore.WHITE}{Style.BRIGHT}{Back.GREEN}'
        low = f'{Fore.GREEN}{Back.WHITE}'
        menu_entry = [f'{" "*(int(slot/2)-3)}{e}{" "*(int(slot/2)-3)}' for e in self.menu_entry]
        menu_entry = [f'{high}{e}{Style.RESET_ALL}' if menu_entry[self.index] == e else f'{low}{e}{Style.RESET_ALL}' for e in menu_entry]
        print(f'{Fore.WHITE}{Style.BRIGHT}{Back.BLACK}|{Style.RESET_ALL}'.join(menu_entry))

        menu_to_show =  self.menu_entry[self.index]
        if menu_to_show == 'Listeners':
            self.listener_menu()
        elif menu_to_show == 'Agents':
            self.agents_menu()
        elif menu_to_show == 'Overview':
            print('Overview Menu HERE!!')
            self.listener_menu()
        elif menu_to_show == 'Quit':
            self.quit_menu()
        # self.sub_init()

    def menu_init(self):
        self.print_menu()

    ### sub menus

    def quit_menu(self):
        ### Listeners main menu
        qm_title = '\n\n       Are you sure???\n'
        qm_items = ['No!', 'No!', 'No!', 'Yes', 'No!', 'No!', 'No!']
        qm_back = False
        qm = TerminalMenu(
            menu_entries=qm_items,
            title=qm_title,
            menu_cursor=self.cursor_kill,
            menu_cursor_style=self.cursor_style_kill,
            menu_highlight_style=self.h_kill_style,
            cycle_cursor=True,
            clear_screen=False,
            accept_keys=('enter', 'ctrl-e', 'ctrl-w')
        )

        while not qm_back:
            qm_sel = qm.show()

            if qm.chosen_accept_key == 'ctrl-w':
                self.on_activate_l()
                qm_back = True
            elif qm.chosen_accept_key == 'ctrl-e':
                qm_back = True
                self.on_activate_r()
            else:
                if qm_sel == 3:
                    system('clear')
                    qm_back = True

    def agent_list_gen(self):
        ### Agents List
        agents = self.stash.get_agents()
        if agents:
            agent_list = [f'{a[0]} @ {a[1]}' for a in agents]
            agent_list.append('Back')
        else:
            agent_list = ['NO ACTIVE AGENTS, you n00b', 'Back']
        return agent_list

    def agents_menu(self):
        ### Agents main menu
        amm_title = '\n\n       Agents Menu\n'
        # amm_items = ['Show Agents', 'Kill Agent', 'Back']
        amm_items = ['Show Agents', 'Kill Agent']
        amm_back = False
        amm = TerminalMenu(
            menu_entries=amm_items,
            title=amm_title,
            menu_cursor=self.cursor,
            menu_cursor_style=self.cursor_style,
            menu_highlight_style=self.h_style,
            cycle_cursor=True,
            clear_screen=False,
            accept_keys=('enter', 'ctrl-e', 'ctrl-w')
        )

        am_list_title = '\n\n       Select Aget to Interact\n'
        am_list_items = self.agent_list_gen()
        am_list_back = False
        am_list_menu = TerminalMenu(
            menu_entries=am_list_items,
            title=am_list_title,
            menu_cursor=self.cursor,
            menu_cursor_style=self.cursor_style,
            menu_highlight_style=self.h_style,
            cycle_cursor=True,
            clear_screen=False,
            accept_keys=('enter', 'ctrl-e', 'ctrl-w'),
            preview_command=self.short_com_hist,
            preview_size=0.85,
            preview_title=f'{Style.BRIGHT}Short Commands History{Style.RESET_ALL}'
        )

        ### Listener Kill Menu
        ### use same items fo prev menu
        am_kill_title = '\n\n       Agents Killer\n'
        am_kill_back = False
        am_kill_menu = TerminalMenu(
            menu_entries=am_list_items,
            title=am_kill_title,
            menu_cursor=self.cursor_kill,
            menu_cursor_style=self.cursor_style_kill,
            menu_highlight_style=self.h_kill_style,
            cycle_cursor=True,
            clear_screen=False,
            accept_keys=('enter', 'ctrl-e', 'ctrl-w')
        )

        # amm_sel = amm.show()

        # agents menu loop [0-2] ['Show agents', 'Kill Agents', 'Back']
        while not amm_back:
            amm_sel = amm.show()

            if amm.chosen_accept_key == 'ctrl-w':
                amm_back = True
                self.on_activate_l()
            elif amm.chosen_accept_key == 'ctrl-e':
                amm_back = True
                self.on_activate_r()
            else:

                
                if amm_sel == 0:
                    ## agents list menu
                    # find a way to regenerate agent list
                    # am_list_menu.menu_entries = self.agent_list_gen()
                    while not am_list_back:
                        am_list_sel = am_list_menu.show()

                        if am_list_menu.chosen_accept_key == 'ctrl-w':
                            am_list_back = True
                            amm_back = True
                            self.on_activate_l()
                        elif am_list_menu.chosen_accept_key == 'ctrl-e':
                            am_list_back = True
                            amm_back = True
                            self.on_activate_r()
                        else:
                            if am_list_items[am_list_sel] not in ['Back', 'NO ACTIVE AGENTS, you n00b']:
                                task_input = self.get_task_input(am_list_items[am_list_sel].split()[0])
                                
                            am_list_back = True
                            amm_back = True
                            self.print_menu()
                    
                    am_list_back = False
                
                elif amm_sel == 1:
                    ## kill listener menu
                    while not am_kill_back:
                        am_kill_sel = am_kill_menu.show()

                        if am_kill_menu.chosen_accept_key == 'ctrl-w':
                            am_kill_back = True
                            amm_back = True
                            self.on_activate_l()
                        elif am_kill_menu.chosen_accept_key == 'ctrl-e':
                            am_kill_back = True
                            amm_back = True
                            self.on_activate_r()
                        else:
                            if am_list_items[am_kill_sel] not in ['Back', 'NO ACTIVE AGENTS, you n00b']:
                                agent = am_list_items[am_kill_sel].split()[0]
                                command_code = self.gen_command_code()
                                cmd = 'quit'
                                self.stash.set_agent_job(command_code, agent, cmd)
                                self.stash.sql_stash( 'UPDATE agents SET alive = ? WHERE agent_name = ? ;', (False, agent) )

                            am_kill_back = True
                            amm_back = True
                            self.print_menu()

                    am_kill_back = False

    def get_task_input(self, agent):
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.completer)
        header = f'\n\n       Set Task to {agent}. Tab is your friend.'
        cmd = ''
        while cmd == '' or cmd.split()[0] not in self.CMD:
            cmd = input(f'{header}\n{Fore.GREEN}{Style.BRIGHT}{self.cursor}{Style.RESET_ALL}')
        command_code = self.gen_command_code()
        self.stash.set_agent_job(command_code, agent, cmd)

    def gen_command_code(self):
        command_code = ''.join(choice(ascii_letters) for i in range(10))
        comms = self.stash.get_command_codes()
        if comms:
            comms_list = [c[0] for c in comms]
        else:
            comms_list = []
        while command_code in comms_list:
            command_code = ''.join(choice(ascii_letters) for i in range(10))
        return command_code

    def short_com_hist(self, agent):
        high_comm = f'{Fore.GREEN}{Style.BRIGHT} Task > {Fore.WHITE}'
        high_resp = f'{Fore.CYAN} Result > '
        comms = self.stash.get_agents_comm_list(agent.split()[0])
        ret = '\n'
        for c in comms:
            cra = c[1].replace('\r','').split('\n')
            cr = cra[0]
            if len(cra) > 1:
                # cr = ''.join([f'{" "*11}{Fore.CYAN}{cc}\n' for cc in cra])
                for i in range(1,len(cra)):
                    cr += f'{" "*10}{Fore.CYAN}{cra[i]}\n'
            ret += f'{high_comm}{c[0]}\n{high_resp}{cr}{Style.RESET_ALL}\n'
        return ret


    def listener_menu(self):
        ### Listeners main menu
        lmm_title = '\n\n       Listeners Menu\n'
        # lmm_items = ['Show Listeners', 'Kill Listener', 'Back']
        lmm_items = ['Show Listeners', 'Kill Listener']
        lmm_back = False
        lmm = TerminalMenu(
            menu_entries=lmm_items,
            title=lmm_title,
            menu_cursor=self.cursor,
            menu_cursor_style=self.cursor_style,
            menu_highlight_style=self.h_style,
            cycle_cursor=True,
            clear_screen=False,
            accept_keys=('enter', 'ctrl-e', 'ctrl-w')
        )

        ### Listeners List
        lm_list_title = '\n\n       Available Listeners\n'
        listeners = self.stash.get_listeners()
        if listeners:
            lm_list_items = [l[0] for l in listeners]
            lm_list_items.append('Back')
        else:
            lm_list_items = ['NO ACTIVE LISTENERS', 'Back']
        lm_list_back = False
        lm_list_menu = TerminalMenu(
            menu_entries=lm_list_items,
            title=lm_list_title,
            menu_cursor=self.cursor,
            menu_cursor_style=self.cursor_style,
            menu_highlight_style=self.h_style,
            cycle_cursor=True,
            clear_screen=False,
            accept_keys=('enter', 'ctrl-e', 'ctrl-w')
        )

        ### Listener Kill Menu
        ### use same items fo prev menu
        lm_kill_title = '\n\n       Listeners Killer\n'
        lm_kill_back = False
        lm_kill_menu = TerminalMenu(
            menu_entries=lm_list_items,
            title=lm_kill_title,
            menu_cursor=self.cursor_kill,
            menu_cursor_style=self.cursor_style_kill,
            menu_highlight_style=self.h_kill_style,
            cycle_cursor=True,
            clear_screen=False,
            accept_keys=('enter', 'ctrl-e', 'ctrl-w')
        )

        # lmm_sel = lmm.show()

        # Listeners menu loop [0-2] ['Show Listeners', 'Kill Listener', 'Back']
        while not lmm_back:
            lmm_sel = lmm.show()

            if lmm.chosen_accept_key == 'ctrl-w':
                lmm_back = True
                self.on_activate_l()
            elif lmm.chosen_accept_key == 'ctrl-e':
                lmm_back = True
                self.on_activate_r()
            else:
                if lmm_sel == 0:
                    ## Listeners list menu
                    while not lm_list_back:
                        lm_list_sel = lm_list_menu.show()
                        if lm_list_items[lm_list_sel] in ['NO ACTIVE LISTENERS', 'Back']:
                            lm_list_back = True
                    
                    lm_list_back = False
                
                elif lmm_sel == 1:
                    ## kill listener menu
                    while not lm_kill_back:
                        lm_kill_sel = lm_kill_menu.show()
                        if lm_list_items[lm_kill_sel] in ['NO ACTIVE LISTENERS', 'Back']:
                            lm_kill_back = True
                    
                    lm_kill_back = False
                


    # def sub_init(self):
    #     self.main_sub()