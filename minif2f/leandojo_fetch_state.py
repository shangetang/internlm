# Lean proof search with LeanDojo interaction
# Author: Sean Welleck

#20250105 modified by Shange, whole proof
import json, os
import heapq
import subprocess
import time
import transformers
# import vllm
from datetime import datetime
from lean_dojo import *
from pathlib import Path
from tqdm import tqdm, trange

os.environ['TOKENIZERS_PARALLELISM'] = 'false'


def chat_template_to_prompt(prompt_list):
    result = ""
    total_step = len(prompt_list)
    for i, message in enumerate(prompt_list):
        result += ('<|im_start|>' + message['role'] +
                   '\n' + message['content'])
        if i+1 != total_step:
            result += '<|im_end|>\n'
        elif message['role'] == 'user':
            result += '<|im_end|>\n<|im_start|>assistant\n'
    return result

def prompt_style_internlm_chat_stepprover_extractor(result:str):
    return result

def _prompt_function(theorem, state, proof_before=""):
    input_template = (  f"---\nNAME: {theorem.full_name}\n\n"
                            # f"---\nFILE:{theorem.file_path}\n\n"
                            f"---\nPROOF_BEFORE: {proof_before}\n\n"
                            f"---\nSTATE_BEFORE: {state}\n\n"
                            f"---\nTACTIC: "
                        )
    prompt = [{"role": "user", "content": input_template}]
    return prompt

# def generate_vllm(prompt, model, tokenizer, temperatures, num_samples, stop, max_tokens=256):
#     if not isinstance(prompt, str):
#         prompt = chat_template_to_prompt(prompt)
#     texts, scores = [], []
#     for temperature in temperatures:
#         params = vllm.SamplingParams(
#             n=num_samples,
#             temperature=temperature,
#             use_beam_search=temperature==0.0,
#             max_tokens=max_tokens,
#             stop=stop,
#             length_penalty=0.0 if temperature==0.0 else 1.0,
#             logprobs=True,
#         )
#         outputs = model.generate([prompt], params, use_tqdm=False)
#         if len(outputs) == 0:
#             return [], []
#         for output in outputs[0].outputs:
#             text = output.text.replace(tokenizer.eos_token, '')
#             score = output.cumulative_logprob/max(len(output.token_ids), 1)
#             texts.append(text)
#             scores.append(score)

#     texts = list(map(prompt_style_internlm_chat_stepprover_extractor,texts))
#     texts, scores = _unique_sorted(texts, scores)
#     return texts, scores


def _unique_sorted(texts, scores):
    texts_ = []
    scores_ = []
    for t, s in sorted(zip(texts, scores), key=lambda x: -x[1]):
        if t not in texts_:
            texts_.append(t)
            scores_.append(s)
    return texts_, scores_


def _tactic_state(state):
    if isinstance(state, TacticState):
        ts = state.pp
    else:
        ts = state.unsolved_tactic_state
    return ts





def _save(model_name, results, args_dict, output_dir, shard):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_file = os.path.join(
        output_dir,
        'results__%s__%s.json' % (model_name.replace('/', '_'), shard)
    )
    with open(output_file, 'w') as f:
        json.dump({
            'results': results,
            'args': args_dict
            }, f, indent=4)
        print(output_file)



def _load_data(dataset_name, dataset_path):
    if 'minif2f' in dataset_name:
        data = []
        with open(dataset_path) as f:
            for line in f.readlines():
                data_ = json.loads(line)
                data.append(data_)

        if 'valid' in dataset_name:
            data = [x for x in data if x['split'] == 'valid']
        else:
            data = [x for x in data if x['split'] == 'test']
        repo = LeanGitRepo(data[0]['url'], data[0]['commit'])
    else:
        raise NotImplementedError(dataset_name)

    return repo, data


def print_stats(results):
    print(len([x for x in results if x['success']]) / len(results))
    print("# successes: ", len([x for x in results if x['success']]), sep="\t")

