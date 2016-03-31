
from loopinf.game.game import Grid


field = Grid.load('../levels/10')


def show_accessible_count(field):
	parts = ['  ']
	for m in range(len(field.cells[0])):
		parts.append('{0:2d}'.format(m))
	parts.append('\n')
	for k, row in enumerate(field.cells):
		parts.append('{0:2d} '.format(k))
		for cell in row:
			if cell.is_empty() == 1:
				parts.append('  ')
			else:
				parts.append(str(len(cell.accessible)) + ' ')
		parts.append('\n')
	return ''.join(parts[:-1])


""" Store available states on each cell. """
print(field)
for k, m, cell in field:
	cell.accessible = set()
	for n in range(4):
		cell.turn_right()
		cell.accessible.add(cell.to_int())

""" Remove inaccessible states. """
def has_dir(cell, dirname):
	for state in cell.accessible:
		cell.update_from_int(state)
		if getattr(cell, dirname):
			return True
	return False

print(show_accessible_count(field))
change_count = -1
while change_count:
	print('*** step ***', change_count)
	change_count = 0
	for k, m, cell in field:
		for state in tuple(cell.accessible):
			cell.update_from_int(state)
			check_dirs = (
				('left', 'right', 0, -1),
				('right', 'left', 0, +1),
				('top', 'bottom', -1, 0),
				('bottom', 'top', +1, 0),
			)
			for here, opposite, dk, dm in check_dirs:
				if getattr(cell, here):
					try:
						neighbour = field[k + dk, m + dm]
					except IndexError:
						# print('removing', cell, 'at', k, m, 'due to', opposite, '[empty]')
						cell.accessible.remove(state)
						change_count + 1
						break
					else:
						if not has_dir(neighbour, opposite):
							# print('removing', cell, 'at', k, m, 'due to', opposite)
							cell.accessible.remove(state)
							change_count += 1
							break
		if len(cell.accessible) == 1:
			cell.update_from_int(next(iter(cell.accessible)))
			check_dirs = (
				('left', 'right', 0, -1),
				('right', 'left', 0, +1),
				('top', 'bottom', -1, 0),
				('bottom', 'top', +1, 0),
			)
			for here, opposite, dk, dm in check_dirs:
				if getattr(cell, here):
					try:
						neighbour = field[k + dk, m + dm]
					except IndexError:
						pass
					else:
						for state in tuple(neighbour.accessible):
							neighbour.update_from_int(state)
							if not getattr(neighbour, opposite):
								# print('removing', neighbour, 'at', k, m, 'forced from', here)
								neighbour.accessible.remove(state)
								change_count + 1
		#todo: tmp
		cell.update_from_int(next(iter(cell.accessible)))
		# if cell.right:
		# 	try:
		# 		neighbour = field[k, m+1]
		# 	except IndexError:
		# 		print('removing', cell, 'at', k, m, 'due to left [empty]')
		# 		change_count += 1
		# 		cell.accessible.remove(state)
		# 	else:
		# 		if not has_dir(neighbour, 'left'):
		# 			print('removing', cell, 'at', k, m, 'due to left')
		# 			change_count += 1
		# 			cell.accessible.remove(state)
print(show_accessible_count(field))
print('change_count', change_count)

print(field)


