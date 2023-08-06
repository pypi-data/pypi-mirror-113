import collections
import threading
import inspect
import time
import json
import sys

import websocket
import requests

from .common import *

websocket.enableTrace(False) # disable auto-outputting of socket events

class Dev:
    '''
    Holds all the information and plumbing required to connect to netsblox, exchange messages, and call RPCs.
    '''

    def __init__(self, *, run_forever = False):
        '''
        Opens a new client connection to NetsBlox, allowing you to access any of the NetsBlox services from python.

        :run_forever: prevents the python program from terminating even after the end of your script.
        This is useful if you have long-running programs that are based on message-passing rather than looping.
        '''

        self._client_id = f'_pyblox{round(time.time() * 1000)}'
        self._base_url = 'https://dev.netsblox.org'

        # set these up before the websocket since it might send us messages
        self._message_cv = threading.Condition(threading.Lock())
        self._message_queue = collections.deque()
        self._message_handlers = {}

        # create a websocket and start it before anything non-essential (has some warmup communication)
        self._ws_lock = threading.Lock()
        self._ws = websocket.WebSocketApp(self._base_url.replace('http', 'ws'),
            on_open = self._ws_open, on_close = self._ws_close, on_error = self._ws_error, on_message = self._ws_message)
        self._ws_thread = threading.Thread(target = self._ws.run_forever)
        self._ws_thread.setDaemon(not run_forever)
        self._ws_thread.start()

        # create a thread to manage the message queue
        self._message_thread = threading.Thread(target = self._message_router)
        self._message_thread.setDaemon(True)
        self._message_thread.start()

        res = requests.post(f'{self._base_url}/api/newProject',
            small_json({ 'clientId': self._client_id, 'name': None }),
            headers = { 'Content-Type': 'application/json' })
        res = json.loads(res.text)
        self._project_id = res['projectId']
        self._project_name = res['name']
        self._role_id = res['roleId']
        self._role_name = res['roleName']

        self.air_quality = AirQuality(self)
        self.alexa = Alexa(self)
        self.autograders = Autograders(self)
        self.base_x = BaseX(self)
        self.battleship = Battleship(self)
        self.covid19 = COVID19(self)
        self.chart = Chart(self)
        self.cloud_variables = CloudVariables(self)
        self.connect_n = ConnectN(self)
        self.core_nlp = CoreNLP(self)
        self.dev = Dev(self)
        self.earth_orbit = EarthOrbit(self)
        self.earthquakes = Earthquakes(self)
        self.eclipse2017 = Eclipse2017(self)
        self.execute = Execute(self)
        self.geolocation = Geolocation(self)
        self.google_maps = GoogleMaps(self)
        self.google_street_view = GoogleStreetView(self)
        self.hangman = Hangman(self)
        self.historical_temperature = HistoricalTemperature(self)
        self.human_mortality_database = HumanMortalityDatabase(self)
        self.hurricane_data = HurricaneData(self)
        self.ice_core_data = IceCoreData(self)
        self.io_tscape = IoTScape(self)
        self.key_value_store = KeyValueStore(self)
        self.mauna_loa_co2_data = MaunaLoaCO2Data(self)
        self.met_museum = MetMuseum(self)
        self.movie_db = MovieDB(self)
        self.nasa = NASA(self)
        self.nplayer = NPlayer(self)
        self.new_york_public_library = NewYorkPublicLibrary(self)
        self.new_york_times = NewYorkTimes(self)
        self.ocean_data = OceanData(self)
        self.paleocean_oxygen_isotopes = PaleoceanOxygenIsotopes(self)
        self.parallel_dots = ParallelDots(self)
        self.phone_iot = PhoneIoT(self)
        self.project_gutenberg = ProjectGutenberg(self)
        self.public_roles = PublicRoles(self)
        self.robo_scape = RoboScape(self)
        self.service_creation = ServiceCreation(self)
        self.simple_hangman = SimpleHangman(self)
        self.smithsonian = Smithsonian(self)
        self.star_map = StarMap(self)
        self.thingspeak = Thingspeak(self)
        self.this_xdoes_not_exist = ThisXDoesNotExist(self)
        self.traffic = Traffic(self)
        self.translation = Translation(self)
        self.trivia = Trivia(self)
        self.twenty_questions = TwentyQuestions(self)
        self.twitter = Twitter(self)
        self.water_watch = WaterWatch(self)
        self.weather = Weather(self)

    def _ws_open(self, ws):
        with self._ws_lock:
            ws.send(small_json({ 'type': 'set-uuid', 'clientId': self._client_id }))

    def _ws_close(self, ws, status, message):
        print('ws close', file=sys.stderr)
    def _ws_error(self, ws, error):
        print('ws error:', error, file=sys.stderr)

    def _ws_message(self, ws, message):
        try:
            message = json.loads(message)
            ty = message['type']

            if ty == 'connected': # currently unused
                return
            elif ty == 'ping':
                with self._ws_lock:
                    ws.send(small_json({ 'type': 'pong' }))
                    return
            elif ty == 'message':
                with self._message_cv:
                    self._message_queue.append(message)
                    self._message_cv.notify()
        except:
            pass
    
    def send_message(self, msg_type, **args):
        with self._ws_lock:
            self._ws.send(small_json({
                'type': 'message', 'msgType': msg_type, 'content': args,
                'dstId': 'everyone in room', 'srcId': self.get_public_role_id()
            }))

    @staticmethod
    def _check_handler(handler, content):
        argspec = inspect.getfullargspec(handler)
        unused_params = set(content.keys())
        for arg in argspec.args + argspec.kwonlyargs:
            if arg not in content:
                return f'    unknown param: \'{arg}\' typo?\n    available params: {list(content.keys())}'
            unused_params.remove(arg)
        return { k: content[k] for k in content.keys() if k not in unused_params } if unused_params and argspec.varkw is None else content
    def _message_router(self):
        while True:
            try:
                message = None
                handlers = None
                with self._message_cv:
                    while not self._message_queue:
                        self._message_cv.wait()
                    message = self._message_queue.popleft()
                    handlers = self._message_handlers.get(message['msgType'])
                    handlers = handlers[:] if handlers is not None else [] # iteration without mutex needs a (shallow) copy

                content = message['content']
                for handler in handlers: # without mutex lock so we don't block new ws messages or on_message()
                    packet = Dev._check_handler(handler, content)
                    if type(packet) == str:
                        print(f'\'{message["msgType"]}\' message handler error:\n{packet}', file=sys.stderr)
                        continue

                    try:
                        handler(**packet) # the handler could be arbitrarily long and is fallible
                    except:
                        pass
            except:
                pass
    
    def _on_message(self, msg_type, handler):
        with self._message_cv:
            handlers = self._message_handlers.get(msg_type)
            if handlers is None:
                handlers = []
                self._message_handlers[msg_type] = handlers
            handlers.append(handler)
    def on_message(self, msg_type, handler=None):
        '''
        Adds a new message handler for incoming messages of the given type.
        If :handler: is specified, it is used as the message handler.
        Otherwise, this returns an annotation type that can be applied to a function definition.
        For example, the following would cause on_start to be called on every incoming 'start' message.

        @client.on_message('start')
        def on_start():
            print('started')
        '''
        if handler is not None:
            self._on_message(msg_type, handler)
        else:
            def wrapper(f):
                self._on_message(msg_type, f)
                return f
            return wrapper
    
    def _call(self, service, rpc, payload):
        payload = { k: prep_send(v) for k,v in payload.items() }
        state = f'uuid={self._client_id}&projectId={self._project_id}&roleId={self._role_id}&t={round(time.time() * 1000)}'
        url = f'{self._base_url}/services/{service}/{rpc}?{state}'
        res = requests.post(url,
            small_json(payload), # if the json has unnecessary white space, request on the server will hang for some reason
            headers = { 'Content-Type': 'application/json' })

        if res.status_code == 200:
            try:
                return json.loads(res.text)
            except:
                return res.text # strings are returned unquoted, so they'll fail to parse as json
        elif res.status_code == 404:
            raise NotFoundError(res.text)
        elif res.status_code == 500:
            raise ServerError(res.text)
        else:
            raise Exception(f'Unknown error: {res.status_code}\n{res.text}')

    def disconnect(self):
        '''
        Disconnects the client from the NetsBlox server.
        If the client was created with :run_forever:, this will allow the program to terminate.
        '''
        with self._ws_lock:
            self._ws.close() # closing the websocket will kill the deamon thread

    def get_public_role_id(self):
        return f'{self._role_name}@{self._project_name}@{self._client_id}'

class AirQuality:
    '''
    The AirQuality Service provides access to real-time air quality data using the AirNowAPI.
    For more information, check out https://docs.airnowapi.org/.
    '''
    def __init__(self, client):
        self._client = client
    def quality_index(self, latitude, longitude):
        '''
        Get air quality index of closest reporting location for coordinates
        '''
        return self._client._call('AirQuality', 'qualityIndex', { 'latitude': latitude, 'longitude': longitude })
    def quality_index_by_zip_code(self, zip_code):
        '''
        Get air quality index of closest reporting location for ZIP code
        '''
        return self._client._call('AirQuality', 'qualityIndexByZipCode', { 'zipCode': zip_code })
class Alexa:
    '''
    The Alexa service provides capabilities for building your own Alexa skills!
    
    An Alexa skill consists of some general information (such as the name to use
    for invocation) as well as a list of supported intents. An intent is a command
    or question to which the skill can respond. Intents consist of a name, list of
    utterances, and any required slots. Utterances are examples of how the user might
    phrase questions or commands. Slots are used to define placeholders for concepts
    like names, cities, etc.
    
    When Alexa determines that a request was made to a given intent, the slots are
    resolved to their corresponding values and then passed to the "handler" for the
    intent.
    '''
    def __init__(self, client):
        self._client = client
    def create_skill(self, configuration):
        '''
        Create an Alexa Skill from a configuration.
        '''
        return self._client._call('Alexa', 'createSkill', { 'configuration': configuration })
    def invoke_skill(self, id, utterance):
        '''
        Invoke the skill with the given utterance using the closest intent.
        '''
        return self._client._call('Alexa', 'invokeSkill', { 'ID': id, 'utterance': utterance })
    def delete_skill(self, id):
        '''
        Delete the given Alexa Skill (created within NetsBlox).
        '''
        return self._client._call('Alexa', 'deleteSkill', { 'ID': id })
    def list_skills(self):
        '''
        List the IDs of all the Alexa Skills created in NetsBlox for the given user.
        '''
        return self._client._call('Alexa', 'listSkills', {  })
    def get_skill(self, id):
        '''
        Get the configuration of the given Alexa Skill.
        '''
        return self._client._call('Alexa', 'getSkill', { 'ID': id })
    def update_skill(self, id, configuration):
        '''
        Update skill configuration with the given ID.
        '''
        return self._client._call('Alexa', 'updateSkill', { 'ID': id, 'configuration': configuration })
    def get_skill_categories(self):
        '''
        Get a list of all valid categories for Alexa skills.
        '''
        return self._client._call('Alexa', 'getSkillCategories', {  })
    def get_slot_types(self):
        '''
        Get a list of all valid slot types that can be added to an intent.
        '''
        return self._client._call('Alexa', 'getSlotTypes', {  })
class Autograders:
    '''
    The Autograders service enables users to create custom autograders for
    use within NetsBlox.
    
    For more information, check out https://editor.netsblox.org/docs/services/Autograders/index.html
    '''
    def __init__(self, client):
        self._client = client
    def create_autograder(self, configuration):
        '''
        Create an autograder using the supplied configuration.
        '''
        return self._client._call('Autograders', 'createAutograder', { 'configuration': configuration })
    def get_autograders(self):
        '''
        List the autograders for the given user.
        '''
        return self._client._call('Autograders', 'getAutograders', {  })
    def get_autograder_config(self, name):
        '''
        Fetch the autograder configuration.
        '''
        return self._client._call('Autograders', 'getAutograderConfig', { 'name': name })
class BaseX:
    '''
    The BaseX Service provides access to an existing BaseX instance.
    '''
    def __init__(self, client):
        self._client = client
    def query(self, url, database, query, username=None, password=None):
        '''
        Evaluate an XQuery expression.
        '''
        return self._client._call('BaseX', 'query', { 'url': url, 'database': database, 'query': query, 'username': username, 'password': password })
    def command(self, url, command, username=None, password=None):
        '''
        Execute a single database command.
        
        A list of commands can be found at http://docs.basex.org/wiki/Commands
        '''
        return self._client._call('BaseX', 'command', { 'url': url, 'command': command, 'username': username, 'password': password })
class Battleship:
    '''
    The Battleship Service provides helpful utilities for building a distributed
    game of battleship.
    
    Overview
    --------
    
    Like regular Battleship, the Battleship service has two states: placing ships and shooting at ships.
    During placement, it expects each role to place each ship on his/her board and will not allow the game to proceed to the shooting phase until each role has placed all his/her ships.
    Placement, firing and starting blocks will return true if successful or an error message if it fails.
    
    Blocks
    ------
    
    - place <ship> at <row> <column> facing <direction> - Places a ship on your board with the front at the given row and column facing the given direction. Returns true if placed successfully (eg, on the board and not overlapping another ship). Also, placing a ship twice results in a move (not duplicates).
    - start game - Try to start the game. If both users have all their ships placed, it should return true and send start messages to all roles. Otherwise, it will return with a message saying that it is waiting on a specific role.
    - fire at <row> <column> - This block allows the user to try to fire at the given row and column. It returns true if it was a valid move; otherwise it will return an error message like it's not your turn!. On a successful move, the server will send either a hit or miss message to everyone in the room. Then it will send a your turn message to the player to play next.
    - active ships for <role> - This block returns a list of all ships that are still afloat for the given role. If no role is specified, it defaults to the sender's role.
    - all ships - Returns a list of all ship names. Useful in programmatically placing ships.
    - ship length <ship> - Returns the length of the given ship.
    - restart game - Restarts the given game (all boards, etc)
    
    Message Types
    -------------
    
    - start - Received when start game finishes successfully for any role. After game has officially started, users can no longer move ships.
    - your turn - Received when the given role's turn starts.
    - hit - role is the owner of the ship that has been hit. ship is the name of the ship that has been hit, and row and column provide the location on the board where it was hit. sunk provides a true/false value for if the ship was sunk.
    - miss - role is the owner of the board receiving the shot and row and column correspond to the board location or the shot.
    '''
    def __init__(self, client):
        self._client = client
    def reset(self):
        '''
        Resets the game by clearing the board and reverting to the placing phase
        '''
        return self._client._call('Battleship', 'reset', {  })
    def start(self):
        '''
        Begins the game, if board is ready
        '''
        return self._client._call('Battleship', 'start', {  })
    def place_ship(self, ship, row, column, facing):
        '''
        Place a ship on the board
        '''
        return self._client._call('Battleship', 'placeShip', { 'ship': ship, 'row': row, 'column': column, 'facing': facing })
    def fire(self, row, column):
        '''
        Fire a shot at the board
        '''
        return self._client._call('Battleship', 'fire', { 'row': row, 'column': column })
    def remaining_ships(self, role_id):
        '''
        Get number of remaining ships of a role
        '''
        return self._client._call('Battleship', 'remainingShips', { 'roleID': role_id })
    def all_ships(self):
        '''
        Get list of ship types
        '''
        return self._client._call('Battleship', 'allShips', {  })
    def ship_length(self, ship):
        '''
        Get length of a ship type
        '''
        return self._client._call('Battleship', 'shipLength', { 'ship': ship })
