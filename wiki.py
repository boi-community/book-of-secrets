# This plugin handles searching of the Binding of Isaac wiki.
import hikari
import lightbulb
import subprocess
import sys

import main

# Doing it this way since I really don't want to have people need to make a custom image just for a silly little plugin
try:
    import fandom
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fandom-py"])
    import fandom


def get_enabled_guilds():
    main.load_plugin_configs("wiki", plugin.d)
    return tuple(plugin.d["config"].keys())


plugin = lightbulb.Plugin("Wiki", include_datastore=True)


@plugin.command
@lightbulb.option("query", "Query to run against the wiki")
@lightbulb.command(
    "wiki", "Check the Isaac wiki for information", guilds=get_enabled_guilds()
)
@lightbulb.implements(lightbulb.SlashCommand)
async def wiki(ctx: lightbulb.Context) -> None:
    response = None
    page = None
    try:
        page = fandom.page(ctx.options.query)
    except fandom.error.PageError:
        search = fandom.search(ctx.options.query)

        if not search:
            response = "There is no page on the wiki matching this query, and I could not find any similar results. Please try a different query."
        else:
            response = f"There is no page on the wiki matching this query. I found a similar page called `{search[0][0]}`, though!"
            page = fandom.page(search[0][0])

    if page:
        await ctx.respond((response if response else "") + f"\n{page.url}")
    else:
        await ctx.respond(response)


def load(bot):
    bot.add_plugin(plugin)
    fandom.set_wiki("BindingOfIsaacRebirth")


def unload(bot):
    bot.remove_plugin(plugin)
