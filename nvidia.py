from adb import adb_commands
from adb.sign_pythonrsa import PythonRSASigner

class shield:
	buttons = { 
		'power': 'KEYCODE_POWER',
		'sleep': 'KEYCODE_SLEEP',
		'wake': 'KEYCODE_WAKEUP',
		'home': 'KEYCODE_HOME',
		'back': 'KEYCODE_BACK',
		'search': 'KEYCODE_SEARCH',
		'up': 'KEYCODE_DPAD_UP',
		'down': 'KEYCODE_DPAD_DOWN',
		'left': 'KEYCODE_DPAD_LEFT',
		'right': 'KEYCODE_DPAD_RIGHT',
		'center': 'KEYCODE_DPAD_CENTER',
		'volume up': 'KEYCODE_VOLUME_UP',
		'volume down': 'KEYCODE_VOLUME_DOWN',
		'rewind': 'KEYCODE_MEDIA_REWIND',
		'ff': 'KEYCODE_MEDIA_FAST_FORWARD',
		'play/pause': 'KEYCODE_MEDIA_PLAY_PAUSE',
		'previous': 'KEYCODE_MEDIA_PREVIOUS',
		'next': 'KEYCODE_MEDIA_NEXT',
	}

	apps = {
		'hbo': 'com.hbo.hbonow',
		'prime': 'com.amazon.amazonvideo.livingroom',
		'music': 'com.google.android.music',
		'youtube': 'com.google.android.youtube.tv',
		'ted':  'com.ted.android.tv',
		'hulu': 'com.hulu.livingroomplus',
		'netflix': 'com.netflix.ninja',
		'youtubetv': 'com.google.android.youtube.tvunplugged',
		'disney': 'com.disney.disneyplus',
		'kodi': 'org.xbmc.kodi',
		'twitch': 'tv.twitch.android.app',
		'vudu': 'air.com.vudu.air.DownloaderTablet',
		'plex': 'com.plexapp.android',
		'cbs': 'com.cbs.ott',
		'pbs': 'com.pbs.video',
		'amazonmusic': 'com.amazon.music.tv',
		'pandora': 'com.pandora.android.atv',
		'spotify': 'com.spotify.tv.android',
		'games': 'com.nvidia.tegrazone3'
	}

	launch_activities = {
		'hbo': 'com.hbo.go.LaunchActivity',
		'prime': 'com.amazon.ignition.IgnitionActivity',
		'music': '.tv.HomeActivity',
		'youtube': 'com.google.android.apps.youtube.tv.activity.ShellActivity',
		'ted':  '.view.MainActivity',
		'hulu': '.WKFactivity',
		'netflix': '.MainActivity',
		'youtubetv': 'com.google.android.apps.youtube.tvunplugged.activity.MainActivity',
		'disney': 'com.bamtechmedia.dominguez.main.MainActivity',
		'kodi': '.Splash',
		'twitch': 'tv.twitch.android.apps.TwitchActivity',
		'vudu': '.TvMainActivity',
		'plex': 'com.plexapp.plex.activities.SplashActivity',
		'cbs': 'com.cbs.app.tv.ui.activity.SplashActivity',
		'pbs': '.ui.main.activities.StartupActivity',
		'amazonmusic': '.activity.MainActivity',
		'pandora': 'com.pandora.android.MainActivity',
		'spotify': '.SpotifyTVActivity',
		'games': 'com.nvidia.tegrazone.leanback.LBMainActivity'
	}

	def __init__( self, ip = b'SHIELD:5555' ):
		if isinstance( ip, str ):
			ip = str.encode( ip )
		self.app_packages = { self.apps[key]: key for key in self.apps }
		self.shield_ip_and_port = ip
		self.connect()

	def connect( self ):
		signed_key = PythonRSASigner.FromRSAKeyPath( 'adbkey' )
		self.device = adb_commands.AdbCommands().ConnectDevice( serial=self.shield_ip_and_port, rsa_keys=[ signed_key ] )

	def shell( self, arg ):
		# Nvidia disconnects inactive debuggers so we reconnect and retry on failure
		for i in range(2):
			try:
				# Shell() appends a newline so we strip it
				return self.device.Shell( arg )[:-1]
			except ( ConnectionResetError, AttributeError ):
				self.connect()

	def press( self, button ):
		if button not in self.buttons:
			return { 'error': f'unknown button "{button}"'}

		self.shell( f'input keyevent {self.buttons[ button ]}' )

	def launch( self, app ):
		if app not in self.apps:
			return { 'error': f'no such app "{app}"' }
		activity = self._get_launch_activity( app )
		if not activity:
			return { 'error': f'no launch activity found for app "{app}"' }

		app_launch_activity = f'{self.apps[ app ]}/{activity}'
		return self.shell( f'am start -n {app_launch_activity}')

	def get_current_app( self ):
		app_activity = self.shell( 'dumpsys window windows | grep -E mCurrentFocus | sed -E "s/.*Window\{(.*)\}/\\1/" | cut -F 3' )
		app, _, activity = app_activity.partition("/")
		return app, activity or None, self.app_packages.get(app)

	def type( self, text ):
		return self.shell( "input text {text}" )

	def get_power( self ):
		return self.shell( 'dumpsys power 2> /dev/null | grep "mWakefulness=" | cut -d "=" -f 2' )

	def get_packages( self ):
		return self.shell( 'pm list packages -e -3 | cut -d":" -f2-' ).splitlines()

	def add_app( self, app, package ):
		self.apps[ app ] = package
		self.app_packages[ package ] = app

	def _get_launch_activity( self, app ):
		if app in self.launch_activities:
			return self.launch_activities[ app ]

		package = self.apps.get( app, None )

		if app and package:
			activity = self.shell( f'cmd package resolve-activity --brief {package} | tail -n 1 | cut -d"/" -f2-' )
			if activity and activity != 'No activity found':
				self.launch_activities[ app ] = activity
				return activity