class COVID19:
    '''
    The COVID-19 Service provides access to the 2019-nCoV dataset compiled by Johns Hopkins University.
    This dataset includes deaths, confirmed cases, and recoveries related to the COVID-19 pandemic.
    
    For more information, check out https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases
    '''
    def __init__(self, client):
        self._client = client
    def get_confirmed_counts(self, country, state=None, city=None):
        '''
        Get number of confirmed cases of COVID-19 by date for a specific country and state.
        
        Date is in month/day/year format.
        '''
        return self._client._call('COVID-19', 'getConfirmedCounts', { 'country': country, 'state': state, 'city': city })
    def get_death_counts(self, country, state=None, city=None):
        '''
        Get number of cases of COVID-19 resulting in death by date for a specific country and state.
        
        Date is in month/day/year format.
        '''
        return self._client._call('COVID-19', 'getDeathCounts', { 'country': country, 'state': state, 'city': city })
    def get_recovered_counts(self, country, state=None, city=None):
        '''
        Get number of cases of COVID-19 in which the person recovered by date for a specific country and state.
        
        Date is in month/day/year format.
        '''
        return self._client._call('COVID-19', 'getRecoveredCounts', { 'country': country, 'state': state, 'city': city })
    def get_locations_with_data(self):
        '''
        Get a list of all countries (and states, cities) with data available.
        '''
        return self._client._call('COVID-19', 'getLocationsWithData', {  })
    def get_location_coordinates(self, country, state=None, city=None):
        '''
        Get the latitude and longitude for a location with data available.
        '''
        return self._client._call('COVID-19', 'getLocationCoordinates', { 'country': country, 'state': state, 'city': city })
class Chart:
    '''
    A charting service powered by gnuplot.
    '''
    def __init__(self, client):
        self._client = client
    def draw(self, lines, options=None):
        '''
        Create charts and histograms from data.
        '''
        return self._client._call('Chart', 'draw', { 'lines': lines, 'options': options })
    def default_options(self):
        '''
        Get the default options for the Chart.draw RPC.
        '''
        return self._client._call('Chart', 'defaultOptions', {  })
class CloudVariables:
    '''
    The CloudVariables Service provides support for storing variables on the cloud.
    Variables can be optionally password-protected or stored only for the current user.
    
    Cloud variables that are inactive (no reads or writes) for 30 days are subject to deletion.
    '''
    def __init__(self, client):
        self._client = client
    def get_variable(self, name, password=None):
        '''
        Get the value of a cloud variable
        '''
        return self._client._call('CloudVariables', 'getVariable', { 'name': name, 'password': password })
    def set_variable(self, name, value, password=None):
        '''
        Set a cloud variable.
        If a password is provided on creation, the variable will be password-protected.
        '''
        return self._client._call('CloudVariables', 'setVariable', { 'name': name, 'value': value, 'password': password })
    def delete_variable(self, name, password=None):
        '''
        Delete a given cloud variable
        '''
        return self._client._call('CloudVariables', 'deleteVariable', { 'name': name, 'password': password })
    def lock_variable(self, name, password=None):
        '''
        Lock a given cloud variable.
        
        A locked variable cannot be changed by anyone other than the person
        who locked it. A variable cannot be locked for more than 5 seconds.
        '''
        return self._client._call('CloudVariables', 'lockVariable', { 'name': name, 'password': password })
    def unlock_variable(self, name, password=None):
        '''
        Unlock a given cloud variable.
        
        A locked variable cannot be changed by anyone other than the person
        who locked it. A variable cannot be locked for more than 5 minutes.
        '''
        return self._client._call('CloudVariables', 'unlockVariable', { 'name': name, 'password': password })
    def get_user_variable(self, name):
        '''
        Get the value of a variable for the current user.
        '''
        return self._client._call('CloudVariables', 'getUserVariable', { 'name': name })
    def set_user_variable(self, name, value):
        '''
        Set the value of the user cloud variable for the current user.
        '''
        return self._client._call('CloudVariables', 'setUserVariable', { 'name': name, 'value': value })
    def delete_user_variable(self, name):
        '''
        Delete the user variable for the current user.
        '''
        return self._client._call('CloudVariables', 'deleteUserVariable', { 'name': name })
class ConnectN:
    '''
    The ConnectN Service provides helpers for building games like Connect-4 and Tic-Tac-Toe.
    '''
    def __init__(self, client):
        self._client = client
    def new_game(self, row=None, column=None, num_dots_to_connect=None):
        '''
        Create a new ConnectN game
        '''
        return self._client._call('ConnectN', 'newGame', { 'row': row, 'column': column, 'numDotsToConnect': num_dots_to_connect })
    def play(self, row, column):
        '''
        Play at the given row, column to occupy the location.
        '''
        return self._client._call('ConnectN', 'play', { 'row': row, 'column': column })
    def is_game_over(self):
        '''
        Check if the current game is over.
        '''
        return self._client._call('ConnectN', 'isGameOver', {  })
    def is_full_board(self):
        '''
        Check if every position on the current board is occupied.
        '''
        return self._client._call('ConnectN', 'isFullBoard', {  })
class CoreNLP:
    '''
    Use CoreNLP to annotate text.
    For more information, check out https://stanfordnlp.github.io/CoreNLP/.
    '''
    def __init__(self, client):
        self._client = client
    def get_annotators(self):
        '''
        Get a list of all the supported annotators.
        The complete list is available at https://stanfordnlp.github.io/CoreNLP/annotators.html.
        '''
        return self._client._call('CoreNLP', 'getAnnotators', {  })
    def annotate(self, text, annotators=None):
        '''
        Annotate text using the provided annotators.
        '''
        return self._client._call('CoreNLP', 'annotate', { 'text': text, 'annotators': annotators })
class Dev:

    def __init__(self, client):
        self._client = client
    def echo(self, argument):
        '''
        A function responding with the provided argument.
        '''
        return self._client._call('Dev', 'echo', { 'argument': argument })
    def throw(self, msg):
        '''
        A function throwing an error.
        '''
        return self._client._call('Dev', 'throw', { 'msg': msg })
    def image(self):
        '''
        A function returning an image.
        '''
        return self._client._call('Dev', 'image', {  })
    def echo_if_within(self, input):
        '''
        Echo if the input is within 10 and 20 (manual test for parameterized types)
        '''
        return self._client._call('Dev', 'echoIfWithin', { 'input': input })
    def detect_abort(self):
        '''
        Sleep for 3 seconds and detect if the RPC was aborted.
        '''
        return self._client._call('Dev', 'detectAbort', {  })
    def caller_info(self):
        '''
        Return the caller info as detected by the server.
        '''
        return self._client._call('Dev', 'callerInfo', {  })
    def sum(self, numbers):
        '''
        Return the sum of the inputs
        '''
        return self._client._call('Dev', 'sum', { 'numbers': numbers })
    def echo_options_example(self, options):
        '''
        Call an argument with a duck typed options object
        '''
        return self._client._call('Dev', 'echoOptionsExample', { 'options': options })
    def get_logs(self):
        '''
        Fetch debug logs for debugging remotely.
        '''
        return self._client._call('Dev', 'getLogs', {  })
    def clear_logs(self):
        '''
        Fetch debug logs for debugging remotely.
        '''
        return self._client._call('Dev', 'clearLogs', {  })
