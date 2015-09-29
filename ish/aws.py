#!/usr/bin/env python3
import boto3


def get_instances():
    return boto3.resource('ec2').instances.all()


def get_running_instances(ec2_instances):
    return [instance for instance in ec2_instances
            if instance.state['Name'] == 'running']


def id_targets_for_instances(instances):
    return [(inst.id, [inst.private_ip_address]) for inst in instances]


def name_tag_targets_for_instances(ilist):
    tag_nodes = {}

    for i in ilist:
        if i.tags is None:
            continue
        for tag in i.tags:
            if tag['Key'] == 'Name':
                name = tag['Value']
                if name not in tag_nodes:
                    tag_nodes[name] = []
                tag_nodes[name].append(i.private_ip_address)

    return [('name:{}'.format(tag), ips) for tag, ips in tag_nodes.items()]


def environment_tag_targets_for_instances(ilist):
    """
    Generate List of possible targets ordered by environment key.
    """
    env_nodes = {}

    for i in ilist:
        if i.tags is None:
            continue
        for tag in i.tags:
            if tag['Key'] == 'environment' or tag['Key'] == 'Environment':
                name = tag['Value']
                if name not in env_nodes:
                    env_nodes[name] = []
                env_nodes[name].append(i.private_ip_address)

    return [('env:{}'.format(env), ips) for env, ips in env_nodes.items()]


def asg_targets_for_instances(ilist):
    asg_nodes = {}

    for i in ilist:
        if i.tags is None:
            continue
        for tag in i.tags:
            if tag['Key'] == 'aws:autoscaling:groupName':
                name = tag['Value']
                if name not in asg_nodes:
                    asg_nodes[name] = []
                asg_nodes[name].append(i.private_ip_address)

    return [('asg:{}'.format(asg), ips) for asg, ips in asg_nodes.items()]


def opsworks_instance_name_targets_for_instances(ilist):
    """
    Generate targets list by opwsorks instance name
    """
    oin_nodes = {}

    for i in ilist:
        if i.tags is None:
            continue
        for tag in i.tags:
            if tag['Key'] == 'opsworks:instance':
                name = tag['Value']
                if name not in oin_nodes:
                    oin_nodes[name] = []
                oin_nodes[name].append(i.private_ip_address)

    return [('oin:{}'.format(oin), ips) for oin, ips in oin_nodes.items()]


def opsworks_instance_stack_targets_for_instances(ilist):
    """
    Generate targets list by opwsorks stack name
    """
    ois_nodes = {}

    for i in ilist:
        if i.tags is None:
            continue
        for tag in i.tags:
            if tag['Key'] == 'opsworks:stack':
                name = tag['Value']
                if name not in ois_nodes:
                    ois_nodes[name] = []
                ois_nodes[name].append(i.private_ip_address)

    return [('ois:{}'.format(ois), ips) for ois, ips in ois_nodes.items()]


def ami_targets_for_instances(ilist):
    ami_nodes = {}

    for i in ilist:
        if i.image_id not in ami_nodes:
            ami_nodes[i.image_id] = []
        ami_nodes[i.image_id].append(i.private_ip_address)

    return [(ami, ips) for ami, ips in ami_nodes.items()]


def targets_for_instances(_instances):
    """
    Aggregate all possible instance mappings
    """
    by_id = id_targets_for_instances(_instances)
    by_image = ami_targets_for_instances(_instances)
    by_name_tag = name_tag_targets_for_instances(_instances)
    by_environment_tag = environment_tag_targets_for_instances(_instances)
    by_asg = asg_targets_for_instances(_instances)
    by_oin = opsworks_instance_name_targets_for_instances(_instances)
    by_ois = opsworks_instance_stack_targets_for_instances(_instances)

    return dict(
        by_id +
        by_name_tag +
        by_environment_tag +
        by_image +
        by_asg +
        by_ois +
        by_oin
        )


def targets():
    return targets_for_instances(get_running_instances(get_instances()))
