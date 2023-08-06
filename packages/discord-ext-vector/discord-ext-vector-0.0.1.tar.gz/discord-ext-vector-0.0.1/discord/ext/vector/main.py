import discord

from discord.ext import commands

class Colour(discord.Color):

    @classmethod
    def logo_blue(cls):
        """A factory method that returns a :class:`Colour` with a value of ``2F54FE``.
        """
        return cls(0x2F54FE)

    @classmethod
    def blurple(cls):
        """A factory method that returns a :class:`Colour` with a value of ``5865F2``.
        """
        return cls(0x5865F2)

    @classmethod
    def old_blurple(cls):

        """A factory method that returns a :class:`Colour` with a value of ``7289da``.
        """
        return discord.Color.blurple()

Color = Colour