import pathlib
from pathlib import Path
def resume_from(results_filename, data, model_name, shard):
    results_path = Path(results_filename)
    if results_path.is_dir():
        results_path = results_path / ('results__%s__%s.json' % (model_name.replace('/', '_'), shard))
    if results_path.exists():
        results = json.load(open(results_path))['results']
        data = data[len(results):]
        print("=== Resuming from %d" % (len(results)))
        return results, data
    else:
        return [],data


def make_output_dir(output_dir):
    dt = datetime.now().strftime("%d-%m-%Y-%H-%M")
    output_dir = os.path.join(output_dir, dt)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    return output_dir


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model-name', 
        required=True
    )
    parser.add_argument(
        '--dataset-name',
        default='minif2f-test',
        choices=['minif2f-valid', 'minif2f-test']
    )
    parser.add_argument('--shard', type=int, required=True)
    parser.add_argument('--resume-from', type=str, default=None)
    parser.add_argument('--dataset-path', default='data/minif2f-lean4.7.0.jsonl')
    parser.add_argument('--output-dir', default='output/minif2f')
    parser.add_argument('--early-stop', action='store_true')
    parser.add_argument('--tp-degree', type=int, default=1)
    parser.add_argument('--num-shards', type=int, default=8)
    parser.add_argument('--max-iters', type=int, default=100)
    parser.add_argument('--timeout', type=int, default=1200)
    parser.add_argument('--num-examples', type=int, default=-1)
    parser.add_argument('--num-samples', type=int, default=32)
    parser.add_argument('--clear-process-hours', type=int, default=3)
    parser.add_argument('--temperatures', type=float, nargs='+', default=[0.0])

    parser.add_argument('--output_path',type=str,default='')
    args = parser.parse_args()

    timeout = args.timeout
    output_dir = make_output_dir(args.output_dir)

    repo, data = _load_data(args.dataset_name, args.dataset_path)
    shard_size = len(data) // args.num_shards
    # data = data[args.shard*shard_size:(args.shard+1)*shard_size] if args.num_shards > 1+ args.shard else data[args.shard*shard_size:]
    # print("Shard size: %d" % (len(data)))


    if args.resume_from is not None:
        results, data = resume_from(args.resume_from, data, args.model_name,args.shard)
    else:
        results = []

    start = time.time()
    all_results = []
    for example in tqdm(data, total=len(data)):
        file_path = example['file_path']
        theorem_name = example['full_name']
        theorem = Theorem(repo, file_path, theorem_name)

        with Dojo(theorem, hard_timeout=timeout,additional_imports=["Mathlib.Tactic"]) as (dojo, init_state):
            ts = _tactic_state(init_state)
            proof_before = ""
            # State de-duplication needs re-compile Lean 4, whose code will be released soon.
            # Here we are tolerating duplicated states, should not impact performance on miniF2F. 
            # proof_before = "\n".join(steps)

            prompt= _prompt_function(theorem, ts, proof_before)


        print(theorem_name)



        # result_dict["problem_id"] = theorem_name
        example["state"] = ts
        example["prompt"] = prompt

        all_results.append(example)

    with open(args.output_path,"r") as file:
        json.dump(all_results,file,indent = 4)

    print(f"saved to {args.output_path}")



        # attempt_results = best_first_search(
        #     theorem, model, tokenizer,
        #     max_iters=args.max_iters,
        #     prompt_fn=_prompt_function,
        #     temperatures=args.temperatures,
        #     num_samples=args.num_samples,
        #     timeout=args.timeout,
        #     early_stop=args.early_stop
        # )

        # result = {
        #     'attempt_results': attempt_results,
        #     'success': any([x['success'] for x in attempt_results]),
        #     'example': example
        # }

        # results.append(result)

        # _save(
        #     model_name=args.model_name,
        #     results=results,
        #     args_dict=args.__dict__,
        #     output_dir=output_dir,
        #     shard=args.shard
        # )
        # print_stats(results)


        # The proof search occasionally leaves Lean processes open. As a workaround,
        # we periodically kill all Lean processes. Note that this may cause a proof search failure.
    if args.shard == 0:
        hours = 60*60*args.clear_process_hours
        if time.time() - start > hours:
            print("=== Killing active leanprover processes to mitigate leak")
            os.system("ps aux | grep leanprover | awk '{print $2}' | xargs kill -9")
            start = time.time()
