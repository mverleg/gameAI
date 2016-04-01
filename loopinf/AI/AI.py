
from loopinf.game.game import Grid


class ImpossibleSituation(Exception):
	pass


class NoMoreDeductiveSteps(Exception):
	pass


field = Grid.load('../levels/52')


def show_accessible_count(field):
	parts = ['  ']
	for m in range(len(field.cells[0])):
		parts.append(' {0:2d}'.format(m))
	parts.append('\n')
	for k, row in enumerate(field.cells):
		parts.append('{0:2d} '.format(k))
		for cell in row:
			if cell.is_empty() == 1:
				parts.append('   ')
			elif len(cell.accessible) == 0:
				parts.append('XX ')
			else:
				cell.update_from_int(next(iter(cell.accessible)))
				parts.append(str(cell) + str(len(cell.accessible)) + ' ')
		parts.append('\n')
	print(''.join(parts[:-1]))


""" Store available states on each cell. """
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


def deduction(field):
	# print(show_accessible_count(field))
	change_count = -1
	while change_count:
		# print('*** step ***', change_count)
		change_count = 0
		for k, m, cell in field:
			for state in tuple(cell.accessible):
				cell.update_from_int(state)
				# print(k, m, state, cell)
				check_dirs = (
					('left', 'right', 0, -1),
					('right', 'left', 0, +1),
					('top', 'bottom', -1, 0),
					('bottom', 'top', +1, 0),
				)
				for here, opposite, dk, dm in check_dirs:
					# print(k, m, 'if getattr(cell, here):', str(cell), here, getattr(cell, here))
					if getattr(cell, here):
						try:
							neighbour = field[k + dk, m + dm]
						except IndexError:
							# print('removing', cell, 'at', k, m, 'due to', here, 'being empty')
							cell.accessible.remove(state)
							change_count + 1
							break
						else:
							if not has_dir(neighbour, opposite):
								# print('removing', cell, 'at', k, m, 'due to', here, 'not having', opposite)
								cell.accessible.remove(state)
								change_count += 1
								break
							# else:
								# print('keeping', cell, 'at', k, m, 'for', here)
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
									# print('removing', neighbour, 'at', k + dk, m + dm, 'forced by not having', opposite, 'by', here, 'at', k, m)
									neighbour.accessible.remove(state)
									change_count + 1
	for k, m, cell in field:
		if len(cell.accessible) < 1:
			raise ImpossibleSituation('at {0:d}, {1:d}'.format(k, m))
		elif len(cell.accessible) > 1:
			raise NoMoreDeductiveSteps('at {0:d}, {1:d} ({2:d} options left)'.format(k, m, len(cell.accessible)))

	return field


def attempt(field):
	# show_accessible_count(field)
	try:
		field = deduction(field)
	except ImpossibleSituation:
		# print('*** WRONG ATTEMPT ***')
		# show_accessible_count(field)
		return None
	except NoMoreDeductiveSteps:
		for k, m, cell in field:
			if len(cell.accessible) > 1:
				for state in cell.accessible:
					cell.update_from_int(state)
					print('RECURSION LEVEL FOR', cell, 'AT', k, m)
					subfield = field.copy()
					for sk, sm, subcell in field:
						# print('SET', sk, sm, 'TO', subcell.accessible)
						subfield[sk, sm].accessible = set(iter(subcell.accessible))
					subfield[k, m].accessible = {state}
					found = attempt(subfield)
					if found:
						# solutions.append(found)
						return found
					else:
						print('dead end')
	else:
		return field


field = attempt(field)
print(field)
exit()
# print('found {0:d} solutions'.format(len(solutions)))
# for sol in solutions:
# 	for k, m, cell in sol:
# 		cell.update_from_int(next(iter(cell.accessible)))
# 	print(field)