class EarthOrbit:
    '''
    Access to Astronomical Solutions for Earth Paleoclimates. There are three researches (in 1993, 2004, and 2010) about 
    earth orbital parameters' data. This service only uses the 2004 data. 
    
    For more information, check out
    http://vo.imcce.fr/insola/earth/online/earth/earth.html.
    
    Original datasets are available at:
    
    - http://vo.imcce.fr/insola/earth/online/earth/La2004/INSOLN.LA2004.BTL.100.ASC
    - http://vo.imcce.fr/insola/earth/online/earth/La2004/INSOLN.LA2004.BTL.250.ASC
    - http://vo.imcce.fr/insola/earth/online/earth/La2004/INSOLN.LA2004.BTL.ASC
    - http://vo.imcce.fr/insola/earth/online/earth/La2004/INSOLP.LA2004.BTL.ASC
    - http://vo.imcce.fr/webservices/miriade/proxy.php?file=http://145.238.217.35//tmp/insola/insolaouto7Yk3u&format=text
    - http://vo.imcce.fr/webservices/miriade/proxy.php?file=http://145.238.217.38//tmp/insola/insolaouteXT96X&format=text
    '''
    def __init__(self, client):
        self._client = client
    def get_longitude(self, startyear=None, endyear=None):
        '''
        Get longitude of perihelion from moving equinox by year. For more information about this, please visit:
        https://www.physics.ncsu.edu/classes/astron/orbits.html
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('EarthOrbit', 'getLongitude', { 'startyear': startyear, 'endyear': endyear })
    def get_obliquity(self, startyear=None, endyear=None):
        '''
        Get obliquity by year. For more information about obliquity, please visit:
        https://climate.nasa.gov/news/2948/milankovitch-orbital-cycles-and-their-role-in-earths-climate/
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('EarthOrbit', 'getObliquity', { 'startyear': startyear, 'endyear': endyear })
    def get_eccentricity(self, startyear=None, endyear=None):
        '''
        Get eccentricity by year. For more information about eccentricity, please visit: 
        https://climate.nasa.gov/news/2948/milankovitch-orbital-cycles-and-their-role-in-earths-climate/
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('EarthOrbit', 'getEccentricity', { 'startyear': startyear, 'endyear': endyear })
    def get_insolation(self, startyear=None, endyear=None):
        '''
        Get insolation by year. Insolation here is the amount of solar radiation received at 65 N in June on Earth.
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('EarthOrbit', 'getInsolation', { 'startyear': startyear, 'endyear': endyear })
    def get_precession(self, startyear=None, endyear=None):
        '''
        Get precession by year. For more information about precession, please visit:
        https://climate.nasa.gov/news/2948/milankovitch-orbital-cycles-and-their-role-in-earths-climate/
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('EarthOrbit', 'getPrecession', { 'startyear': startyear, 'endyear': endyear })
class Earthquakes:
    '''
    The Earthquakes Service provides access to historical earthquake data.
    For more information, check out https://earthquake.usgs.gov/.
    '''
    def __init__(self, client):
        self._client = client
    def stop(self):
        '''
        Stop sending earthquake messages
        '''
        return self._client._call('Earthquakes', 'stop', {  })
    def by_region(self, min_latitude, max_latitude, min_longitude, max_longitude, start_time=None, end_time=None, min_magnitude=None, max_magnitude=None):
        '''
        Send messages for earthquakes within a given region
        '''
        return self._client._call('Earthquakes', 'byRegion', { 'minLatitude': min_latitude, 'maxLatitude': max_latitude, 'minLongitude': min_longitude, 'maxLongitude': max_longitude, 'startTime': start_time, 'endTime': end_time, 'minMagnitude': min_magnitude, 'maxMagnitude': max_magnitude })
class Eclipse2017:
    '''
    The Eclipse2017 Service provides access to US weather data along the path of the Great American Eclipse.
    For more information about the eclipse, check out https://www.greatamericaneclipse.com/.
    '''
    def __init__(self, client):
        self._client = client
    def eclipse_path(self):
        '''
        Get the path of the eclipse as a list of latitude, longitude, and time.
        '''
        return self._client._call('Eclipse2017', 'eclipsePath', {  })
    def available_stations(self, max_reading_median, max_distance_from_center, latitude=None, longitude=None, max_distance_from_point=None):
        '''
        Get a list of reporting weather stations for the given arguments.
        '''
        return self._client._call('Eclipse2017', 'availableStations', { 'maxReadingMedian': max_reading_median, 'maxDistanceFromCenter': max_distance_from_center, 'latitude': latitude, 'longitude': longitude, 'maxDistanceFromPoint': max_distance_from_point })
    def stations(self):
        '''
        Get a list of reporting stations IDs (pws field).
        '''
        return self._client._call('Eclipse2017', 'stations', {  })
    def station_info(self, station_id):
        '''
        Get information about a given reporting station.
        '''
        return self._client._call('Eclipse2017', 'stationInfo', { 'stationId': station_id })
    def past_temperature(self, station_id, time):
        '''
        Get historical temperature for a given weather station.
        '''
        return self._client._call('Eclipse2017', 'pastTemperature', { 'stationId': station_id, 'time': time })
    def past_condition(self, station_id, time):
        '''
        Get historical conditions at a given weather station.
        '''
        return self._client._call('Eclipse2017', 'pastCondition', { 'stationId': station_id, 'time': time })
    def temperature_history(self, station_id, limit):
        '''
        Get the reported temperatures for a given weather station.
        '''
        return self._client._call('Eclipse2017', 'temperatureHistory', { 'stationId': station_id, 'limit': limit })
    def condition_history(self, station_id, limit):
        '''
        Get the reported conditions for a given weather station.
        '''
        return self._client._call('Eclipse2017', 'conditionHistory', { 'stationId': station_id, 'limit': limit })
    def temperature_history_range(self, station_id, start_time, end_time):
        '''
        Get the reported temperatures during a given time for a given weather station.
        '''
        return self._client._call('Eclipse2017', 'temperatureHistoryRange', { 'stationId': station_id, 'startTime': start_time, 'endTime': end_time })
    def condition_history_range(self, station_id, start_time, end_time):
        '''
        Get the reported conditions during a given time for a given weather station.
        '''
        return self._client._call('Eclipse2017', 'conditionHistoryRange', { 'stationId': station_id, 'startTime': start_time, 'endTime': end_time })
    def stations_info(self):
        '''
        Get information about all reporting weather stations.
        '''
        return self._client._call('Eclipse2017', 'stationsInfo', {  })
    def select_section_based(self, num_sections, per_section):
        '''
        Divide the eclipse path into a number of sections and select weather stations from each section.
        '''
        return self._client._call('Eclipse2017', 'selectSectionBased', { 'numSections': num_sections, 'perSection': per_section })
    def select_point_based(self):
        '''
        Get stations selected based on the points of the eclipse path.
        '''
        return self._client._call('Eclipse2017', 'selectPointBased', {  })
class Execute:
    '''
    The Execute Service provides capabilities for executing blocks on the NetsBlox
    server. This is particularly useful for batching RPC requests.
    '''
    def __init__(self, client):
        self._client = client
    def call(self, fn):
        '''
        Execute a function on the NetsBlox server.
        '''
        return self._client._call('Execute', 'call', { 'fn': fn })
class Geolocation:
    '''
    The Geolocation Service provides access to the Google Places API and geocoding capabilities.
    For more information, check out https://developers.google.com/places/
    
    Terms of service: https://developers.google.com/maps/terms
    '''
    def __init__(self, client):
        self._client = client
    def geolocate(self, address):
        '''
        Geolocates the address and returns the coordinates
        '''
        return self._client._call('Geolocation', 'geolocate', { 'address': address })
    def city(self, latitude, longitude):
        '''
        Get the name of the city nearest to the given latitude and longitude.
        '''
        return self._client._call('Geolocation', 'city', { 'latitude': latitude, 'longitude': longitude })
    def county(self, latitude, longitude):
        '''
        Get the name of the county (or closest equivalent) nearest to the given latitude and longitude.
        If the country does not have counties, it will return the corresponding division for administrative level 2.
        
        For more information on administrative divisions, check out https://en.wikipedia.org/wiki/List_of_administrative_divisions_by_country
        '''
        return self._client._call('Geolocation', 'county*', { 'latitude': latitude, 'longitude': longitude })
    def state(self, latitude, longitude):
        '''
        Get the name of the state (or closest equivalent) nearest to the given latitude and longitude.
        If the country does not have states, it will return the corresponding division for administrative level 1.
        
        For more information on administrative divisions, check out https://en.wikipedia.org/wiki/List_of_administrative_divisions_by_country
        '''
        return self._client._call('Geolocation', 'state*', { 'latitude': latitude, 'longitude': longitude })
    def state_code(self, latitude, longitude):
        '''
        Get the code for the state (or closest equivalent) nearest to the given latitude and longitude.
        If the country does not have states, it will return the corresponding division for administrative level 1.
        
        For more information on administrative divisions, check out https://en.wikipedia.org/wiki/List_of_administrative_divisions_by_country
        '''
        return self._client._call('Geolocation', 'stateCode*', { 'latitude': latitude, 'longitude': longitude })
    def country(self, latitude, longitude):
        '''
        Get the name of the country nearest to the given latitude and longitude.
        '''
        return self._client._call('Geolocation', 'country', { 'latitude': latitude, 'longitude': longitude })
    def country_code(self, latitude, longitude):
        '''
        Get the code for the country nearest to the given latitude and longitude.
        '''
        return self._client._call('Geolocation', 'countryCode', { 'latitude': latitude, 'longitude': longitude })
    def info(self, latitude, longitude):
        '''
        Get administrative division information for the given latitude and longitude.
        '''
        return self._client._call('Geolocation', 'info', { 'latitude': latitude, 'longitude': longitude })
    def nearby_search(self, latitude, longitude, keyword=None, radius=None):
        '''
        Find places near an earth coordinate (latitude, longitude) (maximum of 10 results)
        '''
        return self._client._call('Geolocation', 'nearbySearch', { 'latitude': latitude, 'longitude': longitude, 'keyword': keyword, 'radius': radius })
class GoogleMaps:
    '''
    The GoogleMaps Service provides access to the Google Maps API along with helper functions for interacting with the maps (such as converting coordinates).
    For more information, check out https://developers.google.com/maps/documentation/static-maps/intro
    
    Terms of use: https://developers.google.com/maps/terms
    '''
    def __init__(self, client):
        self._client = client
    def get_map(self, latitude, longitude, width, height, zoom):
        '''
        Get a map image of the given region.
        '''
        return self._client._call('GoogleMaps', 'getMap', { 'latitude': latitude, 'longitude': longitude, 'width': width, 'height': height, 'zoom': zoom })
    def get_satellite_map(self, latitude, longitude, width, height, zoom):
        '''
        Get a satellite map image of the given region.
        '''
        return self._client._call('GoogleMaps', 'getSatelliteMap', { 'latitude': latitude, 'longitude': longitude, 'width': width, 'height': height, 'zoom': zoom })
    def get_terrain_map(self, latitude, longitude, width, height, zoom):
        '''
        Get a terrain map image of the given region.
        '''
        return self._client._call('GoogleMaps', 'getTerrainMap', { 'latitude': latitude, 'longitude': longitude, 'width': width, 'height': height, 'zoom': zoom })
    def get_xfrom_longitude(self, longitude):
        '''
        Convert longitude to the x value on the map image.
        '''
        return self._client._call('GoogleMaps', 'getXFromLongitude', { 'longitude': longitude })
    def get_yfrom_latitude(self, latitude):
        '''
        Convert latitude to the y value on the map image.
        '''
        return self._client._call('GoogleMaps', 'getYFromLatitude', { 'latitude': latitude })
    def get_longitude_from_x(self, x):
        '''
        Convert x value of map image to longitude.
        '''
        return self._client._call('GoogleMaps', 'getLongitudeFromX', { 'x': x })
    def get_latitude_from_y(self, y):
        '''
        Convert y value of map image to latitude.
        '''
        return self._client._call('GoogleMaps', 'getLatitudeFromY', { 'y': y })
    def get_earth_coordinates(self, x, y):
        '''
        Get the earth coordinates [latitude, longitude] of a given point in the last requested map image [x, y].
        '''
        return self._client._call('GoogleMaps', 'getEarthCoordinates', { 'x': x, 'y': y })
    def get_image_coordinates(self, latitude, longitude):
        '''
        Get the image coordinates [x, y] of a given location on the earth [latitude, longitude].
        '''
        return self._client._call('GoogleMaps', 'getImageCoordinates', { 'latitude': latitude, 'longitude': longitude })
    def get_distance(self, start_latitude, start_longitude, end_latitude, end_longitude):
        '''
        Get the straight line distance between two points in meters.
        '''
        return self._client._call('GoogleMaps', 'getDistance', { 'startLatitude': start_latitude, 'startLongitude': start_longitude, 'endLatitude': end_latitude, 'endLongitude': end_longitude })
    def max_longitude(self):
        '''
        Get the maximum longitude of the current map.
        '''
        return self._client._call('GoogleMaps', 'maxLongitude', {  })
    def max_latitude(self):
        '''
        Get the maximum latitude of the current map.
        '''
        return self._client._call('GoogleMaps', 'maxLatitude', {  })
    def min_longitude(self):
        '''
        Get the minimum longitude of the current map.
        '''
        return self._client._call('GoogleMaps', 'minLongitude', {  })
    def min_latitude(self):
        '''
        Get the minimum latitude of the current map.
        '''
        return self._client._call('GoogleMaps', 'minLatitude', {  })
class GoogleStreetView:
    '''
    The GoogleStreetView Service provides access to the Google Street View Image API
    For more information, check out https://developers.google.com/maps/documentation/streetview/intro
    
    Terms of use: https://developers.google.com/maps/terms
    '''
    def __init__(self, client):
        self._client = client
    def get_view(self, latitude, longitude, width, height, fieldofview, heading, pitch):
        '''
        Get Street View image of a location using coordinates
        '''
        return self._client._call('GoogleStreetView', 'getView', { 'latitude': latitude, 'longitude': longitude, 'width': width, 'height': height, 'fieldofview': fieldofview, 'heading': heading, 'pitch': pitch })
    def get_view_from_address(self, location, width, height, fieldofview, heading, pitch):
        '''
        Get Street View image of a location from a location string
        '''
        return self._client._call('GoogleStreetView', 'getViewFromAddress', { 'location': location, 'width': width, 'height': height, 'fieldofview': fieldofview, 'heading': heading, 'pitch': pitch })
    def get_info(self, latitude, longitude, fieldofview, heading, pitch):
        '''
        Get Street View metadata of a location using coordinates.
        
        Status explanation:
        
        - OK - No errors occurred.
        - ZERO_RESULTS - No image could be found near the provided location.
        - NOT_FOUND - The location provided could not be found.
        '''
        return self._client._call('GoogleStreetView', 'getInfo', { 'latitude': latitude, 'longitude': longitude, 'fieldofview': fieldofview, 'heading': heading, 'pitch': pitch })
    def get_info_from_address(self, location, fieldofview, heading, pitch):
        '''
        Get Street View metadata of a location using a location query.
        
        Status explanation:
        
        - OK - No errors occurred.
        - ZERO_RESULTS - No image could be found near the provided location.
        - NOT_FOUND - The location provided could not be found.
        '''
        return self._client._call('GoogleStreetView', 'getInfoFromAddress', { 'location': location, 'fieldofview': fieldofview, 'heading': heading, 'pitch': pitch })
    def is_available(self, latitude, longitude, fieldofview, heading, pitch):
        '''
        Check for availability of imagery at a location using coordinates
        '''
        return self._client._call('GoogleStreetView', 'isAvailable', { 'latitude': latitude, 'longitude': longitude, 'fieldofview': fieldofview, 'heading': heading, 'pitch': pitch })
    def is_available_from_address(self, location, fieldofview, heading, pitch):
        '''
        Check for availability of imagery at a location using an address
        '''
        return self._client._call('GoogleStreetView', 'isAvailableFromAddress', { 'location': location, 'fieldofview': fieldofview, 'heading': heading, 'pitch': pitch })
class Hangman:
    '''
    The Hangman Service provides helpers for mediating a distributed game of hangman.
    '''
    def __init__(self, client):
        self._client = client
    def set_word(self, word):
        '''
        Set current word for the game
        '''
        return self._client._call('Hangman', 'setWord', { 'word': word })
    def get_currently_known_word(self):
        '''
        Get current word for the game
        '''
        return self._client._call('Hangman', 'getCurrentlyKnownWord', {  })
    def guess(self, letter):
        '''
        Make a guess in the game
        '''
        return self._client._call('Hangman', 'guess', { 'letter': letter })
    def is_word_guessed(self):
        '''
        Get if word has been guessed
        '''
        return self._client._call('Hangman', 'isWordGuessed', {  })
    def get_wrong_count(self):
        '''
        Get number of wrong guesses made
        '''
        return self._client._call('Hangman', 'getWrongCount', {  })
class HistoricalTemperature:
    '''
    Access to Berkeley Earth data.
    See http://berkeleyearth.org/data/ for additional details.
    
    These RPCs take a region argument, which can either be a country
    or one of the following special values:
    
    - all land - get data for all landmasses around the world
    - global - get data for the entire Earth (including oceans)
    - northern hemisphere - only northern landmasses
    - southern hemisphere - only southern landmasses
    '''
    def __init__(self, client):
        self._client = client
    def monthly_anomaly(self, region):
        '''
        Get the monthly anomaly data for a region
        '''
        return self._client._call('HistoricalTemperature', 'monthlyAnomaly', { 'region': region })
    def annual_anomaly(self, region):
        '''
        Get the 12 month averaged anomaly data for a region
        '''
        return self._client._call('HistoricalTemperature', 'annualAnomaly', { 'region': region })
    def five_year_anomaly(self, region):
        '''
        Get the 5-year averaged anomaly data for a region
        '''
        return self._client._call('HistoricalTemperature', 'fiveYearAnomaly', { 'region': region })
    def ten_year_anomaly(self, region):
        '''
        Get the 10-year averaged anomaly data for a region
        '''
        return self._client._call('HistoricalTemperature', 'tenYearAnomaly', { 'region': region })
    def twenty_year_anomaly(self, region):
        '''
        Get the 20-year averaged anomaly data for a region
        '''
        return self._client._call('HistoricalTemperature', 'twentyYearAnomaly', { 'region': region })
class HumanMortalityDatabase:
    '''
    This service accesses data from the human mortality database which tabulates
    death rates broken down by age group and gender for various countries.
    
    For more information, see https://www.mortality.org/.
    
    Note: for countries that don't report separate male and female death counts,
    the gender breakdowns are just the total multiplied by a rough estimate
    of the percent of people in that country who are male/female.
    '''
    def __init__(self, client):
        self._client = client
    def get_all_data(self):
        '''
        Get all the mortality data. This is potentially a lot of data.
        Only use this if you truly need access to all data.
        
        This is returned as structured data organized by country, then by date (mm/dd/yyyy), then by gender, then by category.
        '''
        return self._client._call('HumanMortalityDatabase', 'getAllData', {  })
    def get_countries(self):
        '''
        Get a list of all the countries represented in the data.
        These are not the country names, but a unique identifier for them.
        '''
        return self._client._call('HumanMortalityDatabase', 'getCountries', {  })
    def get_genders(self):
        '''
        Get a list of all the valid genders represented in the data.
        These can be used in a query.
        '''
        return self._client._call('HumanMortalityDatabase', 'getGenders', {  })
    def get_categories(self):
        '''
        Get a list of all the categories represented in the data.
        These can be used in a query.
        '''
        return self._client._call('HumanMortalityDatabase', 'getCategories', {  })
    def get_all_data_for_country(self, country):
        '''
        Get all the data associated with the given country.
        This is an object organized by year, then by week, then broken down by gender.
        '''
        return self._client._call('HumanMortalityDatabase', 'getAllDataForCountry', { 'country': country })
    def get_time_series(self, country, gender=None, category=None):
        '''
        Get the time series data for the given country, filtered to the specified gender and category
        in month/day/year format.
        '''
        return self._client._call('HumanMortalityDatabase', 'getTimeSeries', { 'country': country, 'gender': gender, 'category': category })
class HurricaneData:
    '''
    The HurricaneData service provides access to the revised Atlantic hurricane
    database (HURDAT2) from the National Hurricane Center (NHC).
    
    For more information, check out https://www.aoml.noaa.gov/hrd/data_sub/re_anal.html
    '''
    def __init__(self, client):
        self._client = client
    def get_hurricane_data(self, name, year):
        '''
        Get hurricane data including location, maximum winds, and central pressure.
        '''
        return self._client._call('HurricaneData', 'getHurricaneData', { 'name': name, 'year': year })
    def get_hurricanes_in_year(self, year):
        '''
        Get the names of all hurricanes occurring in the given year.
        '''
        return self._client._call('HurricaneData', 'getHurricanesInYear', { 'year': year })
    def get_years_with_hurricane_named(self, name):
        '''
        Get the years in which a hurricane with the given name occurred.
        '''
        return self._client._call('HurricaneData', 'getYearsWithHurricaneNamed', { 'name': name })
class IceCoreData:
    '''
    Access to NOAA Paleoclimatology ice core data.
    
    For more information, check out
    https://www.ncdc.noaa.gov/data-access/paleoclimatology-data/datasets/ice-core.
    
    Original datasets are available at:
    
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/antarctica2015co2composite.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/antarctica2015co2law.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/antarctica2015co2wais.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/vostok/co2nat.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/vostok/deutnat.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/epica_domec/edc3deuttemp2007.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/greenland/summit/grip/isotopes/gripd18o.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/vostok/gt4nat.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/law/law2012d18o.txt
    - https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/wdc05a2013d18o.txt
    '''
    def __init__(self, client):
        self._client = client
    def get_ice_core_names(self):
        '''
        Get names of ice cores with data available.
        '''
        return self._client._call('IceCoreData', 'getIceCoreNames', {  })
    def get_data_availability(self):
        '''
        Get a table showing the amount of available data for each ice core.
        '''
        return self._client._call('IceCoreData', 'getDataAvailability', {  })
    def get_carbon_dioxide_data(self, core, startyear=None, endyear=None):
        '''
        Get CO2 in ppm (parts per million) by year from the ice core.
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('IceCoreData', 'getCarbonDioxideData', { 'core': core, 'startyear': startyear, 'endyear': endyear })
    def get_delta18_odata(self, core, startyear=None, endyear=None):
        '''
        Get delta-O-18 in per mil (parts per thousand) by year from the ice core.
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('IceCoreData', 'getDelta18OData', { 'core': core, 'startyear': startyear, 'endyear': endyear })
    def get_deuterium_data(self, core, startyear=None, endyear=None):
        '''
        Get deuterium in per mil (parts per thousand) by year from the ice core.
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('IceCoreData', 'getDeuteriumData', { 'core': core, 'startyear': startyear, 'endyear': endyear })
    def get_temperature_data(self, core, startyear=None, endyear=None):
        '''
        Get temperature difference in Celsius by year from the ice core.
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('IceCoreData', 'getTemperatureData', { 'core': core, 'startyear': startyear, 'endyear': endyear })
    def get_ice_core_metadata(self, core):
        '''
        Get metadata about an ice core including statistics about the available data.
        '''
        return self._client._call('IceCoreData', 'getIceCoreMetadata', { 'core': core })
class IoTScape:
    '''
    The IoTScape Service enables remote devices to provide custom services. Custom
    Services can be found under the "Community/Devices" section using the call <RPC>
    block.
    '''
    def __init__(self, client):
        self._client = client
    def get_devices(self, service):
        '''
        List IDs of devices associated for a service
        '''
        return self._client._call('IoTScape', 'getDevices', { 'service': service })
    def get_services(self):
        '''
        List all IoTScape services registered with the server
        '''
        return self._client._call('IoTScape', 'getServices', {  })
    def get_message_types(self, service):
        '''
        List the message types associated with a service
        '''
        return self._client._call('IoTScape', 'getMessageTypes', { 'service': service })
    def send(self, service, id, command):
        '''
        Make a call to a device as a text command
        '''
        return self._client._call('IoTScape', 'send', { 'service': service, 'id': id, 'command': command })
class KeyValueStore:
    '''
    The KeyValueStore Service provides basic storage functionality using a hierarchical
    key-value storage (similar to CloudVariables).
    '''
    def __init__(self, client):
        self._client = client
    def get(self, key, password=None):
        '''
        Get the stored value for a key.
        '''
        return self._client._call('KeyValueStore', 'get', { 'key': key, 'password': password })
    def put(self, key, value, password=None):
        '''
        Set the stored value for a key.
        '''
        return self._client._call('KeyValueStore', 'put', { 'key': key, 'value': value, 'password': password })
    def delete(self, key, password=None):
        '''
        Delete the stored value for a key.
        '''
        return self._client._call('KeyValueStore', 'delete', { 'key': key, 'password': password })
    def parent(self, key):
        '''
        Get the ID of the parent key.
        '''
        return self._client._call('KeyValueStore', 'parent', { 'key': key })
    def child(self, key, password=None):
        '''
        Get the IDs of the child keys.
        '''
        return self._client._call('KeyValueStore', 'child', { 'key': key, 'password': password })
class MaunaLoaCO2Data:
    '''
    Access to NOAA Earth System Research Laboratory data collected from Mauna Loa, Hawaii.
    
    See https://www.esrl.noaa.gov/gmd/ccgg/trends/ for additional details.
    '''
    def __init__(self, client):
        self._client = client
    def get_raw_co2(self, startyear=None, endyear=None):
        '''
        Get the mole fraction of CO2 (in parts per million) by year. Missing measurements
        are interpolated.
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('MaunaLoaCO2Data', 'getRawCO2', { 'startyear': startyear, 'endyear': endyear })
    def get_co2_trend(self, startyear=None, endyear=None):
        '''
        Get the mole fraction of CO2 (in parts per million) by year with the seasonal
        cycle removed.
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('MaunaLoaCO2Data', 'getCO2Trend', { 'startyear': startyear, 'endyear': endyear })
class MetMuseum:
    '''
    Access the Metropolitan Museum of Art's collection.
    For explanation on the different attributes for each object,
    visit https://metmuseum.github.io.
    '''
    def __init__(self, client):
        self._client = client
    def fields(self):
        '''
        Get a list of available attributes for museum's objects
        '''
        return self._client._call('MetMuseum', 'fields', {  })
    def advanced_search(self, field, query, skip=None, limit=None):
        '''
        Search the Metropolitan Museum of Art
        '''
        return self._client._call('MetMuseum', 'advancedSearch', { 'field': field, 'query': query, 'skip': skip, 'limit': limit })
    def get_info(self, id):
        '''
        Retrieves extended information about a single object
        '''
        return self._client._call('MetMuseum', 'getInfo', { 'id': id })
    def get_image_urls(self, id):
        '''
        Retrieves the image links for a public domain object
        Note: use costume loader library to load the images.
        '''
        return self._client._call('MetMuseum', 'getImageUrls', { 'id': id })
    def search_by_country(self, query):
        return self._client._call('MetMuseum', 'searchByCountry', { 'query': query })
    def search_by_artist_display_bio(self, query):
        return self._client._call('MetMuseum', 'searchByArtistDisplayBio', { 'query': query })
    def search_by_artist_display_name(self, query):
        return self._client._call('MetMuseum', 'searchByArtistDisplayName', { 'query': query })
    def search_by_dimensions(self, query):
        return self._client._call('MetMuseum', 'searchByDimensions', { 'query': query })
    def search_by_object_name(self, query):
        return self._client._call('MetMuseum', 'searchByObjectName', { 'query': query })
    def search_by_classification(self, query):
        return self._client._call('MetMuseum', 'searchByClassification', { 'query': query })
    def search_by_title(self, query):
        return self._client._call('MetMuseum', 'searchByTitle', { 'query': query })
    def search_by_credit_line(self, query):
        return self._client._call('MetMuseum', 'searchByCreditLine', { 'query': query })
    def search_by_object_date(self, query):
        return self._client._call('MetMuseum', 'searchByObjectDate', { 'query': query })
    def search_by_medium(self, query):
        return self._client._call('MetMuseum', 'searchByMedium', { 'query': query })
    def search_by_repository(self, query):
        return self._client._call('MetMuseum', 'searchByRepository', { 'query': query })
    def search_by_department(self, query):
        return self._client._call('MetMuseum', 'searchByDepartment', { 'query': query })
    def search_by_is_highlight(self, query):
        return self._client._call('MetMuseum', 'searchByIsHighlight', { 'query': query })
class MovieDB:
    '''
    The MovieDB Service provides access to movie data using TMDB (The MovieDB API).
    For more information, check out https://www.themoviedb.org/
    
    Terms of use: https://www.themoviedb.org/documentation/api/terms-of-use
    '''
    def __init__(self, client):
        self._client = client
    def search_movie(self, title):
        '''
        Search for a given movie and return movie IDs.
        '''
        return self._client._call('MovieDB', 'searchMovie', { 'title': title })
    def search_person(self, name):
        '''
        Search for a given actor and return person IDs.
        '''
        return self._client._call('MovieDB', 'searchPerson', { 'name': name })
    def movie_backdrop_path(self, id):
        '''
        Get the image path for a given movie backdrop.
        '''
        return self._client._call('MovieDB', 'movieBackdropPath', { 'id': id })
    def movie_budget(self, id):
        '''
        Get the budget for a given movie.
        '''
        return self._client._call('MovieDB', 'movieBudget', { 'id': id })
    def movie_genres(self, id):
        '''
        Get the genres of a given movie.
        '''
        return self._client._call('MovieDB', 'movieGenres', { 'id': id })
    def movie_original_language(self, id):
        '''
        Get the original language of a given movie.
        '''
        return self._client._call('MovieDB', 'movieOriginalLanguage', { 'id': id })
    def movie_original_title(self, id):
        '''
        Get the original title of a given movie.
        '''
        return self._client._call('MovieDB', 'movieOriginalTitle', { 'id': id })
    def movie_overview(self, id):
        '''
        Get an overview for a given movie.
        '''
        return self._client._call('MovieDB', 'movieOverview', { 'id': id })
    def movie_popularity(self, id):
        '''
        Get the popularity for a given movie.
        
        For more information, check out https://developers.themoviedb.org/3/getting-started/popularity
        '''
        return self._client._call('MovieDB', 'moviePopularity', { 'id': id })
    def movie_poster_path(self, id):
        '''
        Get the poster path for a given movie.
        '''
        return self._client._call('MovieDB', 'moviePosterPath', { 'id': id })
    def movie_production_companies(self, id):
        '''
        Get the production companies for a given movie.
        '''
        return self._client._call('MovieDB', 'movieProductionCompanies', { 'id': id })
    def movie_production_countries(self, id):
        '''
        Get the countries in which a given movie was produced.
        '''
        return self._client._call('MovieDB', 'movieProductionCountries', { 'id': id })
    def movie_release_date(self, id):
        '''
        Get the release data for a given movie.
        '''
        return self._client._call('MovieDB', 'movieReleaseDate', { 'id': id })
    def movie_revenue(self, id):
        '''
        Get the revenue for a given movie.
        '''
        return self._client._call('MovieDB', 'movieRevenue', { 'id': id })
    def movie_runtime(self, id):
        '''
        Get the runtime for a given movie.
        '''
        return self._client._call('MovieDB', 'movieRuntime', { 'id': id })
    def movie_spoken_languages(self, id):
        '''
        Get the spoken languages for a given movie.
        '''
        return self._client._call('MovieDB', 'movieSpokenLanguages', { 'id': id })
    def movie_tagline(self, id):
        '''
        Get the tagline for a given movie.
        '''
        return self._client._call('MovieDB', 'movieTagline', { 'id': id })
    def movie_title(self, id):
        '''
        Get the title for a given movie.
        '''
        return self._client._call('MovieDB', 'movieTitle', { 'id': id })
    def movie_vote_average(self, id):
        '''
        Get the average vote for a given movie.
        '''
        return self._client._call('MovieDB', 'movieVoteAverage', { 'id': id })
    def movie_vote_count(self, id):
        '''
        Get the vote count for a given movie.
        '''
        return self._client._call('MovieDB', 'movieVoteCount', { 'id': id })
    def person_biography(self, id):
        '''
        Get the biography for a given person.
        '''
        return self._client._call('MovieDB', 'personBiography', { 'id': id })
    def person_birthday(self, id):
        '''
        Get the birthday of a given person.
        '''
        return self._client._call('MovieDB', 'personBirthday', { 'id': id })
    def person_deathday(self, id):
        '''
        Get the death date of a given person.
        '''
        return self._client._call('MovieDB', 'personDeathday', { 'id': id })
    def person_gender(self, id):
        '''
        Get the gender of a given person.
        '''
        return self._client._call('MovieDB', 'personGender', { 'id': id })
    def person_name(self, id):
        '''
        Get the name of a given person.
        '''
        return self._client._call('MovieDB', 'personName', { 'id': id })
    def person_place_of_birth(self, id):
        '''
        Get the place of birth for a given person.
        '''
        return self._client._call('MovieDB', 'personPlaceOfBirth', { 'id': id })
    def person_popularity(self, id):
        '''
        Get the popularity of a given person.
        
        For more information, check out https://developers.themoviedb.org/3/getting-started/popularity
        '''
        return self._client._call('MovieDB', 'personPopularity', { 'id': id })
    def person_profile_path(self, id):
        '''
        Get the profile path for a given person.
        '''
        return self._client._call('MovieDB', 'personProfilePath', { 'id': id })
    def movie_cast_characters(self, id):
        '''
        Get the cast characters for a given movie.
        '''
        return self._client._call('MovieDB', 'movieCastCharacters', { 'id': id })
    def movie_cast_names(self, id):
        '''
        Get the cast names for a given movie.
        '''
        return self._client._call('MovieDB', 'movieCastNames', { 'id': id })
    def movie_cast_person_ids(self, id):
        '''
        Get the cast IDs for a given movie.
        '''
        return self._client._call('MovieDB', 'movieCastPersonIDs', { 'id': id })
    def movie_cast_profile_paths(self, id):
        '''
        Get the cast profile paths for a given movie.
        '''
        return self._client._call('MovieDB', 'movieCastProfilePaths', { 'id': id })
    def movie_crew_names(self, id):
        '''
        Get the crew names for a given movie.
        '''
        return self._client._call('MovieDB', 'movieCrewNames', { 'id': id })
    def movie_crew_jobs(self, id):
        '''
        Get the crew jobs for a given movie.
        '''
        return self._client._call('MovieDB', 'movieCrewJobs', { 'id': id })
    def movie_crew_person_ids(self, id):
        '''
        Get the crew IDs for a given movie.
        '''
        return self._client._call('MovieDB', 'movieCrewPersonIDs', { 'id': id })
    def movie_crew_profile_paths(self, id):
        '''
        Get the crew profile paths for a given movie.
        '''
        return self._client._call('MovieDB', 'movieCrewProfilePaths', { 'id': id })
    def person_image_file_paths(self, id):
        '''
        Get the image paths for a given person.
        '''
        return self._client._call('MovieDB', 'personImageFilePaths', { 'id': id })
    def person_image_aspect_ratios(self, id):
        '''
        Get the image aspect ratios for a given person.
        '''
        return self._client._call('MovieDB', 'personImageAspectRatios', { 'id': id })
    def person_image_heights(self, id):
        '''
        Get the image heights for a given person.
        '''
        return self._client._call('MovieDB', 'personImageHeights', { 'id': id })
    def person_image_widths(self, id):
        '''
        Get the image widths for a given person.
        '''
        return self._client._call('MovieDB', 'personImageWidths', { 'id': id })
    def person_image_vote_counts(self, id):
        '''
        Get the image vote counts for a given person.
        '''
        return self._client._call('MovieDB', 'personImageVoteCounts', { 'id': id })
    def person_cast_characters(self, id):
        '''
        Get the characters played by a given person.
        '''
        return self._client._call('MovieDB', 'personCastCharacters', { 'id': id })
    def person_cast_movie_ids(self, id):
        '''
        Get the movies in which a given person was cast.
        '''
        return self._client._call('MovieDB', 'personCastMovieIDs', { 'id': id })
    def person_cast_original_titles(self, id):
        '''
        Get the original titles in which a given person was cast.
        '''
        return self._client._call('MovieDB', 'personCastOriginalTitles', { 'id': id })
    def person_cast_poster_paths(self, id):
        '''
        Get the cast poster paths for a given person.
        '''
        return self._client._call('MovieDB', 'personCastPosterPaths', { 'id': id })
    def person_cast_release_dates(self, id):
        '''
        Get the cast release dates for a given person.
        '''
        return self._client._call('MovieDB', 'personCastReleaseDates', { 'id': id })
    def person_cast_titles(self, id):
        '''
        Get the cast titles for a given person.
        '''
        return self._client._call('MovieDB', 'personCastTitles', { 'id': id })
    def person_crew_movie_ids(self, id):
        '''
        Get the movie IDs for which a given person was a member of the crew.
        '''
        return self._client._call('MovieDB', 'personCrewMovieIDs', { 'id': id })
    def person_crew_jobs(self, id):
        '''
        Get the crew jobs for a given person.
        '''
        return self._client._call('MovieDB', 'personCrewJobs', { 'id': id })
    def person_crew_original_titles(self, id):
        '''
        Get the original titles for which a given person was a member of the crew.
        '''
        return self._client._call('MovieDB', 'personCrewOriginalTitles', { 'id': id })
    def person_crew_poster_paths(self, id):
        '''
        Get the poster paths for movies in which a given person was a member of the crew.
        '''
        return self._client._call('MovieDB', 'personCrewPosterPaths', { 'id': id })
    def person_crew_release_dates(self, id):
        '''
        Get the release dates for movies in which a given person was a member of the crew.
        '''
        return self._client._call('MovieDB', 'personCrewReleaseDates', { 'id': id })
    def person_crew_titles(self, id):
        '''
        Get the crew titles for a given person.
        '''
        return self._client._call('MovieDB', 'personCrewTitles', { 'id': id })
    def get_image(self, path):
        '''
        Get an image from a path.
        '''
        return self._client._call('MovieDB', 'getImage', { 'path': path })
class NASA:
    '''
    The NASA Service provides access to planetary pictures and mars weather data.
    For more information, check out https://api.nasa.gov/.
    '''
    def __init__(self, client):
        self._client = client
    def apod(self):
        '''
        Fetch the "Astronomy Picture of the Day" from NASA
        '''
        return self._client._call('NASA', 'apod', {  })
    def apod_details(self):
        '''
        Fetch additional information about the "Astronomy Picture of the Day"
        '''
        return self._client._call('NASA', 'apodDetails', {  })
    def apod_media(self):
        '''
        NASA's 'Astronomy Picture of the Day' media
        '''
        return self._client._call('NASA', 'apodMedia', {  })
class NPlayer:
    '''
    The NPlayer Service provides helpers RPCs for ensuring round-robin turn taking
    among the roles in the project's room.
    
    Each role will receive a "start game" message at the start and then "start turn"
    message when it is the given role's turn to act.
    '''
    def __init__(self, client):
        self._client = client
    def start(self):
        '''
        Start a new turn-based game.
        '''
        return self._client._call('NPlayer', 'start', {  })
    def get_n(self):
        '''
        Get the number of detected players in the game.
        '''
        return self._client._call('NPlayer', 'getN', {  })
    def get_active(self):
        '''
        Get the player whose turn it currently is.
        '''
        return self._client._call('NPlayer', 'getActive', {  })
    def get_previous(self):
        '''
        Get the player who played last.
        '''
        return self._client._call('NPlayer', 'getPrevious', {  })
    def get_next(self):
        '''
        Get the player who will be active next.
        '''
        return self._client._call('NPlayer', 'getNext', {  })
    def end_turn(self, next=None):
        '''
        End your current turn.
        '''
        return self._client._call('NPlayer', 'endTurn', { 'next': next })
class NewYorkPublicLibrary:
    '''
    The New York Public Library (NYPL) Service provides access to NYPL's online repository of historical items.
    '''
    def __init__(self, client):
        self._client = client
    def search(self, term, per_page=None, page=None):
        '''
        Search the New York Public Library collection and return matching items.
        Because there may be many matching items, search results are arranged in pages.
        You can specify the number of items in each page and the page number to retrieve.
        
        This returns a list of up to perPage matches.
        Each item in the list is structured data containing details about the object.
        This includes:
        
        - uuid - a general identifier for the object, needed for NewYorkPublicLibrary.getDetails
        - itemID - another identifier, needed for NewYorkPublicLibrary.getImage
        - title - the title of the object
        - dateDigitized - a timestamp of when the object was added to the database
        '''
        return self._client._call('NewYorkPublicLibrary', 'search', { 'term': term, 'perPage': per_page, 'page': page })
    def get_details(self, uuid):
        '''
        Get details about the item.
        This requires the uuid for the object, which can be retrieved from NewYorkPublicLibrary.search.
        '''
        return self._client._call('NewYorkPublicLibrary', 'getDetails', { 'uuid': uuid })
    def get_image(self, item_id):
        '''
        Get an image of the object.
        This requires the itemID for the object, which can be retrieved from NewYorkPublicLibrary.search.
        '''
        return self._client._call('NewYorkPublicLibrary', 'getImage', { 'itemID': item_id })
class NewYorkTimes:
    '''
    The NewYorkTimes service provides access to the New York Times API including access
    to Moview Reviews, Top Stories, and their Semantic API.
    '''
    def __init__(self, client):
        self._client = client
    def get_top_stories(self, section):
        '''
        Get the top stories for a given section.
        '''
        return self._client._call('NewYorkTimes', 'getTopStories', { 'section': section })
    def get_article_sections(self):
        '''
        Get a list of all valid article sections.
        '''
        return self._client._call('NewYorkTimes', 'getArticleSections', {  })
    def get_latest_articles(self, section):
        '''
        Get the latest articles in a given section.
        '''
        return self._client._call('NewYorkTimes', 'getLatestArticles', { 'section': section })
    def get_movie_critics(self):
        '''
        Get a list of movie critics.
        '''
        return self._client._call('NewYorkTimes', 'getMovieCritics', {  })
    def get_movie_critic_info(self, name):
        '''
        Get information about a given movie critic.
        '''
        return self._client._call('NewYorkTimes', 'getMovieCriticInfo', { 'name': name })
    def search_movie_reviews(self, query, offset=None):
        '''
        Search for movie reviews starting at "offset". Returns up to 20 results.
        '''
        return self._client._call('NewYorkTimes', 'searchMovieReviews', { 'query': query, 'offset': offset })
    def get_movie_reviews(self, offset=None):
        '''
        Get 20 movie reviews starting at "offset".
        '''
        return self._client._call('NewYorkTimes', 'getMovieReviews', { 'offset': offset })
    def get_movie_reviews_by_critic(self, critic, offset=None):
        '''
        Get 20 movie reviews by a given critic starting at "offset".
        '''
        return self._client._call('NewYorkTimes', 'getMovieReviewsByCritic', { 'critic': critic, 'offset': offset })
    def get_critics_picks(self, offset=None):
        '''
        Get 20 movie reviews picked by critics starting at "offset".
        '''
        return self._client._call('NewYorkTimes', 'getCriticsPicks', { 'offset': offset })
    def search_articles(self, query, offset=None):
        '''
        Search for articles given a query. Up to 10 articles will be returned.
        More articles can be retrieved by specifying the "offset" or number of
        results to skip before returning the results.
        '''
        return self._client._call('NewYorkTimes', 'searchArticles', { 'query': query, 'offset': offset })
    def get_best_sellers(self, list, date=None):
        '''
        Get the best selling books for a given list and date.
        '''
        return self._client._call('NewYorkTimes', 'getBestSellers', { 'list': list, 'date': date })
    def get_best_seller_lists(self):
        '''
        Get the best seller list names.
        '''
        return self._client._call('NewYorkTimes', 'getBestSellerLists', {  })
    def get_top_best_sellers(self, date):
        '''
        Get the top 5 books for all the best seller lists for a given date.
        '''
        return self._client._call('NewYorkTimes', 'getTopBestSellers', { 'date': date })
    def search_best_sellers(self, title=None, author=None, offset=None):
        '''
        Search for books on current or previous best seller lists.
        '''
        return self._client._call('NewYorkTimes', 'searchBestSellers', { 'title': title, 'author': author, 'offset': offset })
    def search_concepts(self, query):
        '''
        Search for concepts of interest.
        '''
        return self._client._call('NewYorkTimes', 'searchConcepts', { 'query': query })
    def get_concept_info(self, concept):
        '''
        Get additional information about a concept such as links to other concepts and
        geocodes.
        '''
        return self._client._call('NewYorkTimes', 'getConceptInfo', { 'concept': concept })
    def get_concept_types(self):
        '''
        Get a list of all concept types.
        '''
        return self._client._call('NewYorkTimes', 'getConceptTypes', {  })
    def get_articles_with_concept(self, concept):
        '''
        Fetch up to 10 articles containing the given concept.
        '''
        return self._client._call('NewYorkTimes', 'getArticlesWithConcept', { 'concept': concept })
    def get_most_emailed_articles(self, period):
        '''
        Get the most emailed articles over the past day, week, or month.
        '''
        return self._client._call('NewYorkTimes', 'getMostEmailedArticles', { 'period': period })
    def get_most_viewed_articles(self, period):
        '''
        Get the most viewed articles over the past day, week, or month.
        '''
        return self._client._call('NewYorkTimes', 'getMostViewedArticles', { 'period': period })
    def get_most_shared_articles(self, period):
        '''
        Get the articles shared most on Facebook over the past day, week, or month.
        '''
        return self._client._call('NewYorkTimes', 'getMostSharedArticles', { 'period': period })
class OceanData:
    '''
    The OceanData service provides access to scientific ocean data including
    temperature and sea level.
    
    For more information, check out:
    
    - http://www.columbia.edu/~mhs119/Sensitivity+SL+CO2/
    - https://www.paleo.bristol.ac.uk/~ggdjl/warm_climates/hansen_etal.pdf.
    '''
    def __init__(self, client):
        self._client = client
    def get_oxygen_ratio(self, start_year=None, end_year=None):
        '''
        Get historical oxygen isotope ratio values by year.
        
        If startYear or endYear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('OceanData', 'getOxygenRatio', { 'startYear': start_year, 'endYear': end_year })
    def get_deep_ocean_temp(self, start_year=None, end_year=None):
        '''
        Get historical deep ocean temperatures in Celsius by year.
        
        If startYear or endYear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('OceanData', 'getDeepOceanTemp', { 'startYear': start_year, 'endYear': end_year })
    def get_surface_temp(self, start_year=None, end_year=None):
        '''
        Get historical surface ocean temperatures in Celsius by year.
        
        If startYear or endYear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('OceanData', 'getSurfaceTemp', { 'startYear': start_year, 'endYear': end_year })
    def get_sea_level(self, start_year=None, end_year=None):
        '''
        Get historical sea level in meters by year.
        
        If startYear or endYear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('OceanData', 'getSeaLevel', { 'startYear': start_year, 'endYear': end_year })
class PaleoceanOxygenIsotopes:
    '''
    Access to NOAA Global Pliocene-Pleistocene Benthic d18O Stack.
    
    For more information, check out
    https://www.ncdc.noaa.gov/paleo-search/study/5847
    
    Original datasets are available at:
    https://www1.ncdc.noaa.gov/pub/data/paleo/contributions_by_author/lisiecki2005/lisiecki2005.txt.
    '''
    def __init__(self, client):
        self._client = client
    def get_delta18_o(self, startyear=None, endyear=None):
        '''
        Get delta 18O value (unit: per mill. It is a parts per thousand unit, often used directly to 
        refer to isotopic ratios and calculated by calculating the ratio of isotopic concentrations in 
        a sample and in a standard, subtracting one and multiplying by one thousand).
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('PaleoceanOxygenIsotopes', 'getDelta18O', { 'startyear': startyear, 'endyear': endyear })
    def get_delta18_oerror(self, startyear=None, endyear=None):
        '''
        Get delta 18O error value (unit: per mill).
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('PaleoceanOxygenIsotopes', 'getDelta18OError', { 'startyear': startyear, 'endyear': endyear })
    def get_average_sedimentation_rates(self, startyear=None, endyear=None):
        '''
        Get average sedimentation rate value (unit: centimeter per kiloyear).
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('PaleoceanOxygenIsotopes', 'getAverageSedimentationRates', { 'startyear': startyear, 'endyear': endyear })
    def get_normalized_sedimentation_rates(self, startyear=None, endyear=None):
        '''
        Get normalized sedimentation rate value (unit: dimensionless).
        
        If startyear or endyear is provided, only measurements within the given range will be returned.
        '''
        return self._client._call('PaleoceanOxygenIsotopes', 'getNormalizedSedimentationRates', { 'startyear': startyear, 'endyear': endyear })
