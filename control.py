from src import logging_main
from src import switchbot

if __name__ == "__main__":
    # home control
    logger_name = __name__
    logging_main.handler(
        logger_name+"start", "INFO",
        "air conditioning system Start"
    )
    switchbot_instance = switchbot.SwitchBotOperator()
    switchbot_instance.controller()
    logging_main.handler(
        logger_name+"end", "INFO",
        "air conditioning system End"
    )
