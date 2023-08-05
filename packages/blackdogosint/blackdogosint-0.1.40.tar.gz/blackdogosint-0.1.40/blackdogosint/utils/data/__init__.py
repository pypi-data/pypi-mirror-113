import pkg_resources
useragents = 'file://' + pkg_resources.resource_filename(__name__, 'useragents')
apikeys= 'file://' + pkg_resources.resource_filename(__name__, 'api-key.yaml')
ipranges= 'file://' + pkg_resources.resource_filename(__name__, 'ip-ranges.json')
resolvers= 'file://' + pkg_resources.resource_filename(__name__, 'resolvers.txt')