class ParallelDots:
    '''
    Uses ParallelDots AI to process or compare text for a variety of features.
    See the API documentation, at 
    http://apis.paralleldots.com/text_docs/index.html
    
    Terms of use: https://www.paralleldots.com/terms-and-conditions
    '''
    def __init__(self, client):
        self._client = client
    def get_sentiment(self, text):
        '''
        Find the overall sentiment of the given text along with the confidence score.
        The returned structured data hasa confidence level for each of the following sentiment categories:
        negative, neutral, and positive.
        '''
        return self._client._call('ParallelDots', 'getSentiment', { 'text': text })
    def get_similarity(self, text1, text2):
        '''
        Get the level of similarity between two snippets of text.
        Note that the two pieces of text should be long, like full sentences (not just 2 words).
        '''
        return self._client._call('ParallelDots', 'getSimilarity', { 'text1': text1, 'text2': text2 })
    def get_named_entities(self, text):
        '''
        Identify named entities in the given text.
        '''
        return self._client._call('ParallelDots', 'getNamedEntities', { 'text': text })
    def get_keywords(self, text):
        '''
        Extract keywords from the given text along with their confidence score.
        '''
        return self._client._call('ParallelDots', 'getKeywords', { 'text': text })
    def get_taxonomy(self, text):
        '''
        Classify the given text into IAB categories.
        
        For more information about IAB categories, see
        https://www.iab.com/guidelines/iab-quality-assurance-guidelines-qag-taxonomy/
        '''
        return self._client._call('ParallelDots', 'getTaxonomy', { 'text': text })
    def get_emotion(self, text):
        '''
        Find the emotion in the given text.
        This is returned as structured data containing confidence levels for each of the following emotions:
        excited, angry, bored, fear, sad, and happy.
        '''
        return self._client._call('ParallelDots', 'getEmotion', { 'text': text })
    def get_sarcasm_probability(self, text):
        '''
        Compute the probability of sarcasm for the given text.
        '''
        return self._client._call('ParallelDots', 'getSarcasmProbability', { 'text': text })
    def get_intent(self, text):
        '''
        Get the intent of the given text along with the confidence score.
        This is returned as structed data with confidence levels for each of the following intents:
        news, query, spam, marketing, and feedback.
        '''
        return self._client._call('ParallelDots', 'getIntent', { 'text': text })
    def get_abuse(self, text):
        '''
        Classify the given text as abusive, hate_speech, or neither.
        The returned structured data has confidence levels for each of these categories.
        '''
        return self._client._call('ParallelDots', 'getAbuse', { 'text': text })
