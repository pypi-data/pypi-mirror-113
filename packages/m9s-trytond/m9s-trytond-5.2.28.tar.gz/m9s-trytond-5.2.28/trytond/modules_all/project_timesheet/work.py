# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from trytond.wizard import Wizard, StateAction
from trytond.pyson import PYSONEncoder
from trytond.transaction import Transaction

__all__ = ['WorkOpenTimesheetLine', 'WorkOpenAllTimesheetLine']


class WorkOpenTimesheetLine(Wizard):
    'Open All Timesheet Lines from Project Work'
    __name__ = 'project.work.open.timesheet.line'
    start_state = 'open_'
    open_ = StateAction('timesheet.act_line_form')

    def do_open_(self, action):
        Work = Pool().get('project.work')

        active_ids = Transaction().context['active_ids']
        works = Work.search([('id', 'in', active_ids)])
        action['pyson_domain'] = PYSONEncoder().encode([
                ('work', 'in', [tw.id for w in works
                        for tw in w.timesheet_works]),
                ])

        return action, {}


class WorkOpenAllTimesheetLine(Wizard):
    'Open All Timesheet Lines from Project Work'
    __name__ = 'project.work.open.all.timesheet.line'
    start_state = 'open_'
    open_ = StateAction('timesheet.act_line_form')

    def do_open_(self, action):
        Work = Pool().get('project.work')

        active_ids = Transaction().context['active_ids']
        works = Work.search([('parent', 'child_of', active_ids)])
        action['pyson_domain'] = PYSONEncoder().encode([
                ('work', 'in', [tw.id for w in works
                        for tw in w.timesheet_works]),
                ])

        return action, {}
