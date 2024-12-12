class MissConfError(Exception):
    """
    MissConfError helps to document missing configuration values from subcommands,
    it presents a friendly message together with example of what is missing.

    Example:
    ``
        acct = cmd.obj['config.account']
        if acct is None:
            raise MissConfError(topic="config", entry="account", example="VALID_OP_ACCOUNT")
    ``
    """
    def __init__(self, topic, entry, example):
        self.topic = topic
        self.entry = entry
        self.example = example
        super().__init__(self._generate_message())

    def _generate_message(self):
        return (f"Missing entry '{self.entry}' on '{self.topic}'.\n"
                f"Ensure you have the following in your configuration:\n\n"
                f"[{self.topic}]\n"
                f"{self.entry} = {self.example}\n")
