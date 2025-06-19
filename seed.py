from llama_cpp import Llama

def generate_with_seed(
    llm: Llama,
    prompt: str,
    seed: int,
    temperature: float = 0.8,
    top_k: int = 40,
    top_p: float = 0.95,
    max_tokens: int = 128,
) -> str:
    """
    Generate a deterministic response from a pre-loaded llama.cpp model.

    llm.reset() must be called first to clear the context and KV cache,
    then passing `seed` here reseeds the RNG for this single generation.
    """
    # reset context & kv-cache so every run starts fresh
    llm.reset()

    resp = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        seed=seed,
    )
    return resp["choices"][0]["text"].lstrip()


if __name__ == "__main__":
    # --- Configuration ---
    MODEL_PATH = "/home/rickojn/coding/llama.cpp/models/llama-2-7b-chat.Q4_K_M.gguf"
    PROMPT     = "Once upon a time"
    SEED1       = 1234
    SEED2       = 5678
    TEMP       = 1.0
    TOP_K      = 10
    TOP_P      = 0.9
    MAXTOKENS  = 50
    N_CTX      = 2048

    # 1. Load the model only once
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=N_CTX,
        no_perf=True, 
        verbose=False,
    )

    # 2. Run multiple generations with the same parameters
    for i in range(3):
        out = generate_with_seed(
            llm=llm,
            prompt=PROMPT,
            seed=SEED1,
            temperature=TEMP,
            top_k=TOP_K,
            top_p=TOP_P,
            max_tokens=MAXTOKENS,
        )
        print(f"Run #{i+1} with seed {SEED1}:\n{PROMPT} ... {out}\n{'─'*40}\n")
    for i in range(3):
        out = generate_with_seed(
            llm=llm,
            prompt=PROMPT,
            seed=SEED2,
            temperature=TEMP,
            top_k=TOP_K,
            top_p=TOP_P,
            max_tokens=MAXTOKENS,
        )
        print(f"Run #{i+1} with seed {SEED2}:\n{PROMPT}{out}\n{'─'*40}\n")
