from execredis.connection import ClientsConnection, ClusterClientsConnection


class ExecRedisClients:
    def __new__(cls, clients_name, redis_config=None):
        cls.__clients_name = clients_name
        cls.__redis_config = (redis_config or {clients_name: {}})[cls.__clients_name]
        if cls.__redis_config.pop('cluster', None):
            return ClusterClientsConnection(**cls.__redis_config)
        return ClientsConnection(**cls.__redis_config)
