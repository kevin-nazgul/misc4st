# coding=utf8
__author__ = 'kevinhuang'

import sublime, sublime_plugin
from xml.dom import minidom
from xml.dom.minidom import Node


class MiscMainCommand(sublime_plugin.TextCommand):
	def dispatchCommand(self, edit, expr):
		args = expr.split(' ')
		if len(args) <= 0: return

		if 'unindent_xml' == args[0]:
			self.unindentXml(edit)

	def remove_blanks(self, node):
		for x in node.childNodes:
			if x.nodeType == Node.TEXT_NODE:
				if x.nodeValue:
					x.nodeValue = x.nodeValue.strip()
			elif x.nodeType == Node.ELEMENT_NODE:
				self.remove_blanks(x)

	# 去除xml标签之间的空白
	def unindentXml(self, edit):
		regions = self.view.sel()
		for region in regions:
			rawStr = self.view.substr(region)
			xmlRoot = minidom.parseString(rawStr)
			rawStr = xmlRoot.toprettyxml(indent='\n', newl='\n')
			lines = rawStr.split('\n')
			rawStr = ''
			for line in lines:
				if not line.startswith('<?xml') and line.strip() != '':
					rawStr = rawStr + line.strip()
			self.view.replace(edit, region, rawStr)


	def run(self, edit, **args):
		def onDone(expr):
			self.dispatchCommand(edit, expr)

		if args['source'] == 'commands':
			self.dispatchCommand(edit, args['cmd_line'])
		else:
			self.view.window().show_input_panel('command: ', '', onDone, None, None)
