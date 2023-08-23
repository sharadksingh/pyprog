import tempfile
#import commands
import os

#commandname = "cat"

f = tempfile.NamedTemporaryFile(delete=False)
f.write("oh hello there")
f.close() # file is not immediately deleted because we
          # used delete=False

res = commands.getoutput("%s %s" % (commandname,f.name))
print(res)

os.unlink(f.name)
