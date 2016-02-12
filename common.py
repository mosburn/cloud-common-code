""" This is a common library nor intended or designed to be run by itself
"""

__author__ = 'mosburn'


def get_regions(beanstalk=False):
    """ Provides a consistent interface between cloud providers

    :param beanstalk: If set to True, will check for partial regions
    :return: regions_list
    """
    if beanstalk:
        region_list = get_beanstalk_regions()
    else:
        region_list = get_ec2_regions()
    return region_list


def get_ec2_regions():
    """Generates a list of valid region names for our use.
    Default excluded regions are cn-north-1 and us-gov-west-1

    returns: region_list
    """
    import boto.ec2

    # excluding these regions as they have non-standard access requirements.
    excluded = ['cn-north-1', 'us-gov-west-1']

    # our final region list
    region_list = []

    # Get all the regions
    regions = boto.ec2.regions()

    for region in regions:
        region_name = region.name
        # Now kick out the excluded regions
        if region_name not in excluded:
            region_list.append(region_name)

    return region_list


def get_beanstalk_regions():
    """Generates a list of valid region names for our use.
    This is a truncated list as ElasticBeanstalk is a dependency for several
    higher level services and is not available in every region on launch, this
    will allow us to determine if we can use a new region at launch based on our
    usage.

    Default excluded regions are cn-north-1 and us-gov-west-1

    returns: region_list
    """
    import boto.beanstalk

    # excluding these regions as they have non-standard access requirements.
    excluded = ['cn-north-1', 'us-gov-west-1']

    # our final region list
    region_list = []

    # Get all the regions
    regions = boto.beanstalk.regions()

    for region in regions:
        region_name = region.name
        # Now kick out the excluded regions
        if region_name not in excluded:
            region_list.append(region_name)

    return region_list


def get_instances(awsregion):
    """ Gets a list of instances
    :param awsregion: The region to connect to

    :return: instanceList
    """

    instanceList = []
    conn = boto.ec2.connect_to_region(region_name=awsregion)
    reservations = conn.get_all_reservations()
    for reservation in reservations:
        for instance in reservation.instances:
            instanceList.append([instance])

    return instanceList


def printTags(awsregion, filters=False, ccFilters=False):
    """ Prints the tags for each instance
    :param filters: Any filters generated from :xomeCloudCommons.get_filters()
    :param ccFilters: Cost Center specific filters
    :return:
    """

    instances = aws.get_instances(awsregion)
    for instance in instances:
        if instance.tags['Name']:
            print "Name: " + instance.tags['Name'] + '\n'
        else:
            print "Unamed Server\n"
        print "Instance Id: " + instance.id + '\n'
        if instance.tags['Function']:
            print "Function: " + instance.tags['Function'] + '\n'
        if instance.tags['CostCenter']:
            if "costCenter" in filters:
                if instance.tags['CostCenter'] in ccFilters:
                    print "Cost Center: " + instance.tags['CostCenter'] + '\n'
        if instance.tags['Production']:
            if "prod" not in filters:
                print "Is this a Production server:  " + instance.tags['Production'] + '\n'
        if instance.tags['Beta']:
            if "beta" not in filters:
                print "Is this a Beta server: " + instance.tags['Beta'] + '\n'
        if instance.tags['Development']:
            if "dev" not in filters:
                print "Is this a Development server: " + instance.tags['Development'] + '\n'
        if instance.tags['Tower']:
            if "tower" not in filters:
                print "Is this Tower managed: " + instance.tags['Tower'] + '\n'
        if instance.tags['Octopus']:
            if "octopus" not in filters:
                print "Is this Octopus managed: " + instance.tags['Octopus'] + '\n'


def get_account_number():
    """ Gets the current account number
    Created so I do not have to remember how to do this every time
    :return: Returns the current account number
    """
    import boto
    return boto.connect_iam().get_user().arn.split(':')[4]
