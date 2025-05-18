from html.parser import HTMLParser

class ExamplesReader(HTMLParser):
	def __init__(self, out_list, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.out_list = out_list
		self.state = []
	def handle_starttag(self, tag, attrs):
		self.state.append(tag)
	def handle_endtag(self, tag):
		last = None
		while last != tag:
			last = self.state.pop()
	def handle_data(self, data):
		if last[-2:] == ["pre", "code"]:
			self.out_list.append(data)
	def reset(self):
		self.state.clear()
		super().reset()
