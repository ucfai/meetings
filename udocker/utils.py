from datetime import date as dt

def get_sem():
	yr = dt.today().year
	mo = dt.today().month
	sp = (1,  4)
	su = (5,  7)
	fa = (8, 12)

	sp_sem = (dt(yr, sp[0], 1), dt(yr, sp[1], 1))
	su_sem = (dt(yr, su[0], 1), dt(yr, su[1], 1))
	fa_sem = (dt(yr, fa[0], 1), dt(yr, fa[1], 1))

	if   mo <= sp_sem[1].month:
		sem = "sp"
	elif mo <= su_sem[1].month:
		sem = "su"
	else:
		sem = "fa"

	return sem + str(yr)[-2:]