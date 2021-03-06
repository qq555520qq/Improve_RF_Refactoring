#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from robot304.errors import ExecutionFailed, DataError, PassExecution
from robot304.model import SuiteVisitor
from robot304.result import TestSuite, Result
from robot304.utils import get_timestamp, is_list_like, NormalizedDict, unic
from robot304.variables import VariableScopes

from .context import EXECUTION_CONTEXTS
from .steprunner import StepRunner
from .namespace import IMPORTER, Namespace
from .status import SuiteStatus, TestStatus
from .timeouts import TestTimeout


# Some 'extract method' love needed here. Perhaps even 'extract class'.

class Runner(SuiteVisitor):

    def __init__(self, output, settings):
        self.result = None
        self._output = output
        self._settings = settings
        self._variables = VariableScopes(settings)
        self._suite = None
        self._suite_status = None
        self._executed_tests = None

    @property
    def _context(self):
        return EXECUTION_CONTEXTS.current

    def start_suite(self, suite):
        self._output.library_listeners.new_suite_scope()
        result = TestSuite(source=suite.source,
                           name=suite.name,
                           doc=suite.doc,
                           metadata=suite.metadata,
                           starttime=get_timestamp())
        if not self.result:
            result.set_criticality(self._settings.critical_tags,
                                   self._settings.non_critical_tags)
            self.result = Result(root_suite=result)
            self.result.configure(status_rc=self._settings.status_rc,
                                  stat_config=self._settings.statistics_config)
        else:
            self._suite.suites.append(result)
        self._suite = result
        self._suite_status = SuiteStatus(self._suite_status,
                                         self._settings.exit_on_failure,
                                         self._settings.exit_on_error,
                                         self._settings.skip_teardown_on_exit)
        ns = Namespace(self._variables, result, suite.resource)
        ns.start_suite()
        ns.variables.set_from_variable_table(suite.resource.variables)
        EXECUTION_CONTEXTS.start_suite(result, ns, self._output,
                                       self._settings.dry_run)
        self._context.set_suite_variables(result)
        if not self._suite_status.failures:
            ns.handle_imports()
            ns.variables.resolve_delayed()
        result.doc = self._resolve_setting(result.doc)
        result.metadata = [(self._resolve_setting(n), self._resolve_setting(v))
                           for n, v in result.metadata.items()]
        self._context.set_suite_variables(result)
        self._output.start_suite(ModelCombiner(suite, result,
                                               tests=suite.tests,
                                               suites=suite.suites,
                                               test_count=suite.test_count))
        self._output.register_error_listener(self._suite_status.error_occurred)
        self._run_setup(suite.keywords.setup, self._suite_status)
        self._executed_tests = NormalizedDict(ignore='_')

    def _resolve_setting(self, value):
        if is_list_like(value):
            return self._variables.replace_list(value, ignore_errors=True)
        return self._variables.replace_string(value, ignore_errors=True)

    def end_suite(self, suite):
        self._suite.message = self._suite_status.message
        self._context.report_suite_status(self._suite.status,
                                          self._suite.full_message)
        with self._context.suite_teardown():
            failure = self._run_teardown(suite.keywords.teardown, self._suite_status)
            if failure:
                self._suite.suite_teardown_failed(unic(failure))
                if self._suite.statistics.critical.failed:
                    self._suite_status.critical_failure_occurred()
        self._suite.endtime = get_timestamp()
        self._suite.message = self._suite_status.message
        self._context.end_suite(ModelCombiner(suite, self._suite))
        self._suite = self._suite.parent
        self._suite_status = self._suite_status.parent
        self._output.library_listeners.discard_suite_scope()
        if not suite.parent:
            IMPORTER.close_global_library_listeners()

    def visit_test(self, test):
        if test.name in self._executed_tests:
            self._output.warn("Multiple test cases with name '%s' executed in "
                              "test suite '%s'." % (test.name, self._suite.longname))
        self._executed_tests[test.name] = True
        result = self._suite.tests.create(name=test.name,
                                          doc=self._resolve_setting(test.doc),
                                          tags=self._resolve_setting(test.tags),
                                          starttime=get_timestamp(),
                                          timeout=self._get_timeout(test))
        self._context.start_test(result)
        self._output.start_test(ModelCombiner(test, result))
        status = TestStatus(self._suite_status, result.critical)
        if not status.failures and not test.name:
            status.test_failed('Test case name cannot be empty.')
        if not status.failures and not test.keywords.normal:
            status.test_failed('Test case contains no keywords.')
        if status.exit:
            self._add_exit_combine()
            result.tags.add('robot-exit')
        self._run_setup(test.keywords.setup, status, result)
        try:
            if not status.failures:
                StepRunner(self._context,
                           test.template).run_steps(test.keywords.normal)
            else:
                status.test_failed(status.message)
        except PassExecution as exception:
            err = exception.earlier_failures
            if err:
                status.test_failed(err)
            else:
                result.message = exception.message
        except ExecutionFailed as err:
            status.test_failed(err)
        result.status = status.status
        result.message = status.message or result.message
        if status.teardown_allowed:
            with self._context.test_teardown(result):
                failure = self._run_teardown(test.keywords.teardown, status,
                                             result)
                if failure and result.critical:
                    status.critical_failure_occurred()
        if not status.failures and result.timeout and result.timeout.timed_out():
            status.test_failed(result.timeout.get_message())
            result.message = status.message
        result.status = status.status
        result.endtime = get_timestamp()
        self._output.end_test(ModelCombiner(test, result))
        self._context.end_test(result)

    def _add_exit_combine(self):
        exit_combine = ('NOT robot-exit', '')
        if exit_combine not in self._settings['TagStatCombine']:
            self._settings['TagStatCombine'].append(exit_combine)

    def _get_timeout(self, test):
        if not test.timeout:
            return None
        return TestTimeout(test.timeout.value, test.timeout.message,
                           self._variables)

    def _run_setup(self, setup, status, result=None):
        if not status.failures:
            exception = self._run_setup_or_teardown(setup)
            status.setup_executed(exception)
            if result and isinstance(exception, PassExecution):
                result.message = exception.message

    def _run_teardown(self, teardown, status, result=None):
        if status.teardown_allowed:
            exception = self._run_setup_or_teardown(teardown)
            status.teardown_executed(exception)
            failed = not isinstance(exception, PassExecution)
            if result and exception:
                result.message = status.message if failed else exception.message
            return exception if failed else None

    def _run_setup_or_teardown(self, data):
        if not data:
            return None
        try:
            name = self._variables.replace_string(data.name)
        except DataError as err:
            if self._settings.dry_run:
                return None
            return err
        if name.upper() in ('', 'NONE'):
            return None
        try:
            StepRunner(self._context).run_step(data, name=name)
        except ExecutionFailed as err:
            return err


class ModelCombiner(object):

    def __init__(self, data, result, **priority):
        self.data = data
        self.result = result
        self.priority = priority

    def __getattr__(self, name):
        if name in self.priority:
            return self.priority[name]
        if hasattr(self.result, name):
            return getattr(self.result, name)
        if hasattr(self.data, name):
            return getattr(self.data, name)
        raise AttributeError(name)