class PhoneIoT:
    '''
    PhoneIoT is a service in NetsBlox <https://netsblox.org/>_ that's meant to teach Internet of Things (IoT) topics as early as K-12 education.
    It allows you to programmatically access your smartphone's sensors and display.
    This includes accessing hardware sensors such as the accelerometer, gyroscope, microphone, camera, and many others depending on the device.
    PhoneIoT also allows you to control a customizable interactive display, enabling you to use your device as a custom remote control, or even create and run distributed (multiplayer) applications.
    The limits are up to your imagination!
    
    To get started using PhoneIoT, download the PhoneIoT app on your mobile device, available for Android <https://play.google.com/store/apps/details?id=org.netsblox.phoneiot>_ and iOS (*coming soon*), and then go to the NetsBlox editor <https://editor.NetsBlox.org>_.
    In the top left of the editor, you should see a grid of several colored tabs.
    Under the Network tab, grab a call block and place it in the center script area.
    Click the first dropdown on the call block and select the PhoneIoT service.
    The second dropdown selects the specific *Remote Procedure Call* (RPC) to execute - see the table of contents  for information about the various RPCs.
    
    Inside the PhoneIoT app on your mobile device, click the button at the top left to open the menu, and then click connect.
    If you successfully connected, you should get a small popup message at the bottom of the screen.
    If you don't see this message, make sure you have either Wi-Fi or mobile data turned on and try again.
    Near the top of the menu, you should see an ID and password, which will be needed to connect to the device from NetsBlox.
    
    Back in NetsBlox, select the setCredentials RPC and give it your ID and password.
    For convenience, you might want to save the ID in a variable (e.g. device), as it will be referenced many times.
    If you click the call block to run it, you should get an OK result, meaning you successfully connected.
    If you don't see this, make sure you entered the ID and password correctly.
    
    You're now ready to start using the other RPCs in PhoneIoT to communicate with the device!
    '''
    def __init__(self, client):
        self._client = client
    def get_color(self, red, green, blue, alpha=None):
        '''
        Many of the Display RPCs take one or more optional parameters for controlling display color, which is specified as an integer.
        This RPC is a convenience function for constructing a color code from red, green, blue, and alpha values (each is 0-255).
        
        The alpha value controls transparency, with 0 being invisible and 255 being opaque.
        If not specified, alpha will default to 255.
        '''
        return self._client._call('PhoneIoT', 'getColor', { 'red': red, 'green': green, 'blue': blue, 'alpha': alpha })
    def magnitude(self, vec):
        '''
        Given a list of numbers representing a vector, this RPC returns the magnitude (length) of the vector.
        This can be used to get the total acceleration from the accelerometer (which gives a vector).
        '''
        return self._client._call('PhoneIoT', 'magnitude', { 'vec': vec })
    def normalize(self, vec):
        '''
        Given a list of numbers representing a vector, returns the normalized vector (same direction but with a magnitude of 1.0).
        This is identical to dividing each component by the magnitude.
        '''
        return self._client._call('PhoneIoT', 'normalize', { 'vec': vec })
    def clear_controls(self, device):
        '''
        Removes all controls from the device's canvas.
        If you would instead like to remove a specific control, see PhoneIoT.removeControl.
        '''
        return self._client._call('PhoneIoT', 'clearControls', { 'device': device })
    def remove_control(self, device, id):
        '''
        Removes a control with the given ID if it exists.
        If the control does not exist, does nothing (but still counts as success).
        If you would instead like to remove all controls, see PhoneIoT.clearControls.
        '''
        return self._client._call('PhoneIoT', 'removeControl', { 'device': device, 'id': id })
    def add_label(self, device, x, y, text=None, options=None):
        '''
        Adds a label control to the canvas at the given position.
        If text is not specified, it default to empty, which can be used to hide the label when nothing needs to be displayed.
        The text can be modified later via PhoneIoT.setText.
        
        Labels do not have a size, so they also don't do text wrapping.
        Because of this, you should keep label text relatively short.
        If you need a large amount of text written, consider using PhoneIoT.addTextField with readonly = true.
        '''
        return self._client._call('PhoneIoT', 'addLabel', { 'device': device, 'x': x, 'y': y, 'text': text, 'options': options })
    def add_button(self, device, x, y, width, height, text=None, options=None):
        '''
        Adds a button to the display with the given position and size.
        If not specified, the default text for a button is empty, which can be used to just make a colored, unlabeled button.
        The text can be modified later via PhoneIoT.setText.
        '''
        return self._client._call('PhoneIoT', 'addButton', { 'device': device, 'x': x, 'y': y, 'width': width, 'height': height, 'text': text, 'options': options })
    def add_image_display(self, device, x, y, width, height, options=None):
        '''
        Adds an image display wit hthe given position and size.
        If not specified, an image display is readonly, meaning that the user cannot modify its content.
        If (explicitly) not set to readonly, then the user can click on the image display to change the image to a new picture from the camera.
        '''
        return self._client._call('PhoneIoT', 'addImageDisplay', { 'device': device, 'x': x, 'y': y, 'width': width, 'height': height, 'options': options })
    def add_text_field(self, device, x, y, width, height, options=None):
        '''
        Adds a text field to the canvas.
        These are typically used to display large blocks of text, or to accept input text from the user.
        If not set to readonly, the user can click on the text field to change its content.
        
        If you have a small amount of text you need to show and would otherwise make this control readonly, consider using PhoneIoT.addLabel instead.
        '''
        return self._client._call('PhoneIoT', 'addTextField', { 'device': device, 'x': x, 'y': y, 'width': width, 'height': height, 'options': options })
    def add_joystick(self, device, x, y, width, options=None):
        '''
        Adds a joystick control to the canvas at the given position and size.
        No height parameter is given because joysticks are always circular (similar to passing style = circle to PhoneIoT.addButton).
        
        The position of the joystick is given by a vector [x, y], which is normalized to a length of 1.
        If you would prefer to not have this normalization and want rectangular coordinates instead of circular, consider using PhoneIoT.addTouchpad instead.
        '''
        return self._client._call('PhoneIoT', 'addJoystick', { 'device': device, 'x': x, 'y': y, 'width': width, 'options': options })
    def add_touchpad(self, device, x, y, width, height, options=None):
        '''
        Adds a touchpad control to the canvas at the given position and size.
        This control is similar to the joystick control, except that it is rectangular,
        the vector is not normalized to a distance of 1,
        the "stick" does not move back to (0, 0) upon letting go,
        and there is an additional "tag" value denoting if each event was a touch down, move, or up.
        
        Although the vector value is not normalized to a length of 1,
        each component (x and y individually) is in [-1, 1].
        '''
        return self._client._call('PhoneIoT', 'addTouchpad', { 'device': device, 'x': x, 'y': y, 'width': width, 'height': height, 'options': options })
    def add_slider(self, device, x, y, width, options=None):
        '''
        Adds a slider control to the display.
        Sliders can be moved around to input or display any value in the range [0, 1].
        If you need values outside of this range, you can do a little math to map them to [0, 1] or vice versa.
        
        You can read and write the value of a slider with PhoneIoT.getLevel and PhoneIoT.setLevel.
        Note that if the control is set to readonly, the user cannot change the value, but you can still do so from code.
        '''
        return self._client._call('PhoneIoT', 'addSlider', { 'device': device, 'x': x, 'y': y, 'width': width, 'options': options })
    def add_toggle(self, device, x, y, text=None, options=None):
        '''
        Adds a toggle control to the canvas at the given location.
        The text parameter can be used to set the initial text shown for the toggle (defaults to empty),
        but this can be changed later with PhoneIoT.setText.
        '''
        return self._client._call('PhoneIoT', 'addToggle', { 'device': device, 'x': x, 'y': y, 'text': text, 'options': options })
    def add_radio_button(self, device, x, y, text=None, options=None):
        '''
        Adds a radio button to the canvas.
        Radio buttons are like toggles (checkboxes), except that they are organized into groups
        and the user can check at most one radion button from any given group.
        These can be used to accept multiple-choice input from the user.
        '''
        return self._client._call('PhoneIoT', 'addRadioButton', { 'device': device, 'x': x, 'y': y, 'text': text, 'options': options })
    def set_text(self, device, id, text=None):
        '''
        Sets the text content of the text-like control with the given ID.
        This can be used on any control that has text, such as a button, label, or text field.
        '''
        return self._client._call('PhoneIoT', 'setText', { 'device': device, 'id': id, 'text': text })
    def get_text(self, device, id):
        '''
        Gets the current text content of the text-like control with the given ID.
        This can be used on any control that has text, such as a button, label, or text field.
        '''
        return self._client._call('PhoneIoT', 'getText', { 'device': device, 'id': id })
    def get_position(self, device, id):
        '''
        Gets the current x and y values for the current position of a positional control.
        This does *not* give the location of the control on the screen.
        Positional controls are controls whose primary interaction is through position.
        For instance, this is used for both joystick and touchpad controls.
        
        For a joystick, this always returns a vector normalized to a length of 1.0.
        If the user is not touching the joystick, it will automatically go back to the center, [0, 0].
        
        For a touchpad, this will either give you the current location of the touch (a list of [x, y])
        or an error if the user is not touching the screen.
        
        If you want to get the value of a slider, use PhoneIoT.getLevel instead.
        
        Instead of calling this in a loop, it is likely better to use the event optional parameter of
        PhoneIoT.addJoystick or PhoneIoT.addTouchpad.
        '''
        return self._client._call('PhoneIoT', 'getPosition', { 'device': device, 'id': id })
    def get_level(self, device, id):
        '''
        Get the current value (a single number) of a value-like control.
        Currently, the only supported control is a slider, which returns a value in [0, 1].
        
        Instead of calling this in a loop, it is likely better to use the event optional parameter of PhoneIoT.addSlider.
        
        If you want to get the cursor position of a joystick or touchpad, use PhoneIoT.getPosition instead.
        '''
        return self._client._call('PhoneIoT', 'getLevel', { 'device': device, 'id': id })
    def set_level(self, device, id, value):
        '''
        Set the current value (a single number) of a value-like control.
        Currently, the only supported control is a slider, which sets the displayed value.
        
        Note that you can use this RPC even if the control is set to readonly mode (it's only readonly to the user).
        '''
        return self._client._call('PhoneIoT', 'setLevel', { 'device': device, 'id': id, 'value': value })
    def authenticate(self, device):
        '''
        This RPC simply checks that the connection to the device is still good.
        In particular, you can use this to check if the password is still valid.
        '''
        return self._client._call('PhoneIoT', 'authenticate', { 'device': device })
    def listen_to_gui(self, device):
        '''
        This RPC requests that you receive any events from the *Graphical User Interface* (GUI) on the phone's display.
        This is needed to receive any type of GUI event, including button clicks, joystick movements, and textbox update events.
        You only need to call this RPC once, which you can do at the start of your program (but after calling PhoneIoT.setCredentials).
        
        See the Display section for more information.
        '''
        return self._client._call('PhoneIoT', 'listenToGUI', { 'device': device })
    def listen_to_sensors(self, device, sensors=None):
        '''
        This RPC requests that you receive periodic sensor update events from the device.
        The sensors input is a list of pairs (lists of length 2), where each pair is a sensor name and an update period in milliseconds.
        You can have different update periods for different sensors.
        You will receive a message of the same name as the sensor at most once per whatever update period you specified.
        Any call to this RPC will invalidate all previous calls - thus, calling it with an empty list will stop all updates.
        
        This method of accessing sensor data is often easier, as it doesn't require loops or error-checking code.
        If a networking error occurs, you simply miss that single message.
        
        The PhoneIoT.getSensors RPC can be used to get a list of the valid sensor names.
        See the Sensors section for more information, esp. the required fields for each message type.
        '''
        return self._client._call('PhoneIoT', 'listenToSensors', { 'device': device, 'sensors': sensors })
    def get_sensors(self):
        '''
        This RPC returns a list containing the name of every sensor supported by PhoneIoT.
        Note that your specific device might not support all of these sensors, depending on the model.
        
        See Sensors for more information.
        '''
        return self._client._call('PhoneIoT', 'getSensors', {  })
    def set_credentials(self, device, password):
        '''
        This is the first RPC you should *always* call when working with PhoneIoT.
        It sets the login credentials (password) to use for all future interactions with the device.
        '''
        return self._client._call('PhoneIoT', 'setCredentials', { 'device': device, 'password': password })
    def is_pressed(self, device, id):
        '''
        Checks if the pressable control with the given ID is currently pressed.
        This can be used on any pressable control, which currently includes buttons, joysticks, and touchpads.
        
        By calling this RPC in a loop, you could perform some action every second while a button is held down.
        If you would instead like to receive click events, see the event optional parameter of PhoneIoT.addButton.
        '''
        return self._client._call('PhoneIoT', 'isPressed', { 'device': device, 'id': id })
    def get_toggle_state(self, device, id):
        '''
        Gets the toggle state of a toggleable control.
        This can be used on any toggleable control, such as toggles and radio buttons.
        '''
        return self._client._call('PhoneIoT', 'getToggleState', { 'device': device, 'id': id })
    def set_toggle_state(self, device, id, state):
        '''
        Sets the toggle state of a toggleable control with the given ID.
        This can be used on any toggleable control, such as toggles and radio buttons.
        If state is true, the toggleable becomes checked, otherwise it is unchecked.
        
        If used on a radio button, it sets the state independent of the control's group.
        That is, although the user can't select multiple radio buttons in the same group, you can do so programmatically through this RPC.
        '''
        return self._client._call('PhoneIoT', 'setToggleState', { 'device': device, 'id': id, 'state': state })
    def get_orientation(self, device):
        '''
        Gets the current output of the orientation sensor, relative to Earth's magnetic reference frame.
        This is given as a vector (list) with three angular components (in degrees):
        
        - azimuth (effectively the compass heading) [-180, 180]
        - pitch (vertical tilt) [-90, 90]
        - roll [-180, 180]
        
        If you are getting inconsistent values for the first (azimuth) angle,
        try moving and rotating your device around in a figure-8 to recalibrate it.
        
        Sensor name: orientation
        
        Message fields: x, y, z, heading, dir, cardinalDir, device
        '''
        return self._client._call('PhoneIoT', 'getOrientation', { 'device': device })
    def get_compass_heading(self, device):
        '''
        Gets the current compass heading from the device. This is similar to PhoneIoT.getBearing, except that it returns the angle from magnetic north, rather than the direction of travel.
        This is provided by the magnetic field sensor, so using this RPC on devices without a magnetometer will result in an error.
        The output of this RPC assumes the device is face-up.
        
        If you are getting inconsistent values, try moving and rotating your device around in a figure-8 to recalibrate it.
        
        Sensor name: orientation
        
        Message fields: x, y, z, heading, dir, cardinalDir, device
        '''
        return self._client._call('PhoneIoT', 'getCompassHeading', { 'device': device })
    def get_compass_direction(self, device):
        '''
        Returns the current compass direction of the device, which is one of N, NE, E, SE, S, SW, W, or NW.
        This is provided by the magnetic field sensor, so using this RPC on devices without a magnetometer will result in an error.
        The output of this RPC assumes the device is face-up.
        
        If you are getting inconsistent values, try moving and rotating your device around in a figure-8 to recalibrate it.
        
        Sensor name: orientation
        
        Message fields: x, y, z, heading, dir, cardinalDir, device
        '''
        return self._client._call('PhoneIoT', 'getCompassDirection', { 'device': device })
    def get_compass_cardinal_direction(self, device):
        '''
        Equivalent to PhoneIoT.getCompassDirection, except that it only returns N, E, S, or W.
        
        If you are getting inconsistent values, try moving and rotating your device around in a figure-8 to recalibrate it.
        
        Sensor name: orientation
        
        Message fields: x, y, z, heading, dir, cardinalDir, device
        '''
        return self._client._call('PhoneIoT', 'getCompassCardinalDirection', { 'device': device })
    def get_accelerometer(self, device):
        '''
        Gets the current output of the accelerometer sensor, if the device supports it.
        This is a vector representing the acceleration along the x, y, and z axes, relative to the device.
        When at rest, you can expect to measure the acceleration due to gravity.
        
        Sensor name: accelerometer
        
        Message fields: x, y, z, facingDir, device
        '''
        return self._client._call('PhoneIoT', 'getAccelerometer', { 'device': device })
    def get_facing_direction(self, device):
        '''
        Attempts to determine the general orientation of the device based on the accelerometer output.
        This represents which direction the face of the device's screen is pointing.
        The possible values are:
        
        - up - the device is face up
        - down - the device is face down
        - vertical - the device is upright
        - upside down - the device is vertical, but upside down
        - left - the device is horizontal, lying on its left side (when facing the screen)
        - right - the device is horizontal, lying on its right side (when facing the screen)
        
        Sensor name: accelerometer
        
        Message fields: x, y, z, facingDir, device
        '''
        return self._client._call('PhoneIoT', 'getFacingDirection', { 'device': device })
    def get_gravity(self, device):
        '''
        Attempts to get the gravity acceleration angle, divorced from any linear acceleration the device might be experiencing.
        For example, even if you start running, this vector should always have roughly the same value.
        This is provided by a hybrid sensor, and is not available on all devices.
        
        The counterpart to this RPC is PhoneIoT.getLinearAcceleration.
        
        Sensor name: gravity
        
        Message fields: x, y, z, device
        '''
        return self._client._call('PhoneIoT', 'getGravity', { 'device': device })
    def get_linear_acceleration(self, device):
        '''
        This RPC attempts to get the linear acceleration vector, divorced from the constant gravitational acceleration.
        Theoretically, if the device is at rest this RPC would report a nearly-zero vector (nothing is ever perfectly still).
        This is provided by a hybrid sensor, and is not available on all devices.
        
        The counterpart to this RPC is PhoneIoT.getGravity.
        
        Sensor name: linearAcceleration
        
        Message fields: x, y, z, device
        '''
        return self._client._call('PhoneIoT', 'getLinearAcceleration', { 'device': device })
    def get_gyroscope(self, device):
        '''
        Gets the current output of the gyroscope sensor, which measures rotational acceleration (in degress/s²) along the three axes of the device.
        
        Sensor name: gyroscope
        
        Message fields: x, y, z, device
        '''
        return self._client._call('PhoneIoT', 'getGyroscope', { 'device': device })
    def get_magnetic_field(self, device):
        '''
        Gets the current ouput of the magnetic field sensor, measured in μT (micro Tesla) along each axis of the device.
        This is provided by the magnetic field sensor, so using this RPC on devices without a magnetometer will result in an error.
        
        Notably, this RPC can be used as a compass (measuring Earth's magnetic field).
        
        Sensor name: magneticField
        
        Message fields: x, y, z, device
        '''
        return self._client._call('PhoneIoT', 'getMagneticField', { 'device': device })
    def get_microphone_level(self, device):
        '''
        Gets the current level (volume) of the microphone on the device.
        This is specified as a number where 0.0 denotes silence and 1.0 is the maximum volume the microphone can record.
        
        Sensor name: microphoneLevel
        
        Message fields: volume, device
        '''
        return self._client._call('PhoneIoT', 'getMicrophoneLevel', { 'device': device })
    def get_location(self, device):
        '''
        Gets the current location of the device, specified as latitude and longitude coordinates (in degrees).
        This is provided by the location service on the device, so you must have location turned on and give the app permission.
        
        Sensor name: location
        
        Message fields: latitude, longitude, bearing, altitude, device
        '''
        return self._client._call('PhoneIoT', 'getLocation', { 'device': device })
    def get_bearing(self, device):
        '''
        Returns the current bearing (direction of travel) from the device.
        This is provided by the location sensor, so you must have location turned on and give the app permission.
        The bearing is expressed as the angle (in degrees) from North, going clockwise.
        Thus, you can directly use this value in a point in direction block to point a sprite in the direction of travel (assuming North is up).
        
        Sensor name: location
        
        Message fields: latitude, longitude, bearing, altitude, device
        '''
        return self._client._call('PhoneIoT', 'getBearing', { 'device': device })
    def get_altitude(self, device):
        '''
        Returns the current altitude of the device, expressed in meters above sea level.
        This is provided by the location service on the device, so you must have location turned on and give the app permission.
        
        Sensor name: location
        
        Message fields: latitude, longitude, bearing, altitude, device
        '''
        return self._client._call('PhoneIoT', 'getAltitude', { 'device': device })
    def get_proximity(self, device):
        '''
        Gets the current output of the proximity (distance) sensor, measured in cm.
        Phones typically have this sensor for turning off the display when you put it to your ear, but tablets typically do not.
        In any case, the distances are not typically very long, and some devices only have binary (near/far) sensors.
        
        Sensor name: proximity
        
        Message fields: distance, device
        '''
        return self._client._call('PhoneIoT', 'getProximity', { 'device': device })
    def get_step_count(self, device):
        '''
        Gets the current step count from the device's step counter sensor.
        Not all devices have a step counter sensor, but you can manually emulate one by using the accelerometer.
        
        Sensor name: stepCount
        
        Message fields: count, device
        '''
        return self._client._call('PhoneIoT', 'getStepCount', { 'device': device })
    def get_light_level(self, device):
        '''
        Gets the current light level from the device.
        This is represented as a number with higher values being brighter.
        
        Sensor name: lightLevel
        
        Message fields: value, device
        '''
        return self._client._call('PhoneIoT', 'getLightLevel', { 'device': device })
    def get_image(self, device, id):
        '''
        Gets the displayed image of an image-like control with the given ID.
        This can be used on any control that displays images, which is currently only image displays.
        
        This can be used to retrieve images from the mobile device's camera, by having the user store an image in an image display that has readonly = false.
        See the readonly optional parameter of PhoneIoT.addImageDisplay.
        '''
        return self._client._call('PhoneIoT', 'getImage', { 'device': device, 'id': id })
    def set_image(self, device, id, img):
        '''
        Sets the displayed image of an image-like control with the given ID.
        This can be used on any control that displays images, which is currently only image displays.
        '''
        return self._client._call('PhoneIoT', 'setImage', { 'device': device, 'id': id, 'img': img })
