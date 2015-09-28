
import unittest
import ish.aws
from unittest.mock import Mock, patch


class StubInstance:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestAws(unittest.TestCase):
    def assertItemsEqual(self, a, b):
        self.assertEqual(sorted(a), sorted(b))

    @patch('boto3.resource')
    def test_get_instances(self, botoresource):
        instances = [
            StubInstance(id=1, state={'Name': 'running'}),
            StubInstance(id=2, state={'Name': 'notrunning'})
        ]

        ec2 = Mock()
        ec2.instances.all = Mock(return_value=instances)
        botoresource.return_value = ec2

        self.assertEqual(instances, ish.aws.get_instances())

    def test_get_running_instances(self):
        instances = [
            StubInstance(id=1, state={'Name': 'running'}),
            StubInstance(id=2, state={'Name': 'notrunning'})
        ]
        self.assertItemsEqual(
            [instances[0]],
            ish.aws.get_running_instances(instances),
        )

    def test_id_targets_for_instances(self):
        instances = [
            StubInstance(id=1, private_ip_address='1.2.3.4'),
            StubInstance(id=2, private_ip_address='2.3.4.5')
        ]

        self.assertEqual(
            [
                (1, ['1.2.3.4']),
                (2, ['2.3.4.5'])
            ],
            ish.aws.id_targets_for_instances(instances)
        )

    def test_name_tag_targets_for_instances(self):
        instances = [
            StubInstance(private_ip_address='0.0.0.0', tags=None),
            StubInstance(private_ip_address='1.2.3.4', tags=[
                {'Key': 'foo', 'Value': 'bar'},
                {'Key': 'Name', 'Value': 'myname'}
            ]),
            StubInstance(private_ip_address='2.3.4.5', tags=[
                {'Key': 'foo', 'Value': 'baz'},
                {'Key': 'Name', 'Value': 'myname'}
            ]),
            StubInstance(private_ip_address='3.4.5.6', tags=[
                {'Key': 'foo', 'Value': 'baz'},
                {'Key': 'Name', 'Value': 'newname'}
            ]),
        ]

        self.assertItemsEqual(
            [
                ('name:myname', ['1.2.3.4', '2.3.4.5']),
                ('name:newname', ['3.4.5.6'])
            ],
            ish.aws.name_tag_targets_for_instances(instances)
        )

    def test_asg_targets_for_instances(self):
        instances = [
            StubInstance(private_ip_address='0.0.0.0', tags=None),
            StubInstance(private_ip_address='1.2.3.4', tags=[
                {'Key': 'foo', 'Value': 'bar'},
                {'Key': 'aws:autoscaling:groupName', 'Value': 'foogroup'}
            ]),
            StubInstance(private_ip_address='2.3.4.5', tags=[
                {'Key': 'foo', 'Value': 'baz'},
                {'Key': 'aws:autoscaling:groupName', 'Value': 'bargroup'}
            ]),
            StubInstance(private_ip_address='3.4.5.6', tags=[
                {'Key': 'foo', 'Value': 'baz'},
                {'Key': 'aws:autoscaling:groupName', 'Value': 'foogroup'}
            ]),
        ]

        self.assertItemsEqual(
            [
                ('asg:foogroup', ['1.2.3.4', '3.4.5.6']),
                ('asg:bargroup', ['2.3.4.5'])
            ],
            ish.aws.asg_targets_for_instances(instances)
        )

    def test_ami_targets_for_instances(self):
        instances = [
            StubInstance(private_ip_address='1.2.3.4', image_id='ami-123'),
            StubInstance(private_ip_address='2.3.4.5', image_id='ami-123'),
            StubInstance(private_ip_address='3.4.5.6', image_id='ami-456')
        ]

        self.assertItemsEqual(
            [
                ('ami-123', ['1.2.3.4', '2.3.4.5']),
                ('ami-456', ['3.4.5.6'])

            ],
            ish.aws.ami_targets_for_instances(instances)
        )

    def test_targets_for_instances(self):
        instances = [
            StubInstance(
                id='i-abc123',
                image_id='ami-def456',
                private_ip_address='1.2.3.4',
                tags=[
                    {'Key': 'foo', 'Value': 'bar'},
                    {'Key': 'Name', 'Value': 'servername'},
                    {'Key': 'aws:autoscaling:groupName', 'Value': 'groupname'}
                ]

            )
        ]

        self.assertEqual(
            {
                'name:servername': ['1.2.3.4'],
                'asg:groupname': ['1.2.3.4'],
                'i-abc123': ['1.2.3.4'],
                'ami-def456': ['1.2.3.4'],
            },
            ish.aws.targets_for_instances(instances)
        )

    @patch('boto3.resource')
    def test_targets(self, botoresource):
        instances = [
            StubInstance(
                id='i-abc123',
                image_id='ami-def456',
                private_ip_address='1.2.3.4',
                state={'Name': 'running'},
                tags=[
                    {'Key': 'foo', 'Value': 'bar'},
                    {'Key': 'Name', 'Value': 'servername'},
                    {'Key': 'aws:autoscaling:groupName', 'Value': 'groupname'}
                ]
            ),
            StubInstance(id=2, state={'Name': 'notrunning'})
        ]

        ec2 = Mock()
        ec2.instances.all = Mock(return_value=instances)
        botoresource.return_value = ec2

        self.assertEqual(
            {
                'name:servername': ['1.2.3.4'],
                'asg:groupname': ['1.2.3.4'],
                'i-abc123': ['1.2.3.4'],
                'ami-def456': ['1.2.3.4'],
            },
            ish.aws.targets()
        )
