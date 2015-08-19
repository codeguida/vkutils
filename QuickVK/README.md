## QuickVK

Tools for backup messaging, groups, liked posts and photos. Also allows to read and send messages directly from the terminal.

### Functions

**format(str, \*args, \*\*kw)** - similar to str.format() with the exception that automatically inserts color (dictionary formating).

**printMessages(messages)** - utility function.

**showDialogs(\*\*kw)** - reflecting a convenient way dialogues. Takes the same arguments as the vkapi.messages.getDialogs.

**showDialog(\*\*kw)** - reflecting the history of correspondence with the user in a convenient form. Takes the same arguments as the vkapi.messages.getHistory.

**sendMessage(\*\*kw)** - a convenient feature for sending messages. Takes the same arguments as the vkapi.messages.send, except the message - it is not mandatory, since messages can be entered after the function call.

**copyLiked(count=1, mode="posts")** - returns a list of liked posts (mode="posts") or photos (mode="photos") in length 100*count cells.

**copyGroups(count)** - similar to the previous one, but it works with groups.

**copyMessages(id, count, filename=None)** - retains the conversation with the user "id" in length 200\* count of elements in the file "filename" (default "<id> -messages.txt"). But the file will contain bad-reading data. Read this file in a convenient way by using the function **loadMessagees(filename)**
