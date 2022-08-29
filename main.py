from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random

import convertLinks

Builder.load_file("design.kv")

class DisplayScreen(Screen):
    def spotifyToApple(self, link):
        
        newLink = convertLinks.spotifyToAppleLink(link)
        self.ids.appleMusic.text = newLink

    def appleToSpotify(self, link):
        
        newLink = convertLinks.appleToSpotifyLink(link)
        self.ids.spotify.text = newLink



class MyApp(App):

    def build(self):
        return DisplayScreen()


if __name__ == '__main__':
    MyApp().run()
