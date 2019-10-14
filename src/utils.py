from base_model import IdModel


def json_serialize(result):
    """Uses .json() method of model instances to json serialize instances and list of instances.
    """
    if isinstance(result, IdModel):
        return result.json()
    elif isinstance(result, list):
        return [subresult.json() for subresult in result]
    raise TypeError("Invalid Type: {}".format(type(result)))
