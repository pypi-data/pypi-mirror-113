from loguru import logger

logger.enable("basis")


def test():
    from basis_bi import module as bi

    bi.run_tests()


if __name__ == "__main__":
    test()
