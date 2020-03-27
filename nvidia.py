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
		'hbo': 'com.hbo.hbonow/com.hbo.go.LaunchActivity',
		'prime': 'com.amazon.amazonvideo.livingroom/com.amazon.ignition.IgnitionActivity',
		'music': 'com.google.android.music/.tv.HomeActivity',
		'youtube': 'com.google.android.youtube.tv/com.google.android.apps.youtube.tv.activity.ShellActivity',
		'ted':  'com.ted.android.tv/.view.MainActivity',
                'hulu': 'com.hulu.livingroomplus/.WKFactivity',
                'netflix': 'com.netflix.ninja/.MainActivity',
                'youtubetv': 'com.google.android.youtube.tvunplugged/com.google.android.apps.youtube.tvunplugged.activity.MainActivity',
		'disney': 'com.disney.disneyplus/com.bamtechmedia.dominguez.main.MainActivity',
                'kodi': 'org.xbmc.kodi/.Splash',
                'twitch': 'tv.twitch.android.app/tv.twitch.android.apps.TwitchActivity',
                'vudu': 'air.com.vudu.air.DownloaderTablet/.TvMainActivity',
                'plex': 'com.plexapp.android/com.plexapp.plex.activities.SplashActivity',
		'cbs': 'com.cbs.ott/com.cbs.app.tv.ui.activity.SplashActivity',
		'pbs': 'com.pbs.video/.ui.main.activities.StartupActivity',
		'amazonmusic': 'com.amazon.music.tv/.activity.MainActivity',
		'pandora': 'com.pandora.android.atv/com.pandora.android.MainActivity',
		'spotify': 'com.spotify.tv.android/.SpotifyTVActivity',
		'games': 'com.nvidia.tegrazone3/com.nvidia.tegrazone.leanback.LBMainActivity'
	}

	def __init__( self, ip = b'SHIELD:5555' ):
		if isinstance( ip, str ):
			ip = str.encode( ip )
		self.shield_ip_and_port = ip
		self.connect()

	def connect( self ):
		signed_key = PythonRSASigner.FromRSAKeyPath( 'adbkey' )
		self.device = adb_commands.AdbCommands().ConnectDevice( serial=self.shield_ip_and_port, rsa_keys=[ signed_key ] )

	def shell( self, arg ):
		# Nvidia disconnects inactive debuggers so we reconnect and retry on failure
		for i in range(2):
			try:
				self.device.Shell( arg )
				return
			except ConnectionResetError:
				self.connect()

	def press( self, button ):
		if button not in self.buttons:
			return { 'error': f'unknown button "{button}"'}

		self.shell( f'input keyevent {self.buttons[ button ]}' )

	def launch( self, app ):
		if app not in self.apps:
			return { 'error': f'no such app "{app}"' }

		app_launch_activity = self.apps[ app ]
		self.shell( f'am start -n {app_launch_activity}')
