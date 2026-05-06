from sources.engine import Engine

# The simulation duration in time unit
SIMULATION_DURATION: float = 10000.0


def main():
    engine: Engine = Engine(SIMULATION_DURATION)
    engine.run()


if __name__ == "__main__":
    main()
