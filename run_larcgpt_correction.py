# the experiment ! get gpt4 in here
from openai import OpenAI
import json

# OpenAI の ver 1.0 以降でLLMの出力の取得
client = OpenAI()

def get_llm_response(prompt):

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an autonomous task solver."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


preamble = """
lets play a game where you are transforming an input grid of numbers into an output grid of numbers

the numbers represent different colors:
0 = black
1 = blue
2 = red
3 = green
4 = yellow
5 = gray
6 = magenta
7 = orange
8 = cyan
9 = brown

"""
# def nl_and_io_prompt(task):
    
#     instruction = "here is the instruction of how to transform the grid: \n"
#     instruction += task['description']['description_input'] + task['description']['description_output_grid_size'] + task['description']['description_output']
    
#     train_input = task['problem']['train'][0]['input']
#     train_output = task['problem']['train'][0]['output']
#     input_output_example = "\n\nhere is an example of an input grid and its corresponding output grid:\n"
#     input_output_example += "example input grid:\n" + str(train_input) + "\nexample output grid:\n" + str(train_output) + "\n\n"

#     input_grid = task['problem']['test'][0]['input']

#     prompt = preamble + instruction + input_output_example + "\n\nThe input grid is:\n" + str(input_grid) + "\n\nWhat is the output grid?"
#     return prompt 

def generate_grid_generation_prompt(sample, description):
    
    instruction = "here is the instruction of how to transform the grid: \n"
    instruction += description['description_input'] + description['description_output_grid_size'] + description['description_output']
    
    input_grid = sample['input']

    prompt = preamble + instruction + "\n\nThe input grid is:\n" + str(input_grid) + "\n\nWhat is the output grid?" + "\n\nOutput gird surrounded by <output_grid> and <output_grid>"
    return prompt

def generate_grid_generation_with_feedback_prompt(sample, description, grid_prediction_from_train):
    input_grid = sample['input']
    output_grid = sample['output']
    prompt = f'''Your output was incorrect.
    The correct answer is {grid}.

    Please clearly identify the differences between the correct answer and your output.
    Specifically, highlight which part of the given task description was not accurately executed, resulting in this discrepancy.
    Then, provide the correct answer based on the correct interpretation of the task.'''
    prompt = preamble + description['description_input'] + "\n\nThe input grid is:\n" + str(input_grid) + "\n\nWhat is the output grid?" + "\n\nOutput gird surrounded by <output_grid> and <output_grid>"
    return prompt

if __name__ == '__main__':

    max_num_tasks = 1

    # open results/larc_gpt4.json
    with open('results/larc_gpt4.json') as json_file:
        larc_gpt4 = json.load(json_file)

    print(len(larc_gpt4))
    
    for task in larc_gpt4[:max_num_tasks]:  # 一つのタスクは共通のルールを持つ訓練テストサンプルの集合
        description = task['description']
        for sample in task['problem']['train']:
            prompt = generate_grid_generation_prompt(sample, description)
            print(prompt)

            grid_prediction_from_train = get_llm_response(prompt)
            # <output_grid> で囲まれた部分を取り出す
            grid_prediction_from_train = grid_prediction_from_train.split('<output_grid>')[1].split('</output_grid>')[0]
            print(grid_prediction_from_train)

            if grid_prediction_from_train == sample['output']:
                print("correct")
                break
            



        task['prediction'] = answer

        with open('results/larc_gpt4_newer.json', 'w') as outfile:
            json.dump(larc_gpt4, outfile)