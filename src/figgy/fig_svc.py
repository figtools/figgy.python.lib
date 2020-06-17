from typing import Optional

from botocore.exceptions import ClientError

from .utils import Utils


class FigService:

    def __init__(self, ssm):
        self._ssm = ssm

    @Utils.retry
    def get_fig(self, name: str, prefix: Optional[str] = None) -> Optional[str]:
        """
        Gets a parameter, returns None if parameter doesn't exist.
        Args:
            name: The PS Name - E.G. /app/demo-time/parameter/abc123
            prefix: Namespace prefix for this parameter. I.E. '/app/demo-time
        Returns: str -> Parameter's value
        """

        if prefix:
            if not name.startswith(prefix):
                name = f'{prefix.rstrip("/")}/{name.lstrip("/")}'
        try:
            parameter = self._ssm.get_parameter(Name=name, WithDecryption=True)
            return parameter['Parameter']['Value']
        except ClientError as e:
            if "ParameterNotFound" == e.response['Error']['Code']:
                return None
            else:
                raise
