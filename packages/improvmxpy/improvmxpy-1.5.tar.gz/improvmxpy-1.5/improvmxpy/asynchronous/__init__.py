"""
Hello there!
You may ask why the fuck this code look so weird and ugly.
It is because black formatting ;-;
oops
"""

import aiohttp

import json

import sys


class WrongPatternToken(Exception):
	pass


class NoToken(Exception):
	pass


class TokenError(Exception):
	pass


class NoPermission(Exception):
	pass


class ServerError(Exception):
	pass


url = "https://api.improvmx.com/v3/"
global tokenauth
tokenauth = ""


class SetUp(object):
	def __init__(self, token=None, skipcon=False):
		global tokenauth
		if len(tokenauth) != 35 or len(tokenauth) == 0 or "sk_" not in token:
			print("Adding token")
			if token is None or len(token) == 0 or len(token) != 35:
				raise WrongPatternToken(
					"You have wrong token or You did'nt enter token."
				)
			tokenauth = token
			if skipcon:
				print(f"Your token is {tokenauth}\n Is this right?")
				an = input("Please answer\n Acxept answer yes/no\n").lower()
				if an == "yes":
					if sys.platform == "win32" or sys.platform == "win64":
						import os

						os.system("cls")
						pass
					else:
						import os

						os.system("clear")
		else:
			print("You already setup token!")


class Account(object):
	def __init__(self):
		global tokenauth
		if len(tokenauth) != 35:
			raise NoToken("We don't see any token that you input! You can do that by do call SetUp function")
		self.token = tokenauth

	async def GetAccountDetail(self):
		global tokenauth
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{url}account", auth=aiohttp.BasicAuth("api",self.token)):
				return await self.__CheckResponse(r)

	async def GetWhiteLabelDomain(self):
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{url}account/whitelabels", auth=aiohttp.BasicAuth("api",self.token)):
				return await self.__CheckResponse(r)

	async def __CheckResponse(self, r):
		global tokenauth
		if r.status_code == 401:
			tokenauth = ""
			raise TokenError("Your token is unusable! Please set new token again.")
		if r.status_code == 403:
			raise NoPermission(
				"You don't have enough permission to do this. You may need to subscribe pro or organization plan!"
			)
		if r.status_code == 500:
			raise ServerError(
				"Oops! The ImprovMX server is died or down or there's bug! Please try again later!"
			)
		return await r.json()


class Domains(object):
	def __init__(self):
		global tokenauth
		if len(tokenauth) != 35:
			raise NoToken("We don't see any token that you input! You can do that by call SetUp function!")
		self.token = tokenauth

	async def ListDomains(self, query: str = "", is_active: bool = "", limit=50, page=1):
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{url}domains?q={query}&is_active={is_active}&limit={limit}&page={page}",auth=aiohttp.BasicAuth("api",self.token)):
				return await self.__CheckResponse(r)

	async def AddDomain(self, domain: str, notify_email: str = "", whitelabel: str = ""):
		async with aiohttp.ClientSession() as session:
			async with session.post(f"{url}/domains",auth=aiohttp.BasicAuth("api",self.token),headers={"domain": domain,"notification_email": notify_email,"whitelabel": whitelabel}):
				return await self.__CheckResponse(r)

	async def DomainDetail(self, domain):
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{url}domains/{domain}", auth=aiohttp.BasicAuth("api",self.token)):
				return await self.__CheckResponse(r)

	async def EditDomain(self, domain: str, notify_email: str = "", whitelabel: str = ""):
		async with aiohttp.ClientSession() as session:
			async with session.put(f"{url}domains",auth=aiohttp.BasicAuth("api",self.token),headers={"notification_email": notify_email, "whitelabel": whitelabel},):
				return await self.__CheckResponse(r)

	async def DeleteDomain(self, domain):
		async with aiohttp.ClientSession() as session:
			async with session.delete(f"{url}domains/{domain}", auth=aiohttp.BasicAuth("api",self.token)):
				if json.loads(r.content.decode())["success"] is True:
					return True
				return False

	async def CheckMXDomain(self, domain: str):
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{url}domains/{domain}/check", auth=aiohttp.BasicAuth("api",self.token)):
				return await self.__CheckResponse(r)

	async def __CheckResponse(self, r):
		global tokenauth
		if r.status_code == 401:
			tokenauth = ""
			raise TokenError("Your token is unusable! Please set new token again.")
		if r.status_code == 403:
			raise NoPermission(
				"You don't have enough permission to do this. You may need to subscribe pro or organization plan!"
			)
		if r.status_code == 500:
			raise ServerError(
				"Oops! The ImprovMX server is died or down or there's bug! Please try again later!"
			)
		return await r.json()


