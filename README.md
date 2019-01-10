# Angelbot (of HYPERDEATH)

Discord/Matrix bot for _[The Studio](https://aliceos.app/studio/)_

![Angelbot icon](https://cdn.discordapp.com/app-icons/474592037988204556/fdfed4f7c373edb1f764b26b2665350e.png?size=128)

**Angelbot** is the Discord bot for Project Alice's Studio, responsible for greeting users, starting conversation, and informing users of upcoming updates. Angelbot is written in Python and uses `discord.py`, `matrix_client`, and `Chatterbot`.

## Build/Install Instructions

Angelbot works on Python 3.5 or higher. To install any required packages, run `pip install -r requirements.txt`.

You'll need to make sure that you have the following:

- A Matrix account and the access token to that account
- Discord bot key (Bot token)

Run the following commands to start the Angelbot server:

```bash
export BOT_KEY=<Discord bot key>
export MATRIX_USERNAME=<matrix username without "@" or ":matrix.org">
export MATRIX_TOKEN=<matrix access token>
python bot.py
```

> If you are using an app service like Heroku, you can skip the `export` commands and use the Environment Variables section of the provider instead.

> This repository is also built to run on Heroku, so you won't need to worry about setting up the Procfile or the buildpack.

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
