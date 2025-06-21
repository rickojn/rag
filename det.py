import requests

def generate_with_seed(
    prompt: str,
    seed: int,
    temperature: float,
    top_k: int,
    top_p: float,
    max_tokens: int,
    server_url: str = "http://localhost:8080/completion"
) -> str:
    payload = {
        "prompt": prompt,
        "seed": seed,
        "temperature": temperature,
        "top_k": top_k,
        "top_p": top_p,
        "n_predict": max_tokens,
        "stop": [],
        "stream": False,
    }
    resp = requests.post(server_url, json=payload)
    resp.raise_for_status()
    return resp.json()["content"].lstrip()

if __name__ == "__main__":
    PROMPT     = "Once upon a time"
    SEED1      = 1234
    SEED2      = 5678
    TEMP       = 1.0
    TOP_K      = 10
    TOP_P      = 0.9
    MAXTOKENS  = 50

    print(f"Sending requests to llama.cpp server at http://localhost:8080/completion...\n")

    for i in range(3):
        out = generate_with_seed(
            prompt=PROMPT,
            seed=SEED1,
            temperature=TEMP,
            top_k=TOP_K,
            top_p=TOP_P,
            max_tokens=MAXTOKENS,
        )
        print(f"Run #{i+1} with seed {SEED1}:\n{PROMPT}{out}\n{'─'*40}\n")
    for i in range(3):
        out = generate_with_seed(
            prompt=PROMPT,
            seed=SEED2,
            temperature=TEMP,
            top_k=TOP_K,
            top_p=TOP_P,
            max_tokens=MAXTOKENS,
        )
        print(f"Run #{i+1} with seed {SEED2}:\n{PROMPT}{out}\n{'─'*40}\n")