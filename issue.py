import os
# os.environ["LLAMA_CPP_LIB_PATH"] = "/home/rickojn/coding/llama.cpp/build/bin/"
from llama_cpp import Llama
import time



def generate_with_seed(
    llm: Llama,
    prompt: str,
    seed: int,
    temperature: float,
    top_k: int,
    top_p: float,
    max_tokens: int,
) -> str:
    # reset context & kv-cache so every run starts fresh
    # llm.reset()

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
    MODEL_PATH = "../../models/llama-2-7b-chat.Q4_K_M.gguf"
    PROMPT     = "One Two"
    SEED1       = 1234
    SEED2       = 5678
    TEMP       = 1.0
    TOP_K      = 10
    TOP_P      = 0.9
    MAXTOKENS  = 3
    N_CTX      = 2048

    pause = 0
    print(f"pausing for {pause} seconds ...")
    time.sleep(pause) 
    print(f"loading model from {MODEL_PATH} with context size {N_CTX}...")

    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=N_CTX,
        no_perf=True, 
        verbose=False,
        logits_all=True,
    )

    print(f"model loaded, generating text with temperature={TEMP}, top_k={TOP_K}, top_p={TOP_P}...\n")

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
        print(f"Run #{i+1} with seed {SEED1}:\n{PROMPT}{out}\n{'─'*40}\n")
