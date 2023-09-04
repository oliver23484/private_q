'''
===========================================
        Module: Open-source LLM Setup
===========================================
'''
from langchain.llms import CTransformers
from dotenv import find_dotenv, load_dotenv
import box
import yaml,os
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


# Load environment variables from .env file
load_dotenv(find_dotenv())

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def build_llm():
    # Local CTransformers model
    total_threads = os.cpu_count()//2
    print(total_threads)
    llm = CTransformers(model=cfg.MODEL_BIN_PATH,
                        model_type=cfg.MODEL_TYPE,
                        callbacks=[StreamingStdOutCallbackHandler()],
                        config={'max_new_tokens': cfg.MAX_NEW_TOKENS,
                                'temperature': cfg.TEMPERATURE,
                                'threads':total_threads,
                                }
                        )
    return llm
