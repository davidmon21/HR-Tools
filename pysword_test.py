from pysword.modules import SwordModules
import pysword
import pysword_repo
import os

repodog = pysword_repo.PyswordRepo(swrdpath = os.path.join(os.getenv(u'HOME'), u'.sword'))
#repodog.initiate_repo()
#repodog.update_repo_list()
#repodog.download_repos()
#repodog.install_module('kjv.conf-kjv')
# if repodog.uninstall_module('kjv.conf-kjv_CUSTOMPATH'):
	# print("uninstalled")
# repodog.install_module('drc.conf-drc')
# if repodog.uninstall_module('drc.conf-drc_CUSTOMPATH'):
	# print("uninstalled")
# repodog.install_module('abu.conf-abu-beta')
# if repodog.uninstall_module('abu.conf-abu-beta'):
	# print("uninstalled")
# print(repodog.find_module('abu', beta=True))
# print(repodog.find_module('drc'))
# print(repodog.find_module('netfree',outdated=True))
# repodog.install_module('netfree.conf-netfree', outdated=True)
# if repodog.uninstall_module('netfree.conf-netfree'):
	# print("uninstalled")
# print(repodog.search_section_module("king james","about"))

# print(repodog.find_module('abu'))
#repodog.install_module('chrysostom.conf-chrysostom', preferzip=False)
#repodog.uninstall_module('drc.conf-drc')
#repodog.install_module('drc.conf-drc',preferzip=False)
# repodog.install_module('kjv.conf-kjv')
# print(repodog.find_module('abu', beta=True))
# print(repodog.find_module('drc'))
# print(repodog.find_module('netfree',outdated=True))
modules = SwordModules()
bible = modules.get_bible_from_module(u'd')
print(bible)
#print(bible.get(books=['john'], chapters=[3], verses=16))
