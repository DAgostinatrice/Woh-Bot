from util import *
from cmdtemplate import Command

class addAdminUser(Command):
    """Adds an admin user."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_OWNER
    cmdArguments = " [user]"

    def getDoc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def moreHelp(self):
        return MORE_HELP_ADD_ADMIN_USER.format(self.__str__(), self.cmdArguments)

    async def command(self, p_message):
        """Actual Command"""
        if self.isDisabled:
            return

        if not self.cmdCalled(p_message, self.__str__()):
            return

        if not self.hasPermission(self.permissionLevel, p_message.author.id):
            return

        if HELP_COMMAND_PREFIX in p_message.content.lower():
            await self.client.send_message(p_message.author, self.moreHelp())
            return


        userId = self._remCmd(p_message, self.__str__())
        userId = search(ID_REGEX, userId).group()
        if not IsUserIdValid(self.client.get_all_members(), userId):
            await self.client.send_message(p_message.channel, INVALID_USER)
            return

        for adminUser in m_AdminUserList:
            if ObtainMemberInfo(self.client.get_all_members(), userId, "id", "") == adminUser:
                await self.client.send_message(p_message.channel, ADD_ADMIN_USER_ALREADY)
                return
                
        await self.client.send_message(p_message.channel, ADD_ADMIN_USER_SUCCESS.format(UserFormat(userId)))
        FileAddAdminUser(m_AdminUserList, userId)
