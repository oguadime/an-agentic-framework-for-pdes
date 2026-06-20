from agents.offline_agents import run_offline_agent


def main():
    prompts = [
        "Run a heat equation experiment with alpha=1, nx=101, dt=1e-5, T=0.01.",
        "Run a wave equation experiment with c=1, nx=201, dt=0.0025, T=0.25.",
        "Run an advection experiment with c=1, nx=200, dt=0.002, T=0.2.",
    ]

    for idx, prompt in enumerate(prompts, start=1):
        print("=" * 88)
        print(f"DEMO {idx}: {prompt}")
        print("=" * 88)
        print(run_offline_agent(prompt))


if __name__ == "__main__":
    main()
