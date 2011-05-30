import phpserialize as phpd
""" Deserialises the php stuff and creates objects, not really... big... since there's this like, library... """

def deserialise(raw):
	return phpd.loads(raw)
