import json
import os
import pandas as pd
import ast  # 替代 json.loads，用于解析非标准列表字符串

# 设置路径
base_path = 'data/DDXPlus'
train_file = os.path.join(base_path, 'release_train_patients.csv')
evidence_file = os.path.join(base_path, 'release_evidences.json')
condition_file = os.path.join(base_path, 'release_conditions.json')

# 输出目录
output_dir = 'result/participants_output'
os.makedirs(output_dir, exist_ok=True)

# 读取 CSV 数据
train_df = pd.read_csv(train_file)

# 读取 evidence JSON 数据
with open(evidence_file, 'r', encoding='utf-8') as f:
    evidence_data = json.load(f)

if isinstance(evidence_data, list):
    evidence_map = {item['id']: item for item in evidence_data}
elif isinstance(evidence_data, dict):
    evidence_map = evidence_data
else:
    raise ValueError("release_evidences.json 格式不支持")

# 读取 condition JSON 数据
with open(condition_file, 'r', encoding='utf-8') as f:
    condition_data = json.load(f)

if isinstance(condition_data, list):
    condition_map = {item['id']: item for item in condition_data}
elif isinstance(condition_data, dict):
    condition_map = condition_data
else:
    raise ValueError("release_conditions.json 格式不支持")

# 处理前200个病人
for i in range(min(200, len(train_df))):
    row = train_df.iloc[i]

    # 处理 evidences 字段
    try:
        evidence_ids_raw = ast.literal_eval(row['EVIDENCES']) if pd.notna(row['EVIDENCES']) else []
    except Exception:
        evidence_ids_raw = []

    # 提取真实 evidence ID（去除 _@_ 后面的 value）
    evidence_ids = [eid.split('_@_')[0] for eid in evidence_ids_raw if isinstance(eid, str)]

    # 获取详细的 evidence 信息
    evidence_details = [evidence_map[eid] for eid in evidence_ids if eid in evidence_map]

    # 处理条件信息（使用 PATHOLOGY 字段）
    condition_name = row['PATHOLOGY']
    condition_details = [condition_map[condition_name]] if condition_name in condition_map else []

    # 构建结果
    patient_info = row.to_dict()

    result = {
        'patient_info': patient_info,
        'evidence_details': evidence_details,
        'condition_details': condition_details
    }

    # 保存文件
    filename = f'participant_{i}.json'
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"已保存：{filename}")