class ProjectGutenberg:
    '''
    The Project Gutenberg service provides access to public domain books. For more information, check out https://project-gutenberg.org/.
    '''
    def __init__(self, client):
        self._client = client
    def get_text(self, id):
        '''
        Get the URL for the full text of a given book.
        '''
        return self._client._call('ProjectGutenberg', 'getText', { 'ID': id })
    def get_info(self, id):
        '''
        Get information about a given book including title and author.
        '''
        return self._client._call('ProjectGutenberg', 'getInfo', { 'ID': id })
    def search(self, field, text):
        '''
        Search for a book given title text and optional advanced options. Returns a list of up to 100 book IDs.
        '''
        return self._client._call('ProjectGutenberg', 'search', { 'field': field, 'text': text })
class PublicRoles:
    '''
    The PublicRoles Service provides access to the user's public role
    ID programmatically. This enables communication between projects.
    '''
    def __init__(self, client):
        self._client = client
    def get_public_role_id(self):
        '''
        Get the public role ID for the current role.
        '''
        return self._client._call('PublicRoles', 'getPublicRoleId', {  })
class RoboScape:

    def __init__(self, client):
        self._client = client
    def listen(self, robots):
        '''
        Registers for receiving messages from the given robots.
        '''
        return self._client._call('RoboScape', 'listen', { 'robots': robots })
    def get_robots(self):
        '''
        Returns the MAC addresses of all authorized robots.
        '''
        return self._client._call('RoboScape', 'getRobots', {  })
    def is_alive(self, robot):
        '''
        Returns true if the given robot is alive, sent messages in the
        last two seconds.
        '''
        return self._client._call('RoboScape', 'isAlive', { 'robot': robot })
    def set_speed(self, robot, left, right):
        '''
        Sets the wheel speed of the given robots.
        '''
        return self._client._call('RoboScape', 'setSpeed', { 'robot': robot, 'left': left, 'right': right })
    def set_led(self, robot, led, command):
        '''
        Sets one of the LEDs of the given robots.
        '''
        return self._client._call('RoboScape', 'setLed', { 'robot': robot, 'led': led, 'command': command })
    def beep(self, robot, msec, tone):
        '''
        Beeps with the speaker.
        '''
        return self._client._call('RoboScape', 'beep', { 'robot': robot, 'msec': msec, 'tone': tone })
    def infra_light(self, robot, msec, pwr):
        '''
        Turns on the infra red LED.
        '''
        return self._client._call('RoboScape', 'infraLight', { 'robot': robot, 'msec': msec, 'pwr': pwr })
    def get_range(self, robot):
        '''
        Ranges with the ultrasound sensor
        '''
        return self._client._call('RoboScape', 'getRange', { 'robot': robot })
    def get_ticks(self, robot):
        '''
        Returns the current number of wheel ticks (1/64th rotations)
        '''
        return self._client._call('RoboScape', 'getTicks', { 'robot': robot })
    def drive(self, robot, left, right):
        '''
        Drives the whiles for the specified ticks.
        '''
        return self._client._call('RoboScape', 'drive', { 'robot': robot, 'left': left, 'right': right })
    def set_total_rate(self, robot, rate):
        '''
        Sets the total message limit for the given robot.
        '''
        return self._client._call('RoboScape', 'setTotalRate', { 'robot': robot, 'rate': rate })
    def set_client_rate(self, robot, rate, penalty):
        '''
        Sets the client message limit and penalty for the given robot.
        '''
        return self._client._call('RoboScape', 'setClientRate', { 'robot': robot, 'rate': rate, 'penalty': penalty })
    def send(self, robot, command):
        '''
        Sends a textual command to the robot
        '''
        return self._client._call('RoboScape', 'send', { 'robot': robot, 'command': command })
