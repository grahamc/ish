
import io
import ish.ui
import unittest
from unittest.mock import Mock


class TestUi(unittest.TestCase):
    def setUp(self):
        self.err_mock = io.StringIO()
        self.out_mock = io.StringIO()
        self.exit_mock = Mock()

    def test_stderr(self):
        view = ish.ui.View('stub', err=self.err_mock)
        view.stderr('test')

        self.assertEqual("test\n", self.err_mock.getvalue())

    def test_stdout(self):
        view = ish.ui.View('stub', out=self.out_mock)
        view.stdout('test')

        self.assertEqual("test\n", self.out_mock.getvalue())

    def test_help(self):
        view = ish.ui.View('foo', err=self.err_mock, exit=self.exit_mock)
        view.help()

        self.assertEqual(
            "Usage: foo target [ssh parameters]\n",
            self.err_mock.getvalue()
        )
        self.exit_mock.assert_called_with(1)

    def test_valid_targets(self):
        view = ish.ui.View('stub', out=self.out_mock, exit=self.exit_mock)
        view.valid_targets(['foo', 'bar'])
        self.assertEqual(
            "bar\nfoo\n",
            self.out_mock.getvalue()

        )
        self.exit_mock.assert_called_with(0)

    def test_invalid_target(self):
        view = ish.ui.View('stub', err=self.err_mock, exit=self.exit_mock)
        view.invalid_target('invalid')
        self.assertEqual("No target named invalid\n", self.err_mock.getvalue())

    def test_connect_to(self):
        execvp = Mock()
        view = ish.ui.View(
            'stub',
            err=self.err_mock,
            exit=self.exit_mock,
            execvp=execvp
        )

        view.connect_to('1.2.3.4', ['1.2.3.4', '2.3.4.5'], 'serverA')

        self.assertEqual(
            "Found 2 IPs for serverA:\n"
            " - 1.2.3.4 (selected)\n"
            " - 2.3.4.5\n",
            self.err_mock.getvalue()
        )
        execvp.assert_called_with(
            '/usr/bin/ssh',
            [
                '/usr/bin/ssh',
                '1.2.3.4'
            ]
        )
        self.exit_mock.assert_called_with(2)


class TestInputHandler(unittest.TestCase):
    def setUp(self):
        self.ui = Mock()
        self.ui_constructor = Mock(return_value=self.ui)

    def test_handle_argv_none(self):
        self.ui.help = Mock()

        ih = ish.ui.InputHandler(['ish'], {}, self.ui_constructor)
        self.ui_constructor.assert_called_with('ish')
        ih.handle_argv()
        self.ui.help.assert_called_with()

    def test_handle_argv_completion(self):
        ih = ish.ui.InputHandler(
            ['ish', '--completion'],
            {'foo': [], 'bar': []},
            self.ui_constructor
        )
        self.ui.valid_targets = Mock()
        ih.handle_argv()
        self.ui.valid_targets.assert_called_with({'foo': [], 'bar': []})

    def test_handle_argv_invalid_target(self):
        ih = ish.ui.InputHandler(
            ['ish', 'invalid'],
            {'server1': [], 'server2': []},
            self.ui_constructor
        )
        self.ui.invalid_target = Mock()
        ih.handle_argv()
        self.ui.invalid_target.assert_called_with('invalid')

    def test_handle_argv_valid_target(self):
        ih = ish.ui.InputHandler(
            ['ish', 'valid'],
            {'valid': ['1.2.3.4']},
            self.ui_constructor
        )

        self.ui.connect_to = Mock()
        ih.handle_argv()
        self.ui.connect_to.assert_called_with('1.2.3.4', ['1.2.3.4'], 'valid')