class Aliases(object):
	def __init__(self):
		global tokenauth
		if len(tokenauth) != 35:
			raise NoToken(
				"We don't see any token that you input! You can do that by call SetUp function!"
			)
		self.token = tokenauth

	async def AliasDomainList(self, domain: str, q: str = "", is_active: bool = "", page: str = "1"):
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{url}domains/{domain}/aliases?q={q}&is_active={is_active}&page={page}",auth=aiohttp.BasicAuth("api",self.token),):
				return await self.__CheckResponse(r)

	async def AddNewAlias(self, domain, alias, forward):
		async with aiohttp.ClientSession() as session:
			async with session.post(f"{url}{domain}/aliases",auth=aiohttp.BasicAuth("api",self.token),headers={"alias": alias, "forward": forward},):
				return await self.__CheckResponse(r)

	async def GetDetailAlias(self, domain, alias):
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{url}domains/{domain}/aliases/{alias}", auth=aiohttp.BasicAuth("api",self.token)):
				return await self.__CheckResponse(r)

	async def UpdateAlias(self, domain, alias, forward):
		async with aiohttp.ClientSession() as session:
			async with session.put(f"{url}domains/{domain}/aliases/{alias}",headers={"forward": forward},auth=aiohttp.BasicAuth("api",self.token),):
				return await self.__CheckResponse(r)

	async def DeleteAlias(self, domain, alias):
		async with aiohttp.ClientSession() as session:
			async with session.delete(f"{url}domains/{domain}/aliases/{alias}", auth=aiohttp.BasicAuth("api",self.token)):
				return await self.__CheckResponse(r)

	async def __CheckResponse(self, r):
		global tokenauth
		if r.status_code == 401:
			tokenauth = ""
			raise TokenError("Your token is unusable! Please set new token again.")
		if r.status_code == 403:
			raise NoPermission(
				"You don't have enough permission to do this. You may need to subscribe pro or organization plan!"
			)
		if r.status_code == 500:
			raise ServerError(
				"Oops! The ImprovMX server is died or down or there's bug! Please try again later!"
			)
		return await r.json()


class Logging(object):
	def __init__(self):
		global tokenauth
		if len(tokenauth) != 35:
			raise NoToken(
				"We don't see any token that you input! You can do that by call SetUp function!"
			)
		self.token = tokenauth

	async def GetDomainLog(self, domain, logID=None):
		if logID is not None:
			async with aiohttp.ClientSession() as session:
				async with session.get(f"{url}domains/{domain}/logs",headers={"next_cursor": logID},auth=aiohttp.BasicAuth("api",self.token),):
					return await self.__CheckResponse(r)
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{url}domains/{domain}/logs", auth=aiohttp.BasicAuth("api",self.token)):
				return await self.__CheckResponse(r)

	async def GetAliasLog(self, domain, alias, logID=None):
		if logID is not None:
			async with aiohttp.ClientSession() as session:
				async with session.get(f"{url}domains/{domain}/logs/aliases/{alias}",headers={"next_cursor": logID},auth=aiohttp.BasicAuth("api",self.token),):
					return await self.__CheckResponse(r)
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{url}domains/{domain}/logs/aliases/{alias}", auth=aiohttp.BasicAuth("api",self.token)):
				return await self.__CheckResponse(r)

	async def __CheckResponse(self, r):
		global tokenauth
		if r.status_code == 401:
			tokenauth = ""
			raise TokenError("Your token is unusable! Please set new token again.")
		if r.status_code == 403:
			raise NoPermission(
				"You don't have enough permission to do this. You may need to subscribe pro or organization plan!"
			)
		if r.status_code == 500:
			raise ServerError(
				"Oops! The ImprovMX server is died or down or there's bug! Please try again later!"
			)
		return await r.json()


class SMTPCredential(object):
	def __init__(self):
		global tokenauth
		if len(tokenauth) != 35:
			raise NoToken(
				"We don't see any token that you input! You can do that by call SetUp function!"
			)
		self.token = tokenauth

	async def ListOfSMTPAccount(self, domain):
		async with aiohttp.ClientSession() as session:
			async with session.get(f"{url}domains/{domain}/credentials", auth=aiohttp.BasicAuth("api",self.token)):
				return await self.__CheckResponse(r)

	async def AddNewSMTPAccount(self, domain, username, password):
		async with aiohttp.ClientSession() as session:
			async with session.post(f"{url}domains/{domain}/credentials",auth=aiohttp.BasicAuth("api",self.token),headers={"username": username, "password": password},):
				return await self.__CheckResponse(r)

	async def ChangeSMTPUserPassword(self, domain, username, password):
		async with aiohttp.ClientSession() as session:
			async with session.put(f"{url}domains/{domain}/credentials/{username}",auth=aiohttp.BasicAuth("api",self.token),headers={"password": password},):
				return await self.__CheckResponse(r)

	async def DeleteSMTPUser(self, domain, username):
		async with aiohttp.ClientSession() as session:
			async with session.delete(f"{url}domains/{domain}/credentials/{username}",auth=aiohttp.BasicAuth("api",self.token)) as r:
				if await r.json()["success"] == True:
					return True
			return False

	async def __CheckResponse(self, r):
		global tokenauth
		if r.status_code == 401:
			tokenauth = ""
			raise TokenError("Your token is unusable! Please set new token again.")
		if r.status_code == 403:
			raise NoPermission(
				"You don't have enough permission to do this. You may need to subscribe pro or organization plan!"
			)
		if r.status_code == 500:
			raise ServerError(
				"Oops! The ImprovMX server is died or down or there's bug! Please try again later!"
			)
		return await r.json()