class ServiceCreation:
    '''
    The ServiceCreation Service enables users to create custom services. Custom
    Services can be found under the "Community" section using the call <RPC>
    block.
    '''
    def __init__(self, client):
        self._client = client
    def get_create_from_table_options(self, data):
        '''
        Get the default settings for a given dataset.
        '''
        return self._client._call('ServiceCreation', 'getCreateFromTableOptions', { 'data': data })
    def create_service_from_table(self, name, data, options=None):
        '''
        Create a service using a given dataset.
        '''
        return self._client._call('ServiceCreation', 'createServiceFromTable', { 'name': name, 'data': data, 'options': options })
    def delete_service(self, name):
        '''
        Delete an existing service.
        '''
        return self._client._call('ServiceCreation', 'deleteService', { 'name': name })
class SimpleHangman:
    '''
    The SimpleHangman Service provides RPCs for playing single player hangman.
    The service will choose a word for the player to guess using the given RPCs.
    '''
    def __init__(self, client):
        self._client = client
    def restart(self, word=None):
        '''
        Restart the current game.
        '''
        return self._client._call('SimpleHangman', 'restart', { 'word': word })
    def get_currently_known_word(self):
        '''
        Get the current word with where unknown letters are replaced with "_".
        '''
        return self._client._call('SimpleHangman', 'getCurrentlyKnownWord', {  })
    def guess(self, letter):
        '''
        Guess a letter in the current word.
        '''
        return self._client._call('SimpleHangman', 'guess', { 'letter': letter })
    def is_word_guessed(self):
        '''
        Check if the current word has been guessed correctly.
        '''
        return self._client._call('SimpleHangman', 'isWordGuessed', {  })
    def get_wrong_count(self):
        '''
        Get the current number of incorrect guesses.
        '''
        return self._client._call('SimpleHangman', 'getWrongCount', {  })
