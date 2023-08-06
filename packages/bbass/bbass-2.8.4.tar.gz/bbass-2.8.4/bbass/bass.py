import os
import re
import asyncio 
import bbass.helpers
import chrome_bookmarks as cbook



class Song:
	def __init__(self, name, link):
		self._link = link
		self._name = name
		self._path = None

	@property
	def name(self):
		p1 = re.compile('- YouTube')
		p2 = re.compile(r'\(+\d+\)')
		self._name = helpers.dispose(helpers.reduce_spaces(self._name), p1, p2)
		return self._name
	
	@property
	def link(self):
		# restore the URL from YouTube playlist or video.
		return self._link.split('&', 1)[0]

	@property
	def id(self):
		# https://www.youtube.com/watch?v=k1uUIJPD0Nk -> k1uUIJPD0Nk
		return self.link.split('youtube.com/watch?v=')[-1]
	
	@property
	def command(self):
		return f'cd "{self.path}" && youtube-dl {self.link} --extract-audio --audio-format "mp3" --audio-quality 0 -o "%(title)s.%(ext)s"'

	@property
	def path(self):
		# can't set the path (only when attempt to download).
		return self._path if (self._path and os.path.exists(self._path)) else os.getcwd()

	def is_valid(self):
		return 'youtube.com/watch?v=' in self.link and len(self.id) >= 11

	async def download(self, path=None, force=False, **kwargs):
		self._path = path
		if helpers.present(self.path, self.name + '.mp3'):
			return None
		await asyncio.create_subprocess_shell(self.command)



class Folder:
	def __init__(self, name):
		self.name = name

	def exists(self):
		return any(self.bookmarks)

	def unique(self):
		return [folder.name for folder in cbook.folders].count(self.name) == 1

	@property
	def bookmarks(self):
		bookmarks_list = [folder for folder in cbook.folders if folder.name == self.name]
		exists = any(bookmarks_list)
		return iter() if not exists else filter(lambda book: book['type'] == 'url', bookmarks_list[0]['children'])
	


class Playlist(Folder):
	def __init__(self, name):
		super(Playlist, self).__init__(name)
		self._links = None

	@property
	def songs(self):
		folder_bookmarks = map(lambda song: Song(name=song['name'], link=song['url']), self.bookmarks)
		valid_songs = filter(lambda song: song.is_valid(), folder_bookmarks)

		non_overlapping_songs = []

		for song in valid_songs:
			if song.link not in non_overlapping_songs:
				non_overlapping_songs.append(song.link)
				yield song

	@property
	def links(self):
		return map(lambda song: song.link, self.songs)

	@property
	def names(self):
		return map(lambda song: song.name, self.songs)

	@property
	def commands(self):
		return map(lambda song: song.command, self.songs)

	@property
	def ids(self):
		return map(lambda song: song.id, self.songs)

	def exists(self):
		return any(self.songs)

	async def download(self, path=None):
		await asyncio.gather(*map(lambda song: song.download(path), self.songs))
