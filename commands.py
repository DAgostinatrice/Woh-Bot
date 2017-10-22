from util import *

class WCommand():
    """Class that contains every command Woh Bot has."""
    def __init__(self, client, message):
        """Keyword arguments:
        client -- discord.Client()
        message -- discord.Message()"""
        self.client = client
        self.message = message

    def _getCmd(self, p_cmdName):
        """Returns the command from a
        message's content.
        
        Keyword arguments:
        p_cmdName -- function name/command name"""
        return self.message.content[:len(PREFIX + p_cmdName)]

    def _remCmd(self, p_cmdName):
        """Returns the content of a message
        without the start of the command.
        
        Keyword arguments:
        p_cmdName -- function name/command name"""
        return self.message.content[len(PREFIX + p_cmdName):]

    def cmdCalled(self, p_cmdName):
        """Returns True if the message's command
        is equivalent to a command name, ignoring
        character case.
        Returns False otherwise.
        
        Keyword arguments:
        p_cmdName -- function name/command name"""
        msgCmd = str(self._getCmd(p_cmdName))
        cmd = str(PREFIX + p_cmdName)
        if msgCmd.lower() == cmd.lower():
            return True
        return False

    ####################
    # COMMANDS SECTION #
    ####################
    async def woh(self, p_isDisabled = False):
        """Sends you the list of commands."""
        if p_isDisabled:
            return

        if self.cmdCalled(self.woh.__name__):
            finalHelpMessage = HelpMessage # Normal
            if IsAdminUser(m_AdminUserList, self.message.author.id): # Admin
               finalHelpMessage += AdminHelpMessage

            if IsMe(self.message.author.id): # Owner
                finalHelpMessage += AdminHelpMessage + OwnerHelpMessage
            
            await self.client.send_message(self.message.author, finalHelpMessage)

    async def openTV(self, p_isDisabled = False):
        """Opens TeamViewer and closes it after x seconds."""
        if p_isDisabled:
            return

        if self.cmdCalled(self.openTV.__name__):
            if IsMe(self.message.author.id):
                if platform.system() == 'Windows':
                    proc = Popen(WindowsCmdOpenTV(), shell=True) # Opens TeamViewer.exe
                    await self.client.send_message(self.message.channel, "Opening TeamViewer...\nTeamViewer will maybe close in {0} seconds.".format(SECONDS_TV))
                    await asyncio.sleep(SECONDS_TV)
                    proc.kill() # Closes TeamViewer.exe
                    #await client.send_message(message.channel, "Closing TeamViewer...")
                    return

                if platform.system() == 'Linux':
                    proc = Popen(LinuxCmdOpenTV(), shell=True) # Opens TeamViewer.exe
                    await self.client.send_message(self.message.channel, "Opening TeamViewer...\nTeamViewer will maybe close in {0} seconds.".format(SECONDS_TV))
                    await asyncio.sleep(SECONDS_TV)
                    proc.kill() # Closes TeamViewer.exe
                    #await client.send_message(message.channel, "Closing TeamViewer...")
                    return

                await self.client.send_message(self.message.channel, "**ERROR, host PC is not a Windows or Linux OS**")

    async def town(self, p_isDisabled = False):
        """Population of the town. Woh's Server only."""
        if p_isDisabled:
            return

        if self.cmdCalled(self.town.__name__):
            if self.message.server.id == MyServer():
                command = self._remCmd(self.town.__name__)
                if len(command) != 0:
                    msg = "Shut the Fuck Up Town\nPopulation: {}".format(command)
                    await self.client.send_message(self.message.channel, msg)
                    await self.client.delete_message(self.message)

    async def city(self, p_isDisabled = False):
        """Population of the city. Woh's Server only."""
        if p_isDisabled:
            return

        if self.cmdCalled(self.city.__name__):
            if self.message.server.id == MyServer():
                command = self._remCmd(self.city.__name__)
                if len(command) != 0:
                    msg = "Gotem City\nPopulation: {}".format(command)
                    await self.client.send_message(self.message.channel, msg)
                    await self.client.delete_message(self.message)

    async def listAllUserBD(self, p_isDisabled = False):
        """Lists the entire birthday list."""
        if p_isDisabled:
            return

        if self.cmdCalled(self.listAllUserBD.__name__):
            if IsMe(self.message.author.id):
                if len(m_UserBDList) != 0:
                    head = ["Name", "Birthday(mm-dd)", "User ID"]
                    comboList = []
                    for userBd in m_UserBDList:
                        member = ObtainMemberInfo(m_MemberList, userBd.userId, "mb", "")
                        comboList.append([member.name, userBd.bd, member.id])
                        if len(comboList) == 10:
                            fullMessage = CodeFormat(tabulate(comboList, headers=head, tablefmt="fancy_grid"), "")
                            await self.client.send_message(self.message.author, fullMessage)
                            del comboList
                    if len(comboList) != 0 or comboList is not None:
                        fullMessage = CodeFormat(tabulate(comboList, headers=head, tablefmt="fancy_grid"), "")
                        await self.client.send_message(self.message.author, fullMessage)
                else: 
                    await self.client.send_message(self.message.author, "The list is empty.")

    async def listUserBD(self, p_isDisabled = False):
        """Lists everyone from my birthday list."""
        if p_isDisabled:
            return
        
        if self.cmdCalled(self.listUserBD.__name__):
            serverId = str(self.message.server.id)
            if len(m_UserBDList) != 0:
                for channelBD in m_ChannelBDList:
                    if channelBD.serverId == serverId:
                        comboList = []
                        for userBd in m_UserBDList:
                            if serverId == ObtainMemberInfo(m_MemberList, userBd.userId, "si", serverId):
                                name = ObtainMemberInfo(m_MemberList, userBd.userId, "na", "")
                                comboList.append([name, userBd.bd])
                            if len(comboList) == 10:
                                fullMessage = CodeFormat(tabulate(comboList, headers=["Name", "Birthday(mm-dd)"], tablefmt="fancy_grid"), "")
                                await self.client.send_message(self.message.author, fullMessage)
                                del comboList
                        if len(comboList) != 0 or comboList is not None:
                            fullMessage = CodeFormat(tabulate(comboList, headers=["Name", "Birthday(mm-dd)"], tablefmt="fancy_grid"), "")
                            await self.client.send_message(self.message.author, fullMessage)
            else: 
                await self.client.send_message(self.message.author, "The list is empty.")

    async def addUserBD(self, p_isDisabled = False):
        """Adds you to my birthday list."""
        if p_isDisabled:
            return

        if self.cmdCalled(self.addUserBD.__name__):
            for userBd in m_UserBDList:
                if ObtainMemberInfo(m_MemberList, str(message.author.id), "id", "") == userBd.userId:
                    await self.client.send_message(self.message.channel, "You're already in my list")
                    return
            bd = self._remCmd(self.addUserBD.__name__)
            userId = str(self.message.author.id)

            try:
                bdTest = datetime.strptime(bd, "%m-%d") # Verifying the date
            except ValueError:
                await self.client.send_message(self.message.channel, "**Invalid date**, make sure you entered a possible date.")
                return

            if not IsUserIdValid(m_MemberList, userId): # Supposed to always return true
                await client.send_message(message.channel, "**You're not in my list of Members**")
                return

            FileAddUserBD(m_UserBDList, userId, bd)
            await self.client.send_message(self.message.channel, "Added birthday.")

    async def removeUserBD(self, p_isDisabled = False):
        """Removes a user from my birthday list."""
        if p_isDisabled:
            return
                
        if self.cmdCalled(self.removeUserBD.__name__):
            userId = str(self.message.author.id)
            listIndex = 0 # Will be sent to FileRemoveUserBD
            for userBd in m_UserBDList:
                if userBd.userId == userId:
                    FileRemoveUserBD(m_UserBDList, listIndex)
                    await self.client.send_message(self.message.channel, "You are no longer in my birthday list.")
                    return
                listIndex += 1
            await self.client.send_message(self.message.channel, "Can't remove you if you're not in my list.")

    async def showChannelBD(self, p_isDisabled = False):
        """Shows the current channel used for birthday messages."""
        if p_isDisabled:
            return

        if self.cmdCalled(self.showChannelBD.__name__):
            if IsAdminUser(m_AdminUserList, self.message.author.id) or IsMe(self.message.author.id):
                for channelBD in m_ChannelBDList:
                    if channelBD.serverId == str(self.message.server.id):
                        msg = "I send birthday messages to {}.".format(ChannelFormat(channelBD.channelId))
                        await self.client.send_message(self.message.channel, msg)
                        return
                await self.client.send_message(self.message.channel, "I don't send birthday messages in this server.")

    async def addChannelBD(self, p_isDisabled = False):
        """Sets the channel for birthday messages."""
        if p_isDisabled:
            return

        if self.cmdCalled(self.addChannelBD.__name__):
            if IsAdminUser(m_AdminUserList, self.message.author.id) or IsMe(self.message.author.id):
                channelId = self._remCmd(self.addChannelBD.__name__)
                channelId = search("[0-9]{18}", channelId).group()
                if not IsChannelIdValid(m_ChannelList, channelId):
                    await self.client.send_message(self.message.channel, "**Invalid channel**, make sure you entered a real channel from this server.")
                    return
            
                for channelBD in m_ChannelBDList:
                    if channelBD.channelId == channelId:
                        msg = "**There's already a channel for birthday messages in this server**, delete the current one to change it."
                        await self.client.send_message(self.message.channel, msg)
                        return

                await self.client.send_message(self.message.channel, "I will now send birthday messages in {}.".format(ChannelFormat(channelId)))
                FileAddChannelBD(m_ChannelBDList, channelId, str(self.message.server.id))

    async def removeChannelBD(self, p_isDisabled = False):
        """Unsets the channel for birthday messages."""
        if p_isDisabled:
            return

        if self.cmdCalled(self.removeChannelBD.__name__):
            if IsAdminUser(m_AdminUserList, self.message.author.id) or IsMe(self.message.author.id):
                serverId = str(self.message.server.id)   
                listIndex = 0 # Will be sent to FileRemoveChannelBD
                for channelBD in m_ChannelBDList:
                    if channelBD.serverId == serverId:
                        FileRemoveChannelBD(m_ChannelBDList, listIndex)
                        await self.client.send_message(self.message.channel, "I will no longer send birthday messages in this server.")
                        return
                    listIndex += 1
                await self.client.send_message(self.message.channel, "There's no channel to remove.")

    async def listAdminUser(self, p_isDisabled = False):
        """Lists every admin user."""
        if p_isDisabled:
            return

        if self.cmdCalled(self.listAdminUser.__name__):
            if IsMe(self.message.author.id):
                serverId = str(self.message.server.id)
                if len(m_AdminUserList) != 0:
                    comboList = []
                    for adminUser in m_AdminUserList:
                        if serverId == ObtainMemberInfo(m_MemberList, adminUser, "si", serverId):
                            name = ObtainMemberInfo(m_MemberList, adminUser, "na", "")
                            comboList.append([name])
                        if len(comboList) == 10:
                            fullMessage = CodeFormat(tabulate(comboList, headers=["Name"], tablefmt="fancy_grid"), "")
                            await self.client.send_message(self.message.author, fullMessage)
                            del comboList
                    if len(comboList) != 0 or comboList is not None:
                        fullMessage = CodeFormat(tabulate(comboList, headers=["Name"], tablefmt="fancy_grid"), "")
                        await self.client.send_message(self.message.author, fullMessage)
                else: 
                    await self.client.send_message(self.message.author, "The list is empty.")

    async def addAdminUser(self, p_isDisabled = False):
        """Adds an admin user."""
        if p_isDisabled:
            return

        if self.cmdCalled(self.addAdminUser.__name__):
            if IsMe(self.message.author.id):
                userId = self._remCmd(self.addAdminUser.__name__)
                userId = search("[0-9]{18}", userId).group()
                if not IsUserIdValid(m_MemberList, userId):
                    await self.client.send_message(self.message.channel, "**Invalid user**, make sure you entered a real user from this server.")
                    return

                for adminUser in m_AdminUserList:
                    if ObtainMemberInfo(m_MemberList, userId, "id", "") == adminUser:
                        await self.client.send_message(self.message.channel, "The user is already an admin.")
                        return
                
                await self.client.send_message(self.message.channel, "Admin Added.".format(UserFormat(userId)))
                FileAddAdminUser(m_AdminUserList, userId)

    async def removeAdminUser(self, p_isDisabled = False):
        """Removes an admin user."""
        if p_isDisabled:
            return

        if self.cmdCalled(self.removeAdminUser.__name__):
            if IsMe(self.message.author.id):
                userId = self._remCmd(self.removeAdminUser.__name__)
                userId = re.search("[0-9]{18}", userId).group()
                if not IsUserIdValid(m_MemberList, userId):
                    await self.client.send_message(self.message.channel, "**Invalid user**, make sure you entered a real user from this server.")
                    return

                listIndex = 0
                for adminUser in m_AdminUserList:
                    if ObtainMemberInfo(m_MemberList, userId, "id", "") == adminUser:
                        FileRemoveAdminUser(m_AdminUserList, listIndex)
                        await self.client.send_message(self.message.channel, "Removed User Admin.")
                        return
                    listIndex += 1
                await self.client.send_message(self.message.channel, "Can't remove the user if he's not in the list.")