class Smithsonian:
    '''
    The Smithsonian Service provides access to the Smithsonan open-access EDAN database,
    containing catalogued information on millions of historical items.
    '''
    def __init__(self, client):
        self._client = client
    def search(self, term, count=None, skip=None):
        '''
        Search and return a list of up to count items that match the search term.
        Because there may be a large number of matching items, you can also provide a number of items to skip.
        
        Each item in the returned array is structured data about that matching item.
        The fields for this data include:
        
        - id - the id of the matching item, needed by Smithsonian.getImage.
        - title - the title/name of the matching item
        - types - a list of categories the item falls under (e.g., Vases, Paintings)
        - authors - a list of authors/creators of the item or digitized version
        - topics - a list of topic names for the item (e.g., Anthropology, Ethnology)
        - notes - a list of extra notes about the object, in no particular organization
        - physicalDescription - a list of pairs of [label, content] regarding the physical description of the object
        - sources - a list of pairs of [label, content] describing the source of the item or digitization
        - hasImage - true if the image is listed as having image content in the database. Only items with this field being true can expect Smithsonian.getImage to succeed.
        
        If you would like to search for only items which have image content available,
        you can perform manual filtering on the hasImage field of the results,
        or you can use Smithsonian.searchImageContent, which does the same thing for you.
        '''
        return self._client._call('Smithsonian', 'search', { 'term': term, 'count': count, 'skip': skip })
    def search_image_content(self, term, count=None, skip=None):
        '''
        Equivalent to Smithsonian.search except that only images with image content (hasImage = true) are returned.
        
        The filtering of returned matches is done after pulling data from the database.
        Thus, you should treat count as the max number of *unfiltered* items to return,
        and similarly skip as the number of *unfiltered* items to skip.
        '''
        return self._client._call('Smithsonian', 'searchImageContent', { 'term': term, 'count': count, 'skip': skip })
    def get_image(self, id):
        '''
        Get an image associated with the given object, if available.
        This requires the id of the object, as provided by Smithsonian.search or Smithsonian.searchImageContent.
        '''
        return self._client._call('Smithsonian', 'getImage', { 'id': id })
class StarMap:
    '''
    The StarMap Service provides access to astronomy data using Sloan Digital Sky Survey.
    For more information, check out http://skyserver.sdss.org/dr14/en/home.aspx
    '''
    def __init__(self, client):
        self._client = client
    def arc_hour_min_sec_to_deg(self, arc_hour, arc_min, arc_sec):
        '''
        Convert arc to degree.
        '''
        return self._client._call('StarMap', 'arcHourMinSecToDeg', { 'arcHour': arc_hour, 'arcMin': arc_min, 'arcSec': arc_sec })
    def find_object(self, name):
        '''
        Search for significant object in the sky.
        '''
        return self._client._call('StarMap', 'findObject', { 'name': name })
    def get_image(self, right_ascension, declination, arcseconds_per_pixel, options, width=None, height=None):
        '''
        Get an image of the sky at the given coordinates.
        '''
        return self._client._call('StarMap', 'getImage', { 'right_ascension': right_ascension, 'declination': declination, 'arcseconds_per_pixel': arcseconds_per_pixel, 'options': options, 'width': width, 'height': height })
class Thingspeak:
    '''
    The ThingSpeak Service provides access to the ThingSpeak IoT analytics platform.
    For more information, check out https://thingspeak.com/.
    
    Terms of use: https://thingspeak.com/pages/terms
    '''
    def __init__(self, client):
        self._client = client
    def search_by_tag(self, tag, limit=None):
        '''
        Search for ThingSpeak channels by tag.
        '''
        return self._client._call('Thingspeak', 'searchByTag', { 'tag': tag, 'limit': limit })
    def search_by_location(self, latitude, longitude, distance=None, limit=None):
        '''
        Search for channels by location.
        '''
        return self._client._call('Thingspeak', 'searchByLocation', { 'latitude': latitude, 'longitude': longitude, 'distance': distance, 'limit': limit })
    def search_by_tag_and_location(self, tag, latitude, longitude, distance=None, limit=None):
        '''
        Search for channels by tag and location.
        '''
        return self._client._call('Thingspeak', 'searchByTagAndLocation', { 'tag': tag, 'latitude': latitude, 'longitude': longitude, 'distance': distance, 'limit': limit })
    def channel_feed(self, id, num_result):
        '''
        Get channel feed.
        '''
        return self._client._call('Thingspeak', 'channelFeed', { 'id': id, 'numResult': num_result })
    def private_channel_feed(self, id, num_result, api_key):
        '''
        Request data from a private channel
        '''
        return self._client._call('Thingspeak', 'privateChannelFeed', { 'id': id, 'numResult': num_result, 'apiKey': api_key })
    def channel_details(self, id):
        '''
        Get various details about the channel, including location, fields, tags and name.
        '''
        return self._client._call('Thingspeak', 'channelDetails', { 'id': id })
class ThisXDoesNotExist:
    '''
    This service uses Artificial Intelligence (AI) to make random, realistic images.
    For a list of example websites, see https://thisxdoesnotexist.com/.
    These are typically made by a Generative Adversarial neural Network (GAN).
    Put simply, this involves two AIs: one to make images and another to guess if they're real or fake, and making them compete to mutually improve.
    For more information, see https://en.wikipedia.org/wiki/Generative_adversarial_network.
    '''
    def __init__(self, client):
        self._client = client
    def get_person(self):
        '''
        Gets an image of a person that does not exist
        '''
        return self._client._call('ThisXDoesNotExist', 'getPerson', {  })
    def get_cat(self):
        '''
        Gets an image of a cat that does not exist
        '''
        return self._client._call('ThisXDoesNotExist', 'getCat', {  })
    def get_horse(self):
        '''
        Gets an image of a horse that does not exist
        '''
        return self._client._call('ThisXDoesNotExist', 'getHorse', {  })
    def get_artwork(self):
        '''
        Gets an image of an artwork that does not exist
        '''
        return self._client._call('ThisXDoesNotExist', 'getArtwork', {  })
    def get_waifu(self):
        '''
        Gets an image of a waifu that does not exist
        '''
        return self._client._call('ThisXDoesNotExist', 'getWaifu', {  })
    def get_fursona(self):
        '''
        Gets an image of a fursona that does not exist
        '''
        return self._client._call('ThisXDoesNotExist', 'getFursona', {  })
    def get_pony(self):
        '''
        Gets an image of a pony that does not exist
        '''
        return self._client._call('ThisXDoesNotExist', 'getPony', {  })
    def get_home_interior(self):
        '''
        Gets an image of a home interior that does not exist
        '''
        return self._client._call('ThisXDoesNotExist', 'getHomeInterior', {  })
    def get_congress_person(self):
        '''
        Gets an image of a congress person that does not exist
        '''
        return self._client._call('ThisXDoesNotExist', 'getCongressPerson', {  })
class Traffic:
    '''
    The Traffic Service provides access to real-time traffic data using the Bing Traffic API.
    For more information, check out https://msdn.microsoft.com/en-us/library/hh441725.aspx
    '''
    def __init__(self, client):
        self._client = client
    def search(self, west_longitude, north_latitude, east_longitude, south_latitude):
        '''
        Search for traffic accidents in a given region. Results are sent as messages in the format:
        
        Message type: Traffic
        fields: latitude, longitude, type
        '''
        return self._client._call('Traffic', 'search', { 'westLongitude': west_longitude, 'northLatitude': north_latitude, 'eastLongitude': east_longitude, 'southLatitude': south_latitude })
    def stop(self):
        '''
        Stop any pending requested messages (search results).
        '''
        return self._client._call('Traffic', 'stop', {  })
class Translation:
    '''
    Uses Microsoft's Azure Cognitive Services API to translate text.
    For more information, check out https://azure.microsoft.com/en-us/pricing/details/cognitive-services/translator-text-api/.
    
    Terms of use: https://www.microsoft.com/en-us/servicesagreement
    '''
    def __init__(self, client):
        self._client = client
    def translate(self, text, to, _from=None):
        '''
        Translate text between languages
        '''
        return self._client._call('Translation', 'translate', { 'text': text, 'to': to, 'from': _from })
    def to_english(self, text):
        '''
        Translate text to English
        '''
        return self._client._call('Translation', 'toEnglish', { 'text': text })
    def detect_language(self, text):
        '''
        Attempt to detect language of input text
        '''
        return self._client._call('Translation', 'detectLanguage', { 'text': text })
    def get_supported_languages(self):
        '''
        Attempt to detect language of input text
        '''
        return self._client._call('Translation', 'getSupportedLanguages', {  })
class Trivia:
    '''
    The Trivia Service provides access to trivia questions using the jservice API.
    For more information, check out https://jservice.io.
    '''
    def __init__(self, client):
        self._client = client
    def get_random_question(self):
        '''
        Get a random trivia question.
        This includes the question, answer, and additional information.
        '''
        return self._client._call('Trivia', 'getRandomQuestion', {  })
class TwentyQuestions:
    '''
    The TwentyQuestions Service aids in the creation of a multiplayer
    game of twenty questions.
    '''
    def __init__(self, client):
        self._client = client
    def start(self, answer):
        '''
        Start a new game of twenty questions.
        '''
        return self._client._call('TwentyQuestions', 'start', { 'answer': answer })
    def guess(self, guess):
        '''
        Guess the word or phrase.
        '''
        return self._client._call('TwentyQuestions', 'guess', { 'guess': guess })
    def answer(self, answer):
        '''
        Answer a yes or no question about the secret word or phrase.
        '''
        return self._client._call('TwentyQuestions', 'answer', { 'answer': answer })
    def game_started(self):
        '''
        Check if the game has been started.
        '''
        return self._client._call('TwentyQuestions', 'gameStarted', {  })
    def restart(self):
        '''
        Restart the game.
        '''
        return self._client._call('TwentyQuestions', 'restart', {  })
class Twitter:
    '''
    The Twitter Service provides access to posts and profile information from Twitter.
    For more information, check out https://twitter.com.
    
    Terms of use: https://twitter.com/en/tos
    '''
    def __init__(self, client):
        self._client = client
    def recent_tweets(self, screen_name, count):
        '''
        Get tweets from a user
        '''
        return self._client._call('Twitter', 'recentTweets', { 'screenName': screen_name, 'count': count })
    def followers(self, screen_name):
        '''
        Get the number of users following someone on Twitter
        '''
        return self._client._call('Twitter', 'followers', { 'screenName': screen_name })
    def tweets(self, screen_name):
        '''
        Get the number of tweets someone has made on Twitter
        '''
        return self._client._call('Twitter', 'tweets', { 'screenName': screen_name })
    def search(self, keyword, count):
        '''
        Searches the most recent tweets
        '''
        return self._client._call('Twitter', 'search', { 'keyword': keyword, 'count': count })
    def tweets_per_day(self, screen_name):
        '''
        Get how many tweets per day the user averages (most recent 200)
        '''
        return self._client._call('Twitter', 'tweetsPerDay', { 'screenName': screen_name })
    def favorites(self, screen_name, count):
        '''
        Get the most recent tweets that a user has favorited
        '''
        return self._client._call('Twitter', 'favorites', { 'screenName': screen_name, 'count': count })
    def favorites_count(self, screen_name):
        '''
        Get the number of favorites someone has on Twitter
        '''
        return self._client._call('Twitter', 'favoritesCount', { 'screenName': screen_name })
class WaterWatch:
    '''
    The WaterWatch Service provides access to real-time water data.
    For more information, check out https://waterservices.usgs.gov/
    '''
    def __init__(self, client):
        self._client = client
    def gage_height(self, min_latitude, max_latitude, min_longitude, max_longitude):
        '''
        Get the water data for sites within a bounding box.
        For help interpreting this data, see https://help.waterdata.usgs.gov/tutorials/surface-water-data/how-do-i-interpret-gage-height-and-streamflow-values
        '''
        return self._client._call('WaterWatch', 'gageHeight', { 'minLatitude': min_latitude, 'maxLatitude': max_latitude, 'minLongitude': min_longitude, 'maxLongitude': max_longitude })
    def stream_flow(self, min_latitude, max_latitude, min_longitude, max_longitude):
        '''
        Get stream flow data for sites within a bounding box.
        For help interpreting this data, see https://help.waterdata.usgs.gov/tutorials/surface-water-data/how-do-i-interpret-gage-height-and-streamflow-values
        '''
        return self._client._call('WaterWatch', 'streamFlow', { 'minLatitude': min_latitude, 'maxLatitude': max_latitude, 'minLongitude': min_longitude, 'maxLongitude': max_longitude })
    def water_temp(self, min_latitude, max_latitude, min_longitude, max_longitude):
        '''
        Get the water temperature data for sites within a bounding box.
        '''
        return self._client._call('WaterWatch', 'waterTemp', { 'minLatitude': min_latitude, 'maxLatitude': max_latitude, 'minLongitude': min_longitude, 'maxLongitude': max_longitude })
    def stop(self):
        '''
        Stop sending messages from this service.
        '''
        return self._client._call('WaterWatch', 'stop', {  })
class Weather:
    '''
    The Weather Service provides access to real-time weather data using OpenWeatherMap.
    For more information, check out https://openweathermap.org/.
    
    Terms of Service: https://openweathermap.org/terms
    '''
    def __init__(self, client):
        self._client = client
    def temperature(self, latitude, longitude):
        '''
        Get the current temperature for a given location.
        '''
        return self._client._call('Weather', 'temperature', { 'latitude': latitude, 'longitude': longitude })
    def humidity(self, latitude, longitude):
        '''
        Get the current humidity for a given location.
        '''
        return self._client._call('Weather', 'humidity', { 'latitude': latitude, 'longitude': longitude })
    def description(self, latitude, longitude):
        '''
        Get a short description of the current weather for a given location.
        '''
        return self._client._call('Weather', 'description', { 'latitude': latitude, 'longitude': longitude })
    def wind_speed(self, latitude, longitude):
        '''
        Get the current wind speed for a given location.
        '''
        return self._client._call('Weather', 'windSpeed', { 'latitude': latitude, 'longitude': longitude })
    def wind_angle(self, latitude, longitude):
        '''
        Get the current wind direction for a given location.
        '''
        return self._client._call('Weather', 'windAngle', { 'latitude': latitude, 'longitude': longitude })
    def icon(self, latitude, longitude):
        '''
        Get a small icon of the current weather for a given location.
        '''
        return self._client._call('Weather', 'icon', { 'latitude': latitude, 'longitude': longitude })